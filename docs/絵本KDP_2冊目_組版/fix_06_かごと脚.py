#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""場面03の「棚の脚がかごの手前に描かれている」を画素で直す。

なぜ生成で直さないか（1冊目の原則）:
  かごの位置は生成でようやく合った。前後関係だけのために描き直すと、
  合った位置がまた転ぶ。前後関係は「脚を消して編み目で埋める」だけなので、
  画素で処理するほうが確実で速い。

やり方:
  かごは左右対称に近い。脚はかごの左寄り（左端から約27%）にあるので、
  その鏡像の位置（右寄り）は編み目だけのきれいな面である。
  鏡の位置から縦の帯をそのまま写して、脚を隠す。
  対称位置どうしなので、縁の高さも底の高さも自動的にそろう。

  python3 fix_06_かごと脚.py
"""
import pathlib
import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
IMG  = ROOT/"docs"/"絵本KDP_2冊目_画像"/"04_場面03_おむつがいい.jpg"

# 画素を測って決めた値（原寸4096の座標）
BAND   = (380, 500)   # 脚とその輪郭を含む帯
AXIS   = 570          # かごの左右対称の軸
Y_FROM = 1980         # ここから下を探す
Y_TO   = 2900         # かごの底より少し下まで
FEATHER = 10          # 帯の左右をこの幅でなじませる
RIM_BITE = 16         # 縁より少し上からかごを被せる。
                      # 少ないと、脚の下端に細かいギザつきが残る

def basket_top(g, x):
    """その列で、かごの縁（濃い輪郭）が始まる y を返す。"""
    col = g[Y_FROM:Y_TO, x]
    for i in range(1, len(col)):
        if col[i-1] - col[i] > 25:        # 明るい床から濃い輪郭へ落ちる所
            return Y_FROM + i
    return Y_FROM

def main():
    im = Image.open(IMG).convert("RGB")
    a  = np.asarray(im).astype(np.float32)
    g  = a.mean(axis=2)
    out = a.copy()

    for x in range(BAND[0], BAND[1] + 1):
        xs = AXIS * 2 - x                 # 鏡の位置
        top = basket_top(g, xs)
        # 帯の端はなじませる。真ん中は完全に置き換える
        d = min(x - BAND[0], BAND[1] - x)
        w = 1.0 if d >= FEATHER else d / FEATHER
        out[top:Y_TO, x] = (1 - w) * out[top:Y_TO, x] + w * a[top:Y_TO, xs]

    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(
        IMG, quality=95, dpi=(300, 300))
    print(f"脚を隠した: x{BAND[0]}〜{BAND[1]} を x{AXIS*2-BAND[1]}〜{AXIS*2-BAND[0]} の鏡像で置換")



# ------------------------------------------------------------------
# 第2工程: 消しすぎた脚を描き戻す
#
# 【やらかし】basket_top() は y=1980 から下へ探して最初の濃い線を
# 「かごの縁」とみなしていたが、そこには先に【下段の棚板の前縁】がある。
# 棚板を縁と誤って、棚板〜かごの縁のあいだの脚まで消してしまった。
# 教訓: 「最初に見つかった線」を目的の物と決めつけない。
#       間に何が挟まっているかを先に数えること。
#
# 脚は塗りつぶしの縦帯なので、上の健全な部分を下へ写せば戻せる。
# ------------------------------------------------------------------
LEG    = (380, 492)    # 脚の輪郭を含む左右。
                       # 【やらかし3】最初 (396,484) にしたら輪郭を欠いて
                       # 脚が細く薄く見えた。実測で左輪郭383-394・
                       # 右輪郭480-487。輪郭は必ず帯の内側に入れる
SRC_Y  = (1900, 2000)  # 健全に残っている脚の縦区間
GAP_TOP = 2020         # ここから下が消えている

def rim_top(g, x):
    """かごの縁（本物）を、棚板より下から探す。"""
    for y in range(2120, 2320):
        if g[y-1, x] - g[y, x] > 22:
            return y
    return 2200

def restore_leg():
    """消しすぎた脚を、上の脚を【上下に折り返して】写して描き戻す。

    ここに至るまでに3通り試して、最初の2つは失敗した。記録しておく。

      × 上の帯を下へ繰り返しコピー
          → 繰り返しの継ぎ目が横縞になって出た
      × 1行の断面を全行に引き伸ばす
          → 継ぎ目は消えたが、水彩の質感が失われて
            のっぺりした板になった。印刷に耐えない
      ○ 上の脚を y=GAP_TOP で折り返して写す
          → 折り返し点で画素が連続するので継ぎ目が原理的に出ない。
            水彩の滲みもそのまま持ってこられる

    下端は、列ごとに縁を探すとギザギザの櫛になるので、
    探した値を二次曲線で均してから使う。
    """
    im = Image.open(IMG).convert("RGB")
    a  = np.asarray(im).astype(np.float32)
    g  = a.mean(axis=2)
    out = a.copy()
    x0, x1 = LEG

    xs = np.arange(x0, x1 + 1)
    raw = np.array([rim_top(g, x) for x in xs], dtype=float)
    rim = np.polyval(np.polyfit(xs, raw, 2), xs)      # 櫛を均す

    for k, x in enumerate(xs):
        end = int(rim[k])
        d = min(x - x0, x1 - x)
        w = 1.0 if d >= 4 else d / 4
        for y in range(GAP_TOP, end):
            src = 2 * GAP_TOP - y                      # 折り返し
            if src < 1700:
                break
            out[y, x] = (1 - w) * out[y, x] + w * a[src, x]

    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(
        IMG, quality=95, dpi=(300, 300))
    print(f"脚を描き戻した（折り返し方式）: x{x0}〜{x1}, "
          f"y{GAP_TOP}〜{int(rim.min())}-{int(rim.max())}")




def cleanup():
    """縁から下に残った塗りの残骸を、かごの編み目で消す（仕上げ）。

    折り返しで脚を描き戻したあと、その下に前の試行の細い筋が残っていた。
    縁から下はかごなので、工程1と同じ鏡像でもう一度きれいにする。
    ついでに折り返し点の細い横線をぼかす。
    """
    im = Image.open(IMG).convert("RGB")
    a  = np.asarray(im).astype(np.float32)
    g  = a.mean(axis=2)
    out = a.copy()
    x0, x1 = LEG
    xs = np.arange(x0, x1 + 1)
    raw = np.array([rim_top(g, x) for x in xs], dtype=float)
    rim = np.polyval(np.polyfit(xs, raw, 2), xs)

    for k, x in enumerate(xs):
        top = int(rim[k]) - RIM_BITE           # 縁の線から下はかご
        xsrc = AXIS * 2 - x
        d = min(x - x0, x1 - x)
        w = 1.0 if d >= FEATHER else d / FEATHER
        out[top:Y_TO, x] = (1 - w) * out[top:Y_TO, x] + w * a[top:Y_TO, xsrc]

    # 折り返し点の横線をならす
    band = out[GAP_TOP-4:GAP_TOP+5, x0:x1+1]
    out[GAP_TOP-4:GAP_TOP+5, x0:x1+1] = (
        band * 0.4 + np.roll(band, 1, axis=0) * 0.3 + np.roll(band, -1, axis=0) * 0.3)

    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(
        IMG, quality=95, dpi=(300, 300))
    print("縁から下を編み目で塗り直し、折り返し点をならした")


if __name__ == "__main__":
    main()
    restore_leg()
    cleanup()
