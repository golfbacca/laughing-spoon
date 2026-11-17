"""下絵を印刷用ページ画像（A4・300dpi・グレースケール）に整える。

使い方: python3 build_pages.py <srcフォルダ> <出力フォルダ>

処理（1枚ずつ）:
  1. グレースケール化（色かぶりを除く）
  2. 紙色を純白へ（明るい側90パーセンタイルを255に引き上げ、248以上は255に）
  3. 絵の範囲（枠線を含む）を検出して切り抜く
  4. 安全範囲（A4から上下12mm・左右13mm を除いた 184×273mm）に収まるよう拡大（Lanczos）
  5. 輪郭を軽く強調（アンシャープマスク）
  6. A4（2481×3508px）の白紙の中央に置く
  横長の絵は左に90度回転して縦ページに置く（rotated に記録）。

KDPの余白の下限: 外側6.4mm、綴じ側9.6mm（24〜150ページ）。13mmなら両側どちらに来ても満たす。
"""
import glob, json, os, sys
import numpy as np
from PIL import Image, ImageFilter

DPI = 300
MM = DPI / 25.4
PAGE = (round(210 * MM), round(297 * MM))          # 2480x3508
SAFE = (round(184 * MM), round(273 * MM))          # 2173x3224

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
report = []
for f in sorted(glob.glob(os.path.join(src, '*'))):
    if not f.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    im = Image.open(f).convert('L')
    rotated = im.width > im.height
    if rotated:
        im = im.rotate(90, expand=True)
    a = np.asarray(im).astype(float)
    bg = np.percentile(a, 90)
    a = np.clip(a * 255 / bg, 0, 255)
    a[a >= 248] = 255
    dark = a < 200
    ys, xs = np.where(dark)
    # 端のノイズに引っ張られないよう、0.05%点で範囲を取る
    y0, y1 = np.percentile(ys, [0.05, 99.95]).astype(int)
    x0, x1 = np.percentile(xs, [0.05, 99.95]).astype(int)
    im = Image.fromarray(a.astype('uint8')).crop((x0, y0, x1 + 1, y1 + 1))
    s = min(SAFE[0] / im.width, SAFE[1] / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    page = Image.new('L', PAGE, 255)
    page.paste(im, ((PAGE[0] - im.width) // 2, (PAGE[1] - im.height) // 2))
    name = os.path.splitext(os.path.basename(f))[0]
    page.save(os.path.join(out, name + '.png'), dpi=(DPI, DPI))
    report.append({'file': name, 'scale': round(s, 2), 'rotated': rotated,
                   'placed_mm': [round(im.width / MM), round(im.height / MM)]})
    print(f'{name}\t拡大 {s:.2f}倍\t{"横→回転" if rotated else ""}')
json.dump(report, open(os.path.join(out, 'report.json'), 'w'), ensure_ascii=False, indent=1)
