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
 "06_場面05_どれにする": """

=== THIS PAGE IS STILL WRONG. THE BAND IS STILL THERE. ===
Two attempts have now drawn a horizontal seam across the upper part of
this picture, with a second paper bag and a cropped head above it.

Do this instead:
- COMPOSE THE SCENE NATURALLY AND FILL THE WHOLE SQUARE, edge to edge,
  the way any ordinary illustration fills its frame. Do NOT reserve,
  clear, empty or flatten any part of the picture. Do NOT leave a blank
  band. The empty space for text is made afterwards by hand, not by you.
- ONE continuous room. ONE unbroken wall. ONE paper bag in the whole
  picture, standing on the shelf. No seam, no join, no second panel.
- Exactly TWO characters: Mio and Toton, both whole, both on the same
  floor. No cropped head, no floating hair, no third figure.
- Let the shelf, the wall and the window fill the upper part normally.
""",
 "07_場面06_えらんだ": """

=== THIS PAGE CAME OUT WRONG. FIX EXACTLY THIS. ===
The previous attempt drew Mio with a long chin-length bob, which made Mio
read as clearly a girl. That is wrong for this character.
- Draw Mio's hair SHORT, exactly as in the reference images: a soft crop
  that ends ABOVE the ears at the sides and does not reach the jaw or the
  neck. The ears are not covered by hair.
- Everything else about this scene stays as described above.
""",
 "S13_かべにて": """

=== THIS PICTURE IS APPROVED. CHANGE ONE THING ONLY. ===
The composition, the room, the poses, the faces and Toton are all
correct. Reproduce this picture exactly as it is. Do NOT redraw it, do
NOT reframe it, do NOT move anything.

Change only this:
- Mio's sleeves. They are currently LONG, down to the wrists. Every other
  page in this book has SHORT sleeves. Shorten both sleeves so they end
  high on the upper arm, well above the elbow, leaving both elbows and
  both forearms bare. The body of the shirt stays exactly as long as it
  is now, down to mid-thigh.
- Keep the arm that reaches to the wall in exactly the same position and
  the same shape. Only the fabric on it changes.
""",
 "04_場面03_おむつがいい": """

=== ONE THING TO FIX ON THIS PAGE ===
The previous attempt gave Mio LONG sleeves down to the wrists.
- Mio's moss-green shirt has SHORT sleeves that end high on the upper
  arm, well above the elbow, so both elbows and both forearms are bare.
  The shirt is long in the BODY (down to mid-thigh) but SHORT in the
  SLEEVE. Everything else about this scene stays as described above.
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
