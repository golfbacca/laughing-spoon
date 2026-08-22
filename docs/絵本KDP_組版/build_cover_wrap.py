#!/usr/bin/env python3
"""ペーパーバックの表紙ラップ（裏＋背＋表を1枚）を組む。

  python3 build_cover_wrap.py [背幅インチ]
  既定値は SPINE_IN。KDPの表紙テンプレート画面に出る値を入れる。
"""
import sys, pathlib
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT  = pathlib.Path(__file__).resolve().parents[2]
PAGES = ROOT/"docs"/"絵本KDP_完成ページ"
FONTS = ROOT/"docs"/"絵本KDP_組版"/"fonts"
OUT   = ROOT/"docs"/"絵本KDP_入稿"; OUT.mkdir(exist_ok=True)

TRIM     = 8.5      # 仕上がり 8.5インチ角（KDPのカスタムサイズ）
BLEED    = 0.125    # 塗り足し（外周）
SPINE_IN = 0.056    # 24ページ／プレミアムカラー用紙のときの背幅
SPINE_TEXT_MIN = 0.25   # これ未満の背には文字を入れない

pdfmetrics.registerFont(TTFont("MaruB", str(FONTS/"ZenMaruGothic-Bold.ttf")))

def main():
    spine = float(sys.argv[1]) if len(sys.argv) > 1 else SPINE_IN
    W = TRIM*2 + spine + BLEED*2
    H = TRIM + BLEED*2
    out = OUT/f"表紙ラップ_8.5inch角_背{spine:.4f}in.pdf"
    c = canvas.Canvas(str(out), pagesize=(W*inch, H*inch))
    c.setTitle("トトンと おでかけトイレ 表紙")

    # 背の下地（先に全面を塗ってから絵を重ねる）
    c.setFillColorRGB(0.976, 0.949, 0.898)
    c.rect(0, 0, W*inch, H*inch, stroke=0, fill=1)

    panel = TRIM + BLEED     # 外側の1辺には塗り足しが付く
    # 裏表紙（左）：左端まで塗り足し
    c.drawImage(str(PAGES/"PB_裏表紙_正方形.jpg"), 0, 0,
                width=panel*inch, height=H*inch)
    # 表表紙（右）：右端まで塗り足し
    c.drawImage(str(PAGES/"PB_表表紙_正方形.jpg"),
                (BLEED + TRIM + spine)*inch, 0,
                width=panel*inch, height=H*inch)
    # 背
    c.setFillColorRGB(0.976, 0.949, 0.898)
    c.rect((BLEED + TRIM)*inch, 0, spine*inch, H*inch, stroke=0, fill=1)

    if spine >= SPINE_TEXT_MIN:
        c.setFillColorRGB(74/255, 55/255, 45/255)
        c.saveState()
        c.translate((BLEED + TRIM + spine/2)*inch, H*inch/2)
        c.rotate(-90)
        size = min(14, spine*inch*0.5)
        c.setFont("MaruB", size)
        c.drawCentredString(0, -size*0.35, "トトンと おでかけトイレ")
        c.restoreState()
        note = "背に書名を入れた"
    else:
        note = (f"背幅 {spine:.4f}in は細いため文字を入れていない"
                "（KDPは細い背への文字入れを認めない）")

    c.save()
    print(f"表紙ラップ: {out}")
    print(f"  全体   {W:.4f} x {H:.4f} inch")
    print(f"  内訳   裏 {TRIM} ＋ 背 {spine:.4f} ＋ 表 {TRIM} ＋ 塗り足し左右 {BLEED*2}")
    print(f"  高さ   仕上がり {TRIM} ＋ 塗り足し上下 {BLEED*2}")
    print(f"  {note}")

if __name__ == "__main__":
    main()
