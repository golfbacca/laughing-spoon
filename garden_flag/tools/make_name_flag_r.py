"""大きなプレートに「THE / 名字」を2行で合成"""
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
def bbox(d,t,f):
    l,tp,r,b=d.textbbox((0,0),t,font=f); return r-l,b-tp,l,tp

def render(tag, surname, out_dir="named_r"):
    src=f"upload_r/{tag}_upload_3900x5700.png"
    im=Image.open(src).convert("RGB"); d=ImageDraw.Draw(im)
    x0,y0,x1,y1=B[tag]; fn,col,mx,my,rel=CFG[tag]
    maxw=int((x1-x0)*(1-mx*2)); maxh=int((y1-y0)*(1-my*2))
    fp=os.path.join(FD,fn)
    gap_r=0.12                      # 行間＝大文字サイズの12%
    lo,hi,best=10,900,None
    while lo<=hi:
        mid=(lo+hi)//2
        fb=ImageFont.truetype(fp,mid); fs=ImageFont.truetype(fp,max(8,int(mid*rel)))
        w2,h2,_,_=bbox(d,surname,fb); w1,h1,_,_=bbox(d,"THE",fs)
        total_h=h1+int(mid*gap_r)+h2
        if max(w1,w2)<=maxw and total_h<=maxh:
            best=(mid,fb,fs); lo=mid+1
        else: hi=mid-1
    size,fb,fs=best
    w2,h2,ox2,oy2=bbox(d,surname,fb); w1,h1,ox1,oy1=bbox(d,"THE",fs)
    gap=int(size*gap_r); total=h1+gap+h2
    cx=(x0+x1)//2; top=(y0+y1)//2-total//2
    d.text((cx-w1//2-ox1, top-oy1), "THE", font=fs, fill=col)
    d.text((cx-w2//2-ox2, top+h1+gap-oy2), surname, font=fb, fill=col)
    os.makedirs(out_dir, exist_ok=True)
    p=f"{out_dir}/{tag}_{surname}_3900x5700.png"; im.save(p, optimize=True)
    return size, int(size*rel)

SUR = sys.argv[1] if len(sys.argv)>1 else "SMITHS"
print(f"合成する名字: 「THE {SUR}」\n")
print(f"{'案':<5}{'フォント':<22}{'名字':>9}{'THE':>8}")
print("-"*46)
for t in ["R01","R02","R05","R09","R11"]:
    a,b=render(t,SUR); print(f"{t:<5}{CFG[t][0]:<22}{a:>7}px{b:>6}px")
