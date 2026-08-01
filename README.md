# LINEエモ文字スタンプ シリーズB「呪詛版」

コールセンター（問い合わせ・苦情対応オペレーター）界隈向け、文字のみのエモ文字スタンプ16枚セット。
送信先はオープンチャット（同業の他人）を想定。

## 設計方針

- 「可愛い絵」ではなく **感情のショートカットキー** として設計
- 怒りではなく **「壊れの実況」** を描く。主語を書かないことで黒くする
- 禁止：説教くさいポジティブ／シモ・下ネタ／暴力・脅迫語／特定企業名
- キャラなし、文字のみ

## 中身

| パス | 内容 |
|---|---|
| `stickers/01.png` 〜 `16.png` | スタンプ画像 370×320px・背景透過PNG・白フチ入り（登録順） |
| `stickers/main_240x240.png` | メイン画像 |
| `stickers/tab_96x74.png` | トークルームタブ画像 |
| `stickers/00_ファイル対応表.txt` | 番号と文言の対応表 |
| `gen_stickers.py` | 画像生成スクリプト（Pillow） |
| `docs/LINEスタンプ_コルセン界隈_16枚_Canva手順.txt` | 設計仕様＋Canva手作業手順＋2・3セット目の候補 |

## 画像の作り直し

```
pip install Pillow
apt-get install -y fonts-noto-cjk fonts-noto-cjk-extra fonts-motoya-l-maruberi
python3 gen_stickers.py
```

`gen_stickers.py` 末尾の `S = [...]` が全16枚の設計データ。文言・フォント・サイズ・色・配置を
そこだけ書き換えれば全枚数を再生成できる。確認用のコンタクトシート
（`stickers/_preview_light.png` / `_preview_dark.png`）も同時に出力される。

## 使用フォント（Canvaの指定フォントの代替）

| 役割 | 本来の指定 | 生成に使用 |
|---|---|---|
| 極太 | DELA Gothic One | Noto Sans CJK JP Black |
| 明朝 | しっぽり明朝 | Noto Serif CJK JP Light / Medium |
| 細字 | Noto Sans JP Light | Noto Sans CJK JP Light |
| 手書き | Yusei Magic | MotoyaLMaru（丸ゴシック＋1文字ごとの微回転） |

## LINE申請時の注意

- スタンプは **8 / 16 / 24 / 32 / 40枚** 単位でしか申請できない（本セットは16枚）
- ファイルは `01.png` 〜 `16.png` の番号順でアップロードする
- LINEスタンプメーカー経由の場合、**フチの自動追加を「0／なし」にする**
  （画像側に白フチが入っているため二重になる）
