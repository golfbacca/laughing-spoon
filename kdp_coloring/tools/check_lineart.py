"""ぬりえ下絵の一括検査。

使い方: python3 check_lineart.py <画像フォルダ> [出力フォルダ]
  - 解像度（KDP 8.5x11in・余白0.375inに収めたときのdpi。300未満は不足）
  - 紙色（背景の明るさ。255=純白。245未満は色付き紙に見える）
  - 彩度（0に近いほど純グレー。4超はクリーム色等の色かぶり）
  - 中間調%（鉛筆の陰影の量。20%超は「塗る余地」が少ない）
  - 右下の切り抜きを一覧化（Geminiの透かし ✦ の目視用）→ corners.jpg
  - 完全一致の重複ファイルを検出
"""
import glob, hashlib, os, sys
import numpy as np
from PIL import Image, ImageDraw

src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else src
files = sorted(f for f in glob.glob(os.path.join(src, '**', '*'), recursive=True)
               if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')))
seen, rows, crops = {}, [], []
TW, TH = 8.5 - 0.75, 11 - 0.75
for f in files:
    h = hashlib.md5(open(f, 'rb').read()).hexdigest()
    if h in seen:
        print('重複:', f, '=', seen[h]); continue
    seen[h] = f
    im = Image.open(f).convert('RGB'); w, hh = im.size
    a = np.asarray(im).astype(float); L = a.mean(2)
    bg = np.median(L[L > 200]) if (L > 200).any() else 0
    rows.append((os.path.basename(f), w, hh, round(min(w / TW, hh / TH)), round(bg),
                 round((a.max(2) - a.min(2)).mean(), 1),
                 round(((L > 70) & (L < 190)).mean() * 100, 1)))
    crops.append(im.crop((w - 220, hh - 220, w, hh)))
print('file\tw\th\tdpi\t紙色\t彩度\t中間調%')
for r in rows:
    flag = ' ←dpi不足' if r[3] < 300 else ''
    print('\t'.join(map(str, r)) + flag)
sh = Image.new('RGB', (230 * 8, 250 * ((len(crops) + 7) // 8)), 'white'); d = ImageDraw.Draw(sh)
for i, c in enumerate(crops):
    x, y = (i % 8) * 230, (i // 8) * 250; sh.paste(c, (x + 5, y + 28)); d.text((x + 5, y + 5), str(i + 1), fill='red')
sh.save(os.path.join(out, 'corners.jpg'), quality=90)
