"""ノノグラムの手がかり計算と検査。

検査は2段階:
  1. line_solve  … 行・列ごとの論理だけで最後まで解けるか（＝当てずっぽう不要）
  2. count_solutions … 解の個数を数える（上限2）。1なら一意
本に載せる条件は「1が成功」。1が成功すれば解は必ず1つ。
"""
from functools import lru_cache


def load(path):
    rows = [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip() and not l.startswith(";")]
    w = len(rows[0])
    assert all(len(r) == w for r in rows), f"{path}: 行の長さが不揃い {[len(r) for r in rows]}"
    assert all(set(r) <= set("#.") for r in rows), f"{path}: # と . 以外の文字"
    return [[c == "#" for c in r] for r in rows]


def line_clue(cells):
    out, run = [], 0
    for c in cells:
        if c:
            run += 1
        elif run:
            out.append(run); run = 0
    if run:
        out.append(run)
    return out


def clues(grid):
    rows = [line_clue(r) for r in grid]
    cols = [line_clue([r[x] for r in grid]) for x in range(len(grid[0]))]
    return rows, cols


def _line_possible(clue, known):
    """known: 1=黒, 0=白, None=未定。各マスが黒になれるか・白になれるかを返す。"""
    n, k = len(known), len(clue)

    @lru_cache(maxsize=None)
    def fits(pos, ci):
        # pos 以降に clue[ci:] を置けるか
        if ci == k:
            return all(known[i] != 1 for i in range(pos, n))
        if pos >= n:
            return False
        ok = False
        if known[pos] != 1 and fits(pos + 1, ci):
            ok = True
        L = clue[ci]
        if (pos + L <= n and all(known[i] != 0 for i in range(pos, pos + L))
                and (pos + L == n or known[pos + L] != 1)):
            if fits(min(pos + L + 1, n), ci + 1):
                ok = True
        return ok

    can_b, can_w = [False] * n, [False] * n

    @lru_cache(maxsize=None)
    def mark(pos, ci):
        if not fits(pos, ci):
            return
        if ci == k:
            for i in range(pos, n):
                can_w[i] = True
            return
        if known[pos] != 1 and fits(pos + 1, ci):
            can_w[pos] = True
            mark(pos + 1, ci)
        L = clue[ci]
        if (pos + L <= n and all(known[i] != 0 for i in range(pos, pos + L))
                and (pos + L == n or known[pos + L] != 1)
                and fits(min(pos + L + 1, n), ci + 1)):
            for i in range(pos, pos + L):
                can_b[i] = True
            if pos + L < n:
                can_w[pos + L] = True
            mark(min(pos + L + 1, n), ci + 1)

    if not fits(0, 0):
        return None
    mark(0, 0)
    return can_b, can_w


def line_solve(rows, cols, board=None):
    """論理だけで詰める。戻り値 (board, 状態)。状態: 'solved' / 'stuck' / 'contradiction'"""
    h, w = len(rows), len(cols)
    b = [r[:] for r in board] if board else [[None] * w for _ in range(h)]
    changed = True
    while changed:
        changed = False
        for y in range(h):
            r = _line_possible(tuple(rows[y]), tuple(b[y]))
            if r is None:
                return b, "contradiction"
            for x in range(w):
                if b[y][x] is None and r[0][x] != r[1][x]:
                    b[y][x] = 1 if r[0][x] else 0; changed = True
        for x in range(w):
            r = _line_possible(tuple(cols[x]), tuple(b[y][x] for y in range(h)))
            if r is None:
                return b, "contradiction"
            for y in range(h):
                if b[y][x] is None and r[0][y] != r[1][y]:
                    b[y][x] = 1 if r[0][y] else 0; changed = True
    done = all(c is not None for r in b for c in r)
    return b, "solved" if done else "stuck"


def count_solutions(rows, cols, limit=2):
    def rec(board):
        b, st = line_solve(rows, cols, board)
        if st == "contradiction":
            return 0
        if st == "solved":
            return 1
        y, x = next((y, x) for y in range(len(rows)) for x in range(len(cols)) if b[y][x] is None)
        total = 0
        for v in (1, 0):
            nb = [r[:] for r in b]; nb[y][x] = v
            total += rec(nb)
            if total >= limit:
                break
        return total
    return rec(None)


def check(grid):
    rows, cols = clues(grid)
    b, st = line_solve(rows, cols)
    same = st == "solved" and all((b[y][x] == 1) == grid[y][x] for y in range(len(grid)) for x in range(len(grid[0])))
    n = 1 if same else count_solutions(rows, cols)
    unknown = sum(c is None for r in b for c in r)
    return {"logic_only": same, "solutions": n, "stuck_cells": unknown,
            "fill": sum(map(sum, grid)) / (len(grid) * len(grid[0])),
            "empty_lines": sum(not c for c in rows) + sum(not c for c in cols)}
