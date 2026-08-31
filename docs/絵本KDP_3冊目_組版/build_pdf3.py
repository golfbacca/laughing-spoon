#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3冊目のペーパーバック本文PDF（8.5インチ角・塗り足し込み・全24ページ）。

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
PAGES = ROOT/"docs"/"絵本KDP_3冊目_完成ページ"
FONTS = ROOT/"docs"/"絵本KDP_組版"/"fonts"
OUT   = ROOT/"docs"/"絵本KDP_3冊目_入稿"; OUT.mkdir(exist_ok=True)

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

BODY = ["S01_ねるまえ","02_場面01_めがさめる","03_場面02_むずむず","S04_ふとんのふち",
        "04_場面03_でられない","05_場面04_ここにある","06_場面05_てをのばす",
        "07_場面06_ついた","S09_じぶんでつけられた","08_場面07_ふとんからでる",
        "09_場面08_ろうか","S13_トイレのドア","10_場面09_トイレのなか",
        "11_場面10_おわりのおと","S14_てをあらう","12_場面11_もどる",
        "13_場面12_またねる","S18_つぎのよる"]

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
    out = OUT/"toton03-paperback-interior.pdf"   # 入稿物は英数字名
    c = canvas.Canvas(str(out), pagesize=(PAGE, PAGE))
    c.setTitle("トトンと よるの トイレ")

    text_page(c, [("トトンと よるの トイレ","MaruB",34,INK,2.2),
                  ("","Maru",16,INK,1.4),
                  ("さく・え　はりま せいじ","Maru",16,SOFT,1.6)], top=0.42)
    text_page(c, [("","Maru",16,INK,1.0)], top=0.5)

    for n in BODY:
        c.drawImage(fitted(n), 0, 0, width=PAGE, height=PAGE)
        c.showPage()

    # p21 おさらい
    left_page(c, [
        ("よるの トイレの じゅんばん","MaruB",25,INK,2.4),
        ("① めが さめる","Maru",20,INK,2.0),
        ("② あかりを つける","Maru",20,INK,2.0),
        ("③ ふとんから でる","Maru",20,INK,2.0),
        ("④ トイレまで あるく","Maru",20,INK,2.0),
        ("⑤ ドアを しめる","Maru",20,INK,2.0),
        ("⑥ よいしょ と すわる","Maru",20,INK,2.0),
        ("⑦ てを あらう","Maru",20,INK,2.0),
        ("⑧ ふとんに もどる","Maru",20,INK,2.6),
        ("いちばん さいしょは、","Maru",20,SOFT,1.9),
        ("あかりを つける こと。","Maru",20,SOFT,1.9),
    ], top=0.20)

    # p22 おうちのかたへ
    left_page(c, [
        ("おうちのかたへ","MaruB",24,INK,2.4),
        ("この絵本があつかうのは、「夜のトイレに行けるか」ではなく","Maru",16,INK,1.9),
        ("「暗いから布団から出られない」というつまずきです。","Maru",16,INK,2.4),
        ("行かなきゃ、とわかっている。でも暗い。それだけで","Maru",16,INK,1.9),
        ("体は止まります。その一点だけを扱っています。","Maru",16,INK,2.4),
        ("お話の中で、間に合ったかどうかは書いていません。","Maru",16,INK,1.9),
        ("解決は「トイレに行けた」ではなく","Maru",16,INK,1.9),
        ("「じぶんで あかりを つけた」に置いてあります。","Maru",16,INK,2.4),
        ("ひとつだけ、家でできる準備があります。","Maru",16,SOFT,1.9),
        ("夜の明かりは、お子さんの手が届くところに置いてください。","Maru",16,SOFT,1.9),
        ("壁のスイッチは幼児の背では押せません。","Maru",16,SOFT,1.9),
        ("押せない明かりは、つけなさいと言ってもつけられません。","Maru",16,SOFT,1.9),
    ], top=0.19)

    # p23 シリーズの ほん
    left_page(c, [
        ("シリーズの ほん","MaruB",24,INK,2.6),
        ("トトンと おでかけトイレ","Maru",20,INK,2.0),
        ("　おでかけ さきで「いきたい」と いえる ひ の おはなし","Maru",15,SOFT,2.4),
        ("トトンと はじめての パンツ","Maru",20,INK,2.0),
        ("　おむつから パンツに かわる ひ の おはなし","Maru",15,SOFT,2.4),
        ("トトンと よるの トイレ","Maru",20,INK,2.0),
        ("　よなかに おきた ひ の おはなし（この ほん）","Maru",15,SOFT,2.4),
        ("つぎの おはなし","MaruB",20,INK,2.2),
        ("トトンと てを あらう","Maru",20,INK,2.0),
        ("　あわあわの じゅんばん の おはなし","Maru",15,SOFT,2.0),
    ], top=0.22)

    # p24 奥付
    left_page(c, [
        ("トトンと よるの トイレ","MaruB",22,INK,2.4),
        ("3さい 4さい 5さいの「じぶんで あかりを つける」が","Maru",13,SOFT,1.8),
        ("はじまる えほん","Maru",13,SOFT,2.8),
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
