#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2冊目の絵を1枚ずつ生成する。

  python3 gen2.py 01_表表紙_正方形 09_場面08_かたあし   # 指定した名前だけ
  python3 gen2.py --all                                  # 未生成のものを全部
  python3 gen2.py --list                                 # 名前一覧

キャラを崩さないため、参照画像は必ず添える（引き継ぎ書 0-B）。
  ・基準シート           … 造形の最終確定
  ・1冊目の表表紙        … 2人の大きさの比
  ・すでに承認した2冊目の絵 … 部屋と服の同一性（あれば1枚だけ足す）
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "絵本KDP_組版"))
from gen_image import generate, REF_SHEET, REF_BOTH          # noqa: E402
import prompts2                                              # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
IMG  = ROOT / "docs" / "絵本KDP_2冊目_画像"
IMG.mkdir(exist_ok=True)

# 部屋と服の基準になる絵。1枚できたらここに名前を入れる。
ANCHOR = IMG / "01_表表紙_正方形.jpg"

def refs():
    r = [REF_SHEET, REF_BOTH]
    if ANCHOR.exists():
        r.insert(0, ANCHOR)        # 承認済みを先頭に置くと「編集」寄りになる
    return r

def one(name, force=False):
    out = IMG / f"{name}.jpg"
    if out.exists() and not force:
        print(f"  済み {name}")
        return
    print(f"生成 {name}")
    generate(prompts2.prompt_for(name), str(out), ref_images=refs(), aspect="1:1")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--list":
        for n in prompts2.NAMES: print(" ", n)
    elif a[0] == "--all":
        for n in prompts2.NAMES: one(n)
    else:
        force = "--force" in a
        for n in [x for x in a if not x.startswith("--")]:
            one(n, force=force)
