# 元データ（Gemini の出力そのまま）

Gemini が出したJPEGを**無変換**で置いてある。
ここから `garden_flag/listing/` の出品画像までを再現できる。

| ファイル | 中身 | サイズ |
|---|---|---|
| `R01 STILL WORKING ON IT.jpeg` | 黄色ギンガム・ゴルフバッグ | 1696×2528 |
| `R02 19TH HOLE - ALWAYS OPEN.jpeg` | 鮮やかな緑・グリーンとピン | 1696×2528 |
| `R05 MULLIGANS WELCOME HERE.jpeg` | クリーム地・水彩の花 | 1696×2528 |
| `R09 GONE GOLFING - BACK EVENTUALLY.jpeg` | タータン枠・ゴルフカート | 1696×2528 |
| `R11 GOLF CLUB - MEMBERS ONLY.jpeg` | 濃紺と金・交差クラブ | 1696×2528 |
| `background01.jpeg` | 前庭の花壇 | 2816×1536 |
| `background02.jpeg` | 玄関前 | 2816×1536 |
| `background03.jpeg` | ゴルフコースが見える庭 | 2816×1536 |

**R09 は 2026-09-23 に作り直したもの**（`docs/24_R09の再生成.md`）。
旧版はタータンの柄が崩れていた。

---

## ⚠ R01 は、この元データだけでは正しく再現できない

**R01 のギンガム柄は、この元データの時点で崩れている**
（`docs/23_R01の格子柄の補修.md`）。補修は入稿データを作った**あと**に当てる。

```
source/R01*.jpeg
  ↓ tools/build_upload_r.py        ← 入稿 3900x5700 を作る（柄は崩れたまま）
  ↓ tools/mockup/fix_r01.py        ← ★ここで柄を直す
upload_r/R01_upload_3900x5700.png
```

`fix_r01.py` は初回に `upload_r/_R01_before.png` へ補修前を退避するので、
2回流しても壊れない。

---

## 再現手順

作業ディレクトリに `source/` を `zin/` という名前で置き、`tools/` の中身を並べる。

```bash
python3 build_upload_r.py          # 5案の入稿データ 3900x5700 を作る
python3 mockup/fix_r01.py          # R01 のギンガム柄を補修
python3 detect_plates.py           # 名入れプレートを検出 → bands_r.json
python3 make_name_flag_r.py SMITHS # 名入れ合成
python3 mockup/run_geom.py         # 背景写真の旗の輪郭を実測
python3 mockup/make_mock.py        # モックアップ15枚
python3 mockup/build_listing.py    # 出品画像（1〜4・6〜8枚目）
python3 house/size_two.py          # 5枚目（2サイズ併記の図）
```

必要なもの：Python + Pillow + numpy + scipy。

フォントは `tools/fonts/` に同梱してある（すべて Google Fonts・OFLライセンス）。

| ファイル | 使う案 |
|---|---|
| `PlayfairDisplay.ttf` | R01・R09 の名字 |
| `Oswald.ttf` | R02 の名字 |
| `Lora.ttf` | R05 の名字 |
| `Cinzel.ttf` | R11 の名字 |
| `Montserrat.ttf` | 出品画像の説明文（可変フォント） |
| `BebasNeue.ttf` | 予備 |
