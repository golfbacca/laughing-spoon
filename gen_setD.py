# -*- coding: utf-8 -*-
"""
シリーズD「誤認版」1セット目 16枚 ── 歯科衛生士界隈向け

シリーズCが「見られていない黒さ」（歯科技工士）なのに対し、
Dは「間違われている黒さ」で束ねる。

  職業の誤認　　… 国家資格なのに「助手さん」と呼ばれる
  所要時間の誤認… 15分枠に詰められる
  自己認識の誤認… 患者は「磨いてます」と言う
  可逆性の誤認　… 歯は戻ると思われている
  仕事の中身の誤認… 何と戦っているか誰も知らない

★宛先の設計：歯科衛生士の痛点は院長・歯科医師・同僚にも向くが、
　そこは雇用主と職場内。歯科医院は小規模でLINEに院長がいることも多い。
　一方★患者は外部で匿名★なので、シリーズB（コルセン）の
　「外へ投げる黒さ」がそのまま使える。技工士版のように無生物へ
　ずらす必要が薄い。ただし医療職が患者を揶揄する形は炎上リスクが
　あるため、直接的な揶揄は避け、予約・時間・自分の身体側へ寄せてある。
"""
from sticker_engine import SUMI, CHI, HAI, render_set

STICKERS = [
 ("今日も口の中です", {"blocks":[
    {"text":"今日も","font":"sans_l","size":38,"color":HAI},
    {"text":"口の中です","font":"black","size":58,"color":SUMI,"gap":6},
 ]}),
 ("助手さんじゃないです", {"blocks":[
    {"text":"助手さん","font":"min_l","size":42,"color":HAI},
    {"text":"じゃないです","font":"min_m","size":54,"color":CHI,"gap":8},
 ]}),
 ("また、来なかった", {"blocks":[
    {"text":"また、","font":"min_l","size":38,"color":HAI},
    {"text":"来なかった","font":"min_m","size":56,"color":SUMI,"gap":8},
 ]}),
 ("本日のキャンセル", {"blocks":[
    {"text":"本日のキャンセル","font":"min_r","size":36,"color":SUMI,"spacing":6},
    {"type":"rule","width":296,"thick":3,"color":SUMI,"gap":14},
 ]}),
 ("15分で終わるわけない", {"blocks":[
    {"text":"15分で","font":"sans_l","size":36,"color":HAI},
    {"text":"終わるわけない","font":"sans_l","size":48,"color":SUMI,"gap":6},
 ]}),
 ("まだ、ここにいる", {"blocks":[
    {"text":"まだ、","font":"min_m","size":62,"color":CHI,"align":"left"},
    {"text":"ここにいる","font":"min_l","size":42,"color":HAI,"gap":6,"align":"right"},
 ]}),
 ("指、割れてます", {"blocks":[
    {"text":"指、","font":"min_l","size":36,"color":HAI},
    {"text":"割れてます","font":"min_m","size":56,"color":SUMI,"gap":8},
 ]}),
 ("リコール、返事なし", {"blocks":[
    {"text":"リコール、","font":"sans_l","size":36,"color":SUMI},
    {"text":"返事なし","font":"sans_l","size":54,"color":SUMI,"gap":6},
 ]}),
 ("歯石、取れました", {"blocks":[
    {"text":"歯石、","font":"maru","size":42,"color":SUMI,"jitter":1.7,"seed":3},
    {"text":"取れました","font":"maru","size":66,"color":SUMI,"gap":4,"jitter":1.7,"seed":5},
 ], "rotate":-4}),
 ("磨いてます（そうですか）", {"blocks":[
    {"text":"磨いてます","font":"maru","size":46,"color":SUMI},
    {"text":"（そうですか）","font":"maru","size":26,"color":HAI,"gap":10,"align":"right","alpha":0.82},
 ]}),
 ("予約、詰めすぎです", {"blocks":[
    {"text":"予約、","font":"black","size":34,"color":SUMI},
    {"text":"詰めすぎ","font":"black","size":72,"color":CHI,"gap":2},
    {"text":"です","font":"black","size":40,"color":SUMI,"gap":2},
 ]}),
 ("口の中しか見てない", {"blocks":[
    {"type":"vertical","text":"口の中しか見てない","font":"min_l","size":32,"color":HAI,
     "line":1.0,"dx":58},
 ]}),
 ("歯は、戻りません", {"blocks":[
    {"text":"歯は、戻りません","font":"min_l","size":36,"color":SUMI,"spacing":2},
 ], "dy":30}),
 ("衛生士にしか通じない", {"blocks":[
    {"type":"vertical","text":["衛生士にしか","通じない"],"font":"min_l","size":46,"color":SUMI,
     "line":1.0,"dx":30},
 ]}),
 ("見えない歯石と戦ってる", {"blocks":[
    {"text":"見えない歯石と","font":"sans_l","size":34,"color":SUMI,"spacing":2},
    {"text":"戦ってる","font":"sans_l","size":52,"color":SUMI,"gap":10},
 ]}),
 ("また来てくださいね", {"blocks":[
    {"text":"また来て","font":"min_l","size":32,"color":SUMI},
    {"text":"くださいね","font":"min_l","size":32,"color":SUMI,"gap":10},
 ]}),
]

MAIN = {"blocks":[
    {"text":"今日も","font":"sans_l","size":26,"color":HAI},
    {"text":"口の中です","font":"black","size":40,"color":SUMI,"gap":6},
]}
TAB = {"blocks":[{"text":"歯石","font":"black","size":28,"color":SUMI}]}

if __name__ == "__main__":
    problems = render_set("stickers/setD", 'シリーズD「誤認版」1セット目 16枚',
                          STICKERS, MAIN, TAB)
    print("setD:", problems or "検証OK（余白10px以上・全枚数透過）")
