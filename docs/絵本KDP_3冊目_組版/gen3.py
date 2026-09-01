#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3冊目の絵を1枚ずつ生成する。

  python3 gen3.py 01_表表紙_正方形 07_場面06_ついた
  python3 gen3.py --all
  python3 gen3.py --list

参照画像（引き継ぎ書0-B・2冊目の作業記録）
  ・基準シート        造形の最終確定
  ・2冊目の絵         ふともも丈のシャツ姿と、家の中の描き方
  ・1冊目の表表紙     2人の大きさの比
落ち方の見分け（2冊目 作業記録1・2章）
  KeyError 'parts' … 画像が返らない。構図の問題。粘っても同じ
  通信のエラー      … 4K画像は10MB前後。投げ直せば通る
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "絵本KDP_組版"))
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen_image import generate, REF_SHEET                    # noqa: E402
import prompts3                                              # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
IMG  = ROOT / "docs" / "絵本KDP_3冊目_画像"; IMG.mkdir(exist_ok=True)
IMG2 = ROOT / "docs" / "絵本KDP_2冊目_画像"

REF_NIGHTSHIRT = IMG2 / "12_場面11_はけた.jpg"  # ふともも丈のシャツ姿

# 場面ごとの基準画。承認できた1枚を手でここにコピーして使う。
#   cp 絵本KDP_3冊目_画像/02_場面01_めがさめる.jpg 絵本KDP_3冊目_画像/_anchor_寝室.jpg
BED_ANCHOR  = IMG / "_anchor_寝具.jpg"   # 敷＝クリーム／掛＝緑 が正しく写った1枚
LAMP_ANCHOR = IMG / "_anchor_あかり.jpg" # ドーム型のあかりと丸椅子だけ。布団は写らない
ROOM_ANCHOR = IMG / "_anchor_部屋.jpg"   # 壁・ドア・窓だけ。布団は写らない
HALL_ANCHOR = IMG / "_anchor_廊下.jpg"

BEDROOM = {"01_表表紙_正方形", "S01_ねるまえ", "02_場面01_めがさめる",
           "03_場面02_むずむず", "S04_ふとんのふち", "04_場面03_でられない",
           "05_場面04_ここにある", "06_場面05_てをのばす", "07_場面06_ついた",
           "S09_じぶんでつけられた", "08_場面07_ふとんからでる",
           "13_場面12_またねる", "S18_つぎのよる", "14_裏表紙_正方形"}
CORRIDOR = {"09_場面08_ろうか", "S13_トイレのドア", "10_場面09_トイレのなか",
            "11_場面10_おわりのおと", "S14_てをあらう", "12_場面11_もどる"}

FAILED = []

def refs(name):
    """【やらかし・2026-08-29】最初 1冊目の表表紙（REF_BOTH）を
    身長比の見本として入れていたら、そこに描かれている
    ベージュの短パン・赤いくつ・クリーム色のリュックまで写された。
    プロンプト側は正しく「No backpack anywhere in this book」と
    書いてあったのに、参照画像のほうが強い。
    その本に出てこない服装の絵は、参照に入れない。
    身長比は2冊目の絵（同じ2人が並んでいる）で足りる。

    【やらかし・2026-08-31】同じことが寝具でも起きた。
    表紙を全ページの基準画にしていたら、表紙の緑（＝敷パッドとして
    描かれてしまったもの）が18枚すべてに写り、文章でいくら
    「緑は掛け布団」と書いても直らなかった。
    基準画は場面ごとに持ち、【直したい要素が正しく写っている1枚】
    だけを使う。まだ無いなら基準画なしで1枚目を描き、それを見て
    採否を決めてから基準画にする。"""
    r = [REF_SHEET, REF_NIGHTSHIRT]
    if name in CORRIDOR:
        cand = [HALL_ANCHOR]
    else:
        # 寝具の基準画は【寝具だけ】、あかりの基準画は【布団を写さない切り抜き】。
        # 1枚の絵に両方を任せると、正しくないほうまで一緒に写る。
        cand = [BED_ANCHOR, LAMP_ANCHOR, ROOM_ANCHOR]
    for a in reversed(cand):
        if a.exists():
            r.insert(0, a)
    return r

def trim_border(path):
    """【やらかし・2026-09-01】「FULL BLEED. NO FRAME」と書いてあるのに、
    描き直すたびに白い縁がついた絵が返ってくることがある。
    03 は四辺きっちり132px、12 は上0/下163/左24/右49 と不揃いだった。
    文章では止まらないので、生成後に機械的に切る。
    絵の中に真っ白はほとんど無いので、白の帯だけが確実に取れる。"""
    from PIL import Image
    import numpy as np
    im = Image.open(path).convert("RGB")
    a = np.asarray(im, dtype=int)
    h, w, _ = a.shape
    ink = (a.min(axis=2) < 235)
    rows = np.nonzero(ink.any(axis=1))[0]
    cols = np.nonzero(ink.any(axis=0))[0]
    if len(rows) == 0 or len(cols) == 0:
        return
    t, b, l, r = rows[0], h - 1 - rows[-1], cols[0], w - 1 - cols[-1]
    if max(t, b, l, r) < 8:                     # 縁なし。触らない
        return
    im.crop((int(l), int(t), int(w - r), int(h - b))) \
      .resize((w, h), Image.LANCZOS).save(path, quality=95)
    print(f"  白縁を切った 上{t} 下{b} 左{l} 右{r}")

def one(name, force=False):
    out = IMG / f"{name}.jpg"
    if out.exists() and not force:
        print(f"  済み {name}"); return
    print(f"生成 {name}")
    prompt = prompts3.prompt_for(name)
    for attempt in range(3):
        try:
            generate(prompt, str(out), ref_images=refs(name), aspect="1:1")
            trim_border(out)
            return
        except KeyError:
            FAILED.append(name)
            print(f"  × {name}: 画像が返らない。構図を寄せて描き直すこと")
            return
        except Exception as e:
            print(f"  … {name}: {type(e).__name__}（{attempt+1}回目）")
    FAILED.append(name)
    print(f"  × {name}: 通信で3回とも落ちた")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--list":
        for n in prompts3.NAMES: print(" ", n)
    else:
        force = "--force" in a
        names = prompts3.NAMES if a[0] == "--all" else [x for x in a if not x.startswith("--")]
        for n in names: one(n, force=force)
        print(f"\n完了 {len(names)-len(FAILED)}/{len(names)}")
        if FAILED: print("描き直しが必要:", " ".join(FAILED))
