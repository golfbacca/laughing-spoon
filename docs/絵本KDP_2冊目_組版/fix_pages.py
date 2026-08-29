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

=== THIS PICTURE IS APPROVED. SLIDE ONE OBJECT LEFT. ===
Everything else is correct and must be reproduced exactly: Mio's pose and
face, the three pairs of pants on the floor, Toton, the beige paper bag
standing on the floor, the empty glass-topped two-tier shelf, the open
curtain at the right, the wall, the floor and the framing. Do not redraw
the characters. Do not reframe. Do not move the bag or the shelf.

Slide ONLY the round woven basket to the LEFT, until the shelf's
LEFT-HAND FRONT LEG passes across the basket at this exact place:

  Read the basket's width from its left edge to its right edge.
  The leg must cross it ONE THIRD of the way in FROM THE BASKET'S LEFT
  EDGE. So one third of the basket lies to the LEFT of the leg, and two
  thirds of the basket lie to the RIGHT of the leg.
  The leg therefore sits a little to the LEFT of the basket's centre
  line - not on the centre line, and not at the basket's edge.

Right now the leg is entirely OUTSIDE the basket, standing clear on the
floor to its left, with the whole leg visible down to where it meets the
floor. That is what has to change.

How to check you have done it right:
- Follow the leg downward. It comes down from the shelf, then DISAPPEARS
  behind the basket's rim. Below the rim it is not seen again, and where
  it meets the floor is completely hidden.
- The strip of basket to the left of the leg is about half as wide as
  the strip of basket to the right of it.

Keep the basket the same size, the same weave and the same colour, still
standing flat on the floor. Only one basket. The floor it leaves behind
on the right becomes plain empty wood.
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
