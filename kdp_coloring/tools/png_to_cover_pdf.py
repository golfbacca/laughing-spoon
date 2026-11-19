"""Canvaなどで作った表紙PNG（裏・背・表＋裁ち落としの1枚絵）を、KDP入稿用PDFにする。

使い方: python3 png_to_cover_pdf.py <表紙.png> <ページ数> <出力.pdf>
A4・白い紙の寸法で、PNGの画素数がぴったり合っているか（300dpi）を確かめてから、その大きさのPDFに貼る。
"""
import sys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

png, pages, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
W_in = 0.125 + 8.27 + pages * 0.002252 + 8.27 + 0.125
H_in = 11.69 + 0.25
im = Image.open(png).convert('RGB')
need = (round(W_in * 300), round(H_in * 300))
assert abs(im.width - need[0]) <= 1 and abs(im.height - need[1]) <= 1, ('画素数が合わない', im.size, need)
jpg = out + '.jpg'
im.save(jpg, quality=95, dpi=(300, 300))
pdfmetrics.registerFont(TTFont('Gothic', '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'))
c = canvas.Canvas(out, pagesize=(W_in * 72, H_in * 72), initialFontName='Gothic')
c.drawImage(jpg, 0, 0, W_in * 72, H_in * 72)
c.save()
import os; os.remove(jpg)
print(f'{W_in:.3f} x {H_in:.3f} in で書き出し（画素 {im.size}）')
