#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3冊目の表紙・裏表紙に文字を載せる。

1冊目との違いは1つだけ: ストア表紙も正方形（2560x2560）にする。
1冊目で 1:1.6 にしたら、正方形の本の1ページ目が縮んだ（引き継ぎ書5章）。

出力: docs/絵本KDP_3冊目_完成ページ/
        PB_表表紙_正方形.jpg          ペーパーバックの表面
        PB_裏表紙_正方形.jpg          ペーパーバックの裏面
        01_表表紙_Kindle_正方形2560.jpg  ストア表紙
"""
import math, pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT  = pathlib.Path(__file__).resolve().parents[2]
SRC   = ROOT/"docs"/"絵本KDP_3冊目_画像"
OUT   = ROOT/"docs"/"絵本KDP_3冊目_完成ページ"; OUT.mkdir(exist_ok=True)
SHIP  = ROOT/"docs"/"絵本KDP_3冊目_入稿"; SHIP.mkdir(exist_ok=True)
FONTS = ROOT/"docs"/"絵本KDP_組版"/"fonts"

INK      = (74, 55, 45)
INK_SOFT = (110, 90, 78)
CREAM    = (250, 244, 232)
# 【KDPに弾かれた・2026-08-26】アップロードするファイル名に日本語を入れると
# 「サポートされるファイル形式の表紙をアップロードします」と出る。
# 画像自体は正しいのに、拡張子の判定が通らない。入稿物は英数字名にする。
KINDLE_COVER = "toton03-cover-kindle-2560.jpg"

B = lambda s: ImageFont.truetype(str(FONTS/"ZenMaruGothic-Bold.ttf"), s)
M = lambda s: ImageFont.truetype(str(FONTS/"ZenMaruGothic-Medium.ttf"), s)

TITLE  = ["トトンと", "よるの トイレ"]
SUB    = ["「じぶんで あかりを つける」が はじまる えほん", "3さい 4さい 5さい"]
AUTHOR = "さく・え　はりま せいじ"

BLURB_A = ["よなかに めが さめても、", "ふとんから でて こない。"]
BLURB_B = ["いちばん むずかしいのは", "「トイレに いく こと」じゃなくて、", "「あかりを つける こと」。"]
BLURB_C = ["・たいしょう 3さい 4さい 5さい", "・よみきかせ 3〜4ふん"]

# 絵の上端をどれだけ下へずらすか。2冊目の表紙は元から上が空いているので
# 1冊目（0.150）より小さくてよい。大きくすると足が切れる。
SHIFT_DOWN = 0.075
FADE       = 0.085

def center(d, im, txt, f, y, fill=INK):
    d.text(((im.width - d.textlength(txt, font=f))/2, y), txt, font=f, fill=fill)

def make_headroom(im, shift=SHIFT_DOWN):
    """絵を下へずらし、上に本物の余白を作る。
    絵の側に空白を描かせようとすると幽霊の頭が湧いたため（1冊目の記録）、
    構図は普通に描かせて、余白は組版側で作る。"""
    W, H = im.size
    dy   = int(H*shift); fade = int(H*FADE)
    base = Image.new("RGB", (W, H), CREAM); base.paste(im, (0, dy))
    mask = Image.new("L", (W, H), 255); px = mask.load()
    for y in range(0, min(H, dy+fade)):
        a = 0 if y < dy else int(255*(0.5*(1-math.cos(math.pi*(y-dy)/max(1, fade)))))
        for x in range(W): px[x, y] = a
    return Image.composite(base, Image.new("RGB", (W, H), CREAM), mask)

def titled(im):
    """余白を作った絵に、タイトル・サブタイトル・著者名を置く。"""
    d = ImageDraw.Draw(im); W = im.width
    ft, fs, fa = B(int(W*0.078)), B(int(W*0.0265)), M(int(W*0.025))
    y = int(W*0.028)
    for ln in TITLE:
        center(d, im, ln, ft, y); y += int(W*0.078*1.22)
    y += int(W*0.010)
    for ln in SUB:
        center(d, im, ln, fs, y); y += int(W*0.0265*1.5)
    center(d, im, AUTHOR, fa, int(W*0.915), fill=INK_SOFT)
    return im

def front():
    im = titled(make_headroom(Image.open(SRC/"01_表表紙_正方形.jpg").convert("RGB")))
    im.save(OUT/"PB_表表紙_正方形.jpg", quality=95, dpi=(300, 300))
    print("表表紙(PB)", im.size)
    im.resize((2560, 2560), Image.LANCZOS).save(
        SHIP/KINDLE_COVER, quality=95, dpi=(300, 300))
    print(f"表表紙(Kindle) 2560x2560  {KINDLE_COVER}  ※正方形・英数字名")

def back():
    im = Image.open(SRC/"14_裏表紙_正方形.jpg").convert("RGB")
    d = ImageDraw.Draw(im); W = im.width
    fr, fb, fs = M(int(W*0.027)), B(int(W*0.030)), M(int(W*0.022))
    x, y = int(W*0.085), int(W*0.545)
    for ln in BLURB_A:
        d.text((x, y), ln, font=fr, fill=INK); y += int(W*0.027*1.6)
    y += int(W*0.022)
    for ln in BLURB_B:
        d.text((x, y), ln, font=fb, fill=INK); y += int(W*0.030*1.55)
    y += int(W*0.026)
    for ln in BLURB_C:
        d.text((x, y), ln, font=fs, fill=INK_SOFT); y += int(W*0.022*1.65)
    im.save(OUT/"PB_裏表紙_正方形.jpg", quality=95, dpi=(300, 300))
    print("裏表紙(PB)", im.size)

if __name__ == "__main__":
    front(); back()
