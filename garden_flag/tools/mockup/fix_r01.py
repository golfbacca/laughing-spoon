# -*- coding: utf-8 -*-
"""R01 のギンガム枠の横縞を作り直す。

実測した崩れ（upload_r/_R01_before.png）:
  ・y 1605〜1831 に高さ226pxの濃い縞が1本（他は97〜108px、約2.1倍）
  ・上側の周期198px / 下側の周期213px。縞の位相も1本ずれている

考え方:
  枠は3色の平坦な塗り（セル内の標準偏差 0.8〜1.9）なので
      画素(x,y) = P_L(x) + t(y)·( P_D(x) − P_L(x) )
  と分解できる。P_D/P_L は濃い行・薄い行の横断面（実測）、t(y) は行の濃さ。
  t(y) だけを一定周期に作り直せば、列の構造も黄色地との境目のぼかしも原画のまま残る。

  名前用オーバルは枠に重なっている。形を推定せず、
  「原画」と「原画自身の t_old(y) で再構成した枠」の差からマスクを作って保護する。
  t_old(y) は、オーバルが絶対に届かない列 x 430〜520（実測: オーバルの左端は最小594）で測る。

  上バー(y 812-1110)と下バー(y 5123-5427)は触らない。両端が縞の境目なので角はつながる。
"""
from PIL import Image
import numpy as np
from scipy import ndimage

SRC="upload_r/_R01_before.png"
DST="upload_r/R01_upload_3900x5700.png"
# (帯の範囲, t(y)を測る列, オーバルが入ってくる向き)
BANDS=[((415,728),(430,520),"right"), ((3172,3482),(3380,3465),"left")]
Y0,Y1 = 1110, 5123
N_ROWS = 39                 # 薄で始まり薄で終わる奇数（y=5123 から濃が始まるため）
REF_D  = (2998,3086)
REF_L  = (3106,3191)
EDGE   = 3.0

def tone_wave(y, y0, pitch, edge):
    f=((y-y0)/pitch)%2.0; e=edge/pitch
    return np.clip(np.clip((f-1.0)/e,0,1)-np.clip((f-2.0+e)/e,0,1),0,1)

def main():
    src=np.asarray(Image.open(SRC).convert("RGB")).astype(np.float32)
    out=src.copy()
    pitch=(Y1-Y0)/N_ROWS
    print(f"補修 y {Y0}〜{Y1} ({Y1-Y0}px) → {N_ROWS}行 × {pitch:.2f}px")
    yy=np.arange(Y0,Y1,dtype=np.float32)
    t_new=tone_wave(yy,Y0,pitch,EDGE).astype(np.float32)

    for (x0,x1),(px0,px1),side in BANDS:
        PD=src[REF_D[0]:REF_D[1], x0:x1].mean(axis=0)
        PL=src[REF_L[0]:REF_L[1], x0:x1].mean(axis=0)
        lumD=float(PD[px0-x0:px1-x0].mean()); lumL=float(PL[px0-x0:px1-x0].mean())
        # 原画の行の濃さ（オーバルの届かない列で実測）
        t_old=np.clip((src[Y0:Y1,px0:px1].mean(axis=(1,2))-lumL)/(lumD-lumL),0,1).astype(np.float32)

        G_old=PL[None,:,:]+t_old[:,None,None]*(PD-PL)[None,:,:]
        G_new=PL[None,:,:]+t_new[:,None,None]*(PD-PL)[None,:,:]
        dif=np.abs(src[Y0:Y1,x0:x1]-G_old).max(axis=2)
        raw=dif>20
        raw[:, :6]=False; raw[:, -6:]=False        # 帯と黄色地の境目の微差は拾わない
        # 20px以上続く塊がある行＝オーバルが重なっている行
        solid=ndimage.binary_opening(dif>25, np.ones((1,21)))
        rows=solid.any(1)
        idx=np.arange(x1-x0)[None,:]
        MARGIN=4                                    # 輪郭のぼかし分だけ外へ広げる
        if side=="right":
            first=np.where(raw.any(1), np.argmax(raw,1)-MARGIN, x1-x0)
            mask=(idx>=first[:,None]) & rows[:,None]
        else:
            last=np.where(raw.any(1), (x1-x0-1)-np.argmax(raw[:,::-1],1)+MARGIN, -1)
            mask=(idx<=last[:,None]) & rows[:,None]
        keep=ndimage.gaussian_filter(mask.astype(np.float32),2.0)
        keep=np.clip(keep*1.8,0,1)[:,:,None]

        seam=np.ones((Y1-Y0,1,1),np.float32); k=8
        seam[:k,0,0]=np.linspace(0,1,k); seam[-k:,0,0]=np.linspace(1,0,k)
        w=seam*(1.0-keep)
        old=src[Y0:Y1,x0:x1]
        out[Y0:Y1,x0:x1]=old*(1-w)+G_new*w
        rows=int((mask.any(1)).sum())
        print(f"  帯 x{x0}-{x1}: オーバル等を保護した行 {rows}行 "
              f"(y {Y0+int(np.argmax(mask.any(1)))}〜{Y0+len(mask)-1-int(np.argmax(mask.any(1)[::-1]))})")
    Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(DST, optimize=True)
    print("保存:", DST)

if __name__=="__main__": main()
