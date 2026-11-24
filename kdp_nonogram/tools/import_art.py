"""ドット絵の画像（本人がGeminiなどで作ったもの）を、指定のマス数のノノグラムに落とす。
「黒と判定する基準」と「線を太らせる向き」を総当たりし、論理だけで解ける中で、もとの絵に一番近いものを選ぶ。
使い方: python3 tools/import_art.py 画像 マス数 出力.txt "題"
画像は本人の作ったもの・本人が直したものだけに使う（他人の画像をなぞらない）。"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from from_image import grid_from
from repair import stuck, repair


def dilate(g, dirs):
    h, w = len(g), len(g[0]); o = [r[:] for r in g]
    for y in range(h):
        for x in range(w):
            if g[y][x]:
                for dy, dx in dirs:
                    if 0 <= y + dy < h and 0 <= x + dx < w:
                        o[y + dy][x + dx] = True
    return o


def convert(path, n):
    """戻り値: (絵, 説明) の候補。決まらないマス0のもの"""
    found = []
    for th in (0.5, 0.4, 0.3, 0.2, 0.15):
        base = grid_from(path, n=n, th=th, dark=110)
        for name, dirs in (("そのまま", []), ("右へ太らせる", [(0, 1)]), ("下へ太らせる", [(1, 0)])):
            g = dilate(base, dirs) if dirs else base
            s = stuck(g)
            fill = sum(map(sum, g)) / (n * n)
            if s == 0:
                found.append((fill, g, f"基準{int(th*100)}%・{name}"))
            elif s <= 12:                          # あと少しなら黒を足して直す
                g2, log, left = repair(g, 4, symmetric=False)
                if left == 0:
                    found.append((sum(map(sum, g2)) / (n * n), g2, f"基準{int(th*100)}%・{name}・黒を{len(log)}マス足す"))
        if found:
            break                                  # 基準が高い（線が細い＝もとの絵に近い）ほうを優先
    found.sort(key=lambda t: t[0])                 # 同じ基準の中では黒が少ないもの
    return found


if __name__ == "__main__":
    path, n, out, title = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    res = convert(path, n)
    if not res:
        sys.exit(f"{n}×{n}では論理だけで解ける形にできなかった")
    fill, g, how = res[0]
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"; {title}\n; import_art.py で作成（{how}）\n" + "\n".join("".join("#" if c else "." for c in r) for r in g) + "\n")
    print(f"{out}: {how}  黒の割合 {fill:.0%}")
