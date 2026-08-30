#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一覧で見つかった不具合を、ページ単位で直す（3冊目）。

直し方の原則（1冊目・2冊目の記録）:
  ・崩れたら作り直すのではなく、承認済みの絵を編集する
  ・「描くな」だけでは足りない。「代わりにこれを描け」を添える
  ・位置や大きさは相対語でなく、他の物との重なり・比で言う
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "絵本KDP_組版"))
from gen_image import generate, REF_SHEET
import prompts3

IMG  = pathlib.Path(__file__).resolve().parents[2] / "docs" / "絵本KDP_3冊目_画像"
IMG2 = pathlib.Path(__file__).resolve().parents[2] / "docs" / "絵本KDP_2冊目_画像"

FIX = {
 "09_場面08_ろうか": """

=== THIS PAGE CAME OUT WRONG. FIX THESE THINGS. ===
Two serious errors in the previous attempt.

1. THERE ARE TWO TOTONS IN THE PICTURE, and the smaller one is GLOWING.
   There is only ever ONE Toton in this book, and Toton NEVER glows, in
   any picture, for any reason. Delete the small glowing creature on the
   floor completely. Exactly one Toton, walking on the floor beside Mio's
   ankle, lit only by the lamp, giving off no light of its own.

2. MIO IS NOT CARRYING THE LAMP. Mio must be holding the lit night lamp
   in BOTH HANDS, low in front of the body, so the warm amber pool that
   travels along the corridor floor comes from that lamp in Mio's hands.
   The light source is the object the child is carrying - nothing else in
   this picture gives off light.

Everything else is right: the corridor, Mio seen from behind in the
moss-green nightshirt, the cream toilet door at the far end, the
blue-grey beyond the pool of light. Keep those.
""",

 "10_場面09_トイレのなか": """

=== THIS PAGE CAME OUT WRONG. FIX THESE THINGS. ===

1. There is a pale BAND across the top of the picture with the artwork
   pushed below it. Remove it. COMPOSE THE SCENE NATURALLY AND FILL THE
   WHOLE SQUARE, edge to edge. No band, no strip, no panel, no border,
   no inset, no seam. The corridor wall simply runs to the top edge.

2. There appear to be TWO door panels side by side. There is only ONE
   toilet door in this corridor: a single plain cream panel in its frame,
   closed flat, with one round wooden knob on its RIGHT-HAND edge and the
   open gap along its bottom. Draw one door and nothing beside it.

Keep everything else: warm amber light spilling from the gap under the
door onto the corridor floor, Toton waiting outside facing the door, the
rest of the corridor soft blue-grey, no Mio anywhere, plain empty wall
above the door.
""",

 "S13_トイレのドア": """

=== THIS PAGE CAME OUT WRONG. FIX THIS. ===
The previous attempt drew the picture inside a ROUNDED FRAME, with a
border around it and the corners cut off, like a sticker or a card.
Remove that completely.
The illustration must run all the way to all four edges of the square,
with square corners and no outline, no border, no rounded corner, no
frame and no margin of any kind. It is a full-bleed page of a picture
book, not a framed panel.
Everything inside the picture is correct - the closed cream door, Mio
from behind reaching for the knob with the lamp in the other hand, Toton
beside the feet, the warm pool at the bottom of the door. Keep all of it.
""",

 "06_場面05_てをのばす": """

=== THIS PAGE CAME OUT WRONG. FIX THESE TWO THINGS. ===

1. THE HAND IS AN ADULT'S HAND. It must be a THREE-TO-FIVE-YEAR-OLD's
   hand. Measure it against Toton, who is in the same picture:

       Toton, full height including ears  = 100 units
       The hand, wrist to fingertips      =  38 units

   The hand must be clearly SMALLER than Toton's whole body. Draw a small
   chubby palm with five SHORT rounded fingers, no knuckle detail, no
   tendons, no veins. Keep the forearm short and soft, with the short
   moss-green sleeve at the frame edge.

2. IT DOES NOT LOOK LIKE NIGHT. The background came out almost white.
   This is the last moment BEFORE the lamp is switched on, so the whole
   picture must be the soft dusty BLUE-GREY of the night scenes in this
   book - the same twilight as the pages before it. The lamp on the stool
   is still UNLIT, a plain cream dome with no glow at all.
   The only brightness is a little pale moonlight. Nothing is warm yet.
""",

 "S04_ふとんのふち": """

=== ONE THING TO FIX ON THIS PAGE ===
The hand gripping the quilt reads as an ADULT's hand - too long, too
lean. It is a THREE-TO-FIVE-YEAR-OLD's hand. Measure it against Toton,
who is in the same picture:

    Toton, full height including ears  = 100 units
    The hand, wrist to fingertips      =  38 units

Draw a small chubby palm with five SHORT rounded fingers bunched into the
quilt, no knuckle detail, no tendons, no veins, and a short soft forearm
entering from the top of the frame.
Everything else stays exactly as it is: the quilt, the futon edge, the
floor, Toton looking up, and the blue-grey night.
""",
}

if __name__ == "__main__":
    for name in (sys.argv[1:] or FIX):
        out = IMG / f"{name}.jpg"
        refs = [out, REF_SHEET, IMG2 / "12_場面11_はけた.jpg"]
        print(f"直す {name}")
        try:
            generate(prompts3.prompt_for(name) + FIX[name], str(out), ref_images=refs)
        except Exception as e:
            print(f"  × {name}: {type(e).__name__} {e}")
