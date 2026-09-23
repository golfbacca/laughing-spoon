# -*- coding: utf-8 -*-
"""ハウスフラッグ 24.5"x32" の入稿データを、既存の 12"x18" 入稿データから組む。

12x18の入稿データには、案ごとの手当て（R01のギンガム補修、R11の紺の地色など）が
すでに入っている。元のJPEGからやり直さず、**そこから組む**のが安全。

  12x18 の「見える範囲」 3600x4800 (12"x16")
    ↓ 高さを合わせて拡大
  24.5x32 の「見える範囲」 7350x8700 (24.5"x29")
    ↓ 足りない左右は、旗の地色を端から伸ばして埋める
"""
from PIL import Image, ImageDraw
import numpy as np, glob, os

CW,CH=7800,10012          # ハウスのキャンバス
BX,BY=225,206             # 裁ち落とし（左右0.75in / 上下0.69in）
SLEEVE=900                # 袖3インチと仮定（※Printifyで要確認）
SRC_VIS=(150,750,3750,5550)   # 12x18入稿の「見える範囲」3600x4800

os.makedirs("house",exist_ok=True)
vis_y0=BY+SLEEVE; vis_y1=CH-BY          # 見える範囲の縦
vis_h=vis_y1-vis_y0
print(f"ハウスの見える範囲: 幅{CW-2*BX}px({(CW-2*BX)/300:.1f}in) × 高さ{vis_h}px({vis_h/300:.1f}in)")
prev=[]
import sys
SRCDIR=sys.argv[1] if len(sys.argv)>1 else "upload_r"
PAT=sys.argv[2] if len(sys.argv)>2 else "R*_upload_3900x5700.png"
for f in sorted(glob.glob(f"{SRCDIR}/{PAT}")):
    tag=os.path.basename(f)[:3]
    im=Image.open(f).convert("RGB").crop(SRC_VIS)      # 12x18の見える範囲だけ
    s=vis_h/im.height
    nw,nh=int(round(im.width*s)), vis_h
    big=im.resize((nw,nh), Image.LANCZOS)
    cv=Image.new("RGB",(CW,CH))
    px=(CW-nw)//2
    # 左右の余白は、旗の端の列をそのまま伸ばす（地色が自然につながる）
    a=np.asarray(big)
    left=np.repeat(a[:,:1,:], max(0,px), axis=1)
    right=np.repeat(a[:,-1:,:], max(0,CW-px-nw), axis=1)
    row=np.concatenate([left,a,right],axis=1)[:, :CW]
    # 上下も同様に端を伸ばす（袖の中と裁ち落としに入る）
    top=np.repeat(row[:1,:,:], vis_y0, axis=0)
    bot=np.repeat(row[-1:,:,:], CH-vis_y1, axis=0)
    full=np.concatenate([top,row,bot],axis=0)[:CH]
    cv=Image.fromarray(full)
    suf=os.path.basename(f).replace("_3900x5700.png","")
    cv.save(f"house/{suf}_house_7800x10012.png", optimize=True)
    m=(CW-2*BX-nw)/2/300
    print(f"{tag}: 倍率{s:.2f} 実効{300/ (s*1.954) :.0f}DPI(元画像から) 旗の幅{nw}px({nw/300:.1f}in) "
          f"左右の余白 各{m:.2f}in")
    pv=cv.crop((BX,vis_y0,CW-BX,vis_y1))
    w=300; prev.append((tag, pv.resize((w,int(w*pv.height/pv.width)), Image.LANCZOS)))
W=prev[0][1].width; H=prev[0][1].height
o=Image.new("RGB",(W*5+60,H+30),(255,255,255)); d=ImageDraw.Draw(o)
for i,(t,p) in enumerate(prev):
    d.text((10+i*(W+10),8),t,fill=(0,0,0)); o.paste(p,(10+i*(W+10),24))
o.save("house_visible2.png"); print("saved house_visible2.png", o.size)
