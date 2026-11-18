"""KDPペーパーバックの表紙（裏表紙＋背＋表紙の1枚）を作る。

使い方: python3 build_cover.py <cover.json> <出力PDF> [確認用PNG]

寸法（KDPの計算式）:
  背幅   = 本文ページ数 × 0.002252in（白い紙・白黒）
  全体幅 = 裁ち落とし0.125 + 判型幅 + 背幅 + 判型幅 + 0.125
  高さ   = 判型高さ + 0.125×2
  背の文字はKDPの規定で左右0.0625inの余白が要る。86ページだと背幅0.19inで、文字は約5ptまでしか入らないため入れない。
  バーコードはKDPが裏表紙の右下に自動で入れる（幅2in×高さ1.2in、端から0.25in）。そこは空けておく。
"""
import json, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reportlab.pdfgen import canvas

C = json.load(open(sys.argv[1], encoding='utf-8'))
out_pdf = sys.argv[2]
out_png = sys.argv[3] if len(sys.argv) > 3 else None
DPI = 300
TW, TH = C['trim_in']
BLEED = 0.125
spine = C['pages'] * 0.002252
W_in, H_in = BLEED + TW + spine + TW + BLEED, TH + 2 * BLEED
px = lambda v: round(v * DPI)
W, H = px(W_in), px(H_in)
MIN = '/usr/share/fonts/opentype/ipafont-mincho/ipam.ttf'
GOT = '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'
F = lambda path, pt: ImageFont.truetype(path, round(pt * DPI / 72))

bg = tuple(C['back_color'])
cv = Image.new('RGB', (W, H), bg)
d = ImageDraw.Draw(cv)
x_spine = px(BLEED + TW)
x_front = px(BLEED + TW + spine)

# --- 表紙：カラーの絵を裁ち落としまで敷く ---
art = Image.open(C['front_image']).convert('RGB')
# 絵に描き込まれた枠線（ぬりえ用の黒い枠）を検出して、その内側だけを使う。表紙に枠線が出ると裁ち落としでずれて目立つ
import numpy as np
g = np.asarray(art.convert('L')) < 110
cols = np.where(g.mean(0) > 0.6)[0]; rows = np.where(g.mean(1) > 0.6)[0]
if len(cols) >= 2 and len(rows) >= 2:
    k = 8
    art = art.crop((cols[cols < art.width // 2].max() + k, rows[rows < art.height // 2].max() + k,
                    cols[cols > art.width // 2].min() - k, rows[rows > art.height // 2].min() - k))
fw, fh = W - x_front, H
s = max(fw / art.width, fh / art.height)
art = art.resize((round(art.width * s), round(art.height * s)), Image.LANCZOS)
oy = round((art.height - fh) * C.get('front_crop_from_top', 0.5))
ox = (art.width - fw) // 2
cv.paste(art.crop((ox, oy, ox + fw, oy + fh)), (x_front, 0))

# 書名の帯（上）
band_top = px(BLEED + 0.55); band_h = px(2.15)
over = Image.new('RGBA', (fw, band_h), (255, 255, 255, 228))
cv.paste(over, (x_front, band_top), over)
cx = x_front + (px(BLEED) * 0 + px(TW) // 2) + 0  # 表紙の中心（裁ち落とし側は除く）
cx = x_front + px(TW) // 2
d.text((cx, band_top + px(0.62)), C['title'], font=F(MIN, 38), fill=(30, 30, 30), anchor='mm')
d.text((cx, band_top + px(1.38)), C['subtitle'], font=F(MIN, 15.5), fill=(70, 70, 70), anchor='mm')
tb = d.textbbox((cx, band_top + px(0.62)), C['title'], font=F(MIN, 38), anchor='mm')
assert tb[0] >= x_front + px(0.375) and tb[2] <= x_front + px(TW) - px(0.375), ('書名が安全範囲外', tb)
d.line((cx - px(2.6), band_top + px(1.02), cx + px(2.6), band_top + px(1.02)), fill=(150, 150, 150), width=3)

# 下絵の拡大（中身が細密な線画であることを見せる）
ins = C.get('inset')
if ins:
    la = Image.open(ins['image']).convert('L')
    l, t, r, b = ins['box']
    crop = la.crop((round(l * la.width), round(t * la.height), round(r * la.width), round(b * la.height)))
    D = px(ins['diameter_in'])
    crop = crop.resize((D, D), Image.LANCZOS).convert('RGB')
    mask = Image.new('L', (D, D), 0); ImageDraw.Draw(mask).ellipse((0, 0, D - 1, D - 1), fill=255)
    icx = x_front + px(TW) - px(0.55) - D // 2
    icy = H - px(BLEED) - px(1.55) - D // 2
    ring = px(0.06)
    ImageDraw.Draw(cv).ellipse((icx - D // 2 - ring, icy - D // 2 - ring, icx + D // 2 + ring, icy + D // 2 + ring), fill=(255, 255, 255))
    cv.paste(crop, (icx - D // 2, icy - D // 2), mask)
    lab = ins['label']
    tb = d.textbbox((0, 0), lab, font=F(GOT, 10.5))
    lw = tb[2] - tb[0] + px(0.24)
    d.rounded_rectangle((icx - lw // 2, icy + D // 2 + px(0.12), icx + lw // 2, icy + D // 2 + px(0.48)), radius=px(0.08), fill=(255, 255, 255))
    d.text((icx, icy + D // 2 + px(0.30)), lab, font=F(GOT, 10.5), fill=(50, 50, 50), anchor='mm')

# 著者名（左下）
au = C['author']
tb = d.textbbox((0, 0), au, font=F(MIN, 15))
aw = tb[2] - tb[0] + px(0.5)
ay = H - px(BLEED) - px(0.95)
d.rounded_rectangle((x_front + px(0.45), ay, x_front + px(0.45) + aw, ay + px(0.5)), radius=px(0.08), fill=(255, 255, 255))
d.text((x_front + px(0.45) + aw // 2, ay + px(0.25)), au, font=F(MIN, 15), fill=(40, 40, 40), anchor='mm')

# --- 裏表紙 ---
bx0 = px(BLEED + 0.6); bx1 = x_spine - px(0.6)
y = px(BLEED + 0.7)
d.text((bx0, y), C['back_heading'], font=F(MIN, 19), fill=(30, 30, 30)); y += px(0.55)


def wrap(text, font, width):
    lines, cur = [], ''
    for ch in text:
        if d.textlength(cur + ch, font=font) > width:
            if ch in '、。）」' and cur:
                lines.append(cur + ch); cur = ''; continue
            lines.append(cur); cur = ch
        else:
            cur += ch
    return lines + ([cur] if cur else [])

f_body = F(MIN, 11)
for p in C['back_text']:
    for ln in wrap(p, f_body, bx1 - bx0):
        d.text((bx0, y), ln, font=f_body, fill=(45, 45, 45)); y += px(0.24)
    y += px(0.1)
y += px(0.05)
f_pt = F(GOT, 10)
for p in C['back_points']:
    for i, ln in enumerate(wrap(p, f_pt, bx1 - bx0 - px(0.25))):
        d.text((bx0 + (0 if i == 0 else px(0.25)), y), ('・' if i == 0 else '') + ln, font=f_pt, fill=(60, 60, 60)); y += px(0.22)
y += px(0.25)

# 中身の見本（2行×3列）
thumbs = C['back_thumbs']
cols = 3; gap = px(0.18)
tw = (bx1 - bx0 - gap * (cols - 1)) // cols
th = round(tw * 297 / 210)
bar_top = H - px(BLEED) - px(0.25) - px(1.2) - px(0.15)   # バーコード領域の上端
rows = (len(thumbs) + cols - 1) // cols
avail = bar_top - y
if rows * th + (rows - 1) * gap > avail:
    th = (avail - (rows - 1) * gap) // rows; tw = round(th * 210 / 297)
x_start = bx0
for i, t in enumerate(thumbs):
    im = Image.open(t).convert('RGB').resize((tw, th), Image.LANCZOS)
    x = x_start + (i % cols) * (tw + gap); yy = y + (i // cols) * (th + gap)
    d.rectangle((x - 3, yy - 3, x + tw + 2, yy + th + 2), fill=(200, 200, 200))
    cv.paste(im, (x, yy))

cv.save(out_png or '/dev/null', format='PNG') if out_png else None
tmp = out_pdf + '.jpg'
cv.save(tmp, quality=95, dpi=(DPI, DPI))
c = canvas.Canvas(out_pdf, pagesize=(W_in * 72, H_in * 72))
c.drawImage(tmp, 0, 0, W_in * 72, H_in * 72)
c.save()
import os; os.remove(tmp)
print(f'全体 {W_in:.3f} x {H_in:.3f} in（{W}x{H}px）、背幅 {spine:.4f} in')
