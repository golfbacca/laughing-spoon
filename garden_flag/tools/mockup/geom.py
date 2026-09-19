# -*- coding: utf-8 -*-
"""背景写真の白フラッグ面の輪郭を実測する。

  ・布の判定: 輝度>170 かつ 彩度<26
    （実測値 — 布 sat 2〜11 / 旗のすぐ上の淡い空 19〜27 / 芝 30以上 / 外壁 29〜59）
  ・背景も白い箇所（bg02 の外壁）は判定不能。その行は捨て、
    判定できた行の傾きで外挿する
  ・輪郭は直線ではなく曲線で持つ（布はたわむ）
"""
from PIL import Image
import numpy as np

LUM_MIN, SAT_MAX = 165, 14

def maps(path):
    a=np.asarray(Image.open(path).convert("RGB")).astype(int)
    return (0.299*a[:,:,0]+0.587*a[:,:,1]+0.114*a[:,:,2]), (a.max(2)-a.min(2))

def ray(lum,sat,start,step,limit,lmin=None,smax=None):
    lmin=LUM_MIN if lmin is None else lmin; smax=SAT_MAX if smax is None else smax
    p=start
    while (limit-p)*np.sign(step)>0:
        if not (lum[p]>lmin and sat[p]<smax): return float(p-step)
        p+=step
    return np.nan                      # 限界まで布判定＝背景も白い＝判定不能

def medf(v,k):
    k=int(min(k, len(v) if len(v)%2 else len(v)-1))
    if k<3: return v.astype(float)
    p=k//2; vv=np.pad(v.astype(float),p,mode="edge")
    return np.median(np.stack([vv[i:i+len(v)] for i in range(k)]),axis=0)

def repair(t, v, deg=2, tol=10.0, it=4):
    """欠測と外れ値を除いて多項式で近似する。
       布の輪郭はなめらかな曲線なので、中央値フィルタのようなギザギザが出ない。
       測れた行が半分未満なら、外挿が暴れないよう直線に落とす。"""
    t=np.asarray(t,float); v=np.asarray(v,float); ok=~np.isnan(v)
    if ok.sum()<10: raise ValueError("測定できた行が少なすぎる")
    if ok.mean()<0.5: deg=min(deg,1)
    tt,vv=t[ok],v[ok]
    for _ in range(it):
        c=np.polyfit(tt,vv,deg); r=np.abs(vv-np.polyval(c,tt))
        k=r<max(tol,2.0*r.std())
        if k.sum()<max(10,deg+2): break
        tt,vv=tt[k],vv[k]
    return np.polyval(np.polyfit(tt,vv,deg), t)

def measure(path, seed, name="", verbose=True, thr=None):
    lmin,smax=(thr if thr else (LUM_MIN,SAT_MAX))
    """seed=(cx,cy, 左限界, 右限界, 上限界, 下限界)"""
    lum,sat=maps(path); H,W=lum.shape
    cx,cy,xlo,xhi,ylo,yhi=seed
    rows=np.arange(int(cy-(yhi-ylo)*0.30), int(cy+(yhi-ylo)*0.30))
    xL=np.full(len(rows), float(cx)); xR=np.full(len(rows), float(cx))
    for it in range(3):
        xc=((xL+xR)/2).astype(int)
        L=repair(rows,[ray(lum[y],sat[y],c,-1,xlo,lmin,smax) for y,c in zip(rows,xc)], deg=2)
        R=repair(rows,[ray(lum[y],sat[y],c,+1,xhi,lmin,smax) for y,c in zip(rows,xc)], deg=2)
        wid=np.median(R)-np.median(L)
        cols=np.arange(int(np.median(L)+wid*0.08), int(np.median(R)-wid*0.08))
        yc=int((rows[0]+rows[-1])/2)
        T=repair(cols,[ray(lum[:,x],sat[:,x],yc,-1,ylo,lmin,smax) for x in cols], deg=1)
        B=repair(cols,[ray(lum[:,x],sat[:,x],yc,+1,yhi,lmin,smax) for x in cols], deg=3)
        y0,y1=int(np.floor(T.min())), int(np.ceil(B.max()))
        nrows=np.arange(y0,y1+1)
        xL=np.interp(nrows,rows,L); xR=np.interp(nrows,rows,R)   # 行数を必ず合わせる
        rows=nrows
    rows=np.arange(y0,y1+1)
    mask=np.zeros((H,W),bool)
    Ti=np.interp(np.arange(W),cols,T,left=T[0],right=T[-1])
    Bi=np.interp(np.arange(W),cols,B,left=B[0],right=B[-1])
    for j,y in enumerate(rows):
        a0=max(0,int(np.floor(xL[j]))-1); a1=min(W-1,int(np.ceil(xR[j]))+1)
        if a1<=a0: continue
        xs=np.arange(a0,a1+1)
        mask[y, xs[(y>=Ti[xs]-1.5)&(y<=Bi[xs]+1.5)]]=True
    if verbose:
        w=xR.mean()-xL.mean(); h=B.mean()-T.mean()
        print(f"{name}: 左 {xL.min():.0f}〜{xL.max():.0f}  右 {xR.min():.0f}〜{xR.max():.0f}  "
              f"上 {T.min():.0f}〜{T.max():.0f}  裾 {B.min():.0f}〜{B.max():.0f}")
        print(f"{' '*len(name)}  幅{w:.0f} 高{h:.0f} 縦横比 {h/w:.3f}  画素 {mask.sum():,}")
    return mask
