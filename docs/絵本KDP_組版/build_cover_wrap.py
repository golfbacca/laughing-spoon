#!/usr/bin/env python3
"""ペーパーバックの表紙（裏＋背＋表の1枚）を組む。

背幅だけは本の実ページ数と用紙で決まり、KDPの画面でしか分からない。
KDPの「表紙テンプレート」ダウンロード画面に表示される背幅（インチ）を
下の SPINE_IN に入れてから実行すること。

  python3 build_cover_wrap.py 0.06
  （引数で背幅インチを渡すこともできる）
"""
import sys, pathlib
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

ROOT  = pathlib.Path(__file__).resolve().parents[2]
PAGES = ROOT/"docs"/"絵本KDP_完成ページ"
FONTS = ROOT/"docs"/"絵本KDP_組版"/"fonts"
OUT   = ROOT/"docs"/"絵本KDP_入稿"; OUT.mkdir(exist_ok=True)

TRIM     = 8.5      # 仕上がり 8.5インチ角
BLEED    = 0.125    # 塗り足し（外周3辺）
SPINE_IN = 0.0      # ★KDPの表紙テンプレート画面に出る背幅（インチ）
DPI      = 300

pdfmetrics.registerFont(TTFont("MaruB", str(FONTS/"ZenMaruGothic-Bold.ttf")))

def main():
    spine = float(sys.argv[1]) if len(sys.argv) > 1 else SPINE_IN
    if spine <= 0:
        print("背幅が未設定です。")
        print("KDPの表紙テンプレート画面に出る背幅（インチ）を引数で渡してください。")
        print("  例: python3 build_cover_wrap.py 0.0625")
        return

    W = TRIM*2 + spine + BLEED*2      # 裏 + 背 + 表 + 左右の塗り足し
    H = TRIM + BLEED*2
    out = OUT/f"表紙_ラップ_背{spine:.4f}in.pdf"
    c = canvas.Canvas(str(out), pagesize=(W*inch, H*inch))

    back  = str(PAGES/"14_裏表紙_2to3.jpg")
    front = str(PAGES/"01_表表紙_2to3.jpg")

    # 元画像は 2:3（縦長）。8.5インチ角のパネルに入れるため、
    # 中央基準で正方形に切り出してから配置する。
    def square(path, tag):
        im = Image.open(path); w, h = im.size
        s = min(w, h)
        im = im.crop(((w-s)//2, (h-s)//2, (w-s)//2+s, (h-s)//2+s))
        p = OUT/f"_tmp_{tag}.jpg"; im.save(p, quality=95)
        return str(p)

    panel = TRIM + BLEED                      # 外側は塗り足しぶん広い
    c.drawImage(square(back, "back"),   0, 0, width=panel*inch, height=H*inch)
    c.drawImage(square(front, "front"),
                (BLEED + TRIM + spine)*inch, 0, width=panel*inch, height=H*inch)

    # 背：明るい下地に縦書きふうの1行（背が細い場合は文字を省く）
    c.setFillColorRGB(0.98, 0.95, 0.90)
    c.rect((BLEED + TRIM)*inch, 0, spine*inch, H*inch, stroke=0, fill=1)
    if spine >= 0.20:
        c.setFillColorRGB(74/255, 55/255, 45/255)
        c.saveState()
        c.translate((BLEED + TRIM + spine/2)*inch, H*inch/2)
        c.rotate(-90)
        t = "トトンと おでかけトイレ"
        size = min(14, spine*inch*0.55)
        c.setFont("MaruB", size)
        c.drawCentredString(0, -size*0.35, t)
        c.restoreState()
    else:
        print("背幅が細いため、背の文字は入れませんでした（KDPは細い背への"
              "文字入れを認めないことがあります。画面の要件を確認してください）。")

    c.save()
    for tag in ("back", "front"):
        (OUT/f"_tmp_{tag}.jpg").unlink(missing_ok=True)
    print(f"表紙ラップ: {out}")
    print(f"  全体 {W:.4f} x {H:.4f} inch（背 {spine:.4f} inch・塗り足し込み）")

if __name__ == "__main__":
    main()
