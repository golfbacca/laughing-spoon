# -*- coding: utf-8 -*-
"""補修後の R09 から 名入れ3種 → モックアップ3枚 → 出品画像7枚 を作り直す"""
import importlib, sys
sys.argv=["x","SMITHS"]
import make_name_flag_r as M
for sur in ("SMITHS","MILLERS","ANDERSONS"):
    a,b=M.render("R09",sur); print(f"  名入れ R09 {sur}: 名字{a}px THE{b}px", flush=True)
from composite import composite
import numpy as np
OUT_W,OUT_H,FLAG,ANCH=2000,1500,0.80,0.46
def fh(mp):
    m=np.load(mp); iy=np.arange(m.shape[0]); cols=np.where(m.any(0))[0]
    return float(np.median([iy[m[:,x]].max()-iy[m[:,x]].min() for x in cols]))
for bg in ("background01","background02","background03"):
    mp=f"mask_{bg}.npy"
    composite(f"zin/{bg}.jpeg","named_r/R09_SMITHS_3900x5700.png",mp,
              f"mock/R09_{bg[-2:]}.jpg", scale=OUT_H*FLAG/fh(mp), crop=(OUT_W,OUT_H,ANCH), verbose=False)
    print(f"  モックアップ R09 x {bg}", flush=True)
import listing_img as L
d="listing/R09_gone-golfing"
import shutil, os
os.makedirs(d, exist_ok=True)
shutil.copy("mock/R09_03.jpg", f"{d}/1_main.jpg")
L.img_personalize("R09",         f"{d}/2_personalize.jpg")
shutil.copy("mock/R09_01.jpg",   f"{d}/3_scene.jpg")
L.img_closeup("mock/R09_03.jpg", f"{d}/4_closeup.jpg","SOFT, FADE-RESISTANT FABRIC")
L.img_size("R09",                f"{d}/5_size.jpg")
L.img_double("R09",              f"{d}/6_double_sided.jpg")
L.img_notice("R09",              f"{d}/7_flag_only.jpg")
print("  出品画像7枚 完了", flush=True)
