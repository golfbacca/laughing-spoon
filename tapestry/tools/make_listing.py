#!/usr/bin/env python3
"""出品画像のうち、写真を使わない図版を作る（M01の4色ぶん）。

  3_art.jpg      … 絵の全体（平置き）
  5_sizes.jpg    … 4サイズを同じ縮尺で並べ、身長5'6"の人と比べる
  6_colors.jpg   … 4色の一覧（この出品の色に印）
  7_details.jpg  … 仕様（素材・縁・サイズ）

部屋の写真（1・2枚目）は Gemini で作った背景に貼り込む（docs/07）。
全画像 2000×1500（4:3）。Etsyの一覧は4:3で切り出すので最初から合わせる。
"""
import os
import cairosvg
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(ROOT, "..", "garden_flag", "tools", "fonts")
CW, CH = 2000, 1500
BG = (244, 240, 232)
INK = (43, 43, 43)
SUB = (110, 104, 96)

COLORS = [  # (キー, 英語名)
    ("dawn", "Dawn Pink"),
    ("dusk", "Desert Dusk"),
    ("night", "Moonlit Night"),
    ("sage", "Sage Forest"),
]
SIZES = [(26, 36), (50, 60), (68, 80), (88, 104)]
ART_ASPECT = 13650 / 16125


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def art(key, width):
    png = cairosvg.svg2png(url=os.path.join(ROOT, "source", f"M01_{key}.svg"), output_width=width)
    return Image.open(BytesIO(png)).convert("RGB")


def crop_to(img, aspect):
    """中央を残して、指定の縦横比に切る（Printifyの cover と同じ）。"""
    w, h = img.size
    if w / h > aspect:
        nw = round(h * aspect)
        x = (w - nw) // 2
        return img.crop((x, 0, x + nw, h))
    nh = round(w / aspect)
    y = (h - nh) // 2
    return img.crop((0, y, w, y + nh))


def shadow_paste(canvas, img, xy, blur=18, offset=(0, 10)):
    from PIL import ImageFilter
    sh = Image.new("RGBA", (img.width + blur * 4, img.height + blur * 4), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((blur * 2, blur * 2, blur * 2 + img.width, blur * 2 + img.height),
                                 fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.paste(sh, (xy[0] - blur * 2 + offset[0], xy[1] - blur * 2 + offset[1]), sh)
    canvas.paste(img, xy)


def centered(d, text, cx, y, f, fill):
    w = d.textlength(text, font=f)
    d.text((cx - w / 2, y), text, font=f, fill=fill)


def img_art(key):
    c = Image.new("RGB", (CW, CH), BG)
    h = 1300
    a = art(key, round(h * ART_ASPECT)).resize((round(h * ART_ASPECT), h), Image.LANCZOS)
    shadow_paste(c, a, ((CW - a.width) // 2, (CH - h) // 2))
    return c


def person(d, x, floor, px_per_in):
    """身長66インチ(5'6")の人の平塗りシルエット。x は足元の中心。"""
    s = px_per_in
    col = (150, 142, 132)
    head_r = 4.3 * s
    top = floor - 66 * s
    d.ellipse((x - head_r, top, x + head_r, top + 2 * head_r), fill=col)
    neck = top + 2 * head_r + 0.8 * s
    d.rounded_rectangle((x - 8 * s, neck, x + 8 * s, neck + 26 * s), radius=4 * s, fill=col)  # 胴
    d.rounded_rectangle((x - 7 * s, neck + 22 * s, x - 0.6 * s, floor), radius=2.5 * s, fill=col)  # 脚
    d.rounded_rectangle((x + 0.6 * s, neck + 22 * s, x + 7 * s, floor), radius=2.5 * s, fill=col)
    d.rounded_rectangle((x - 10.5 * s, neck + 1 * s, x - 7.2 * s, neck + 25 * s), radius=1.6 * s, fill=col)  # 腕
    d.rounded_rectangle((x + 7.2 * s, neck + 1 * s, x + 10.5 * s, neck + 25 * s), radius=1.6 * s, fill=col)


def img_sizes(key):
    c = Image.new("RGB", (CW, CH), BG)
    d = ImageDraw.Draw(c)
    centered(d, "Choose Your Size", CW / 2, 70, font("PlayfairDisplay.ttf", 92), INK)
    centered(d, "Shown to scale  ·  Portrait orientation", CW / 2, 190, font("Montserrat.ttf", 38), SUB)
    s = 6.4  # px / inch
    floor = 1240
    gap = 50
    base = art(key, 1600)
    total = sum(round(w * s) for w, _ in SIZES) + gap * len(SIZES) + 80
    x = (CW - total) // 2
    lab = font("Montserrat.ttf", 40)
    lab2 = font("Montserrat.ttf", 30)
    for w, h in SIZES:
        pw, ph = round(w * s), round(h * s)
        a = crop_to(base, w / h).resize((pw, ph), Image.LANCZOS)
        shadow_paste(c, a, (x, floor - ph), blur=10, offset=(0, 6))
        centered(d, f'{w}" × {h}"', x + pw / 2, floor + 28, lab, INK)
        centered(d, f"{round(w * 2.54)} × {round(h * 2.54)} cm", x + pw / 2, floor + 82, lab2, SUB)
        x += pw + gap
    px = x + 40
    person(d, px, floor, s)
    centered(d, "5'6\" person", px, floor + 28, lab2, SUB)
    assert px + 70 < CW - 40, px
    d.line((90, floor, CW - 90, floor), fill=(200, 192, 180), width=3)
    return c


def img_colors(key):
    c = Image.new("RGB", (CW, CH), BG)
    d = ImageDraw.Draw(c)
    centered(d, "Also Available In", CW / 2, 80, font("PlayfairDisplay.ttf", 88), INK)
    h = 520
    w = round(h * ART_ASPECT)
    gap = (CW - 4 * w) // 5
    assert gap >= 40, gap
    for i, (k, name) in enumerate(COLORS):
        x = gap + i * (w + gap)
        y = 470
        a = art(k, w).resize((w, h), Image.LANCZOS)
        if k == key:
            d.rounded_rectangle((x - 16, y - 16, x + w + 16, y + h + 16), radius=10, outline=INK, width=6)
        shadow_paste(c, a, (x, y), blur=10, offset=(0, 6))
        centered(d, name, x + w / 2, y + h + 46, font("Montserrat.ttf", 44), INK)
        if k == key:
            centered(d, "this listing", x + w / 2, y + h + 110, font("Montserrat.ttf", 32), SUB)
    return c


def img_details(key):
    c = Image.new("RGB", (CW, CH), BG)
    d = ImageDraw.Draw(c)
    h = 1220
    a = art(key, round(h * ART_ASPECT)).resize((round(h * ART_ASPECT), h), Image.LANCZOS)
    shadow_paste(c, a, (120, (CH - h) // 2))
    x = 120 + a.width + 130
    d.text((x, 200), "Details", font=font("PlayfairDisplay.ttf", 96), fill=INK)
    items = [
        ("Printed on 100% polyester", "Vivid dye-sublimation print"),
        ("Hemmed edges", "Clean finish on all four sides"),
        ("Lightweight", "Easy to hang, move, or fold"),
        ("4 portrait sizes", '26×36" up to 88×104"'),
        ("Made to order", "Printed just for you after you order"),
    ]
    y = 400
    for t, sub in items:
        d.ellipse((x, y + 22, x + 18, y + 40), fill=INK)
        d.text((x + 44, y), t, font=font("Montserrat.ttf", 48), fill=INK)
        d.text((x + 44, y + 64), sub, font=font("Montserrat.ttf", 34), fill=SUB)
        y += 170
    return c


def main():
    for key, _ in COLORS:
        out = os.path.join(ROOT, "listing", f"M01_{key}")
        os.makedirs(out, exist_ok=True)
        for name, fn in (("3_art", img_art), ("5_sizes", img_sizes),
                         ("6_colors", img_colors), ("7_details", img_details)):
            fn(key).save(os.path.join(out, f"{name}.jpg"), quality=92)
        print(out)


if __name__ == "__main__":
    main()
