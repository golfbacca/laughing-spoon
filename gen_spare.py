# -*- coding: utf-8 -*-
"""
差し替え用の予備スタンプ

set1 #11「今の、通報案件」／ set2 #09「録音、残ってます」／ set2 #12「番号、覚えました」
の3枚は、単体で見ると受信者への威圧に読めるためリジェクトされる可能性がある。
その場合に即差し替えられるよう、凍結中の候補から同テーマの代替を用意しておく。

  set1 #11 → 頭の中だけ叫んでた   （実況のまま、威圧の要素だけ抜いた）
  set2 #09 → 席だけ埋まってる     （構造への呪詛。対象が人でなく職場になる）
  set2 #12 → 目、開いてるだけ     （壊れの実況。set2 のテーマにより忠実）
"""
import os
from sticker_engine import SUMI, HAI, build, verify

SPARE = [
 ("set1_11_差し替え_頭の中だけ叫んでた", {"blocks":[
    {"text":"頭の中だけ","font":"black","size":38,"color":SUMI},
    {"text":"叫んでた","font":"black","size":62,"color":HAI,"gap":4},
 ]}),
 ("set2_09_差し替え_席だけ埋まってる", {"blocks":[
    {"text":"席だけ","font":"sans_l","size":36,"color":HAI},
    {"text":"埋まってる","font":"sans_l","size":52,"color":SUMI,"gap":6},
 ]}),
 ("set2_12_差し替え_目、開いてるだけ", {"blocks":[
    {"text":"目、","font":"sans_l","size":36,"color":HAI},
    {"text":"開いてるだけ","font":"sans_l","size":50,"color":SUMI,"gap":6},
 ]}),
]

if __name__ == "__main__":
    out = "stickers/spare"
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))
    for name, spec in SPARE:
        build(spec).save(os.path.join(out, name + ".png"))
    print("spare:", verify(out) or "検証OK（余白10px以上・全枚数透過）")
