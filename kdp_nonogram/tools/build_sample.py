"""見本PDFを作る（8.5×11インチ・1ページ1問・末尾に解答）。
検査に通らない問題が1つでもあれば、PDFを作らずに止まる。"""
import sys, glob, os
sys.path.insert(0, os.path.dirname(__file__))
from nonogram import load, clues, check
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

ROOT = os.path.join(os.path.dirname(__file__), "..")
W, H = 8.5 * inch, 11 * inch
MARGIN = 0.45 * inch   # KDPの下限は外側0.25・内側0.375インチ（150ページまで）


def title_of(path):
    return open(path, encoding="utf-8").readline().lstrip("; ").strip()


def draw_puzzle(c, grid, no, solved=False, box=None):
    rows, cols = clues(grid)
    h, w = len(grid), len(grid[0])
    kr, kc = max(len(r) for r in rows), max(len(r) for r in cols)
    x0, y0, bw, bh = box
    cell = min(bw / (w + kr * 0.62), bh / (h + kc * 0.62))
    cw = cell * 0.62                      # 手がかり欄の1マス
    gx = x0 + (bw - (w * cell + kr * cw)) / 2 + kr * cw
    gy_top = y0 + bh - (bh - (h * cell + kc * cw)) / 2 - kc * cw
    fs = cell * 0.52

    def num(cx, by, v):
        # 2桁は欄からはみ出す。小さくすると読みにくい（本人指摘）ので、高さは1桁と同じまま横だけ詰める
        t = c.beginText()
        t.setFont("Helvetica-Bold", fs)
        hs = 68 if v >= 10 else 100
        t.setHorizScale(hs)
        t.setTextOrigin(cx - c.stringWidth(str(v), "Helvetica-Bold", fs) * hs / 200, by)
        t.textOut(str(v))
        c.drawText(t)

    for x, cl in enumerate(cols):         # 列の手がかり（下詰め）
        for i, v in enumerate(reversed(cl or [0])):  # 空の列は 0 と書く
            num(gx + x * cell + cell / 2, gy_top + i * cw + cw * 0.28, v)
    for y, rl in enumerate(rows):         # 行の手がかり（右詰め）
        for i, v in enumerate(reversed(rl or [0])):
            num(gx - i * cw - cw / 2 - cw * 0.08, gy_top - y * cell - cell / 2 - fs * 0.35, v)
    if solved:
        c.setFillGray(0.15)
        for y in range(h):
            for x in range(w):
                if grid[y][x]:
                    c.rect(gx + x * cell, gy_top - (y + 1) * cell, cell, cell, stroke=0, fill=1)
        c.setFillGray(0)
    for i in range(w + 1):
        c.setLineWidth(1.6 if i % 5 == 0 else 0.5)
        c.line(gx + i * cell, gy_top, gx + i * cell, gy_top - h * cell)
    for i in range(h + 1):
        c.setLineWidth(1.6 if i % 5 == 0 else 0.5)
        c.line(gx, gy_top - i * cell, gx + w * cell, gy_top - i * cell)
    return cell


def main(out, folder="puzzles"):
    files = sorted(glob.glob(os.path.join(ROOT, folder, "*.txt")))
    grids = [(f, load(f)) for f in files]
    bad = [os.path.basename(f) for f, g in grids if not check(g)["logic_only"]]
    if bad:
        sys.exit(f"検査に通らない問題があるので中止: {bad}")
    c = canvas.Canvas(out, pagesize=(W, H))
    sizes = []
    for n, (f, g) in enumerate(grids, 1):
        c.setFont("Helvetica-Bold", 22)
        c.drawString(MARGIN, H - MARGIN - 14, f"Puzzle {n}")
        c.setFont("Helvetica", 12)
        c.drawRightString(W - MARGIN, H - MARGIN - 12, f"{len(g[0])} x {len(g)}")
        cell = draw_puzzle(c, g, n, box=(MARGIN, MARGIN + 0.3 * inch, W - 2 * MARGIN, H - 2 * MARGIN - 0.8 * inch))
        sizes.append(cell / inch)
        c.setFont("Helvetica", 10)
        c.drawCentredString(W / 2, MARGIN - 6, str(n))
        c.showPage()
    # 解答：1ページに6問
    per, colsn = 6, 2
    bw, bh = (W - 2 * MARGIN) / colsn, (H - 2 * MARGIN - 0.5 * inch) / 3
    for i, (f, g) in enumerate(grids):
        k = i % per
        if k == 0:
            c.setFont("Helvetica-Bold", 22)
            c.drawString(MARGIN, H - MARGIN - 14, "Solutions")
        bx = MARGIN + (k % colsn) * bw
        by = H - MARGIN - 0.5 * inch - (k // colsn + 1) * bh
        draw_puzzle(c, g, i + 1, solved=True, box=(bx + 8, by + 22, bw - 16, bh - 30))
        c.setFont("Helvetica", 11)
        c.drawCentredString(bx + bw / 2, by + 8, f"{i + 1}. {title_of(f)}")
        if k == per - 1 or i == len(grids) - 1:
            c.showPage()
    c.save()
    print(f"{out}: {len(grids)}問  数字の高さ {min(sizes)*0.52*0.72*25.4:.1f}mm〜  マスの大きさ {min(sizes):.2f}〜{max(sizes):.2f} インチ（{min(sizes)*25.4:.1f}〜{max(sizes)*25.4:.1f} mm）")


if __name__ == "__main__":
    main(*sys.argv[1:3])
