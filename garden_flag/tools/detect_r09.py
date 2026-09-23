# -*- coding: utf-8 -*-
"""R09 の名入れプレートを検出し、bands_r.json の R09 だけ更新する"""
from PIL import Image, ImageDraw
import numpy as np, json
from collections import deque
def largest_rect(m):
    h,w=m.shape; heights=np.zeros(w,int); best=(0,0,0,0,0)
    for y in range(h):
        heights=np.where(m[y],heights+1,0); st=[]; i=0; hh=list(heights)+[0]
        while i<len(hh):
            if not st or hh[st[-1]]<=hh[i]: st.append(i); i+=1
            else:
                top=st.pop(); left=st[-1]+1 if st else 0
                ar=hh[top]*(i-left)
                if ar>best[0]: best=(ar,left,y-hh[top]+1,i-1,y)
    return best[1:]
n="R09"
im=Image.open(f"upload_r/{n}_upload_3900x5700.png").convert("RGB")
s=8; sm=im.resize((3900//s,5700//s), Image.LANCZOS); a=np.asarray(sm).astype(int)
H,W,_=a.shape; best=None
for sy in (0.62,0.68,0.74,0.80):
    for sx in (0.40,0.50,0.60):
        seed=(int(H*sy), int(W*sx)); base=a[seed].astype(int)
        ok=np.abs(a-base).max(axis=2)<20
        if not ok[seed]: continue
        m=np.zeros_like(ok); q=deque([seed]); m[seed]=True
        while q:
            cy,cx=q.popleft()
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=cy+dy,cx+dx
                if 0<=ny<H and 0<=nx<W and ok[ny,nx] and not m[ny,nx]: m[ny,nx]=True; q.append((ny,nx))
        cnt=m.sum()
        if cnt < H*W*0.02 or cnt > H*W*0.45: continue
        ys,xs=np.where(m)
        if ys.min() < H*0.45: continue
        sub=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
        rx0,ry0,rx1,ry1=largest_rect(sub)
        R=[int((xs.min()+rx0)*s),int((ys.min()+ry0)*s),int((xs.min()+rx1+1)*s),int((ys.min()+ry1+1)*s)]
        area=(R[2]-R[0])*(R[3]-R[1])
        if best is None or area>best[0]: best=(area,R,tuple(base))
_,R,col=best
print(f"{n}: プレート地色 {col}  内接長方形 {R}  {R[2]-R[0]} x {R[3]-R[1]}")
print(f"   上端750pxとの関係: プレート上端 y={R[1]} （750より下なら安全）")
b=json.load(open("bands_r.json")); b[n]=R; json.dump(b,open("bands_r.json","w"))
print("bands_r.json を更新:", b[n])
# 目視確認用
pv=im.copy(); d=ImageDraw.Draw(pv,"RGBA")
d.rectangle(R, outline=(255,0,255,255), width=14)
d.rectangle([0,0,3900,750], fill=(255,0,0,60))
pv.resize((3900//6,5700//6),Image.LANCZOS).save("r09_plate.png")
