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

CREAM      = (250, 244, 232)   # タイトル帯の色
SHIFT_DOWN = 0.150             # 絵を下へずらす量（画像高さ比）
FADE       = 0.085             # 絵の上端をクリームに溶かす幅

def make_headroom(im):
    """絵を下へずらし、上に本物の余白を作る。
    絵の側に空白を描かせようとすると幽霊の頭が湧いたため、
    構図は普通に描かせて、余白は組版側で作る方式にした。
    下端は空の道なので、切り落としても失うものが無い。"""
    import math
    W, H = im.size
    dy   = int(H * SHIFT_DOWN)
    fade = int(H * FADE)
    base = Image.new("RGB", (W, H), CREAM)
    base.paste(im, (0, dy))                     # はみ出した下端は自動で切れる
    mask = Image.new("L", (W, H), 255)
    px = mask.load()
    for y in range(0, min(H, dy + fade)):
        if y < dy:
            a = 0
        else:
            t = (y - dy) / max(1, fade)
            a = int(255 * (0.5 * (1 - math.cos(math.pi * t))))
        for x in range(W):
            px[x, y] = a
    return Image.composite(base, Image.new("RGB", (W, H), CREAM), mask)

def front():
    im = Image.open(SRC/"01_表表紙_正方形.jpg").convert("RGB")
    im = make_headroom(im)
    d = ImageDraw.Draw(im); W = im.width
    ft = B(int(W*0.078)); fs = B(int(W*0.0265)); fa = M(int(W*0.025))
    y = int(W*0.040)
    for ln in TITLE:
        center(d, im, ln, ft, y); y += int(W*0.078*1.22)
    y += int(W*0.012)
    for ln in SUB:
        center(d, im, ln, fs, y); y += int(W*0.0265*1.5)
    center(d, im, AUTHOR, fa, int(W*0.915), fill=INK_SOFT)
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

def kindle():
    """同じ正方形の絵から Kindle 表紙（1 : 1.6 の縦長）を作る。
    上にクリームの余白を足して縦長にし、そこにタイトルを置く。
    ペーパーバックと同じ絵・同じ書体になるので、2つの表紙が揃う。"""
    import math
    art = Image.open(SRC/"01_表表紙_正方形.jpg").convert("RGB")
    W = art.width
    H = int(round(W / 0.625))              # 1 : 1.6
    dy = H - art.height                    # 上に足すクリームの高さ
    im = Image.new("RGB", (W, H), CREAM)
    im.paste(art, (0, dy))
    fade = int(art.height * 0.10)
    mask = Image.new("L", (W, H), 255); px = mask.load()
    for y in range(0, min(H, dy + fade)):
        a = 0 if y < dy else int(255*(0.5*(1-math.cos(math.pi*(y-dy)/max(1,fade)))))
        for x in range(W): px[x, y] = a
    im = Image.composite(im, Image.new("RGB",(W,H),CREAM), mask)

    d = ImageDraw.Draw(im)
    ft = B(int(W*0.088)); fs = B(int(W*0.030)); fa = M(int(W*0.028))
    y = int(H*0.045)
    for ln in TITLE:
        center(d, im, ln, ft, y); y += int(W*0.088*1.22)
    y += int(W*0.012)
    for ln in SUB:
        center(d, im, ln, fs, y); y += int(W*0.030*1.5)
    center(d, im, AUTHOR, fa, int(H*0.945), fill=INK_SOFT)

    im.resize((1600, 2560), Image.LANCZOS).save(
        OUT/"01_表表紙_Kindle_1600x2560.jpg", quality=95, dpi=(300,300))
    print("表表紙(Kindle) 1600x2560")

if __name__ == "__main__":
    front(); back(); kindle()
