"""参考写真をウィキメディア・コモンズから探して落とす（実物の形を知るための参考用。なぞらない・本に載せない）。
使い方: python3 tools/ref_photo.py "Himeji Castle" 保存先フォルダ [枚数]
- 保存先はリポジトリの外（スクラッチパッド）にすること。写真には撮影者の権利がある
- 通信は curl で、環境の許可リストにある commons.wikimedia.org（検索）と upload.wikimedia.org（元ファイル）だけ
- 写真は縮小版（幅500・thumb.wikimedia.org）を落とす。元ファイルを続けて落とすとサイト側に断られる
- .claude/settings.json に、この2つのホスト宛ての curl を許すルールがある（2026-11-23 本人了承）"""
import sys, os, json, subprocess, urllib.parse
from PIL import Image


def curl(url, out=None):
    # 名乗りは正直に（ブラウザのふりをしない）。名乗らないと「要求が多すぎる」と断られやすい。個人情報は入れない
    cmd = ["curl", "-sS", "-L", "-m", "60", "-A", "nonogram-ref-photo/0.1 (hobby puzzle book; reference lookup)"] + (["-o", out] if out else []) + [url]
    return subprocess.run(cmd, capture_output=True, text=not out).stdout


def search(query, n=4):
    q = urllib.parse.urlencode({"action": "query", "generator": "search", "gsrsearch": query + " filetype:bitmap",
                                "gsrnamespace": 6, "gsrlimit": n, "prop": "imageinfo",
                                "iiprop": "url|size|extmetadata", "iiurlwidth": 500, "format": "json"})
    import time
    for attempt in range(3):                      # たまに空の応答が返るので、少し待って取り直す
        txt = curl("https://commons.wikimedia.org/w/api.php?" + q)
        if txt.strip().startswith("{"):
            break
        time.sleep(15)
    else:
        sys.exit("検索の応答が空でした: " + repr(txt[:200]))
    data = json.loads(txt)
    pages = sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0))
    out = []
    for p in pages:
        ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
        # 縮小版（幅500）を使う。元ファイルを続けて落とすと「負荷が高い」と断られた（429）
        out.append({"title": p["title"], "url": (ii.get("thumburl") or ii["url"]).split("?")[0], "size": 0,
                    "license": m.get("LicenseShortName", {}).get("value", "?")})
    return out


if __name__ == "__main__":
    query, folder = sys.argv[1], sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    os.makedirs(folder, exist_ok=True)
    for i, r in enumerate(search(query, n)):
        if r["size"] > 12_000_000:
            print(i, "大きすぎるので飛ばす", r["size"], r["title"]); continue
        raw = os.path.join(folder, f"{i}_raw")
        curl(r["url"], raw)
        try:
            im = Image.open(raw).convert("RGB"); im.thumbnail((600, 600)); im.save(os.path.join(folder, f"{i}.jpg")); os.remove(raw)
            print(i, im.size, r["license"], r["title"])
        except Exception as e:
            print(i, "画像として開けない", e, r["title"])
