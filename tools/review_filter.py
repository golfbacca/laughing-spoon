# -*- coding: utf-8 -*-
"""
レビュー絞り込みロジック

依頼の核心：「紙の質感とか配慮ではなく、中身のイラスト・線画に言及したもの」だけを残す。

ネットワークを一切使わないので、取得元（Amazon / Goodreads）が決まる前でも
単体でテストできる。test_review_filter.py を参照。

判定は文単位。レビュー全体を残すか捨てるかではなく、
「中身に言及している文」を抜き出す。1件のレビューに
「紙が薄い。でも絵柄は素晴らしい」が混在するのが普通のため。
"""
import re

# ---------------------------------------------------------------------------
# 一次語：これが出たら「中身への言及」と判定する。
# 画そのもの・線・構図・密度に関する語だけを入れる。
# ---------------------------------------------------------------------------
PRIMARY = [
    # 絵そのもの
    r"illustrat\w*", r"drawing\w*", r"artwork", r"art\s?work", r"the art\b",
    r"art\s?style", r"image\w*", r"picture\w*", r"design\w*", r"scene\w*",
    r"sketch\w*", r"graphic\w*", r"render\w*",
    # 線
    r"line\s?art", r"line\s?work", r"linework", r"outline\w*",
    r"\blines?\b", r"stroke\w*", r"contour\w*",
    # 密度・構図
    r"intricate", r"detailed", r"\bdetails?\b", r"complex\w*", r"\bbusy\b",
    r"simplistic", r"\bsimple\b", r"composition\w*", r"\bspacing\b",
    r"white\s?space", r"open\s?space\w*", r"small\s?space\w*",
    r"tiny\s?space\w*", r"large\s?space\w*",
    # 題材の扱い（描かれているものへの評価）
    r"subject\s?matter", r"variety", r"repetiti\w*", r"duplicat\w*",
]

# ---------------------------------------------------------------------------
# 物理語：紙・製本・配送・価格。これ「だけ」の文は落とす。
# 一次語と同居する文は残す（「紙は薄いが線は綺麗」を捨てないため）。
# ---------------------------------------------------------------------------
PHYSICAL = [
    r"\bpaper\b", r"bleed\s?through", r"bleedthrough", r"\bbleeds?\b",
    r"ghost\w*", r"\bmarkers?\b", r"gel\s?pens?", r"\bink\b",
    r"binding", r"\bspine\b", r"glued?", r"perforat\w*", r"tear\s?out",
    r"single[\s-]?sided", r"double[\s-]?sided", r"back\s?of\s?the\s?page",
    r"shipping", r"arrived", r"deliver\w*", r"packag\w*", r"\bdamaged?\b",
    r"\bprice[ds]?\b", r"expensive", r"\brefund\w*", r"\bseller\b",
    r"\bkindle\b", r"paperback", r"\bbook\s?size\b",
]

# ---------------------------------------------------------------------------
# 地雷語：星1で頻出する、KDP塗り絵特有の致命的な不満。
# 自作するうえで一番読む価値があるのはここなので、別枠で集計する。
# ---------------------------------------------------------------------------
RED_FLAGS = {
    "AI生成疑い": [
        r"\bA\.?I\.?\b", r"ai[\s-]?generated", r"ai\s?art",
        r"computer[\s-]?generated", r"machine[\s-]?generated",
    ],
    "トレース・流用疑い": [
        r"trac(ed|ing)", r"clip\s?art", r"clipart", r"stock\s?(image|photo)",
        r"copy[\s-]?paste", r"public\s?domain",
    ],
    "使い回し": [
        r"same\s+(image|picture|drawing|page)", r"repeat\w*",
        r"duplicat\w*", r"over\s?and\s?over",
    ],
    "画質不良": [
        r"low[\s-]?res\w*", r"pixelat\w*", r"blurr?y", r"fuzzy",
        r"jagged", r"grainy", r"watermark\w*", r"\bartifacts?\b",
    ],
    "線が塗れない": [
        r"too\s?(thin|fine|small)", r"hard\s?to\s?(see|color)",
        r"can'?t\s?color", r"too\s?dark", r"solid\s?black",
    ],
    "題材が的外れ": [
        r"not\s?(really\s?)?japanese", r"doesn'?t\s?look\s?japanese",
        r"nothing\s?to\s?do\s?with", r"generic", r"\bchinese\b",
    ],
}

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")


def _compile(patterns):
    return [re.compile(p, re.IGNORECASE) for p in patterns]


_PRIMARY_RE = _compile(PRIMARY)
_PHYSICAL_RE = _compile(PHYSICAL)
_RED_RE = {k: _compile(v) for k, v in RED_FLAGS.items()}


def split_sentences(text):
    """レビュー本文を文に割る。ピリオドを打たない書き手が多いので改行でも割る。"""
    if not text:
        return []
    return [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]


def _hits(regexes, text):
    found = []
    for r in regexes:
        m = r.search(text)
        if m:
            found.append(m.group(0).lower())
    return sorted(set(found))


def red_flags(text):
    """本文全体にかかる地雷語を、カテゴリ名 -> 該当語 で返す。"""
    out = {}
    for name, regexes in _RED_RE.items():
        h = _hits(regexes, text or "")
        if h:
            out[name] = h
    return out


def analyze(text):
    """
    本文を解析して、中身に言及している文だけを抜き出す。

    戻り値:
        {
          "is_content": bool,          # 中身への言及が1文でもあるか
          "sentences": [               # 中身に言及している文だけ
             {"text": str, "terms": [str], "with_physical": bool},
          ],
          "red_flags": {カテゴリ: [語]},
          "physical_only": bool,       # 物理語のみで中身の言及がない
        }
    """
    sentences = split_sentences(text)
    picked = []
    saw_physical = False

    for s in sentences:
        prim = _hits(_PRIMARY_RE, s)
        phys = _hits(_PHYSICAL_RE, s)
        if phys:
            saw_physical = True
        if prim:
            picked.append({
                "text": s,
                "terms": prim,
                "with_physical": bool(phys),
            })

    return {
        "is_content": bool(picked),
        "sentences": picked,
        "red_flags": red_flags(text),
        "physical_only": (not picked) and saw_physical,
    }


def keep(review, stars=(1, 5)):
    """
    1件のレビューを採用するか判定する。

    review は少なくとも "star"(int) と "body"(str) を持つ dict。
    既定では星5と星1のみを対象にする（依頼の指定）。
    """
    if review.get("star") not in stars:
        return False, None
    result = analyze(review.get("body", ""))
    return result["is_content"], result
