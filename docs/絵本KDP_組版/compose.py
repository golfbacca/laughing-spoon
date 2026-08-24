#!/usr/bin/env python3
"""絵本の本文テキストを画像に載せて、完成ページを書き出す。

使い方:  python3 compose.py
出力:    docs/絵本KDP_完成ページ/  に 4096x4096 の JPG（本文）と
         表紙・裏表紙（2:3）を書き出す。
文字の色・サイズ・位置はすべてこのファイル上部の設定で変えられる。
"""
import pathlib, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT  = pathlib.Path(__file__).resolve().parents[2]
SRC   = ROOT / "docs" / "絵本KDP_画像"
OUT   = ROOT / "docs" / "絵本KDP_完成ページ"
FONTS = ROOT / "docs" / "絵本KDP_組版" / "fonts"

# ---- 見た目の設定（ここだけ触れば調整できる）--------------------
FONT_BODY   = FONTS / "ZenMaruGothic-Medium.ttf"   # 本文
FONT_SUB    = FONTS / "ZenMaruGothic-Bold.ttf"     # 表紙サブタイトル・裏表紙見出し
INK         = (74, 55, 45)      # 文字色：黒でなく濃い茶。絵に馴染む
INK_SOFT    = (110, 90, 78)     # 補助テキスト（裏表紙の箇条書き）
BODY_PT     = 150               # 本文の文字サイズ（4096px幅に対して）
LINE_GAP    = 1.55              # 行送り（文字サイズ比）
MARGIN_X    = 320               # 左右の余白
BAND_PAD    = 150               # 帯の内側の上下余白
SUB_Y       = 0.258             # 表紙サブタイトルの上端（画像高さ比）
# -----------------------------------------------------------------

def font(path, size): return ImageFont.truetype(str(path), size)

def draw_lines(im, lines, where, size=BODY_PT, fnt=None, fill=INK,
               align="left", gap=LINE_GAP, x_off=0, y_off=0):
    """where: 'top' か 'bottom'。指定した帯の中に行を積む。"""
    d = ImageDraw.Draw(im)
    f = font(fnt or FONT_BODY, size)
    lh = int(size * gap)
    block_h = lh * len(lines)
    if where == "top":
        y = BAND_PAD + y_off
    else:
        y = im.height - BAND_PAD - block_h + y_off
    for ln in lines:
        if align == "center":
            w = d.textlength(ln, font=f)
            x = (im.width - w) / 2 + x_off
        else:
            x = MARGIN_X + x_off
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return im

# ---- 本文（docs/絵本KDP_本文テキスト.txt と同じ内容を保持）-------
PAGES = [
 ("S01_いえをでる",         "top",    ["きょうは こうえんへ いく ひ。",
                                      "ミオちゃんが くつを はく。",
                                      "トトンは リュックの よこで まって いる。"]),
 ("02_場面01_バス",         "bottom", ["バスに のって、こうえんへ。",
                                      "ミオちゃんの となりに トトンが すわって いる。"]),
 ("03_場面02_公園であそぶ",  "top",    ["すべりだいも ブランコも たのしい。",
                                      "トトンも いっしょに はしる。"]),
 ("S04_きづく",            "bottom", ["あれ。",
                                      "ミオちゃんの あしが とまった。"]),
 ("04_場面03_もじもじ",      "bottom", ["おなかの したの ほうが",
                                      "むずむず する。"]),
 ("05_場面04_言えない",      "bottom", ["でも、まだ あそびたい。",
                                      "ミオちゃんは なにも いわなかった。",
                                      "トトンが リュックの ひもを ぎゅっと にぎる。"]),
 ("06_場面05_いまいこう",    "top",    ["トトンが ちいさな こえで いった。",
                                      "「いま、いこう」"]),
 ("07_場面06_言えた",        "top",    ["ミオちゃんは かおを あげた。",
                                      "「トイレ、いきたい」",
                                      "いえた。"]),
 ("S09_トイレがみえる",      "bottom", ["こうえんの トイレが みえてきた。"]),
 ("08_場面07_知らないドア",  "bottom", ["しらない ドア。",
                                      "なかは すこし くらい。"]),
 ("09_場面08_ノック",        "top",    ["トトンが せのびして",
                                      "ドアを たたく。",
                                      "トン、トン。",
                                      "だれも いない。はいって いいよ。"],
                                     {"scale": 0.76, "x": 0.40, "y": 0.0}),
 ("10_場面09_トイレの中",    "top",    ["ドアを しめる。",
                                      "パンツを おろす。",
                                      "よいしょ と すわる。",
                                      "あしが とどかない ときは、だいに のせる。"]),
 ("S13_ドアがあく",         "top",    ["ドアが あいた。",
                                      "ミオちゃんが でてきた。"]),
 ("S14_レバー",            "top",    ["よこの レバーに てを のばす。"]),
 ("11_場面10_おわりの音",    "top",    ["ジャーッ。",
                                      "おおきな おと。",
                                      "「これは おわりの おと」",
                                      "トトンが いった。"]),
 ("12_場面11_手をあらう",    "bottom", ["てを あらう。",
                                      "トトンが リュックから タオルを だす。"]),
 ("13_場面12_公園にもどる",  "top",    ["また はしれる。",
                                      "トトンの みみが ぴくっと うごいた。",
                                      "「つぎも いえるよ」"]),
 ("S18_つぎのおでかけ",      "bottom", ["つぎの おでかけの ひ。",
                                      "ミオちゃんが じぶんから いった。",
                                      "「トイレ、いきたい」"]),
]

def main():
    OUT.mkdir(exist_ok=True)
    for entry in PAGES:
        stem, where, lines = entry[0], entry[1], entry[2]
        opt = entry[3] if len(entry) > 3 else {}
        src = SRC / f"{stem}.jpg"
        im = Image.open(src).convert("RGB")
        size = BODY_PT if max(len(l) for l in lines) <= 26 else int(BODY_PT * 0.86)
        size = int(size * opt.get("scale", 1.0))
        draw_lines(im, lines, where, size=size,
                   x_off=int(im.width * opt.get("x", 0.0)),
                   y_off=int(im.height * opt.get("y", 0.0)))
        im.save(OUT / f"{stem}.jpg", quality=93, dpi=(300, 300))
        print("本文", stem)

    # 表紙：サブタイトルを足す（メインタイトルは絵に描き込み済み）
    for name in ["01_表表紙_2to3", "01_表表紙_Kindle_1600x2560"]:
        im = Image.open(SRC / f"{name}.jpg").convert("RGB")
        s = im.width / 3392          # 2:3原版を基準にした倍率
        d = ImageDraw.Draw(im)
        f = font(FONT_SUB, int(96 * s))
        # 長いので2行に割る。タイトルは絵に描き込み済みなので、その下に置く。
        parts = ["「いま いきたい」が いえるように なる えほん",
                 "2さい 3さい 4さい"]
        y = int(im.height * SUB_Y)   # タイトルの下端より下
        for p in parts:
            w = d.textlength(p, font=f)
            d.text(((im.width - w) / 2, y), p, font=f, fill=INK)
            y += int(96 * s * 1.45)
        im.save(OUT / f"{name}.jpg", quality=95, dpi=(300, 300))
        print("表紙", name)

    # 裏表紙：あらすじ
    im = Image.open(SRC / "14_裏表紙_2to3.jpg").convert("RGB")
    d = ImageDraw.Draw(im)
    fb = font(FONT_SUB, 130); fr = font(FONT_BODY, 118); fs = font(FONT_BODY, 96)
    x = 330; y = int(im.height * 0.40)
    for ln in ["おうちの トイレは できるのに、", "おでかけ さきだと いえない。"]:
        d.text((x, y), ln, font=fr, fill=INK); y += int(118 * 1.55)
    y += 90
    for ln in ["いちばん むずかしいのは", "「がまん」じゃなくて、「いう こと」。"]:
        d.text((x, y), ln, font=fb, fill=INK); y += int(130 * 1.5)
    y += 120
    for ln in ["・たいしょう 2さい 3さい 4さい", "・よみきかせ 3〜4ふん"]:
        d.text((x, y), ln, font=fs, fill=INK_SOFT); y += int(96 * 1.6)
    im.save(OUT / "14_裏表紙_2to3.jpg", quality=95, dpi=(300, 300))
    print("裏表紙")

if __name__ == "__main__":
    main()
