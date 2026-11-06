"""Pinterest 用の縦長ピン画像（1000x1500, 2:3）を作る。
写真は zazzle_calendar/upload/ の入稿用（切り抜きのみ・無加工）を縮小して配置するだけ。
使い方: python3 make_pins.py
"""
import calendar, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UP = os.path.join(ROOT, 'upload')
OUT = os.path.join(ROOT, 'pins')
FONTS = os.path.join(os.path.dirname(ROOT), 'garden_flag', 'tools', 'fonts')
SERIF = os.path.join(FONTS, 'PlayfairDisplay.ttf')
SANS = os.path.join(FONTS, 'Montserrat.ttf')

W, H = 1000, 1500
BG = (239, 234, 226)
INK = (38, 36, 34)
SUB = (110, 104, 96)
LINE = (214, 208, 200)

PINS = [
    ('00_cover_snowfall.jpg', None, 'Four Seasons in Tsumago'),
    ('01_jan_persimmons_snow.jpg', 1, 'Persimmons in the Snow'),
    ('02_feb_ice_lanterns.jpg', 2, 'Ice Lanterns at Night'),
    ('03_mar_camellia_steps.jpg', 3, 'Fallen Camellias'),
    ('04_apr_cherry_ikomaya.jpg', 4, 'Cherry Blossoms on the Nakasendo'),
    ('05_may_hanamomo.jpg', 5, 'Hanamomo in Bloom'),
    ('06_jun_flooded_paddy.jpg', 6, 'Rice Paddies in Early Summer'),
    ('07_jul_buckwheat.jpg', 7, 'Buckwheat in Bloom'),
    ('08_aug_lanterns.jpg', 8, 'Lanterns After the Rain'),
    ('09_sep_sunset.jpg', 9, 'Autumn Sunset in Kiso'),
    ('10_oct_terashita_autumn.jpg', 10, 'A Misty Autumn Day'),
    ('11_nov_persimmons_mist.jpg', 11, 'Persimmons in the Mist'),
    ('12_dec_snow_steps.jpg', 12, 'Snow on the Old Road'),
]


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if path == SANS:
        f.set_variation_by_name(weight or 'Medium')
    return f


def spaced(d, xy, text, f, fill, spacing, anchor_center=True):
    widths = [d.textlength(c, font=f) for c in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = xy[0] - total / 2 if anchor_center else xy[0]
    for c, w in zip(text, widths):
        d.text((x, xy[1]), c, font=f, fill=fill)
        x += w + spacing


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def draw_grid(d, x0, y0, w, month):
    f_m = font(SERIF, 34); f_wd = font(SANS, 15, 'SemiBold'); f_n = font(SANS, 20, 'Medium')
    d.text((x0, y0), f'{calendar.month_name[month]}  2027', font=f_m, fill=INK)
    y = y0 + 62
    cw = w / 7
    for i, wd in enumerate(['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']):
        d.text((x0 + cw * i + cw / 2, y), wd, font=f_wd, fill=SUB, anchor='mt')
    y += 30
    d.line((x0, y, x0 + w, y), fill=LINE, width=2)
    weeks = calendar.Calendar(firstweekday=6).monthdayscalendar(2027, month)
    rh = 46
    for r, wk in enumerate(weeks):
        for c, day in enumerate(wk):
            if day:
                d.text((x0 + cw * c + cw / 2, y + 12 + r * rh), str(day), font=f_n, fill=INK, anchor='mt')
    return y + 12 + len(weeks) * rh


def make(fn, month, title):
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    spaced(d, (W / 2, 58), 'TSUMAGO  ·  KISO VALLEY  ·  JAPAN', font(SANS, 18), SUB, 3)
    cx0, cx1, cy0 = 70, 930, 112
    pw = cx1 - cx0 - 40
    photo = Image.open(os.path.join(UP, fn)).convert('RGB')
    ph = round(pw * photo.height / photo.width)
    photo = photo.resize((pw, ph), Image.LANCZOS)
    py = cy0 + 44
    if month:
        rows = len(calendar.Calendar(firstweekday=6).monthdayscalendar(2027, month))
        card_h = 44 + ph + 34 + 104 + rows * 46 + 40
    else:
        card_h = 44 + ph + 30 + 230
    # card + shadow
    d.rectangle((cx0 + 6, cy0 + 8, cx1 + 6, cy0 + card_h + 8), fill=(225, 219, 210))
    d.rectangle((cx0, cy0, cx1, cy0 + card_h), fill=(255, 255, 255))
    # wire binding
    for x in range(cx0 + 30, cx1 - 20, 26):
        d.rounded_rectangle((x, cy0 - 10, x + 10, cy0 + 16), radius=5, outline=(140, 140, 140), width=3)
    im.paste(photo, (cx0 + 20, py))
    if month:
        draw_grid(d, cx0 + 40, py + ph + 34, pw - 40, month)
    else:
        fy = py + ph + 50
        d.text((W / 2, fy), '2027', font=font(SERIF, 110), fill=INK, anchor='mt')
        spaced(d, (W / 2, fy + 140), 'WALL CALENDAR', font(SANS, 22), SUB, 6)
    # title + footer
    f_t = font(SERIF, 56)
    lines = wrap(d, title, f_t, 860)
    top, bottom = cy0 + card_h + 10, H - 110
    ty = (top + bottom) / 2 - (len(lines) * 68) / 2
    for i, line in enumerate(lines):
        d.text((W / 2, ty + i * 68), line, font=f_t, fill=INK, anchor='mt')
    d.text((W / 2, H - 92), '2027 Photo Calendar  ·  Photographed by my father', font=font(SANS, 22), fill=SUB, anchor='mt')
    spaced(d, (W / 2, H - 52), 'KISO VALLEY LIGHT', font(SANS, 20, 'SemiBold'), INK, 5)
    out = os.path.join(OUT, 'pin_' + fn.replace('.jpg', '.jpg'))
    im.save(out, quality=92)
    return out, ty


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for fn, m, t in PINS:
        print(make(fn, m, t))
