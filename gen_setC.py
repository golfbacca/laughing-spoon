# -*- coding: utf-8 -*-
"""
シリーズC「不可視版」1セット目 16枚 ── 歯科技工士界隈向け

シリーズBが「攻撃されている黒さ」（客・カスハラ）なのに対し、
こちらは「見られていない黒さ」で束ねる。
削ったものは口の中に入って二度と見られず、作った人の名前はどこにも出ない。

★宛先の設計：技工士の不満の最大の鉱脈は歯科医師・指示書だが、そこは
　取引先であり同じLINEグループにいることもある。人を直接叩く札を作ると
　「職場で使えないスタンプ」になるため、攻撃先は指示書・納期・再製という
　無生物にずらしてある（主語を書かない設計はシリーズBと共通）。
"""
from sticker_engine import SUMI, CHI, HAI, render_set

STICKERS = [
 ("今日も技工です", {"blocks":[
    {"text":"今日も","font":"sans_l","size":38,"color":HAI},
    {"text":"技工です","font":"black","size":68,"color":SUMI,"gap":6},
 ]}),
 ("咬合器の上では完璧だった", {"blocks":[
    {"text":"咬合器の上では","font":"min_l","size":40,"color":SUMI},
    {"text":"完璧だった","font":"min_m","size":54,"color":CHI,"gap":8},
 ]}),
 ("口の中で、一生見られない", {"blocks":[
    {"text":"口の中で、","font":"min_l","size":36,"color":HAI},
    {"text":"一生見られない","font":"min_m","size":48,"color":SUMI,"gap":8},
 ]}),
 ("本日の再製報告", {"blocks":[
    {"text":"本日の再製報告","font":"min_r","size":44,"color":SUMI,"spacing":6},
    {"type":"rule","width":296,"thick":3,"color":SUMI,"gap":14},
 ]}),
 ("指示書、シェードが無い", {"blocks":[
    {"text":"指示書、","font":"sans_l","size":36,"color":SUMI},
    {"text":"シェードが無い","font":"sans_l","size":46,"color":SUMI,"gap":6},
 ]}),
 ("まだ、この仕事です", {"blocks":[
    {"text":"まだ、","font":"min_m","size":62,"color":CHI,"align":"left"},
    {"text":"この仕事です","font":"min_l","size":42,"color":HAI,"gap":6,"align":"right"},
 ]}),
 ("爪は、黒いまま", {"blocks":[
    {"text":"爪は、","font":"min_l","size":36,"color":HAI},
    {"text":"黒いまま","font":"min_m","size":58,"color":SUMI,"gap":8},
 ]}),
 ("明日まで、が常態", {"blocks":[
    {"text":"明日まで、","font":"min_l","size":40,"color":SUMI},
    {"text":"が常態","font":"min_m","size":72,"color":CHI,"gap":12},
 ]}),
 ("適合、良好", {"blocks":[
    {"text":"適合、","font":"maru","size":42,"color":SUMI,"jitter":1.7,"seed":3},
    {"text":"良好","font":"maru","size":80,"color":SUMI,"gap":4,"jitter":1.7,"seed":5},
 ], "rotate":-4}),
 ("誰にも会ってない（平気）", {"blocks":[
    {"text":"誰にも会ってない","font":"maru","size":40,"color":SUMI},
    {"text":"（平気）","font":"maru","size":26,"color":HAI,"gap":10,"align":"right","alpha":0.82},
 ]}),
 ("作った人はここにいない", {"blocks":[
    {"text":"作った人は","font":"black","size":40,"color":SUMI},
    {"text":"ここにいない","font":"black","size":54,"color":SUMI,"gap":2},
 ]}),
 ("換気扇の音だけ", {"blocks":[
    {"type":"vertical","text":"換気扇の音だけ","font":"min_l","size":34,"color":HAI,
     "line":1.0,"dx":58},
 ]}),
 ("削った分は戻らない", {"blocks":[
    {"text":"削った分は戻らない","font":"min_l","size":36,"color":SUMI,"spacing":2},
 ], "dy":30}),
 ("技工士にしか通じない", {"blocks":[
    {"type":"vertical","text":["技工士にしか","通じない"],"font":"min_l","size":46,"color":SUMI,
     "line":1.0,"dx":30},
 ]}),
 ("気づかれないのが成功", {"blocks":[
    {"text":"気づかれないのが","font":"sans_l","size":36,"color":SUMI,"spacing":2},
    {"text":"成功","font":"sans_l","size":72,"color":SUMI,"gap":10},
 ]}),
 ("朝までに、なんとかします", {"blocks":[
    {"text":"朝までに、","font":"min_l","size":32,"color":SUMI},
    {"text":"なんとかします","font":"min_l","size":32,"color":SUMI,"gap":10},
 ]}),
]

MAIN = {"blocks":[
    {"text":"今日も","font":"sans_l","size":28,"color":HAI},
    {"text":"技工です","font":"black","size":48,"color":SUMI,"gap":6},
]}
TAB = {"blocks":[{"text":"技工","font":"black","size":28,"color":SUMI}]}

if __name__ == "__main__":
    problems = render_set("stickers/setC", 'シリーズC「不可視版」1セット目 16枚',
                          STICKERS, MAIN, TAB)
    print("setC:", problems or "検証OK（余白10px以上・全枚数透過）")
