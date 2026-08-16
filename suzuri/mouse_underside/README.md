# ステッカー「裏返したマウスのボール」

平成レトロ／ノートPC向け。SUZURI出品用。

## ファイル

| ファイル | 内容 |
|---|---|
| `raw.png` | 生成AIが出した元画像（**ここに保存する**） |
| `sticker.png` | 入稿用の透過PNG（スクリプトが生成） |

`raw.png` はまだ置かれていません。生成画像をこの名前で保存してください。

## 手順

```
python3 tools/suzuri_cutout.py suzuri/mouse_underside/raw.png \
    -o suzuri/mouse_underside/sticker.png
```

詳細は `docs/SUZURI_マウス裏_入稿手順.txt`。
出品文（商品名・説明文・タグ・トリブン）は `docs/SUZURI_マウス裏_出品一式.txt`。

## 生成プロンプト

`docs/SUZURI_マウス裏_出品一式.txt` の設計に対応する英語プロンプトは
`prompt.txt` にある。横展開（フロッピー／CD-R／スケルトン）を作るときは
これをベースにモチーフだけ差し替える。
