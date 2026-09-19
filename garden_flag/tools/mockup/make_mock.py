# -*- coding: utf-8 -*-
"""出品用モックアップを作る。
   ・Etsyの検索一覧は 4:3 で中央を切るので、最初から 4:3 / 2000x1500 で出す
   ・旗が枠の高さの80%を占めるように、背景の拡大率を写真ごとに決める
     （旗そのものは3600x5400の原寸デザインから描くので、拡大しても鮮明なまま）
"""
from composite import composite
import numpy as np, glob, os, re
os.makedirs("mock", exist_ok=True)
OUT_W,OUT_H = 2000,1500
FLAG_RATIO = 0.80                 # 旗の高さ / 枠の高さ
ANCHOR     = 0.46                 # 旗の中心を置く縦位置

def flag_height(mask_path):
    m=np.load(mask_path); iy=np.arange(m.shape[0])
    cols=np.where(m.any(0))[0]
    return float(np.median([iy[m[:,x]].max()-iy[m[:,x]].min() for x in cols]))

designs={re.match(r"(R\d+)",os.path.basename(p)).group(1):p for p in sorted(glob.glob("named_r/*.png"))}
for bg in ("background01","background02","background03"):
    mp=f"mask_{bg}.npy"
    sc=OUT_H*FLAG_RATIO/flag_height(mp)
    print(f"\n{bg}: 旗の高さ {flag_height(mp):.0f}px → 背景を {sc:.2f}倍 (旗が枠の{FLAG_RATIO:.0%})")
    for code,dp in designs.items():
        composite(f"zin/{bg}.jpeg", dp, mp, f"mock/{code}_{bg[-2:]}.jpg",
                  scale=sc, crop=(OUT_W,OUT_H,ANCHOR), verbose=(code=="R01"))
print("\n", len(glob.glob("mock/R*.jpg")), "枚")
