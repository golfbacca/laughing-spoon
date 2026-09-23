# -*- coding: utf-8 -*-
"""R09（赤と緑のタータン枠）の柄の規則性を測る。

  使い方: python3 check_tartan.py <Geminiが出した画像> [...]

タータンは織物なので、**四辺すべてが同じ周期**でなければならない。
縦と横で周期が違う／途中で周期が変わる／ブロックが抜ける、は全部欠陥。

やりかた:
  1. 緑の画素だけを取り出す（タータンの緑）
  2. 外周の四辺それぞれで、緑のブロックの位置と幅を測る
  3. 一辺の中のばらつきと、四辺どうしの食い違いを数値で出す

判定:
  四辺の周期の食い違い  10% 以内
  一辺の中のばらつき    25% 以内     両方みたせば合格
"""
from PIL import Image
import numpy as np
import sys, os, statistics as st

def blocks(sig, minrun):
    on=sig>0.45
    out=[]; s=0
    for i in range(1,len(on)):
        if on[i]!=on[i-1]: out.append((bool(on[s]),s,i-s)); s=i
    out.append((bool(on[s]),s,len(on)-s))
    return [(p,l) for t,p,l in out if t and l>=minrun]

def side(gmask, axis, lo, hi, minrun, label, wide_only=True):
    sig = gmask[:, lo:hi].mean(axis=1) if axis==0 else gmask[lo:hi, :].mean(axis=0)
    b=blocks(sig, minrun)
    if wide_only and b:
        lm=max(l for _,l in b)
        b=[(p,l) for p,l in b if l>=lm*0.55]          # 細い罫線は除き、広いブロックだけ見る
    if len(b)<4: return None
    starts=[p for p,_ in b]
    gaps=[starts[i+1]-starts[i] for i in range(len(starts)-1)]
    # 間隔を「短い」「長い」の2群に分ける。規則正しいタータンは各群がよく揃う
    mid=(min(gaps)+max(gaps))/2
    shortg=[x for x in gaps if x<=mid] or gaps
    longg =[x for x in gaps if x> mid] or gaps
    def dev(v):
        m=st.median(v); return m, (max(abs(x-m) for x in v)/m*100 if m else 0)
    sm,sd=dev(shortg); lm,ld=dev(longg)
    return dict(label=label, n=len(b), gaps=gaps,
                short=sm, short_dev=sd, long=lm, long_dev=ld,
                period=sm+lm, dev=max(sd,ld))

def check(path):
    im=Image.open(path).convert("RGB")
    a=np.asarray(im).astype(int); H,W,_=a.shape
    R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]
    g=((G>R+12)&(G<180)&(R<160)).astype(float)
    def band(dens, limit):
        """外周から見て、柄の密度が高い連続範囲＝枠の帯"""
        d=dens[:limit]
        pk=int(np.argmax(d)); th=d[pk]*0.35
        lo=pk
        while lo>0 and d[lo-1]>th: lo-=1
        hi=pk
        while hi<limit-1 and d[hi+1]>th: hi+=1
        return lo,hi+1
    colden=g.mean(axis=0); rowden=g.mean(axis=1)
    lx0,lx1=band(colden, W//3)
    rx1,rx0=[W-v for v in band(colden[::-1], W//3)]
    ty0,ty1=band(rowden, H//4)
    by1,by0=[H-v for v in band(rowden[::-1], H//4)]
    mr_v=max(4,int(H*0.012)); mr_h=max(4,int(W*0.012))
    res=[r for r in (
        side(g,0,lx0,lx1,mr_v,f"左帯(縦) x{lx0}-{lx1}"),
        side(g,0,rx0,rx1,mr_v,f"右帯(縦) x{rx0}-{rx1}"),
        side(g,1,ty0,ty1,mr_h,f"上バー(横) y{ty0}-{ty1}"),
        side(g,1,by0,by1,mr_h,f"下バー(横) y{by0}-{by1}")) if r]
    print(f"\n=== {os.path.basename(path)}  {W}x{H} ===")
    if len(res)<3:
        print("  緑のタータンを検出できず。画像が違うかもしれない"); return None
    for r in res:
        print(f"  {r['label']:<22}: ブロック{r['n']:>2}個  短い間隔 {r['short']:>6.1f}px(±{r['short_dev']:>5.1f}%)"
              f"  長い間隔 {r['long']:>6.1f}px(±{r['long_dev']:>5.1f}%)  1周期 {r['period']:>6.1f}px")
        print(f"      間隔: {[int(x) for x in r['gaps']]}")
    meds=[r['period'] for r in res]
    spread=(max(meds)-min(meds))/st.median(meds)*100
    worst=max(r['dev'] for r in res)
    print(f"\n  四辺の1周期の食い違い: {spread:>5.1f} %   （10%以内なら合格）")
    print(f"  一辺の中のばらつき   : {worst:>5.1f} %   （25%以内なら合格）")
    ok = spread<=10 and worst<=25
    print(f"  判定: {'✅ 合格' if ok else '❌ 不合格 — 作り直し'}")
    return ok

if __name__=="__main__":
    for f in sys.argv[1:]: check(f)
