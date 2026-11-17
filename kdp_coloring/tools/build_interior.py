"""KDP用の本文PDF（A4・白黒）を組む。

使い方: python3 build_interior.py <ページ画像フォルダ> <content.json> <出力PDF>

content.json:
{
 "title": "...", "subtitle": "...", "author": "...",
 "howto": ["段落", ...],
 "colophon": ["行", ...],
 "chapters": [{"name": "第1章 札幌", "intro": "...", "items": [{"no": 1, "title": "...", "text": "...", "image": "01_xxx"}]}]
}

ページ構成（左綴じ・横書き。奇数ページ＝右ページ）:
  1 扉（書名） / 2 この本の使い方 / 3 目次
  4 解説1（＋第1章の導入） / 5 ぬりえ1 / 6 解説2 / 7 ぬりえ2 ...
  ぬりえは必ず右ページ。裏（次の左ページ）は文字だけの解説なので、裏写りしても絵は汚れない。
  最後に 空白（ぬりえ40の裏）/ 試し塗り（右）/ 奥付（その裏）。
"""
import json, os, sys
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('Mincho', '/usr/share/fonts/opentype/ipafont-mincho/ipam.ttf'))
pdfmetrics.registerFont(TTFont('Gothic', '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'))
W, H = 210 * mm, 297 * mm
INK, GRAY = (0.1, 0.1, 0.1), (0.45, 0.45, 0.45)

pages_dir, content_path, out = sys.argv[1:4]
C = json.load(open(content_path, encoding='utf-8'))


def wrap(text, font, size, width):
    """日本語を1文字単位で折り返す（行頭禁則つき）。"""
    lines, cur = [], ''
    for ch in text:
        if ch == '\n':
            lines.append(cur); cur = ''; continue
        if pdfmetrics.stringWidth(cur + ch, font, size) > width:
            if ch in '、。，．）」』！？ー' and cur:
                cur += ch; lines.append(cur); cur = ''; continue
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def para(c, text, x, y, width, font='Mincho', size=11.5, lead=1.85, color=INK):
    c.setFont(font, size); c.setFillColorRGB(*color)
    for ln in wrap(text, font, size, width):
        c.drawString(x, y, ln); y -= size * lead
    return y


def as_jpeg(png):
    """PDFを軽くするため、グレースケールJPEG（品質92）に変換して埋め込む。PNGのままだと170MBになる。"""
    from PIL import Image
    jpg = os.path.splitext(png)[0] + '.jpg'
    if not os.path.exists(jpg) or os.path.getmtime(jpg) < os.path.getmtime(png):
        Image.open(png).convert('L').save(jpg, quality=92, dpi=(300, 300))
    return jpg


def folio(c, n):
    c.setFont('Gothic', 8.5); c.setFillColorRGB(*GRAY)
    c.drawCentredString(W / 2, 12 * mm, str(n))


items = [(ch, it) for ch in C['chapters'] for it in ch['items']]
c = canvas.Canvas(out, pagesize=(W, H))
c.setTitle(C['title']); c.setAuthor(C.get('author', ''))
page = 0


def newpage():
    global page
    if page:
        c.showPage()
    page += 1

# 1 扉
newpage()
c.setFillColorRGB(*INK); c.setFont('Mincho', 30)
c.drawCentredString(W / 2, H * 0.62, C['title'])
c.setFont('Mincho', 13); c.setFillColorRGB(*GRAY)
c.drawCentredString(W / 2, H * 0.62 - 16 * mm, C['subtitle'])
if C.get('author'):
    c.setFont('Gothic', 10); c.drawCentredString(W / 2, H * 0.18, C['author'])

# 2 この本の使い方
newpage()
c.setFont('Gothic', 15); c.setFillColorRGB(*INK)
c.drawString(25 * mm, H - 35 * mm, 'この本の使い方')
y = H - 50 * mm
for p in C['howto']:
    y = para(c, p, 25 * mm, y, W - 50 * mm) - 4 * mm
folio(c, page)

# 3 目次（2段組）
newpage()
c.setFont('Gothic', 15); c.setFillColorRGB(*INK)
c.drawString(20 * mm, H - 30 * mm, '目次')
first_art = 5  # 解説kは 2k+2、ぬりえkは 2k+3
col_w = (W - 50 * mm) / 2
x0s = [20 * mm, 20 * mm + col_w + 10 * mm]
col, y = 0, H - 45 * mm
for ch in C['chapters']:
    need = (len(ch['items']) + 1) * 6.2 * mm + 3 * mm
    if y - need < 20 * mm and col == 0:
        col, y = 1, H - 45 * mm
    x = x0s[col]
    c.setFont('Gothic', 10); c.setFillColorRGB(*INK); c.drawString(x, y, ch['name']); y -= 6.2 * mm
    for it in ch['items']:
        c.setFont('Mincho', 9.5)
        c.drawString(x + 3 * mm, y, f"{it['no']:02d}  {it['title']}")
        c.drawRightString(x + col_w, y, str(2 * it['no'] + 3))
        y -= 6.2 * mm
    y -= 3 * mm
folio(c, page)

# 解説（左）とぬりえ（右）
for ch, it in items:
    newpage()  # 解説 = 偶数ページ
    y = H - 30 * mm
    if ch['items'][0] is it:
        c.setFont('Gothic', 13); c.setFillColorRGB(*INK); c.drawString(25 * mm, y, ch['name'])
        c.setLineWidth(0.4); c.setStrokeColorRGB(*GRAY); c.line(25 * mm, y - 3 * mm, W - 25 * mm, y - 3 * mm)
        y = para(c, ch['intro'], 25 * mm, y - 11 * mm, W - 50 * mm, size=10.5, color=GRAY) - 14 * mm
    else:
        c.setFont('Gothic', 9); c.setFillColorRGB(*GRAY); c.drawString(25 * mm, y, ch['name']); y -= 18 * mm
    c.setFont('Gothic', 34); c.setFillColorRGB(0.75, 0.75, 0.75); c.drawString(25 * mm, y, f"{it['no']:02d}")
    c.setFont('Mincho', 20); c.setFillColorRGB(*INK); c.drawString(25 * mm + 26 * mm, y + 1 * mm, it['title'])
    para(c, it['text'], 25 * mm, y - 16 * mm, W - 50 * mm)
    folio(c, page)
    newpage()  # ぬりえ = 奇数ページ（ページ番号は入れない）
    c.drawImage(as_jpeg(os.path.join(pages_dir, it['image'] + '.png')), 0, 0, W, H)

# 試し塗り：右ページに置く。左ページだとその紙の表がぬりえ40になり、試し塗りの色が絵に裏写りする
newpage()  # ぬりえ40の裏は空白
newpage()
c.setFont('Gothic', 15); c.setFillColorRGB(*INK); c.drawString(25 * mm, H - 35 * mm, '試し塗りのページ')
para(c, '色鉛筆やペンの色味、重ね塗りの具合を試してみましょう。', 25 * mm, H - 47 * mm, W - 50 * mm, size=10.5, color=GRAY)
c.setLineWidth(0.5); c.setStrokeColorRGB(0.6, 0.6, 0.6)
for r in range(8):
    for k in range(6):
        c.rect(25 * mm + k * 27 * mm, H - 75 * mm - r * 24 * mm, 22 * mm, 18 * mm)
folio(c, page)

# 奥付（試し塗りの裏＝偶数ページで終える）
newpage()
y = 70 * mm
c.setFont('Mincho', 12); c.setFillColorRGB(*INK); c.drawString(25 * mm, y + 20 * mm, C['title'])
c.setLineWidth(0.4); c.line(25 * mm, y + 16 * mm, W - 25 * mm, y + 16 * mm)
for ln in C['colophon']:
    c.setFont('Mincho', 9.5); c.drawString(25 * mm, y + 8 * mm, ln); y -= 6 * mm
c.save()
print('pages', page)
