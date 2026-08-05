# -*- coding: utf-8 -*-
"""
シリーズA「諦念版」16枚（キャラクター入り）
テーマ：健気な諦念 ── 誰も呪わず、自分の状態をただ報告する

シリーズBが墨と血の冷たい配色・明朝／極太で組まれているのに対し、
こちらはキャラクターの実測色に合わせた温かい配色と丸ゴシックで組む。
別ラインであることが一目でわかる状態にしてある。
"""
from sticker_engine import render_set

# キャラクター画像から実測した色（tools/cutout.py で切り抜いた PNG を採色）
SUMI_A  = (55, 50, 43, 255)     # 線と同じチャコール #37322B
TERRA   = (187, 121, 99, 255)   # マイクのテラコッタ #BB7963
SLATE   = (116, 133, 132, 255)  # ヘッドセットのスレート #748584

A = "assets_charA/"


def S(text_blocks, char, char_area=46000, dy=0):
    return {"blocks": text_blocks + [
        {"type": "char", "path": A + char, "area": char_area, "gap": 10}], "dy": dy}


def T(text, size=36, color=SUMI_A, **kw):
    return dict(text=text, font="maru", size=size, color=color, **kw)


STICKERS = [
 ("私は悪くない、たぶん", S([T("私は悪くない、", 34),
                            T("たぶん", 30, SLATE, gap=2, align="right")], "01.png")),
 ("声だけ元気だった",     S([T("声だけ元気だった", 36)], "02.png")),
 ("息、してた？私",       S([T("息、してた？私", 36)], "03.png")),
 ("謝る係、今日も",       S([T("謝る係、今日も", 36)], "04.png")),
 ("保留で深呼吸してる",   S([T("保留で深呼吸してる", 32)], "05.png")),
 ("トイレが一番静か",     S([T("トイレが一番静か", 34)], "06.png")),
 ("上を出せ、出しました", S([T("上を出せ、", 30),
                            T("出しました", 36, gap=2)], "07.png")),
 ("ガチャ切り、ありがとう", S([T("ガチャ切り、", 30),
                              T("ありがとう", 36, TERRA, gap=2)], "08.png")),
 ("30分、同じ話",       S([T("30分、同じ話", 36)], "09.png")),
 ("電話、鳴らないで",     S([T("電話、鳴らないで", 34, TERRA)], "10.png")),
 ("笑顔で話せ、だって",   S([T("笑顔で話せ、", 32),
                            T("だって", 30, SLATE, gap=2, align="right")], "11.png")),
 ("切った瞬間また鳴る",   S([T("切った瞬間また鳴る", 32)], "12.png")),
 ("家でも着信音がする",   S([T("家でも着信音がする", 32)], "13.png")),
 ("まだ声が出る",         S([T("まだ声が出る", 40, TERRA)], "14.png")),
 ("今日のぶん、終わった", S([T("今日のぶん、終わった", 32)], "15.png")),
 ("お茶が冷めてる",       S([T("お茶が冷めてる", 36)], "16.png")),
]

MAIN = {"blocks": [
    T("私は悪くない、", 24),
    dict(T("たぶん", 22, SLATE), gap=2, align="right"),
    {"type": "char", "path": A + "01.png", "area": 15000, "gap": 6},
]}
TAB = {"blocks": [{"type": "char", "path": A + "KAKUTEI_Single.png", "area": 3400}]}

if __name__ == "__main__":
    problems = render_set("stickers/setA", 'シリーズA「諦念版」16枚',
                          STICKERS, MAIN, TAB)
    print("setA:", problems or "検証OK（余白10px以上・全枚数透過）")
