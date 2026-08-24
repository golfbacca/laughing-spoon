# -*- coding: utf-8 -*-
"""P13（09_場面08_ノック）の確定修正。生成AIは使わない。
   ドアの右側の壁に、左側にだけあった「幅木の下端の線」を継ぎ足す。
   線は左側の実際の筆致をそのまま横へ写して使う（描き足しではない）。
"""
import numpy as np
from PIL import Image

SRC = "docs/絵本KDP_画像/09_場面08_ノック.jpg"   # ※実行は「修正前」の画像に対して行うこと
OUT = "p13_fixed.png"

orig = np.asarray(Image.open(SRC).convert("RGB")).astype(np.float32)
a = orig.copy()
H, W, _ = a.shape

Y0, Y1 = 3488, 3540          # 線を含む帯
SX0, SX1 = 30, 470           # 左側の見本（ドアの左の幅木の下端）
DX0, DX1 = 2318, 4096        # 貼る先（ドア枠の右外側から画面右端まで）

src = orig[Y0:Y1, SX0:SX1, :]
src_lum = src.mean(axis=2)
bg = np.percentile(src_lum, 92)          # 線でない部分の明るさ
alpha = np.clip((bg - src_lum) / 95.0, 0.0, 1.0)   # 線のところだけ濃い

n = SX1 - SX0
period = 2 * n - 2                      # 折り返して繰り返す（継ぎ目が出ない）
for i, x in enumerate(range(DX0, DX1)):
    k = i % period
    sx = k if k < n else period - k
    col_a = alpha[:, sx][:, None]
    dst = a[Y0:Y1, x, :]
    keep = (dst.mean(axis=1) < 205)[:, None]        # キャラの輪郭には乗せない
    a[Y0:Y1, x, :] = np.where(keep, dst,
                              dst * (1 - col_a) + src[:, sx, :] * col_a)

Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(OUT)
print("saved", OUT)
