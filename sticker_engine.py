# -*- coding: utf-8 -*-
"""
LINEエモ文字スタンプ 生成エンジン

セット定義（gen_set1.py / gen_set2.py）から呼ばれる共通部分。
370x320px・背景透過PNG・全文字に白フチ（ダークモードのトーク背景対策）。
"""
import os
from PIL import Image, ImageDraw, ImageFont

NOTO = "/usr/share/fonts/opentype/noto/"
FONTS = {
    "black":  (NOTO + "NotoSansCJK-Black.ttc", 0),    # 極太＝DELA Gothic One 代替
    "sans_l": (NOTO + "NotoSansCJK-Light.ttc", 0),    # 細字＝Noto Sans JP Light 相当
    "min_l":  (NOTO + "NotoSerifCJK-Light.ttc", 0),   # 明朝＝しっぽり明朝 代替
    "min_r":  (NOTO + "NotoSerifCJK-Regular.ttc", 0),
    "min_m":  (NOTO + "NotoSerifCJK-Medium.ttc", 0),
    "maru":   ("/usr/share/fonts/truetype/motoya-mtlmr3m/MTLmr3m.ttf", 0),  # 丸ゴ＝手書き系代替
}
_cache = {}
def F(key, size):
    k = (key, size)
    if k not in _cache:
        path, idx = FONTS[key]
        _cache[k] = ImageFont.truetype(path, size, index=idx)
    return _cache[k]

SUMI  = (26, 26, 26, 255)     # 墨：基調
CHI   = (123, 30, 30, 255)    # 血：呪い・敵意
HAI   = (110, 110, 110, 255)  # 灰：無感情・麻痺
WHITE = (255, 255, 255, 255)

W, H = 370, 320
MARGIN = 12


def stroke_for(size):
    return max(3, min(6, round(size * 0.085)))


def _crop(img):
    bb = img.getbbox()
    return img.crop(bb) if bb else img


def render_run(runs, fkey, size, spacing=0, jitter=0, seedbase=0):
    """runs: [(text, color), ...] を1行に横並び描画。白フチ付き。"""
    font = F(fkey, size)
    sw = stroke_for(size)
    pad = size + sw * 3
    widths = []
    total = 0
    for text, _ in runs:
        for ch in text:
            w = font.getlength(ch)
            widths.append(w)
            total += w + spacing
    total = max(total - spacing, 1)
    canvas = Image.new("RGBA", (int(total) + pad * 2, int(size * 2.4) + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    x = pad
    i = 0
    for text, color in runs:
        for ch in text:
            if jitter:
                sub = Image.new("RGBA", (int(size * 2.6), int(size * 2.6)), (0, 0, 0, 0))
                ImageDraw.Draw(sub).text((size * 0.35, size * 0.35), ch, font=font, fill=color,
                                         stroke_width=sw, stroke_fill=WHITE)
                ang = ((seedbase * 7 + i * 13) % 9 - 4) * (jitter / 4.0)
                sub = sub.rotate(ang, resample=Image.BICUBIC)
                canvas.alpha_composite(sub, (int(x - size * 0.35), int(pad - size * 0.35)))
            else:
                d.text((x, pad), ch, font=font, fill=color, stroke_width=sw, stroke_fill=WHITE)
            x += widths[i] + spacing
            i += 1
    return _crop(canvas)


def render_vertical(text, fkey, size, color, line=1.02, col_gap=14):
    """text が list の場合は縦書き複数列。日本語の縦組みなので右→左の順に並べる。"""
    if isinstance(text, (list, tuple)):
        cols = [render_vertical(t, fkey, size, color, line) for t in text]
        w = sum(c.width for c in cols) + col_gap * (len(cols) - 1)
        h = max(c.height for c in cols)
        canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        x = w
        for c in cols:                      # 先頭の列を一番右へ
            x -= c.width
            canvas.alpha_composite(c, (x, 0))
            x -= col_gap
        return canvas

    font = F(fkey, size)
    sw = stroke_for(size)
    pad = size + sw * 3
    step = size * line
    canvas = Image.new("RGBA", (int(size * 2) + pad * 2, int(step * len(text)) + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    cx = canvas.width / 2
    for i, ch in enumerate(text):
        w = font.getlength(ch)
        d.text((cx - w / 2, pad + i * step), ch, font=font, fill=color,
               stroke_width=sw, stroke_fill=WHITE)
    return _crop(canvas)


def render_rule(width, thick, color):
    sw = 3
    img = Image.new("RGBA", (width + sw * 2, thick + sw * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width - 1, img.height - 1], fill=WHITE)
    d.rectangle([sw, sw, sw + width - 1, sw + thick - 1], fill=color)
    return img


def build(spec, size=(W, H), margin=None):
    cw, ch = size
    m = MARGIN if margin is None else margin
    safe_w, safe_h = cw - m * 2, ch - m * 2
    layers = []
    for b in spec["blocks"]:
        t = b.get("type", "text")
        if t == "vertical":
            img = render_vertical(b["text"], b["font"], b["size"], b.get("color", SUMI), b.get("line", 1.02))
        elif t == "rule":
            img = render_rule(b["width"], b.get("thick", 3), b.get("color", SUMI))
        else:
            runs = b["runs"] if "runs" in b else [(b["text"], b.get("color", SUMI))]
            img = render_run(runs, b["font"], b["size"], b.get("spacing", 0),
                             b.get("jitter", 0), b.get("seed", 0))
        if b.get("alpha", 1.0) < 1.0:
            a = img.getchannel("A").point(lambda v: int(v * b["alpha"]))
            img.putalpha(a)
        layers.append((img, b))

    gaps = [b.get("gap", 8) for _, b in layers[1:]]
    total_h = sum(im.height for im, _ in layers) + sum(gaps)
    max_w = max(im.width for im, _ in layers)

    # セーフエリアに収まらなければ全体を縮小
    scale = min(1.0, safe_w / max_w, safe_h / total_h)
    if scale < 1.0:
        layers = [(im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))),
                             Image.LANCZOS), b) for im, b in layers]
        gaps = [g * scale for g in gaps]
        total_h = sum(im.height for im, _ in layers) + sum(gaps)

    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    y = (ch - total_h) / 2 + spec.get("dy", 0)
    for i, (im, b) in enumerate(layers):
        if i:
            y += gaps[i - 1]
        align = b.get("align", "center")
        if align == "center":
            x = (cw - im.width) / 2
        elif align == "left":
            x = m + safe_w * 0.05
        else:
            x = cw - m - im.width - safe_w * 0.05
        x += b.get("dx", 0)
        canvas.alpha_composite(im, (int(round(x)), int(round(y))))
        y += im.height

    if spec.get("rotate"):
        canvas = canvas.rotate(spec["rotate"], resample=Image.BICUBIC, expand=False)
    return canvas


def _sheet(out, count, bg, fname):
    cols = 4
    rows = (count + cols - 1) // cols
    pad = 14
    img = Image.new("RGBA", (cols * W + pad * (cols + 1), rows * H + pad * (rows + 1)), bg)
    for i in range(count):
        st = Image.open(os.path.join(out, f"{i+1:02d}.png"))
        c, r = i % cols, i // cols
        img.alpha_composite(st, (pad + c * (W + pad), pad + r * (H + pad)))
    img.convert("RGB").save(os.path.join(out, fname), quality=95)


def render_set(out_dir, title, stickers, main, tab):
    """stickers: [(文言, spec), ...] を 01.png… に書き出し、メイン／タブ／確認シート／対応表も作る。"""
    os.makedirs(out_dir, exist_ok=True)
    for f in os.listdir(out_dir):
        os.remove(os.path.join(out_dir, f))

    for i, (label, spec) in enumerate(stickers, 1):
        build(spec).save(os.path.join(out_dir, f"{i:02d}.png"))

    build(main, size=(240, 240)).save(os.path.join(out_dir, "main_240x240.png"))
    build(tab, size=(96, 74), margin=5).save(os.path.join(out_dir, "tab_96x74.png"))

    _sheet(out_dir, len(stickers), (235, 236, 238, 255), "_preview_light.png")
    _sheet(out_dir, len(stickers), (28, 28, 30, 255), "_preview_dark.png")

    with open(os.path.join(out_dir, "00_ファイル対応表.txt"), "w", encoding="utf-8") as f:
        f.write(f"{title} / 登録順\n")
        f.write("=" * 42 + "\n\n")
        for i, (label, _) in enumerate(stickers, 1):
            f.write(f"{i:02d}.png   {label}\n")
        f.write("\nmain_240x240.png   メイン画像（240x240）\n")
        f.write("tab_96x74.png      トークルームタブ画像（96x74）\n")
        f.write("_preview_light.png / _preview_dark.png   確認用（申請には使わない）\n")
        f.write("\n全スタンプ画像: 370x320px / 背景透過PNG / 白フチ入り\n")
        f.write("この番号順のままLINE Creators Marketにアップロードしてください。\n")

    return verify(out_dir)


def verify(out_dir):
    """余白・透過・サイズを検証して問題のあった画像を返す。"""
    problems = []
    for f in sorted(os.listdir(out_dir)):
        if not f.endswith(".png") or f.startswith("_"):
            continue
        im = Image.open(os.path.join(out_dir, f))
        w, h = im.size
        if im.mode != "RGBA" or im.getchannel("A").getextrema()[0] != 0:
            problems.append((f, "透過なし"))
            continue
        bb = im.getchannel("A").getbbox()
        limit = 5 if f.startswith("tab") else 10
        margin = min(bb[0], bb[1], w - bb[2], h - bb[3])
        if margin < limit:
            problems.append((f, f"余白{margin}px"))
        if os.path.getsize(os.path.join(out_dir, f)) > 1_000_000:
            problems.append((f, "1MB超"))
    return problems
