from PIL import Image, ImageDraw
import numpy as np, os, glob
OUT="upload_r"; os.makedirs(OUT, exist_ok=True)
CW,CH=3900,5700; BLEED=150; SLEEVE=600; PAD=120
def bg_color(a):
    h,w,_=a.shape; m=max(2,int(min(h,w)*0.02))
    ring=np.concatenate([a[:m].reshape(-1,3),a[-m:].reshape(-1,3),a[:,:m].reshape(-1,3),a[:,-m:].reshape(-1,3)])
    q=(ring//8*8); v,c=np.unique(q,axis=0,return_counts=True); return v[c.argmax()].astype(int)
def cbox(a,bg,tol=26,frac=0.02):
    h,w,_=a.shape; d=np.abs(a.astype(int)-bg).max(axis=2)>tol
    t=next((y for y in range(h) if d[y].mean()>frac),0); b=next((y for y in range(h-1,-1,-1) if d[y].mean()>frac),h-1)
    l=next((x for x in range(w) if d[:,x].mean()>frac),0); r=next((x for x in range(w-1,-1,-1) if d[:,x].mean()>frac),w-1)
    return l,t,r+1,b+1

print(f"{'案':<5}{'背景色':>16}{'元の上端':>9}{'左':>6}{'右':>6}{'下':>6}{'端接触':>8}{'倍率':>7}{'配置後の上端':>13}")
print("-"*82)
for f in sorted(glob.glob("zin/R*.jpeg")):
    tag=os.path.basename(f)[:3]
    im=Image.open(f).convert("RGB"); a=np.asarray(im); bg=bg_color(a); W,H=im.size
    l,t,r,b=cbox(a,bg)
    touch=(l<=1) or (r>=W-1)
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
    pv=cv.copy(); d=ImageDraw.Draw(pv,"RGBA")
    d.rectangle([0,0,CW,BLEED+SLEEVE],fill=(255,0,0,70))
    d.rectangle([BLEED,BLEED,CW-BLEED,CH-BLEED],outline=(0,90,255,255),width=10)
    pv.resize((CW//6,CH//6),Image.LANCZOS).save(f"{OUT}/pv_{tag}.png")
    print(f"{tag:<5}{str(tuple(bg)):>16}{t/H*100:>8.1f}%{l/W*100:>5.1f}%{(W-r)/W*100:>5.1f}%{(H-b)/H*100:>5.1f}%{('はい' if touch else 'いいえ'):>8}{s:>7.2f}{py+nt:>12}px")
