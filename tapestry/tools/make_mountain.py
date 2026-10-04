#!/usr/bin/env python3
"""層状の山並み＋太陽／月のタペストリー（SVG）を色違いで生成する。

形（山の稜線・太陽の位置）は全色で共通。色だけを差し替える＝シリーズとして揃う。
キャンバスは 88×104 の印刷エリア 13650×16125（縦長4サイズ共通の絵。docs/04）。
重要な要素（太陽・月）は全サイズ共通の安全域 x 1,420〜12,230 / y 1,230〜14,895 に入れる。

使い方: python3 tapestry/tools/make_mountain.py            # 全色
        python3 tapestry/tools/make_mountain.py dusk night  # 指定した色だけ
出力:   tapestry/source/M01_<色>.svg と tapestry/preview/M01_<色>.png（幅1365px）
"""
import math
import os
import random
import sys

W, H = 13650, 16125
SAFE = (1420, 1230, 12230, 14895)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---- 形（全色共通） -------------------------------------------------------
SUN_CX, SUN_CY, SUN_R = W * 0.5, H * 0.40, W * 0.165
# 山の層：奥→手前。基準の高さ（谷の高さ）と、峰のリスト (中心u, 高さ, 半幅, 尖り)
# 尖り>1 で峰が尖る（奥の層＝山）。手前ほど低く丸く（丘）。
# 最奥の2峰の谷に太陽が収まる構図。
LAYERS = [
    (0.555, [(0.17, 0.200, 0.36, 1.6), (0.83, 0.180, 0.36, 1.6)]),
    (0.625, [(-0.02, 0.140, 0.26, 1.5), (0.36, 0.105, 0.20, 1.5), (0.70, 0.130, 0.24, 1.5)]),
    (0.700, [(0.22, 0.100, 0.30, 1.3), (0.62, 0.060, 0.18, 1.3), (0.97, 0.110, 0.30, 1.3)]),
    (0.775, [(0.05, 0.060, 0.35, 1.0), (0.48, 0.050, 0.30, 1.0), (0.86, 0.065, 0.32, 1.0)]),
    (0.850, [(0.30, 0.050, 0.40, 1.0), (0.78, 0.040, 0.35, 1.0)]),
    (0.925, [(0.10, 0.035, 0.40, 1.0), (0.60, 0.040, 0.45, 1.0)]),
]


def ridge(base, peaks):
    """稜線の点列。峰は (1-|x|)^尖り の山形を max で重ねる（峰が独立して立つ）。"""
    pts = []
    n = 120
    for i in range(n + 1):
        u = -0.02 + 1.04 * i / n
        h = 0.0
        for c, amp, w, sharp in peaks:
            x = abs(u - c) / w
            if x < 1:
                h = max(h, amp * (1 - x) ** sharp if sharp > 1.05 else amp * math.cos(x * math.pi / 2) ** 2)
        pts.append((u * W, (base - h) * H))
    return pts


def smooth_path(pts):
    """Catmull-Rom → 3次ベジェ。下辺を閉じて塗れる形にする。"""
    d = [f"M{pts[0][0]:.0f},{H + 10} L{pts[0][0]:.0f},{pts[0][1]:.0f}"]
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.0f},{c1[1]:.0f} {c2[0]:.0f},{c2[1]:.0f} {p2[0]:.0f},{p2[1]:.0f}")
    d.append(f"L{pts[-1][0]:.0f},{H + 10} Z")
    return " ".join(d)


RIDGES = [smooth_path(ridge(*L)) for L in LAYERS]


def crescent(cx, cy, r, ox, oy):
    """円A(cx,cy,r) から 円B(cx+ox,cy+oy,r) を引いた三日月（円弧2本の正確な形）。"""
    d = math.hypot(ox, oy)
    mx, my = cx + ox / 2, cy + oy / 2
    h = math.sqrt(r * r - (d / 2) ** 2)
    nx, ny = -oy / d, ox / d
    p1 = (mx + h * nx, my + h * ny)
    p2 = (mx - h * nx, my - h * ny)
    # Aの弧はBから遠い側（大きい弧）、Bの弧はAの内側（小さい弧）
    return (f"M{p1[0]:.1f},{p1[1]:.1f} A{r:.1f},{r:.1f} 0 1,1 {p2[0]:.1f},{p2[1]:.1f} "
            f"A{r:.1f},{r:.1f} 0 0,0 {p1[0]:.1f},{p1[1]:.1f} Z")


# ---- 色（ここだけ差し替える） ---------------------------------------------
PALETTES = {
    # 夜明け：桃色〜すみれ
    "dawn": dict(sky=("#f3c9b8", "#fbe9dc"), sun="#f29e7f", rings="#f6b59a",
                 ridges=["#e9b2a1", "#d68f86", "#b96f80", "#8c5376", "#5e3b62", "#33244a"]),
    # 夕暮れ：テラコッタ（ボーホー寄り）
    "dusk": dict(sky=("#f2c08a", "#f8e4c6"), sun="#e06f3c", rings="#ea915c",
                 ridges=["#eaa46b", "#d27f4a", "#ad5c3b", "#7f4231", "#542d25", "#2f1b17"]),
    # 夜：紺に月と星（celestial）
    "night": dict(sky=("#0e1a33", "#2b3d66"), sun="#f1e4c4", rings=None, moon=True,
                  ridges=["#3b4f7c", "#30436c", "#26365a", "#1d2a47", "#151f36", "#0d1424"]),
    # 森：セージグリーン
    "sage": dict(sky=("#dfe3cf", "#f2f0e3"), sun="#e9b44c", rings="#eec777",
                 ridges=["#b9c4a4", "#97a884", "#768a69", "#566c52", "#3b4f3d", "#23322a"]),
}


def build(name, pal):
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    a('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="{pal["sky"][0]}"/>'
      f'<stop offset="0.6" stop-color="{pal["sky"][1]}"/></linearGradient></defs>')
    a(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')

    if pal.get("moon"):
        rnd = random.Random(7)
        for _ in range(140):  # 星：空の範囲だけ
            x, y = rnd.uniform(0, W), rnd.uniform(0, H * 0.55)
            if math.hypot(x - SUN_CX, y - SUN_CY) < SUN_R * 1.5:
                continue
            r = rnd.choice([18, 24, 30, 30, 40, 55])
            a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{pal["sun"]}" '
              f'fill-opacity="{rnd.uniform(0.55, 1):.2f}"/>')
        # 三日月：右上に寄せた円でくり抜く（右下が欠ける＝左に膨らむ月）
        r = SUN_R * 0.85
        a(f'<path fill="{pal["sun"]}" d="{crescent(SUN_CX, SUN_CY - SUN_R * 0.35, r, r * 0.42, -r * 0.22)}"/>')
    else:
        for k, f in ((3, 1.75), (2, 1.48), (1, 1.24)):  # 太陽の輪（外ほど薄く）
            a(f'<circle cx="{SUN_CX:.0f}" cy="{SUN_CY:.0f}" r="{SUN_R * f:.0f}" '
              f'fill="{pal["rings"]}" fill-opacity="{0.18 * (4 - k):.2f}"/>')
        a(f'<circle cx="{SUN_CX:.0f}" cy="{SUN_CY:.0f}" r="{SUN_R:.0f}" fill="{pal["sun"]}"/>')

    for d, c in zip(RIDGES, pal["ridges"]):
        a(f'<path d="{d}" fill="{c}"/>')
    a('</svg>')
    return "\n".join(o)


def main(names):
    import cairosvg
    os.makedirs(os.path.join(ROOT, "source"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "preview"), exist_ok=True)
    for n in names:
        svg = build(n, PALETTES[n])
        fn = os.path.join(ROOT, "source", f"M01_{n}.svg")
        open(fn, "w").write(svg)
        cairosvg.svg2png(bytestring=svg.encode(), output_width=1365,
                         write_to=os.path.join(ROOT, "preview", f"M01_{n}.png"))
        print(fn)


if __name__ == "__main__":
    main(sys.argv[1:] or list(PALETTES))
