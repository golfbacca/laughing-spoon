# -*- coding: utf-8 -*-
"""2サイズ併記のサイズ図（出品画像5枚目の差し替え版）"""
from PIL import Image, ImageDraw
import listing_img as L

W,H=L.W,L.H
def img_size_two(tag, out):
    base=Image.new("RGB",(W,H),L.CREAM); d=ImageDraw.Draw(base)
    f1=L.F(72,"Bold"); f2=L.F(40,"SemiBold"); f3=L.F(30,"Medium"); f4=L.F(34,"Bold")
    L.text(d,(W//2,52),"TWO SIZES",f1,L.INK,"ma")
    L.text(d,(W//2,140),"Pick your size at checkout",f3,L.SUB,"ma")

    small_h=560                      # 12x18
    big_h  =int(small_h*32/18)       # 24.5x32 を同じ縮尺で
    # ハウスは実際の入稿データ（7800x10012）の裁ち範囲から描く。引き伸ばさない
    big =L.flat_flag(f"house/{tag}_SMITHS_house_7800x10012.png", big_h, (225,206,7575,9806))
    small=L.flat_flag(f"named_r/{tag}_SMITHS_3900x5700.png", small_h, L.TRIM)
    gap=180
    tot=big.width+gap+small.width; x=(W-tot)//2
    by=200; sy=by+big.height-small.height          # 下端をそろえる
    base.paste(big,(x,by),big); base.paste(small,(x+big.width+gap,sy),small)

    for cx,lab,sub,ww in ((x+big.width//2, 'HOUSE FLAG', '24.5 x 32 in  ·  62 x 81 cm', big.width),
                          (x+big.width+gap+small.width//2, 'GARDEN FLAG', '12 x 18 in  ·  30 x 46 cm', small.width)):
        L.text(d,(cx,by+big.height+26),lab,f4,L.ACC,"ma")
        L.text(d,(cx,by+big.height+76),sub,f3,L.INK,"ma")
    L.rule(d,by+big.height+140)
    L.text(d,(W//2,by+big.height+176),
           "The house flag is about 3.6x the area. Both are printed on both sides.",
           f3,L.SUB,"ma")
    base.save(out,quality=92,subsampling=0)

if __name__=="__main__":
    import os
    os.makedirs("size2",exist_ok=True)
    for t in ("R01","R02","R05","R09","R11"):
        img_size_two(t, f"size2/{t}_5_size.jpg"); print("  ",t)
    from PIL import Image as I
    o=I.new("RGB",(430*5+60,323+20),(255,255,255))
    for i,t in enumerate(("R01","R02","R05","R09","R11")):
        o.paste(I.open(f"size2/{t}_5_size.jpg").resize((430,323),I.LANCZOS),(10+i*440,10))
    o.save("size2_sheet.png"); print("saved")
