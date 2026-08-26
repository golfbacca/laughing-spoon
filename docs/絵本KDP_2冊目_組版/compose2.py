#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2冊目の本文テキストを画像に載せて、完成ページを書き出す。

1冊目の compose.py と同じ構造。PAGES だけ差し替えてある（引き継ぎ書2章）。
使い方:  python3 compose2.py
出力:    docs/絵本KDP_2冊目_完成ページ/ に 4096x4096 の JPG
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT  = pathlib.Path(__file__).resolve().parents[2]
SRC   = ROOT / "docs" / "絵本KDP_2冊目_画像"
OUT   = ROOT / "docs" / "絵本KDP_2冊目_完成ページ"
FONTS = ROOT / "docs" / "絵本KDP_組版" / "fonts"      # 1冊目と同じ書体を使う

FONT_BODY = FONTS / "ZenMaruGothic-Medium.ttf"
FONT_SUB  = FONTS / "ZenMaruGothic-Bold.ttf"
INK       = (74, 55, 45)
INK_SOFT  = (110, 90, 78)
BODY_PT   = 150
LINE_GAP  = 1.55
MARGIN_X  = 320
BAND_PAD  = 150

def font(path, size): return ImageFont.truetype(str(path), size)

def draw_lines(im, lines, where, size=BODY_PT, fnt=None, fill=INK,
               align="left", gap=LINE_GAP, x_off=0, y_off=0):
    d = ImageDraw.Draw(im)
    f = font(fnt or FONT_BODY, size)
    lh = int(size * gap)
    block_h = lh * len(lines)
    y = BAND_PAD + y_off if where == "top" else im.height - BAND_PAD - block_h + y_off
    for ln in lines:
        x = (im.width - d.textlength(ln, font=f)) / 2 + x_off if align == "center" \
            else MARGIN_X + x_off
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return im

# ---- 本文（docs/絵本KDP_2冊目_本文テキスト.txt と同じ内容を保持）----
PAGES = [
 ("S01_あさ",             "top",    ["きょうは とくべつな あさ。",
                                     "ミオちゃんが おきて きた。",
                                     "トトンは たなの したで まって いる。"]),
 ("02_場面01_ふくろ",      "bottom", ["たなの うえに、あたらしい ふくろ。",
                                     "きのう おみせで かって きた ふくろ。"]),
 ("03_場面02_あける",      "top",    ["ふくろを あける。",
                                     "なかから パンツが でてきた。"]),
 ("S04_ならべる",          "bottom", ["ゆかに ならべる。",
                                     "3まい ならんだ。"]),
 ("04_場面03_おむつがいい", "bottom", ["ミオちゃんは いっぽ さがった。",
                                     "「おむつが いい」"]),
 ("05_場面04_だきしめる",   "bottom", ["おむつを むねに だいた。",
                                     "トトンが リュックの ひもを ぎゅっと にぎる。"]),
 ("06_場面05_どれにする",   "top",    ["トトンが パンツを ひろげた。",
                                     "「どれに する」"]),
 ("07_場面06_えらんだ",     "top",    ["ミオちゃんが てを のばした。",
                                     "きいろの パンツを とった。",
                                     "えらんだ。"]),
 ("S09_すわる",            "bottom", ["ゆかに すわる。",
                                     "トトンが よこに くる。"]),
 ("08_場面07_おむつをぬぐ", "top",    ["おむつを ぬぐ。",
                                     "まるめて、ごみばこに いれる。",
                                     "トトンは パンツを もって まって いる。"]),
 ("09_場面08_かたあし",     "top",    ["かたほうの あしを いれる。",
                                     "ぐらぐら する。"]),
 ("S13_かべにて",          "top",    ["かべに てを ついた。",
                                     "もう ぐらぐら しない。"]),
 ("10_場面09_もういっぽう", "top",    ["もういっぽうの あしを いれる。",
                                     "ゆっくりで いい。"]),
 ("11_場面10_ひっぱる",     "top",    ["りょうてで もって、",
                                     "きゅっと ひっぱりあげる。"]),
 ("S14_みおろす",          "bottom", ["ミオちゃんが したを みた。",
                                     "きいろが みえる。"]),
 ("12_場面11_はけた",       "top",    ["じぶんで はけた。",
                                     "トトンの みみが ぴくっと うごいた。",
                                     "「じぶんで はけた」"]),
 ("13_場面12_おでかけ",     "top",    ["ベージュの ズボンを はいて、",
                                     "あかい くつを はく。",
                                     "きょうは こうえんへ いく ひ。"]),
 ("S18_つぎのあさ",        "bottom", ["つぎの あさ。",
                                     "ミオちゃんが じぶんで ふくろに てを のばした。",
                                     "「きょうも えらべる」"]),
]

def main():
    OUT.mkdir(exist_ok=True)
    for entry in PAGES:
        stem, where, lines = entry[0], entry[1], entry[2]
        opt = entry[3] if len(entry) > 3 else {}
        im = Image.open(SRC / f"{stem}.jpg").convert("RGB")
        size = BODY_PT if max(len(l) for l in lines) <= 26 else int(BODY_PT * 0.86)
        size = int(size * opt.get("scale", 1.0))
        draw_lines(im, lines, where, size=size,
                   x_off=int(im.width * opt.get("x", 0.0)),
                   y_off=int(im.height * opt.get("y", 0.0)))
        im.save(OUT / f"{stem}.jpg", quality=93, dpi=(300, 300))
        print("本文", stem)

if __name__ == "__main__":
    main()
