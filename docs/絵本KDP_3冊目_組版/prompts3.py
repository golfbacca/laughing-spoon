#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3冊目「トトンと よるの トイレ」の画像プロンプトを組み立てる。

方針（1冊目・2冊目の作業記録から）:
  ・共有ブロック（ABSOLUTE / STYLE / CHARACTER LOCK）は1冊目の
    プロンプトファイルから機械的に抜く。手で写さない
  ・小道具には「形」だけでなく「状態」まで書く（2冊目 作業記録8章）
  ・位置は相対語ではなく【重なり】で言う（同14章）
  ・仕様を足したら、既に描いた絵に遡って当てる（同12章）

この本だけの難所:
  夜の本なのに、シリーズのスタイルは高明度である。
  暗さを黒で作ると、3冊並べたとき別の本になる。
  暗さは【青みのグレー】で作り、あかりがついたら【琥珀色】が差す。
  この対比そのものが本の主題（差別化設計3章）。

使い方:
    python3 prompts3.py          → 20枚ぶんの .txt を書き出す
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT  = ROOT / "docs" / "絵本KDP_3冊目_画像プロンプト"
BOOK1_PROMPT = ROOT / "docs" / "絵本KDP_画像プロンプト" / "10_場面09_トイレの中.txt"

_src = BOOK1_PROMPT.read_text(encoding="utf-8")
SHARED = _src[_src.index("=== ABSOLUTE RULES ==="):_src.index("=== THIS IMAGE ===")].rstrip()

# ---- ミオちゃんの服（3冊目・夜のすがた）------------------------
MIO_CLOTHES = """- Clothing in this book (Mio is at home at night): the SAME plain
  moss-green shirt, worn as a nightshirt - TUNIC LENGTH, hanging down to
  MID-THIGH and completely covering the hips and bottom at all times.
  Short sleeves ending high on the upper arm, so the elbows and forearms
  are bare. Bare legs below the hem, white ankle socks, no shoes.
  No backpack anywhere in this book.
- WHAT MIO DOES **NOT** WEAR HERE: no beige shorts, no red sneakers, no
  cream backpack. Those belong to the daytime books in this series and
  must not appear. At night Mio wears the moss-green nightshirt and white
  ankle socks, and nothing else at all.
- HAIR: Mio's hair is SHORT. A soft crop that ends ABOVE the ears at the
  sides and never reaches the jaw or the chin. It must read
  gender-neutral. Never a chin-length bob.
"""
_pat = re.compile(r'- Clothing, identical in every image:.*?\n(?=- Mio is fully clothed)', re.S)
assert _pat.search(SHARED), "1冊目の服装ブロックが見つからない"
SHARED = _pat.sub(MIO_CLOTHES, SHARED)

# ---- 夜の光。この本の要 -----------------------------------------
NIGHT = """=== NIGHT LIGHT SPEC - THE HEART OF THIS BOOK. READ IT ALL. ===
This is a night-time book, but it belongs to a bright, high-key picture
book series. Darkness must never be made with black.

- THE DARK: a soft, dusty BLUE-GREY twilight. Everything stays readable -
  you can always see the shapes of the room, the furniture and the
  characters. Never black, never murky, never harsh. Think of a room lit
  only by a little moonlight through a curtain.
- THE LAMP LIGHT: a warm AMBER glow, soft-edged, pooling outward. Where
  it falls, the usual warm palette of the series comes back: cream, warm
  beige, light wood.
- The two together are the whole visual arc of the book: cool blue-grey
  before the lamp is on, warm amber after. Each scene below says which
  state it is in.
- No hard shadows, no dramatic contrast, no spooky mood at any point.
  The night is quiet and safe, not frightening.

=== THE LAMP - IDENTICAL IN EVERY SCENE THAT SHOWS IT ===
One small portable night lamp. It is the object the whole book turns on.
- Shape: a small rounded dome, about the size of the child's two hands
  together, like a smooth mushroom cap on a low base. Plain cream body.
- On its top is ONE large soft round button. That is how it is switched
  on - a child presses the whole top down. NO wall switch, NO cord, NO
  toggle, NO pull-string anywhere in this book.
- OFF state: the dome is plain cream, unlit, and the room is blue-grey.
- ON state: the dome glows warm amber from inside, and a soft pool of
  amber light spreads onto whatever is nearest.
- It stands on the low wooden stool beside the pillow, within easy reach
  of a child lying down. From the scene where Mio takes it, Mio carries
  it in both hands.
- No writing, no logo, no pattern on it.

=== TOTON NEVER GLOWS. THIS IS NOT NEGOTIABLE. ===
Toton gives off NO light of its own, in any picture, at any moment.
It is not luminous, not glowing, not shining, not radiant, and it never
lights the way for anybody. It is simply lit BY the lamp, the same as the
furniture is. In the dark scenes Toton is a soft blue-grey shape like
everything else.
The child makes the light. The companion does not.
"""

# ---- 部屋 -------------------------------------------------------
ROOM = """=== THE BEDROOM - IDENTICAL IN EVERY SCENE THERE ===
One small Japanese bedroom, drawn the same way every time.
- Floor: light warm wood, simple boards. Wall: plain pale cream.
- ONE futon laid directly on the floor, low and flat: a plain cream
  mattress with a soft moss-green quilt and one cream pillow.
- Beside the pillow, on the LEFT: ONE low wooden stool, knee height, with
  the night lamp standing on its top. Nothing else on it.
  There is EXACTLY ONE stool in the whole room. Never draw a second stool,
  a second table or any other small piece of furniture beside it.
- On the RIGHT: one window with a plain cream curtain, closed at night,
  with a little pale moonlight coming through the fabric.
- The bedroom door is in the BACK wall, plain cream, closed.
- Nothing else. No toys, no pictures, no clutter, no plants.
- NO text, NO logos, NO brand marks anywhere.

=== THE CORRIDOR AND THE TOILET DOOR ===
- The corridor is plain: cream walls, the same light wood floor, and a
  simple skirting board. It runs away from the camera.
- At its end, ONE toilet door: a plain cream panel in a proper frame,
  with a round wooden knob on its RIGHT-HAND edge and hinges on the left.
- GAP UNDER THE DOOR: the door does not reach the floor. There is an open
  gap about one hand's width tall along its whole bottom edge. This gap
  is present every time the door is shown.
- No other doors, no pictures on the corridor walls, no rugs.
"""

MODESTY = """=== HOW MIO IS SHOWN - MANDATORY ===
- Mio is fully clothed in every frame of this book, without exception.
- The moss-green nightshirt is tunic length and reaches mid-thigh at all
  times, in every pose, including lying down, kneeling and walking.
- Draw only the body parts the scene lists. Do not widen the framing.
- Toton wears only its small yellow backpack, and no clothing ever.
"""

HEIGHT = """=== TOTON'S HEIGHT - MEASURE IT ===
  Mio, ground to top of head       = 100 units
  Toton, ground to top of its ears =  60 units
The TOP OF TOTON'S HEAD is level with the BOTTOM HEM of Mio's shirt.
Toton is obviously the smaller of the two.
"""

NO_TEXT = """=== NO TEXT, NO STRAY SHAPES ===
Render no writing of any kind - no kana, no kanji, no letters, no
numbers, no signage, no signature.
No floating or disembodied head, hair, hand or limb anywhere. Every shape
must belong to one complete character or to the room itself.
"""

def out_spec(text_space):
    """【やらかし・2026-08-29】
    「TEXT SPACE: 上3分の1を平らに保て」と書くと、モデルは
    絵の上にクリーム色の帯を足して、その下に絵を押し込む。
    1冊目・2冊目でも同じ事故が起きている（2冊目 作業記録3章）。

    帯が出なかったのは表紙だけで、表紙のプロンプトにだけ
    「COMPOSE IT NATURALLY, FILLING THE WHOLE SQUARE」があった。
    そこで全ページにその言い方を入れ、静かな場所は
    「余白を空けろ」ではなく「そこは壁である／床である」と
    情景の事実として書く。
    """
    return f"""=== OUTPUT SPEC ===
- Square 1:1 composition.
- COMPOSE THE SCENE NATURALLY AND FILL THE WHOLE SQUARE, edge to edge,
  the way any ordinary illustration fills its frame.
  Do NOT reserve, clear, empty or flatten any part of the picture.
  Do NOT add a band, a strip, a panel, a border, a margin or an inset.
  There is no seam anywhere. The room simply runs to all four edges.
  The space for Japanese text is made afterwards by hand, not by you.
- In this scene the {text_space} happens to be plain and undecorated
  anyway. Draw it plainly, as an ordinary part of the room - no face and
  no busy detail there - and let it reach the edge of the picture.
- Generate at the largest square size the model offers.
- Target for print: 2625 x 2625 px at 300 dpi
  (8.5 inch trim + 0.125 inch bleed on each side).
- Keep every important element at least 150 px inside all four edges.
"""


BASE = [NIGHT, ROOM, MODESTY, HEIGHT]

# ---- 20枚。(ファイル名, TEXT SPACE, この絵の指定) ----------------
SCENES = [
("01_表表紙_正方形", "whole picture", """
FRONT COVER ARTWORK for a SQUARE picture book. No text at all.

NIGHT, LAMP ON. Mio stands in the bedroom holding the little night lamp
in both hands at chest height, and it glows warm amber up onto Mio's face
and chest. Mio looks straight at the viewer with a calm, quietly proud
half-smile - the face of someone who has just done something alone.
Toton stands on the floor beside Mio, lit by that same amber pool, calm
and neutral, ears twitching with one small motion mark beside each ear.
Toton does not glow.
Behind them the room falls away into soft blue-grey: the futon, the
stool, the curtained window with a little moonlight.

COMPOSE IT NATURALLY, FILLING THE WHOLE SQUARE.
Heads around the middle of the picture, feet well inside the bottom edge.
Do NOT reserve, clear or flatten any part of the picture, and do not
leave a blank band - the space for the title is made afterwards by hand.
"""),

("S01_ねるまえ", "upper part of the picture, which is plain wall", """
EVENING, LAMP ON, curtains closed. Mio is getting into the futon: sitting
on it, lifting the moss-green quilt with one hand, about to lie down.
Calm and sleepy, a small easy mouth.
On the low wooden stool beside the pillow, the night lamp stands lit, its
warm amber glow pooling over the pillow and the near half of the futon.
Toton sits on the floor at the foot of the stool, looking up at Mio,
calm and neutral. Toton does not glow.
The far side of the room is soft blue-grey.
The top third of the picture is plain wall.
"""),

("02_場面01_めがさめる", "lower part of the picture, which is plain floor", """
DEEP NIGHT, LAMP OFF. The whole room is soft dusty blue-grey, lit only by
a little pale moonlight through the closed curtain. Nothing is black; the
futon, the stool and the walls are all clearly visible.

Mio has just woken: lying on the futon under the quilt, eyes OPEN, head
turned a little to one side, looking out into the dim room. Not crying,
not frightened - just awake and still.
The night lamp stands UNLIT on the stool, a plain cream dome.
Toton lies curled beside the pillow, awake, a blue-grey shape, looking at
Mio. Toton does not glow.
The bottom third of the picture is plain empty floor.
"""),

("03_場面02_むずむず", "upper part of the picture, which is plain wall", """
DEEP NIGHT, LAMP OFF. Same blue-grey room, same futon.

Mio is still lying down but has drawn both knees up under the quilt and
pressed one hand against the tummy over the quilt. The face is a small
uncomfortable frown - the body has said something. Eyes open, looking
down towards the quilt.
The lamp stands UNLIT on the stool.
Toton sits up beside the pillow now, watching Mio quietly.
The top third of the picture is plain wall.
"""),

("S04_ふとんのふち", "lower part of the picture, which is plain floor", """
DEEP NIGHT, LAMP OFF. CLOSE VIEW of the edge of the futon.

The picture contains only: the moss-green quilt, the cream mattress edge,
the wooden floor beside it, ONE small hand, and Toton.
Mio's hand grips the hem of the quilt tightly, knuckles showing, fingers
bunched into the fabric. The forearm comes in from the top of the frame
and is cut off there - no head, no face, no body in this picture.
Toton stands on the floor just below the hand, looking up at it.
Everything is soft blue-grey.
The bottom third of the picture is plain empty floor.
"""),

("04_場面03_でられない", "lower part of the picture, which is plain floor", """
DEEP NIGHT, LAMP OFF. THE HESITATION. This is a core page.

Mio has sat up on the futon, quilt pushed back over the legs, and has
stopped there. Both hands rest on the quilt, shoulders drawn in a little,
head turned towards the dim room beyond the futon. The mouth is a small
uncertain line. Mio is looking OUT at the dark, and not moving.
Between Mio and the bedroom door there is a clear stretch of empty
blue-grey floor. That empty stretch is the point of the picture.
The lamp stands UNLIT on the stool at Mio's other side.
Toton stands on the floor beside the futon with BOTH HANDS GRIPPING THE
BACKPACK STRAPS - the anxious pose. Toton does not glow.
The bottom third of the picture is plain empty floor.
"""),

("05_場面04_ここにある", "lower part of the picture, which is plain floor", """
DEEP NIGHT, LAMP OFF. Still blue-grey.

Toton has turned and is looking UP at the low wooden stool beside the
pillow, where the unlit lamp stands. One of Toton's short front limbs is
raised slightly towards it - not touching it, just pointing the way with
its whole body. Toton is calm, mouth a single flat line.
Mio, still sitting on the futon, has turned to follow Toton's look, head
coming round towards the stool.
The unlit lamp is clearly visible on the stool: a plain cream dome with
one big round button on top.
Toton does not glow, and does not touch the lamp.
The bottom third of the picture is plain empty floor.
"""),

("06_場面05_てをのばす", "upper part of the picture, which is plain wall", """
DEEP NIGHT, LAMP STILL OFF. CLOSE VIEW of the stool and the lamp.

Mio's arm reaches in from the right of the frame and the fingertips are
just arriving at the top of the unlit lamp, almost touching the big round
button. You can see the hand, the forearm and the short moss-green sleeve
at the frame edge - nothing else of Mio.
The lamp is still unlit, plain cream, and the whole picture is blue-grey.
Toton stands on the floor below the stool, looking up at the hand.
The top third of the picture is plain wall.
"""),

("07_場面06_ついた", "upper part of the picture, which is plain wall", """
THE MOMENT THE LAMP COMES ON. This is the core page of the whole book.

THE LAMP STAYS ON THE STOOL. Mio is NOT holding it and NOT carrying it.
This is the only page in the book where the lamp is switched on, and it
is switched on exactly where it stands, on the stool.
Mio is still ON THE FUTON, kneeling up on the quilt and leaning across
towards the stool, with one arm stretched out to it. The other hand rests
on the futon for balance.

That outstretched hand is pressing down on the big round button, and the
lamp has JUST lit: the cream dome glows warm amber from inside and a soft pool of
amber light spreads out across the stool, up Mio's arm, and onto Mio's
face and the near part of the futon. The rest of the room is still
blue-grey, so the warm pool reads clearly against it.
Mio's face is lit from below by that warm light, eyes a little wide,
mouth soft - surprise turning into relief.
Toton stands on the floor in the edge of the pool of light, lit by it,
calm and neutral. Toton does not glow by itself.
Make the contrast between the warm pool and the cool room the subject of
this picture.
The top third of the picture is plain wall.
"""),

("S09_じぶんでついた", "lower part of the picture, which is plain floor", """
LAMP ON. The warm amber pool now fills the near half of the room; the far
corners stay soft blue-grey.

Mio sits on the futon looking at the lit lamp, a small calm smile, both
hands resting in the lap. Shoulders relaxed.
Toton stands on the floor beside the stool, looking up at Mio, with ONE
SMALL MOTION MARK BESIDE EACH EAR - the ears are twitching. This is the
happy pose and it must be clearly visible here.
Toton does not glow; it is simply lit by the lamp.
The bottom third of the picture is plain empty floor.
"""),

("08_場面07_ふとんからでる", "upper part of the picture, which is plain wall", """
LAMP ON, standing on the stool. Mio is getting out of the futon: quilt
folded back, one white-socked foot already flat on the wooden floor, the
other still on the mattress, one hand on the floor for balance, body
leaning forward. The face is set and awake.
The amber light from the lamp falls across the floor where the foot has
landed. Beyond the pool, the room is blue-grey.
Toton stands on the floor waiting, calm and neutral.
The top third of the picture is plain wall.
"""),

("09_場面08_ろうか", "upper part of the picture, which is plain wall", """
THE CORRIDOR, LAMP CARRIED. Mio walks away from the camera down the
corridor, seen from BEHIND - the back of the head, the moss-green
nightshirt to mid-thigh, bare legs, white socks on the wooden floor.
Mio carries the lit lamp in BOTH HANDS, held low in front of the body, so
a warm amber pool travels along the floor and up the corridor walls just
ahead of the feet. Beyond that pool the corridor is soft blue-grey, and
at its far end the cream toilet door is only just visible.
Toton walks on the floor beside Mio's ankle, inside the pool of light,
lit by it. Toton does not glow.
The top third of the picture is plain wall.
"""),

("S13_トイレのドア", "upper part of the picture, which is plain wall", """
THE TOILET DOOR, seen from the corridor. LAMP CARRIED.

The plain cream door fills the middle of the picture, closed, with its
round wooden knob on the RIGHT-HAND edge and the open gap along the
bottom. Mio stands in front of it, seen from behind and slightly to the
side, holding the lit lamp in one hand down at the side and reaching the
other hand up to the knob.
The amber pool lights the lower part of the door and the floor in front
of it; the top of the door and the corridor above fade to blue-grey.
Toton stands on the floor beside Mio's feet, in the light, looking up.
The top third of the picture is plain wall.
"""),

("10_場面09_トイレのなか", "upper part of the picture, which is plain wall", """
MIO IS NOT IN THIS PICTURE. Do not draw Mio, or any part of Mio.

The toilet door is now CLOSED, flat against its frame, seen from the
corridor. Mio is entirely behind it.
Through the open gap along the bottom of the door, WARM AMBER LIGHT spills
out onto the corridor floor in a low bright band - the lamp is inside with
Mio. That band of light is the subject of the picture.
Toton stands on the corridor floor OUTSIDE the door, in that spilled
light, facing the door, waiting patiently, calm and neutral.
The rest of the corridor is soft blue-grey.

HARD LIMITS
- The door stays shut. You cannot see into the room behind it at all.
- Do NOT show Mio's body, face, hands or feet anywhere.
- Do NOT show a toilet, a bowl, a sink or any fixture.
- Above the door frame there is nothing but plain empty wall. No dome, no
  arch, no head, no lamp, no sign, no window.
The top third of the picture is plain wall.
"""),

("11_場面10_おわりのおと", "upper part of the picture, which is plain wall", """
STILL OUTSIDE THE CLOSED DOOR, the same set as the picture before, and
Mio is still not in it.

The band of warm amber light still spills from the gap under the door.
Now add THREE soft curved motion lines in the air on either side of the
door, at about knob height, to show a sound coming through it - simple
gentle arcs in the same soft line as the rest of the book, nothing harsh.
Toton stands outside the door as before, facing it, ears twitching with
one small motion mark beside each ear.
The corridor stays soft blue-grey.
Same hard limits as before: door shut, no Mio, no fixtures, plain wall
above the door.
The top third of the picture is plain wall.
"""),

("S14_てをあらう", "lower part of the picture, which is plain floor", """
CLOSE VIEW OF A SMALL WASHBASIN in the corridor by the toilet door.
LAMP ON, standing on the edge of the basin.

The picture contains only: a simple plain cream basin, a single tap, two
small hands under a thin stream of water, the lit lamp on the basin edge
casting warm amber over everything, and Toton.
The forearms come in from the top of the frame, in short moss-green
sleeves, and are cut off there - no head, no face, no body.
Toton stands on the floor below, looking up. Toton does not glow.
Beyond the amber pool the wall is blue-grey.
The bottom third of the picture is plain empty floor.
"""),

("12_場面11_もどる", "upper part of the picture, which is plain wall", """
BACK ALONG THE CORRIDOR, LAMP CARRIED, walking TOWARDS the camera now.
Mio comes back up the corridor holding the lit lamp in both hands in
front of the body. The warm amber pool lights Mio's face gently from
below, and the face is calm and easy - the walk back is not frightening.
Behind Mio the corridor recedes into soft blue-grey.
Toton walks beside Mio's ankle inside the pool of light.
The top third of the picture is plain wall.
"""),

("13_場面12_またねる", "upper part of the picture, which is plain wall", """
BACK IN THE BEDROOM. LAMP ON, standing on the stool again where it began.

Mio is lying down in the futon under the moss-green quilt, curled on one
side facing the lamp, eyes CLOSED, mouth soft and settled - already
falling asleep. The warm amber pool covers the pillow and Mio's face and
the near part of the futon. The far side of the room is blue-grey.
Toton lies curled on the floor beside the stool, also settling, calm.
Quiet, warm, finished.
The top third of the picture is plain wall.
"""),

("S18_つぎのよる", "lower part of the picture, which is plain floor", """
ANOTHER NIGHT, LAMP OFF, blue-grey room, the same futon and stool.

Mio has woken again and is already sitting up, and this time reaches
straight out towards the unlit lamp on the stool without hesitating -
the arm extended, the hand almost at the button, the face calm and
matter-of-fact. No drawn-in shoulders, no uncertainty.
Toton stands on the floor beside the stool with ONE SMALL MOTION MARK
BESIDE EACH EAR - the happy pose.
The bottom third of the picture is plain empty floor.
"""),

("14_裏表紙_正方形", "lower two thirds, which is plain floor", """
BACK COVER ARTWORK for a SQUARE picture book. No text at all.

A quiet closing image. The bedroom at night, seen from a little distance.
On the low wooden stool the night lamp stands LIT, its warm amber pool
spreading over the stool and the pillow beside it. The futon is empty and
neatly turned back. The rest of the room is soft blue-grey.
Far off to the right, small and seen from BEHIND, Mio and Toton walk away
towards the bedroom door together, at the edge of the light.

IMPORTANT COMPOSITION: keep all of this in the UPPER THIRD of the
picture. The BOTTOM TWO THIRDS must be plain, empty, evenly-toned floor
with no objects and no detail at all - text is placed there later.
Leave the lower RIGHT corner especially plain and empty.
"""),
]

HEADER = """■ {name}
■ 3冊目「トトンと よるの トイレ」
■ 使い方: この行から下を全部まとめて1回で貼る。1枚ぶんです。
          CHARACTER LOCK / NIGHT LIGHT SPEC を省略しないこと。
          とくに「Toton never glows」は消さない。
          消した瞬間に、先行する既刊と同じ本になります。
--------------------------------------------------------------
"""

def build(name, ts, scene):
    body = [SHARED, "=== THIS IMAGE ===" + scene.rstrip()]
    body += [b.rstrip() for b in BASE]
    body += [NO_TEXT.rstrip(), out_spec(ts).rstrip()]
    return HEADER.format(name=name) + "\n\n".join(body) + \
           "\n--------------------------------------------------------------\n"

def prompt_for(name):
    for n, ts, sc in SCENES:
        if n == name:
            return build(n, ts, sc)
    raise KeyError(name)

NAMES = [s[0] for s in SCENES]

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for n, ts, sc in SCENES:
        p = OUT / f"{n}.txt"
        p.write_text(build(n, ts, sc), encoding="utf-8")
        print(f"  {len(p.read_text(encoding='utf-8')):6d} 文字  {p.name}")
    print(f"合計 {len(SCENES)} 枚")
