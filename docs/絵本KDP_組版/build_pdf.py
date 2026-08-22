#!/usr/bin/env python3
"""ペーパーバック本文PDF（8.5インチ角・塗り足し込み・全24ページ）。

  p1     中扉
  p2     とびら裏（余白）
  p3-20  本文18場面
  p21    トイレの じゅんばん（おさらい）
  p22    おうちのかたへ
  p23    つぎの おはなし
  p24    奥付

白紙で埋めず、24ページすべてに中身を入れてある。
"""
import pathlib, tempfile
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT  = pathlib.Path(__file__).resolve().parents[2]
PAGES = ROOT/"docs"/"絵本KDP_完成ページ"
FONTS = ROOT/"docs"/"絵本KDP_組版"/"fonts"
OUT   = ROOT/"docs"/"絵本KDP_入稿"; OUT.mkdir(exist_ok=True)

TRIM, BLEED = 8.5*inch, 0.125*inch
PAGE = TRIM + BLEED*2
INK, SOFT = (74/255,55/255,45/255), (110/255,90/255,78/255)
MIN_PAGES = 24
PRINT_PX  = 2625   # 8.75inch × 300dpi。これ以上は印刷に使われない
_TMP = pathlib.Path(tempfile.mkdtemp())

def fitted(name):
    """印刷に必要な画素数まで落とした一時ファイルを返す。"""
    src = PAGES/f"{name}.jpg"
    im = Image.open(src)
    if max(im.size) > PRINT_PX:
        im = im.resize((PRINT_PX, PRINT_PX), Image.LANCZOS)
    out = _TMP/f"{name}.jpg"
    im.save(out, quality=92, optimize=True, dpi=(300,300))
    return str(out)

BODY = ["S01_いえをでる","02_場面01_バス","03_場面02_公園であそぶ","S04_きづく",
        "04_場面03_もじもじ","05_場面04_言えない","06_場面05_いまいこう","07_場面06_言えた",
        "S09_トイレがみえる","08_場面07_知らないドア","09_場面08_ノック","10_場面09_トイレの中",
        "S13_ドアがあく","S14_レバー","11_場面10_おわりの音","12_場面11_手をあらう",
        "13_場面12_公園にもどる","S18_つぎのおでかけ"]

pdfmetrics.registerFont(TTFont("Maru",  str(FONTS/"ZenMaruGothic-Medium.ttf")))
pdfmetrics.registerFont(TTFont("MaruB", str(FONTS/"ZenMaruGothic-Bold.ttf")))

def text_page(c, blocks, top=0.30):
    """blocks: (テキスト, フォント, サイズ, 色, 行送り) の並び。中央そろえ。"""
    y = PAGE - PAGE*top
    for txt, fnt, size, col, gap in blocks:
        c.setFillColorRGB(*col); c.setFont(fnt, size)
        if txt:
            w = c.stringWidth(txt, fnt, size)
            c.drawString((PAGE-w)/2, y, txt)
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
    out = OUT/"本文_ペーパーバック_8.5inch角.pdf"
    c = canvas.Canvas(str(out), pagesize=(PAGE, PAGE))
    c.setTitle("トトンと おでかけトイレ")

    # p1 中扉
    text_page(c, [("トトンと おでかけトイレ","MaruB",34,INK,2.2),
                  ("","Maru",16,INK,1.4),
                  ("さく・え　はりま せいじ","Maru",16,SOFT,1.6)], top=0.42)
    # p2 とびら裏
    text_page(c, [("","Maru",16,INK,1.0)], top=0.5)

    # p3-20 本文
    for n in BODY:
        c.drawImage(fitted(n), 0, 0, width=PAGE, height=PAGE)
        c.showPage()

    # p21 おさらい
    left_page(c, [
        ("トイレの じゅんばん","MaruB",26,INK,2.4),
        ("① ドアを たたく　トン、トン","Maru",20,INK,2.0),
        ("② ドアを しめる","Maru",20,INK,2.0),
        ("③ パンツを おろす","Maru",20,INK,2.0),
        ("④ よいしょ と すわる","Maru",20,INK,2.0),
        ("⑤ あしが とどかない ときは だいに のせる","Maru",20,INK,2.0),
        ("⑥ ジャーッ　これは おわりの おと","Maru",20,INK,2.0),
        ("⑦ てを あらう","Maru",20,INK,2.6),
        ("いちばん さいしょは、","Maru",20,SOFT,1.9),
        ("「トイレ、いきたい」と いう こと。","Maru",20,SOFT,1.9),
    ], top=0.22)

    # p22 おうちのかたへ
    left_page(c, [
        ("おうちのかたへ","MaruB",24,INK,2.4),
        ("この絵本があつかうのは、「がまん」ではなく","Maru",16,INK,1.9),
        ("「言い出せない」というつまずきです。","Maru",16,INK,2.4),
        ("おうちのトイレはできるのに、おでかけ先だと","Maru",16,INK,1.9),
        ("言えない。その一点だけを扱っています。","Maru",16,INK,2.4),
        ("お話の中で、トイレが成功したかどうかは","Maru",16,INK,1.9),
        ("書いていません。解決は「できた」ではなく","Maru",16,INK,1.9),
        ("「言えた」に置いてあります。","Maru",16,INK,2.4),
        ("読んだあと、外出先で「トイレ、いきたい」と","Maru",16,SOFT,1.9),
        ("言えたときは、出た・出ないにかかわらず","Maru",16,SOFT,1.9),
        ("言えたことをほめてあげてください。","Maru",16,SOFT,1.9),
    ], top=0.20)

    # p23 つぎの おはなし
    left_page(c, [
        ("つぎの おはなし","MaruB",24,INK,2.6),
        ("トトンと はじめての パンツ","Maru",20,INK,2.0),
        ("　おむつから パンツに かわる ひ の おはなし","Maru",15,SOFT,2.6),
        ("トトンと てを あらう","Maru",20,INK,2.0),
        ("　あわあわの じゅんばん の おはなし","Maru",15,SOFT,2.6),
        ("トトンと よるの トイレ","Maru",20,INK,2.0),
        ("　よなかに おきた ひ の おはなし","Maru",15,SOFT,2.0),
    ], top=0.24)

    # p24 奥付
    left_page(c, [
        ("トトンと おでかけトイレ","MaruB",22,INK,2.4),
        ("2さい 3さい 4さいの「いま いきたい」が","Maru",14,SOFT,1.8),
        ("いえるように なる えほん","Maru",14,SOFT,2.8),
        ("さく・え　はりま せいじ","Maru",16,INK,2.8),
        ("本書のイラストは生成AIを使用して制作しています。","Maru",13,SOFT,2.0),
    ], top=0.26)

    c.save()
    n = 2 + len(BODY) + 4
    print(f"PDF: {out}")
    print(f"  ページサイズ {PAGE/inch:.3f} x {PAGE/inch:.3f} inch（塗り足し込み）")
    print(f"  仕上がり     {TRIM/inch:.2f} inch角")
    print(f"  構成: 中扉1 ＋ とびら裏1 ＋ 本文{len(BODY)} ＋ 巻末4 = {n}ページ")
    print(f"  白紙: なし（最低{MIN_PAGES}ページを中身で満たした）")

if __name__ == "__main__":
    main()
