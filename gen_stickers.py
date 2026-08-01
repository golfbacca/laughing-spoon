# -*- coding: utf-8 -*-
"""
LINEスタンプ シリーズB「呪詛版」 16枚 + メイン + タブ 生成
370x320 / 背景透過PNG / 全文字に白フチ
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stickers")
os.makedirs(OUT, exist_ok=True)

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

SUMI  = (26, 26, 26, 255)
CHI   = (123, 30, 30, 255)
HAI   = (110, 110, 110, 255)
WHITE = (255, 255, 255, 255)

W, H = 370, 320
MARGIN = 12
SAFE_W, SAFE_H = W - MARGIN * 2, H - MARGIN * 2


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


def build(spec, size=(W, H)):
    cw, ch = size
    safe_w, safe_h = cw - MARGIN * 2, ch - MARGIN * 2
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
            x = MARGIN + safe_w * 0.05
        else:
            x = cw - MARGIN - im.width - safe_w * 0.05
        x += b.get("dx", 0)
        canvas.alpha_composite(im, (int(round(x)), int(round(y))))
        y += im.height

    if spec.get("rotate"):
        canvas = canvas.rotate(spec["rotate"], resample=Image.BICUBIC, expand=False)
    return canvas


# ─────────────────────────────────────────────
# 16枚の設計（登録順）
# ─────────────────────────────────────────────
S = [
 ("01_今、修羅場です", {"blocks":[
    {"text":"今、","font":"black","size":44,"color":SUMI},
    {"text":"修羅場です","font":"black","size":66,"color":CHI,"gap":4},
 ]}),
 ("02_私が決めた規約じゃない", {"blocks":[
    {"text":"私が","font":"black","size":46,"color":CHI},
    {"text":"決めた規約","font":"black","size":54,"color":SUMI,"gap":2},
    {"text":"じゃない","font":"black","size":54,"color":SUMI,"gap":2},
 ]}),
 ("03_助けて、は言えない", {"blocks":[
    {"text":"助けて","font":"min_m","size":86,"color":CHI},
    {"text":"は言えない","font":"min_l","size":26,"color":HAI,"gap":14,"align":"right"},
 ]}),
 ("04_本日の被弾報告", {"blocks":[
    {"text":"本日の被弾報告","font":"min_r","size":44,"color":SUMI,"spacing":6},
    {"type":"rule","width":296,"thick":3,"color":SUMI,"gap":14},
 ]}),
 ("05_隣の席、静かになった", {"blocks":[
    {"text":"隣の席、","font":"min_l","size":40,"color":SUMI},
    {"text":"静かになった","font":"min_l","size":44,"color":SUMI,"gap":38},
 ]}),
 ("06_今の、生き物だった", {"blocks":[
    {"text":"今の、","font":"min_l","size":38,"color":SUMI},
    {"runs":[("生き物",CHI),("だった",SUMI)],"font":"min_m","size":50,"spacing":4,"gap":8},
 ]}),
 ("07_まだ辞めてない", {"blocks":[
    {"text":"まだ","font":"min_m","size":66,"color":CHI,"align":"left"},
    {"text":"辞めてない","font":"min_l","size":44,"color":HAI,"gap":6,"align":"right"},
 ]}),
 ("08_明日も鳴る、必ず", {"blocks":[
    {"text":"明日も鳴る、","font":"min_l","size":40,"color":SUMI},
    {"text":"必ず","font":"min_m","size":84,"color":CHI,"gap":12},
 ]}),
 ("09_生きてる人、挙手", {"blocks":[
    {"text":"生きてる人、","font":"maru","size":42,"color":SUMI,"jitter":1.7,"seed":3},
    {"text":"挙手","font":"maru","size":72,"color":SUMI,"gap":4,"jitter":1.7,"seed":5},
 ], "rotate":-4}),
 ("10_誰か代わって（無理か）", {"blocks":[
    {"text":"誰か代わって","font":"maru","size":52,"color":SUMI},
    {"text":"（無理か）","font":"maru","size":28,"color":HAI,"gap":10,"align":"right","alpha":0.82},
 ]}),
 ("11_今の、通報案件", {"blocks":[
    {"text":"今の、","font":"black","size":34,"color":SUMI},
    {"text":"通報","font":"black","size":80,"color":CHI,"gap":2},
    {"text":"案件","font":"black","size":44,"color":SUMI,"gap":2},
 ]}),
 ("12_守ってもらえない側", {"blocks":[
    {"type":"vertical","text":"守ってもらえない側","font":"min_l","size":32,"color":HAI,"line":1.0},
 ], "dx":0}),
 ("13_人間の消耗品です", {"blocks":[
    {"text":"人間の消耗品です","font":"min_l","size":40,"color":SUMI,"spacing":3},
 ], "dy":30}),
 ("14_同業しかわからない", {"blocks":[
    {"type":"vertical","text":["同業しか","わからない"],"font":"min_l","size":46,"color":SUMI,"line":1.0},
 ]}),
 ("15_これ読める人は仲間", {"blocks":[
    {"text":"これ読める人は","font":"sans_l","size":38,"color":SUMI,"spacing":2},
    {"text":"仲間","font":"sans_l","size":58,"color":CHI,"gap":10},
 ]}),
 ("16_明日も生きてたら会おう", {"blocks":[
    {"text":"明日も生きてたら","font":"min_l","size":38,"color":SUMI},
    {"text":"会おう","font":"min_l","size":38,"color":SUMI,"gap":10},
 ]}),
]
# 縦書き2枚は右に寄せる
S[11][1]["blocks"][0]["dx"] = 58
S[13][1]["blocks"][0]["dx"] = 30   # 2列になった分、寄せ幅を控えめに

mapping = []
for i, (name, spec) in enumerate(S, 1):
    fn = f"{i:02d}.png"
    build(spec).save(os.path.join(OUT, fn))
    mapping.append((fn, name.split("_", 1)[1]))

# メイン画像 240x240
build({"blocks":[
    {"text":"今、","font":"black","size":32,"color":SUMI},
    {"text":"修羅場です","font":"black","size":46,"color":CHI,"gap":4},
]}, size=(240, 240)).save(os.path.join(OUT, "main_240x240.png"))

# タブ画像 96x74
MARGIN = 5
build({"blocks":[
    {"text":"修羅場","font":"black","size":23,"color":SUMI},
]}, size=(96, 74)).save(os.path.join(OUT, "tab_96x74.png"))
MARGIN = 12

# ── 確認用コンタクトシート（明るい背景／暗い背景） ──
def sheet(bg, fname):
    cols, rows = 4, 4
    pad = 14
    sw, sh = W, H
    img = Image.new("RGBA", (cols * sw + pad * (cols + 1), rows * sh + pad * (rows + 1)), bg)
    for i, (name, _) in enumerate(S):
        st = Image.open(os.path.join(OUT, f"{i+1:02d}.png"))
        c, r = i % cols, i // cols
        img.alpha_composite(st, (pad + c * (sw + pad), pad + r * (sh + pad)))
    img.convert("RGB").save(os.path.join(OUT, fname), quality=95)

sheet((235, 236, 238, 255), "_preview_light.png")   # 明るいトーク背景
sheet((28, 28, 30, 255),   "_preview_dark.png")     # ダークモード

with open(os.path.join(OUT, "00_ファイル対応表.txt"), "w", encoding="utf-8") as f:
    f.write("LINEスタンプ シリーズB「呪詛版」16枚 / 登録順\n")
    f.write("=" * 42 + "\n\n")
    for fn, label in mapping:
        f.write(f"{fn}   {label}\n")
    f.write("\nmain_240x240.png   メイン画像（240x240）\n")
    f.write("tab_96x74.png      トークルームタブ画像（96x74）\n")
    f.write("_preview_light.png / _preview_dark.png   確認用（申請には使わない）\n")
    f.write("\n全スタンプ画像: 370x320px / 背景透過PNG / 白フチ入り\n")
    f.write("この番号順のままLINE Creators Marketにアップロードしてください。\n")
print("done:", len(os.listdir(OUT)), "files")
for f in sorted(os.listdir(OUT)):
    if not f.endswith(".png"):
        continue
    im = Image.open(os.path.join(OUT, f))
    print(f"  {f}  {im.size}  {im.mode}  {os.path.getsize(os.path.join(OUT,f))//1024}KB")
