# -*- coding: utf-8 -*-
"""シリーズC 01番の差し替え候補を、スタンプ／メイン／タブの3点セットで比較する。

01「今日も削ってます」は stickers/setC/01.png であると同時に
メイン画像とタブ画像の元にもなっている。つまり1枚の文言変更が
★ストアのサムネイルとトークルームのタブ★まで変える。
だから候補は必ずこの3点セットで見比べること。

背景：ココナラの現役技工士から「①今日も削っています→何を削っているのか？」
という質問が来た。あわせて公開情報でも
  ・職業紹介での技工士の仕事は「製作・加工・修理」と書かれ、削るは前面に出ない
  ・「歯を削る」は歯科医師の作業として強く定着している
という材料が出ており、「削る」が技工士の自称動詞として最適か未確定。

出力： stickers/_compare/setC01_light.png / setC01_dark.png
       stickers/_compare/setC06_light.png / setC06_dark.png
★_compare は検討用。申請には絶対に使わないこと★
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw
from sticker_engine import SUMI, CHI, HAI, WHITE, build, F

OUT = "stickers/_compare"


def st(second, size):
    """01番のスタンプ本体（370x320）。1行目は全候補で共通。"""
    return {"blocks": [
        {"text": "今日も", "font": "sans_l", "size": 38, "color": HAI},
        {"text": second, "font": "black", "size": size, "color": SUMI, "gap": 6},
    ]}


def main_spec(second, size):
    return {"blocks": [
        {"text": "今日も", "font": "sans_l", "size": 28, "color": HAI},
        {"text": second, "font": "black", "size": size, "color": SUMI, "gap": 6},
    ]}


def tab_spec(text):
    return {"blocks": [{"text": text, "font": "black", "size": 28, "color": SUMI}]}


# (見出し, 2行目, スタンプの字送り, メインの字送り, タブ文言, 備考)
V01 = [
    ("A 今日も削ってます（現行）", "削ってます", 60, 42, "削る",
     "身体性は一番強い。ただし「歯を削る」は歯科医師の作業と読める余地"),
    ("B 今日も技工です",           "技工です",   68, 48, "技工",
     "「技工」は界隈の自称語で曖昧さゼロ。D/Eと構造が揃う"),
    ("C 今日も納期です",           "納期です",   68, 48, "納期",
     "納期は技工士の核。毎日ある。ただし動詞ではなく状態"),
    ("D 今日も作ってます",         "作ってます", 60, 42, "作る",
     "最も安全だが、誰にでも言えるので界隈語として弱い"),
]

V06 = [
    ("A まだ削ってる（現行）", [("まだ", "min_m", 66, CHI, "left"),
                                ("削ってる", "min_l", 44, HAI, "right")]),
    ("B まだ技工してる",       [("まだ", "min_m", 66, CHI, "left"),
                                ("技工してる", "min_l", 42, HAI, "right")]),
    ("C まだ続けてる",         [("まだ", "min_m", 66, CHI, "left"),
                                ("続けてる", "min_l", 44, HAI, "right")]),
]


def spec06(blocks):
    out = []
    for i, (text, font, size, color, align) in enumerate(blocks):
        b = {"text": text, "font": font, "size": size, "color": color, "align": align}
        if i:
            b["gap"] = 6
        out.append(b)
    return {"blocks": out}


def label(draw, x, y, text, size, color):
    draw.text((x, y), text, font=F("sans_l", size), fill=color)


def sheet01(bg, fg, sub, fname):
    pad, lab_w = 20, 300
    row_h = 340
    w = lab_w + 370 + 240 + 96 + pad * 5
    h = row_h * len(V01) + pad * 2
    img = Image.new("RGBA", (w, h), bg)
    d = ImageDraw.Draw(img)
    for i, (name, second, s_sz, m_sz, tab, note) in enumerate(V01):
        y = pad + i * row_h
        label(d, pad, y + 90, name, 24, fg)
        # 備考は折り返して2行まで
        for j in range(0, len(note), 17):
            label(d, pad, y + 130 + (j // 17) * 26, note[j:j + 17], 17, sub)
        x = pad * 2 + lab_w
        img.alpha_composite(build(st(second, s_sz)), (x, y))
        x += 370 + pad
        img.alpha_composite(build(main_spec(second, m_sz), size=(240, 240)), (x, y + 40))
        x += 240 + pad
        img.alpha_composite(build(tab_spec(tab), size=(96, 74), margin=5), (x, y + 123))
    img.convert("RGB").save(os.path.join(OUT, fname), quality=95)


def sheet06(bg, fg, fname):
    pad, lab_w = 20, 260
    row_h = 340
    w = lab_w + 370 + pad * 3
    h = row_h * len(V06) + pad * 2
    img = Image.new("RGBA", (w, h), bg)
    d = ImageDraw.Draw(img)
    for i, (name, blocks) in enumerate(V06):
        y = pad + i * row_h
        label(d, pad, y + 140, name, 24, fg)
        img.alpha_composite(build(spec06(blocks)), (pad * 2 + lab_w, y))
    img.convert("RGB").save(os.path.join(OUT, fname), quality=95)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sheet01((238, 239, 241, 255), (26, 26, 26, 255), (120, 120, 120, 255), "setC01_light.png")
    sheet01((28, 28, 30, 255), (235, 235, 235, 255), (150, 150, 150, 255), "setC01_dark.png")
    sheet06((238, 239, 241, 255), (26, 26, 26, 255), "setC06_light.png")
    sheet06((28, 28, 30, 255), (235, 235, 235, 255), "setC06_dark.png")
    print("比較シートを", OUT, "に出力しました（申請には使わないこと）")
