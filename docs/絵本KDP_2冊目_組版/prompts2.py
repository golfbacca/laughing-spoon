#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2冊目「トトンと はじめての パンツ」の画像プロンプトを組み立てる。

方針（1冊目の失敗から）:
  ・共有ブロック（ABSOLUTE RULES / STYLE LOCK / CHARACTER LOCK）は
    1冊目のプロンプトファイルから機械的に抜いて使う。手で写さない。
    写すとキャラ設定がじわじわずれる（作業指示書 2223行の事故）。
  ・ミオちゃんの服だけ、2冊目用に差し替える（家の中・ふともも丈）。
    理由は 調査記録5章（着替えの場面で露出を出さないため）。
  ・MODESTY 行は着替えに関わる全場面に入れる。省略しない。

使い方:
    python3 prompts2.py          → 20枚ぶんの .txt を書き出す
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT  = ROOT / "docs" / "絵本KDP_2冊目_画像プロンプト"
BOOK1_PROMPT = ROOT / "docs" / "絵本KDP_画像プロンプト" / "10_場面09_トイレの中.txt"

# ---- 共有ブロックを1冊目から抜く ---------------------------------
_src = BOOK1_PROMPT.read_text(encoding="utf-8")
SHARED = _src[_src.index("=== ABSOLUTE RULES ==="):_src.index("=== THIS IMAGE ===")].rstrip()

# ---- ミオちゃんの服を2冊目用に差し替える -------------------------
MIO_CLOTHES_BOOK2 = """- Clothing in this book (Mio is at home in the morning, not dressed to
  go out): the SAME plain moss-green shirt, but TUNIC LENGTH - it hangs
  down to MID-THIGH and completely covers the hips and bottom at all
  times. Short sleeves ending high on the upper arm, so the elbows and
  forearms are bare. Bare legs below the shirt hem, white ankle socks,
  no shoes indoors. No backpack indoors.
  In the LAST TWO SCENES ONLY, Mio also puts on beige shorts and red
  sneakers, returning to the outdoor look of the first book.
- HAIR - THIS DRIFTED ONCE ALREADY: Mio's hair is SHORT. A simple soft
  crop that ends ABOVE the ears at the sides and never reaches the jaw
  or the chin. It must read gender-neutral. Do NOT draw a chin-length
  bob. Do NOT draw hair falling past the ears onto the neck.
"""
_pat = re.compile(r'- Clothing, identical in every image:.*?\n(?=- Mio is fully clothed)', re.S)
assert _pat.search(SHARED), "1冊目の服装ブロックが見つからない。抜き出しをやり直すこと"
SHARED = _pat.sub(MIO_CLOTHES_BOOK2, SHARED)

# ---- この本だけの固定仕様 ---------------------------------------
ROOM = """=== ROOM SPEC - IDENTICAL IN EVERY INDOOR SCENE ===
One single room, drawn the same way every time. This is a fixed set.
- A quiet corner of a family home, early morning. Warm and plain.
- Wall: plain pale cream. Floor: light warm wood, simple boards.
- On the LEFT: one low wooden shelf, about chest height to Mio.
  Its top surface is clear except where a scene says otherwise.
- On the RIGHT: one window with soft morning light and a plain
  cream curtain. The light falls gently from the right.
- On the floor beside the shelf: one small round woven basket,
  used as the waste basket.
- Nothing else. No furniture clutter, no pictures on the wall,
  no toys scattered about, no rug patterns, no plants.
- NO text, NO logos, NO brand marks anywhere in the room.
"""

PANTS = """=== PANTS SPEC - IDENTICAL IN EVERY SCENE THAT SHOWS THEM ===
Three pairs of small toddler underpants, drawn as simple flat garments.
- Plain solid colours, one each: SOFT YELLOW, PALE SKY BLUE, SOFT CORAL.
- Simple shape with a plain ribbed waistband. No patterns, no prints,
  no characters, no stripes, no letters, no numbers of any kind.
- They are ordinary, modest, everyday children's underwear, drawn the
  way a clothing shape is drawn - soft, rounded, unremarkable.
- Mio always chooses the SOFT YELLOW pair. Once chosen, it is always
  the yellow one in every later scene.
- The paper shop bag is plain warm beige with simple rope handles and
  NO writing on it.
"""

MODESTY = """=== HOW THE CLOTHING IS SHOWN - MANDATORY, DO NOT OMIT ===
- Mio's moss-green shirt is tunic length and reaches MID-THIGH in every
  frame. It covers Mio from the shoulders down to mid-thigh at all times,
  in every pose, including bending, sitting and stepping.
- Mio is fully clothed in every frame of this book, without exception.
- The underpants are drawn as a simple flat everyday garment: held up in
  the hands, lying folded on the floor, or gathered down around the
  ankles or calves. Draw them the way a folded shirt is drawn.
- Where Mio steps into the garment, draw ONLY the legs below the knee
  together with the garment down near the ankles. Everything higher up
  stays covered by the shirt, and the shirt stays down.
- Toton wears only its small yellow backpack. Toton holds the garment out
  flat and does nothing else with it.
"""

MODESTY_LIGHT = """=== WHAT IS IN FRAME - MANDATORY ===
- This is a tightly cropped picture. Draw only the body parts listed in
  THIS IMAGE and nothing more. Do not widen the framing.
- Mio is fully clothed in the moss-green shirt, which is tunic length.
- Toton wears only its small yellow backpack.
"""

def out_spec(text_space):
    return f"""=== OUTPUT SPEC ===
- Square 1:1 composition.
- Generate at the largest square size the model offers.
- Target for print: 2625 x 2625 px at 300 dpi
  (8.5 inch trim + 0.125 inch bleed on each side).
- Keep every important element at least 150 px inside all four edges.
- TEXT SPACE: {text_space}. That area must stay low-detail and close to a
  single even colour, so Japanese text can be placed on it later.
  Do not put a face or any busy detail there.
"""

NO_TEXT = """=== NO TEXT, NO STRAY SHAPES ===
Render no writing of any kind - no kana, no kanji, no letters, no
numbers, no signage, no signature.
No floating or disembodied head, hair, hand or limb anywhere. Every
shape must belong to one complete character or to the room itself.
"""

HEIGHT = """=== TOTON'S HEIGHT - MEASURE IT ===
  Mio, ground to top of head       = 100 units
  Toton, ground to top of its ears =  60 units
The TOP OF TOTON'S HEAD is level with the BOTTOM HEM of Mio's shirt.
Toton is obviously the smaller of the two. Earlier attempts in the first
book drew Toton up at Mio's shoulder or chin. Far too big.
"""

# ---- 20枚。(ファイル名, TEXT SPACE, この絵の指定, 追加ブロック) ----
SCENES = [
("01_表表紙_正方形", "none - this is cover art", """
FRONT COVER ARTWORK for a SQUARE picture book. No text at all.

Mio and Toton stand side by side, both facing the viewer, in the room.
Mio holds up ONE soft yellow pair of underpants in both hands, at chest
height, in front of the body, the way a child proudly shows something
they picked out. Mio is smiling calmly - relaxed eyes, a small easy
smile. Toton stands on the floor beside Mio, calm and neutral, mouth a
single flat line, its ears twitching with one small motion mark beside
each ear.
Behind them: the low wooden shelf on the left with the plain beige paper
bag on it, and the bright window on the right. Soft morning light.

COMPOSE IT NATURALLY, FILLING THE WHOLE SQUARE.
Place the two characters so their heads sit around the middle of the
picture and their feet rest well inside the bottom edge.
Do not leave a blank band anywhere. Just draw the scene.
The title is added later by hand, so leave no gap for it.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("S01_あさ", "top third", """
Morning. Mio has just got up and is walking into the room from the
right, still sleepy but calm, arms relaxed at the sides.
Toton is already waiting UNDER the low wooden shelf on the left, sitting
on the floor in the shadow beneath it, looking towards Mio. Calm and
neutral.
On top of the shelf sits one plain beige paper shop bag with rope
handles, unopened.
Simple, quiet, warm. The top third of the picture is plain wall.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("02_場面01_ふくろ", "bottom third", """
Close on the low wooden shelf. On top of it sits ONE plain beige paper
shop bag with rope handles, still folded shut at the top.
Mio stands in front of the shelf, seen from behind and slightly to the
side, looking up at the bag. Only Mio's back and the back of the head
are toward us. Toton stands on the floor beside Mio's ankle, also
looking up at the bag.
The bag is the clear subject. Nobody touches it yet.
The bottom third of the picture is plain empty wood floor.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("03_場面02_あける", "top third", """
Mio has taken the beige paper bag down and set it on the floor. Mio
kneels beside it and holds the bag open with both hands, looking in.
Toton stands close on the other side of the bag, leaning forward
slightly to look in as well. Both calm and curious.
Out of the mouth of the bag, the folded edge of the SOFT YELLOW pair and
a corner of the PALE SKY BLUE pair are just visible - only the folded
fabric, nothing else.
The top third of the picture is plain wall.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("S04_ならべる", "bottom third", """
Overhead-ish view of the light wood floor. THREE pairs of small
underpants lie side by side in a neat row on the floor: soft yellow on
the left, pale sky blue in the middle, soft coral on the right. Each one
lies flat and folded, plain and simple.
The empty beige paper bag lies on its side behind the row.
Toton stands at the left end of the row on the floor, looking along it.
Mio is NOT in this picture - only the pants, the bag and Toton.
The bottom third of the picture is plain empty wood floor.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("04_場面03_おむつがいい", "bottom third", """
Mio has taken ONE STEP BACK from the row of three pants on the floor.
Mio stands with both feet together, hands held close in front of the
chest, shoulders slightly drawn in, looking down at the pants with a
small uncertain mouth. Not crying, not upset - just hesitant, pulling
back a little.
The three pairs lie on the floor in front of Mio, a clear gap of empty
floor between them and Mio's feet. That gap is the point of the picture.
Toton stands to the side, on the floor, watching Mio quietly. Both of
Toton's hands GRIP THE BACKPACK STRAPS - the anxious pose.
The bottom third of the picture is plain empty wood floor.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("05_場面04_だきしめる", "bottom third", """
Mio holds a folded white nappy against the chest with both arms, hugging
it, looking down at it. The nappy is drawn as a simple plain white
folded rectangle with soft rounded corners - a clean unused one, clearly
just an object being held. It is NOT worn, NOT unfolded, NOT on a body.
Mio's face is calm but reluctant.
Toton stands on the floor beside Mio, both hands GRIPPING THE BACKPACK
STRAPS - the anxious pose - looking up at Mio.
The three pairs of pants are still on the floor behind them, out of
focus and small.
The bottom third of the picture is plain empty wood floor.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("06_場面05_どれにする", "top third", """
Toton has picked up the SOFT YELLOW pair and holds it spread open
between its two stubby front limbs, lifting it up towards Mio, offering
it. The garment hangs flat and simple from Toton's grip.
Toton looks up at Mio, calm, mouth a single flat line.
Mio crouches down to Toton's level, hands resting on the knees, looking
at the yellow pants. The uncertain expression is softening.
The other two pairs, blue and coral, still lie on the floor nearby.
The top third of the picture is plain wall.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("07_場面06_えらんだ", "top third", """
Mio has reached out and taken hold of the SOFT YELLOW pair. Mio now
holds it in both hands at chest height, looking down at it with a small
calm smile - the moment of having chosen.
Toton stands on the floor just below, both front limbs still slightly
raised from having offered it, ears twitching with one small motion mark
beside each ear - the happy pose.
The blue and coral pairs remain on the floor, no longer the subject.
The top third of the picture is plain wall.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("S09_すわる", "bottom third", """
Mio sits down on the light wood floor, legs folded to one side, the
tunic-length shirt draped over the lap and knees so the hips and thighs
are completely covered. Mio holds the soft yellow pants in the lap with
both hands, looking down at them, calm.
Toton walks in from the right and sits down on the floor beside Mio,
close, facing the same way. Calm and neutral.
The bottom third of the picture is plain empty wood floor.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("08_場面07_おむつをぬぐ", "top third", """
MIO IS NOT IN THIS PICTURE AT ALL. Do not draw Mio, or any part of Mio -
no hand, no foot, no hair, no shadow of a child.

The picture shows only:
- The small round woven waste basket on the floor beside the shelf. One
  clean white nappy sits in it, folded and rolled into a neat plain
  white bundle - drawn simply, the way a rolled towel is drawn.
- Toton standing on the floor a little way from the basket, facing the
  viewer, holding the SOFT YELLOW pair spread open between its two
  stubby front limbs, held ready at its own chest height, waiting.
- Toton is calm and neutral, mouth a single flat line, looking slightly
  upward and off to the side, as though waiting for someone just out of
  frame.
The room behind them as always: cream wall, wood floor, the shelf edge.
The top third of the picture is plain wall.

This composition is deliberate. The words carry what happens; the
picture shows only the basket, the bundle and Toton waiting.
Keep the frame to those three things.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("09_場面08_かたあし", "top third", """
Mio stands on the wood floor, putting ONE foot into the soft yellow
pants. The garment is held open low down, gathered at ANKLE HEIGHT, and
one foot is stepping into it.
CAMERA AND FRAMING: we see Mio from the front, standing. The tunic-length
shirt hangs down to mid-thigh and covers everything above the knee.
Below the shirt hem: bare knees, bare shins, white ankle socks, and the
yellow garment gathered down at ankle level around one foot.
Mio is slightly off balance on one leg, the free arm out to the side for
balance, body tilted a little, face concentrating - a small determined
mouth. One small motion mark beside the raised foot to show the wobble.
Toton stands on the floor nearby, watching, calm and neutral.
The top third of the picture is plain wall.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("S13_かべにて", "top third", """
Mio stands on the wood floor, seen from the front and slightly to one
side, and has placed ONE flat hand against the plain cream wall on the
left to steady itself. That arm is straight and firm. The other arm hangs
relaxed at the side. Both feet are on the floor in white ankle socks,
standing balanced and still.
Mio looks down towards the floor, the face calm and settled - the wobble
has passed. No motion marks anywhere in this picture.
Mio wears the tunic-length moss-green shirt reaching mid-thigh, with bare
knees and shins below it. Nothing is being held.
Toton stands on the floor beside Mio's feet, looking up at Mio, calm and
neutral.
The room as always: cream wall, light wood floor, the shelf edge at the
left, the window's soft light from the right.
The top third of the picture is plain wall.
""", [ROOM, MODESTY, HEIGHT]),

("10_場面09_もういっぽう", "top third", """
CLOSE VIEW OF THE FLOOR, camera down low near the floorboards.

The picture contains only: light wood floor, the bottom edge of a
moss-green shirt hem, two lower legs from just below the knee down,
white ankle socks, and Toton.
One sock-foot rests flat on the floor. The other lifts a little, toes
tilted, mid-step, with one small motion mark beside it.
Draw NO other object on the floor. No garment, no cloth, no bag, nothing
lying about - just the bare wood floor, the two feet and Toton.
Nothing above the knees is in the picture; the frame simply ends there.
Toton stands on the floor beside the feet, facing them, calm and neutral.
The top third of the picture is plain empty floor and skirting board.
""", [ROOM, MODESTY_LIGHT, HEIGHT]),

("11_場面10_ひっぱる", "top third", """
HEAD AND SHOULDERS PORTRAIT OF MIO. Nothing below the chest is in the
picture; the frame ends there.

Mio's face fills the middle of the picture, seen from the front, tilted
down a little. The eyes look downward at something below the frame. The
mouth is a small firm line, set with effort. Cheeks slightly flushed.
Both shoulders are lifted and drawn in, and the tops of both upper arms
angle downward and outward, so you can read that both hands are busy
somewhere below the frame.
The moss-green shirt collar and the short sleeve edges are visible at
the bottom of the picture.
Two small motion marks in the air beside the shoulders, both pointing
upward, to show effort.
Background: plain cream wall, softly lit. Toton is not in this picture.
The top third of the picture is plain empty wall.
""", [ROOM, MODESTY_LIGHT, HEIGHT]),

("S14_みおろす", "bottom third", """
HEAD AND SHOULDERS PORTRAIT OF MIO, seen slightly from one side and a
little from above. Nothing below the chest is in the picture.

Mio's chin is tucked down and the eyes look downward at something below
the frame. A small pleased smile - quiet, private satisfaction. The
shoulders have dropped and relaxed.
The moss-green shirt collar and short sleeve edges are visible at the
bottom of the picture.
Further back and small, past Mio's shoulder, Toton stands on the floor
looking up. Soft focus, simple.
Background: plain cream wall with the window's warm light from the right.
The bottom third of the picture is plain empty wall and floor.
""", [ROOM, MODESTY_LIGHT, HEIGHT]),

("12_場面11_はけた", "top third", """
Mio stands upright and relaxed, both arms slightly out and away from the
body, chest a little lifted - the quiet pride of having done it alone.
A calm, easy smile. Same tunic-length shirt to mid-thigh, bare knees and
shins, white ankle socks. The thin sliver of soft yellow waistband still
just visible at the shirt hem, nothing more.
Toton stands on the floor beside Mio, looking up, with ONE SMALL MOTION
MARK BESIDE EACH EAR - the ears are twitching. This is the happy pose
and it must be clearly visible in this picture.
Warm morning light from the window on the right.
The top third of the picture is plain wall.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("13_場面12_おでかけ", "top third", """
A DIFFERENT part of the same home: the small entrance hall. Plain cream
wall, a step down to a lower tiled floor, the front door softly
suggested on the right. Same warm palette, same style.

Mio now wears the FULL OUTDOOR OUTFIT from the first book: the
moss-green shirt (still tunic length), BEIGE SHORTS over it at the
waist, and is bending down to put on the RED SNEAKERS, one already on,
one being pulled onto the other foot. The small cream backpack sits on
the step beside Mio, ready.
Mio's face is bright and ready to go.
Toton stands on the step beside the backpack, calm and neutral,
its own small yellow backpack on its back.
The top third of the picture is plain wall.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("S18_つぎのあさ", "bottom third", """
The next morning. The same room, the same light.
Mio walks up to the low wooden shelf on the left and reaches out with
one hand towards the beige paper bag on top of it - reaching for it
without being asked. Calm, easy, matter of fact. A small smile.
Same home clothes as the earlier scenes: tunic-length moss-green shirt
to mid-thigh, bare knees and shins, white ankle socks.
Toton stands on the floor below, looking up at Mio, with ONE SMALL
MOTION MARK BESIDE EACH EAR - the happy pose.
The bottom third of the picture is plain empty wood floor.
""", [ROOM, PANTS, MODESTY, HEIGHT]),

("14_裏表紙_正方形", "bottom two thirds", """
BACK COVER ARTWORK for a SQUARE picture book. No text at all.

A quiet, simple closing image. The same room, seen from a little
distance and slightly above.
On the light wood floor near the bottom of the picture: the plain beige
paper bag, standing open and empty, and beside it the PALE SKY BLUE and
SOFT CORAL pairs still lying folded and neat, waiting for another day.
Mio and Toton are seen SMALL and from BEHIND, walking away towards the
bright window on the right, side by side, Toton on the floor beside
Mio's ankle. Only their backs. Morning light ahead of them.

IMPORTANT COMPOSITION: keep all of this in the UPPER THIRD of the
picture. The BOTTOM TWO THIRDS must be plain, empty, evenly-lit wood
floor and wall with no objects and no detail at all - text is placed
there later. Do not put anything in the bottom two thirds.
Leave the lower RIGHT corner especially plain and empty.
""", [ROOM, PANTS, MODESTY, HEIGHT]),
]

HEADER = """■ {name}
■ 2冊目「トトンと はじめての パンツ」
■ 使い方: この行から下を全部まとめて1回で貼る。1枚ぶんです。
          途中の CHARACTER LOCK と MODESTY を省略しないこと。
          省略した瞬間に顔がぶれるか、出してはいけない絵が出ます。
--------------------------------------------------------------
"""

def build(name, text_space, scene, extras):
    body = [SHARED, "=== THIS IMAGE ===" + scene.rstrip()]
    body += [b.rstrip() for b in extras]
    body += [NO_TEXT.rstrip(), out_spec(text_space).rstrip()]
    return HEADER.format(name=name) + "\n\n".join(body) + \
           "\n--------------------------------------------------------------\n"

def prompt_for(name):
    for n, ts, sc, ex in SCENES:
        if n == name:
            return build(n, ts, sc, ex)
    raise KeyError(name)

NAMES = [s[0] for s in SCENES]

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for n, ts, sc, ex in SCENES:
        p = OUT / f"{n}.txt"
        p.write_text(build(n, ts, sc, ex), encoding="utf-8")
        print(f"  {len(p.read_text(encoding='utf-8')):6d} 文字  {p.name}")
    print(f"合計 {len(SCENES)} 枚")
