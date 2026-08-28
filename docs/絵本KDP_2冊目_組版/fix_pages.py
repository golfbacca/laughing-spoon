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

=== THIS PICTURE IS APPROVED. CHANGE THREE THINGS ONLY. ===
Keep EXACTLY as they are: Mio's pose (one step back, hands held close in
front of the chest, shoulders drawn in, the small uncertain mouth), the
three pairs of pants laid in a row on the floor with the gap of empty
floor between them and Mio's feet, Toton with both hands gripping the
backpack straps, the beige paper bag standing on the floor, the shelf's
position and size, and the framing.

1. THE SHELF TOP IS THE WRONG MATERIAL.
   It is currently a solid opaque WOODEN plank. On every other page this
   shelf has a CLEAR GLASS TOP set in a thin wooden frame - you look
   straight through the glass and see the wooden lower shelf beneath it,
   with a few soft pale highlights sliding across the glass.
   Replace the wooden top with that glass top. If you cannot see through
   it, it is still wrong. The lower shelf stays plain solid wood.

2. THE CURTAIN IS CLOSED. IT SHOULD BE OPEN.
   It currently spreads across and covers the window. Instead, gather it
   and push it to ONE SIDE, hanging in soft vertical folds, still full
   length down to the floor. Beside it the window is left OPEN, so the
   morning light pours in: draw that opening as a soft field of warm,
   almost-white light with no hard edges - no frame, no sill, no glazing
   bars, no pane lines.

3. THE BASKET IS NOT FAR ENOUGH LEFT.
   The round woven basket currently sits in under the shelf, between its
   legs. Move it OUT and well to the LEFT: it stands on the open floor
   beyond the shelf's left-hand leg, at the far left of the picture,
   clear of the shelf entirely. It becomes the leftmost object in the
   room. Nothing of it is tucked under the furniture.
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
