"""本人が一覧の画像に手を入れて送ってきた絵を読む。
画像のどこに絵があっても、薄い灰色の格子線を1本ずつ見つけ、線と線の中点を見て黒白を決める。
使い方: python3 tools/read_edited.py 画像 マス数 [出力.txt "題"]"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image


def _peaks(v, th):
    idx = [k for k in range(len(v)) if v[k] > th]
    out, cur = [], [idx[0]]
    for k in idx[1:]:
        if k - cur[-1] <= 2:
            cur.append(k)
        else:
            out.append(sum(cur) / len(cur)); cur = [k]
    out.append(sum(cur) / len(cur))
    return out


def _regular(p, n):
    """n+1 本の等間隔の線の並びを探す（題の文字などの余計な線を除く）"""
    best = None
    for i in range(len(p) - n):
        seg = p[i:i + n + 1]
        d = np.diff(seg)
        err = d.std() / d.mean()
        if best is None or err < best[0]:
            best = (err, seg)
    return best


def read(path, n):
    im = Image.open(path)
    bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im.convert("RGBA"))
    a = np.asarray(bg.convert("L")).astype(float)
    g = (a > 150) & (a < 236)
    cs, rs = g.sum(0), g.sum(1)
    ex, xs = _regular(_peaks(cs, cs.max() * 0.45), n)
    ey, ys = _regular(_peaks(rs, rs.max() * 0.45), n)
    cell = (xs[-1] - xs[0]) / n
    h = max(2, int(cell * 0.22))
    rows, amb = [], []
    for r in range(n):
        line = []
        for c in range(n):
            cx, cy = (xs[c] + xs[c + 1]) / 2, (ys[r] + ys[r + 1]) / 2
            m = a[int(cy - h):int(cy + h + 1), int(cx - h):int(cx + h + 1)].mean()
            if 70 < m < 185:
                amb.append((r, c, round(m)))
            line.append(m < 128)
        rows.append(line)
    return rows, amb, (round(cell, 1), round(ex, 3), round(ey, 3))


if __name__ == "__main__":
    from nonogram import check
    g, amb, info = read(sys.argv[1], int(sys.argv[2]))
    r = check(g)
    print("1マス(画素)・格子のばらつき", info, "あいまい", amb, "論理だけ", r["logic_only"], "解", r["solutions"], "残り", r["stuck_cells"])
    print("\n".join("".join("#" if c else "." for c in row) for row in g))
    if len(sys.argv) > 4:
        with open(sys.argv[3], "w", encoding="utf-8") as f:
            f.write(f"; {sys.argv[4]}\n" + "\n".join("".join("#" if c else "." for c in row) for row in g) + "\n")
