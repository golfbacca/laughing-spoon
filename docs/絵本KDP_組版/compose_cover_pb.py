#!/usr/bin/env python3
"""ペーパーバック（8.5インチ角）用の表紙・裏表紙に文字を載せる。
出力: docs/絵本KDP_完成ページ/ に PB_表表紙_正方形.jpg / PB_裏表紙_正方形.jpg
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT  = pathlib.Path(__file__).resolve().parents[2]
SRC   = ROOT/"docs"/"絵本KDP_画像"
OUT   = ROOT/"docs"/"絵本KDP_完成ページ"; OUT.mkdir(exist_ok=True)
FONTS = ROOT/"docs"/"絵本KDP_組版"/"fonts"

INK      = (74, 55, 45)
INK_SOFT = (110, 90, 78)
B  = lambda s: ImageFont.truetype(str(FONTS/"ZenMaruGothic-Bold.ttf"), s)
M  = lambda s: ImageFont.truetype(str(FONTS/"ZenMaruGothic-Medium.ttf"), s)

TITLE = ["トトンと", "おでかけトイレ"]
SUB   = ["「いま いきたい」が いえるように なる えほん", "2さい 3さい 4さい"]
AUTHOR = "さく・え　はりま せいじ"

BLURB_A = ["おうちの トイレは できるのに、", "おでかけ さきだと いえない。"]
BLURB_B = ["いちばん むずかしいのは", "「がまん」じゃなくて、「いう こと」。"]
BLURB_C = ["・たいしょう 2さい 3さい 4さい", "・よみきかせ 3〜4ふん"]

def center(d, im, txt, f, y, fill=INK):
    w = d.textlength(txt, font=f)
    d.text(((im.width - w)/2, y), txt, font=f, fill=fill)

def front():
    im = Image.open(SRC/"01_表表紙_正方形.jpg").convert("RGB")
    d = ImageDraw.Draw(im); W = im.width
    ft = B(int(W*0.080)); fs = B(int(W*0.0275)); fa = M(int(W*0.026))
    y = int(W*0.055)
    for ln in TITLE:
        center(d, im, ln, ft, y); y += int(W*0.080*1.22)
    y += int(W*0.012)
    for ln in SUB:
        center(d, im, ln, fs, y); y += int(W*0.0275*1.5)
    y += int(W*0.010)
    center(d, im, AUTHOR, fa, y, fill=INK_SOFT)
    im.save(OUT/"PB_表表紙_正方形.jpg", quality=95, dpi=(300,300))
    print("表表紙(PB)", im.size)

def back():
    im = Image.open(SRC/"14_裏表紙_正方形.jpg").convert("RGB")
    d = ImageDraw.Draw(im); W = im.width
    fr = M(int(W*0.027)); fb = B(int(W*0.030)); fs = M(int(W*0.022))
    x = int(W*0.085); y = int(W*0.615)
    for ln in BLURB_A:
        d.text((x, y), ln, font=fr, fill=INK); y += int(W*0.027*1.6)
    y += int(W*0.022)
    for ln in BLURB_B:
        d.text((x, y), ln, font=fb, fill=INK); y += int(W*0.030*1.55)
    y += int(W*0.026)
    for ln in BLURB_C:
        d.text((x, y), ln, font=fs, fill=INK_SOFT); y += int(W*0.022*1.65)
    im.save(OUT/"PB_裏表紙_正方形.jpg", quality=95, dpi=(300,300))
    print("裏表紙(PB)", im.size)

if __name__ == "__main__":
    front(); back()
