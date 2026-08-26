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
exactly as it is. Do NOT redraw the characters. Do NOT reframe.

Change only the BEIGE PAPER BAG:
- It currently has NO handles, and its top is folded or creased flat like
  a paper lunch sack. Every other page in this book shows the same bag
  with handles and an open top.
- Give it TWO ROPE HANDLES: a pair of thin twisted cord handles looped
  over the top edge, standing up as two small arcs above the mouth of the
  bag. Draw them clearly.
- Open its mouth: the top edge becomes a plain straight rim, unfolded and
  uncreased. Remove the fold.
- Keep the bag in exactly the same place, at the same size and angle,
  in the same beige paper, with no writing on it.
""",
 "05_場面04_だきしめる": """

=== THIS PICTURE IS APPROVED. CHANGE ONE OBJECT ONLY. ===
The characters, their poses, their faces, the room, the furniture, the
colours and the whole composition are correct. Reproduce this picture
exactly as it is. Do NOT redraw the characters. Do NOT reframe.

Change only the BEIGE PAPER BAG:
- It currently has NO handles, and its top is folded or creased flat like
  a paper lunch sack. Every other page in this book shows the same bag
  with handles and an open top.
- Give it TWO ROPE HANDLES: a pair of thin twisted cord handles looped
  over the top edge, standing up as two small arcs above the mouth of the
  bag. Draw them clearly.
- Open its mouth: the top edge becomes a plain straight rim, unfolded and
  uncreased. Remove the fold.
- Keep the bag in exactly the same place, at the same size and angle,
  in the same beige paper, with no writing on it.
""",
 "S09_すわる": """

=== THIS PICTURE IS APPROVED. CHANGE ONE OBJECT ONLY. ===
The characters, their poses, their faces, the room, the furniture, the
colours and the whole composition are correct. Reproduce this picture
exactly as it is. Do NOT redraw the characters. Do NOT reframe.

Change only the BEIGE PAPER BAG:
- It currently has NO handles, and its top is folded or creased flat like
  a paper lunch sack. Every other page in this book shows the same bag
  with handles and an open top.
- Give it TWO ROPE HANDLES: a pair of thin twisted cord handles looped
  over the top edge, standing up as two small arcs above the mouth of the
  bag. Draw them clearly.
- Open its mouth: the top edge becomes a plain straight rim, unfolded and
  uncreased. Remove the fold.
- Keep the bag in exactly the same place, at the same size and angle,
  in the same beige paper, with no writing on it.
""",
 "02_場面01_ふくろ": """

=== THIS PICTURE IS APPROVED. CHANGE ONE THING ONLY. ===
The characters, their poses, the room, the furniture, the colours and the
whole composition are correct. Reproduce this picture exactly as it is.
Do NOT redraw the characters. Do NOT reframe.

Change only the top of the BEIGE PAPER BAG on the shelf:
- Its mouth is currently FOLDED OVER and creased shut. Every other page in
  this book shows this bag with its mouth open.
- Unfold it. The top edge becomes a plain straight rim, open and
  uncreased, with the two rope handles still looped over it as they are
  now.
- Everything else about the bag stays identical: same position, same size,
  same angle, same beige paper, no writing.
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
