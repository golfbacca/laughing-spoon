#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S01「ねるまえ」で、ミオがTシャツ＋半ズボンになっているのを
スモック（ふともも丈の一枚もの）に直す。

  python3 fix_s01_smock.py            # 上書き
  python3 fix_s01_smock.py --out DIR  # 試し書き

やり方（生成し直さない。作業記録16章）:
  1. 輪郭線で囲まれた領域として【半ズボン】を切り出す
     色ではシャツと分けられない。あかりの強い暖色に照らされていて、
     オリーブのシャツと淡い黄のズボンの RGB がほぼ重なるため。
     線で切るとひと息で分かれる。
  2. ズボンをシャツの色に置き換える
     左が明るく右が暗い照明の勾配があるので、単一の色で塗らない。
     【列ごとに】すぐ上のシャツの色を見本にしてずらす。
  3. 腰の縫い目（シャツの裾線）を消して一枚につなげる
     消すのは【内側の線だけ】。外側の輪郭線は服の形なので残す。
"""
import sys, pathlib
import numpy as np
from PIL import Image
from scipy import ndimage

IMG = pathlib.Path(__file__).resolve().parents[1] / "絵本KDP_3冊目_画像"
NAME = "S01_ねるまえ"

# 調べる範囲と種の点（画像を 0..1 で正規化）
BOX = (.30, .58, .46, .72)
SEED_SHORTS = (.400, .665)
SEED_SHIRT = (.420, .560)


def regions(a):
    h, w, _ = a.shape
    x0, x1 = int(BOX[0] * w), int(BOX[1] * w)
    y0, y1 = int(BOX[2] * h), int(BOX[3] * h)
    v = a[y0:y1, x0:x1].mean(axis=2).astype(np.float32)
    loc = ndimage.uniform_filter(v, size=41)
    lab, _ = ndimage.label(v > (loc - 18))
    dark = v < (loc - 18)

    def pick(seed):
        sy, sx = int(seed[1] * h) - y0, int(seed[0] * w) - x0
        k = lab[sy, sx]
        if k == 0:
            raise ValueError("種の点が線の上にある")
        return lab == k

    return (x0, y0), pick(SEED_SHORTS), pick(SEED_SHIRT), dark


def main(out_dir=None):
    p = IMG / f"{NAME}.jpg"
    a = np.asarray(Image.open(p).convert("RGB"), dtype=np.float32)
    h, w, _ = a.shape
    (ox, oy), shorts, shirt, dark = regions(a)

    full_s = np.zeros((h, w), bool)
    full_s[oy:oy + shorts.shape[0], ox:ox + shorts.shape[1]] = shorts
    full_t = np.zeros((h, w), bool)
    full_t[oy:oy + shirt.shape[0], ox:ox + shirt.shape[1]] = shirt
    full_d = np.zeros((h, w), bool)
    full_d[oy:oy + dark.shape[0], ox:ox + dark.shape[1]] = dark

    ys, xs = np.nonzero(full_s)
    cx0, cx1 = xs.min(), xs.max() + 1

    # --- 2. 列ごとに、すぐ上のシャツの色を見本にしてずらす -------------
    out = a.copy()
    off = np.full((w, 3), np.nan, np.float32)
    for x in range(cx0, cx1):
        col_s = np.nonzero(full_s[:, x])[0]
        if len(col_s) < 30:
            continue
        top = col_s.min()
        band = np.nonzero(full_t[max(0, top - 420):top - 20, x])[0]
        if len(band) < 40:
            continue
        band += max(0, top - 420)
        ref = a[band, x, :].mean(axis=0)
        cur = a[col_s, x, :].mean(axis=0)
        off[x] = ref - cur
    # 欠けている列は前後から埋め、なだらかにする
    for c in range(3):
        col = off[:, c]
        idx = np.nonzero(~np.isnan(col))[0]
        if len(idx) == 0:
            raise SystemExit("見本になるシャツの画素が見つからない")
        col[:] = np.interp(np.arange(w), idx, col[idx])
        off[:, c] = ndimage.uniform_filter1d(col, 220)
    for c in range(3):
        ch = out[:, :, c]
        ch[full_s] = (a[:, :, c] + off[:, c][None, :])[full_s]

    # --- 3. 腰の縫い目（内側の線）だけ消す ----------------------------
    # 上にシャツ、下にズボンがある暗い画素＝内側の縫い目
    # 【つまずき】上下 90px で探したら、ふとももの輪郭や背景の線まで
    # 「挟まれている」と判定され、消した跡が帯状ににじんだ。
    # 縫い目は服の中の細い線なので、探す幅は狭く、
    # 横もズボンの左右幅の中だけに限る。
    up = ndimage.binary_dilation(full_t, np.ones((34, 1)))
    dn = ndimage.binary_dilation(full_s, np.ones((34, 1)))
    seam = full_d & up & dn
    band = np.zeros_like(seam)
    band[:, cx0:cx1] = True
    seam &= band
    seam = ndimage.binary_dilation(seam, np.ones((5, 5)))
    seam &= ~full_t & ~full_s        # 領域そのものは触らない
    if seam.any():
        sy, sx = np.nonzero(seam)
        y0s, y1s = max(0, sy.min() - 60), min(h, sy.max() + 60)
        x0s, x1s = max(0, sx.min() - 60), min(w, sx.max() + 60)
        tile = out[y0s:y1s, x0s:x1s].copy()
        mk = seam[y0s:y1s, x0s:x1s]
        ring = ndimage.binary_dilation(mk, np.ones((17, 17))) & ~mk
        for c in range(3):
            ch = tile[:, :, c]
            ch[mk] = ch[ring].mean()
            for _ in range(160):
                ch[mk] = ndimage.uniform_filter(ch, size=3)[mk]
            tile[:, :, c] = ch
        out[y0s:y1s, x0s:x1s] = tile

    dst = (pathlib.Path(out_dir) / f"{NAME}.jpg") if out_dir else p
    Image.fromarray(np.clip(out, 0, 255).astype("uint8")).save(dst, quality=95)
    print(f"  ズボン {full_s.sum()}px を塗り替え、縫い目 {seam.sum()}px を消した")
    print(f"  → {dst}")


if __name__ == "__main__":
    d = None
    if "--out" in sys.argv:
        d = sys.argv[sys.argv.index("--out") + 1]
    main(d)
