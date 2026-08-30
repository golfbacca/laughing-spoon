#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""【3冊目では使えない。実行しても止まる】

★★ この本にこのツールを使ってはいけない ★★

  このツールは「青系画素の最大の連結塊」をトトンとみなす。
  昼の本ではそれで正しかったが、3冊目は夜の本で、
  部屋の壁そのものが青灰色である。
  実際に測ると基準色が R146 G155 B179 になった。
  これはトトンの水色（R214 G223 B244 前後）ではなく、【壁の色】である。
  このまま --apply すると、壁の色に合わせて絵を壊す。
  2冊目で床の青いパンツを拾って2枚を退色させたのと同じ失敗である。

  そこで、拾った領域が画面の15%を超えたら止めるようにした。
  夜の本のトトンの色は、一覧シートを目で見て確かめること。

（以下は元の説明）
トトンの体色のぶれを、生成ではなく画素で直す。

なぜ生成で直さないか（1冊目の原則の応用）:
  色だけの問題で描き直すと、せっかく合った構図（足の本数など）が
  また転ぶ。色は数値で測れて数値で直せるので、画素で直すほうが確実。

測り方:
  トトンの淡い水色にあたる画素を拾って平均RGBを出す。
  正しい絵は G が R より10前後 高い（水色）。
  紫に転んだ絵は R が G を上回る。

  python3 fix_toton_color.py            測るだけ
  python3 fix_toton_color.py --apply    ずれた絵を直す
"""
import sys, pathlib
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import prompts3

IMG = pathlib.Path(__file__).resolve().parents[2]/"docs"/"絵本KDP_3冊目_画像"
TOL = 10.0       # これ以上離れたら直す。±10は水彩のゆらぎの範囲なので、
                 # それ未満は触らない。2回かけて2枚を退色させた（下記の罠）

def mask_of(a):
    """トトン本体だけを拾う。

    【罠・2026-08-26に実際にやらかした】
    「青っぽい画素すべて」でマスクを作ると、床に置いた青いパンツや
    白い靴下まで入る。場面06ではそちらが多数派になり、
    トトンではなくパンツの色を補正してしまった。
    しかも2回かけたのでトトンのほうが退色した。

    そこで、青系画素の【最大の連結塊】だけをトトンとみなす。
    パンツや靴下は小さいので落ちる。
    直したあとは必ず測り直し、画素数が急に減っていないか見ること。
    減っていたら、そのページは補正が外れている。
    """
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (b - r > 15) & (b > 150) & (b < 252) & (r > 120)
    m = ndimage.binary_opening(m, np.ones((5, 5)))
    lab, n = ndimage.label(m)
    if n == 0:
        return np.zeros_like(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    big = (lab == (int(np.argmax(sizes)) + 1))
    return big if big.sum() > 4000 else np.zeros_like(m)

def measure(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    m = mask_of(a)
    if m.sum() < 3000:
        return None, m
    return np.array([a[..., c][m].mean() for c in range(3)]), m

def main(apply=False):
    # 夜の本で壁を拾っていないかを先に確かめる。
    # 面積で見ると表紙は光が当たっていて通ってしまうので、【色そのもの】で見る。
    # トトンの水色は R214 G223 B244 前後と明るい。夜の壁は R146 前後と暗い。
    probe = {}
    for n in prompts3.NAMES:
        v, _ = measure(IMG/f"{n}.jpg")
        if v is not None:
            probe[n] = v
    if probe:
        med = np.median(np.array(list(probe.values())), axis=0)
        if med[0] < 190:
            raise SystemExit(
                f"中止: 拾った色の中央値が R{med[0]:.0f} G{med[1]:.0f} B{med[2]:.0f} で暗すぎる。\n"
                "  トトンの水色（R214 G223 B244 前後）ではなく、\n"
                "  夜の青灰色の壁を拾っている。この本にこのツールは使えない。\n"
                "  トトンの色は一覧シートを目で見て確かめること。")
    stats = {}
    for n in prompts3.NAMES:
        v, _ = measure(IMG/f"{n}.jpg")
        if v is not None:
            stats[n] = v
    # 基準は「G が R より高い（＝水色のまま）」絵だけの平均
    target = np.median(np.array(list(stats.values())), axis=0)
    print(f"基準色 R{target[0]:.0f} G{target[1]:.0f} B{target[2]:.0f}"
          f"（{len(stats)}枚の中央値）\n")

    for n, v in stats.items():
        d = float(np.linalg.norm(v - target))
        if d <= TOL:
            print(f"  OK   {n:<26} 差 {d:4.1f}")
            continue
        print(f"  直す {n:<26} 差 {d:4.1f}  R{v[0]:.0f} G{v[1]:.0f} B{v[2]:.0f}")
        if not apply:
            continue
        p = IMG/f"{n}.jpg"
        im = Image.open(p).convert("RGB")
        a = np.asarray(im).astype(np.float32)
        m = mask_of(a.astype(np.int16))
        # マスクをぼかして、境目に段差が出ないようにする
        soft = np.asarray(Image.fromarray((m*255).astype(np.uint8))
                          .filter(ImageFilter.GaussianBlur(6))).astype(np.float32)/255.0
        off = (target - v).astype(np.float32)
        a += soft[..., None] * off[None, None, :]
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(
            p, quality=95, dpi=(300, 300))
        v2, _ = measure(p)
        print(f"       → R{v2[0]:.0f} G{v2[1]:.0f} B{v2[2]:.0f}"
              f"  差 {float(np.linalg.norm(v2-target)):.1f}")

if __name__ == "__main__":
    main(apply="--apply" in sys.argv)
