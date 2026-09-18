"""
名入れ合成：空のリボン／プレートに買い手の名字を描画する

使い方:
    python3 make_name_flag.py "THE JOHNSONS"

入力: upload/<TAG>_upload_3900x5700.png （リボンが空欄の状態）
出力: named/<TAG>_<名前>_3900x5700.png

bands.json には案ごとの「文字を置ける長方形」が入っている。
これはリボンが弧を描いているため、**弧の内側に内接する最大長方形**を
自動計算したもの（docs/14 参照）。単純な外接矩形だと文字が輪郭線を
またいでしまう（N01・N09で実際に発生した）。

フォントは Google Fonts から取得して fonts/ に置く:
    Playfair Display Bold / Oswald Bold / Lora Bold / Cinzel Bold / Bebas Neue

注文が来たら年号ではなく名字を差し替えるだけ。3秒で入稿データができる。
ゴルフタオルの make_year_towel.py と同じ運用。
"""

from PIL import Image, ImageDraw, ImageFont
import json, os, sys

BANDS=json.load(open("bands.json"))
FONTS="fonts"
# 案ごと: フォント / 文字色 / 帯に対する余白率(左右, 上下) / 縦位置の微調整(px)
CFG={
 # 帯は「弧の内側に内接する長方形」なので余白は小さくてよい
 "N01": ("PlayfairDisplay.ttf",(21,68,42),  0.05,0.10, -18),
 "N02": ("Oswald.ttf",         (30,95,25),  0.07,0.16,  0),
 "N05": ("Lora.ttf",           (72,68,62),  0.05,0.12,  0),
 "N09": ("PlayfairDisplay.ttf",(24,74,45),  0.05,0.10,  0),
 "N10": ("Oswald.ttf",         (60,50,30),  0.06,0.14,  0),
}
def fit(draw, text, fontpath, maxw, maxh):
    lo,hi=10,600; best=None
    while lo<=hi:
        mid=(lo+hi)//2
        f=ImageFont.truetype(fontpath, mid)
        l,t,r,b=draw.textbbox((0,0), text, font=f)
        if (r-l)<=maxw and (b-t)<=maxh: best=(mid,f,r-l,b-t,l,t); lo=mid+1
        else: hi=mid-1
    return best

def render(tag, name, src=None, out=None):
    src = src or f"upload/{tag}_upload_3900x5700.png"
    im=Image.open(src).convert("RGB"); d=ImageDraw.Draw(im)
    x0,y0,x1,y1=BANDS[tag]
    fname,color,mx,my,dy=CFG[tag]
    bw,bh=x1-x0,y1-y0
    maxw,maxh=int(bw*(1-mx*2)), int(bh*(1-my*2))
    size,f,tw,th,ox,oy=fit(d, name, os.path.join(FONTS,fname), maxw, maxh)
    cx,cy=(x0+x1)//2,(y0+y1)//2+dy
    d.text((cx-tw//2-ox, cy-th//2-oy), name, font=f, fill=color)
    out = out or f"named/{tag}_THE_SMITHS_3900x5700.png"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, optimize=True)
    return size

NAME = sys.argv[1] if len(sys.argv)>1 else "THE SMITHS"
print(f"合成する文字: 「{NAME}」\n")
print(f"{'案':<6}{'フォント':<22}{'文字サイズ':>10}")
print("-"*40)
for t in ["N01","N02","N05","N09","N10"]:
    s=render(t, NAME)
    print(f"{t:<6}{CFG[t][0]:<22}{s:>8}px")
