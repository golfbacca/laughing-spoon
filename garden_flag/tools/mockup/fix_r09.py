# -*- coding: utf-8 -*-
"""R09 のタータン枠：欠落している緑ブロックを1つ補う（案A）

実測したセット（上バーの横方向＝正しい繰り返し）:
    緑204 / 赤38 / 緑203 / 赤145 / 細緑27 / 赤145   → 1周期 762px

左右の帯（縦方向）の「広い緑ブロックの対」の位置:
    (952,1163) (1845,2097) (2505,2745) (3284,3491) (4229, ????) (4991,5198)
    → 4229 の相方が無い。セットどおりなら 4229+200+38 = 4467 にあるはず。
      実際にはそこに細い緑(4580, 高さ31)があるだけ。

対応: 既存の広いブロック(y2745, 高さ204)を y4467 へ複製する。
      ブロックの上下は「赤→ハッチ→赤」の硬い切り替わりなので、
      綾織りの斜線の位相合わせは不要（斜線はブロックを挟んで途切れる）。
"""
from PIL import Image
import numpy as np

SRC="upload_r/_R09_before.png"
DST="upload_r/R09_upload_3900x5700.png"
BANDS=[(440,670),(3228,3458)]     # 左帯・右帯（クリーム地の余白ごと）
SRC_Y=(2745,2949)                 # 複製元の広い緑ブロック（高さ204）
DST_Y=4467                        # セットが示す欠落位置

def main():
    im=Image.open(SRC).convert("RGB")
    a=np.asarray(im).astype(np.uint8).copy()
    h=SRC_Y[1]-SRC_Y[0]
    for x0,x1 in BANDS:
        a[DST_Y:DST_Y+h, x0:x1]=a[SRC_Y[0]:SRC_Y[1], x0:x1]
    Image.fromarray(a).save(DST, optimize=True)
    print(f"y {SRC_Y[0]}〜{SRC_Y[1]} の緑ブロック(高さ{h}px)を y {DST_Y}〜{DST_Y+h} へ複製")
    print("保存:", DST)

if __name__=="__main__": main()
