# tapestry/ — Etsy タペストリー（Printify製造）

2026-10-03 着手。

**始める前に `../docs/EtsyとPrintifyの知見.md` を読むこと。**

## 文書

| ファイル | 中身 |
|---|---|
| `docs/01_立ち上げ.md` | 知見をタペストリーに当てはめた結果・最初に本人に確認してもらうこと |
| `docs/02_Printify実数とSVG方針.md` | Printifyの原価・入稿px・SVGの制約・作風の候補 |
| `docs/03_サイズ一覧と検索語と試験入稿.md` | 8サイズの正体・オートコンプリート結果・試験SVGの見方 |
| `tools/check_svg.py` | 入稿SVGの検査（20MB・20,000パス・text無し・image無し） |
| `tools/make_print_test.py` → `test/print_test.svg` | Printifyの切れ方とSVG機能を測る試験用SVG |

## 状態

| 項目 | 状態 |
|---|---|
| テーマ | **B：売れ筋のテーマ（ゴルフではない）**。作風は検索語を見て決める |
| 入稿形式 | **SVG**（13650×16125px は非現実的）。**こちらがコードで書く** |
| Printifyの原価・入稿px | 88×104 で **$47.62・13650×16125px**。他サイズは未確認 |
| サイズ | **縦4（26×36/50×60/68×80/88×104）＋横4。** 縦横は混ぜない。原価は88×104の$47.62のみ判明 |
| 検索語の裏付け | `celestial` `mountain` `boho` `abstract` は**実在・`large`も出る**。`mushroom` は毛布が混ざる。競合の強さは未測定 |
| プロバイダ | **MWW On Demand（米国唯一・★8.3）を手動で選ぶ** |
| 試験入稿 | `test/print_test.svg` 作成済み。**本人のPreview待ち** |
