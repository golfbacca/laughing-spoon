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
- PROPORTIONS: Mio is a small child and is drawn at about THREE
  HEAD-HEIGHTS tall - the head is large, roughly a third of the whole
  figure, the limbs short and soft. NEVER draw Mio at four or more
  head-heights; that reads as a school-age child, not a preschooler.
- SLEEVES: the nightshirt has SHORT sleeves that end high on the upper
  arm, well above the elbow. Both elbows and both forearms are bare in
  every picture. Mio never wears long sleeves anywhere in this book.
  MIO WEARS NOTHING UNDERNEATH THE NIGHTSHIRT. There is no undershirt,
  no base layer, no thin inner sleeve and no second garment of any kind.
  Where the short sleeve ends, there is BARE SKIN - the same pink-cream
  skin tone as the face and the hands - all the way to the fingers.
  Never draw a thin pale-green sleeve continuing down the forearm.
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
- Shape: a smooth rounded DOME on a low cylindrical base - like half an
  egg sitting on a short round foot. About the size of the child's two
  hands together. Plain cream body.
  IT IS NOT A MUSHROOM. No stalk, no stem, no flared overhanging cap, no
  gills, no narrow neck. The dome sits directly on its base and the base
  is only slightly narrower than the dome.
- IT HAS NO HANDLE, no strap, no loop and no hook. It can only be
  CARRIED IN BOTH HANDS, cradled from underneath, or set down on a
  surface. It is never dangled from the fingers, never hung, and never
  held by its rim with one hand.
- On its top is ONE large soft round button. That is how it is switched
  on - a child presses the whole top down. NO wall switch, NO cord, NO
  toggle, NO pull-string anywhere in this book.
- OFF state: the dome is a DULL, MATT, SLIGHTLY GREYED cream. It is a
  dark object in a dark room, no brighter than the pillow beside it.
  NO bright highlight on its crown, NO gloss, NO sheen, NO halo, NO glow
  of any kind around it, and NO warm light anywhere on the wall, the
  floor, the stool or the bedding. Its shaded side is blue-grey like
  everything else. A reader must be able to tell at a glance that it is
  switched off. The whole room is blue-grey twilight, and Mio's face and
  the futon carry the same cool shading as the walls.
- ON state: the dome glows warm amber from inside, and a soft pool of
  amber light spreads onto whatever is nearest.
- Every scene below says OFF or ON. The two states must look obviously
  different. A scene marked LAMP OFF must never read as if it were lit.
- It stands on the low wooden stool beside the pillow, within easy reach
  of a child lying down. From the scene where Mio takes it, Mio carries
  it in both hands.
- No writing, no logo, no pattern on it.

=== TOTON'S BACKPACK - WHEN IT IS ON AND WHEN IT IS OFF ===
Toton's small backpack is a warm MUSTARD YELLOW. It is never blue and
never any other colour.
- WHENEVER TOTON IS AWAKE, IT IS WEARING THE BACKPACK. That is every
  page of this book except the two below.
- TOTON TAKES THE BACKPACK OFF ONLY TO SLEEP. On the two pages where it
  is asleep, it sits on the floor with its eyes closed and the backpack
  lies on the floorboards beside it, straps upward.
- Toton never sleeps lying down, and never sleeps wearing the backpack.

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
- ONE futon laid directly on the floor. It is made of EXACTLY THREE
  pieces of bedding and nothing else, stacked in this order:

  1. THE UNDER-FUTON (the mattress). A plain CREAM slab lying directly on
     the floor, thin and low. Its front SIDE FACE - its thickness - is
     visible along the bottom edge, which is how you can tell it is the
     mattress. Its top surface is smooth and flat: NO quilting, NO hem
     roll, NO folded-back corner, NO turned-down edge anywhere on it.
     THIS IS THE ONLY THING MIO'S BODY EVER RESTS ON. Mio always sits,
     kneels and lies DIRECTLY ON THE CREAM.

  2. THE COVER QUILT. A soft MOSS-GREEN quilt. It goes OVER Mio, or is
     thrown back and lies in a loose heap BESIDE her. It is NEVER
     underneath Mio and is NEVER used as a mattress or a pad.

  3. ONE CREAM PILLOW, lying on the cream mattress at its left end.

  THE TEST FOR EVERY PICTURE: wherever Mio's body touches the bedding,
  the colour under her is CREAM. Moss-green appears only ON TOP OF Mio,
  or heaped BESIDE her. Never draw Mio sitting, kneeling or lying on the
  moss-green.

  FORBIDDEN, because these keep appearing by mistake:
  - a second cream cloth laid on top of the green quilt
  - a folded-back cream edge, a rolled cream hem, or a turned-down collar
    of cream cloth anywhere on the bedding
  - the green drawn as a thick quilted pad or mattress topper
  - two pillows, a stack of pillows, or a green pillow
- Beside the pillow, on the LEFT: ONE low wooden stool, knee height, with
  the night lamp standing on its top. Nothing else on it.
  The stool has four round wooden legs and a HORIZONTAL CROSS-BRACE
  joining the legs partway down, like a simple milking stool. That brace
  is always visible.
  There is EXACTLY ONE stool in the whole room. Never draw a second stool,
  a second table or any other small piece of furniture beside it.
- On the RIGHT: one window with a plain cream curtain, closed at night,
  with a little pale moonlight coming through the fabric.
- THE LAYOUT NEVER CHANGES, whatever the camera angle:
    the futon lies along the middle of the room with its PILLOW END at
    the LEFT; the stool stands just beyond the pillow, still on the LEFT;
    the plain cream bedroom door is in the BACK wall, closed, roughly
    behind the middle of the futon; the curtained window is on the RIGHT
    wall, which meets the back wall at a right angle.
    Left to right, therefore: stool and pillow, then the futon, then the
    window. Keep that order in every picture of this room.
- Nothing else. No toys, no pictures, no clutter, no plants.
- NO text, NO logos, NO brand marks anywhere.

=== THE CORRIDOR - ONE FIXED LAYOUT, ONE FIXED CAMERA ===
The corridor is drawn from the SAME viewpoint in every corridor scene:
the camera stands at the bedroom end and looks straight along it, so the
corridor runs away from the viewer into the picture.

Three things are always in the same place:
- FAR END, straight ahead: ONE toilet door, closed unless the scene says
  otherwise. A plain cream panel in a proper frame, a round wooden knob
  on its RIGHT-HAND edge, hinges on the left.
- RIGHT-HAND WALL, partway along, nearer the camera than the door: ONE
  small washbasin. A plain white basin on a simple light-wood cabinet, a
  single tap, no mirror, no bottles, no towel rail. It stands against the
  right wall and juts into the corridor, so from this camera it is seen
  from its side, on the RIGHT of the picture.
- LEFT-HAND WALL: completely bare.

THE WASHBASIN STANDS AGAINST A FLAT WALL. The right-hand wall runs
straight from one end of the corridor to the other. There is NO alcove,
NO niche and NO recess in it - the wall never steps back to make a bay
for the basin. The basin simply stands against the flat wall and juts
out into the corridor.
THE BASIN IS WELL IN FRONT OF THE TOILET DOOR, about halfway along the
corridor, much nearer the camera than the door. It is never level with
the door and never tucked in beside the door frame.
Each scene below says whether the basin is in shot. When it is, draw it
on the right against the flat wall. When a scene says the basin is not
in shot, the right-hand wall is plain and flat all the way along.
THE TOILET DOOR IS ALWAYS AT THE FAR END, straight ahead. It is NEVER on
the right-hand wall and never on the left-hand wall. There is exactly ONE
door in the corridor, and no other doors anywhere.

- GAP UNDER THE DOOR: the door does not reach the floor. There is an open
  gap about one hand's width tall along its whole bottom edge. This gap
  is present every time the door is shown.
- No pictures on the corridor walls, no rugs, no clutter.
- Cream walls, the same light wood floor, a simple skirting board.
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

NO_TEXT = """=== FULL BLEED. NO FRAME. ===
The illustration runs all the way to all four edges of the square, with
SQUARE corners. No border, no outline, no rounded corner, no vignette,
no margin, no drop shadow around the picture, and no card or sticker
look. It is a full-bleed page of a picture book.

=== NO TEXT, NO STRAY SHAPES ===
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
EVENING, LAMP ON, curtains closed. Mio is getting into the futon.
Mio SITS DIRECTLY ON THE CREAM MATTRESS, and with one hand HOLDS THE
MOSS-GREEN QUILT UP AND CLEAR OF HER, about to slide underneath it and
lie down. Because the quilt is lifted, the cream mattress is plainly
visible underneath it and under her. She is NOT sitting on the green.
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

Mio has just woken. She LIES DIRECTLY ON THE CREAM MATTRESS with the
MOSS-GREEN QUILT DRAWN UP OVER HER BODY to the shoulders, so only her
head, her neck and one forearm are outside it. Eyes OPEN, head turned a
little to one side, looking out into the dim room. Not crying, not
frightened - just awake and still.
Mio's body rests DIRECTLY ON THE CREAM MATTRESS. The moss-green quilt is only ever over her or heaped beside her, never under her.
The night lamp stands UNLIT on the stool, a plain cream dome.
TOTON IS ASLEEP, exactly as on the last page of the book. It is SEATED
ON THE FLOOR beside the pillow, its bottom on the floorboards and its
short back legs folded out in front of it, the body settled and low. Its
EYES ARE CLOSED - two short closed curves instead of the usual black
dots. It is not lying down and not standing.
TOTON'S BACKPACK IS OFF. It has been taken off for the night and lies on
the floorboards right beside Toton, resting on its back with its two
straps upward. Toton is NOT wearing it here.
THE BACKPACK IS YELLOW - a warm mustard yellow, the same one Toton wears
in the daytime books. It is never blue and never any other colour.
Toton is a soft blue-grey shape in the dark, and does not glow.
Mio has woken alone; Toton has not noticed yet.
The bottom third of the picture is plain empty floor.
"""),

("03_場面02_むずむず", "upper part of the picture, which is plain wall", """
DEEP NIGHT, LAMP OFF. Same blue-grey room, same futon.

Mio is still lying on her side ON THE CREAM MATTRESS, head on the cream
pillow, with the MOSS-GREEN QUILT OVER HER. She has drawn both knees up
under the quilt and pressed one hand against her tummy on top of it. Her
lower arm is folded under her body, and the cream mattress is visible
beneath that arm and beneath her shoulder and cheek. The face is a small
uncomfortable frown - the body has said something. Eyes open, looking
down towards the quilt.
The quilt is a single sheet lying over her; it does NOT have a hole in it
and her upper body does NOT emerge through a gap in it.
Mio's body rests DIRECTLY ON THE CREAM MATTRESS. The moss-green quilt is only ever over her or heaped beside her, never under her.
The lamp stands UNLIT on the stool.
Toton sits up beside the pillow now, watching Mio quietly.
The top third of the picture is plain wall.
"""),

("S04_ふとんのふち", "lower part of the picture, which is plain floor", """
DEEP NIGHT, LAMP OFF. Everything soft dusty blue-grey.

WHOLE FIGURE, not a close-up. Mio has sat halfway up, SITTING ON THE
CREAM MATTRESS, and is gripping the hem of the moss-green quilt with
BOTH small hands, pulling it a little towards the chin. The quilt lies
over her legs; the cream mattress shows under her and beside her.
Mio's body rests DIRECTLY ON THE CREAM MATTRESS. The moss-green quilt is only ever over her or heaped beside her, never under her.
 The shoulders are drawn in, the head is
turned towards the dim room, the mouth a small tight line.
Draw Mio's whole upper body: head, shoulders, the short-sleeved
nightshirt, both bare forearms, both hands on the quilt.
The lamp stands UNLIT on the stool at the left, a plain cream dome.
Toton sits on the floor beside the futon, looking up at Mio, calm.
The lower part of the picture is plain empty wood floor.
"""),
("04_場面03_でられない", "lower part of the picture, which is plain floor", """
DEEP NIGHT, LAMP OFF. THE HESITATION. This is a core page.

Mio has SAT UP ON THE CREAM MATTRESS, the moss-green quilt pushed back
so that it lies over her lower legs only, and has stopped there. Her
bottom and both hands are on the CREAM; the green is over her shins.
Mio's body rests DIRECTLY ON THE CREAM MATTRESS. The moss-green quilt is only ever over her or heaped beside her, never under her.
Shoulders drawn in a little,
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
DEEP NIGHT, LAMP OFF. THE LAMP IS NOT LIT IN THIS PICTURE.
The whole room is cool dusty blue-grey, exactly as dark as the two pages
before it. The cream dome on the stool is DULL AND MATT, with no
highlight on its crown, no sheen, no halo and no glow. There is NO warm
light anywhere in this picture - not on the wall, not on the floor, not
on the stool, not on the bedding, not on Mio. Mio's face and the futon
carry the same cool blue-grey shading as the walls.

Toton has turned and is looking UP at the low wooden stool beside the
pillow, where the unlit lamp stands. One of Toton's short front limbs is
raised slightly towards it - not touching it, just pointing the way with
its whole body. Toton is calm, mouth a single flat line.
Mio, still SITTING ON THE CREAM MATTRESS with the moss-green quilt over
her legs, has turned to follow Toton's look, head coming round towards
the stool.
Mio's body rests DIRECTLY ON THE CREAM MATTRESS. The moss-green quilt is only ever over her or heaped beside her, never under her.
The unlit lamp is clearly visible on the stool: a plain cream dome with
one big round button on top.
Toton does not glow, and does not touch the lamp.
The bottom third of the picture is plain empty floor.
"""),

("06_場面05_てをのばす", "upper part of the picture, which is plain wall", """
DEEP NIGHT, LAMP STILL OFF. Everything is the soft dusty blue-grey of the
night pages. The lamp on the stool is unlit - a plain cream dome with no
glow at all. The only brightness is a little pale moonlight.

WHOLE FIGURE, not a close-up of a hand. Mio is KNEELING UP ON THE CREAM
MATTRESS - both knees on the cream - and leaning across towards the stool
beside the pillow, one arm stretched out, the fingertips just arriving
above the unlit lamp - almost touching it, not yet pressing. The other
hand rests ON THE CREAM MATTRESS for balance.
The moss-green quilt has been thrown back and lies in a loose heap
BEHIND her, off to one side. Nothing green is under her.
Mio's body rests DIRECTLY ON THE CREAM MATTRESS. The moss-green quilt is only ever over her or heaped beside her, never under her.
Mio's face is turned towards the lamp, mouth small and set, eyes open.
Draw Mio's whole body: head, shoulders, the moss-green nightshirt to
mid-thigh, the knees on the cream mattress, the white socks.
Toton stands on the floor below the stool, looking up at the reaching
hand, calm and neutral. Toton does not glow.
The upper part of the picture is plain blue-grey wall.
"""),
("07_場面06_ついた", "upper part of the picture, which is plain wall", """
THE MOMENT THE LAMP COMES ON. This is the core page of the whole book.

THE LAMP STAYS ON THE STOOL. Mio is NOT holding it and NOT carrying it.
This is the only page in the book where the lamp is switched on, and it
is switched on exactly where it stands, on the stool.
Mio is still on the futon, KNEELING UP ON THE CREAM MATTRESS - both
knees on the cream - and leaning across towards the stool, with one arm
stretched out to it. The other hand rests ON THE CREAM MATTRESS for
balance. The moss-green quilt lies thrown back in a heap behind her.
Mio's body rests DIRECTLY ON THE CREAM MATTRESS. The moss-green quilt is only ever over her or heaped beside her, never under her.

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

("S09_じぶんでつけられた", "lower part of the picture, which is plain floor", """
LAMP ON. The warm amber pool now fills the near half of the room; the far
corners stay soft blue-grey.

Mio SITS ON THE CREAM MATTRESS looking at the lit lamp, a small calm
smile, both hands resting in the lap. Shoulders relaxed. The moss-green
quilt lies thrown back in a loose heap beside her.
Mio's body rests DIRECTLY ON THE CREAM MATTRESS. The moss-green quilt is only ever over her or heaped beside her, never under her.
Toton stands on the floor beside the stool, looking up at Mio, with ONE
SMALL MOTION MARK BESIDE EACH EAR - the ears are twitching. This is the
happy pose and it must be clearly visible here.
Toton does not glow; it is simply lit by the lamp.
The bottom third of the picture is plain empty floor.
"""),

("08_場面07_ふとんからでる", "upper part of the picture, which is plain wall", """
LAMP ON, standing on the stool. Mio is getting out of the futon. She
SITS ON THE EDGE OF THE CREAM MATTRESS with the moss-green quilt thrown
right back into a heap behind her, one white-socked foot already flat on
the wooden floor, the other still on the cream mattress, one hand on the
floor for balance, body leaning forward. The face is set and awake.
Mio's body rests DIRECTLY ON THE CREAM MATTRESS. The moss-green quilt is only ever over her or heaped beside her, never under her.
The amber light from the lamp falls across the floor where the foot has
landed. Beyond the pool, the room is blue-grey.
Toton stands on the floor waiting, calm and neutral.
The top third of the picture is plain wall.
"""),

("09_場面08_ろうか", "upper part of the picture, which is plain wall", """
THE CORRIDOR, LAMP CARRIED. Mio walks away from the camera down the
corridor, seen from BEHIND - the back of the head, the moss-green
nightshirt to mid-thigh, bare legs, white socks on the wooden floor.
THE BACK OF MIO'S HEAD: the hair is a SHORT crop. It ends WELL ABOVE the
nape, so the whole neck is bare, and it ends above the ears at the sides.
Seen from behind it is a small round cap of hair with a bare neck under
it. It is NOT a bob, NOT chin-length, and never touches the shoulders.
THERE IS ONLY ONE DOOR in this picture, at the far end. Do not draw a
second door, a doorway or a door frame on either side wall.
Mio carries the lit lamp in BOTH HANDS, held low in front of the body, so
a warm amber pool travels along the floor and up the corridor walls just
ahead of the feet. Beyond that pool the corridor is soft blue-grey, and
at its far end the cream toilet door is only just visible.
THE WASHBASIN IS NOT IN THIS PICTURE. The camera is further along the
corridor than the basin, so the basin is behind the viewer and out of
shot. Both side walls are therefore completely plain and flat: no basin,
no cabinet, no tap, and above all NO ALCOVE, NO NICHE and NO RECESS -
the walls never step back anywhere. Just two plain flat walls running
away to the door.
THE TOILET DOOR IS AT THE FAR END, straight ahead, and it is CLOSED.
There is no door on the right-hand wall and no door on the left-hand
wall, and no gap of dark room showing beside the door.
Toton walks on the floor beside Mio's ankle, inside the pool of light,
lit by it. Toton does not glow.
The top third of the picture is plain wall.
"""),

("S13_トイレのドア", "upper part of the picture, which is plain wall", """
THE TOILET DOOR, seen from the corridor.

Stand the camera back a little, so some corridor is visible on either
side of the door and the whole basin fits in.
The plain cream door stands at the far end in the middle of the picture,
closed, with its round wooden knob on the RIGHT-HAND edge and the open
gap along its bottom. There is only ONE door.
THE WASHBASIN IS NOT IN THIS PICTURE. The camera is further along the
corridor than the basin, so the basin is behind the viewer and out of
shot. Both side walls are therefore completely plain and flat: no basin,
no cabinet, no tap, and above all NO ALCOVE, NO NICHE and NO RECESS -
the walls never step back anywhere. Just two plain flat walls running
away to the door.
THE TOILET DOOR IS AT THE FAR END, straight ahead, and it is CLOSED.
There is no door on the right-hand wall and no door on the left-hand
wall, and no gap of dark room showing beside the door.

Mio stands in front of it, seen from behind and slightly to the side.
THE BACK OF MIO'S HEAD: the hair is a SHORT crop that ends WELL ABOVE the
nape, leaving the whole neck bare, and above the ears at the sides. It is
NOT a bob, NOT chin-length, and never reaches the jaw.
THE LAMP IS NOT IN MIO'S HANDS. Mio has SET IT DOWN on the corridor
floor beside one foot, where it stands upright and lit, throwing a warm
amber pool up onto the bottom of the door and across the floor. Both of
Mio's hands are free. THE RAISED HAND IS ALREADY TOUCHING THE ROUND KNOB
- the small fingers are closed around it, in contact with it, not
hovering near it and not reaching towards the flat of the door. The other
hand hangs at her side.
The lamp has no handle and is never dangled - that is why it is on the
floor here.
Above the pool of light the door and the corridor fade to blue-grey.
Toton stands on the floor beside the lamp, in the light, looking up.
The upper part of the picture is plain wall.
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
THE WASHBASIN IS IN THIS PICTURE. On the RIGHT-HAND WALL of the
corridor, nearer the camera than the toilet door, the small white
washbasin on its light-wood cabinet stands against the wall and juts into
the corridor. It is seen from the side, on the RIGHT of the picture. Do
not leave that stretch of wall empty.
THE TOILET DOOR IS AT THE FAR END, straight ahead. There is no door on
the right-hand wall and no door on the left-hand wall.
The basin stands in the blue-grey, outside the band of light.
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
THE WASHBASIN IS IN THIS PICTURE. On the RIGHT-HAND WALL of the
corridor, nearer the camera than the toilet door, the small white
washbasin on its light-wood cabinet stands against the wall and juts into
the corridor. It is seen from the side, on the RIGHT of the picture. Do
not leave that stretch of wall empty.
THE TOILET DOOR IS AT THE FAR END, straight ahead. There is no door on
the right-hand wall and no door on the left-hand wall.
The corridor stays soft blue-grey.
Same hard limits as before: door shut, no Mio, no fixtures, plain wall
above the door.
The top third of the picture is plain wall.
"""),

("S14_てをあらう", "lower part of the picture, which is plain floor", """
THE WASHBASIN IN THE CORRIDOR. Same corridor, same camera as every other
corridor page: the camera stands at the bedroom end and looks along it.

LAYOUT, AND IT MUST MATCH THE OTHER CORRIDOR PAGES EXACTLY:
- The basin is on the RIGHT-HAND WALL, on the RIGHT of the picture,
  fairly close to the camera. Plain white basin, light-wood cabinet, one
  tap, no mirror.
- The TOILET DOOR is at the FAR END of the corridor, straight ahead and
  BEYOND MIO, small with distance, closed now. It is NOT on the
  right-hand wall. There is no other door anywhere in this picture, and
  no door beside or behind Toton.
- The left-hand wall is bare.

WHOLE FIGURE, SEEN FROM THE SIDE. Mio stands at the basin FACING RIGHT,
towards the right-hand wall, up on tiptoe a little, both hands held under
a thin stream of water from the single tap. Head bent forward, looking
down at the hands. The whole child is in the picture: head, body, the
short-sleeved nightshirt to mid-thigh, bare legs, white socks on the
floor.
The lit lamp stands on the corner of the basin, throwing warm amber over
the water, the hands and Mio's face.
There is NO mirror above the basin - the wall above it is plain. Do not
draw a mirror, a frame or a reflection anywhere, and never let an arm or
a hand appear out of the wall.
Toton stands on the floor beside Mio's feet, looking up.
Beyond the amber pool the corridor is soft blue-grey.
The lower part of the picture is plain empty floor.
"""),
("12_場面11_もどる", "upper part of the picture, which is plain wall", """
BACK ALONG THE CORRIDOR, LAMP CARRIED, walking TOWARDS the camera now.
Mio comes back up the corridor holding the lit lamp in both hands in
front of the body. The warm amber pool lights Mio's face gently from
below, and the face is calm and easy - the walk back is not frightening.
Behind Mio the corridor recedes into soft blue-grey, with the closed
toilet door small at its far end.
THE WASHBASIN IS IN THIS PICTURE. On the RIGHT-HAND WALL of the
corridor, nearer the camera than the toilet door, the small white
washbasin on its light-wood cabinet stands against the wall and juts into
the corridor. It is seen from the side, on the RIGHT of the picture. Do
not leave that stretch of wall empty.
THE TOILET DOOR IS AT THE FAR END, straight ahead. There is no door on
the right-hand wall and no door on the left-hand wall.
Mio has already walked past the basin, so it stands behind her on the
right, at the edge of the light.
Toton walks beside Mio's ankle inside the pool of light.
The top third of the picture is plain wall.
"""),

("13_場面12_またねる", "upper part of the picture, which is plain wall", """
BACK IN THE BEDROOM, and the lamp has been SWITCHED OFF again. The room
has returned to soft dusty blue-grey, with a little pale moonlight
through the curtain. The lamp stands UNLIT on the stool where it began -
a plain cream dome, no glow.

Mio LIES DIRECTLY ON THE CREAM MATTRESS, curled on one side, head on the
ONE CREAM pillow, with the MOSS-GREEN QUILT DRAWN UP OVER HER BODY to the
shoulders so that only her head and one hand are outside it. Eyes CLOSED,
mouth soft and settled - already asleep. Peaceful, not frightened. The
dark is just the dark now.
Mio's body rests DIRECTLY ON THE CREAM MATTRESS. The moss-green quilt is
over her, never under her. She is not lying on top of the green.

TOTON IS SITTING DOWN, NOT STANDING. This matters. Toton is SEATED ON THE
FLOOR beside the stool, its bottom on the floorboards and its short back
legs folded out in front of it, the body settled and low - the posture of
a small animal that has sat down for the night. Do not draw Toton
standing upright on its feet.
Its EYES ARE CLOSED - two short closed curves instead of the usual black
dots. Calm and settled, asleep sitting up.
TOTON'S YELLOW BACKPACK IS OFF. It has been taken off for the night and
lies on the floorboards right beside Toton, resting on its back with its
two straps upward, small and neat. Toton is NOT wearing it in this
picture; it is the only page where the backpack is off.
TOTON HAS NO TAIL. Do not draw a round tail, a stub, a bobble or any
tail-like shape behind it. Toton is not a cat and not a rabbit: one
continuous egg-shaped body, two small round ears set high and wide
apart, and nothing behind.
The upper part of the picture is plain wall.
"""),
("S18_つぎのよる", "lower part of the picture, which is plain floor", """
ANOTHER NIGHT, LAMP OFF, blue-grey room, the same futon and stool.

Mio has woken again and is already SITTING UP ON THE CREAM MATTRESS,
with the moss-green quilt thrown back into a loose heap beside her, and
this time reaches straight out towards the unlit lamp on the stool
without hesitating - the arm extended, the hand almost at the button.
Mio's body rests DIRECTLY ON THE CREAM MATTRESS. The moss-green quilt is
never under her.
HER FACE IS PLEASED. THE CORNERS OF HER MOUTH ARE TURNED UP in a clear,
warm little smile - not a flat line, not a neutral mouth. The eyes are
soft and easy. This is the last picture in the book and she is confident
now. No drawn-in shoulders, no uncertainty.
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
