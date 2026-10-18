# 10. Printify に4色を登録する（下書き保存まで）

**この文書は「下書き保存」で止まる。Etsy への公開はしない。**
（⚠ Printify の `Publish` は **Etsy で即公開**になる。下書きにはならない。`docs/EtsyとPrintifyの知見.md` §2）

所要時間の目安：1色あたり15分 × 4色。2色目からは早くなる。

---

## 0. 価格の方針変更（⚠ 本人の確認待ち）

`docs/06` は**送料無料**で価格を組んでいたが、**送料は買い手負担に変える**ことを提案する。

| | 送料無料（`docs/06`） | **送料は買い手負担（提案）** |
|---|---|---|
| 検索結果の一覧に出る価格 | 26×36 で $29.99 | **$25.19**（送料は一覧に出ない） |
| サイズ別の送料が不明な問題 | 利益が送料しだいでぶれる（$8なら26×36は$1.94） | **Printifyの実費が買い手に渡るので、利益がぶれない** |
| Etsyの設定 | 送料を価格に織り込み、配送プロファイルを無料に | **Printifyが作る配送プロファイルをそのまま使う** |
| ガーデンフラッグ | — | 同じやり方（`docs/EtsyとPrintifyの知見.md` §6） |

**定価を置き、Etsyで30%OFFを掛ける**（ガーデンフラッグと同じ。上位はほぼ全件セール中・`docs/05`）。

| サイズ | **Printifyに入れる定価** | 30%OFF後（買い手が見る） | 送料$5.29なら買い手の総額 | 利益 | 率 |
|---|---:|---:|---:|---:|---:|
| 26×36 | **35.99** | $25.19 | $30.48 | **$5.09** | 20% |
| 50×60 | **64.99** | $45.49 | $50.78 | **$15.63** | 34% |
| 68×80 | **92.99** | $65.09 | $70.38 | **$21.90** | 34% |
| 88×104 | **121.99** | $85.39 | $90.68 | **$28.71** | 34% |

（利益 ＝ セール後価格 − 原価 −（セール後価格＋送料）×9.5% − $0.45。送料が$8でも利益の差は$0.3未満）

---

## 1. 準備：ファイルをPCに落とす

このブランチを丸ごとZIPで落とす（押すとダウンロードが始まる）。

```bash
start https://github.com/golfbacca/laughing-spoon/archive/refs/heads/claude/eager-turing-ncw0ey.zip
```

展開すると `laughing-spoon-claude-eager-turing-ncw0ey` というフォルダができる。使うのは：

| もの | 場所 |
|---|---|
| 入稿データ（SVG）4つ | `tapestry/source/M01_dawn.svg` ほか |
| 出品画像 7枚 × 4色 | `tapestry/listing/M01_<色>/1_bedroom.jpg` 〜 `7_details.jpg` |
| タイトル・タグ・説明文 | 同じフォルダの `title.txt` / `tags.txt` / `description.txt` |

色とフォルダの対応：

| 色 | フォルダ | 英語名 |
|---|---|---|
| 夜明け | `M01_dawn` | Dawn Pink |
| 夕暮れ | `M01_dusk` | Desert Dusk |
| 夜 | `M01_night` | Moonlit Night |
| 森 | `M01_sage` | Sage Forest |

**最初は「夜」から。** Printifyで一度試して問題が無かった色なので、詰まりにくい。

---

## 2. 商品を作る（4色くりかえす）

### 2-1. 製造元を選んで、デザイン画面を開く

```bash
start https://printify.com/app/products/241/generic-brand/indoor-wall-tapestry
```

1. ページを少し下へ。**「Select a fulfillment option」** の下の **`Choose manually`** を押す
2. **★8.3 MWW On Demand** の行の右、濃い色のボタン **`Start designing`** を押す
   ⚠ `Printify Choice` の方から入らない。注文ごとに工場が変わり、色味が揃わない（`docs/03`）

### 2-2. サイズを選ぶ

3. 右側の **`Select variants`**（白いボタン）を押す
4. 次の **4つだけ**にチェック。**横長（36"×26" など）は入れない**

   - [x] 26" × 36"
   - [x] 50" × 60"
   - [x] 68" × 80"
   - [x] 88" × 104"

5. 左の **`Print area size`** が **`13650 × 16125 px`** になっていることを確かめる
   （88×104が一番大きいので、この値になる）

### 2-3. デザインを載せる

6. 左の列のいちばん上 **`Upload`** → その色の SVG（例 `M01_night.svg`）を選ぶ
7. **灰色のふちまで絵で埋まっている**ことを確かめる。四隅に白い隙間があったら止まって画面を送る
8. 右上の白いボタン **`Preview`** を押す
9. **`Mockup color mode`** を **`Realistic (CMYK)`** にする（初期値のRGBは実物より鮮やか）
10. サイズを **`88" × 104"`** と **`26" × 36"`** に切り替えて、絵が切れすぎていないか見る
    （26×36は左右が少し切れるのが正常。月・太陽が切れていなければよい）
11. 右下の緑のボタン **`Save product`** を押す

→ 商品の編集画面（タブが並ぶ画面）に移る。

### 2-4. タイトル・説明文・タグ（`Listing details` 付近）

12. **Title** に `title.txt` の中身を貼る
13. **Description** の中身を全部消して、`description.txt` の中身を貼る
14. **Tags** に `tags.txt` の中身を貼る（カンマ区切りのまま）。**13個**になっているか見る

### 2-5. 価格（`Pricing` タブ）

15. 各サイズの **Retail price** に、上の §0 の **定価** を入れる

| サイズ | 入れる値 |
|---|---:|
| 26" × 36" | 35.99 |
| 50" × 60" | 64.99 |
| 68" × 80" | 92.99 |
| 88" × 104" | 121.99 |

16. **Profit** の列が出ていたら、その数字をスクショする（送料の扱いの確認に使う）
    ⚠ **「Pricing: Too high」と出ても無視してよい**（定価を高く置いて30%OFFにする設計のため。知見 §2）

### 2-6. 写真（`Mockups` タブ）

17. **`Deselect all`** を押して、Printifyの既製モックアップの選択を全部外す
18. **`⬆ Upload`** を押し、その色のフォルダの **`1_bedroom.jpg` 〜 `7_details.jpg`** の7枚を選ぶ
19. **`1_bedroom.jpg` に `★ Primary` を付ける**（検索結果のサムネイルになる）
20. 選択数が **7** で、既製の写真が混ざっていないことを確かめる

⚠ 写真の並びは**アップロードが終わった順**になる（ファイル名順ではない）。Etsy側で公開後に直す。

### 2-7. 保存（ここで止まる）

21. **`Save as draft`**（下書き保存）を押す
    ⚠ **`Publish` は押さない。** Etsyで即公開になる

**`Publishing settings` の `Tags` のチェックは、今は触らなくてよい。**
`Save as draft` で外れてしまうので、**公開する直前に入れる**（知見 §2）。

---

## 3. 下書きを作ったら、確かめてほしいこと（1色ぶんでよい）

### 3-1. 送料

Printifyの商品画面か、`Pricing` タブに **サイズ別の送料（Shipping）** が出ていればスクショ。
出ていなければ、下のURLの **`Shipping`** 欄を開いてスクショ。

```bash
start https://printify.com/app/products/241/generic-brand/indoor-wall-tapestry
```

### 3-2. 吊り具（hanging hardware）が付くか

商品ページの **`About`** や **`Key features`** に、`grommets`（ハトメ）・`hooks`（フック）・
`hanging kit` などの語があるか見る。**どこにも無ければ「付かない」と判断して説明文のままでよい。**

確証が欲しければ、Printifyのサポート（画面右下の吹き出し）に次の1通を送る（**500字以内**・知見 §1）：

```
Hello. For the Indoor Wall Tapestry (product 241) made by MWW On Demand, does the tapestry ship with any hanging hardware, such as grommets, hooks, or a rod? Or is it the fabric only, with hemmed edges? I need to describe it correctly to my customers. If you cannot confirm this, please say so directly. Thank you.
```

> 〔訳〕MWW On Demand製造の Indoor Wall Tapestry（商品241）には、ハトメ・フック・棒などの吊り具が付きますか。
> それとも縁を縫っただけの布のみですか。買い手に正しく説明したいので教えてください。
> **確認できない場合は、はっきりそう言ってください。**

最後の1文は知見 §1 の「人間に回す言い方」。ボットに「分かりません」と白黒つけさせる。

---

## 4. このあと（別の文書で出す）

- Etsy側：カテゴリ・属性（Attributes）・写真の並び替え
- 公開：`Tags` にチェック → `Save as draft` を挟まず `Publish` → **すぐ30%OFF**
- 広告

**4色ぶんの下書きができたら、1色の編集画面のスクショ（各タブ）を送ってほしい。**
抜けがないかをこちらで見る。
