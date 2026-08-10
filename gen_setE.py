# -*- coding: utf-8 -*-
"""
シリーズE「未経験版」1セット目 16枚 ── 部活動顧問（専門外）界隈向け

ターゲットは「教員全体」ではなく、文科省 教員勤務実態調査（H28）の
★中学校で担当教科が保健体育ではなく、かつ担当部活動の競技の経験も
　ない教員＝45.9%★ に絞ってある。母数10万人規模。

シリーズCが「見られていない黒さ」、Dが「間違われている黒さ」なのに対し、
Eは★「やったことがないのにやらされている黒さ」★。
顧問は選べない。競技も選べない。土日も最初から決まっている。

★宛先の設計：この界隈は宛先の選択肢が無い。
　①保護者 …★絶対NG★。教員が保護者を揶揄すると実際に問題になる
　②生徒　 …★絶対NG★。職業ごと燃える
　③管理職 … 上司。NG
　→ ④制度（土日・手当・大会・専門外・勤務時間）しか残らない。
　　 選択肢が無いことが、かえって設計の迷いを消している。

★生徒を守る札を必ず1枚入れること（15番）★
　16枚の中に「生徒は悪くない」が入っていることで、セット全体が
　「生徒への不満」ではなく「制度への不満」だと読める。
　この1枚が無いと、同じ16枚が炎上材料になりうる。
"""
from sticker_engine import SUMI, CHI, HAI, render_set

STICKERS = [
 ("今日も部活です", {"blocks":[
    {"text":"今日も","font":"sans_l","size":38,"color":HAI},
    {"text":"部活です","font":"black","size":62,"color":SUMI,"gap":6},
 ]}),
 ("経験者は生徒のほう", {"blocks":[
    {"text":"経験者は","font":"min_l","size":42,"color":HAI},
    {"text":"生徒のほう","font":"min_m","size":54,"color":SUMI,"gap":8},
 ]}),
 ("ルール、昨日覚えました", {"blocks":[
    {"text":"ルール、","font":"min_l","size":38,"color":HAI},
    {"text":"昨日覚えました","font":"min_m","size":48,"color":SUMI,"gap":8},
 ]}),
 ("本日の勤務時間", {"blocks":[
    {"text":"本日の勤務時間","font":"min_r","size":44,"color":SUMI,"spacing":6},
    {"type":"rule","width":296,"thick":3,"color":SUMI,"gap":14},
 ]}),
 ("専門、違います", {"blocks":[
    {"text":"専門、","font":"sans_l","size":36,"color":HAI},
    {"text":"違います","font":"sans_l","size":56,"color":SUMI,"gap":6},
 ]}),
 ("まだ、顧問です", {"blocks":[
    {"text":"まだ、","font":"min_m","size":62,"color":CHI,"align":"left"},
    {"text":"顧問です","font":"min_l","size":44,"color":HAI,"gap":6,"align":"right"},
 ]}),
 ("授業の準備はいつ", {"blocks":[
    {"text":"授業の準備は","font":"min_l","size":40,"color":SUMI},
    {"text":"いつ","font":"min_m","size":72,"color":CHI,"gap":12},
 ]}),
 ("日曜も、あります", {"blocks":[
    {"text":"日曜も、","font":"min_l","size":40,"color":SUMI},
    {"text":"あります","font":"min_m","size":64,"color":CHI,"gap":10},
 ]}),
 ("初勝利、しました", {"blocks":[
    {"text":"初勝利、","font":"maru","size":42,"color":SUMI,"jitter":1.7,"seed":3},
    {"text":"しました","font":"maru","size":66,"color":SUMI,"gap":4,"jitter":1.7,"seed":5},
 ], "rotate":-4}),
 ("教えられます（たぶん）", {"blocks":[
    {"text":"教えられます","font":"maru","size":44,"color":SUMI},
    {"text":"（たぶん）","font":"maru","size":26,"color":HAI,"gap":10,"align":"right","alpha":0.82},
 ]}),
 ("実質、無償です", {"blocks":[
    {"text":"実質、","font":"black","size":34,"color":SUMI},
    {"text":"無償","font":"black","size":80,"color":CHI,"gap":2},
    {"text":"です","font":"black","size":44,"color":SUMI,"gap":2},
 ]}),
 ("代わりがいません", {"blocks":[
    {"type":"vertical","text":"代わりがいません","font":"min_l","size":32,"color":HAI,
     "line":1.0,"dx":58},
 ]}),
 ("土日は、ありました", {"blocks":[
    {"text":"土日は、ありました","font":"min_l","size":34,"color":SUMI,"spacing":2},
 ], "dy":30}),
 ("顧問にしかわからない", {"blocks":[
    {"type":"vertical","text":["顧問にしか","わからない"],"font":"min_l","size":46,"color":SUMI,
     "line":1.0,"dx":30},
 ]}),
 ("生徒は悪くないんです", {"blocks":[
    {"text":"生徒は","font":"sans_l","size":34,"color":SUMI,"spacing":2},
    {"text":"悪くないんです","font":"sans_l","size":46,"color":SUMI,"gap":10},
 ]}),
 ("来週も、行きます", {"blocks":[
    {"text":"来週も、","font":"min_l","size":32,"color":SUMI},
    {"text":"行きます","font":"min_l","size":32,"color":SUMI,"gap":10},
 ]}),
]

MAIN = {"blocks":[
    {"text":"今日も","font":"sans_l","size":26,"color":HAI},
    {"text":"部活です","font":"black","size":44,"color":SUMI,"gap":6},
]}
TAB = {"blocks":[{"text":"部活","font":"black","size":28,"color":SUMI}]}

if __name__ == "__main__":
    problems = render_set("stickers/setE", 'シリーズE「未経験版」1セット目 16枚',
                          STICKERS, MAIN, TAB)
    print("setE:", problems or "検証OK（余白10px以上・全枚数透過）")
