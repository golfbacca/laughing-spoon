#!/usr/bin/env python3
"""部屋の写真（Gemini・無地の白いタペストリー）に M01 を貼り込む。出品画像の1・2・4枚目。

やり方は garden_flag/tools/mockup/composite.py と同じ：
  1. 白い布を検出（彩度が低い・明るい・暖色でない）
  2. 行ごとの左右端・列ごとの上下端で座標を正規化して絵を流し込む → たわみが残る
  3. 元写真の明暗を乗算で戻す → しわと影が残る

背景写真の白い布の右下で、影になった壁まで拾ってしまう（彩度がほぼ同じ）。
→ 右端は上半分の直線を、下端は左60%の曲線を、それぞれ外へ延ばして布の形を決める。

使い方: python3 tapestry/tools/compose_room.py
出力:   listing/M01_<色>/1_bedroom.jpg, 2_living.jpg, 4_closeup.jpg（2000×1500）
"""
import os
from io import BytesIO
import numpy as np
import cairosvg
from PIL import Image, ImageFilter
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
COLORS = ["dawn", "dusk", "night", "sage"]
# 背景ごとの「布がこの中にある」外枠（x0,y0,x1,y1。目測＋実測で決めた・docs/09）
SCENES = {
    "bedroom": dict(file="bedroom.jpg", box=(700, 30, 1662, 1122)),
    "living": dict(file="living.jpg", box=(670, 60, 1684, 1150)),
}


def detect(img, box):
    im = np.asarray(img).astype(float)
    mx, mn = im.max(2), im.min(2)
    S = (mx - mn) / np.maximum(mx, 1) * 255
    m = (S < 7) & (mx > 140) & (im[:, :, 0] - im[:, :, 2] < 6)
    keep = np.zeros_like(m)
    keep[box[1]:box[3], box[0]:box[2]] = True
    m = ndimage.binary_opening(m & keep, iterations=2)
    lab, _ = ndimage.label(m)
    m = lab == lab[(box[1] + box[3]) // 3, (box[0] + box[2]) // 2]
    m = ndimage.binary_fill_holes(ndimage.binary_closing(m, iterations=6))

    H, W = m.shape
    rows = np.where(m.any(1))[0]
    cols = np.where(m.any(0))[0]
    xl = np.array([np.where(m[y])[0].min() for y in rows], float)
    xr = np.array([np.where(m[y])[0].max() for y in rows], float)
    yt = np.array([np.where(m[:, x])[0].min() for x in cols], float)
    yb = np.array([np.where(m[:, x])[0].max() for x in cols], float)
    # 4辺とも、外れ値を除いたなめらかな曲線にする（生のデータは壁の影の漏れや凹みを含む）
    # 右端・下端は漏れが外側に大きく出るので、信頼できる側（右端＝上半分、下端＝左60%）の
    # 直線から始め、そこから±6px（元写真の画素）以内の点だけで2次曲線を当て直す
    tol = 6 * H / 1792  # 許容ずれ（元写真で6px。2倍に拡大したときは12px）

    def robust(t, v, deg, seed):
        k = np.polyfit(t[seed], v[seed], 1)
        for _ in range(3):
            ok = np.abs(v - np.polyval(k, t)) < tol
            k = np.polyfit(t[ok], v[ok], deg)
        return np.polyval(k, t), ok.mean()
    half = np.arange(len(rows)) < len(rows) // 2
    left = np.arange(len(cols)) < int(len(cols) * 0.6)
    every_r = np.ones(len(rows), bool)
    every_c = np.ones(len(cols), bool)
    xl, fl = robust(rows, xl, 2, every_r)
    xr, fr = robust(rows, xr, 2, half)
    yt, ft = robust(cols, yt, 4, every_c)
    yb, fb = robust(cols, yb, 2, left)
    print(f"   採用した点の割合 左{fl:.0%} 右{fr:.0%} 上{ft:.0%} 下{fb:.0%}")

    ys, xs = np.mgrid[0:H, 0:W]
    XL = np.full(H, np.inf); XR = np.full(H, -np.inf)
    XL[rows], XR[rows] = xl, xr
    YT = np.full(W, np.inf); YB = np.full(W, -np.inf)
    inside = (cols >= xl.min()) & (cols <= xr.max())
    YT[cols[inside]], YB[cols[inside]] = yt[inside], yb[inside]
    mask = (xs >= XL[:, None]) & (xs <= XR[:, None]) & (ys >= YT[None, :]) & (ys <= YB[None, :])
    # 曲線は大まかな形（右端以外）。角の近くでは実際の端から数px ずれ、白い布が細く残る。
    # → 曲線の ±8px（元写真）の範囲で、明るさがいちばん大きく落ちる位置（布の端→影）を
    #   1行・1列ずつ探し、中央値でならして端にする。範囲を限るので壁の影へは漏れない
    lum = ndimage.gaussian_filter(0.299 * im[:, :, 0] + 0.587 * im[:, :, 1] + 0.114 * im[:, :, 2], 0.8)
    win = int(round(8 * H / 1792))

    def refine(edge, idx, outward, axis):
        new = edge.copy()
        for i in idx:
            e = int(round(edge[i]))
            lo, hi = e - win, e + win
            if axis == "x":
                if lo < 1 or hi >= W - 1: continue
                prof = lum[i, lo - 1:hi + 2]
            else:
                if lo < 1 or hi >= H - 1: continue
                prof = lum[lo - 1:hi + 2, i]
            drop = (prof[1:-1] - prof[2:]) if outward > 0 else (prof[1:-1] - prof[:-2])
            new[i] = lo + int(np.argmax(drop))
        sm = ndimage.median_filter(new[idx], 31, mode="nearest")
        sm = ndimage.uniform_filter1d(sm.astype(float), 31, mode="nearest")
        new[idx] = np.clip(sm, edge[idx] - win, edge[idx] + win)
        return new
    XL = refine(XL, rows, -1, "x")
    # 右端は壁の影が布の色に近く、端の取り違えでぎざぎざになる → 曲線を平行に動かすだけにする
    d = []
    for y in rows[::7]:
        e = int(round(XR[y]))
        if e + win + 2 < W:
            prof = lum[y, e - win - 1:e + win + 2]
            d.append(int(np.argmax(prof[1:-1] - prof[2:])) - win)
    XR = XR + float(np.median(d))
    cin = cols[np.isfinite(YT[cols])]
    YT = refine(YT, cin, -1, "y")
    YB = refine(YB, cin, +1, "y")
    mask = (xs >= XL[:, None]) & (xs <= XR[:, None]) & (ys >= YT[None, :]) & (ys <= YB[None, :])
    return mask, XL, XR, YT, YB


def art(key, width):
    png = cairosvg.svg2png(url=os.path.join(ROOT, "source", f"M01_{key}.svg"), output_width=width)
    return Image.open(BytesIO(png)).convert("RGB")


def compose(bg, mask, XL, XR, YT, YB, design):
    H, W = mask.shape
    out = np.asarray(bg).astype(np.float32)
    ys, xs = np.where(mask)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    # 写真の布の縦横比に合わせて、絵の中央を切る（引き伸ばさない）
    ar = np.median((XR - XL)[np.isfinite(XL)]) / np.median((YB - YT)[np.isfinite(YT)])
    dw, dh = design.size
    if dw / dh > ar:
        nw = round(dh * ar); design = design.crop(((dw - nw) // 2, 0, (dw + nw) // 2, dh))
    else:
        nh = round(dw / ar); design = design.crop((0, (dh - nh) // 2, dw, (dh + nh) // 2))
    da = np.asarray(design).astype(np.float32)
    Hd, Wd = da.shape[:2]
    gy, gx = np.mgrid[y0:y1 + 1, x0:x1 + 1]
    u = np.clip((gx - XL[gy]) / np.maximum(XR[gy] - XL[gy], 1), 0, 1)
    v = np.clip((gy - YT[gx]) / np.maximum(YB[gx] - YT[gx], 1), 0, 1)
    warp = np.stack([ndimage.map_coordinates(da[:, :, k], [v * (Hd - 1), u * (Wd - 1)], order=1)
                     for k in range(3)], axis=2)
    sub = out[y0:y1 + 1, x0:x1 + 1]
    lum = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
    p = np.percentile(lum[mask[y0:y1 + 1, x0:x1 + 1]], 98)
    shade = np.clip(lum / max(p, 1), 0, 1.1) ** 0.92
    painted = np.clip(warp * shade[:, :, None], 0, 255)
    alpha = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.4)),
                       np.float32)[y0:y1 + 1, x0:x1 + 1, None] / 255
    out[y0:y1 + 1, x0:x1 + 1] = sub * (1 - alpha) + painted * alpha
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def to_43(img):
    W, H = img.size
    w = round(H * 4 / 3)
    x = (W - w) // 2
    return img.crop((x, 0, x + w, H)).resize((2000, 1500), Image.LANCZOS)


def main():
    for scene, cfg in SCENES.items():
        bg = Image.open(os.path.join(ROOT, "mockup_bg", cfg["file"])).convert("RGB")
        mask, XL, XR, YT, YB = detect(bg, cfg["box"])
        ys, xs = np.where(mask)
        print(f"{scene}: 布 x {xs.min()}〜{xs.max()} / y {ys.min()}〜{ys.max()} "
              f"縦横比 {(xs.max()-xs.min())/(ys.max()-ys.min()):.3f}")
        # 寄りの画像用に、背景を2倍にしてから貼る（絵がぼけない）
        if scene == "bedroom":
            bg2 = bg.resize((bg.width * 2, bg.height * 2), Image.LANCZOS)
            m2 = detect(bg2, [v * 2 for v in cfg["box"]])
        for key in COLORS:
            outdir = os.path.join(ROOT, "listing", f"M01_{key}")
            os.makedirs(outdir, exist_ok=True)
            img = compose(bg, mask, XL, XR, YT, YB, art(key, 1600))
            name = "1_bedroom" if scene == "bedroom" else "2_living"
            to_43(img).save(os.path.join(outdir, f"{name}.jpg"), quality=92)
            if scene == "bedroom":
                big = compose(bg2, *m2, art(key, 3200))
                cx, cy = (xs.min() + xs.max()), int((ys.min() + ys.max()) * 0.8)
                big.crop((cx - 1000, cy - 750, cx + 1000, cy + 750)).save(
                    os.path.join(outdir, "4_closeup.jpg"), quality=92)
    print("done")


if __name__ == "__main__":
    main()
