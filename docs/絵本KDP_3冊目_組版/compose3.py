#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3冊目の本文テキストを画像に載せて、完成ページを書き出す。

1冊目・2冊目と同じ構造。PAGES だけ差し替えてある。
使い方:  python3 compose3.py
出力:    docs/絵本KDP_3冊目_完成ページ/ に 4096x4096 の JPG
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT  = pathlib.Path(__file__).resolve().parents[2]
SRC   = ROOT / "docs" / "絵本KDP_3冊目_画像"
OUT   = ROOT / "docs" / "絵本KDP_3冊目_完成ページ"
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

# ---- 本文（docs/絵本KDP_3冊目_本文テキスト.txt と同じ内容を保持）----
PAGES = [
 ("S01_ねるまえ",          "top",    ["ねる まえ。",
                                     "ミオちゃんが ふとんに はいる。",
                                     "まくらもとに ちいさな あかり。"]),
 ("02_場面01_めがさめる",   "bottom", ["よなかに めが さめた。",
                                     "へやが くらい。"]),
 ("03_場面02_むずむず",     "top",    ["おなかの したの ほうが",
                                     "むずむず する。"]),
 ("S04_ふとんのふち",       "bottom", ["いかなきゃ。",
                                     "ミオちゃんは ふとんの ふちを にぎった。"]),
 ("04_場面03_でられない",   "bottom", ["でも、くらい。",
                                     "ふとんから でられない。",
                                     "トトンが リュックの ひもを ぎゅっと にぎる。"]),
 ("05_場面04_ここにある",   "bottom", ["トトンが まくらもとを みた。",
                                     "「ここに ある」"]),
 ("06_場面05_てをのばす",   "top",    ["ミオちゃんが てを のばした。",
                                     "ゆびが あかりに とどいた。"]),
 ("07_場面06_ついた",       "top",    ["カチッ。",
                                     "つけた。",
                                     "あかりが ついた。"]),
 ("S09_じぶんでついた",     "bottom", ["トトンの みみが ぴくっと うごいた。",
                                     "「じぶんで ついた」"]),
 ("08_場面07_ふとんからでる","top",   ["ふとんから でる。",
                                     "ゆかは つめたい。"]),
 ("09_場面08_ろうか",       "top",    ["あかりを もって、ろうかを あるく。",
                                     "まえが すこし みえる。"]),
 ("S13_トイレのドア",       "top",    ["トイレの ドア。",
                                     "ノブに てを かける。"]),
 ("10_場面09_トイレのなか", "top",    ["ドアを しめる。",
                                     "パンツを おろす。",
                                     "よいしょ と すわる。",
                                     "あかりは ドアの したから もれて いる。"]),
 ("11_場面10_おわりのおと", "top",    ["ジャーッ。",
                                     "よるの おとは おおきい。",
                                     "でも、おわりの おと。"]),
 ("S14_てをあらう",         "bottom", ["てを あらう。",
                                     "みずも つめたい。"]),
 ("12_場面11_もどる",       "top",    ["あかりを もって、ふとんに もどる。",
                                     "ろうかは もう ながく ない。"]),
 ("13_場面12_またねる",     "top",    ["ふとんに もぐる。",
                                     "あかりを けす。",
                                     "ミオちゃんは また ねむった。"]),
 ("S18_つぎのよる",         "bottom", ["つぎの よる。",
                                     "ミオちゃんが じぶんで あかりに てを のばした。",
                                     "「つぎの よるも つけられる」"]),
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
