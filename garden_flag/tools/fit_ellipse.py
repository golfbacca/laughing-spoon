# -*- coding: utf-8 -*-
"""楕円のプレートに、長方形ではなく「楕円そのもの」に合わせて文字を入れる。

いまの方式:
  楕円 → 最大内接長方形 → さらに余白を引く → その中に文字
  R01 では 楕円の幅2513px に対して文字枠が1414px（56%）しか取れていなかった。

新しい方式:
  文字の各行の四隅が楕円の内側にあるかを直接判定して、入る最大サイズを二分探索する。
  幅の広い行（名字）は楕円が最も広い高さに置かれるので、大きく取れる。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def bbox(d,t,f):
    l,tp,r,b=d.textbbox((0,0),t,font=f); return r-l,b-tp,l,tp

def inside(x,y,cx,cy,a,b):
    return ((x-cx)/a)**2 + ((y-cy)/b)**2 <= 1.0

def fit_two_lines(oval, top_text, main_text, font_path, rel=0.40, gap_r=0.12,
                  pad=60, y_shift=0.0, lo=10, hi=1400):
    """oval=(cx,cy,a,b)。文字の四隅が楕円(半径 a-pad, b-pad)の内側に入る最大サイズを返す"""
    cx,cy,a,b=oval; A=a-pad; B=b-pad
    d=ImageDraw.Draw(Image.new("RGB",(10,10)))
    best=None
    while lo<=hi:
        S=(lo+hi)//2
        fb=ImageFont.truetype(font_path,S); ft=ImageFont.truetype(font_path,max(8,int(S*rel)))
        w2,h2,ox2,oy2=bbox(d,main_text,fb); w1,h1,ox1,oy1=bbox(d,top_text,ft)
        gap=int(S*gap_r); total=h1+gap+h2
        top=cy+y_shift*b-total/2
        boxes=[(cx-w1/2, top,        cx+w1/2, top+h1),
               (cx-w2/2, top+h1+gap, cx+w2/2, top+h1+gap+h2)]
        ok=all(inside(X,Y,cx,cy,A,B) for x0,y0,x1,y1 in boxes
               for X,Y in ((x0,y0),(x1,y0),(x0,y1),(x1,y1)))
        if ok: best=(S,fb,ft,boxes); lo=S+1
        else:  hi=S-1
    return best

if __name__=="__main__":
    OV=(1950.0,3603.0,1256.0,835.0)
    fp="fonts/PlayfairDisplay.ttf"
    print("R01 の名入れ：いまの方式と、楕円に直接合わせた場合の比較\n")
    print(f"{'名字':<14}{'いまの方式':>11}{'楕円に合わせる':>15}{'倍率':>8}")
    print("-"*50)
    import json
    B_=json.load(open("bands_r.json"))["R01"]
    d=ImageDraw.Draw(Image.new("RGB",(10,10)))
    for sur in ("SMITHS","MILLERS","ANDERSONS","WASHINGTONS","HIGGINBOTHAMS"):
        # いまの方式
        x0,y0,x1,y1=B_; mw=int((x1-x0)*0.8); mh=int((y1-y0)*0.68)
        lo,hi,old=10,900,0
        while lo<=hi:
            m=(lo+hi)//2
            fb=ImageFont.truetype(fp,m); ft=ImageFont.truetype(fp,max(8,int(m*0.40)))
            w2,h2,_,_=bbox(d,sur,fb); w1,h1,_,_=bbox(d,"THE",ft)
            if max(w1,w2)<=mw and h1+int(m*0.12)+h2<=mh: old=m; lo=m+1
            else: hi=m-1
        r=fit_two_lines(OV,"THE",sur,fp)
        new=r[0] if r else 0
        print(f"{sur:<14}{old:>9}px{new:>13}px{new/old:>7.2f}倍")
