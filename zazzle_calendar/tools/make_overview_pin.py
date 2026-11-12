"""12か月を1枚にまとめた Pinterest ピン（1000x1500）。写真は upload/ の入稿用を縮小して並べるだけ。"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UP = os.path.join(ROOT, 'upload'); OUT = os.path.join(ROOT, 'pins')
FONTS = os.path.join(os.path.dirname(ROOT), 'garden_flag', 'tools', 'fonts')
SERIF = os.path.join(FONTS, 'PlayfairDisplay.ttf'); SANS = os.path.join(FONTS, 'Montserrat.ttf')
W, H = 1000, 1500
BG = (239, 234, 226); INK = (38, 36, 34); SUB = (110, 104, 96)
MONTHS = [('01_jan_persimmons_snow.jpg', 'JAN'), ('02_feb_ice_lanterns.jpg', 'FEB'), ('03_mar_camellia_steps.jpg', 'MAR'),
          ('04_apr_cherry_ikomaya.jpg', 'APR'), ('05_may_hanamomo.jpg', 'MAY'), ('06_jun_flooded_paddy.jpg', 'JUN'),
          ('07_jul_buckwheat.jpg', 'JUL'), ('08_aug_lanterns.jpg', 'AUG'), ('09_sep_sunset.jpg', 'SEP'),
          ('10_oct_terashita_autumn.jpg', 'OCT'), ('11_nov_persimmons_mist.jpg', 'NOV'), ('12_dec_snow_steps.jpg', 'DEC')]


def sans(size, w='SemiBold'):
    f = ImageFont.truetype(SANS, size); f.set_variation_by_name(w); return f


def spaced(d, cx, y, text, f, fill, sp):
    ws = [d.textlength(c, font=f) for c in text]; x = cx - (sum(ws) + sp * (len(text) - 1)) / 2
    for c, w in zip(text, ws):
        d.text((x, y), c, font=f, fill=fill); x += w + sp


def main():
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    spaced(d, W / 2, 56, 'TSUMAGO  ·  KISO VALLEY  ·  JAPAN', sans(18, 'Medium'), SUB, 3)
    d.text((W / 2, 100), '12 Months in Tsumago', font=ImageFont.truetype(SERIF, 64), fill=INK, anchor='mt')
    spaced(d, W / 2, 190, '2027 PHOTO WALL CALENDAR', sans(20), SUB, 5)
    cols, rows, gap, mx = 3, 4, 14, 50
    top = 250; cw = (W - 2 * mx - gap * (cols - 1)) // cols; ch = round(cw * 8.5 / 11); lh = 34
    f_m = sans(18)
    for i, (fn, m) in enumerate(MONTHS):
        r, c = divmod(i, cols); x = mx + c * (cw + gap); y = top + r * (ch + lh + gap)
        p = Image.open(os.path.join(UP, fn)).convert('RGB').resize((cw, ch), Image.LANCZOS)
        im.paste(p, (x, y)); spaced(d, x + cw / 2, y + ch + 8, m, f_m, INK, 4)
    y_end = top + rows * (ch + lh + gap)
    d.text((W / 2, (y_end + H - 60) / 2 - 8), 'Every photo taken by my father in our hometown', font=ImageFont.truetype(SERIF, 34), fill=INK, anchor='mm')
    spaced(d, W / 2, H - 52, 'KISO VALLEY LIGHT', sans(20), INK, 5)
    out = os.path.join(OUT, 'pin_13_overview_12months.jpg'); im.save(out, quality=92); print(out, y_end)


if __name__ == '__main__':
    main()
