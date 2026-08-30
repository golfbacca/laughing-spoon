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

ANCHOR = IMG / "01_表表紙_正方形.jpg"          # 1枚できたら夜の基準になる
REF_NIGHTSHIRT = IMG2 / "12_場面11_はけた.jpg"  # ふともも丈のシャツ姿

FAILED = []

def refs():
    """【やらかし・2026-08-29】最初 1冊目の表表紙（REF_BOTH）を
    身長比の見本として入れていたら、そこに描かれている
    ベージュの短パン・赤いくつ・クリーム色のリュックまで写された。
    プロンプト側は正しく「No backpack anywhere in this book」と
    書いてあったのに、参照画像のほうが強い。
    その本に出てこない服装の絵は、参照に入れない。
    身長比は2冊目の絵（同じ2人が並んでいる）で足りる。"""
    r = [REF_SHEET, REF_NIGHTSHIRT]
    if ANCHOR.exists():
        r.insert(0, ANCHOR)
    return r

def one(name, force=False):
    out = IMG / f"{name}.jpg"
    if out.exists() and not force:
        print(f"  済み {name}"); return
    print(f"生成 {name}")
    prompt = prompts3.prompt_for(name)
    for attempt in range(3):
        try:
            generate(prompt, str(out), ref_images=refs(), aspect="1:1")
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
