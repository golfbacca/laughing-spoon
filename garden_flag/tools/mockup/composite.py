# -*- coding: utf-8 -*-
"""入稿データ(3900x5700)を、背景写真の白フラッグ面へ貼り込む。

  ・横は「その行の左端〜右端」、縦は「その列の上端〜下端」で正規化して貼る。
    布のたわみ・裾のカーブ・下に向かって広がる揺れが、そのまま保たれる。
  ・切り出す上端を袖の分だけ動かし、写真に写っている旗の縦横比に合わせる。
      縦横比1.50 = 裁ち落とし後の全面(12"x18")が写っている
      縦横比1.33 = 袖(上2")が隠れ、12"x16"だけが写っている
    → 実測した縦横比に応じて連続的に選ぶので、デザインを左右に切らずに済む。
  ・元写真の明暗を乗算で戻し、しわと影を保つ。
"""
from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage

BLEED=150; W_TRIM=3600; Y_HEM=5550        # 裁ち落とし後の下端
TOP_TRIM=150; TOP_VISIBLE=750             # 全面 / 袖を除いた見える範囲 の上端

def medf(v,k):
    k=int(min(k, len(v) if len(v)%2 else len(v)-1))
    if k<3: return np.asarray(v,float)
    p=k//2; vv=np.pad(np.asarray(v,float),p,mode="edge")
    return np.median(np.stack([vv[i:i+len(v)] for i in range(k)]),axis=0)

def smooth(v,k=11):
    """中央値フィルタ後の整数の段差をならし、貼り込みに階段が出ないようにする"""
    v=np.asarray(v,float); k=int(min(k, len(v)))
    if k<3: return v
    w=np.ones(k)/k
    return np.convolve(np.pad(v,(k//2,k//2),mode="edge"), w, mode="valid")[:len(v)]

def spans(mask):
    """行ごとの左右端、列ごとの上下端（なめらかな曲線として返す）"""
    H,W=mask.shape; iy=np.arange(H); ix=np.arange(W)
    rows=np.where(mask.any(1))[0]; cols=np.where(mask.any(0))[0]
    xl=smooth(medf(np.array([ix[mask[y]].min() for y in rows],float),15))
    xr=smooth(medf(np.array([ix[mask[y]].max() for y in rows],float),15))
    yt=smooth(medf(np.array([iy[mask[:,x]].min() for x in cols],float),15))
    yb=smooth(medf(np.array([iy[mask[:,x]].max() for x in cols],float),15))
    return rows,cols,xl,xr,yt,yb

def source_box(target_ar):
    top=int(round(min(max(Y_HEM - W_TRIM*target_ar, TOP_TRIM), TOP_VISIBLE)))
    return (BLEED, top, BLEED+W_TRIM, Y_HEM), (Y_HEM-top)/W_TRIM

def composite(bg_path, design_path, mask_path, out_path, shade_gamma=0.92, verbose=True,
              scale=1.0, crop=None, out_size=None):
    """scale: 背景を先に拡大してから貼ると、デザインは原寸のまま載るので旗が鮮明になる
       crop:  (幅,高さ,旗の中心を置く縦位置) で切り出す。Etsyの一覧は4:3で中央を切るため"""
    bg=Image.open(bg_path).convert("RGB")
    mask=np.load(mask_path)
    if scale!=1.0:
        W,H=int(round(bg.width*scale)), int(round(bg.height*scale))
        bg=bg.resize((W,H), Image.LANCZOS)
        mask=np.asarray(Image.fromarray(mask.astype(np.uint8)*255).resize((W,H), Image.BILINEAR))>127
    W,H=bg.size
    out=np.asarray(bg).astype(np.float32)
    rows,cols,xl,xr,yt,yb=spans(mask)

    target_ar=float(np.median(yb-yt))/float(np.median(xr-xl))
    box,src_ar=source_box(target_ar)
    des=Image.open(design_path).convert("RGB").crop(box)
    Wd,Hd=des.size; da=np.asarray(des).astype(np.float32)
    if verbose:
        print(f"   旗 幅{np.median(xr-xl):.0f} 高{np.median(yb-yt):.0f} 縦横比{target_ar:.3f}"
              f" → 切り出し上端 y={box[1]} (袖の {(box[1]-TOP_TRIM)/6:.0f}% を隠す"
              f" / 版{src_ar:.3f} / 残る伸縮 {(target_ar/src_ar-1)*100:+.1f}%)")

    y0,y1=rows[0],rows[-1]; x0,x1=cols[0],cols[-1]
    ys,xs=np.mgrid[y0:y1+1, x0:x1+1]
    XL=xl[ys-y0]; XR=xr[ys-y0]; YT=yt[xs-x0]; YB=yb[xs-x0]
    u=np.clip((xs-XL)/np.maximum(XR-XL,1),0,1)
    v=np.clip((ys-YT)/np.maximum(YB-YT,1),0,1)
    warp=np.stack([ndimage.map_coordinates(da[:,:,k],[v*(Hd-1),u*(Wd-1)],order=1,mode="nearest")
                   for k in range(3)],axis=2)

    sub=out[y0:y1+1, x0:x1+1]
    lum=0.299*sub[:,:,0]+0.587*sub[:,:,1]+0.114*sub[:,:,2]
    p=np.percentile(lum[mask[y0:y1+1, x0:x1+1]],98)
    shade=np.clip(lum/max(p,1),0,1.12)**shade_gamma
    painted=np.clip(warp*shade[:,:,None],0,255)

    alpha=np.zeros((H,W),np.float32); alpha[mask]=1.0
    alpha=np.asarray(Image.fromarray((alpha*255).astype(np.uint8))
                     .filter(ImageFilter.GaussianBlur(1.4)),np.float32)/255.0
    a=alpha[y0:y1+1, x0:x1+1][:,:,None]
    out[y0:y1+1, x0:x1+1]=sub*(1-a)+painted*a
    img=Image.fromarray(np.clip(out,0,255).astype(np.uint8))
    if crop:
        cw,ch,anchor=crop
        cx=(cols[0]+cols[-1])/2; cy=(rows[0]+rows[-1])/2
        L=int(round(cx-cw/2)); T=int(round(cy-ch*anchor))
        L=max(0,min(L,W-cw)); T=max(0,min(T,H-ch))
        img=img.crop((L,T,L+cw,T+ch))
        if out_size and img.size!=tuple(out_size): img=img.resize(tuple(out_size), Image.LANCZOS)
    img.save(out_path, quality=94, subsampling=0)
    return out_path
