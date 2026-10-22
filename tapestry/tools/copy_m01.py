#!/usr/bin/env python3
"""M01の出品文言（タイトル・タグ・説明文）と、Etsyの上限の検査。docs/08 と同じ内容。

検査のあと、コピー用に listing/M01_<色>/title.txt・tags.txt・description.txt を書き出す。
"""
import os
COMMON_TAGS = ["mountain tapestry", "wall hanging", "large tapestry", "boho tapestry",
               "mountain wall art", "minimalist wall art", "bedroom wall decor",
               "dorm room decor", "landscape tapestry"]
LISTINGS = {
    "night": ("Mountain Tapestry Wall Hanging, Moon and Stars Celestial Tapestry, "
              "Large Boho Wall Art, Minimalist Night Sky Bedroom Decor",
              ["celestial tapestry", "moon tapestry", "night sky tapestry", "starry sky decor"]),
    "dusk": ("Mountain Tapestry Wall Hanging, Boho Sunset Tapestry, Large Desert Sun Wall Art, "
             "Terracotta Minimalist Landscape Decor",
             ["sunset tapestry", "desert wall art", "terracotta decor", "boho sun tapestry"]),
    "dawn": ("Mountain Tapestry Wall Hanging, Pink Sunrise Tapestry, Large Boho Wall Art, "
             "Pastel Minimalist Landscape Bedroom Decor",
             ["sunrise tapestry", "pink tapestry", "pastel wall art", "boho sun tapestry"]),
    "sage": ("Mountain Tapestry Wall Hanging, Sage Green Tapestry, Large Boho Sun Wall Art, "
             "Minimalist Nature Landscape Bedroom Decor",
             ["sage green decor", "green tapestry", "nature tapestry", "sun tapestry"]),
}
BANNED = ["woven", "cotton", "linen", "fringe", "handmade"]  # 事実と違う語（docs/05）

ok = True
for k, (title, extra) in LISTINGS.items():
    tags = COMMON_TAGS + extra
    probs = []
    if len(title) > 140:
        probs.append(f"タイトル{len(title)}字")
    if len(tags) != 13 or len(set(tags)) != 13:
        probs.append("タグ数/重複")
    probs += [f"タグ長 {t}({len(t)})" for t in tags if len(t) > 20]
    probs += [f"禁止語 {b}" for b in BANNED if b in (title + " ".join(tags)).lower()]
    ok &= not probs
    print(f"{k}: タイトル{len(title)}字 / タグ{len(tags)}個 / 最長{max(map(len, tags))}字 "
          f"{'OK' if not probs else probs}")
    print("   ", ", ".join(tags))
NAMES = {"dawn": "Dawn Pink", "dusk": "Desert Dusk", "night": "Moonlit Night", "sage": "Sage Forest"}
LEAD = {
    "night": "Layered peaks under a crescent moon and a sky full of stars, in deep navy tones.",
    "dusk": "Layered peaks beneath a glowing desert sun, in warm terracotta tones.",
    "dawn": "Layered peaks greeting a soft pink sunrise, in gentle pastel tones.",
    "sage": "Layered peaks under a golden sun, in calm sage green tones.",
}
BODY = """Bring the calm of the mountains to your wall. {lead}

WHAT YOU GET
- One printed wall tapestry, 100% polyester
- Vivid dye-sublimation print with hemmed edges
- Lightweight and easy to hang, move, or fold

SIZES (portrait)
- 26" x 36" (66 x 91 cm)
- 50" x 60" (127 x 152 cm)
- 68" x 80" (173 x 203 cm)
- 88" x 104" (224 x 264 cm) - larger than a person; please measure your wall

Please note: the smallest size (26" x 36") is a little narrower, so a small strip on the left and right edges of the artwork is trimmed. The {focal} and mountains stay fully visible.

GOOD TO KNOW
- This is a printed tapestry, not woven. The surface is smooth and flat, with no fringe.
- Hanging hardware is not included.
- Each tapestry is made to order just for you.
- Colors may vary slightly between screens and the printed fabric.

ABOUT THE ARTWORK
- This design was created by our small studio using AI-assisted digital tools.
- The room photos are digital mockups, made to show the style and approximate size. The printed design is the same as shown.

MORE COLORS
This design also comes in {others}. Visit the shop to see them all.
"""
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "listing")
for k, (title, extra) in LISTINGS.items():
    others = [NAMES[o] for o in ("dawn", "dusk", "night", "sage") if o != k]
    desc = BODY.format(lead=LEAD[k], focal="moon" if k == "night" else "sun",
                       others=f"{others[0]}, {others[1]}, and {others[2]}")
    assert not any(b in desc.lower() for b in ("cotton", "linen", "handmade")), k
    assert len(desc) <= 13000
    d = os.path.join(root, f"M01_{k}")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "title.txt"), "w").write(title + "\n")
    open(os.path.join(d, "tags.txt"), "w").write(", ".join(COMMON_TAGS + extra) + "\n")
    open(os.path.join(d, "description.txt"), "w").write(desc)
print("コピー用ファイルを listing/M01_<色>/ に書き出した")
raise SystemExit(0 if ok else 1)
