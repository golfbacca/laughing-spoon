# -*- coding: utf-8 -*-
"""
シリーズB「呪詛版」1セット目 16枚
テーマ：実況と連帯 ── オープンチャットに投げる、外へ向いた黒さ
"""
from sticker_engine import SUMI, CHI, HAI, render_set

STICKERS = [
 ("今、修羅場です", {"blocks":[
    {"text":"今、","font":"black","size":44,"color":SUMI},
    {"text":"修羅場です","font":"black","size":66,"color":CHI,"gap":4},
 ]}),
 ("私が決めた規約じゃない", {"blocks":[
    {"text":"私が","font":"black","size":46,"color":CHI},
    {"text":"決めた規約","font":"black","size":54,"color":SUMI,"gap":2},
    {"text":"じゃない","font":"black","size":54,"color":SUMI,"gap":2},
 ]}),
 ("助けて、は言えない", {"blocks":[
    {"text":"助けて","font":"min_m","size":86,"color":CHI},
    {"text":"は言えない","font":"min_l","size":26,"color":HAI,"gap":14,"align":"right"},
 ]}),
 ("本日の被弾報告", {"blocks":[
    {"text":"本日の被弾報告","font":"min_r","size":44,"color":SUMI,"spacing":6},
    {"type":"rule","width":296,"thick":3,"color":SUMI,"gap":14},
 ]}),
 ("隣の席、静かになった", {"blocks":[
    {"text":"隣の席、","font":"min_l","size":40,"color":SUMI},
    {"text":"静かになった","font":"min_l","size":44,"color":SUMI,"gap":38},
 ]}),
 ("今の、生き物だった", {"blocks":[
    {"text":"今の、","font":"min_l","size":38,"color":SUMI},
    {"runs":[("生き物",CHI),("だった",SUMI)],"font":"min_m","size":50,"spacing":4,"gap":8},
 ]}),
 ("まだ辞めてない", {"blocks":[
    {"text":"まだ","font":"min_m","size":66,"color":CHI,"align":"left"},
    {"text":"辞めてない","font":"min_l","size":44,"color":HAI,"gap":6,"align":"right"},
 ]}),
 ("明日も鳴る、必ず", {"blocks":[
    {"text":"明日も鳴る、","font":"min_l","size":40,"color":SUMI},
    {"text":"必ず","font":"min_m","size":84,"color":CHI,"gap":12},
 ]}),
 ("生きてる人、挙手", {"blocks":[
    {"text":"生きてる人、","font":"maru","size":42,"color":SUMI,"jitter":1.7,"seed":3},
    {"text":"挙手","font":"maru","size":72,"color":SUMI,"gap":4,"jitter":1.7,"seed":5},
 ], "rotate":-4}),
 ("誰か代わって（無理か）", {"blocks":[
    {"text":"誰か代わって","font":"maru","size":52,"color":SUMI},
    {"text":"（無理か）","font":"maru","size":28,"color":HAI,"gap":10,"align":"right","alpha":0.82},
 ]}),
 ("今の、通報案件", {"blocks":[
    {"text":"今の、","font":"black","size":34,"color":SUMI},
    {"text":"通報","font":"black","size":80,"color":CHI,"gap":2},
    {"text":"案件","font":"black","size":44,"color":SUMI,"gap":2},
 ]}),
 ("守ってもらえない側", {"blocks":[
    {"type":"vertical","text":"守ってもらえない側","font":"min_l","size":32,"color":HAI,
     "line":1.0,"dx":58},
 ]}),
 ("人間の消耗品です", {"blocks":[
    {"text":"人間の消耗品です","font":"min_l","size":40,"color":SUMI,"spacing":3},
 ], "dy":30}),
 ("同業しかわからない", {"blocks":[
    {"type":"vertical","text":["同業しか","わからない"],"font":"min_l","size":46,"color":SUMI,
     "line":1.0,"dx":30},
 ]}),
 ("これ読める人は仲間", {"blocks":[
    {"text":"これ読める人は","font":"sans_l","size":38,"color":SUMI,"spacing":2},
    {"text":"仲間","font":"sans_l","size":58,"color":CHI,"gap":10},
 ]}),
 ("明日も生きてたら会おう", {"blocks":[
    {"text":"明日も生きてたら","font":"min_l","size":38,"color":SUMI},
    {"text":"会おう","font":"min_l","size":38,"color":SUMI,"gap":10},
 ]}),
]

MAIN = {"blocks":[
    {"text":"今、","font":"black","size":32,"color":SUMI},
    {"text":"修羅場です","font":"black","size":46,"color":CHI,"gap":4},
]}
TAB = {"blocks":[{"text":"修羅場","font":"black","size":23,"color":SUMI}]}

if __name__ == "__main__":
    problems = render_set("stickers/set1", 'シリーズB「呪詛版」1セット目 16枚',
                          STICKERS, MAIN, TAB)
    print("set1:", problems or "検証OK（余白10px以上・全枚数透過）")
