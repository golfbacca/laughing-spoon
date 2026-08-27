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
 "S13_かべにて": """

=== THIS PICTURE IS APPROVED. MIRROR ONE OBJECT. ===
Mio, the pose, the hand on the wall, the face, the legs, the socks,
Toton, the room, the furniture and the framing are all correct.
Reproduce them exactly. Do not redraw the characters. Do not reframe.
Do not move either foot.

Do exactly one thing to the yellow garment: MIRROR IT LEFT-TO-RIGHT
about the ankle it is hanging on.

- Keep the ribbed waistband ring exactly where it is now, around the same
  ankle, at the same height and the same size.
- Right now the body of the garment, and the empty second leg opening,
  spread out to the VIEWER'S RIGHT - away from the other foot, off toward
  Toton. Flip that to the opposite side.
- After the flip, the body of the garment and the empty leg opening lie
  on the floor to the VIEWER'S LEFT, in the space BETWEEN the two feet,
  right next to the bare white sock. The empty opening faces that sock,
  open and waiting for it.
- Nothing of the garment extends past the feet on the outer side any
  more. The floor to the viewer's right of the garment is bare wood.
- Same soft yellow, same size, same ribbed waistband.
""",
 "04_場面03_おむつがいい": """

=== THIS PICTURE IS APPROVED. PUT ONE OBJECT BACK ON THE FLOOR. ===
Mio, the pose, the face, the three pairs of pants on the floor, Toton,
the two-tier shelf, the full-length curtain, the basket, the wall and the
framing are all correct. Reproduce them exactly. Do not redraw the
characters, do not reframe, do not move anything else.

Move ONE object: the beige paper bag.
- It is currently standing on TOP of the two-tier shelf. That is wrong
  for this moment in the story: the bag was taken down and opened on the
  floor on the previous pages, and it has not been put back yet.
- Put it back down ON THE FLOOR, standing upright on its own flat base,
  near the foot of the shelf on the LEFT of the picture, clear of the row
  of pants.
- The top of the shelf is then empty.
- The bag keeps its cord handles HANGING DOWN against its front face,
  drooping below the rim from two small eyelets in the front paper, and
  its mouth stays open and unfolded.
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
