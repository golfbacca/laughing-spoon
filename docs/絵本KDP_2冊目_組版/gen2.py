#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2冊目の絵を1枚ずつ生成する。

  python3 gen2.py 01_表表紙_正方形 09_場面08_かたあし   # 指定した名前だけ
  python3 gen2.py --all                                  # 未生成のものを全部
  python3 gen2.py --list                                 # 名前一覧

キャラを崩さないため、参照画像は必ず添える（引き継ぎ書 0-B）。
  ・基準シート           … 造形の最終確定
  ・1冊目の表表紙        … 2人の大きさの比
  ・すでに承認した2冊目の絵 … 部屋と服の同一性（あれば1枚だけ足す）
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "絵本KDP_組版"))
from gen_image import generate, REF_SHEET, REF_BOTH          # noqa: E402
import prompts2                                              # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
IMG  = ROOT / "docs" / "絵本KDP_2冊目_画像"
IMG.mkdir(exist_ok=True)

# 部屋と服の基準になる絵。1枚できたらここに名前を入れる。
ANCHOR = IMG / "01_表表紙_正方形.jpg"

def refs():
    r = [REF_SHEET, REF_BOTH]
    if ANCHOR.exists():
        r.insert(0, ANCHOR)        # 承認済みを先頭に置くと「編集」寄りになる
    return r

FAILED = []

def one(name, force=False):
    """1枚落ちても全体を止めない。落ちたものは最後にまとめて出す。
    画像が返らない主因は安全フィルタで、MODESTY文を否定形で書くと
    かえって弾かれる（2026-08-26に場面07で発生）。肯定形で書くこと。"""
    out = IMG / f"{name}.jpg"
    if out.exists() and not force:
        print(f"  済み {name}")
        return
    print(f"生成 {name}")
    prompt = prompts2.prompt_for(name)
    for attempt in range(3):
        try:
            generate(prompt, str(out), ref_images=refs(), aspect="1:1")
            return
        except KeyError:
            # 画像が返らない。プロンプトの構図の問題なので、粘っても同じ。
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
        for n in prompts2.NAMES: print(" ", n)
    else:
        force = "--force" in a
        names = prompts2.NAMES if a[0] == "--all" else [x for x in a if not x.startswith("--")]
        for n in names:
            one(n, force=force)
        print(f"\n完了 {len(names)-len(FAILED)}/{len(names)}")
        if FAILED:
            print("描き直しが必要:", " ".join(FAILED))
