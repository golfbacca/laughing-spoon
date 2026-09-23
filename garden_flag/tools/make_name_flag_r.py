# -*- coding: utf-8 -*-
"""大きなプレートに「THE / 名字」を2行で合成する。

プレートの形に応じて2通りの合わせ方を使う。

  長方形のプレート（R02/R05/R09/R11）
    帯の内側に余白を取り、その長方形に収まる最大サイズを二分探索する。

  楕円のプレート（R01）
    楕円に内接する長方形を使うと、**楕円の幅2513pxに対して1414px(56%)**しか
    使えず、文字が不必要に小さくなる（2026-09-23 本人の指摘で判明）。
    → 文字の各行の四隅が楕円の内側にあるかを直接判定する方式に変更。
      1.54〜1.66倍のサイズが取れ、リングまでの余裕も0.22〜0.32インチ確保できる。
"""
from PIL import Image, ImageDraw, ImageFont
import json, os, sys

B=json.load(open("bands_r.json")); FD="fonts"
# 案: フォント / 文字色 / 左右余白率 / 上下余白率 / 「THE」の相対サイズ
CFG={
 "R01": ("PlayfairDisplay.ttf",(21,68,42),   0.10,0.16, 0.40),
 "R02": ("Oswald.ttf",         (28,92,24),   0.08,0.14, 0.38),
 "R05": ("Lora.ttf",           (72,68,62),   0.09,0.16, 0.40),
 "R09": ("PlayfairDisplay.ttf",(28,74,45),   0.09,0.14, 0.40),
 "R11": ("Cinzel.ttf",         (203,166,80), 0.09,0.16, 0.42),
}
# 楕円プレートの案は、楕円そのものに合わせる。(中心x, 中心y, 半径a, 半径b, 内側の余裕)
ELLIPSE={"R01": (1950.0, 3603.0, 1256.0, 835.0, 60.0)}
GAP_R=0.12                      # 行間＝名字のサイズの12%

def bbox(d,t,f):
    l,tp,r,b=d.textbbox((0,0),t,font=f); return r-l,b-tp,l,tp

def _fit_rect(d, fp, surname, maxw, maxh, rel):
    lo,hi,best=10,900,None
    while lo<=hi:
        mid=(lo+hi)//2
        fb=ImageFont.truetype(fp,mid); ft=ImageFont.truetype(fp,max(8,int(mid*rel)))
        w2,h2,_,_=bbox(d,surname,fb); w1,h1,_,_=bbox(d,"THE",ft)
        if max(w1,w2)<=maxw and h1+int(mid*GAP_R)+h2<=maxh: best=(mid,fb,ft); lo=mid+1
        else: hi=mid-1
    return best

def _fit_ellipse(d, fp, surname, ov, rel):
    """各行の四隅が楕円の内側に入る最大サイズ"""
    cx,cy,a,b,pad=ov; A,Bb=a-pad,b-pad
    ins=lambda x,y: ((x-cx)/A)**2+((y-cy)/Bb)**2 <= 1.0
    lo,hi,best=10,1400,None
    while lo<=hi:
        S=(lo+hi)//2
        fb=ImageFont.truetype(fp,S); ft=ImageFont.truetype(fp,max(8,int(S*rel)))
        w2,h2,_,_=bbox(d,surname,fb); w1,h1,_,_=bbox(d,"THE",ft)
        gap=int(S*GAP_R); total=h1+gap+h2; top=cy-total/2
        boxes=((cx-w1/2,top,cx+w1/2,top+h1),
               (cx-w2/2,top+h1+gap,cx+w2/2,top+h1+gap+h2))
        if all(ins(X,Y) for x0,y0,x1,y1 in boxes for X,Y in ((x0,y0),(x1,y0),(x0,y1),(x1,y1))):
            best=(S,fb,ft); lo=S+1
        else: hi=S-1
    return best

def render(tag, surname, out_dir="named_r"):
    im=Image.open(f"upload_r/{tag}_upload_3900x5700.png").convert("RGB")
    d=ImageDraw.Draw(im)
    fn,col,mx,my,rel=CFG[tag]; fp=os.path.join(FD,fn)
    if tag in ELLIPSE:
        cx,cy,_,_,_=ELLIPSE[tag]
        size,fb,ft=_fit_ellipse(d,fp,surname,ELLIPSE[tag],rel)
    else:
        x0,y0,x1,y1=B[tag]
        cx,cy=(x0+x1)/2,(y0+y1)/2
        size,fb,ft=_fit_rect(d,fp,surname,int((x1-x0)*(1-mx*2)),int((y1-y0)*(1-my*2)),rel)
    w2,h2,ox2,oy2=bbox(d,surname,fb); w1,h1,ox1,oy1=bbox(d,"THE",ft)
    gap=int(size*GAP_R); total=h1+gap+h2; top=cy-total/2
    d.text((cx-w1/2-ox1, top-oy1), "THE", font=ft, fill=col)
    d.text((cx-w2/2-ox2, top+h1+gap-oy2), surname, font=fb, fill=col)
    os.makedirs(out_dir, exist_ok=True)
    im.save(f"{out_dir}/{tag}_{surname}_3900x5700.png", optimize=True)
    return size, int(size*rel)

if __name__=="__main__":
    SUR = sys.argv[1] if len(sys.argv)>1 else "SMITHS"
    print(f"合成する名字: 「THE {SUR}」\n")
    print(f"{'案':<5}{'合わせ方':<10}{'フォント':<22}{'名字':>9}{'THE':>8}")
    print("-"*56)
    for t in ["R01","R02","R05","R09","R11"]:
        a,b=render(t,SUR)
        print(f"{t:<5}{('楕円' if t in ELLIPSE else '長方形'):<10}{CFG[t][0]:<22}{a:>7}px{b:>6}px")
