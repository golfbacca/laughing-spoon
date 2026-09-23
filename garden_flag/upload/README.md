# 入稿データ（Printify にアップロードするファイル）

すべて **3900 × 5700 px / 300DPI**。Printify の「Garden and House Banner 12"×18"」用。

## このフォルダ直下 — 商品作成に使う5枚

名字が **THE SMITHS** で入っている。**Printify の商品作成はこれを使う。**

| ファイル | 決め台詞 |
|---|---|
| `R01_SMITHS_3900x5700.png` | STILL WORKING ON IT |
| `R02_SMITHS_3900x5700.png` | 19TH HOLE - ALWAYS OPEN |
| `R05_SMITHS_3900x5700.png` | MULLIGANS WELCOME HERE |
| `R09_SMITHS_3900x5700.png` | GONE GOLFING - BACK EVENTUALLY |
| `R11_SMITHS_3900x5700.png` | GOLF CLUB - MEMBERS ONLY |

## `blank/` — 名字が空の版

**注文が来たときに、ここへ名字を合成する。**

```bash
python3 make_name_flag_r.py JOHNSONS
```

`tools/` の中で実行する（`blank/` を `upload_r/` という名前で置く）。
`bands_r.json` と `fonts/` が必要。どちらもリポジトリに入っている。

※ 末尾に **S を付ける**（`THE JOHNSONS` になる）。
※ 既に S で終わる名字（例 `ROGERS`）は **`ROGERS`** のまま。

## 検証済みの値（2026-09-23）

| | 結果 |
|---|---|
| 寸法 | 5枚とも 3900×5700 |
| 上端750px（袖＋裁ち落としで見えない範囲）への侵食 | **5枚とも 0.00%** |
| R01 のギンガム柄 | 縞43本・高さ97〜109px・**ばらつき ±6%**（補修済み） |
| R09 のタータン柄 | ブロック9個・高さ210〜235px（再生成版） |
| 下部文言の裁ちからの余白 | 全案 **0.70インチ以上**（安全域0.25"に対し十分） |

## 作り直すには

`garden_flag/source/README.md` の手順を参照。
⚠ **R01 は入稿データを作ったあとに `tools/mockup/fix_r01.py` を当てること。**
