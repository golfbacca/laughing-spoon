#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一覧で見つかった不具合を、ページ単位で直す。

直し方の原則（1冊目の記録）:
  ・崩れたら「作り直す」のではなく「承認済みの絵を編集する」
  ・「描くな」だけでは足りない。必ず「代わりにこれを描け」を添える
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "絵本KDP_組版"))
from gen_image import generate, REF_SHEET, REF_BOTH
import prompts2

IMG = pathlib.Path(__file__).resolve().parents[2] / "docs" / "絵本KDP_2冊目_画像"
ANCHOR = IMG / "01_表表紙_正方形.jpg"

FIX = {
 "04_場面03_おむつがいい": """

=== THIS PICTURE IS APPROVED. MOVE ONE OBJECT BACK DOWN. ===
Everything else is correct and must be reproduced exactly: Mio's pose and
face, the three pairs of pants on the floor, Toton with both hands on its
backpack straps, the glass-topped two-tier shelf, the basket overlapping
the shelf's left-hand leg, the open curtain hanging loose at the right,
and the framing. Do not redraw the characters. Do not move the basket.

Move ONLY the beige paper bag:
- It is currently standing on TOP of the shelf. It should not be there.
  On the previous pages it was taken down and opened on the floor, and
  nobody has put it back yet.
- Put it on the FLOOR, standing upright on its own flat base, near the
  foot of the shelf on the LEFT, beside the basket and clear of the row
  of pants.
- The TOP OF THE SHELF IS THEN COMPLETELY EMPTY. Nothing stands on it.
- The bag keeps its cord handles HANGING DOWN against its front face,
  drooping below the rim from two small eyelets, mouth open and unfolded.
""",
}

if __name__ == "__main__":
    for name in (sys.argv[1:] or FIX):
        out = IMG / f"{name}.jpg"
        # 直すページ自身を1枚目に置く＝「作り直す」ではなく「編集させる」
        refs = [out, ANCHOR, REF_SHEET, REF_BOTH]
        print(f"直す {name}")
        try:
            generate(prompts2.prompt_for(name) + FIX[name], str(out), ref_images=refs)
        except Exception as e:
            print(f"  × {name}: {type(e).__name__} {e}")
