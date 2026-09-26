# -*- coding: utf-8 -*-
"""名入れ説明文がEtsyの規則に通るかを検査する。

2026-09-27 Printifyサポート（Michael）より判明：
  「名入れの説明文に、大文字が連続する語は最大1つまで」
  これを超えると Publish が汎用エラーで失敗し、理由は画面に出ない。

制限：
  - 全大文字の語（大文字2文字以上が連続）は **1つまで**（0を推奨）
  - Printifyの入力欄は120字まで
"""
import re, sys

MAX_CAPS = 1
MAX_LEN  = 120

def caps_words(t):
    return re.findall(r"\b\w*[A-Z]{2,}\w*\b", t)

def check(name, t):
    cw = caps_words(t)
    ok = len(cw) <= MAX_CAPS and len(t) <= MAX_LEN
    print(f"{name}")
    print(f"  長さ {len(t):>3}字 / {MAX_LEN}   全大文字の語 {len(cw)}個 / {MAX_CAPS}   {'OK' if ok else '★NG'}")
    if cw: print(f"  検出: {cw}")
    print(f"  ---\n  {t}".replace("\n","\n  "))
    print()
    return ok

CAND = {
 "★採用 A3（110字・全大文字0個）":
   'Enter your family name - for example: Smith\nWe print it in capitals as The Smiths. Longer names print smaller.',
 "旧・失敗した文（全大文字3個）":
   'Enter your family name - for example: SMITH\nWe print it as "THE SMITHS". Longer names simply print a little smaller.',
 "旧・引用符だけ外した版（これも失敗）":
   'Enter your family name - for example: SMITH\nWe print it as THE SMITHS. Longer names simply print a little smaller.',
}
if __name__=="__main__":
    if len(sys.argv)>1:
        check("入力された文", sys.argv[1]); sys.exit(0)
    for n,t in CAND.items(): check(n,t)
