#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""あかりの発光部だけを、生成し直さずに画素で縮める。

  python3 shrink_lamp.py --list
  python3 shrink_lamp.py S04_ふとんのふち
  python3 shrink_lamp.py --all

なぜ生成し直さないか（作業記録16章）:
  1か所直すと絵ぜんぶが引き直され、別の場所が崩れる。
  「あかりを小さくする」は幾何の操作なので、画素で直せば
  他はいっさい動かない。副作用がゼロになる。

やっていること:
  1. 種の点から、輪郭線に囲まれた明るい領域を広げて笠を切り出す
     （この絵柄は輪郭線が閉じているので、色ではなく線で切れる）
  2. 笠を消した跡を、境界の色から滑らかに補間して埋める
     （ラプラス方程式をヤコビ法で解く。多重格子で速くする）
  3. 笠を 横2/3・縦1/2 に縮め、底の中心を合わせて貼り戻す
"""
import sys, pathlib
import numpy as np
from PIL import Image
from scipy import ndimage

IMG = pathlib.Path(__file__).resolve().parents[1] / "絵本KDP_3冊目_画像"

MODE = "行"          # 穴の埋め方。"行" か "拡散"
W_SCALE = 2 / 3      # 直径
H_SCALE = 1 / 2      # 発光部の高さ

# ページごとの種の点と探索範囲（画像を 0..1 で正規化した座標）
#   seed  … 笠のまんなか
#   box   … 笠が確実に収まる範囲。ここから外へは広げない
#   stem  … 笠の上に伸びている細い線を一緒に消すなら True
LAMPS = {
    "S01_ねるまえ":            dict(seed=(.115, .565), box=(.02, .22, .40, .70),
                               rect=(.072, .230, .360, .578)),
    "02_場面01_めがさめる":     dict(seed=(.175, .491), box=(.06, .30, .33, .68)),
    "03_場面02_むずむず":       dict(seed=(.196, .480), box=(.08, .32, .32, .66)),
    "S04_ふとんのふち":         dict(seed=(.178, .490), box=(.09, .27, .35, .65)),
    "04_場面03_でられない":     dict(seed=(.162, .472), box=(.05, .28, .32, .66)),
    "05_場面04_ここにある":     dict(seed=(.115, .490), box=(.04, .20, .35, .62),
                               rect=(.082, .232, .360, .581)),
    "06_場面05_てをのばす":     dict(seed=(.148, .480), box=(.06, .25, .34, .62),
                               row_band=0.0,
                               clip=[(.080, .238, .366, .424),
                                     (.080, .300, .424, .600)]),
    "07_場面06_ついた":         dict(seed=(.133, .490), box=(.05, .23, .35, .62),
                               rect=(.084, .243, .354, .585)),
    "S09_じぶんでつけられた":    dict(seed=(.100, .500), box=(.02, .20, .36, .64),
                               rect=(.082, .232, .357, .581)),
    "08_場面07_ふとんからでる":  dict(seed=(.174, .476), box=(.04, .30, .32, .66)),
    "13_場面12_またねる":       dict(seed=(.148, .470), box=(.06, .25, .33, .61),
                               row_band=0.0, clip=[(.092, .248, .368, .430),
                                     (.092, .300, .430, .600)]),
    "S18_つぎのよる":           dict(seed=(.148, .480), box=(.06, .25, .34, .62),
                               row_band=0.0,
                               clip=[(.092, .250, .367, .424),
                                     (.092, .300, .424, .600)]),
    "14_裏表紙_正方形":         dict(seed=(.128, .430), box=(.05, .22, .30, .58)),
    # 【手を出さないページ】
    #   01 表紙 / 12 ろうか / 17 もどる … あかりを両手で持っている。
    #     指が笠を包んでいるので、笠だけ縮めると手が空を掴む。
    #     これは変形では直せない。手ごと描き直しが要る。
    #   13 トイレのドア / 16 てをあらう … 床と洗面台に置いてあるので
    #     機械的に縮められるはずだが、座標を読み違えて別の場所を
    #     触ってしまった。目で測り直してから入れること。
}


def lamp_mask(a, seed, box, rect=None, clip=None, thr=160):
    """笠の範囲を求めて返す。

    rect が与えられていれば、それをそのまま使う（目で読んだ矩形）。
    点灯しているページは輪郭線が光にとけて途切れ、自動では取れない。
    そこだけ手で測るほうが、判定規則をこじらせるより確実だった。
    """
    h, w, _ = a.shape
    if rect is not None:
        rx0, rx1, ry0, ry1 = rect
        m = np.zeros((h, w), bool)
        m[int(ry0 * h):int(ry1 * h), int(rx0 * w):int(rx1 * w)] = True
        return m

    x0, x1 = int(box[0] * w), int(box[1] * w)
    y0, y1 = int(box[2] * h), int(box[3] * h)
    sub = a[y0:y1, x0:x1]
    v = sub.mean(axis=2)
    # 【つまずき】縦に閉じて笠の胴と帯を繋ごうとしたら、壁も明るいので
    # 壁までつながって全部が1つの成分になった。閉じてはいけない。
    # 輪郭線で切れたままにして、必要な成分を名指しで足す。
    lab, _ = ndimage.label(v > thr)
    sy, sx = int(seed[1] * h) - y0, int(seed[0] * w) - x0
    if not (0 <= sy < lab.shape[0] and 0 <= sx < lab.shape[1]):
        raise ValueError("種の点が範囲の外にある")
    idx = lab[sy, sx]
    if idx == 0:
        raise ValueError("種の点が輪郭線の上にある。seed をずらすこと")
    m = lab == idx
    # 笠の上のボタンは別の成分になる。笠の頭のすぐ上を種にして拾う
    ys, xs = np.nonzero(m)
    bx, by = int(xs.mean()), ys.min() - int(0.02 * (y1 - y0))
    if 0 <= by < lab.shape[0]:
        j = lab[by, bx]
        if j not in (0, idx):
            m |= lab == j
    # 【つまずき】笠は、胴・下の帯・ハイライトの境目で細い線に沿って
    # いくつもの成分に切れる。種の点1つでは半分しか取れない。
    # 隣の成分を足す規則も、笠を囲む長方形も試したが、足りない絵と
    # 壁まで飲み込む絵が入れ替わるだけで収束しなかった。
    #
    # 効いたのは【外から届かない領域を取る】やり方。
    # 笠の外周は閉じた輪郭線で囲まれている。だから
    #   1. 暗い画素（輪郭線）を壁とみなす
    #   2. 上・左・右のふちから、壁を越えずに塗れる範囲を「外」とする
    #   3. 「外」でない画素＝輪郭線の内側。中で線が分かれていても一体になる
    # 下のふちは種にしない。笠は座面に接していて下が開いているため。
    ys, xs = np.nonzero(m)
    bw, bh = xs.max() - xs.min(), ys.max() - ys.min()
    tx0 = max(0, xs.min() - int(bw * 0.35))
    tx1 = min(sub.shape[1], xs.max() + int(bw * 0.35))
    ty0 = max(0, ys.min() - int(bh * 0.45))
    ty1 = min(sub.shape[0], ys.max() + int(bh * 0.03))
    tile = v[ty0:ty1, tx0:tx1]
    # 【つまずき】「明るさが中央値-42より上」を輪郭線でないとしたら、
    # 点灯しているページ（全体が明るい）で outline を拾えず失敗した。
    # 明るさの絶対値ではなく【まわりより暗いか】で線を見つける。
    local = ndimage.uniform_filter(tile.astype(np.float32), size=31)
    free = tile > (local - 11)                    # 輪郭線でない画素
    lab2, _ = ndimage.label(free)
    outer = set(lab2[0, :]) | set(lab2[:, 0]) | set(lab2[:, -1])
    outer.discard(0)
    bg = np.isin(lab2, list(outer))
    solid = ~bg
    lab3, _ = ndimage.label(solid)
    k = lab3[sy - ty0, sx - tx0]
    if k == 0:
        # 【つまずき】点灯しているページは、笠の輪郭線が光にとけて
        # 途切れる。囲いが閉じないので「外」が笠の中まで入ってくる。
        # そのときは【種の点から上下左右へ、線に当たるまで走査して】
        # 矩形を決める。囲いが閉じていなくても必ず決まる。
        dark = tile < (local - 11)
        ry, rx = sy - ty0, sx - tx0

        def hit(dy, dx, limit):
            y, x = ry, rx
            for _ in range(limit):
                y += dy; x += dx
                if not (0 <= y < dark.shape[0] and 0 <= x < dark.shape[1]):
                    break
                if dark[y, x]:
                    break
            return y, x
        _, xl = hit(0, -1, tile.shape[1])
        _, xr = hit(0, 1, tile.shape[1])
        yt, _ = hit(-1, 0, tile.shape[0])
        yb, _ = hit(1, 0, tile.shape[0])
        mw, mh = max(1, xr - xl), max(1, yb - yt)
        m2 = np.zeros_like(dark)
        m2[max(0, yt - int(mh * .10)):yb + int(mh * .06),
           max(0, xl - int(mw * .06)):xr + int(mw * .06)] = True
        m2 = ndimage.binary_dilation(m2, np.ones((7, 7)))
        out = np.zeros((h, w), bool)
        out[y0 + ty0:y0 + ty1, x0 + tx0:x0 + tx1] = m2
        return out
    m2 = ndimage.binary_fill_holes(lab3 == k)
    # 【つまずき・2回目】3px しか広げていなかったため、笠の輪郭線
    # （4096角で15px前後）がマスクの外に残った。穴の境界が暗い線に
    # なり、埋めた跡が笠の形の暗い帯になる。輪郭線より広く取ること。
    m2 = ndimage.binary_dilation(m2, np.ones((41, 41)))
    out = np.zeros((h, w), bool)
    out[y0 + ty0:y0 + ty1, x0 + tx0:x0 + tx1] = m2
    if clip is not None:
        # 【つまずき】ミオの指が笠のすぐ上にあるページでは、囲いを
        # たどると指まで一緒に取れて、消したあとが黒い塊になった。
        # 笠の外接矩形を手で測って、それで切り取る。
        rects = clip if isinstance(clip[0], (tuple, list)) else [clip]
        box_m = np.zeros((h, w), bool)
        for cx0, cx1, cy0, cy1 in rects:
            box_m[int(cy0 * h):int(cy1 * h), int(cx0 * w):int(cx1 * w)] = True
        out &= box_m
    return out



def inpaint(a, mask, margin=140, levels=5, iters=120):
    """穴を、境界の色から滑らかに埋める（ラプラス方程式・多重格子）。

    【つまずき1】穴の中身を元の画素のまま反復平均したら、笠と輪郭線の
      色が残って暗い塊になった。平均は質量を保存するので中身は消えない。
      穴をいったん【境界の平均色】で塗りつぶしてから解くこと。
    【つまずき2】4096角のまま反復したら5分でも終わらなかった。
      解くのは【穴の周りだけ】でよい。
    """
    ys, xs = np.nonzero(mask)
    y0, y1 = max(0, ys.min() - margin), min(a.shape[0], ys.max() + margin)
    x0, x1 = max(0, xs.min() - margin), min(a.shape[1], xs.max() + margin)
    sub = a[y0:y1, x0:x1].astype(np.float32)
    mk0 = mask[y0:y1, x0:x1]
    # 見本にする色は、穴からさらに離れた輪の中から取る（輪郭線を避ける）
    edge = (ndimage.binary_dilation(mk0, np.ones((41, 41)))
            & ~ndimage.binary_dilation(mk0, np.ones((13, 13))))

    pyr_m = [mk0]
    for _ in range(levels):
        pyr_m.append(pyr_m[-1][::2, ::2])

    for c in range(3):
        ch = sub[:, :, c].copy()
        ch[mk0] = ch[edge].mean()                     # まず境界の平均色で塗る
        guess = None
        for lv in range(levels, -1, -1):
            step = 2 ** lv
            cur = ch[::step, ::step].copy()
            mk = pyr_m[lv][:cur.shape[0], :cur.shape[1]]
            cur = cur[:mk.shape[0], :mk.shape[1]]
            if guess is not None:
                g = np.asarray(Image.fromarray(guess).resize(
                    (cur.shape[1], cur.shape[0]), Image.BILINEAR), dtype=np.float32)
                cur = np.where(mk, g, cur)
            for _ in range(iters):
                cur = np.where(mk, ndimage.uniform_filter(cur, size=3), cur)
            guess = cur
        g = np.asarray(Image.fromarray(guess).resize(
            (ch.shape[1], ch.shape[0]), Image.BILINEAR), dtype=np.float32)
        sub[:, :, c] = np.where(mk0, g, sub[:, :, c])

    out = a.astype(np.float32).copy()
    out[y0:y1, x0:x1] = sub
    return out


def fill_rows(a, mask):
    """穴を【行ごとに、左右の画素をまっすぐ結んで】埋める。

    拡散で埋めると、穴を横切っていた線（丸椅子の奥の縁、枕の輪郭）が
    消えてしまう。左右で同じ高さにある線は、直線で結べば再現できる。
    """
    out = a.astype(np.float32).copy()
    ys = np.nonzero(mask.any(axis=1))[0]
    for y in ys:
        row = mask[y]
        xs = np.nonzero(row)[0]
        x0, x1 = xs.min(), xs.max()
        l, r = x0 - 1, x1 + 1
        if l < 0 or r >= a.shape[1]:
            continue
        t = np.linspace(0.0, 1.0, x1 - x0 + 3)[1:-1][:, None]
        out[y, x0:x1 + 1] = out[y, l] * (1 - t) + out[y, r] * t
    return out


def add_stem(a, m, height=0.55):
    """笠の上に伸びている細い線を、マスクに足して一緒に消す。

    元の絵に、笠から真上へ伸びる細い線が描かれていることがある。
    仕様では【あかりに紐も吊り具もない】ので、これは描き損じ。
    笠を小さくすると線だけが宙に浮いて目立つため、ここで消す。
    腕などが上にある場合を壊さないよう、【その行の暗い画素が
    ごく少ないとき（＝細い線のとき）だけ】消す。
    """
    ys, xs = np.nonzero(m)
    cx = int(xs.mean())
    top = ys.min()
    half = int((xs.max() - xs.min()) * 0.30)
    up = max(0, top - int((ys.max() - top) * height))
    strip = a[up:top, cx - half:cx + half].mean(axis=2)
    if strip.size == 0:
        return m
    dark = strip < (np.median(strip) - 18)
    per_row = dark.sum(axis=1)
    ok = per_row < (0.16 * strip.shape[1])          # 細い線だけ
    sel = dark & ok[:, None]
    sub = np.zeros_like(m[up:top, cx - half:cx + half])
    sub |= ndimage.binary_dilation(sel, np.ones((5, 21)))
    m = m.copy()
    m[up:top, cx - half:cx + half] |= sub
    return m


def shrink(name, out_dir=None):
    p = IMG / f"{name}.jpg"
    cfg = LAMPS[name]
    im = Image.open(p).convert("RGB")
    a = np.asarray(im, dtype=np.int64)
    h, w, _ = a.shape

    m = lamp_mask(a, cfg["seed"], cfg["box"], cfg.get("rect"), cfg.get("clip"))
    ys, xs = np.nonzero(m)
    keep = m.copy()                      # 笠の形はこちら。線は貼り戻さない
    m = add_stem(a, m)
    ys, xs = np.nonzero(keep)
    lx0, lx1, ly0, ly1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    lw, lh = lx1 - lx0, ly1 - ly0

    lamp = Image.fromarray(a[ly0:ly1, lx0:lx1].astype("uint8"))
    alpha = Image.fromarray((keep[ly0:ly1, lx0:lx1] * 255).astype("uint8"))

    # 【つまずき】拡散だけで埋めると、穴を横切っていた線
    #   （丸椅子の奥の縁）が消える。行ごとの直線補間だけで埋めると、
    #   左右の色が違う行に横縞が出る。どちらか一方では駄目だった。
    # 上（無地の壁）は拡散、下端（座面の縁が通るところ）は行補間、
    # と高さで使い分ける。
    # ミオの手や枕の影がマスクの右に掛かるページでは、行補間が
    # 暗い色を引き伸ばして四角い汚れになる。そこは全部を拡散で埋める。
    ys_m = np.nonzero(m.any(axis=1))[0]
    frac = cfg.get("row_band", 0.22)
    cut = ys_m.max() - int((ys_m.max() - ys_m.min()) * frac)
    m_up, m_lo = m.copy(), m.copy()
    m_up[cut:, :] = False
    m_lo[:cut, :] = False
    filled = a.astype(np.float32)
    if m_up.any():
        filled = inpaint(filled, m_up)
    if m_lo.any():
        filled = fill_rows(filled, m_lo)
    # 【つまずき】跡を消そうと境目を羽根ぼかしで溶かしたら、
    # マスクのふちに残った【古い笠の輪郭】が幽霊のように浮き出た。
    # 穴はぼかさず、そのまま差し替えるのが正しい。
    base = Image.fromarray(np.clip(filled, 0, 255).astype("uint8"))

    nw, nh = max(2, int(round(lw * W_SCALE))), max(2, int(round(lh * H_SCALE)))
    lamp_s = lamp.resize((nw, nh), Image.LANCZOS)
    alpha_s = alpha.resize((nw, nh), Image.LANCZOS)
    # 底の中心をそろえる（座面に乗ったまま小さくなる）
    px = (lx0 + lx1) // 2 - nw // 2
    py = ly1 - nh
    base.paste(lamp_s, (px, py), alpha_s)

    dst = (pathlib.Path(out_dir) / f"{name}.jpg") if out_dir else p
    base.save(dst, quality=95)
    print(f"  {name}  笠 {lw}x{lh} → {nw}x{nh}  （底の中心 {(lx0+lx1)//2},{ly1}）")


if __name__ == "__main__":
    a = sys.argv[1:]
    out = None
    if "--out" in a:
        i = a.index("--out"); out = a[i + 1]; del a[i:i + 2]
    if not a or a[0] == "--list":
        for k in LAMPS: print(" ", k)
    else:
        names = list(LAMPS) if a[0] == "--all" else a
        for n in names:
            try:
                shrink(n, out)
            except Exception as e:
                print(f"  × {n}: {type(e).__name__} {e}")
