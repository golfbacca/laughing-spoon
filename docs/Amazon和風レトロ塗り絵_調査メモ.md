# Amazon.com 和風レトロ塗り絵 レビュー調査メモ

調査日: 2026-08-02

## 依頼内容

Amazon.com の和風レトロ系塗り絵について、10作品 × 各20件のレビューを収集する。

- 対象商品: 直近1ヶ月以内に販売開始されたもの
- ある程度レビューが集まっている（市場規模のある）商品に限定
- 星5・星1 を重点的に見る
- 紙質・配送などではなく、**中身のコンテンツ（イラスト・線画）に言及したレビュー**に絞る

## 結論：レビュー本文は取得できていない

以下2つの理由で、依頼された200件のレビュー収集は現時点で未達。**推測でレビュー文を書くことはしていない。**

### 1. 技術的な遮断（ハードブロッカー）

この実行環境のネットワークポリシーが `amazon.com` への通信を拒否している。

```
curl https://www.amazon.com/  -> CONNECT tunnel failed, response 403
WebFetch https://www.amazon.com/... -> HTTP 403 Forbidden
```

プロキシのステータスにも明示的に記録されている:

```json
{ "kind": "connect_rejected",
  "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)",
  "host": "www.amazon.com:443" }
```

`amazon.co.jp` も同様。さらに `example.com` すら通らないため、
特定ドメインのブロックではなく **許可リスト方式の厳しいポリシー**が敷かれている。

Web検索は使えるが、返ってくるのは商品ページの**タイトル・商品説明文まで**で、
カスタマーレビュー本文・レビュー件数・星の分布は取得できなかった
（レビュー本文を狙った検索クエリを複数試行、いずれも本文は返らず）。

### 2. 条件そのものの矛盾

「直近1ヶ月以内に販売開始」と「ある程度レビューが集まっている」は、
このカテゴリではほぼ両立しない。

KDPのローコンテンツ本（塗り絵）は、発売直後にレビューがほとんど付かない。
検索で見つかった候補も、発売日が確認できたものは全て 2026年5〜6月であり、
**7月以降（直近1ヶ月）に出た商品でレビューが集まっているものは見当たらなかった。**

市場の温度感を見るのが目的であれば、期間を **3〜6ヶ月**に広げる方が
実用的なサンプルが取れる。

## 候補商品リスト（検索で実在を確認）

Amazon.com の商品ページ URL と ASIN は確認済み。
発売日は検索経由で得た値で、**ページ実物では未確認**。
レビュー件数・星の分布は **全て未取得**。

| # | タイトル | 著者 | ASIN | 発売日(未確認) |
|---|---|---|---|---|
| 1 | Japanese Retro Shops Coloring Book | NR Coloring Atelier | B0H665SDGD | 2026-06-20 |
| 2 | Nostalgic Showa Japan | Japan Art Studio | B0H1C2ZSRF | 2026-05-09 |
| 3 | Showa Retro Nostalgia Japan Coloring Book for Adults | Yume K. | B0H1X19MQ6 | 2026-05-13 |
| 4 | Showa Retro Coloring Book: Everyday Life & Gentle Scenery | Ryoko Imagami | B0H5WCZ3KJ | 2026-06-18 |
| 5 | Cozy Retro Japan Coloring Book | Cozy Sakura Atelier | B0H6GL9HS3 | 2026-06-19 |
| 6 | VINTAGE KIMONO COLORING BOOK | yocco | B0H4MQN54X | 不明 |
| 7 | Showa Memories: A Nostalgic Coloring Book for Adults | Masayoshi Matsumae | B0FKGMQTL1 | 不明 |
| 8 | Showa Retro Shopping Street Coloring Book | NOBUKOART | B0H6GBFD61 | 不明 |
| 9 | Nostalgic Japanese Shopping Street | Atelier Yamazaki | B0GYFM2VPC | 不明 |
| 10 | Cute Retro Japan Coloring Book Showa Daily Life | KAJU | B0GT4KK1KQ | 不明 |
| 11 | Showa Life Coloring Book | Miki Art Work | B0GL7BMKRS | 不明 |
| 12 | Showa Summer Coloring Book (Showa Seasons) | Rie Art stadio | B0H2GQ2TJ8 | 不明 |
| 13 | Showa Autumn Coloring Book (Showa Seasons) | Rie Art stadio | B0H37H4HJ8 | 不明 |
| 14 | Lost Japan – Meiji Era Coloring Book | Kazuki K | B0GPDZ27GP | 不明 |

URL は `https://www.amazon.com/dp/<ASIN>` で開ける。

### 読み取れる傾向（レビューではなく商品説明文から）

商品説明文の売り文句を見ると、このジャンルの訴求軸は概ね次に集約される。
レビューの代わりにはならないが、競合が何を「価値」として置いているかは分かる。

- 題材: 商店街 / 喫茶店・kissaten / 路地・横丁 / 屋台・食堂 / 祭り / ネオン / 学校 / 駅
- 線の性質: 「clean lines」「large spaces」「simple and large bold lines」
  → **線の太さと余白の広さ**を明示的に売りにしている商品が複数ある
  （＝ここが評価の分かれ目になっている可能性が高い）
- 想定読者: beginners / seniors / relaxation・mindfulness 文脈

## 進めるための選択肢

1. **環境のネットワークポリシーを緩める** — `amazon.com` を許可した環境を作り直せば、
   商品ページとレビューページを直接読める。最も確実。
   参照: https://code.claude.com/docs/en/claude-code-on-the-web
2. **条件を緩める** — 「直近1ヶ月」を3〜6ヶ月に広げる。
   レビューが集まっている商品を対象にできる（ただし1の解決が別途必要）。
3. **手元で取得したHTMLを渡してもらう** — 商品ページ／レビューページを保存して
   このリポジトリに置いてもらえれば、そこから抽出・分類は実行できる。
