"""追加ピン2種（1000x1500）。写真は upload/ の入稿用を縮小・配置するだけ（AI不使用）。
  pin_14_wall_mockup.jpg : 壁に掛けたカレンダーのイメージ（壁・釘・影は図形で描画）
  pin_15_gift.jpg        : 「A Gift for Japan Lovers」
"""
import calendar, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UP = os.path.join(ROOT, 'upload'); OUT = os.path.join(ROOT, 'pins')
FONTS = os.path.join(os.path.dirname(ROOT), 'garden_flag', 'tools', 'fonts')
SERIF = os.path.join(FONTS, 'PlayfairDisplay.ttf'); SANS = os.path.join(FONTS, 'Montserrat.ttf')
W, H = 1000, 1500
INK = (38, 36, 34); SUB = (110, 104, 96); LINE = (214, 208, 200)


def sans(size, w='SemiBold'):
    f = ImageFont.truetype(SANS, size); f.set_variation_by_name(w); return f


def serif(size):
    return ImageFont.truetype(SERIF, size)


def spaced(d, cx, y, text, f, fill, sp):
    ws = [d.textlength(c, font=f) for c in text]; x = cx - (sum(ws) + sp * (len(text) - 1)) / 2
    for c, w in zip(text, ws):
        d.text((x, y), c, font=f, fill=fill); x += w + sp


def photo(fn, w, h):
    p = Image.open(os.path.join(UP, fn)).convert('RGB'); r = w / h
    if p.width / p.height > r:
        nw = int(p.height * r); x = (p.width - nw) // 2; p = p.crop((x, 0, x + nw, p.height))
    else:
        nh = int(p.width / r); y = (p.height - nh) // 2; p = p.crop((0, y, p.width, y + nh))
    return p.resize((w, h), Image.LANCZOS)


def calendar_page(fn, month, cw):
    """Two Page 形式（上：写真 11x8.5、下：升目 11x8.5）を幅 cw で描く。"""
    ph = round(cw * 8.5 / 11); ch = ph * 2 + 6
    cal = Image.new('RGB', (cw, ch), (252, 251, 248)); d = ImageDraw.Draw(cal)
    cal.paste(photo(fn, cw, ph), (0, 0))
    d.line((0, ph + 3, cw, ph + 3), fill=(205, 200, 192), width=2)
    x0 = int(cw * 0.06); gw = cw - 2 * x0; y0 = ph + 6 + int(ph * 0.08)
    d.text((x0, y0), f'{calendar.month_name[month]}  •  2027', font=serif(int(cw * 0.045)), fill=INK)
    y = y0 + int(cw * 0.085); colw = gw / 7
    for i, wd in enumerate(['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']):
        d.text((x0 + colw * i + colw / 2, y), wd, font=sans(int(cw * 0.018)), fill=SUB, anchor='mt')
    y += int(cw * 0.04); d.line((x0, y, x0 + gw, y), fill=LINE, width=1)
    weeks = calendar.Calendar(firstweekday=6).monthdayscalendar(2027, month)
    rh = (ch - y - int(ph * 0.08)) / len(weeks)
    for r, wk in enumerate(weeks):
        for c, day in enumerate(wk):
            if day:
                d.text((x0 + colw * c + colw - 6, y + r * rh + 6), str(day), font=sans(int(cw * 0.022), 'Medium'), fill=INK, anchor='ra')
        d.line((x0, y + (r + 1) * rh, x0 + gw, y + (r + 1) * rh), fill=(232, 228, 222), width=1)
    # wire binding at top and middle
    for yy in (0, ph + 3):
        for x in range(10, cw - 10, 14):
            d.rounded_rectangle((x, yy - 8, x + 6, yy + 10), radius=3, outline=(120, 120, 120), width=2)
    return cal


def wall_mockup():
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):  # warm plaster wall with soft light from the upper left
        t = y / H; c = (int(236 - 18 * t), int(229 - 18 * t), int(217 - 18 * t)); d.line((0, y, W, y), fill=c)
    light = Image.new('L', (W, H), 0); ImageDraw.Draw(light).ellipse((-400, -500, 900, 700), fill=70)
    light = light.filter(ImageFilter.GaussianBlur(160))
    im = Image.composite(Image.new('RGB', (W, H), (250, 246, 238)), im, light); d = ImageDraw.Draw(im)
    sy = 1140
    # calendar
    cw = 600; cal = calendar_page('01_jan_persimmons_snow.jpg', 1, cw)
    cx = (W - cw) // 2; cy = 140
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).rectangle((cx + 14, cy + 22, cx + cw + 14, cy + cal.height + 22), fill=110)
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    im = Image.composite(Image.new('RGB', (W, H), (120, 110, 98)), im, sh)
    im.paste(cal, (cx, cy)); d = ImageDraw.Draw(im)
    # hanger + nail
    nx = W // 2
    d.line((cx + 60, cy - 6, nx, cy - 70), fill=(90, 90, 90), width=3); d.line((cx + cw - 60, cy - 6, nx, cy - 70), fill=(90, 90, 90), width=3)
    d.ellipse((nx - 7, cy - 78, nx + 7, cy - 64), fill=(70, 66, 60))
    # caption
    d.line((W / 2 - 90, sy + 40, W / 2 + 90, sy + 40), fill=(170, 160, 146), width=2)
    d.text((W / 2, sy + 70), 'Tsumago, Japan  ·  2027  Wall Calendar', font=serif(40), fill=INK, anchor='mt')
    d.text((W / 2, sy + 130), 'Every photo taken by my father in our hometown', font=sans(22, 'Medium'), fill=SUB, anchor='mt')
    spaced(d, W / 2, H - 52, 'KISO VALLEY LIGHT', sans(20), INK, 5)
    im.save(os.path.join(OUT, 'pin_14_wall_mockup.jpg'), quality=92)


def gift():
    BG = (31, 42, 58); CREAM = (245, 238, 226); GOLD = (232, 176, 92)
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    im.paste(photo('08_aug_lanterns.jpg', W, 760), (0, 0))
    fade = Image.new('L', (W, 760), 0); fd = ImageDraw.Draw(fade)
    for y in range(480, 760):
        fd.line((0, y, W, y), fill=int(255 * (y - 480) / 280))
    im.paste(Image.new('RGB', (W, 760), BG), (0, 0), fade); d = ImageDraw.Draw(im)
    spaced(d, W / 2, 790, 'THE PERFECT', sans(26), GOLD, 8)
    d.text((W / 2, 830), 'Gift for', font=serif(96), fill=CREAM, anchor='mt')
    d.text((W / 2, 945), 'Japan Lovers', font=serif(110), fill=CREAM, anchor='mt')
    d.line((W / 2 - 120, 1095, W / 2 + 120, 1095), fill=GOLD, width=3)
    d.text((W / 2, 1120), '2027 Photo Wall Calendar  ·  Tsumago, Kiso Valley', font=sans(24, 'Medium'), fill=CREAM, anchor='mt')
    strip = ['01_jan_persimmons_snow.jpg', '04_apr_cherry_ikomaya.jpg', '07_jul_buckwheat.jpg', '12_dec_snow_steps.jpg']
    gap = 12; sw = (W - 100 - gap * 3) // 4; shh = round(sw * 8.5 / 11)
    for i, fn in enumerate(strip):
        im.paste(photo(fn, sw, shh), (50 + i * (sw + gap), 1185))
    d.text((W / 2, 1185 + shh + 30), '12 photos taken by my father in our hometown', font=sans(22, 'Medium'), fill=(200, 196, 188), anchor='mt')
    spaced(d, W / 2, H - 52, 'KISO VALLEY LIGHT', sans(20), GOLD, 5)
    im.save(os.path.join(OUT, 'pin_15_gift.jpg'), quality=92)


if __name__ == '__main__':
    wall_mockup(); gift(); print('ok')
