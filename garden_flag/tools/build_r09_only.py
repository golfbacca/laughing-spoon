# -*- coding: utf-8 -*-
"""R09 だけ入稿データ 3900x5700 を作り直す（他案の入稿データには触らない）"""
from PIL import Image, ImageDraw
import numpy as np, os
OUT="upload_r"; os.makedirs(OUT, exist_ok=True)
CW,CH=3900,5700; BLEED=150; SLEEVE=600; PAD=120
f="zin/R09  GONE GOLFING - BACK EVENTUALLY.jpeg"; tag="R09"
def bg_color(a):
    h,w,_=a.shape; m=max(2,int(min(h,w)*0.02))
    ring=np.concatenate([a[:m].reshape(-1,3),a[-m:].reshape(-1,3),a[:,:m].reshape(-1,3),a[:,-m:].reshape(-1,3)])
    q=(ring//8*8); v,c=np.unique(q,axis=0,return_counts=True); return v[c.argmax()].astype(int)
def cbox(a,bg,tol=26,frac=0.02):
    h,w,_=a.shape; d=np.abs(a.astype(int)-bg).max(axis=2)>tol
    t=next((y for y in range(h) if d[y].mean()>frac),0); b=next((y for y in range(h-1,-1,-1) if d[y].mean()>frac),h-1)
    l=next((x for x in range(w) if d[:,x].mean()>frac),0); r=next((x for x in range(w-1,-1,-1) if d[:,x].mean()>frac),w-1)
    return l,t,r+1,b+1
im=Image.open(f).convert("RGB"); a=np.asarray(im); bg=bg_color(a); W,H=im.size
l,t,r,b=cbox(a,bg); touch=(l<=1) or (r>=W-1)
x0,x1=(0,CW) if touch else (BLEED+PAD,CW-BLEED-PAD)
y0,y1=BLEED+SLEEVE+60, CH-(BLEED if touch else BLEED+PAD)
cw,ch=r-l,b-t; s=min((x1-x0)/cw,(y1-y0)/ch)
nw,nh=int(round(W*s)),int(round(H*s)); big=im.resize((nw,nh), Image.LANCZOS)
nl,nt=int(round(l*s)),int(round(t*s)); ncw,nch=int(round(cw*s)),int(round(ch*s))
px=x0+((x1-x0)-ncw)//2-nl; py=y0+((y1-y0)-nch)//2-nt
if touch:
    cv=Image.new("RGB",(CW,CH),tuple(bg)); cv.paste(big,(px,py))
else:
    arr=np.asarray(big); pt,pl=max(0,py),max(0,px); pb,pr=max(0,CH-(py+nh)),max(0,CW-(px+nw))
    p=np.pad(arr,((pt,pb),(pl,pr),(0,0)),mode="edge")
    cv=Image.fromarray(p[max(0,-py):max(0,-py)+CH, max(0,-px):max(0,-px)+CW])
cv.save(f"{OUT}/{tag}_upload_3900x5700.png", optimize=True)
print(f"背景色 {tuple(bg)}  元の中身 x{l}-{r} y{t}-{b}  端に接触 {'はい' if touch else 'いいえ'}")
print(f"倍率 {s:.3f}  配置後の中身の上端 y={py+nt}px（見えない範囲は上から750pxまで）")
print(f"保存 {OUT}/{tag}_upload_3900x5700.png")
