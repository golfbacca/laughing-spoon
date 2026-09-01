#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ページ間の【つながり】を機械で調べる。

  python3 check3.py            → 数値と、比較用の帯を書き出す

なぜ要るか（作業記録16章）:
  1枚ずつサムネイルで見ても、ページ間のズレは分からない。
  「指摘された項目が直ったか」しか見ないと、描き直しのたびに
  別の場所が割れていることに気づけない。
  同じ場所だけを切り出して並べ、数値でも出す。
  描き直したら毎回これを通す。目視の前に、まず数字を見る。
"""
import pathlib, sys
import numpy as np
from PIL import Image, ImageDraw

IMG = pathlib.Path(__file__).resolve().parents[1] / "絵本KDP_3冊目_画像"
OUT = pathlib.Path("/tmp")

BEDROOM = [("01","01_表表紙_正方形"),("02","S01_ねるまえ"),("03","02_場面01_めがさめる"),
           ("04","03_場面02_むずむず"),("05","S04_ふとんのふち"),("06","04_場面03_でられない"),
           ("07","05_場面04_ここにある"),("08","06_場面05_てをのばす"),("09","07_場面06_ついた"),
           ("10","S09_じぶんでつけられた"),("11","08_場面07_ふとんからでる"),
           ("18","13_場面12_またねる"),("19","S18_つぎのよる"),("20","14_裏表紙_正方形")]
CORRIDOR = [("12","09_場面08_ろうか"),("13","S13_トイレのドア"),("14","10_場面09_トイレのなか"),
            ("15","11_場面10_おわりのおと"),("16","S14_てをあらう"),("17","12_場面11_もどる")]

def hue_of(a):
    """壁の色みを1つの数字にする。青みの強さ = B - R。"""
    return float(a[:, :, 2].mean() - a[:, :, 0].mean())

def wood_of(a):
    """木の色みを R と、明るさで表す。丸椅子の色ちがいを拾うため。"""
    return float(a[:, :, 0].mean()), float(a.mean())

def report():
    print("■ 寝室 — 壁の青み(B-R) と 左下すみ（丸椅子とあかり）の色")
    print(f"{'#':<5}{'壁の青み':>9}{'すみの明るさ':>13}{'すみのR':>9}")
    rows = []
    for n, f in BEDROOM:
        p = IMG / f"{f}.jpg"
        if not p.exists():
            print(f"{n:<5}（ファイルなし）"); continue
        a = np.asarray(Image.open(p).convert("RGB").resize((512, 512)), dtype=float)
        wall = hue_of(a[40:170, 20:200])
        r, v = wood_of(a[300:420, 10:150])
        rows.append((n, wall, v, r))
        print(f"{n:<5}{wall:9.1f}{v:13.1f}{r:9.1f}")
    if rows:
        for name, i in (("壁の青み", 1), ("すみの明るさ", 2)):
            xs = np.array([r[i] for r in rows]); m = xs.mean()
            bad = [rows[j][0] for j in range(len(rows)) if abs(xs[j] - m) > 1.6 * xs.std()]
            print(f"  {name}: 平均{m:.1f} ばらつき{xs.std():.1f}"
                  f"  外れ → {' '.join(bad) if bad else 'なし'}")

    print()
    print("■ 廊下 — 壁の青み(B-R)")
    for n, f in CORRIDOR:
        p = IMG / f"{f}.jpg"
        if not p.exists():
            print(f"{n:<5}（ファイルなし）"); continue
        a = np.asarray(Image.open(p).convert("RGB").resize((512, 512)), dtype=float)
        print(f"{n:<5}{hue_of(a[60:200, 20:120]):9.1f}")

def strip(pages, box, out, T=330, per=7):
    x0, y0, x1, y1 = box
    rows = (len(pages) + per - 1) // per
    sh = Image.new("RGB", (T * per, (T + 24) * rows), "white")
    d = ImageDraw.Draw(sh)
    for i, (n, f) in enumerate(pages):
        p = IMG / f"{f}.jpg"
        if not p.exists():
            continue
        im = Image.open(p); w, h = im.size
        c = im.crop((int(x0*w), int(y0*h), int(x1*w), int(y1*h))).resize((T, T))
        sh.paste(c, ((i % per) * T, (i // per) * (T + 24) + 24))
        d.text(((i % per) * T + 5, (i // per) * (T + 24) + 5), n, fill="black")
    sh.save(out, quality=92)
    print("  帯:", out)

if __name__ == "__main__":
    report()
    print()
    print("■ 比較用の帯")
    strip(BEDROOM,  (0, .30, .42, .92), OUT / "check_あかりと椅子.jpg")
    strip(BEDROOM,  (0, 0, 1, 1),       OUT / "check_寝室ぜんぶ.jpg")
    strip(CORRIDOR, (0, 0, 1, 1),       OUT / "check_廊下.jpg")
