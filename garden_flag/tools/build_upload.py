"""
ガーデンフラッグ入稿データ生成（3900 x 5700 / 300DPI）

Geminiが出力した縦長デザインを、Printify Garden Flag 12"x18" の
入稿仕様に合わせて配置する。

仕様:
  キャンバス 3900 x 5700
  塗り足し   外周150px（裁ち落とされる）
  スリーブ   仕上がり上端から600px（ポールに巻き込まれて見えない）
  → 上端750px + 安全余白60px = y=810 より下に中身を置く

2種類の配置戦略を自動で切り替える:
  (A) デザインが画像の左右端に届いていない場合
      → 安全域（x 270..3630）に収め、周囲はエッジ複製で埋める
        エッジが背景色なので継ぎ目が出ない。N02の縦縞も保たれる
  (B) デザインが左右端まで届いている場合
      → 全幅を使い、はみ出しは裁ち落とし前提。周囲は背景色でベタ埋め
        エッジ複製すると端の花や細い枠線が横に伸びるため（N05/N10で実際に発生）

必要: Pillow, numpy
"""
from PIL import Image, ImageDraw
import numpy as np, os
SRC="/tmp/claude-0/-home-user-laughing-spoon/93443bf2-c53d-5794-b24f-ada73ab7b2e0/images"
OUT="upload"; os.makedirs(OUT, exist_ok=True)
F=[("N01","5.webp"),("N02","6.webp"),("N05","7.webp"),("N09","3.webp"),("N10","4.webp")]

CW,CH=3900,5700; BLEED=150; SLEEVE=600; PAD=120
def bg_color(a):
    h,w,_=a.shape; m=max(2,int(min(h,w)*0.02))
    ring=np.concatenate([a[:m].reshape(-1,3),a[-m:].reshape(-1,3),a[:,:m].reshape(-1,3),a[:,-m:].reshape(-1,3)])
    q=(ring//8*8); v,c=np.unique(q,axis=0,return_counts=True); return v[c.argmax()].astype(int)
def content_box(a,bg,tol=26,frac=0.02):
    h,w,_=a.shape; d=np.abs(a.astype(int)-bg).max(axis=2)>tol
    t=next((y for y in range(h) if d[y].mean()>frac),0); b=next((y for y in range(h-1,-1,-1) if d[y].mean()>frac),h-1)
    l=next((x for x in range(w) if d[:,x].mean()>frac),0); r=next((x for x in range(w-1,-1,-1) if d[:,x].mean()>frac),w-1)
    return l,t,r+1,b+1

print(f"{'案':<6}{'端に接触':>12}{'横の使い方':>16}{'倍率':>7}{'中身の上端':>11}{'下端':>9}")
print("-"*66)
for n,f in F:
    im=Image.open(os.path.join(SRC,f)).convert("RGB"); a=np.asarray(im); bg=bg_color(a)
    l,t,r,b=content_box(a,bg); W,H=im.size
    touch = (l<=1) or (r>=W-1)          # デザインが左右端まで届いているか
    # 左右端まで届く案は「裁ち落とし前提」で全幅を使う。届かない案は安全域に収める
    x0,x1 = (0,CW) if touch else (BLEED+PAD, CW-BLEED-PAD)
    y0,y1 = BLEED+SLEEVE+60, CH-(BLEED if touch else BLEED+PAD)
    cw,ch=r-l,b-t
    s=min((x1-x0)/cw, (y1-y0)/ch)
    nw,nh=int(round(W*s)),int(round(H*s))
    big=im.resize((nw,nh), Image.LANCZOS)
    nl,nt=int(round(l*s)),int(round(t*s)); ncw,nch=int(round(cw*s)),int(round(ch*s))
    px = x0 + ((x1-x0)-ncw)//2 - nl
    py = y0 + ((y1-y0)-nch)//2 - nt
    # 端に接触する案は「背景色でベタ埋め」、しない案は「エッジ複製」
    if touch:
        canvas=Image.new("RGB",(CW,CH),tuple(bg)); canvas.paste(big,(px,py))
    else:
        arr=np.asarray(big)
        pt,pl=max(0,py),max(0,px); pb,pr=max(0,CH-(py+nh)),max(0,CW-(px+nw))
        p=np.pad(arr,((pt,pb),(pl,pr),(0,0)),mode="edge")
        canvas=Image.fromarray(p[max(0,-py):max(0,-py)+CH, max(0,-px):max(0,-px)+CW])
    canvas.save(f"{OUT}/{n}_upload_3900x5700.png", optimize=True)
    ct,cb = py+nt, py+nt+nch
    pv=canvas.copy(); d=ImageDraw.Draw(pv,"RGBA")
    d.rectangle([0,0,CW,BLEED+SLEEVE],fill=(255,0,0,70))
    d.rectangle([BLEED,BLEED,CW-BLEED,CH-BLEED],outline=(0,90,255,255),width=10)
    pv.resize((CW//6,CH//6),Image.LANCZOS).save(f"{OUT}/preview_{n}.png")
    print(f"{n:<6}{('はい' if touch else 'いいえ'):>12}{('全幅(裁ち落とし)' if touch else '安全域に収める'):>16}{s:>7.2f}{ct:>10}px{cb:>8}px")
