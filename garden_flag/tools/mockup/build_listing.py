# -*- coding: utf-8 -*-
"""5商品 × 出品画像7枚 を書き出す"""
import listing_img as L
from PIL import Image
import os, shutil

CODES=["R01","R02","R05","R09","R11"]
NAME={"R01":"still-working-on-it","R02":"19th-hole","R05":"mulligans",
      "R09":"gone-golfing","R11":"members-only"}
SUB={"R01":"yard","R02":"door","R05":"yard","R09":"door","R11":"door"}   # 2枚目の風景
CLOSE_LABEL="100% POLY POPLIN-CANVAS"
OUT="listing"
os.makedirs(OUT,exist_ok=True)
for c in CODES:
    d=f"{OUT}/{c}_{NAME[c]}"; os.makedirs(d,exist_ok=True)
    shutil.copy(f"mock/{c}_03.jpg", f"{d}/1_main.jpg")                    # コース背景
    L.img_personalize(c,           f"{d}/2_personalize.jpg")
    shutil.copy(f"mock/{c}_{'01' if SUB[c]=='yard' else '02'}.jpg",
                                   f"{d}/3_scene.jpg")
    L.img_closeup(f"mock/{c}_03.jpg", f"{d}/4_closeup.jpg", CLOSE_LABEL)
    L.img_size(c,                  f"{d}/5_size.jpg")
    L.img_double(c,                f"{d}/6_double_sided.jpg")
    L.img_notice(c,                f"{d}/7_flag_only.jpg")
    print(c, "→", len(os.listdir(d)), "枚")
