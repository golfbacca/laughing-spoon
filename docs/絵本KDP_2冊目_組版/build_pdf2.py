#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2冊目のペーパーバック本文PDF（8.5インチ角・塗り足し込み・全24ページ）。

  p1     中扉
  p2     とびら裏（余白）
  p3-20  本文18ページ
  p21    パンツの じゅんばん（おさらい）
  p22    おうちのかたへ
  p23    シリーズの ほん
  p24    奥付

1冊目の build_pdf.py と同じ構造。BODY と巻末の文言だけ差し替えてある。
白紙で埋めず、24ページすべてに中身を入れてある。
"""
import pathlib, tempfile
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT  = pathlib.Path(__file__).resolve().parents[2]
PAGES = ROOT/"docs"/"絵本KDP_2冊目_完成ページ"
FONTS = ROOT/"docs"/"絵本KDP_組版"/"fonts"
OUT   = ROOT/"docs"/"絵本KDP_2冊目_入稿"; OUT.mkdir(exist_ok=True)

TRIM, BLEED = 8.5*inch, 0.125*inch
PAGE = TRIM + BLEED*2
INK, SOFT = (74/255, 55/255, 45/255), (110/255, 90/255, 78/255)
MIN_PAGES = 24
PRINT_PX  = 2625
_TMP = pathlib.Path(tempfile.mkdtemp())

def fitted(name):
    im = Image.open(PAGES/f"{name}.jpg")
    if max(im.size) > PRINT_PX:
        im = im.resize((PRINT_PX, PRINT_PX), Image.LANCZOS)
    out = _TMP/f"{name}.jpg"
    im.save(out, quality=92, optimize=True, dpi=(300, 300))
    return str(out)

BODY = ["S01_あさ","02_場面01_ふくろ","03_場面02_あける","S04_ならべる",
        "04_場面03_おむつがいい","05_場面04_だきしめる","06_場面05_どれにする",
        "07_場面06_えらんだ","S09_すわる","08_場面07_おむつをぬぐ",
        "09_場面08_かたあし","S13_かべにて","10_場面09_もういっぽう",
        "11_場面10_ひっぱる","S14_みおろす","12_場面11_はけた",
        "13_場面12_おでかけ","S18_つぎのあさ"]

pdfmetrics.registerFont(TTFont("Maru",  str(FONTS/"ZenMaruGothic-Medium.ttf")))
pdfmetrics.registerFont(TTFont("MaruB", str(FONTS/"ZenMaruGothic-Bold.ttf")))

def text_page(c, blocks, top=0.30):
    y = PAGE - PAGE*top
    for txt, fnt, size, col, gap in blocks:
        c.setFillColorRGB(*col); c.setFont(fnt, size)
        if txt:
            c.drawString((PAGE - c.stringWidth(txt, fnt, size))/2, y, txt)
        y -= size*gap
    c.showPage()

def left_page(c, blocks, top=0.24, x=0.13):
    y = PAGE - PAGE*top
    for txt, fnt, size, col, gap in blocks:
        c.setFillColorRGB(*col); c.setFont(fnt, size)
        if txt: c.drawString(PAGE*x, y, txt)
        y -= size*gap
    c.showPage()

def main():
    out = OUT/"toton02-paperback-interior.pdf"   # 入稿物は英数字名
    c = canvas.Canvas(str(out), pagesize=(PAGE, PAGE))
    c.setTitle("トトンと はじめての パンツ")

    text_page(c, [("トトンと はじめての パンツ","MaruB",32,INK,2.2),
                  ("","Maru",16,INK,1.4),
                  ("さく・え　はりま せいじ","Maru",16,SOFT,1.6)], top=0.42)
    text_page(c, [("","Maru",16,INK,1.0)], top=0.5)

    for n in BODY:
        c.drawImage(fitted(n), 0, 0, width=PAGE, height=PAGE)
        c.showPage()

    # p21 おさらい
    left_page(c, [
        ("パンツの じゅんばん","MaruB",26,INK,2.4),
        ("① ふくろから だす","Maru",20,INK,2.0),
        ("② ゆかに ならべる","Maru",20,INK,2.0),
        ("③ どれに するか えらぶ","Maru",20,INK,2.0),
        ("④ ゆかに すわる","Maru",20,INK,2.0),
        ("⑤ おむつを ぬぐ","Maru",20,INK,2.0),
        ("⑥ かたほうの あしを いれる","Maru",20,INK,2.0),
        ("⑦ もういっぽうの あしを いれる","Maru",20,INK,2.0),
        ("⑧ きゅっと ひっぱりあげる","Maru",20,INK,2.6),
        ("いちばん さいしょは、","Maru",20,SOFT,1.9),
        ("じぶんで えらぶ こと。","Maru",20,SOFT,1.9),
    ], top=0.20)

    # p22 おうちのかたへ
    left_page(c, [
        ("おうちのかたへ","MaruB",24,INK,2.4),
        ("この絵本があつかうのは、「はけるかどうか」ではなく","Maru",16,INK,1.9),
        ("「おむつを手放したがらない」というつまずきです。","Maru",16,INK,2.4),
        ("パンツは買ってあるのに、いざその日になると","Maru",16,INK,1.9),
        ("「おむつがいい」と言う。その一点だけを扱っています。","Maru",16,INK,2.4),
        ("お話の中で、おむつが外れたかどうかは書いていません。","Maru",16,INK,1.9),
        ("解決は「もらさなかった」ではなく","Maru",16,INK,1.9),
        ("「じぶんで えらんで、じぶんで はけた」に置いてあります。","Maru",16,INK,2.4),
        ("はけるかどうかは体の育ちに左右されますが、","Maru",16,SOFT,1.9),
        ("どれにするかを決めることは、その日その場でできます。","Maru",16,SOFT,1.9),
        ("えらべたときは、そのことをほめてあげてください。","Maru",16,SOFT,1.9),
    ], top=0.19)

    # p23 シリーズの ほん
    left_page(c, [
        ("シリーズの ほん","MaruB",24,INK,2.6),
        ("トトンと おでかけトイレ","Maru",20,INK,2.0),
        ("　おでかけ さきで「いきたい」と いえる ひ の おはなし","Maru",15,SOFT,1.6),
        ("　（はつばいちゅう）","Maru",15,SOFT,2.8),
        ("つぎの おはなし","MaruB",20,INK,2.2),
        ("トトンと てを あらう","Maru",20,INK,2.0),
        ("　あわあわの じゅんばん の おはなし","Maru",15,SOFT,2.6),
        ("トトンと よるの トイレ","Maru",20,INK,2.0),
        ("　よなかに おきた ひ の おはなし","Maru",15,SOFT,2.0),
    ], top=0.22)

    # p24 奥付
    left_page(c, [
        ("トトンと はじめての パンツ","MaruB",22,INK,2.4),
        ("1さい 2さい 3さいの「じぶんで はく」が","Maru",14,SOFT,1.8),
        ("はじまる えほん","Maru",14,SOFT,2.8),
        ("さく・え　はりま せいじ","Maru",16,INK,2.8),
        ("本書のイラストは生成AIを使用して制作しています。","Maru",13,SOFT,2.0),
    ], top=0.26)

    c.save()
    n = 2 + len(BODY) + 4
    print(f"PDF: {out}")
    print(f"  ページサイズ {PAGE/inch:.3f} x {PAGE/inch:.3f} inch（塗り足し込み）")
    print(f"  仕上がり     {TRIM/inch:.2f} inch角")
    print(f"  構成: 中扉1 ＋ とびら裏1 ＋ 本文{len(BODY)} ＋ 巻末4 = {n}ページ")
    if n < MIN_PAGES:
        raise SystemExit(f"中止: {n}ページ。KDPの最低{MIN_PAGES}ページに足りない")
    print(f"  白紙: なし（最低{MIN_PAGES}ページを中身で満たした）")

if __name__ == "__main__":
    main()
