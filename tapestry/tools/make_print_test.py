#!/usr/bin/env python3
"""Printifyの挙動を確かめるための試験用SVG（売り物ではない）。

確かめること:
  1. 十字の目盛り … サイズを切り替えたとき、端がどこまで切れるかを数えて測る
     （1目盛り＝幅/高さの1%。5目盛りごとに赤、10目盛りごとに青。
       中央で交差させているので、四隅で目盛りが隠れない）
  2. 8枠 … 平塗り / 線形グラデ / 円形グラデ / 半透明 / クリップ / 線の太さ /
     透明度つきグラデ / 曲線パス がPrintifyのプレビューで正しく出るか
出力: tapestry/test/print_test.svg
"""
W, H = 13650, 16125  # 88"x104" の Print area（docs/02）
out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a('<defs>'
  '<linearGradient id="lg" x1="0" y1="0" x2="1" y2="0">'
  '<stop offset="0" stop-color="#1b2a4a"/><stop offset="1" stop-color="#f2a65a"/></linearGradient>'
  '<radialGradient id="rg"><stop offset="0" stop-color="#ffe9a8"/>'
  '<stop offset="1" stop-color="#c0392b"/></radialGradient>'
  '<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">'
  '<stop offset="0" stop-color="#f2a65a" stop-opacity="1"/>'
  '<stop offset="1" stop-color="#f2a65a" stop-opacity="0"/></linearGradient>'
  '<clipPath id="cp"><circle cx="0.5" cy="0.5" r="0.5"/></clipPath>'
  '</defs>')
a(f'<rect width="{W}" height="{H}" fill="#efe9dd"/>')


BAND = 800  # 目盛りの帯の太さ(px)


def ruler(horizontal):
    """中央を横切る目盛り。1%ごとに白黒交互、5%ごとに赤、10%ごとに青。"""
    length = W if horizontal else H
    for i in range(100):
        p0, p1 = length * i / 100, length * (i + 1) / 100
        if i % 10 == 0:
            c = "#1f5fbf"
        elif i % 5 == 0:
            c = "#d62828"
        else:
            c = "#222222" if i % 2 else "#ffffff"
        if horizontal:
            a(f'<rect x="{p0:.1f}" y="{H/2-BAND/2}" width="{p1-p0:.1f}" height="{BAND}" fill="{c}"/>')
        else:
            a(f'<rect x="{W/2-BAND/2}" y="{p0:.1f}" width="{BAND}" height="{p1-p0:.1f}" fill="{c}"/>')


# 8枠（左右2列 × 上下2段ずつ。十字の帯を避ける）
bw, bh = 4000, 3200
xs = [W / 4 - bw / 2 + 200, 3 * W / 4 - bw / 2 - 200]
ys = [H / 4 - bh / 2 - 1800, H / 4 - bh / 2 + 1800, 3 * H / 4 - bh / 2 - 1800, 3 * H / 4 - bh / 2 + 1800]
cells = [(x, y) for y in ys for x in xs]
(x, y) = cells[0]; a(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="#2e6f5e"/>')
(x, y) = cells[1]; a(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="url(#lg)"/>')
(x, y) = cells[2]; a(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="url(#rg)"/>')
(x, y) = cells[3]
a(f'<circle cx="{x+bw*0.38}" cy="{y+bh/2}" r="{bh*0.4}" fill="#1f5fbf" fill-opacity="0.5"/>')
a(f'<circle cx="{x+bw*0.62}" cy="{y+bh/2}" r="{bh*0.4}" fill="#d62828" fill-opacity="0.5"/>')
(x, y) = cells[4]
a(f'<g clip-path="url(#cp)" transform="translate({x+(bw-bh)/2},{y}) scale({bh})">'
  '<rect width="0.5" height="1" fill="#1b2a4a"/><rect x="0.5" width="0.5" height="1" fill="#f2a65a"/></g>')
(x, y) = cells[5]
for i, sw in enumerate([5, 10, 20, 40, 80, 160]):  # 線幅(px)。155px/インチ
    yy = y + bh * (i + 0.5) / 6
    a(f'<line x1="{x}" y1="{yy}" x2="{x+bw}" y2="{yy}" stroke="#111" stroke-width="{sw}"/>')
(x, y) = cells[6]
a(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="#2e6f5e"/>')
a(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="url(#fade)"/>')
(x, y) = cells[7]
a(f'<path d="M{x},{y+bh} C{x+bw*0.25},{y} {x+bw*0.5},{y+bh*0.2} {x+bw*0.6},{y+bh*0.6} '
  f'S{x+bw*0.9},{y+bh*0.3} {x+bw},{y+bh*0.5} L{x+bw},{y+bh} Z" fill="#7a4e9c"/>')

ruler(False)
ruler(True)
a('</svg>')

import os
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "test"), exist_ok=True)
fn = os.path.join(os.path.dirname(__file__), "..", "test", "print_test.svg")
open(fn, "w").write("\n".join(out))
print(fn)
