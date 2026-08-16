# -*- coding: utf-8 -*-
"""SUZURIステッカー入稿用。生成画像の地を抜いて透過PNGにする。

生成AIが吐いた画像は「地＝薄いクリーム」「絵の外周＝ほぼ純白のダイカット風フチ」
という二層構造になっている。この2色は近いので、明度の閾値で切ると必ず失敗する。

  実測の例）地 #F0EFE9 は純白との距離が約31、フチは距離0〜6。
  charA 用の tools/cutout.py は TOL=26（純白基準）なので、この画像には効かない。
  純白基準でしきい値を31まで上げると、今度は白フチごと消える。

そこで基準を変える。純白ではなく「四隅から拾った実際の地の色」を基準にして、
そこから TOL 以内の画素だけを地と見なし、画像の外周から連結成分で塗り広げる。
地とフチの距離が31あるので、TOL=14 なら両者は絶対に混ざらない。
実行時に「地→純白の距離」を表示するので、余裕があるかは毎回目で見て確認すること。

使い方:
    python3 tools/suzuri_cutout.py 入力.png
    python3 tools/suzuri_cutout.py 入力.png -o 出力.png
    python3 tools/suzuri_cutout.py 入力.png --strip-border   # 白フチも剥がす
    python3 tools/suzuri_cutout.py 入力.png --strip-border --border 18
                                            # 剥がした上で18pxの白フチを引き直す
    python3 tools/suzuri_cutout.py 入力.png --square          # 正方形余白で囲む
"""
import argparse
import os
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

FEATHER = 0.8  # 縁のジャギをなじませる量。上げすぎると印刷時に輪郭が甘くなる


def _flood_from_edges(mask):
    """mask が True の画素のうち、画像の外周から4近傍で到達できるものだけ返す。
    絵の内側にある同色の閉じた領域（フチの内側の白など）を巻き込まないための処理。"""
    h, w = mask.shape
    hit = np.zeros((h, w), dtype=bool)
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if mask[y, x] and not hit[y, x]:
                hit[y, x] = True
                dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if mask[y, x] and not hit[y, x]:
                hit[y, x] = True
                dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not hit[ny, nx]:
                hit[ny, nx] = True
                dq.append((ny, nx))
    return hit


def _dilate(mask, r):
    """4近傍で r 回膨張させる。"""
    m = mask.copy()
    for _ in range(r):
        m[1:, :] |= m[:-1, :]
        m[:-1, :] |= m[1:, :]
        m[:, 1:] |= m[:, :-1]
        m[:, :-1] |= m[:, 1:]
    return m


def _existing_alpha(path, min_ratio=0.05):
    """すでに背景が透過されている画像なら、そのアルファを返す。そうでなければ None。

    生成AIやダウンロード経路によっては、最初から透過PNGで手に入ることがある。
    その場合に地の色を推定して切り直すと、透明画素のRGB（多くは0,0,0）を
    地の色と誤認して、絵を巻き込んで壊す。先に判定して素通しする。"""
    im = Image.open(path)
    if im.mode not in ("RGBA", "LA", "P"):
        return None
    im = im.convert("RGBA")
    al = np.asarray(im)[:, :, 3]
    if (al == 0).mean() < min_ratio:
        return None  # アルファはあるが実質不透明。切る対象として扱う
    return im, al


def cut(path, tol=14, strip_border=False, white_tol=30, border=0, square=False):
    im = Image.open(path).convert("RGB")
    # int16 だと (255-rgb)**2 の3チャンネル合計が最大195075で溢れて負になる。
    # 距離計算にしか使わないので int32 で持つ。
    rgb = np.asarray(im).astype(np.int32)
    h, w, _ = rgb.shape

    # 地の色は四隅16x16の中央値で決める。1点だけ拾うとノイズを掴む。
    k = max(4, min(h, w) // 64)
    corners = np.concatenate([
        rgb[:k, :k].reshape(-1, 3), rgb[:k, -k:].reshape(-1, 3),
        rgb[-k:, :k].reshape(-1, 3), rgb[-k:, -k:].reshape(-1, 3),
    ])
    bg_color = np.median(corners, axis=0)
    d_white = float(np.sqrt(((255 - bg_color) ** 2).sum()))
    print(f"  地の色      : RGB({int(bg_color[0])}, {int(bg_color[1])}, {int(bg_color[2])})")
    print(f"  地→純白距離 : {d_white:.1f}   （TOL={tol} との差が余裕。10以上あれば安全）")
    if d_white <= tol:
        print("  !! 地が純白に近すぎる。このまま切ると白フチごと消える。", file=sys.stderr)
        print("     --tol を下げるか、地の色を変えて生成し直すこと。", file=sys.stderr)

    dist_bg = np.sqrt(((rgb - bg_color) ** 2).sum(axis=2))
    bg = _flood_from_edges(dist_bg <= tol)

    if strip_border:
        # 地を抜いた結果あらわれた新しい外周から、今度は「純白に近い画素」を
        # 外側へ辿って落とす。ダイカット風の白フチだけが消え、絵は残る。
        dist_w = np.sqrt(((255 - rgb) ** 2).sum(axis=2))
        seed = _dilate(bg, 1) & (dist_w <= white_tol)
        near_white = (dist_w <= white_tol) | bg
        reach = _flood_from_edges(near_white & (_dilate(seed, 1) | near_white))
        bg = bg | (reach & (dist_w <= white_tol))

    alpha = np.where(bg, 0, 255).astype(np.uint8)

    if border > 0:
        # 不透明部分を膨張させて、その差分を白で塗る＝均一な白フチを引き直す
        opaque = alpha > 0
        grown = _dilate(opaque, border)
        ring = grown & ~opaque
        rgb = rgb.copy()
        rgb[ring] = [255, 255, 255]
        alpha = np.where(grown, 255, 0).astype(np.uint8)

    out = Image.fromarray(np.dstack([rgb.astype(np.uint8), alpha]), "RGBA")
    out.putalpha(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(FEATHER)))

    bb = out.getchannel("A").getbbox()
    if bb:
        out = out.crop(bb)

    if square:
        side = max(out.width, out.height)
        pad = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        pad.paste(out, ((side - out.width) // 2, (side - out.height) // 2), out)
        out = pad
    return out


def main():
    p = argparse.ArgumentParser(description="生成画像をSUZURI入稿用の透過PNGにする")
    p.add_argument("src")
    p.add_argument("-o", "--out", help="出力先。省略時は 元名_cut.png")
    p.add_argument("--tol", type=int, default=14, help="地と見なす色距離（既定14）")
    p.add_argument("--strip-border", action="store_true", help="白フチも剥がす")
    p.add_argument("--white-tol", type=int, default=30, help="白フチと見なす色距離（既定30）")
    p.add_argument("--border", type=int, default=0, help="この画素数で白フチを引き直す")
    p.add_argument("--square", action="store_true", help="透明余白で正方形に整える")
    p.add_argument("--pad", type=int, default=0, help="切り詰めたあと足す透明余白の画素数")
    p.add_argument("--scale", type=float, default=1.0, help="最後に拡大する倍率")
    a = p.parse_args()

    src = Image.open(a.src)
    print(f"入力: {a.src}  {src.width}x{src.height}  {src.mode}")
    out_path = a.out or os.path.splitext(a.src)[0] + "_cut.png"

    pre = _existing_alpha(a.src)
    if pre is not None:
        im, al = pre
        print(f"  すでに透過済み（透明 {(al == 0).mean() * 100:.1f}%）。地の切り抜きは行わない。")
        bb = im.getchannel("A").getbbox()
        if bb:
            im = im.crop(bb)
        if a.square:
            side = max(im.width, im.height)
            pad = Image.new("RGBA", (side, side), (0, 0, 0, 0))
            pad.paste(im, ((side - im.width) // 2, (side - im.height) // 2), im)
            im = pad
    else:
        im = cut(a.src, a.tol, a.strip_border, a.white_tol, a.border, a.square)

    if a.pad > 0:
        # 縁のアンチエイリアスが断ち切られないよう、透明の余白を少しだけ残す
        pad = Image.new("RGBA", (im.width + a.pad * 2, im.height + a.pad * 2), (0, 0, 0, 0))
        pad.paste(im, (a.pad, a.pad), im)
        im = pad

    if a.scale != 1.0:
        im = im.resize((round(im.width * a.scale), round(im.height * a.scale)), Image.LANCZOS)

    im.save(out_path)

    # 透明率は事故検知に使う。0%なら地が抜けていない＝失敗。
    ratio = float((np.asarray(im)[:, :, 3] == 0).mean()) * 100
    print(f"出力: {out_path}  {im.width}x{im.height}  透明部分 {ratio:.1f}%")
    if ratio < 1:
        print("  !! ほぼ抜けていない。--tol を上げて試すこと。", file=sys.stderr)
    print("\n  ※ 保存後、必ず画像を開いて「白フチが残っているか」「絵が欠けていないか」")
    print("     を目で確認してから入稿すること。数値だけでは判断できない。")


if __name__ == "__main__":
    main()
