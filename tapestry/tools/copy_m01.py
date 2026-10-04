#!/usr/bin/env python3
"""M01の出品文言（タイトル・タグ）と、Etsyの上限の検査。docs/08 と同じ内容。"""
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
raise SystemExit(0 if ok else 1)
