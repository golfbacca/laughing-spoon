# -*- coding: utf-8 -*-
"""
和風レトロ塗り絵のレビュー収集

    python3 tools/collect_reviews.py --source amazon --provider scraperapi --dump-raw
    python3 tools/collect_reviews.py --source goodreads --dump-raw
    python3 tools/collect_reviews.py --report

取得 -> 正規化 -> 絞り込み(review_filter) -> JSONL + レポート の順で流れる。

■ 検証状況
  Goodreads（fetch_goodreads / parse_goodreads）は 2026-08-05 に実物のHTMLで
  検証済み。本文の在り処は __NEXT_DATA__ の Apollo キャッシュ。詳細は
  parse_goodreads の docstring と docs/レビュー収集_実行手順.md §4 を参照。
  ただし対象15商品は Goodreads 側のレビューが全て0件で、収穫はゼロ。

  Amazon 側（fetch_amazon / parse_amazon）は依然 **未検証**。各API のレスポンスを
  一度も見ていないため、「こう返るはず」という前提で書いてある。
  初回は必ず --dump-raw を付けて実行し、data/raw/ に落ちた実物を見て
  parse_amazon だけを直すこと。直す範囲が parse_* の中だけで済むように、
  取得・正規化・絞り込み・出力を分離してある。

■ 取れる件数の上限（2026-08 時点）
  Amazon は2024年11月にレビューをログインウォール内へ移し、2026年5月に
  商品ページHTMLから本文を削除した。ログアウト状態で取れるのは
  「注目のレビュー」8〜13件程度と星の分布のみ。星別フィルタは使えない。
  詳細は docs/Amazon和風レトロ塗り絵_調査メモ.md を参照。
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_filter import keep  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS = os.path.join(ROOT, "tools", "products.json")
DATA = os.path.join(ROOT, "data")
RAW = os.path.join(DATA, "raw")
OUT_JSONL = os.path.join(DATA, "reviews.jsonl")
REPORT = os.path.join(ROOT, "docs", "レビュー分析.md")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")


# ===========================================================================
# 取得層
# ===========================================================================

def _get(url, headers=None, data=None, timeout=60):
    req = urllib.request.Request(url, data=data, headers=headers or {"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def fetch_amazon(asin, provider, api_key):
    """
    Amazon のレビューを、指定プロバイダ経由で取る。生レスポンス文字列を返す。

    各社のリクエスト形式は公式ドキュメントを確認できていないため未検証。
    401/404 が出たら、まずここのURL・パラメータ名を疑うこと。
    """
    if provider == "scraperapi":
        q = urllib.parse.urlencode({"api_key": api_key, "asin": asin, "country": "us"})
        return _get(f"https://api.scraperapi.com/structured/amazon/review?{q}")

    if provider == "rainforest":
        q = urllib.parse.urlencode({
            "api_key": api_key, "type": "reviews",
            "amazon_domain": "amazon.com", "asin": asin,
        })
        return _get(f"https://api.rainforestapi.com/request?{q}")

    if provider == "oxylabs":
        # OXYLABS_AUTH="user:pass" を環境変数で渡す
        import base64
        auth = base64.b64encode(os.environ["OXYLABS_AUTH"].encode()).decode()
        payload = json.dumps({
            "source": "amazon_reviews", "query": asin,
            "domain": "com", "parse": True,
        }).encode()
        return _get(
            "https://realtime.oxylabs.io/v1/queries",
            headers={"Authorization": f"Basic {auth}",
                     "Content-Type": "application/json"},
            data=payload,
        )

    raise ValueError(f"不明なプロバイダ: {provider}")


def fetch_goodreads(isbn):
    """
    Goodreads の書籍ページHTMLを取る。有料APIは不要。

    /book/isbn/<isbn> は書籍ページへリダイレクトする。
    公式APIは2020年12月に廃止済みなのでHTMLを読むしかない。
    979-8 始まり（KDP）の収録は歯抜けなので、404 は普通に起きる。
    """
    return _get(f"https://www.goodreads.com/book/isbn/{isbn}")


# ===========================================================================
# 正規化層（★実物を見て直す場所はここだけ）
# ===========================================================================

def parse_amazon(raw, provider, product):
    """生レスポンス -> レビュー dict のリスト。"""
    doc = json.loads(raw)

    if provider == "scraperapi":
        items = doc.get("reviews", [])
        get = lambda d, *k: next((d[x] for x in k if d.get(x) is not None), None)
        return [{
            "source": "amazon",
            "product_id": product["asin"],
            "title": product["title"],
            "star": _to_star(get(r, "stars", "rating")),
            "date": get(r, "date"),
            "review_title": get(r, "title"),
            "body": get(r, "review", "body", "text") or "",
        } for r in items]

    if provider == "rainforest":
        return [{
            "source": "amazon",
            "product_id": product["asin"],
            "title": product["title"],
            "star": _to_star(r.get("rating")),
            "date": (r.get("date") or {}).get("raw"),
            "review_title": r.get("title"),
            "body": r.get("body") or "",
        } for r in doc.get("reviews", [])]

    if provider == "oxylabs":
        out = []
        for res in doc.get("results", []):
            content = res.get("content", {})
            for r in content.get("reviews", []):
                out.append({
                    "source": "amazon",
                    "product_id": product["asin"],
                    "title": product["title"],
                    "star": _to_star(r.get("rating")),
                    "date": r.get("timestamp"),
                    "review_title": r.get("title"),
                    "body": r.get("content") or r.get("text") or "",
                })
        return out

    raise ValueError(provider)


_NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.S
)


def parse_goodreads(raw, product):
    """
    Goodreads のHTML -> レビュー dict のリスト。

    ■ 本文の在り処（2026-08 に実物のHTMLで確認）

      `application/ld+json` は **外れ**。@type=Book が1つあるだけで、
      入っているのは name / isbn / author / aggregateRating（平均と件数）まで。
      schema.org の review プロパティは無く、本文は1文字も無い。

      当たりは `__NEXT_DATA__`（Next.js のSSRペイロード）。この中の
      Apollo キャッシュにレビュー本体が正規化された形で入っている:

        props.pageProps.apolloState
          ├ "ROOT_QUERY"
          │    └ "getReviews" -> {totalCount, edges:[{node:{__ref:"Review:..."}}]}
          └ "Review:kca://review:goodreads/..." -> 本体
               rating        1〜5 の int（未評価は null）
               text          本文。プレーンテキストではなくHTML断片
               createdAt     エポックミリ秒
               spoilerStatus bool
               creator       {"__ref": "User:..."} で User エントリを指す

      edges は初期表示分だけで、1商品あたり最大30件。続きは
      クライアント側の GraphQL 追加リクエストなので、HTML からは取れない。
      ただし本件の対象商品はレビューが片手で足りる規模なので実害は無い。

      `text` は <br /> <b> <i> <a> <blockquote> <img> と HTML エンティティを
      含むので、素通ししてはいけない。review_filter は改行も文の区切りとして
      扱うため、<br /> は改行に落とすのが正しい。

    ■ レビュー0件のとき
      ROOT_QUERY に "getReviews" キー自体が生えない（Review: エントリも0）。
      これは異常ではないので、例外にせず空リストを返す。

    ■ product_id には ISBN ではなく ASIN を入れる
      レポートは商品単位で集計する。Amazon 側と同じキーにしておかないと
      同じ商品が出所ごとに別商品として2つ並ぶ。出所は "source" で区別できる。
    """
    m = _NEXT_DATA_RE.search(raw or "")
    if not m:
        # 空レスポンスや、レビューを含まない別レイアウトへ飛ばされた場合。
        # ld+json には本文が無いので、ここから救う手立ては無い。
        raise ValueError(
            "__NEXT_DATA__ が無い（応答 %d 文字）。"
            "ISBN が Goodreads に無い（979-8 の KDP 発行は歯抜け）か、"
            "取得がブロックされた可能性がある。" % len(raw or "")
        )

    state = json.loads(m.group(1)).get("props", {}).get("pageProps", {}).get("apolloState")
    if not isinstance(state, dict):
        raise ValueError("__NEXT_DATA__ に apolloState が無い。Goodreads 側の構造変更を疑う。")

    # 表示順を保つため、まず getReviews の edges をたどる。
    # キーが無い＝レビュー0件。取りこぼしの保険として Review: エントリも拾う。
    refs = []
    for key, val in state.get("ROOT_QUERY", {}).items():
        if key == "getReviews" or key.startswith("getReviews("):
            for edge in (val or {}).get("edges", []):
                ref = (edge.get("node") or {}).get("__ref")
                if ref:
                    refs.append(ref)
    for key in state:
        if key.startswith("Review:") and key not in refs:
            refs.append(key)

    out = []
    for ref in refs:
        r = state.get(ref)
        if not isinstance(r, dict):
            continue
        body = _html_to_text(r.get("text"))
        if not body:
            continue  # 星だけ付けて本文が無いレビュー
        out.append({
            "source": "goodreads",
            "product_id": product["asin"],
            "title": product["title"],
            "star": _to_star(r.get("rating")),
            "date": _epoch_ms_to_date(r.get("createdAt")),
            "review_title": None,  # Goodreads のレビューに表題は無い
            "body": body,
        })
    return out


def _html_to_text(fragment):
    """Goodreads の text（HTML断片）を、文単位で読める素のテキストにする。"""
    if not fragment:
        return ""
    s = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", fragment)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</?(p|div|blockquote|li)\b[^>]*>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)          # 残る <b> <i> <a> <img> などを落とす
    s = html.unescape(s)                   # &amp; &quot; &#39; を戻す
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def _epoch_ms_to_date(v):
    """createdAt（エポックミリ秒）を 'YYYY-MM-DD' にする。"""
    if not isinstance(v, (int, float)):
        return None
    return time.strftime("%Y-%m-%d", time.gmtime(v / 1000))


def _to_star(v):
    """'4.0 out of 5 stars' / 4.0 / '4' のどれでも int にする。"""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return int(round(v))
    m = re.search(r"\d+(\.\d+)?", str(v))
    return int(round(float(m.group(0)))) if m else None


# ===========================================================================
# 実行
# ===========================================================================

def load_products():
    with open(PRODUCTS, encoding="utf-8") as f:
        return json.load(f)["products"]


def collect(source, provider, api_key, dump_raw, limit, stars):
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(DATA, exist_ok=True)
    products = load_products()[:limit] if limit else load_products()

    kept, seen, failed = [], 0, []
    for i, p in enumerate(products, 1):
        ident = p["asin"] if source == "amazon" else p["isbn"]
        print(f"[{i}/{len(products)}] {source} {ident} {p['title'][:44]}")
        try:
            if source == "amazon":
                raw = fetch_amazon(p["asin"], provider, api_key)
                name = f"amazon_{provider}_{p['asin']}.json"
            else:
                raw = fetch_goodreads(p["isbn"])
                name = f"goodreads_{p['isbn']}.html"

            if dump_raw:
                with open(os.path.join(RAW, name), "w", encoding="utf-8") as f:
                    f.write(raw)

            reviews = (parse_amazon(raw, provider, p) if source == "amazon"
                       else parse_goodreads(raw, p))
        except Exception as e:
            print(f"    -> 失敗: {type(e).__name__}: {e}")
            failed.append((ident, f"{type(e).__name__}: {e}"))
            continue

        seen += len(reviews)
        for r in reviews:
            ok, analysis = keep(r, stars=stars)
            if ok:
                r["analysis"] = analysis
                kept.append(r)
        print(f"    -> 取得 {len(reviews)} 件 / 採用 {len(kept)} 件（累計）")
        time.sleep(1)

    with open(OUT_JSONL, "w", encoding="utf-8") as f:
        for r in kept:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\n取得 {seen} 件 -> 星{'・'.join(map(str, stars))}かつ中身への言及あり {len(kept)} 件")
    print(f"書き出し: {OUT_JSONL}")
    if failed:
        print(f"\n失敗 {len(failed)} 件:")
        for ident, why in failed:
            print(f"  {ident}: {why}")
    return kept


def build_report():
    """reviews.jsonl から docs/レビュー分析.md を組む。"""
    if not os.path.exists(OUT_JSONL):
        print(f"{OUT_JSONL} がない。先に収集すること。")
        return 1

    rows = [json.loads(l) for l in open(OUT_JSONL, encoding="utf-8")]
    by_product, flags = {}, {}
    for r in rows:
        by_product.setdefault((r["product_id"], r["title"]), []).append(r)
        for cat in r.get("analysis", {}).get("red_flags", {}):
            flags[cat] = flags.get(cat, 0) + 1

    L = ["# 和風レトロ塗り絵 レビュー分析", "",
         f"対象 {len(by_product)} 商品 / 採用 {len(rows)} 件", "",
         "中身（イラスト・線画）に言及した文だけを抜き出している。",
         "紙質・製本・配送・価格のみのレビューは除外済み。", ""]

    if flags:
        L += ["## 星1で多い不満（地雷語の検出数）", "",
              "| 分類 | 件数 |", "|---|---|"]
        for cat, n in sorted(flags.items(), key=lambda x: -x[1]):
            L.append(f"| {cat} | {n} |")
        L.append("")

    L += ["## 商品別", ""]
    for (pid, title), revs in sorted(by_product.items()):
        five = [r for r in revs if r["star"] == 5]
        one = [r for r in revs if r["star"] == 1]
        L += [f"### {title}", "",
              f"`{pid}` — 星5 {len(five)}件 / 星1 {len(one)}件", ""]
        for label, group in (("星5", five), ("星1", one)):
            if not group:
                continue
            L.append(f"**{label}**")
            L.append("")
            for r in group:
                for s in r["analysis"]["sentences"]:
                    note = " ※紙の話と同居" if s["with_physical"] else ""
                    L.append(f"- {s['text']}{note}")
            L.append("")

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"書き出し: {REPORT}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="和風レトロ塗り絵のレビュー収集")
    ap.add_argument("--source", choices=["amazon", "goodreads"])
    ap.add_argument("--provider", choices=["scraperapi", "rainforest", "oxylabs"],
                    default="scraperapi", help="Amazon取得に使うAPI")
    ap.add_argument("--api-key", default=os.environ.get("REVIEW_API_KEY"),
                    help="既定は環境変数 REVIEW_API_KEY")
    ap.add_argument("--dump-raw", action="store_true",
                    help="生レスポンスを data/raw/ に残す（初回は必ず付ける）")
    ap.add_argument("--limit", type=int, help="先頭N商品だけ試す")
    ap.add_argument("--stars", default="1,5", help="採用する星。既定 1,5")
    ap.add_argument("--report", action="store_true", help="収集済みJSONLからレポートを組む")
    a = ap.parse_args()

    if a.report:
        return build_report()
    if not a.source:
        ap.error("--source か --report のどちらかが要る")
    if a.source == "amazon" and a.provider != "oxylabs" and not a.api_key:
        ap.error("--api-key か環境変数 REVIEW_API_KEY が要る")

    stars = tuple(int(s) for s in a.stars.split(","))
    collect(a.source, a.provider, a.api_key, a.dump_raw, a.limit, stars)
    return 0


if __name__ == "__main__":
    sys.exit(main())
