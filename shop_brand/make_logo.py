# -*- coding: utf-8 -*-
"""Etsyのショップアイコン（500x500）を3案作る。

Etsyの推奨は500x500。検索やレビュー欄では**70px程度**まで縮むので、
作ったあと必ず縮小版で読めるかを確認すること。
配色は出品画像と同じ（garden_flag/tools/mockup/listing_img.py）。
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

S=500
CREAM=(249,246,240); INK=(38,42,38); ACC=(22,86,52); RED=(190,45,45); GOLD=(203,166,80)
FD="../garden_flag/tools/fonts"
def bebas(sz): return ImageFont.truetype(f"{FD}/BebasNeue.ttf", sz)
def mont(sz,w="Bold"):
    f=ImageFont.truetype(f"{FD}/Montserrat.ttf",sz); f.set_variation_by_name(w); return f

def ctext(d,xy,s,f,fill,spacing=0):
    d.text(xy,s,font=f,fill=fill,anchor="mm")

def golf_ball(size, body=CREAM, dim=(222,219,210)):
    """ディンプル付きのゴルフボール（4倍で描いて縮小）"""
    k=4; n=size*k
    im=Image.new("RGBA",(n,n),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.ellipse([0,0,n-1,n-1],fill=body+(255,))
    r=n*0.052; step=n*0.145
    y=step*0.6
    row=0
    while y<n:
        x=step*0.6 + (step/2 if row%2 else 0)
        while x<n:
            if ((x-n/2)**2+(y-n/2)**2)**0.5 < n/2-r*1.6:
                d.ellipse([x-r,y-r,x+r,y+r],fill=dim+(255,))
            x+=step
        y+=step; row+=1
    # 右下に軽い陰
    sh=Image.new("L",(n,n),0); ImageDraw.Draw(sh).ellipse([n*0.18,n*0.18,n*1.02,n*1.02],fill=46)
    sh=sh.filter(ImageFilter.GaussianBlur(n*0.07))
    im.paste(Image.new("RGBA",(n,n),(90,95,88,255)), (0,0), Image.composite(sh,Image.new("L",(n,n),0),im.split()[3]))
    return im.resize((size,size),Image.LANCZOS)

# ---------------------------------------------------------------- A 旗とグリーン
def logo_A(out):
    im=Image.new("RGB",(S,S),CREAM); d=ImageDraw.Draw(im)
    d.ellipse([18,18,S-18,S-18],outline=ACC,width=9)
    # グリーン
    d.ellipse([112,232,388,330],fill=ACC)
    d.ellipse([228,258,266,276],fill=(18,60,38))          # カップ
    # ポールと旗
    d.line([(247,262),(247,118)],fill=INK,width=9)
    d.polygon([(251,122),(348,152),(251,182)],fill=RED)
    ctext(d,(S//2,392),"ONE PURE STRIKE",bebas(54),ACC)
    im.save(out,quality=95)

# ---------------------------------------------------------------- B ゴルフボール
def logo_B(out):
    im=Image.new("RGB",(S,S),ACC); d=ImageDraw.Draw(im)
    b=golf_ball(236); im.paste(b,(132,96),b)
    d.line([(96,330),(404,330)],fill=GOLD,width=6)
    ctext(d,(S//2,392),"ONE PURE STRIKE",bebas(56),CREAM)
    im.save(out,quality=95)

# ---------------------------------------------------------------- C 文字だけ
def logo_C(out):
    im=Image.new("RGB",(S,S),ACC); d=ImageDraw.Draw(im)
    d.rectangle([24,24,S-24,S-24],outline=GOLD,width=5)
    ctext(d,(S//2,150),"ONE",bebas(104),CREAM)
    ctext(d,(S//2,255),"PURE",bebas(104),GOLD)
    ctext(d,(S//2,360),"STRIKE",bebas(104),CREAM)
    im.save(out,quality=95)

# ---------------------------------------------------------------- D 旗（文字なし・推奨）
def logo_D(out):
    """Etsyはアイコンの隣に必ずショップ名を文字で出すので、アイコンに名前は要らない。
       文字を外して図を大きくすると、70pxでの判別が段違いに良くなる。"""
    im=Image.new("RGB",(S,S),CREAM); d=ImageDraw.Draw(im)
    d.ellipse([14,14,S-14,S-14],outline=ACC,width=14)
    d.ellipse([78,300,422,432],fill=ACC)            # グリーン
    d.ellipse([222,336,278,362],fill=(16,56,34))     # カップ
    d.line([(250,344),(250,92)],fill=INK,width=15)   # ポール
    d.polygon([(258,98),(400,150),(258,202)],fill=RED)
    im.save(out,quality=95)

# ---------------------------------------------------------------- E ボール（文字なし）
def logo_E(out):
    im=Image.new("RGB",(S,S),ACC); d=ImageDraw.Draw(im)
    b=golf_ball(372); im.paste(b,(64,64),b)
    im.save(out,quality=95)

if __name__=="__main__":
    for n,fn in (("A",logo_A),("B",logo_B),("C",logo_C),("D",logo_D),("E",logo_E)):
        fn(f"logo_{n}.png"); print(f"  logo_{n}.png")
    # 比較シート：原寸・140px・70px を並べる
    NAMES="DAECB"
    sheet=Image.new("RGB",(S*len(NAMES)+20*(len(NAMES)+1), S+230),(255,255,255)); sd=ImageDraw.Draw(sheet)
    f=mont(26,"SemiBold"); fs=mont(20,"Medium")
    for i,n in enumerate(NAMES):
        im=Image.open(f"logo_{n}.png"); x=20+i*(S+20)
        sheet.paste(im,(x,60))
        sd.text((x+S//2,36),n,font=f,fill=(30,30,30),anchor="mm")
        for j,px in enumerate((140,70)):
            sheet.paste(im.resize((px,px),Image.LANCZOS),(x+20+j*180, S+90))
            sd.text((x+20+j*180+px//2, S+90+px+22),f"{px}px",font=fs,fill=(90,90,90),anchor="mm")
    sd.text((40,S+76),"actual display size on Etsy (approx. 70px in listings / reviews)",font=fs,fill=(90,90,90))
    sheet.save("_comparison.png",quality=92); print("  _comparison.png")
