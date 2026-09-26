# 26. Printifyドラフト5件の埋め残しと修正（2026-09-24）

本人が5商品ともPrintifyにアップし、ドラフトのまま画面を送ってくれた。
**5枚の画面を読んで、埋め残し・既定値のまま・事故になる箇所を特定した記録。**

作業の順番と1クリック単位の手順は本文のとおり。
**Printifyの設定変更はすべて本人が行う**（こちらは代行しない）。

---

## 0. まとめ（5商品の状態）

| 商品 | タグ | 名入れの文 | 価格 | Tags同期 | 文字数上限 | 特記 |
|---|---|---|---|---|---|---|
| R01 まだ練習中（黄ギンガム） | 13/13 ✓ | ✓ | 既定 | **✗ OFF** | 13 | — |
| R02 19番ホール（緑） | 13/13 ✓ | ✓ | 既定 | **✗ OFF** | 13 | **⚠ 複数商品リスティングに入っている** |
| R05 マリガン（生成り・花） | 13/13 ✓ | **✗ Printifyの既定文のまま** | 既定 | **✗ OFF** | 13 | — |
| R09 ゴルフ中（タータン） | 13/13 ✓ | ✓ | **24.5×32が $42.38** | **✗ OFF** | 13 | 「Pricing: Too high」表示 |
| R11 ゴルフ倶楽部（紺） | 13/13 ✓ | ✓ | 既定 | **✗ OFF** | 13 | — |

**できている点**（直す必要なし）：
タイトル5件とも `docs/21` どおり ／ タグ13個とも入っている ／
**12"×18" と 24.5"×32" の両サイズが選択済み** ／ 名入れスイッチON ／
説明文は入っている（ただし後述の1か所だけ差し替えが要る）。

---

## 1. ⚠ 公開前に必ず潰す（放置すると事故）

### A. 「Tags」の同期がOFF（5商品とも）

`Publishing settings` タブ → 一番下 **Synced product details** の中で、
**`Tags` だけチェックが外れている。**

Printify側に13個入っていても、**このチェックが外れているとEtsyへ送られない。**
`Listing health` が「13/13 tags added ✓」と出るので気づきにくい。

→ **チェックを入れる。** これで `docs/22` §2-9 のEtsy側でのタグ貼り付け作業が丸ごと不要になる
（カンマで分割されるか不明という不安も消える）。

### B. R05 の名入れ説明文が Printify の既定文のまま

いま入っているのは：
> Please add only the text you want printed on your product. Reach out to us directly for any additional requests.

これは **Printifyが勝手に入れた汎用文**で、「名字を入れてください」と言っていない。
このまま公開すると、**買い手が何を打てばいいか分からず、空欄や長文が来る。**

→ 他4商品と同じ文に差し替える（第2節に貼り付け用の文がある）。

### C. R02 が「複数商品リスティング（Multi-Product Listing）」に入っている

R02の画面の上に青い帯が出ている：
> This product is included in one or more Multi-Product Listings.
> Changes to mockups, variants, or pricing will apply there as well.
>
> （この商品は複数商品リスティングに含まれています。
> 　モックアップ・バリエーション・価格の変更は、そちらにも反映されます）

**5案は1案ずつ別リスティングで出す設計**（`docs/18` の広告で案ごとのクリック率を比べるため）。
グループに入ったままだと、**価格変更が意図しない別商品に波及する**か、
**Etsy側で1つのリスティングにまとめられる**おそれがある。

→ 帯の右の **「View Multi-Product Listings」** を押して、中身を確認してほしい。
**何が入っているかを教えてもらえれば、外すべきかどうか判断する。**
（R09の 24.5×32 だけ価格が $42.38 になっているのも、これが原因の可能性がある）

---

## 2. 5商品すべてに入れる値

### 2-1. 価格（`Pricing` タブ）

| サイズ | いま | **入れる値** | 原価 | Etsy手数料 | 利益 | 率 |
|---|---:|---:|---:|---:|---:|---:|
| 12" × 18" | $22.99 | **39.99** | $10.49 | $4.86 | **$24.64** | 62% |
| 24.5" × 32" | $34.99（R09は$42.38） | **74.99** | $20.44 | $8.18 | **$46.37** | 62% |

入れたあと **Profit の列がこの数字になっていれば正しい。**

**⚠ これは定価。** Etsy側で **30%OFF のセール**を掛けて、
買い手に見える値段は **$27.99 / $52.49** になる（`docs/16`・`docs/25`）。

セール後の実際の利益：

| | 表示 | 利益 | 率 |
|---|---:|---:|---:|
| ガーデン 12×18 | $27.99 | **$13.78** | 40.1% |
| ハウス 24.5×32 | $52.49 | **$26.01** | 44.2% |

**「Pricing: Too high ⚠」が5商品とも出るが、無視してよい。**
Printifyは**市場の中央値（$22.74・`docs/12`実測）と比べているだけ**で、
セール価格を知らない。こちらは「定価を高く置いて常時30%OFF」という設計なので、
**買い手に見える $27.99 は中央値のすぐ上。**警告は的外れ。

### 2-2. 名入れ（`Personalization` タブ）

**Personalization instruction for buyers** に入れる文（5商品とも同じ）：

```
Enter your family name - for example: SMITH
We print it as "THE SMITHS". Longer names simply print a little smaller.
```

> 名字を入力してください（例：SMITH）。「THE SMITHS」と印刷します。
> 長い名字はその分だけ小さく印刷されます。

**115字（上限120字）。**

**Character limit for buyer response：`13` → `16` に変える。**

理由：買い手が打つのは名字だけで、こちらが `S` を足す。
**16字なら印刷されるのは最大17字。** 実在する長い名字は14字
（`CHRISTOPHERSON` / `SCHWARZENEGGER`）までなので**16で実質すべて通る。**

13のままだと14字の名字が弾かれる。逆に上限を外すと
`THE SMITH FAMILY EST 2015` のような一文を打たれて極端に小さくなる。
**16は「名字以外は打てない」と伝わる長さ。**（実測は `docs/21` 第7節）

**以前の `Any length fits.`（長さの制限はありません）は使わない。**
Printifyは上限欄が必須なので、**制限を入れながら「制限はない」と書くのは矛盾になる。**

### 2-3. 説明文（`Listing details` タブ）

いまの2行目が **`12 x 18 inches`** とだけ書いてあり、
**24.5×32 を売るのに 12×18 しか書いていない状態**になっている。
（下の WHAT YOU GET には両サイズが書いてあるので、文中で食い違っている）

冒頭の2行だけ差し替える。→ 全文は `docs/21` 第6節。

**前：**
```
Personalized golf garden flag with your family name on it. Double-sided,
12 x 18 inches, and made to live outdoors. A golf gift that actually gets used.
```
**後：**
```
Personalized golf garden flag with your family name on it. Double-sided and
made to live outdoors. Pick the garden size 12 x 18 in, or the big house flag
24.5 x 32 in. A golf gift that actually gets used.
```

> 名字を入れられるゴルフ・ガーデンフラッグ。両面印刷、屋外用。
> **ガーデンサイズ 12×18インチか、大きいハウスフラッグ 24.5×32インチを選べます。**
> 本当に使われるゴルフの贈り物。

`Pick`（選んでください）は `Available in`（〜があります）より**買い手に決めさせる語**で、
2サイズあることを「選択肢」として前に出せる。
`the big house flag`（大きいハウスフラッグ）と **big を足したのは、
24.5×32 という数字だけでは米国の買い手も大きさを実感できない**ため。

同じ節の中の1行も直してある：

| 前 | 後 |
|---|---|
| `Any name fits - longer names simply print a little smaller.` | `Longer names simply print a little smaller - they still fit.` |

（16字の上限を入れたので「どんな名前でも入る」とは言えなくなった。
`they still fit`（それでも収まります）を後ろに置いて、**不安だけ先に消す語順**にしてある）

### 2-4. 写真（`Mockups` タブ）

いま **11/20 selected**。ここに並んでいるのは **Printifyの既製モックアップ20枚**で、
**こちらが作った出品画像40枚はこの画面に出てこない**（Printifyは存在を知らない）。

このまま公開すると **Etsyに11枚の既製写真が送られる。**
既製モックアップは競合と同じ絵になるので、**こちらの8枚だけを送りたい**（`docs/15` の指摘☆9）。
（※ここに「Etsyの写真枠は10枚」と書いていたのは誤り。**実際は20枚**。2026-09-26訂正）

#### ✅ 確定：Printifyの「Upload」にこちらの8枚を入れる（R01で実証・2026-09-24）

`Mockups` タブのタイルの中の **「⬆ Upload」** に、
**こちらの出品画像を入れられることを本人がR01で確認した。**

**これでEtsy側の写真作業が丸ごと消える。**

| | 既製を1枚残す案（没） | **Upload（採用）** |
|---|---|---|
| Etsyでの写真作業 | 1枚消して8枚アップ × 5商品 | **なし。目視確認だけ** |
| 再公開したとき | Etsy側の写真が既製品に戻る | **こちらの8枚が送り直される** |
| `Mockups` の同期チェック | 公開後に外す必要あり | **入れたままでよい** |
| 並び順とサムネイル | Etsyでドラッグして調整 | **Printify側のPrimaryで決まる** |

出品画像は **2000×1500px（4:3）** で、**Etsyの推奨サイズそのもの**。

**⚠ 前言撤回：`Mockups` の同期チェックは外さない。**
以前このファイルに「公開後に外す」と書いたが、それは
**Etsyに手で上げた写真を守るため**の話だった。
**こちらの8枚がモックアップそのものになった**ので、外す理由が消えた。
むしろ**入れたままにしないと、再公開でこちらの写真が送られない。**

#### 手順（残り4商品ぶん・1商品あたり2分）

1. 商品を開く → **`Mockups`** タブ
2. **「Deselect all」**（既製11枚の選択を外す）
3. **「⬆ Upload」** → `listing/<商品フォルダ>/` の **1〜8を番号順**に
4. **`1_main.jpg` に `★ Primary` を付ける**（検索結果のサムネイルになる）
5. 選択数が **8** になっていること、既製が混ざっていないことを確認

商品フォルダ：

| 案 | フォルダ |
|---|---|
| R01 まだ練習中 | `listing/R01_still-working-on-it/` |
| R02 19番ホール | `listing/R02_19th-hole/` |
| R05 マリガン | `listing/R05_mulligans/` |
| R09 ゴルフ中 | `listing/R09_gone-golfing/` |
| R11 ゴルフ倶楽部 | `listing/R11_members-only/` |

#### ⚠ 出品画像は7枚ではなく8枚（2026-09-24 本人の指摘で判明）

本人の指摘：**「listing_house にある『TWO SIZES』は入れなくてよい？」**

**入れないと駄目だった。** `docs/22` は「1〜7を番号順に」と書いていたが、
その7枚目までに入っていたサイズ図は **12×18だけの図**で、
**24.5×32を売っているのに存在が写真に出ない**状態だった。

2サイズ併記の図は `listing_house/` という**別フォルダに置いたまま**で、
番号も振っていなかったため、手順書から漏れた。**フォルダの作りが原因。**

→ **番号を振り直して商品フォルダに入れた。** `listing_house/` は廃止。

| 番号 | ファイル | 中身 |
|---|---|---|
| 1 | `1_main.jpg` | 庭に立てた主画像（**検索結果のサムネイル**） |
| 2 | `2_personalize.jpg` | 名入れの説明 |
| 3 | `3_scene.jpg` | 設置シーン |
| 4 | `4_closeup.jpg` | 生地の拡大（`100% POLY POPLIN-CANVAS`） |
| **5** | **`5_two_sizes.jpg`** | **2サイズ併記（新）。どちらを買うかの判断材料** |
| 6 | `6_size_12x18.jpg` | 12×18の寸法図。**袖2インチの注記**が入っている |
| 7 | `7_double_sided.jpg` | 両面印刷 |
| 8 | `8_flag_only.jpg` | **スタンド別売りの注意書き**＋お手入れ |

**5と6は両方要る。** 5はサイズ選択の判断、6は袖2インチ（＝スタンド別売り事故の予防）で、
役割が違う。Etsyの枠は10枚なので削る必要もない。

### 2-5. 触らなくてよいもの

| 項目 | いまの値 | 判断 |
|---|---|---|
| Shipping profile | Automatically assign and update… | **そのままでよい。** 公開後にEtsy側で $6.39 / $1.99 になっているか確認する |
| Variant visibility | Only show in stock variants… | 両サイズとも在庫ありなので影響なし |
| Hide in store | OFF | そのまま |
| タイトル | `docs/21` どおり | そのまま |
| タグ13個 | 入っている | そのまま（第1節Aのチェックを入れるだけ） |

---

## 3. 入稿データの確認（1商品だけでよい）

**7800×10012 の `house/` 版を載せたかどうか**を確認したい。
3900×5700 の方を載せていると、**24.5×32 で上下が各2.31インチ切れる**（`docs/25` 第4節）。

1. 右上の黒いボタン **「Edit design」** を押す
2. 左の **「Uploads」** タブを開く
3. 使っている画像のファイル名の下に出ている**寸法**を見る

→ **`7800 × 10012` なら正しい。** `3900 × 5700` なら差し替えが要る。
ファイルは `garden_flag/upload/house/` にある（例 `R09_SMITHS_house_7800x10012.png`）。

---

## 4. ハウスフラッグの検索語は、いまは狙わない（判断の記録）

タイトルに `House Flag` を足す案を検討したが、**今回は入れない。**

理由：**出品画像7枚のうち6枚がガーデンサイズの写真**で、
ハウスフラッグのモックアップがまだ無い（`docs/25` 第3節）。
`golf house flag` で来た人が**ガーデンの写真ばかりの画面に着地すると、見ずに戻る。**

`docs/04` の診断どおり、いまの課題は**リスティング品質スコアを育てること**。
**転換しない流入を増やすのは、そのスコアを直接下げる。**

→ **ハウス用のモックアップを作ってから、タイトルとタグに入れる。**
そのとき差し替える候補は `double sided flag`（機能語で検索されにくい）→ `golf house flag`。


---

## 5. R02の画面で確認したこと（2026-09-24）

本人が5商品とも設定を入れ終え、R02の画面を送ってくれた。

### 合っていた（実測で確認）

| 項目 | 画面の値 | 判定 |
|---|---|---|
| 12"×18" | $39.99 → Profit **$24.64（62%）** | ✅ 予測と1セント一致 |
| 24.5"×32" | $74.99 → Profit **$46.37（62%）** | ✅ 同上 |
| 文字数上限 | 16 | ✅ |
| 説明文 | `Pick the garden size 12 x 18 in, or the big house flag 24.5 x 32 in.` | ✅ |
| モックアップ | 8枚・全部こちらの画像・Primaryは `1_main` | ✅ |
| 複数商品リスティングの帯 | 消えた | ✅ |

**手数料の式 `買い手総額 × 9.5% + $0.45` は3回目の検算でも一致。** 採算計算は確定とみなす。

### ⚠ 名入れの説明文が旧版のまま

文字数カウンタが **`96 / 120`**。文字数を数えたところ：

| | 文字数 |
|---|---:|
| 旧（`Any length fits.` 版） | **96字** ← 入っているのはこれ |
| 新（2026-09-24版） | 116字 |

**上限を16にしたのに、文面は「長さの制限はありません」のまま。** 矛盾が残っている。
→ 第2-2節の文に差し替える。R05はさらに別（Printifyの既定文）なので同様に。

### ⚠ 写真の並び順が入れ替わる

8枚まとめてアップすると、**アップロード完了順に並ぶ**らしい。
ファイル名は1〜8なので、名前順ではない。R02の実際の並び：

| 位置 | 入っていた画像 | 本来 |
|---:|---|---|
| 1 | `1_main` | ✅ |
| 2 | `6_size_12x18` | `2_personalize` |
| 3 | `5_two_sizes` | `3_scene` |
| 4 | `8_flag_only` | `4_closeup` |
| 5 | `4_closeup` | `5_two_sizes` |
| 6 | `7_double_sided` | `6_size_12x18` |
| 7 | `2_personalize` | `7_double_sided` |
| 8 | `3_scene` | `8_flag_only` |

**サムネイル（1枚目）は正しいので致命傷ではない。**
ただし2枚目が寸法図面、**名入れの説明が7枚目**。
1ページ目の83%が名入れ商品という市場（`docs/12`）で、**一番の売りが一番見られない位置**にある。

対処は未確定。**PrintifyでドラッグできるかをR02で試す。**
できなければ1枚ずつ順にアップし直すか、Etsy側で並べ替える。

### ⚠ Tags の同期チェックが保存されない

本人の報告：**チェックを入れて `Save as draft` を押し、開き直すとまた外れている。**

→ **`Publish` を押す直前にチェックを入れ、`Save as draft` を挟まずそのまま `Publish`。**
公開後、Etsy側でタグが13個入ったかを必ず目で確認する。
入っていなければ `docs/21` のカンマ区切りのタグ行をEtsyに貼る。

### ~~次の一手：R02を1商品だけ先に公開する~~（本人の提案で変更。下の第6節へ）

こちらからPrintifyもEtsyも見えないため、以下が確かめられない。
**1商品だけ出せば、事故っても1件で済む。**

| 確かめること | なぜ重要か |
|---|---|
| **Etsyで「下書き」になるか「即公開」か** | 即公開だと**30%OFFを掛ける前**に $39.99 のまま棚に出る |
| Printifyの写真順がEtsyにそのまま行くか | 行くなら**Etsy側でドラッグして直せる** |
| タグが13個入ったか | 同期チェックが効いたかの確認 |
| 名入れが「必須（Required）」になっているか | 任意だと空欄注文が来る |


---

## 6. 挙動の確認は「捨てられるテスト品」でやる（2026-09-24・本人の提案）

本人の提案：**「今回のシリーズではなく、別の商品をテストで作って出してみたら分かるんじゃない？」**

**こちらの案（R02を1つだけ先に出す）より良い。** 採用する。

| | R02を先に出す（没） | **テスト品を出す（採用）** |
|---|---|---|
| 5商品の公開日 | **ずれる** | **そろう** |
| 即公開された場合 | $39.99のまま本番が棚に出る | **捨てればいい** |
| コスト | $0 | **出品料 $0.20** |

**5商品の公開日がそろうことが重要。** ずれると広告の開始日がばらけて、
`docs/18` の30日テストで案ごとのクリック率を比較できなくなる。

### テスト品に必要な設定（これが無いと答えが出ない）

| 確かめること | テスト品に要る設定 |
|---|---|
| Etsyで下書きか即公開か | なし（どの商品でも同じ） |
| **写真の並び順**がPrintifyのまま行くか | **自分でアップした画像が複数枚**必要。既製モックアップのままでは分からない |
| **Tagsの同期**が効くか | タグを数個 ＋ `Publishing settings` の `Tags` にチェック |
| **名入れが「必須」**になるか | `Personalization` をON |

写真は `listing/R01_still-working-on-it/` の8枚をそのまま流用してよい。

### その前に：設定を見れば実験なしで分かるかもしれない

```
https://printify.com/app/account/connections
```

接続中のEtsyストアの設定に、**新商品を下書きで出すか即販売開始かの切り替え**があるはず。
`Publish as draft` / `Make products visible` のような文言を探す。
**あれば、一番リスクの大きい疑問は実験なしで消える。**

### 使うテスト品

本人が既に持っている **「Garden & House Banner | Generic」**
（ゴルフタオルの `STILL CHASING ONE PURE STRIKE` を載せたもの）。
既製モックアップ10枚・**タグ0個**・価格はPrintify既定（$22.99–42.38）。

### 段取り

1. 上の接続設定を探す
2. `Listing details` → タグを3つ。**`zztest one` / `zztest two` / `zztest three`**
   （`zz` で始めるのは**Etsy側で入ったか一目で分かる**ようにするため）
3. `Mockups` → `Deselect all` → `⬆ Upload` で
   `listing/R01_still-working-on-it/` の1〜8を番号順。Primaryは `1_main`
4. `Personalization` をON（文面は何でもよい）
5. `Publishing settings` の **`Tags` にチェック** → **`Save as draft` を挟まず即 `Publish`**
   ⚠ **価格は触らない**（テスト品なので既定のまま）
6. Etsyで確認：**下書きか販売中か／写真の並び／`zztest` タグが入ったか／
   名入れが必須か／画像がにじんでいないか**
7. 確認後、Etsyで **`Deactivate`**（削除より先に無効化。戻せる）

### 副産物：「Pricing: Too high」は無視してよいと確定した

このテスト品は **Printifyの既定価格のまま（$22.99–42.38）なのに
「Pricing: Too high」が出ている。**

| 商品 | 24.5×32の価格 | 警告 |
|---|---:|---|
| R01 / R02 / R05 / R11（既定） | $34.99 | Pricing: Good |
| R09（既定） | $42.38 | **Too high** |
| テスト品（既定） | $42.38 | **Too high** |
| R02（$74.99に変更後） | $74.99 | **Too high** |

**閾値は $34.99 と $42.38 の間にある。** こちらの価格設定とは無関係に、
**上のサイズの金額だけで機械的に出る警告。** 無視してよい。

**コストは出品料 $0.20。** 消しても返らないが、4つの疑問が潰せるなら安い。


---

## 7. テスト公開の結果（2026-09-26）

テスト品「Garden & House Banner」に R01の8枚・タグ3つ・名入れONを入れて公開した。
**4つの疑問すべてに答えが出た。**

| 疑問 | 結果 |
|---|---|
| **Etsyで下書きか即公開か** | **★即公開。`Active` / Listed on Sep 26, 2026** |
| 写真8枚が届くか | **届いた**（"Add photos 12 remaining" → 20−12＝8） |
| 写真の並び順 | **1枚だけずれる。`2_personalize` が最後尾** |
| **Tagsの同期** | **効いた。** `zztest one / two / three` が3つとも入った |
| 名入れ | **`Required` になっている。** 文面もPrintifyのものがそのまま届く |
| 価格・在庫 | 両サイズ届いた（$22.99 / $42.38・qty 999・Visible） |
| カテゴリ | Printifyが **`Banners & Signs`** を設定 |

### Etsyに届いた写真の順（テスト品の実測）

`1_main` → `3_scene` → `4_closeup` → `5_two_sizes` → `6_size_12x18`
→ `7_double_sided` → `8_flag_only` → **`2_personalize`（最後尾）**

**`2_personalize` だけが後ろに回る。** 他は番号順。
→ **Etsy側で2番目へドラッグして直す**（1商品1ドラッグ）。

### 訂正：Etsyの写真枠は20枚（10枚ではない）

画面に **"Add up to 20 photos and 2 videos"** と出ている。
このファイルの第2-4節に「10枚」と書いていたのは誤り。訂正済み。
**こちらの8枚だけを送る方針は変わらない。**

### サムネイルの `Adjust thumbnails` は触らない

Etsyは**1枚目の写真を正方形・縦長・横長に切ってサムネイルにする。**
`Adjust thumbnails` のスライダーを右に振ると**「THE SMITHS」の文字だけのアップ**になり、
検索結果で旗に見えなくなる。**`Cancel` で閉じること。**

初期状態で問題ないことを実測した。**5案とも正方形に切って旗が丸ごと収まり、
決め台詞の行まで読める**（R02の `19TH HOLE - ALWAYS OPEN` だけ下端ぎりぎり）。

### 即公開だと分かったので、公開の段取りを変える

**Printify側（公開前）**

1. 名入れの文面を5商品とも新版に（R05はPrintifyの既定文なので特に）
2. **`Tags` にチェック → `Save as draft` を挟まず即 `Publish`**
3. **5商品を続けて公開する**（間を空けない）

**Etsy側（直後・5〜10分以内）**

4. Marketing → Sales and discounts → **30%OFF、この5商品だけ** → 表示 $27.99 / $52.49

⚠ この間は定価 $39.99 / $74.99 のまま棚に出る。ただし
**いまの店はEtsy検索からの流入がゼロ**（`docs/04`）で広告も未開始なので実害はほぼ無い。

**各商品で（1商品2分）**

5. `Photo & Video` で **「YOUR FAMILY NAME ON IT」を2番目へドラッグ**
6. `Item Details` のカテゴリ → `Change` → `garden flag` で検索。
   より具体的なカテゴリがあればそちらへ。無ければ `Banners & Signs` のまま
7. `Item Options` の属性提案 → `Add all` のあと**値を目で確認**
   （AIの推測なので素材が違うことがある。正しくは **Polyester**）

### 未確認のまま残るもの

| # | こと | 影響 |
|---|---|---|
| 1 | 文字数上限16がEtsyに届いたか | Etsyの名入れ欄に文字数が表示されない。公開後に鉛筆アイコンで確認 |
| 2 | 再公開したとき写真の並びが戻るか | 戻ったら再度ドラッグ |

---

## 8. Publish が失敗した（2026-09-26・原因未特定）

本番商品で `Publish` を押したところ：

> Sorry, we couldn't publish this product. Please try again later or get in touch
> with support if the issue reoccurs.

**Printifyの汎用エラーで、文面から原因は分からない。**
数分前にテスト品は同じ店・同じ接続で成功している。

### 切り分けの順番

| # | やること | 分かること |
|---|---|---|
| 1 | **先にEtsyの商品一覧を見る** | ⚠失敗表示でもEtsy側に出来ていることがある。出来ているのに再Publishすると**重複＋出品料2回** |
| 2 | Printifyの商品一覧（`Back to My Products`）でカードの表示を見る | トーストより詳しい理由が出ることがある |
| 3 | 3分待って再 `Publish` | エラー文が `try again later` なので一時的な不具合の可能性。立て続けの作成はEtsy API側で弾かれることがある |
| 4 | **`Tags` のチェックを外して `Publish`** | 通ればタグが原因。テスト品はタグ3つで成功、本番は13個 |
| 5 | Etsy接続を繋ぎ直す（`printify.com/app/account/connections`） | 接続が原因かどうか。⚠OAuth画面は必ず本人が操作 |

### 最初に知りたい3点

1. どの商品で出たか
2. Etsyにその商品は出来ていたか
3. **他の4つでも同じエラーが出るか**

3が「1つだけ失敗」ならその商品固有（文言か画像）、
「全部失敗」なら接続かEtsy側。切り分けの効率が大きく変わる。

### 切り分けの結果（2026-09-26）

本人の報告：**5商品すべて失敗。Etsyには1件も出来ていない。**

こちら側で文言を機械検査した（`docs/21` の内容をEtsyの上限と照合）：

| 検査 | 結果 |
|---|---|
| タイトル5件 | 120〜127字（上限140） **OK** |
| タグ | 5件とも13個・最長18字（上限20） **OK** |
| 説明文 | 2,038字（上限13,000） **OK** |
| 名入れ説明 | 116字（Printify上限120） **OK** |
| 使用文字 | **全部ASCII。** Etsyが弾く文字なし |

**→ 商品の中身は原因ではない。**

次の3つが揃っているので、**Printify↔Etsyの通信側**と判断する：
1. 5件すべて同じエラー
2. Etsy側に1件も作成されていない
3. **十数分前に、同じストア・同じ接続でテスト品が公開に成功している**

### やる順番（改訂）

| # | やること |
|---|---|
| 1 | **30分待って1商品だけ再 `Publish`。** Etsyに何も出来ていないので重複の心配はない（毎回Etsy側は確認する） |
| 2 | **1商品だけ `Tags` を外して `Publish`。** テスト品はタグ3個で成功、本番は13個。数の差だけが未検証 |
| 3 | **Printifyサポートへ**（下に英文あり）。こちらからもEtsyからも見えないログを持っている |

### ⚠ Etsyストアの `Disconnect` は押さない

前に「繋ぎ直す」と書いたのは**取り消す。**
Printifyでストアを切断すると**公開中の商品の紐付けが外れる。**
いま**ゴルフタオル9商品が公開中**なので巻き込む危険がある。
**サポートに確認してから。**

### サポートに送る英文

```
Hello,

I cannot publish any of my products to my Etsy store. All 5 fail with the
same message:

"Sorry, we couldn't publish this product. Please try again later or get in
touch with support if the issue reoccurs."

Details:
- Etsy store: OnePureStrike
- Date/time: 26 Sep 2026, around 21:30 JST (UTC+9)
- Product type: "Garden and House Banner" by Pic The Gift,
  2 variants (12x18 and 24.5x32)
- All 5 products fail. Nothing is created on the Etsy side.
- A test product published successfully about 15 minutes earlier,
  from the same store and the same connection.

Could you check the API response you are receiving from Etsy for these
publish attempts? The on-screen message does not tell me what is wrong,
and I would rather not keep retrying and risk creating duplicate listings.

Thank you.
```

**狙い**：`All 5 fail / Nothing is created on the Etsy side` で切り分け済みを先に示し、
`A test product published successfully ... same connection` で**接続は生きている**と証明する。
これで1次対応の「再試行してください」「再接続してください」を両方先回りで潰せる。
`Could you check the API response you are receiving from Etsy` は
**サポートにしかできない作業を名指しで頼む**言い方。

（サポートの回答が来たらここに追記する）

### 再試行も失敗。「新規作成が止められている」線が出てきた（2026-09-26）

30分待って再 `Publish` → 確認ダイアログ `Sync and publish changes?` が出て
`Confirm` → **`Publishing` 状態になったあと、同じエラーで失敗。**

`Publishing` まで進むということは、**Printifyは要求を受け付け、EtsyのAPIを叩いて
そこで蹴られている。**

タグも機械検査した：5案とも**13個・最長18字・重複なし・空なし**。
**文言はこれで完全に除外。**

#### 見落としていた点

確認ダイアログに **`Republishing will not impact SEO ranking`** とある。
**「再公開」という語が出るのは、既にEtsyと紐付いている商品。**

| | 操作の中身 | 結果 |
|---|---|---|
| テスト品 | **既存リスティングの更新**だった可能性 | 成功 |
| 本番5商品 | **新規リスティングの作成** | 全部失敗 |

**テスト品の成功は「新規作成ができる」証明になっていなかったかもしれない。**
もしそうなら、**Etsy側で新規リスティングの作成だけが止まっている。**
それを止める原因はほぼ支払い関係。

#### 確認すること（無料・1分）

| # | 見るところ | 何を見るか |
|---|---|---|
| 1 | `etsy.com/your/shops/me/finances/payment-account` | **`Amount due` に未払いがないか。** Etsyは請求が滞ると新規出品を止める。テスト品の出品料$0.20が計上された時点で弾かれた、という筋は時系列が合う |
| 2 | `etsy.com/your/shops/me/dashboard` | 画面上部の**赤/オレンジの警告帯** |
| 3 | 本人の記憶 | **テスト品は今日が初公開だったか。** 初めてなら新規作成は通っていたことになり、1の線は薄い |

⚠ **支払い操作は必ず本人。** こちらは金額の有無を見てもらうだけ。

#### この確認が空振りだった場合

`Tags` を外して1商品だけ `Publish`（2クリック）→ それでも駄目ならサポートへ。

### 支払いの線は空振り。新規作成も通っていた（2026-09-26）

本人が3点とも確認してくれた結果、**こちらの仮説は2つとも外れた。**

| # | 確認結果 |
|---|---|
| 1 | Payment account は **Current −$0.22**。ただし同じ画面に **`Nothing due for September`**（9月分の請求なし）、**`Auto-billing: Monthly on 1st · MasterCard`**。**期限超過ではない。10月1日に自動引き落とし。支払い操作は不要** |
| 2 | ダッシュボードに警告帯なし |
| 3 | **テスト品は今日が初めての出品。→ 新規リスティングの作成は通っている** |

**−$0.22 は未払いではなく、今月たまった手数料（テスト品の出品料$0.20など）。**
Etsyが出品を止めるのは「**期限を過ぎた**残高」があるとき。この画面はその状態ではない。

### 残った差は3つ（未検証）

| | テスト品（成功） | 本番（失敗） |
|---|---|---|
| タグ | 3個 | **13個** |
| 配送プロファイル | 既存を使った可能性 | **`Automatically assign`（新規作成が要る）** |
| 名入れ | Printifyの既定文 | **こちらの文＋上限16** |
| 写真8枚 / 両サイズ | 同じ | 同じ |

#### 1つずつトグルを倒して1商品だけ `Publish`（各2クリック・入力は消えない）

| | やること | 狙い |
|---|---|---|
| A | `Publishing settings` → `Tags` のチェックを外す | タグ13個が原因か |
| **B** | `Shipping` → プロファイルを `Automatically assign…` から**既存のもの**（ゴルフタオルで使用中）に変える | **一番怪しい。** 新規プロファイル作成でEtsyに蹴られている可能性 |
| C | `Personalization` → `Enable personalization` をOFF | 名入れが原因か（原因特定用。この状態では本番公開しない） |

#### サポートへ送る英文（除外済み事項を追記した版）

```
Hello,

I cannot publish any of my products to my Etsy store. All 5 fail with:

"Sorry, we couldn't publish this product. Please try again later or get in
touch with support if the issue reoccurs."

The product goes into "Publishing" state, then fails.

Details:
- Etsy store: OnePureStrike
- Date/time: 26 Sep 2026, from about 21:30 JST (UTC+9), still failing
- Product type: "Garden and House Banner" by Pic The Gift,
  2 variants (12x18 and 24.5x32)
- All 5 products fail. Nothing is created on the Etsy side.

What I have already ruled out:
- A different product published successfully to the same store about 15
  minutes before, as a brand new listing. So the connection works and new
  listing creation works.
- My Etsy payment account shows "Nothing due for September" and auto-billing
  is active. There is no overdue balance.
- No warning banners on my Etsy shop dashboard.
- Title 120-127 characters, 13 tags each 20 characters or fewer with no
  duplicates, description about 2,000 characters, all plain ASCII.

Could you look up the actual API response Etsy is returning for these publish
attempts? The on-screen message does not say what is wrong, and I do not want
to keep retrying blindly.

Thank you.
```

**「すでに除外できたこと」を先に並べるのが要点。**
英語サポートの1次対応はテンプレで「再試行」「再接続」「支払い確認」の3つを返してくる。
それを全部先回りで潰してあるので、**ログを見る2次対応へ直行できる。**

### 投げ先は Printify のサポート（Etsyではない）

| 理由 | |
|---|---|
| エラーを出しているのはPrintify | 文面の `get in touch with support` は**Printify自身**を指す |
| EtsyのAPIを叩いているのはPrintify | **Etsyが何を返したかを見られるのはPrintifyだけ。** 本人の画面にもEtsyの画面にも出ない |
| Etsyに投げると差し戻される | 「連携アプリの問題なので開発元へ」と返すのが定番 |

**投げ方：Printifyの画面の左下の隅にある黒い丸のチャットボタン。** あれがサポートのチャット。

#### Printifyが「Etsy側の問題」と言ってきた場合のEtsy宛の文

Etsyの画面の**右下 `💬 Get Help`** から。

```
Hello,

A third-party app (Printify) is failing to create new listings on my shop
through the Etsy API. It has been failing since 26 Sep 2026, around 21:30
JST. Nothing is created on my side.

Another listing was created successfully through the same app about 15
minutes before the failures started, so the app connection itself works.

My payment account shows "Nothing due" and auto-billing is active, and there
are no warnings on my shop dashboard.

Is there anything on my shop or my account that would block new listings
from being created through the API?

Thank you.
```

#### 補足：Printifyの商品ページに出る赤い帯

商品ページ上部に残る赤い帯は**今回のエラーが表示され続けているだけ**で、
別の障害ではない。Etsyのダッシュボードの警告帯とは別物。

### サポート1次対応の返答と、その返し方（2026-09-26）

Printifyからの返答（要旨）：

> 通常すぐ公開されるが、混雑時や大量公開時は遅延する。**公開処理に数時間かかることがあり、
> 24時間は超えず、その後 Publishing 状態が解除される。**
> 今回は複数商品で失敗しているので**設定上の問題**で止まっている可能性がある。
> **Printifyの担当者がEtsyとの連携を確認したり、公開処理を停止したりできる。**

**典型的な1次対応で、前提がずれている。**

| 向こうの前提 | 実際 |
|---|---|
| `Publishing` のまま止まっている | **数秒で解け、赤いエラー帯が出て失敗する** |
| 24時間待てば解決 | 商品は**下書きに戻り `Publish` ボタンが復活している** |

**ここを正さないと「24時間お待ちください」で1日潰れる。**

ただし2段落目は使える。**「担当者がEtsy連携を確認できます」と向こうが自分で書いている。**
それをそのまま依頼に変換する。

#### 返信した文

```
Thank you for the reply.

To be clear, this is not a delay. The products do not stay in "Publishing"
state. They enter "Publishing" for a few seconds, then fail with a red error
banner on the product page:

"Sorry, we couldn't publish this product. Please try again later or get in
touch with support if the issue reoccurs."

The product then returns to draft state, with the "Publish" button available
again. This has been repeating since 26 Sep 2026, about 21:30 JST.

Yes, please have an agent check the Etsy integration for my store now.

Specifically, could you tell me the actual error response that Etsy's API
returned for these publish attempts? That is the one piece of information I
cannot see from my side, and it would tell us which setting is wrong.

Store: OnePureStrike (Etsy)
Product type: "Garden and House Banner" by Pic The Gift, 2 variants
Affected: all 5 products. Example product URL.

Note: a different product published successfully to the same store about 15
minutes before the failures began, as a brand new listing.

Thank you.
```

#### 書き方の型（次に同種のことが起きたら流用する）

| 英語 | 狙い |
|---|---|
| **To be clear, this is not a delay.** | **相手の前提を最初の一文で否定する。** 曖昧にするとテンプレ回答のループに入る |
| `enter "Publishing" for a few seconds, then fail` / `returns to draft state, with the "Publish" button available again` | 遅延ではない**証拠を、観察できる事実として2つ**出す。「エラーが出ます」だけでは通らない |
| **Yes, please have an agent check ... now** | 向こうが「担当者が確認できます」と書いた文を**そのまま依頼に変換。** 自分で出した選択肢は断りにくい |
| **That is the one piece of information I cannot see from my side** | **そちらにしかできない作業だと確定させる。**「調べてください」より効く |

向こうも「設定上の問題かもしれない」と言っているので、
**待つ間にB（配送プロファイル）→A（タグ）→C（名入れ）を潰す作業は無駄にならない。**

### ★Printifyのサポートチャットは1通500字まで（2026-09-26 実測）

1通目が **ちょうど500字で切れて**いた。
`Nothing is created on th` で途切れており、**肝心の「すでに除外できたこと」が届いていなかった。**
テンプレ返答が来たのはそのため。

**上限500字。以後、サポートへは500字以内に分けて送ること。**

#### 添付ファイルではなく分割して送る

| 理由 | |
|---|---|
| **返答が日本語で来た＝チャットが自動翻訳されている** | **添付ファイルは翻訳されない** |
| 1次対応は添付を開かないことが多い | 本文に書いたほうが確実に読まれる |

#### 送り直した3通（実測 399 / 418 / 228字）

**1通目（399字）— これだけ読まれても効くように先頭に置く**

```
This is not a delay. The product stays in "Publishing" only a few seconds, then shows a red error banner and returns to draft, with the Publish button active again. It has repeated since 26 Sep, 21:30 JST.

Please have an agent check the Etsy integration for my store now, and tell me the actual error response Etsy's API returned for these attempts. That is the one thing I cannot see from my side.
```

**2通目（418字）**

```
Already ruled out:

1. Another product published fine to the same store 15 minutes before, as a brand new listing. So the connection works and new listing creation works.
2. Etsy payment account says "Nothing due", auto-billing active, no overdue balance.
3. No warning banners on my Etsy dashboard.
4. Title 120-127 chars. 13 tags, each 20 chars or fewer, no duplicates. Description about 2000 chars. All plain ASCII.
```

**3通目（228字）**

```
Store: OnePureStrike (Etsy)
Product type: "Garden and House Banner" by Pic The Gift, 2 variants (12x18 and 24.5x32)
All 5 products are affected.

Example product:
https://printify.com/app/product-details/<商品ID>
```

#### 分割の設計

**「遅延ではない」と「Etsyの応答を教えてほしい」を1通目に固める。**
2通目以降が読まれなくても、**24時間待ちのループには入らない。**
除外リストと識別子は2・3通目に回してよい。

### B：配送プロファイルは `Pic The Gift, 976` を選ぶ（2026-09-27）

プルダウンの選択肢は3つ。

| 選択肢 | 中身 |
|---|---|
| `Automatically assign and update profile if needed` | 既定。公開のたびにプロファイルを更新しに行く |
| **`Standard: Pic The Gift, 976, 5353, Home Decor: 2-30 business days`** | **976 = Garden and House Banner（`docs/01`）。これが正解** |
| `Standard: Taylor, 1614, Home Decor: 2-30 business days` | **1614 = ゴルフタオル**（`golf_towel/HANDOFF.md`）。**タオルの送料と納期がフラッグに適用されてしまう。使わない** |

#### 分かったこと：プロファイルはEtsy側に既に存在する

`Pic The Gift, 976, **5353**` の `5353` は**EtsyのプロファイルID**。
つまり**Etsy側にもう作られている**（テスト品も同じ Pic The Gift / 976 なので、
その公開時に作られたはず）。

**→「新規プロファイルの作成で蹴られている」という筋は薄い。**
ただし `Automatically assign` のままだと公開のたびに更新しに行くので、
明示指定に変える価値は残る。

#### 押す順番（Tagsを落とさないため）

1. プルダウンで `Standard: Pic The Gift, 976, 5353` を選ぶ
2. ⚠ **`Save as draft` は押さない**（Tagsのチェックが外れる）
3. `Publishing settings` タブ → **`Tags` にチェック**
4. そのまま緑の `Publish`

### 後回しの検討事項：送料無料にするかどうか

`Shipping` タブに **`Free shipping — Enable free Standard shipping ($6.39)`** があり、いまOFF。
`docs/10` の採算はこれ（買い手が送料負担）で組んである。

**ただしEtsyは米国向けに送料無料の商品を検索で優遇する。**
いま **$27.99 + $6.39 = $34.38** で、**Etsyの送料無料保証ライン $35 のすぐ下**。

売価を上げて送料込みにする案は、**広告を回して実数が出てから**検討する。
（`docs/16` の公開1週間後の価格調整と合わせて判断）

### B は外れ。残りの手（2026-09-27 00:06）

配送プロファイルを `Pic The Gift, 976, 5353` に明示指定して `Publish` → **同じエラー。**

ここまでで**シロと確認できたもの**：

| | |
|---|---|
| Etsyとの接続 | テスト品が同じ接続で公開成功 |
| 新規リスティングの作成 | 同上（テスト品は初出品） |
| 支払い | `Nothing due`・自動請求有効・期限超過なし |
| ショップの状態 | Etsyのダッシュボードに警告帯なし |
| 文言の中身 | タイトル/タグ/説明文/名入れとも上限内・全ASCII（機械検査） |
| **配送プロファイル** | **明示指定しても失敗（B）** |

#### 残る手

| | やること | 狙い |
|---|---|---|
| A | `Publishing settings` → `Tags` のチェックを外す → `Publish` | タグ13個が原因か |
| **D** | **「⋮」→ `Duplicate` で商品を複製し、複製を何も変えずに `Publish`** | **★本命。この5商品のレコード自体が壊れている線** |
| C | `Personalization` をOFF → `Publish` | 名入れが原因か（特定用。この状態では本番公開しない） |

**Dを推す理由：** 接続・支払い・新規作成・配送・文言が全部シロなら、
残るのは**最初の公開失敗で元レコードに内部状態が残った**という線。
複製はまっさらな別レコードなので切り分けになる。

- **複製が通る** → 原因は元レコード。**5つとも複製し直して公開すれば解決**（テストと解決が同時）
- **複製も落ちる** → レコードの問題ではない。サポート待ちに絞る

#### ここまでで駄目なら待つ

サポートには投函済み。こちらで確かめられることは出し尽くした。
**向こうがEtsyのAPI応答を見れば一発**なので、返事を待つのが一番早い。

### ★原因は名入れ（Personalization）だった（2026-09-27）

| テスト | 結果 |
|---|---|
| A タグを外す | **通らず** → タグはシロ |
| D 商品を複製 | **複製できず**（Printifyに複製の項目が無かった） |
| **C 名入れをOFF** | **★通った** |

Cはタグ同期ONのまま通っているので、**タグ・タイトル・説明文・価格・写真8枚・
配送プロファイルはすべてシロ**と確定。**名入れだけが原因。**

⚠ **この時点でR05はEtsyに公開されている（名入れ無しの状態）。**
説明文に「PERSONALIZE ボタンを押してください」とあるのにボタンが無い。
流入はほぼゼロだが、把握しておくこと。

#### 名入れの中で疑わしいのは2つ

成功したテスト品の名入れは **Printifyの既定文・既定の文字数上限**。
本番5商品との差はこの2点だけ。

| # | 差 |
|---|---|
| 1 | **説明文に二重引用符 `"THE SMITHS"` が2個** |
| 2 | **文字数上限を 13 → 16 に変更** |

#### 次の手（R05だけで試す。残り4つは触らない）

| | やること | 狙い |
|---|---|---|
| **E** | **名入れをONに戻して `Publish`** | ★本命。R05はEtsyと紐付いたので**次は「新規作成」ではなく「更新」**。Etsyは作成時と更新時で検証の厳しさが違うことがある |
| F | 名入れの文から**引用符を外す**（下記・114字） | APIに渡す文字列の引用符は**エスケープ漏れで通信を壊す典型** |
| G | 文字数上限を **16 → 13** に戻す | テスト品は既定値13のまま成功している |

**Eが通れば、残り4つも「名入れOFFで公開 → ONに戻して再公開」の2段構えで解決する。**

**Fの文（引用符なし・114字）**

```
Enter your family name - for example: SMITH
We print it as THE SMITHS. Longer names simply print a little smaller.
```

引用符を外しても意味は変わらない（大文字だけで十分目立つ）。

**Gの副作用**：13だと14字の名字（CHRISTOPHERSON等）が弾かれる。
`docs/21` 第7節の判断と矛盾するが、**公開できないよりはるかにマシ。**

#### サポートへ送った追加の1通（438字）

```
Update: I found the trigger. The product publishes fine when Personalization is OFF. It fails every time Personalization is ON.

Everything else is unchanged and fine: 13 tags, shipping profile set explicitly to Pic The Gift 976, our own title, description and mockups.

Personalization settings that fail: Required, character limit 16, and instruction text containing double quotes.

What does Etsy return for the personalization fields?
```

### E も失敗。サポートはボットだった。→ 回り道で解決する（2026-09-27）

名入れをONに戻して `Publish` → **また失敗。**
R05はEtsyと紐付いている（`See in store` が出ている）ので**「更新」でも落ちる。**

サポートの返答：

> Etsyがパーソナライズ設定に対して返した実際のAPIレスポンスは、**利用可能な情報では確認できません。**
> （中略）ただし、今回の組み合わせについて**Etsyが返す具体的なレスポンス内容までは記載されていません。**

**ドキュメントを検索して答えているだけのボット。** アカウントのログを見ていない。
→ 人間へのエスカレーションを要求した（378字）。

```
This answer looks like it came from documentation, not from my account's logs. Please escalate this to a human support agent.

I need someone who can look at the actual publish attempts on my store and see what Etsy returned. If support cannot see that either, please say so directly, and instead tell me which personalization settings are known to work when publishing to Etsy.
```

`If support cannot see that either, please say so directly`（見られないならそうとはっきり言ってください）が要点。
**ボットが一番苦手な、白黒つけさせる質問。** ここで人間に回る。

---

## 9. ★回り道：Printifyの名入れ機能は、そもそも要らない

**`docs/22` 第4部の運用では、Printifyの名入れ中継機能を使っていない。**
注文が来たらEtsyの注文画面で名字を読み、こちらのスクリプトでデザインを作り直し、
Printifyで差し替える手作業。

**必要なのは「Etsyの商品ページに名前の入力欄があること」だけ。**
**それはEtsy側で直接足せる。**

### 手順（1商品あたり5分）

**① Printifyで公開する**

1. `Personalization` タブ → **`Enable personalization` をOFF**
2. `Publishing settings` → **`Tags` にチェック、`Personalization` のチェックを外す**
   ⚠ `Personalization` の同期を切らないと、**再公開のたびにEtsy側の名入れ欄が消される**
3. **`Publish`**

**② Etsyで名入れ欄を足す**

1. `etsy.com/your/shops/me/tools/listings` から商品を開く
2. **`Item Options`** タブ
3. `Custom options` の **`+ Add field`**

| 項目 | 値 |
|---|---|
| 種類 | **Text box** |
| Required | **チェックを入れる** |
| Instructions | 下記 |
| Character limit | **16** |

```
Enter your family name - for example: SMITH
We print it as "THE SMITHS". Longer names simply print a little smaller.
```

4. **`Publish changes`**

### 残っている任意の検証

原因を潰しておきたい場合のみ。**回り道で完成するので急がない。**

| | やること |
|---|---|
| F | 名入れの文から**二重引用符2個を外す**（`We print it as THE SMITHS.`）→ ONのまま `Publish` |
| G | 文字数上限を **16 → 13**（成功したテスト品は既定値のまま） |

**APIに渡す文字列の引用符は、エスケープ漏れで通信を壊す典型。** Fが本命。

### 人間の担当者に繋がった（2026-09-27）

エスカレーション要求が効いて、ボットから人間へ回った
（`The estimated wait time is 6-8 minutes.`）。

**「見られないならそうとはっきり言ってください」と白黒つけさせる質問が効いた。**
ボットはこの形の質問を処理できない。以後も同じ手が使える。

#### 担当者に送った3通

**1通目（433字）— 切り分け結果と依頼**

```
Thank you. Here is the isolated result.

Publishing this product to Etsy fails every time Personalization is ON, and succeeds immediately when Personalization is OFF. Nothing else is changed between the two attempts.

It fails both when creating a new listing and when updating a listing that is already live on Etsy.

Could you look at the publish logs for my store and tell me the error Etsy returns for the personalization fields?
```

**2通目（393字）— 識別子と除外済み**

```
Store: OnePureStrike (Etsy)
Product: https://printify.com/app/product-details/<商品ID>
Blueprint: Garden and House Banner, Pic The Gift, 2 variants.

Personalization used: enabled, Required, character limit 16, instruction text 116 characters including two double quote marks.

Already ruled out: tags, shipping profile, title, description, price, mockups, payment, connection.
```

**3通目（383字）— ★回り道の裏取り。これが一番実利がある**

```
If this cannot be fixed today, please confirm my workaround is safe:

1. Publish from Printify with Personalization OFF.
2. Add the personalization field manually on the Etsy listing.
3. Uncheck Personalization under Synced product details in Printify.

Will Printify leave the Etsy personalization field alone after that, including when I edit the design for an order and republish?
```

**狙い：** 原因が今日分からなくても、**回り道が安全だとメーカー自身に確認できれば明日には出せる。**
「直してくれ」だけで終わらせず、**動く道の裏取りを取りに行く。**

### F（引用符を外す）も失敗（2026-09-27）

名入れの文から二重引用符2個を外して `Publish` → **同じエラー。**
**引用符は原因ではない。**

未検証で残っているのは **G（文字数上限 16 → 13）だけ。**
成功したテスト品は13（Printifyの既定値）だった。

**Gも駄目なら、名入れ設定の中身に関係なく「ONにすると落ちる」ということ。**
原因究明は担当者に任せ、**第9節の回り道（Etsy側で名入れ欄を足す）で5商品とも出す。**

#### サポートチャットは数分放置すると一時停止する

> This conversation is currently paused. We've saved all your progress, and the chat
> will automatically resume as soon as a message is sent from either side!

**担当者の枠を失わないよう、何か送って再開させること。**
検証しながら待つときは注意。

2通目は引用符の件を反映した版に差し替えた（411字）。

```
Store: OnePureStrike (Etsy)
Product: https://printify.com/app/product-details/<商品ID>
Blueprint: Garden and House Banner, Pic The Gift, 2 variants.

Personalization used: enabled, Required, character limit 16. I also tried removing the double quotes from the instruction text. It still failed.

Already ruled out: tags, shipping profile, title, description, price, mockups, payment, connection.
```
