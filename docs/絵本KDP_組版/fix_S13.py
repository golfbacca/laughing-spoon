# -*- coding: utf-8 -*-
"""P15 (S13_ドアがあく) の確定修正。生成AIは使わない。
   A) ドア下端を「短いドア」に直す（窓状の切り抜き＝下桟と縦の脚を消す）
   B) 壁を P14 と同じ「大きなタイル1種類」に直す（小タイルの帯を消す）
"""
import numpy as np
from PIL import Image

SRC = "docs/絵本KDP_画像/S13_ドアがあく.jpg"   # ※実行は「修正前」の画像に対して行うこと
OUT = "p15_fixed.png"

orig = np.asarray(Image.open(SRC).convert("RGB")).astype(np.float32)
a = orig.copy()
H, W, _ = a.shape

# ================================================================ A) ドア下端
# ドア下端の「窓のような切り抜き」を消す。下端の線は元のまま残し、
# その下にあった下桟の線と右の縦の脚を、床の画素を引き伸ばして消す。
D = lambda x: 3222.0 - 0.26 * (x - 1610.0)
X0, X1 = 1560, 2078

def src_off(x):
    if x <= 1840: return 60.0
    if x <= 1990: return 60.0 + (x - 1840) * (105.0 - 60.0) / 150.0
    return 105.0 + min(x - 1990, 76) * (150.0 - 105.0) / 76.0

def taper(x):
    l = min(1.0, (x - X0) / 48.0)
    r = min(1.0, (X1 - 1 - x) / 26.0)
    return max(0.0, min(l, r))

FAR = 430.0
for x in range(X0, X1):
    d = D(x)
    y0 = int(round(d + 7))
    ys = int(round(d + max(7.0, src_off(x) * taper(x))))
    yf = min(int(round(d + FAR)), H - 2)
    src = orig[ys:yf, x, :]
    m = yf - y0
    idx = (np.arange(m) / max(m - 1, 1) * (src.shape[0] - 1)).astype(int)
    a[y0:yf, x, :] = src[idx]

# 左右の継ぎ目を横方向にぼかす
for sx in (X0, X1 - 1):
    d = D(sx)
    for y in range(int(d) + 10, min(int(d + FAR), H - 2)):
        seg = a[y, sx - 26:sx + 26, :].copy()
        ker = np.ones(17) / 17.0
        for c in range(3):
            a[y, sx - 26:sx + 26, c] = np.convolve(
                np.pad(seg[:, c], (17, 17), mode="edge"), ker, mode="same")[17:-17]

# ================================================================ B) 壁
def smooth1d(v, k):
    ker = np.ones(k) / k
    pad = np.pad(v, (k, k), mode="edge")
    return np.convolve(pad, ker, mode="same")[k:-k]

WALL = [
    dict(x0=0,    x1=1370, top=lambda x: 1685.0,
         fri=lambda x: 1832.0 + 0.0393 * x,
         bot=lambda x: 2690.0 + 0.1900 * x,
         verts=[290, 680, 1070], pad=16, rows=3),
    dict(x0=3272, x1=4096, top=lambda x: 1694.0,
         fri=lambda x: 1905.0 + 0.0800 * (x - 3300),
         bot=lambda x: 3269.0 + 0.2027 * (x - 3300),
         verts=[3480, 3870], pad=62, rows=4),
]

# B-1 小タイルの帯を消す（帯の上の線は P14 と同じく1本だけ残す）
for w in WALL:
    xs = np.arange(w["x0"], w["x1"])
    base = np.zeros((len(xs), 3), np.float32)
    for i, x in enumerate(xs):
        f = int(round(w["fri"](x)))
        base[i] = np.median(orig[f + 70:f + 150, x, :], axis=0)
    for c in range(3):
        base[:, c] = smooth1d(base[:, c], 121)
    for i, x in enumerate(xs):
        t = int(round(w["top"](x))); f = int(round(w["fri"](x)))
        y0, y1 = t + 6, f + w["pad"]
        n = y1 - y0
        ramp = np.clip(np.linspace(0, 1, n) * 60, 0, 1)[:, None]  # 上端だけ少しなじませる
        a[y0:y1, x, :] = a[y0:y1, x, :] * (1 - ramp) + base[i][None, :] * ramp
        # 下側の継ぎ目をぼかす
        for k in range(20):
            wgt = 1.0 - k / 20.0
            y = y1 + k
            a[y, x, :] = a[y, x, :] * (1 - wgt * 0.85) + base[i] * (wgt * 0.85)

# B-2 P14 と同じ大きなタイルの目地を引く
DELTA = np.array([-24.0, -30.0, -38.0])

def is_wall(px):
    r, g, b = px[0], px[1], px[2]
    return ((r + g + b) / 3.0 > 203) and (r > b + 5) and (r > g + 2)

def stroke(y, x, wgt):
    if 0 <= y < H and 0 <= x < W and is_wall(a[y, x]):
        a[y, x, :] = np.clip(a[y, x, :] + DELTA * wgt, 0, 255)

for w in WALL:
    for x in range(w["x0"], w["x1"]):
        t, b = w["top"](x), w["bot"](x)
        for fr in [k / w["rows"] for k in range(1, w["rows"])]:
            c = t + (b - t) * fr
            for k in range(-3, 4):
                stroke(int(round(c)) + k, x, max(0.0, 1.0 - abs(k) / 3.6))
    for vx in w["verts"]:
        t, b = w["top"](vx), w["bot"](vx)
        for y in range(int(t) + 10, int(b) - 6):
            for k in range(-3, 4):
                stroke(y, vx + k, max(0.0, 1.0 - abs(k) / 3.6))

Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(OUT)
print("saved", OUT)
