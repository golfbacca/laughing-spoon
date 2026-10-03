#!/usr/bin/env python3
"""Printify入稿用SVGの検査。

Printifyヘルプセンターの制約（tapestry/docs/02）:
  ファイル 20MB以下 / パス要素 20,000個以下 / <text>不可 / ラスター埋め込みは非推奨

使い方: python3 tapestry/tools/check_svg.py ファイル.svg [...]
"""
import os
import sys
import xml.etree.ElementTree as ET

MAX_BYTES = 20 * 1024 * 1024
MAX_PATHS = 20000
SHAPES = {"path", "rect", "circle", "ellipse", "line", "polyline", "polygon"}


def local(tag):
    return tag.rsplit("}", 1)[-1]


def check(fn):
    ok = True
    size = os.path.getsize(fn)
    root = ET.parse(fn).getroot()
    tags = [local(e.tag) for e in root.iter()]
    n_path = tags.count("path")
    n_shape = sum(tags.count(t) for t in SHAPES)
    n_text = tags.count("text") + tags.count("tspan")
    n_image = tags.count("image")
    n_filter = tags.count("filter")
    print(f"== {fn}")
    print(f"  width×height : {root.get('width')} × {root.get('height')}  viewBox={root.get('viewBox')}")
    rows = [
        ("ファイルサイズ", f"{size/1024/1024:.2f} MB", size <= MAX_BYTES, "≤ 20MB"),
        ("path要素", n_path, n_path <= MAX_PATHS, "≤ 20,000"),
        ("図形要素の合計", n_shape, n_shape <= MAX_PATHS, "≤ 20,000（安全側で全図形を数える）"),
        ("<text>", n_text, n_text == 0, "0（アウトライン化必須）"),
        ("<image>", n_image, n_image == 0, "0（ラスター埋め込み）"),
    ]
    for name, val, good, rule in rows:
        ok &= good
        print(f"  {'OK ' if good else 'NG '} {name}: {val}  [{rule}]")
    if n_filter:
        print(f"  注意 <filter> が {n_filter} 個。Printifyで出るか未確認")
    return ok


if __name__ == "__main__":
    results = [check(f) for f in sys.argv[1:]]
    sys.exit(0 if results and all(results) else 1)
