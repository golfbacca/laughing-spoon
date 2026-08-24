# -*- coding: utf-8 -*-
"""P13（09_場面08_ノック）の確定修正。生成AIは使わない。

【診断】
  壁と床の境目（幅木の下端の線）は y≈3500。ドア枠の足元 y≈3520 と一致していて、
  壁とドアの側は互いに整合している。
  一方トトンの足は y≈3420、ミオの足は y≈3430、2人の影は y≈3370-3465。
  2人と影が境目より上にあるので、床ではなく壁の中に立っていることになり、
  宙に浮いて見える。

【直し方】
  キャラは1ピクセルも触らない。壁と床の境目のほうを 150px 引き上げる。
   A) ドアの左（x<1200。キャラがいない）は y>=3120 をまとめて 150px 持ち上げる。
      これで壁のタイル下端の線・幅木の線・ドア枠の足元・枠の影が一緒に上がる。
   B) ドアの右（x>=2308）は、キャラが重なるので線だけを引き直す。
      古い線を消し、タイル下端の線を 150px 上に写し、
      幅木の下端の線は左側の実物の画素を写して同じ高さに引く。
      キャラに重なる画素には描かない（線はキャラの後ろを通る）。
  結果、境目は y≈3350 になり、足も影も境目より下＝床の上になる。
"""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SRC = "p13_prev.jpg"   # ← commit b257987 時点の 09_場面08_ノック.jpg
OUT = "p13_fixed5.png"
DY  = 150

orig = np.asarray(Image.open(SRC).convert("RGB")).astype(np.float32)
a = orig.copy()
H, W, _ = orig.shape
lum = orig.mean(axis=2)

# ---------------------------------------------------------------- A) 左側
LX1, AY0 = 1200, 3120
strip = orig[AY0 + DY:, :LX1, :]
a[AY0:H - DY, :LX1, :] = strip
a[H - DY:, :LX1, :] = orig[H - 1, :LX1, :][None, :, :]

# ---------------------------------------------------------------- B) 右側
RX0 = 2308

# キャラだけの面（横に細長い線は縦方向の opening で落とす）
free = lum >= 168
lab, _ = ndi.label(free)
border = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1]); border.discard(0)
inside = ~np.isin(lab, list(border))
lab2, n2 = ndi.label(inside)
sizes = ndi.sum(inside, lab2, range(1, n2 + 1))
big = np.isin(lab2, [i + 1 for i, s in enumerate(sizes) if s > 120000])
chars = ndi.binary_opening(big, structure=np.ones((61, 1)))
chars = ndi.binary_dilation(ndi.binary_fill_holes(chars), iterations=10)

# B-1 新しいタイル下端の線より下に残る「古い線」と「縦の目地の続き」を消す。
#     影（y>=3376）には触らない。
EY0, EY1 = 3182, 3388
# 帯の中の線（古いタイル下端の線・縦の目地の続き）を、
# モルフォロジーの closing で消す。壁のむらは残るので継ぎ目が出ない。
band = orig[EY0:EY1, RX0:W, :].copy()
closed = band.copy()
for c in range(3):
    closed[:, :, c] = ndi.grey_closing(closed[:, :, c], size=(71, 1))
    closed[:, :, c] = ndi.grey_closing(closed[:, :, c], size=(1, 71))
ramp = np.ones(EY1 - EY0, np.float32)
ramp[:24] = np.linspace(0, 1, 24)
ramp[-24:] = np.linspace(1, 0, 24)
w = ramp[:, None] * (~chars[EY0:EY1, RX0:W])
a[EY0:EY1, RX0:W, :] = band * (1 - w[..., None]) + closed * w[..., None]

# B-2 タイル下端の線を 150px 上へ写す（線の濃さだけを重ねる）
S0, S1 = 3296, 3384
seg2 = orig[S0:S1, RX0:W, :]
bg2 = np.percentile(seg2.mean(axis=2), 88, axis=0)[None, :]
al2 = np.clip((bg2 - seg2.mean(axis=2) - 6.0) / 60.0, 0, 1)
# 写す元にキャラ（靴）が写り込んでいる列はそのまま使うと、
# 靴の先が 150px 上の空中に写ってしまう。
# その列は「一番近い、キャラの写っていない列」の画素で代用する。
valid = ~chars[S0:S1, RX0:W].any(axis=0)
vi = np.where(valid)[0]
xs_all = np.arange(W - RX0)
pos = np.clip(np.searchsorted(vi, xs_all), 1, len(vi) - 1)
lo, hi = vi[pos - 1], vi[pos]
nearest = np.where(xs_all - lo <= hi - xs_all, lo, hi)
seg2 = seg2[:, nearest, :]
al2 = al2[:, nearest]
al2 *= ~chars[S0 - DY:S1 - DY, RX0:W]
dst = a[S0 - DY:S1 - DY, RX0:W, :]
a[S0 - DY:S1 - DY, RX0:W, :] = dst * (1 - al2[..., None]) + seg2 * al2[..., None]

# B-3 幅木の下端の線を、左側の実物の画素から写して同じ高さに引く
SY0, SY1, SX0, SX1 = 3486, 3530, 30, 470
src = orig[SY0:SY1, SX0:SX1, :]
sl = src.mean(axis=2)
alpha = np.clip((np.percentile(sl, 92) - sl) / 95.0, 0, 1)
n = SX1 - SX0
period = 2 * n - 2
DEST_Y = SY0 - DY
for i, x in enumerate(range(RX0, W)):
    kk = i % period
    sx = kk if kk < n else period - kk
    ca = alpha[:, sx]
    for j in range(SY1 - SY0):
        y = DEST_Y + j
        if chars[y, x]:
            continue
        a[y, x, :] = a[y, x, :] * (1 - ca[j]) + src[j, sx, :] * ca[j]

Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(OUT)
print("saved", OUT)
