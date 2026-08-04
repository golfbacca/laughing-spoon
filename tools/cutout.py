# -*- coding: utf-8 -*-
"""白背景のキャラ画像を透過PNGにする。
地の色がクリーム（白に近い）なので、明度の閾値では体まで消える。
四隅から連結領域を塗りつぶして「外側の白」だけを背景と判定する。"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter
from collections import deque

SRC="charA"; DST="charA_cut"
os.makedirs(DST, exist_ok=True)
TOL = 26          # 白との距離のしきい値
FEATHER = 0.8     # 縁のなじませ

def cut(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    # 白からの距離
    dist = np.sqrt(((255 - a) ** 2).sum(axis=2))
    near_white = dist <= TOL
    # 四隅・四辺から連結成分を辿る（外側の白だけを背景にする）
    bg = np.zeros((h, w), dtype=bool)
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if near_white[y, x] and not bg[y, x]: bg[y, x] = True; dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if near_white[y, x] and not bg[y, x]: bg[y, x] = True; dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = y+dy, x+dx
            if 0 <= ny < h and 0 <= nx < w and near_white[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True; dq.append((ny, nx))
    # 生成時のノイズで、白から少し外れた画素が縁に点在する。
    # しきい値を上げると地のクリーム（白との距離31）まで巻き込むので、
    # 上げずに「外周の孤立した点」だけを落とす。
    bg[:3, :] = True; bg[-3:, :] = True; bg[:, :3] = True; bg[:, -3:] = True

    # 外側から辿れない閉じた白領域が3種類できる。扱いを分ける必要がある。
    #   (a) ヘッドバンドと頭の隙間 … 抜く。画像面積の約1.7%と大きい
    #   (b) コードの巻きの内側     … 抜く。背景が透けるべき場所
    #   (c) 歯・目のハイライト     … 残す。白いままでないと不気味になる
    # (b)と(c)は面積が重なる（どちらも0.03%前後）ので大きさでは分けられない。
    # (b)は細いコードで囲まれているだけなので、少し膨らませると背景に接する。
    # (c)は顔の内側にあるので接しない。これで判別する。
    strict = (dist <= 14) & ~bg
    AREA_BIG = 0.008 * h * w      # (a)の判定。画像の大きさに比例させる
    R = 8                          # 膨張させる画素数
    seen = np.zeros((h, w), dtype=bool)
    ys, xs = np.nonzero(strict)
    for sy, sx in zip(ys, xs):
        if seen[sy, sx]: continue
        comp = []; q = deque([(sy, sx)]); seen[sy, sx] = True
        while q:
            y, x = q.popleft(); comp.append((y, x))
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny, nx = y+dy, x+dx
                if 0 <= ny < h and 0 <= nx < w and strict[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; q.append((ny, nx))
        drop = len(comp) >= AREA_BIG
        if not drop:
            ay = [p[0] for p in comp]; ax = [p[1] for p in comp]
            y0, y1 = max(0, min(ay)-R-1), min(h, max(ay)+R+2)
            x0, x1 = max(0, min(ax)-R-1), min(w, max(ax)+R+2)
            m = np.zeros((y1-y0, x1-x0), dtype=bool)
            for y, x in comp: m[y-y0, x-x0] = True
            for _ in range(R):                       # 4近傍で膨張
                m[1:, :] |= m[:-1, :]; m[:-1, :] |= m[1:, :]
                m[:, 1:] |= m[:, :-1]; m[:, :-1] |= m[:, 1:]
            drop = bool((m & bg[y0:y1, x0:x1]).any())  # 背景に接したら(b)
        if drop:
            for y, x in comp: bg[y, x] = True

    alpha = np.where(bg, 0, 255).astype(np.uint8)
    out = Image.fromarray(np.dstack([np.asarray(im), alpha]), "RGBA")
    # 縁のジャギをなじませる
    al = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(FEATHER))
    out.putalpha(al)
    bb = out.getchannel("A").getbbox()
    return out.crop(bb) if bb else out

rows=[]
for f in sorted(os.listdir(SRC)):
    if not f.lower().endswith(".png"): continue
    im = cut(os.path.join(SRC, f))
    im.save(os.path.join(DST, f))
    rows.append((f, im.width, im.height))
print(f"{'file':22s} {'切り抜き後':>14s}  縦横比")
for f,w,h in rows:
    print(f"{f:22s} {w:5d}x{h:<5d}   {w/h:.2f}")
hs=[h for n,_,h in rows if not n.startswith("KAKUTEI")]
print(f"\n高さのばらつき: 最小{min(hs)} 最大{max(hs)}  → 合成時に正規化する")
