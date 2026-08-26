#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gemini で絵を1枚つくる。キャラの造形を崩さないための入り口。

このファイルの存在理由:
  1冊目で、プロンプトだけで生成すると何度直してもキャラが別物になった。
  承認済みの絵を「参照画像」として渡すと1回で戻った（作業指示書 第9回の記録）。
  その渡し方を毎回書き直すと事故るので、ここに固定しておく。

使い方:
    from gen_image import generate, REF_SHEET, REF_TOTON, REF_MIO

    # 新しい構図をゼロからつくる（基準シートを必ず添える）
    generate(prompt, "out.jpg", ref_images=[REF_SHEET])

    # 既存ページを手直しする（そのページ自身を1枚目に置く）
    generate(prompt, "out.jpg", ref_images=[直すページ, REF_SHEET])

前提:
    環境変数 GEMINI_API_KEY にキーが入っていること。
    キーはリポジトリに置かない。
"""
import base64, json, os, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
IMG  = ROOT / "docs" / "絵本KDP_画像"

# 参照画像。ここを勝手に差し替えない。
REF_SHEET = IMG / "参照" / "キャラクター基準シート.jpg"   # 5面の基準シート
REF_TOTON = IMG / "10_場面09_トイレの中.jpg"              # トトン全身（正面）
REF_MIO   = IMG / "09_場面08_ノック.jpg"                  # ミオ全身＋顔
REF_BOTH  = IMG / "01_表表紙_正方形.jpg"                  # 2人の大きさの比

MODEL = "gemini-3.1-flash-image"   # Nano Banana 2
# ※ gemini-3-pro-image は503が続いた日がある。落ちたらこちらを試す。

# aspectRatio は次の14種類しか受け付けない。絵本の正方形は "1:1"。
ASPECTS = ["1:1","1:4","1:8","2:3","3:2","3:4","4:1","4:3",
           "4:5","5:4","8:1","9:16","16:9","21:9"]

KEEP = """
=== KEEP （この4行は毎回そのまま入れる）===
- The characters in the reference image are FINAL and APPROVED.
  Reproduce them exactly. Do NOT redesign, restyle, or "improve" them.
- Keep the same line weight, palette, and watercolor texture.
- Toton: pale sky blue body, white belly only, two orange cheek
  circles, solid black dot eyes with no whites and no eyebrows,
  two small round ears set high and wide apart, no tail,
  rounded limb tips with no fingers.
- Mio: short dark brown hair, solid black dot eyes, thin brows,
  green tee, beige shorts, red shoes, cream backpack.
  Toton's head reaches BELOW Mio's chest.
"""


def generate(prompt_text, out_path, model=MODEL, aspect="1:1",
             size="4K", ref_images=(REF_SHEET,), add_keep=True):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("GEMINI_API_KEY が無い。環境設定に入れること。")
    if aspect not in ASPECTS:
        raise SystemExit(f"aspectRatio は {ASPECTS} のいずれか。'{aspect}' は不可")

    parts = []
    for rp in ref_images:                       # 参照画像は必ずテキストより前
        rp = pathlib.Path(rp)
        if not rp.exists():
            raise SystemExit(f"参照画像が無い: {rp}")
        parts.append({"inline_data": {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(rp.read_bytes()).decode()}})
    parts.append({"text": prompt_text + (KEEP if add_keep else "")})

    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": aspect,
                                                 "imageSize": size}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=300) as r:
        res = json.load(r)

    # プロンプトが空のまま投げる事故を検知する（1冊目で6枚無駄にした）
    used = res.get("usageMetadata", {}).get("promptTokenCount")
    if used is not None and used < 400:
        print(f"  警告: promptTokenCount={used}。プロンプトが欠けている疑い")

    for p in res["candidates"][0]["content"]["parts"]:
        if "inlineData" in p:
            pathlib.Path(out_path).write_bytes(
                base64.b64decode(p["inlineData"]["data"]))
            print(f"  保存 {out_path}  (promptTokenCount={used})")
            return out_path
    raise SystemExit("画像が返ってこなかった:\n" + json.dumps(res, ensure_ascii=False)[:800])


if __name__ == "__main__":
    print("参照画像の場所:")
    for p in (REF_SHEET, REF_TOTON, REF_MIO, REF_BOTH):
        print(f"  {'OK ' if p.exists() else '無い'} {p}")
