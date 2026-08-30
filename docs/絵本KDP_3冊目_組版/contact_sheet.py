#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""20枚を1枚の一覧シートにして、キャラのぶれを目で見比べる。

引き継ぎ書0-Bの「新しい絵ができたら基準シートと並べて見る」を、
1枚ずつではなく一覧でやるためのもの。
  python3 contact_sheet.py [出力先]
"""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import prompts3

ROOT = pathlib.Path(__file__).resolve().parents[2]
IMG  = ROOT/"docs"/"絵本KDP_3冊目_画像"
FONT = ROOT/"docs"/"絵本KDP_組版"/"fonts"/"ZenMaruGothic-Medium.ttf"

CELL, COLS, LABEL = 460, 5, 34

def main(out):
    names = prompts3.NAMES
    rows = (len(names)+COLS-1)//COLS
    sheet = Image.new("RGB", (COLS*CELL, rows*(CELL+LABEL)), (255,255,255))
    d = ImageDraw.Draw(sheet); f = ImageFont.truetype(str(FONT), 22)
    for i, n in enumerate(names):
        x, y = (i % COLS)*CELL, (i//COLS)*(CELL+LABEL)
        p = IMG/f"{n}.jpg"
        if p.exists():
            sheet.paste(Image.open(p).convert("RGB").resize((CELL, CELL), Image.LANCZOS), (x, y))
        else:
            d.rectangle([x, y, x+CELL-2, y+CELL-2], fill=(240,236,230))
            d.text((x+16, y+CELL//2), "未生成", font=f, fill=(180,60,60))
        d.text((x+6, y+CELL+4), f"{i+1:02d} {n}"[:30], font=f, fill=(60,50,45))
    sheet.save(out, quality=90)
    print(f"一覧: {out}  {sheet.size}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/sheet.jpg")
