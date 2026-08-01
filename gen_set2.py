# -*- coding: utf-8 -*-
"""
シリーズB「呪詛版」2セット目 16枚
テーマ：壊れの実況 ── 1セット目が「外へ投げる黒さ」なのに対し、こちらは
「自分の内側が壊れていくのを他人事として報告する」内向きの黒さで束ねる。
1セット目で凍結した24案から16枚を選抜。
"""
from sticker_engine import SUMI, CHI, HAI, render_set

STICKERS = [
 ("心、先に退勤した", {"blocks":[
    {"text":"心、","font":"min_l","size":38,"color":HAI},
    {"text":"先に退勤した","font":"min_m","size":54,"color":SUMI,"gap":6},
 ]}),
 ("会話が成立しない", {"blocks":[
    {"text":"会話が成立しない","font":"sans_l","size":40,"color":HAI,"spacing":2},
 ]}),
 ("まだ手が震えてる", {"blocks":[
    {"text":"まだ手が","font":"maru","size":44,"color":SUMI,"jitter":2.0,"seed":2},
    {"text":"震えてる","font":"maru","size":60,"color":SUMI,"gap":6,"jitter":2.2,"seed":7},
 ]}),
 ("上を出せ、私も出したい", {"blocks":[
    {"text":"上を出せ、","font":"min_l","size":40,"color":SUMI},
    {"text":"私も出したい","font":"min_m","size":52,"color":CHI,"gap":8},
 ]}),
 ("感情、在庫切れ", {"blocks":[
    {"text":"感情、","font":"sans_l","size":38,"color":HAI},
    {"text":"在庫切れ","font":"sans_l","size":62,"color":SUMI,"gap":6},
 ]}),
 ("名乗った瞬間終わった", {"blocks":[
    {"text":"名乗った瞬間","font":"black","size":42,"color":SUMI},
    {"text":"終わった","font":"black","size":62,"color":SUMI,"gap":2},
 ]}),
 ("もう痛くない", {"blocks":[
    {"text":"もう痛くない","font":"min_l","size":46,"color":HAI},
 ]}),
 ("途中から記憶がない", {"blocks":[
    {"text":"途中から","font":"sans_l","size":36,"color":HAI},
    {"text":"記憶がない","font":"sans_l","size":52,"color":SUMI,"gap":6},
 ]}),
 ("録音、残ってます", {"blocks":[
    {"text":"録音、","font":"sans_l","size":36,"color":SUMI},
    {"text":"残ってます","font":"sans_l","size":54,"color":SUMI,"gap":6},
 ]}),
 ("私の声じゃない", {"blocks":[
    {"text":"私の声じゃない","font":"min_l","size":46,"color":HAI,"jitter":1.3,"seed":4},
 ]}),
 ("笑いながら削れてる", {"blocks":[
    {"text":"笑いながら","font":"min_l","size":40,"color":SUMI},
    {"text":"削れてる","font":"min_m","size":56,"color":CHI,"gap":8},
 ]}),
 ("番号、覚えました", {"blocks":[
    {"text":"番号、","font":"min_l","size":38,"color":SUMI},
    {"text":"覚えました","font":"min_m","size":54,"color":SUMI,"gap":8},
 ]}),
 ("代わりはいるらしい", {"blocks":[
    {"text":"代わりはいる","font":"min_l","size":44,"color":SUMI},
    {"text":"らしい","font":"min_l","size":30,"color":HAI,"gap":10,"align":"right"},
 ]}),
 ("二度と鳴らないで", {"blocks":[
    {"text":"二度と鳴らないで","font":"min_l","size":42,"color":CHI},
 ]}),
 ("離席が罪になる職場", {"blocks":[
    {"text":"離席が","font":"sans_l","size":36,"color":HAI},
    {"runs":[("罪",CHI),("になる職場",SUMI)],"font":"sans_l","size":48,"gap":6},
 ]}),
 ("謝罪はタダだと思ってる", {"blocks":[
    {"text":"謝罪はタダだと","font":"min_l","size":38,"color":SUMI},
    {"text":"思ってる","font":"min_m","size":54,"color":CHI,"gap":8},
 ]}),
]

MAIN = {"blocks":[
    {"text":"心、","font":"min_l","size":28,"color":HAI},
    {"text":"先に退勤した","font":"min_m","size":34,"color":SUMI,"gap":6},
]}
TAB = {"blocks":[{"text":"退勤","font":"black","size":23,"color":SUMI}]}

if __name__ == "__main__":
    problems = render_set("stickers/set2", 'シリーズB「呪詛版」2セット目 16枚',
                          STICKERS, MAIN, TAB)
    print("set2:", problems or "検証OK（余白10px以上・全枚数透過）")
