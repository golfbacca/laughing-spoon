"""解答図の一覧を1枚の画像にする（絵柄の見た目を確かめる用）。"""
import sys, glob, os
sys.path.insert(0, os.path.dirname(__file__))
from nonogram import load, check
from PIL import Image, ImageDraw, ImageFont
DIR = sys.argv[2] if len(sys.argv) > 2 else "puzzles"
files = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", DIR, "*.txt")))
B, P = 300 if DIR != "puzzles" else 210, 24   # 1枚の絵の一辺
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
cols = 4 if B == 210 else 3; rowsn = -(-len(files) // cols)
W = cols * (B + P) + P; H = rowsn * (B + P + 26) + P
im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
for i, fn in enumerate(files):
    g = load(fn); r = check(g)
    C = B // max(len(g), len(g[0]))
    ox = P + (i % cols) * (B + P); oy = P + (i // cols) * (B + P + 26)
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            d.rectangle([ox + x * C, oy + y * C, ox + x * C + C, oy + y * C + C],
                        fill="black" if c else "white", outline="#bbb")
    ok = "OK" if r["logic_only"] else "NG"
    d.text((ox, oy + len(g) * C + 4), f"{os.path.basename(fn)[:-4]}  {ok}", fill="black" if ok == "OK" else "red", font=f)
im.save(sys.argv[1]); print(im.size)
