# 13. OnePureStrike で公開する手順（2026-11-05 本人決定）

**決定：タペストリーは OnePureStrike で公開する。** 新しい店（StillValleyHome）は Payoneer の口座の結び付きで2週間以上止まっているため
（`docs/12`）。StillValleyHome の調査は急がず並行で続ける。

⚠ **Printify の `Publish` は Etsy で即公開。** 押したら §3 のセールまで間を空けずに進める。
⚠ **いつもの Edge（OnePureStrike のアカウント）で作業する。** InPrivate（StillValleyHome）ではない。

所要時間の目安：Printify 側 1色5分 × 4、Etsy 側 1色5分 × 4、セール5分。

---

## 0. 公開前に決まっていること

| 項目 | 内容 |
|---|---|
| 店 | OnePureStrike（ゴルフタオル9・ガーデンフラッグ5と同じ店） |
| Etsy Ads | **停止中のまま**（`garden_flag/docs/28`）。タペストリーにも広告は出ない |
| Offsite Ads | **参加中**（店全体の設定）。その経由で売れた注文だけ15%。26×36は利益$0.42、他は$7以上（下表） |
| 価格 | 定価 $35.99 / $64.99 / $92.99 / $121.99 → **30%OFF** |
| 送料 | 買い手負担（$5.59 / $6.99 / $9.29 / $9.29） |

### 30%OFF 後の利益（送料はStandard・`docs/10` §5 の実数）

| サイズ | 買い手が見る価格 | 利益（通常） | 利益（Offsite Ads 経由） |
|---|---:|---:|---:|
| 26×36 | $25.19 | $5.04 | $0.42 |
| 50×60 | $45.49 | $15.42 | $7.55 |
| 68×80 | $65.09 | $21.46 | $10.31 |
| 88×104 | $85.39 | $28.25 | $14.04 |

**サイバーセール（11/23〜12/1・40%OFF）にはタペストリーを入れない。**
40%だと 26×36 が Offsite Ads 経由で **−$2.30（赤字）** になる。

---

## 1. Printify：4色の下書きを仕上げる（1色ずつ）

```bash
start https://printify.com/app/products
```

1. 商品一覧で、タペストリーの1つ（例「Mountain Tapestry Wall Hanging, Moon and Stars…」）の**画像**を押して開く
2. 上のタブ **`Listing details`** → **Description** の中身を全部消して、その色の **`description.txt`（新版）** を貼る
   - 新版は末尾近くに **`ABOUT THE ARTWORK`**（AIの開示）がある。旧版には無い（`docs/08` §4）
   - ファイルは下のZIPの `tapestry/listing/M01_<色>/description.txt`
3. **`Mockups`** タブ：写真の四角をドラッグで並べ替えられれば、この順に：
   **寝室 → 居間 → 絵 → 寄り → サイズ → 色 → 仕様**（動かなければ §4 で Etsy 側で直す）
4. 右下の白いボタン **`Save as draft`**
5. 4色くりかえす

最新のファイル一式（説明文は新版）：

```bash
start https://github.com/golfbacca/laughing-spoon/archive/refs/heads/claude/eager-turing-ncw0ey.zip
```

## 2. Printify：公開する（4色続けて）

1色ずつ、**間を空けずに**：

1. 商品を開く → 上のタブ **`Publishing settings`**
2. 一番下 **Details to publish** の **`Tags`** に**チェックを入れる**（初期はOFF。OFFだとタグがEtsyへ送られない）
3. ⚠ **`Save as draft` は押さない**（押すと Tags のチェックが外れる）
4. 右下の黄緑のボタン **`Publish`** を押す
5. 次の色へ

**4色とも「Published」になったら、すぐ §3 へ。**

## 3. Etsy：すぐに30%OFFのセールを掛ける

```bash
start https://www.etsy.com/your/shops/me/sales-discounts
```

1. 画面中ほど「**Drive traffic and move inventory**」の右のカード **`Run a sale`** の **`Set up →`** を押す
   （「Create a sale」という表記は無かった。2026-11-06 本人の画面で確認）
2. 割引：**`Percentage off`** → **`30`**
3. 期間：**今日 〜 30日後**（Etsyの上限は30日）。終わる日をカレンダーに入れる
4. 対象：**`Select listings`**（商品を選ぶ）→ **タペストリー4つだけ**にチェック
   ⚠ 「すべての商品」にしない。タオルはセールにすると赤字になる（`garden_flag/docs/29`）
5. セール名（英字のみ）：`TAPESTRY30`
6. 保存

## 4. Etsy：1商品ずつ整える（4回）

```bash
start https://www.etsy.com/your/shops/me/tools/listings
```

商品を開いて：

| 欄 | やること |
|---|---|
| **写真** | 並びを **寝室 → 居間 → 絵 → 寄り → サイズ → 色 → 仕様** にドラッグで直す。1枚目が寝室なら検索のサムネイルはそれ |
| `Adjust thumbnails` | **触らない**（知見 §4） |
| **About this listing** | Who made it：**`I did`**（デザインは自分）／What is it：**`A finished product`**／When：**`Made to order`**。製造パートナーを聞かれたら **Printify（MWW On Demand）** を登録（AI方針・知見 §9） |
| **Category** | `Wall Hangings` の下の **`Tapestries`** があればそれ（Printifyの自動設定のままならそれでもよい） |
| **Shop section** | 新しく **`Wall Tapestries`** を作って入れる（店のページでゴルフと分かれて並ぶ） |
| **Attributes**（`Item Options` の下の方） | `Add all` のあと値を確認。素材 **Polyester**、向き **Vertical / Portrait**、部屋 **Bedroom / Living room**、色はその商品の色。**`woven` `cotton` が入っていたら消す** |
| 説明文 | 新版（ABOUT THE ARTWORK あり）になっているか目で確認 |
| タグ | 13個入っているか確認。無ければ `tags.txt` を貼る |

## 5. 確認して記録

- 4商品の Etsy のURL（スクショでよい）を送ってもらう
- セールの終わる日
- 公開日の検索順位：`mountain tapestry` / `celestial tapestry` で何ページ目か（`garden_flag/docs/27` と同じ取り方）

## メモ（2026-11-06）

セール画面の「Individual sales and offers」には **CYBER26（11/23〜12/2・40%）だけ**が予定されていた。
**ガーデンフラッグは 10/27 以降、定価 $39.99 のまま**の可能性（`garden_flag/docs/29` の「10/27 に掛け直す」が未実施）。
フラッグにも30%を掛けるなら、**別のセールで 11/22 終了**にする（同じ商品に重なるセールは掛けられないため）。本人の判断待ち。
