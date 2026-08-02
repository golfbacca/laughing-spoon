# -*- coding: utf-8 -*-
"""
review_filter の単体テスト。ネットワーク不要。

    python3 tools/test_review_filter.py

本文は実在レビューではなく、判定の境界を確かめるために書いた検証用サンプル。
"""
import sys
from review_filter import analyze, keep, red_flags


def check(label, cond):
    mark = "OK  " if cond else "FAIL"
    print(f"[{mark}] {label}")
    return cond


def main():
    ok = True

    # --- 中身への言及を拾えるか ---------------------------------------
    r = analyze("The line art is clean and the scenes are charming.")
    ok &= check("線・場面への言及を中身と判定", r["is_content"])
    ok &= check("該当文を1つ抜き出す", len(r["sentences"]) == 1)

    # --- 紙だけの話は落とすか ------------------------------------------
    r = analyze("The paper is very thin and markers bleed through badly.")
    ok &= check("紙・にじみのみの文は中身と判定しない", not r["is_content"])
    ok &= check("physical_only が立つ", r["physical_only"])

    # --- 配送・価格だけの話も落とすか -----------------------------------
    r = analyze("Arrived damaged. Way too expensive for what it is.")
    ok &= check("配送・価格のみは中身と判定しない", not r["is_content"])

    # --- 混在レビューは中身の文だけ残すか -------------------------------
    body = (
        "The paper is thin and bleeds with markers. "
        "But the illustrations are gorgeous and full of detail. "
        "Shipping was fast."
    )
    r = analyze(body)
    ok &= check("混在レビューを中身ありと判定", r["is_content"])
    ok &= check("中身の文だけを1文抜く", len(r["sentences"]) == 1)
    ok &= check(
        "抜いた文がイラストの文",
        "illustrations are gorgeous" in r["sentences"][0]["text"],
    )

    # --- 同一文に両方ある場合は残し、フラグを立てるか --------------------
    r = analyze("The paper is thin but the lines are beautifully drawn.")
    ok &= check("同居文は残す", r["is_content"])
    ok &= check("with_physical が立つ", r["sentences"][0]["with_physical"])

    # --- 地雷語 --------------------------------------------------------
    f = red_flags("These are clearly AI generated and very blurry.")
    ok &= check("AI生成疑いを検出", "AI生成疑い" in f)
    ok &= check("画質不良を検出", "画質不良" in f)

    f = red_flags("The same image is repeated over and over.")
    ok &= check("使い回しを検出", "使い回し" in f)

    f = red_flags("This does not look Japanese at all, very generic.")
    ok &= check("題材が的外れを検出", "題材が的外れ" in f)

    f = red_flags("The lines are too thin and hard to color.")
    ok &= check("線が塗れないを検出", "線が塗れない" in f)

    # --- 星の絞り込み ---------------------------------------------------
    rev = {"star": 3, "body": "The illustrations are nice."}
    kept, _ = keep(rev)
    ok &= check("星3は既定で除外", not kept)

    rev = {"star": 5, "body": "The illustrations are nice."}
    kept, _ = keep(rev)
    ok &= check("星5は採用", kept)

    rev = {"star": 1, "body": "Shipping took forever."}
    kept, _ = keep(rev)
    ok &= check("星1でも中身の言及がなければ除外", not kept)

    # --- 改行しか区切りがない本文 ---------------------------------------
    r = analyze("Paper is thin\nThe drawings are lovely\nCame on time")
    ok &= check("改行区切りでも文を割れる", len(r["sentences"]) == 1)

    # --- 空入力 ---------------------------------------------------------
    r = analyze("")
    ok &= check("空文字で落ちない", not r["is_content"])
    r = analyze(None)
    ok &= check("None で落ちない", not r["is_content"])

    print()
    print("全て通過" if ok else "失敗あり")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
