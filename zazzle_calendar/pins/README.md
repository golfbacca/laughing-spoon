# Pinterest 用ピン画像（13枚・1000×1500・縦横2:3）

作り方：`python3 zazzle_calendar/tools/make_pins.py`（`upload/` の入稿用写真を縮小して配置するだけ。写真の中身は無加工・AI不使用）

- デザイン：生成りの背景に、白いカレンダーのページ（上にリング、写真、2027年のその月の升目）。下にピンの見出しと「2027 Photo Calendar · Photographed by my father / KISO VALLEY LIGHT」
- 表紙だけ升目の代わりに「2027 WALL CALENDAR」
- 升目は日曜始まり（米国式）
- 書体：Playfair Display（見出し）、Montserrat（小さい文字）。`garden_flag/tools/fonts/`

各ピンのタイトル・説明文は `docs/02_出品文言_確定版.md` 第4章。リンクは素の商品URL：
`https://www.zazzle.com/tsumago_nakasendo_japan_four_seasons_calendar-256169120708729755`

## 追加：12か月一覧のピン（2026-11-12）
- `pin_13_overview_12months.jpg`（`tools/make_overview_pin.py`）。12か月の写真を3×4で並べ、月名を添えたもの
- タイトル：`12 Months in Tsumago, Japan: A 2027 Photo Wall Calendar of the Kiso Valley`
- 説明文：`All twelve months of our 2027 wall calendar on one page: persimmons in the snow, ice lanterns on a winter night, fallen camellias, cherry blossoms, flooded rice paddies, buckwheat flowers, lanterns after the rain, an autumn sunset, and snow on the old Nakasendo road. Every photo was taken by my father in and around our hometown, Tsumago, in Japan's Kiso Valley.`
