#!/usr/bin/env python3
"""ペーパーバック本文PDFを作る（8.5インチ角・塗り足し込み・300dpi）。

ページ構成:
  1  中扉（タイトル）
  2  奥付・AI申告の記載
  3-14 本文12場面
  15-24 予備の白ページ（KDPの最低ページ数に合わせるための調整用）
※最低ページ数・判型はKDPの画面で必ず確認すること（このスクリプトの
  MIN_PAGES を実際の値に書き換える）。
"""
import pathlib
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT  = pathlib.Path(__file__).resolve().parents[2]
PAGES = ROOT/"docs"/"絵本KDP_完成ページ"
FONTS = ROOT/"docs"/"絵本KDP_組版"/"fonts"
OUT   = ROOT/"docs"/"絵本KDP_入稿"; OUT.mkdir(exist_ok=True)

TRIM   = 8.5 * inch          # 仕上がり 8.5インチ角
BLEED  = 0.125 * inch        # 塗り足し（各辺）
PAGE   = TRIM + BLEED*2      # 実際のページサイズ
MIN_PAGES = 24               # ★KDPの実際の最低ページ数に書き換える

BODY = ["02_場面01_バス","03_場面02_公園であそぶ","04_場面03_もじもじ",
        "05_場面04_言えない","06_場面05_いまいこう","07_場面06_言えた",
        "08_場面07_知らないドア","09_場面08_ノック","10_場面09_トイレの中",
        "11_場面10_おわりの音","12_場面11_手をあらう","13_場面12_公園にもどる"]

pdfmetrics.registerFont(TTFont("Maru",  str(FONTS/"ZenMaruGothic-Medium.ttf")))
pdfmetrics.registerFont(TTFont("MaruB", str(FONTS/"ZenMaruGothic-Bold.ttf")))

def text_page(c, lines, size=22, top=0.38, gap=1.9, font="Maru"):
    c.setFillColorRGB(74/255, 55/255, 45/255)
    c.setFont(font, size)
    y = PAGE - PAGE*top
    for ln in lines:
        w = c.stringWidth(ln, font, size)
        c.drawString((PAGE - w)/2, y, ln)
        y -= size*gap
    c.showPage()

def main():
    out = OUT/"本文_ペーパーバック_8.5inch角.pdf"
    c = canvas.Canvas(str(out), pagesize=(PAGE, PAGE))
    c.setTitle("トトンと おでかけトイレ")

    # 1 中扉
    text_page(c, ["トトンと おでかけトイレ"], size=34, top=0.42, font="MaruB")
    # 2 奥付
    text_page(c, [
        "トトンと おでかけトイレ",
        "",
        "2さい 3さい 4さいの",
        "「いま いきたい」が いえるように なる えほん",
        "",
        "さく ・ え  ＿＿＿＿",
        "",
        "この本のイラストは 生成AI を使って制作しました。",
    ], size=17, top=0.34, gap=2.0)

    # 3〜 本文
    for n in BODY:
        c.drawImage(str(PAGES/f"{n}.jpg"), 0, 0, width=PAGE, height=PAGE)
        c.showPage()

    # 最低ページ数に満たない分を白ページで埋める
    used = 2 + len(BODY)
    for _ in range(max(0, MIN_PAGES - used)):
        c.showPage()

    c.save()
    total = max(used, MIN_PAGES)
    print(f"PDF: {out}")
    print(f"  ページサイズ {PAGE/inch:.3f} x {PAGE/inch:.3f} inch（塗り足し込み）")
    print(f"  仕上がり     {TRIM/inch:.2f} x {TRIM/inch:.2f} inch")
    print(f"  本文 {len(BODY)}ページ ＋ 中扉・奥付2ページ = {used}ページ")
    print(f"  白ページで {total}ページに調整（MIN_PAGES={MIN_PAGES}）")

if __name__ == "__main__":
    main()
