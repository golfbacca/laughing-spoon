# ONE PURE STRIKE — Etsyゴルフタオル店

三原誠司さん（63歳・ゴルフ歴40年）の副業。ベテランゴルファーの自虐をテーマにしたPODタオルを
Etsyで販売している。デザインの元ネタは全部ご本人の実話（2005年からベスト未更新、練習に数百万円）。

**詳しい経緯・全手順は [HANDOFF.md](HANDOFF.md) を読むこと。**

> このファイルは元々 `C:\Users\bangd\claude-test\CLAUDE.md` にあったもの。
> 2026-09-16 にリポジトリへ取り込んだ。人物像・作業スタイルなど全案件に共通する部分は
> リポジトリルートの `CLAUDE.md` に切り出してある。

---

## 相手のこと

- **英語が苦手**。英語のコピーは必ず日本語訳と語感の解説を添える
- **PC操作の指示は1クリック単位で**。ボタンの色・位置・文言まで書く（本人の言葉:「バカでも分かるように細分化して」）
- PowerPoint/Outlookのマクロは得意。その領域は説明を省いてよい
- **パスワード入力・支払い・OAuth許可・金融口座の操作は必ずご本人**。こちらは代行しない
- デザインの違和感を鋭く指摘してくる。「なんとなく変」ではなく**実測で白黒つける**と喜ばれる

## 環境の制約（重要・最初に読む）

ブラウザ操作は**ほぼ全滅**しているので、Etsy/Printifyの操作は**本人に手順を出す**のが基本。

| 手段 | 状態 |
|---|---|
| アプリ内ブラウザ（mcp__Claude_Browser__*） | **printify.comで2回連続クラッシュ**。使わない |
| Chrome拡張（mcp__claude-in-chrome__*） | printify.com・etsy.com とも「Navigation to this domain is not allowed」 |
| PowerShellでEtsyをfetch | DataDomeが403で弾く。ただし `i.etsystatic.com` のCDN画像は取得可 |
| Chrome拡張でgemini.google.com | **使える**（画像生成で実績あり） |

→ 画像や入稿データは**ローカルで生成**し、アップロードだけ本人にやってもらう。この型で9商品を出品済み。

## 現状（2026-08-10時点）

- **9商品すべて公開中**。全て $19.99、写真7〜8枚付き
- ショップ: onepurestrike.etsy.com / 売上はまだ0件
- 入金経路は開通済み（Etsy → Payoneerウォレット → 三菱UFJ銀行の円口座）
- 委託生産パートナー申告・生成AI申告・属性入力とも完了。規約面はクリーン

## 資産の場所

```
C:\Users\bangd\claude-test\          ← スクリプトと文言（このフォルダ）
C:\Users\bangd\Downloads\Golf Towel\ ← 入稿データ  <TAG>_upload_5043x7350.png
  ├ listing_images\                  ← P08/P15/P20の出品画像＋モックアップ原本
  ├ listing_images_p01\ 〜 _p12\     ← 各商品の出品画像7枚
  ├ listing_images_personalized\     ← パーソナライズ版8枚
  └ personalized\                    ← 年号別の入稿データ
C:\Users\bangd\Downloads\P01_raw.png 〜 P20_raw.png  ← Gemini生成の原本
```

## ツール

| スクリプト | 用途 |
|---|---|
| `make_year_towel.py <年>` | 任意の年号の入稿データを生成（パーソナライズ受注時に使う） |
| `year_mockup.py` | タオル写真に任意の年号を合成 |
| `make_towel_listing_images.py <TAG>` | **汎用**。商品写真＋出品画像7枚を生成 |
| `prepare_designs.py` | P01/02/03/12の修正＋入稿データ生成 |
| `rebuild_p17.py` / `rebuild_p20_dimples.py` | 各デザインの破綻修正（再生成用） |

Pillow 12を使用（`ImageMath.eval`は廃止、`lambda_eval`を使う）。numpyは入っていない。

## 定型手順

**新規出品**: デザイン修正 → `<TAG>_upload_5043x7350.png` 生成 → `make_towel_listing_images.py <TAG>`
→ 文言を書く → Printifyで既存商品を複製してデザイン差し替え → 公開 → Etsyで写真7枚を差し替え → 公開

**Etsyの写真差し替え**: 新しい7枚を**1枚ずつ順番に**追加（まとめて選ぶと順序が崩れる）→ 古い写真を削除 → 公開

**パーソナライズ注文が来たら**: [personalized_order_runbook.md](personalized_order_runbook.md) を見る。
Printifyの「Review needed」に入るので放置すると発送されない。**初回は必ず画面を一緒に確認する**。

## やってはいけないこと

- アプリ内ブラウザでprintify.comを開く（クラッシュする）
- Etsyの写真をまとめて複数選択でアップロード（順序が崩れる）
- 部分的な画像差し替えで境目をぼかす（新旧が二重に見える）
- 明暗マップの平滑化半径を模様の周期より小さくする（古い模様が転写される）
