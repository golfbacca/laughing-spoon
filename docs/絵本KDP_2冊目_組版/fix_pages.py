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
 "01_表表紙_正方形": """

=== THIS PICTURE IS APPROVED. CHANGE ONE OBJECT ONLY. ===
The characters, their poses, their faces, the room, the furniture, the
colours and the whole composition are correct. Reproduce this picture
exactly as it is. Do NOT redraw the characters. Do NOT reframe. Do NOT
move the bag, resize it, or change its angle or its paper colour.

Change ONLY the CORD HANDLES on the beige paper bag:
- They are currently drawn STANDING UP as two stiff arcs above the top
  rim. That is wrong. Nobody is carrying this bag.
- Redraw them HANGING DOWN, limp and slack: the front handle droops
  against the FRONT FACE of the bag, sagging into a loose U that hangs
  BELOW the top rim and rests flat against the paper. The back handle
  does the same on the far side, so it is hidden. Normally only the
  front handle is visible.
- Each end of the cord enters a small round EYELET punched in the OUTER
  FRONT FACE of the bag, a little below the rim. The two eyelets are on
  the front paper, with the cord sagging between them.
- The cord must NOT pass over the rim or drop down inside the bag's
  mouth. Nothing of the cord goes into the opening.
- Leave the mouth of the bag open and unfolded, exactly as it is now.
""",
 "05_場面04_だきしめる": """

=== THIS PICTURE IS APPROVED. CHANGE ONE OBJECT ONLY. ===
The characters, their poses, their faces, the room, the furniture, the
colours and the whole composition are correct. Reproduce this picture
exactly as it is. Do NOT redraw the characters. Do NOT reframe. Do NOT
move the bag, resize it, or change its angle or its paper colour.

Change ONLY the CORD HANDLES on the beige paper bag:
- They are currently drawn STANDING UP as two stiff arcs above the top
  rim. That is wrong. Nobody is carrying this bag.
- Redraw them HANGING DOWN, limp and slack: the front handle droops
  against the FRONT FACE of the bag, sagging into a loose U that hangs
  BELOW the top rim and rests flat against the paper. The back handle
  does the same on the far side, so it is hidden. Normally only the
  front handle is visible.
- Each end of the cord enters a small round EYELET punched in the OUTER
  FRONT FACE of the bag, a little below the rim. The two eyelets are on
  the front paper, with the cord sagging between them.
- The cord must NOT pass over the rim or drop down inside the bag's
  mouth. Nothing of the cord goes into the opening.
- Leave the mouth of the bag open and unfolded, exactly as it is now.
""",
 "07_場面06_えらんだ": """

=== THIS PICTURE IS APPROVED. CHANGE ONE OBJECT ONLY. ===
The characters, their poses, their faces, the room, the furniture, the
colours and the whole composition are correct. Reproduce this picture
exactly as it is. Do NOT redraw the characters. Do NOT reframe. Do NOT
move the bag, resize it, or change its angle or its paper colour.

Change ONLY the CORD HANDLES on the beige paper bag:
- They are currently drawn STANDING UP as two stiff arcs above the top
  rim. That is wrong. Nobody is carrying this bag.
- Redraw them HANGING DOWN, limp and slack: the front handle droops
  against the FRONT FACE of the bag, sagging into a loose U that hangs
  BELOW the top rim and rests flat against the paper. The back handle
  does the same on the far side, so it is hidden. Normally only the
  front handle is visible.
- Each end of the cord enters a small round EYELET punched in the OUTER
  FRONT FACE of the bag, a little below the rim. The two eyelets are on
  the front paper, with the cord sagging between them.
- The cord must NOT pass over the rim or drop down inside the bag's
  mouth. Nothing of the cord goes into the opening.
- Leave the mouth of the bag open and unfolded, exactly as it is now.
""",
 "S09_すわる": """

=== THIS PICTURE IS APPROVED. CHANGE ONE OBJECT ONLY. ===
The characters, their poses, their faces, the room, the furniture, the
colours and the whole composition are correct. Reproduce this picture
exactly as it is. Do NOT redraw the characters. Do NOT reframe. Do NOT
move the bag, resize it, or change its angle or its paper colour.

Change ONLY the CORD HANDLES on the beige paper bag:
- They are currently drawn STANDING UP as two stiff arcs above the top
  rim. That is wrong. Nobody is carrying this bag.
- Redraw them HANGING DOWN, limp and slack: the front handle droops
  against the FRONT FACE of the bag, sagging into a loose U that hangs
  BELOW the top rim and rests flat against the paper. The back handle
  does the same on the far side, so it is hidden. Normally only the
  front handle is visible.
- Each end of the cord enters a small round EYELET punched in the OUTER
  FRONT FACE of the bag, a little below the rim. The two eyelets are on
  the front paper, with the cord sagging between them.
- The cord must NOT pass over the rim or drop down inside the bag's
  mouth. Nothing of the cord goes into the opening.
- Leave the mouth of the bag open and unfolded, exactly as it is now.
""",
 "02_場面01_ふくろ": """

=== THIS PICTURE IS APPROVED. CHANGE ONE OBJECT ONLY. ===
The characters, their poses, their faces, the room, the furniture, the
colours and the whole composition are correct. Reproduce this picture
exactly as it is. Do NOT redraw the characters. Do NOT reframe. Do NOT
move the bag, resize it, or change its angle or its paper colour.

Change ONLY the CORD HANDLES on the beige paper bag:
- Right now the FAR handle stands UP above the rim while the NEAR one
  droops. They must both behave the same way, and both must HANG DOWN.
- The front handle droops against the FRONT FACE of the bag, sagging into
  a loose U that hangs BELOW the top rim and rests flat on the paper. The
  back handle does the same on the far side and is therefore hidden - do
  not show it arching above the rim.
- Each cord end enters a small round EYELET punched in the OUTER FRONT
  FACE, a little below the rim, with the cord sagging between the two.
- No part of the cord passes over the rim or drops inside the bag.
- Leave the mouth of the bag open and unfolded, exactly as it is now.
""",
 "S18_つぎのあさ": """

=== THIS PICTURE IS APPROVED. CHANGE ONE OBJECT ONLY. ===
The characters, their poses, their faces, the room, the furniture, the
colours and the whole composition are correct. Reproduce this picture
exactly as it is. Do NOT redraw the characters. Do NOT reframe.

Change ONLY the beige paper bag standing on the shelf:
- It currently has NO handles and its top is folded and creased shut like
  a paper lunch sack. Every other page shows this bag with cord handles
  and an open top.
- Open its mouth: the top edge becomes a plain straight rim, unfolded and
  uncreased.
- Give it CORD HANDLES that HANG DOWN, limp and slack - never standing up
  as arcs. The front handle droops against the FRONT FACE of the bag,
  sagging into a loose U that hangs BELOW the rim and rests flat on the
  paper. The back handle does the same on the far side and is hidden.
- Each cord end enters a small round EYELET punched in the OUTER FRONT
  FACE, a little below the rim, with the cord sagging between them. The
  cord never passes over the rim or drops inside the bag.
- Keep the bag in the same place, at the same size and angle, same beige
  paper, no writing on it.
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
