"""参考画像の黒い形を n×n のマス目に落とす。
使い方: from_image.grid_from(path, n=30, cut_top=0.0, xstretch=1.0, th=0.45)
  cut_top  … 形の上側をどれだけ切り落とすか（細い相輪などを短くする）
  xstretch … 横に引き伸ばす倍率
  th       … マスの中の黒い画素の割合がこれ以上なら黒"""
from PIL import Image
import numpy as np


def grid_from(path, n=30, cut_top=0.0, xstretch=1.0, th=0.45, dark=90, crop=None):
    a = np.asarray(Image.open(path).convert("L")).astype(float)
    if crop:
        a = a[crop[1]:crop[3], crop[0]:crop[2]]
    m = a < dark
    ys, xs = np.where(m)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    y0 = int(y0 + (y1 - y0) * cut_top)
    m = m[y0:y1, x0:x1]
    h, w = m.shape
    cell = max(h / n, w * xstretch / n)            # 1マスあたりの画素数（縦）
    cw = cell / xstretch                           # 同（横）
    cols, rows = int(round(w / cw)), int(round(h / cell))
    g = [[False] * n for _ in range(n)]
    ox, oy = (n - cols) // 2, n - rows              # 横は中央、縦は下ぞろえ
    for r in range(rows):
        for c in range(cols):
            blk = m[int(r * cell):max(int((r + 1) * cell), int(r * cell) + 1), int(c * cw):max(int((c + 1) * cw), int(c * cw) + 1)]
            if blk.size and blk.mean() >= th:
                g[oy + r][ox + c] = True
    return g
