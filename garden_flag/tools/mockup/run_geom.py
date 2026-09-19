# -*- coding: utf-8 -*-
from geom import measure, maps
from PIL import Image
import numpy as np
from scipy import ndimage

SEEDS={  # (旗の内側の点cx,cy, 左限界, 右限界, 上限界, 下限界)
 "background01": (1680, 720, 1380, 2060, 300, 1160),
 "background02": ( 890, 720,  600, 1200, 300, 1160),
 "background03": ( 860, 760,  560, 1160, 380, 1160),
}
# 背景も白く自動判定できない箇所の実測クランプ
#   bg02 は旗のすぐ右が白い外壁。暗い前景が背景になる y900-1040 で実測 → 右端 x=1108
CLAMP={"background02": dict(x_max=1108)}
# 写真ごとの布判定しきい値（輝度下限, 彩度上限）— それぞれ実測して決めた
#   bg01: 旗のすぐ上の空が淡く 彩度19〜27 → 彩度を14まで絞る
#   bg02: 旗の左下が暖色の影に入り 彩度33 → 彩度を広く取り、白い外壁側はクランプで抑える
THR={"background01":(165,14), "background02":(150,34), "background03":(165,14)}

def polish(mask, path, clamp=None, grow=3, fabthr=(165,14)):
    """残った白い縁を、布らしい画素の範囲でだけ数px広げて拾う"""
    lum,sat=maps(path)
    fab=(lum>fabthr[0])&(sat<fabthr[1])
    m=ndimage.binary_dilation(mask, np.ones((3,3)), iterations=grow) & (fab|mask)
    if clamp:
        if "x_max" in clamp: m[:, clamp["x_max"]+1:]=False
        if "x_min" in clamp: m[:, :clamp["x_min"]]=False
    lab,n=ndimage.label(m); sz=ndimage.sum(m,lab,range(1,n+1))
    m=ndimage.binary_fill_holes(lab==int(np.argmax(sz))+1)
    return m

sheet=[]
for n,s in SEEDS.items():
    m=measure(f"zin/{n}.jpeg", s, n, thr=THR[n])
    m=polish(m, f"zin/{n}.jpeg", CLAMP.get(n), fabthr=THR[n])
    np.save(f"mask_{n}.npy", m)
    ys,xs=np.where(m)
    cols=np.arange(xs.min(),xs.max()+1); iy=np.arange(m.shape[0])
    h=np.array([iy[m[:,x]].max()-iy[m[:,x]].min() for x in cols])
    print(f"{' '*len(n)}  → 仕上げ後 x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} "
          f"幅{xs.max()-xs.min()+1} 高(中央値){np.median(h):.0f} 縦横比{np.median(h)/(xs.max()-xs.min()+1):.3f} 画素{m.sum():,}\n")
    im=Image.open(f"zin/{n}.jpeg").convert("RGB"); W,H=im.size
    arr=np.zeros((H,W,4),np.uint8); arr[m]=(255,0,255,120)
    v=Image.alpha_composite(im.convert("RGBA"),Image.fromarray(arr)).convert("RGB")
    sheet.append(v.crop((max(0,xs.min()-90),max(0,ys.min()-90),min(W,xs.max()+90),min(H,ys.max()+90))))
o=Image.new("RGB",(sum(x.width for x in sheet)+40,max(x.height for x in sheet)+20),(255,255,255)); X=10
for x in sheet: o.paste(x,(X,10)); X+=x.width+10
o.save("flag_detect6.png"); print("saved flag_detect6.png",o.size)
