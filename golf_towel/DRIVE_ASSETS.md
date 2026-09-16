# Google Drive 上の素材索引

2026-09-16、本人が `C:\Users\bangd\Downloads\Golf Towel` を
**マイドライブ ＞ Golf Towel** にアップロード。クラウドセッションから参照できる。

## 取得方法（クラウドセッション）

- 一覧: `mcp__Google_Drive__search_files` に `parentId = '<フォルダID>'`
- **画像の実データ**: `mcp__Google_Drive__download_file_content`（base64で返る）
  - ⚠️ `read_file_content` は画像に対して**空文字を返す**（2026-09-16に確認済み）。使わない
  - base64は大きいので、**本当に必要な1枚だけ**落とすこと

## ルートフォルダ

`Golf Towel` … `1oR2DUbLwyA4Pluc9Sik0Y4t4rI3tSehJ`

## サブフォルダ

| フォルダ | ID |
|---|---|
| `listing_images`（P08/P15/P20の出品画像＋**モックアップ原本**） | `1YhO2gSXlWZxOup2P_oipI5rQQbcxJV1Y` |
| `listing_images_p01` | `1YxQS8NJqujyAnLyOZ4xXOTWEQ_-SyBrS` |
| `listing_images_p02` | `1pk1tJSKmNzsCcVSkqc3HTjm-zKKioUtx` |
| `listing_images_p03` | `1HD4W_49z0e9JZIqO7zgfEiWZhoCD990l` |
| `listing_images_p12` | `1E4hoUgT5oFulXCea7JLoJLoWuxNxZYFM` |
| `listing_images_p17` | `1GWbqvsOcx-yzD3A_nu5vZBaF2u6G6e8o` |
| `listing_images_p20v2` | `1UcK1S8RMnKwPXXmcIYTomAnZ6u0YGIcy` |
| `listing_images_personalized` | `1hU8lOTOOldREgiz3CVGySx0nJ_u0BPr6` |
| `personalized`（年号別入稿データ） | `1S3fyi4GLqvbQeNfeiDPLMA337uinUH00` |

## 最重要ファイル

**モックアップ原本**（Printify生成の実写。2048×2048。全商品写真の土台）

| ファイル | ID |
|---|---|
| `listing_images/p15_mockup_front.jpg` | `1u96ypenbYaNMngdWU_T5n_4zogzGUdUS` |
| `listing_images/p08_mockup_front.jpg` | `10II11rkDcuSXQjk9sv4Ej9qhPkOwjX4A` |
| `listing_images/mockup_front.jpg` | `1C7MwEe3h-OIViVjYMkTa3r2YyJmhSsVe` |
| `listing_images/mockup_back.jpg` | `1x97v2afERzTXvXw36vnQ0bSwhgwiGJZJ` |

この写真における実測座標（`HANDOFF.md` §4-3 より）:
```
PRINT_RECT = (515, 291, 1518, 1753)   # 入稿データ全体が収まる矩形
TOWEL_RECT = (539, 320, 1495, 1727)   # 全面ベタのデザインはここでマスク
TBOX       = (517, 297, 1434, 1700)   # レイアウト用
```

**出品画像7枚の実物**（テンプレートの参考。P15の例）

`P15_img1_main` / `img2_lifestyle` / `img3_closeup` / `img4_size` /
`img5_features` / `img6_gift` / `img7_notice`（すべて `listing_images` 内）

※ P08・P15・P20の2枚目は旧方式の「バッグ装着写真」（`img2_lifestyle`）。
P01/P02/P03/P12/P17は新方式の「オチ解説」。**ガーデンフラッグでは新方式を採用する。**

**入稿データ**（5043×7350・300DPI。ルート直下）

`P01` `P02` `P03` `P12` `P15` `P08` `P17` `_upload_5043x7350.png`、
`P20_upload_fixed_5043x7350.png`、および中間生成物の `*_print.png`

## まだDriveに無いもの（必要になったら本人に依頼）

`C:\Users\bangd\claude-test\` 側にあり、**未アップロード**。

- [ ] `make_towel_listing_images.py` … **最重要**。モックアップ生成と出品画像7枚の実装。
      ガーデンフラッグ版を書く土台になる（`mockup()` と `_clean_plate()`）
- [ ] `make_year_towel.py` / `year_mockup.py` / `prepare_designs.py`
- [ ] `golf_towel_20patterns_brief.md` … 構図ブリーフの書式
- [ ] `p01_p02_p03_p12_listing_copy.md` / `p17_listing_copy.md` /
      `personalized_listing_copy.md` … **英語タイトル・タグ13個・説明文の実物**
- [ ] `personalized_order_runbook.md`

**テキストファイルなのでチャットに貼り付けるだけでよい。** Driveでも可。
