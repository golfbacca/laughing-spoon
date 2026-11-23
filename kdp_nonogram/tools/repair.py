"""論理で解けない絵を、できるだけ少ないマスの変更で解ける絵にする。
1回に「あるマスと、その左右対称の位置のマス」を反転させ、決まらないマスが最も減る変更を選ぶ。これを繰り返す。
使い方: python3 tools/repair.py 絵.txt [最大回数]
結果は標準出力（変えたマスの一覧と、直した絵）。もとのファイルは書き換えない。"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from nonogram import load, clues, line_solve


def stuck(g):
    r, c = clues(g)
    b, st = line_solve(r, c)
    return sum(v is None for row in b for v in row)


def repair(g, max_steps=8, symmetric=True, add_only=True):
    # add_only：白→黒だけを許す。黒→白も許すと輪郭に穴が開いて絵が壊れた（下駄・風鈴・うちわで確認）
    g = [row[:] for row in g]
    h, w = len(g), len(g[0])
    log = []
    cur = stuck(g)
    for _ in range(max_steps):
        if cur == 0:
            break
        best = None
        for y in range(h):
            for x in range((w + 1) // 2 if symmetric else w):
                cells = {(y, x), (y, w - 1 - x)} if symmetric else {(y, x)}
                # 絵から離れた場所は変えない（上下左右どこかに黒がある白マス、または黒マスだけ）
                if add_only and any(g[yy][xx] for yy, xx in cells):
                    continue
                if not any(g[yy][xx] or any(0 <= yy + dy < h and 0 <= xx + dx < w and g[yy + dy][xx + dx]
                                            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))) for yy, xx in cells):
                    continue
                for yy, xx in cells:
                    g[yy][xx] = not g[yy][xx]
                s = stuck(g)
                for yy, xx in cells:
                    g[yy][xx] = not g[yy][xx]
                if best is None or s < best[0]:
                    best = (s, cells)
        if best is None or best[0] >= cur:
            break
        for yy, xx in best[1]:
            g[yy][xx] = not g[yy][xx]
        log.append((sorted(best[1]), "黒に" if g[next(iter(best[1]))[0]][next(iter(best[1]))[1]] else "白に", best[0]))
        cur = best[0]
    return g, log, cur


if __name__ == "__main__":
    g0 = load(sys.argv[1])
    g, log, left = repair(g0, int(sys.argv[2]) if len(sys.argv) > 2 else 8)
    for cells, what, s in log:
        print(f"  {cells} を{what} → 決まらないマス {s}")
    print("結果: 決まらないマス", left)
    print("\n".join("".join("#" if c else "." for c in row) for row in g))
