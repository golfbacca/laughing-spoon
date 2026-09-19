# -*- coding: utf-8 -*-
"""出品画像7枚を作る（2000x1500 / 4:3 — Etsyの一覧に合わせた比率）"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, os

W,H=2000,1500
CREAM=(249,246,240); INK=(38,42,38); SUB=(104,110,104); ACC=(22,86,52); WARN=(150,40,30)
FONT="fonts/Montserrat.ttf"

def F(size, weight="SemiBold"):
    f=ImageFont.truetype(FONT,size); f.set_variation_by_name(weight); return f

def text(d,xy,s,f,fill=INK,anchor="la",spacing=8):
    d.multiline_text(xy,s,font=f,fill=fill,anchor=anchor,spacing=spacing)

def tw(d,s,f):
    l,t,r,b=d.textbbox((0,0),s,font=f); return r-l,b-t

VIS=(150,750,3750,5550)      # 袖を除いた見える範囲
TRIM=(150,150,3750,5550)     # 裁ち落とし後の全面

def flat_flag(path, h, box=VIS, shadow=True, sleeve_line=False):
    """デザインを平置きの旗として描く（影つき）"""
    im=Image.open(path).convert("RGB").crop(box)
    w=int(round(h*im.width/im.height)); im=im.resize((w,h),Image.LANCZOS)
    pad=int(h*0.035)
    card=Image.new("RGBA",(w+pad*2,h+pad*2),(0,0,0,0))
    if shadow:
        sh=Image.new("RGBA",card.size,(0,0,0,0))
        ImageDraw.Draw(sh).rectangle([pad,pad+int(h*0.008),pad+w,pad+h],fill=(30,35,30,70))
        card=Image.alpha_composite(card, sh.filter(ImageFilter.GaussianBlur(pad*0.55)))
    card.paste(im,(pad,pad))
    if sleeve_line:
        d=ImageDraw.Draw(card)
        y=pad+int(h*600/(box[3]-box[1]))
        for x in range(pad,pad+w,30): d.line([x,y,x+16,y],fill=(22,86,52,205),width=4)
    return card

def rule(d,y,x0=140,x1=W-140,c=(214,210,202)):
    d.line([x0,y,x1,y],fill=c,width=3)

# ---------------------------------------------------------------- 02 名入れ説明
def img_personalize(tag, out):
    base=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(base)
    f1=F(78,"Bold"); f2=F(38,"Medium"); f3=F(33,"SemiBold"); f4=F(30,"Medium")
    text(d,(W//2,88),"YOUR FAMILY NAME ON IT",f1,INK,"ma")
    text(d,(W//2,182),"Type any name. We print it and ship it.",f2,SUB,"ma")
    names=["SMITHS","MILLERS","ANDERSONS"]
    fh=760; gap=70
    cards=[flat_flag(f"named_r/{tag}_{n}_3900x5700.png",fh) for n in names]
    tot=sum(c.width for c in cards)+gap*2; x=(W-tot)//2
    for c,n in zip(cards,names):
        base.paste(c,(x,262),c)
        text(d,(x+c.width//2,262+c.height+14),f'"THE {n}"',f3,ACC,"ma")
        x+=c.width+gap
    rule(d,1258)
    steps=["1.  Click PERSONALIZE","2.  Type your family name","3.  We print and ship"]
    x=170
    for s in steps:
        text(d,(x,1318),s,f4,INK); x+=560
    base.save(out,quality=92,subsampling=0)

# ---------------------------------------------------------------- 04 サイズ図
def img_size(tag, out):
    base=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(base)
    f1=F(76,"Bold"); f2=F(46,"SemiBold"); f3=F(32,"Medium")
    text(d,(W//2,60),"12 x 18 INCHES",f1,INK,"ma")
    text(d,(W//2,152),"30 x 46 cm  ·  standard garden flag size",f3,SUB,"ma")
    fh=1000; top=236; cx=W//2-40
    c=flat_flag(f"named_r/{tag}_SMITHS_3900x5700.png",fh,TRIM,sleeve_line=True)
    base.paste(c,(cx-c.width//2,top),c)
    pad=int(fh*0.035)
    L=cx-c.width//2+pad; R=L+c.width-pad*2; T=top+pad; B=T+fh
    d.line([L,B+62,R,B+62],fill=INK,width=4)
    for x in (L,R): d.line([x,B+40,x,B+84],fill=INK,width=4)
    w,_=tw(d,"12 in",f2); d.rectangle([(L+R)//2-w//2-18,B+32,(L+R)//2+w//2+18,B+92],fill=CREAM)
    text(d,((L+R)//2,B+62),"12 in",f2,INK,"mm")
    X=R+104
    d.line([X,T,X,B],fill=INK,width=4)
    for y in (T,B): d.line([X-24,y,X+24,y],fill=INK,width=4)
    w,_=tw(d,"18 in",f2)
    d.rectangle([X-30,(T+B)//2-w//2-18,X+30,(T+B)//2+w//2+18],fill=CREAM)
    t=Image.new("RGBA",(w+24,72),(0,0,0,0))
    ImageDraw.Draw(t).text(((w+24)//2,36),"18 in",font=f2,fill=INK,anchor="mm")
    t=t.rotate(90,expand=True); base.paste(t,(X-t.width//2,(T+B)//2-t.height//2),t)
    ys=T+int(fh*600/5400)
    d.line([L-186,ys,L-26,ys],fill=ACC,width=4)
    d.ellipse([L-32,ys-7,L-18,ys+7],fill=ACC)
    text(d,(L-202,ys),"2 in sleeve\nslides onto the stand",F(31,"SemiBold"),ACC,"rm",spacing=8)
    base.save(out,quality=92,subsampling=0)

# ---------------------------------------------------------------- 05 両面印刷
def img_double(tag, out):
    base=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(base)
    f1=F(76,"Bold"); f2=F(36,"Medium"); f3=F(40,"Bold")
    text(d,(W//2,92),"PRINTED ON BOTH SIDES",f1,INK,"ma")
    text(d,(W//2,192),"The design reads correctly from the front and from the back.",f2,SUB,"ma")
    fh=880
    c=flat_flag(f"named_r/{tag}_SMITHS_3900x5700.png",fh)
    gap=190; tot=c.width*2+gap; x=(W-tot)//2
    for lab in ("FRONT","BACK"):
        base.paste(c,(x,288),c)
        text(d,(x+c.width//2,288+c.height+22),lab,f3,ACC,"ma")
        x+=c.width+gap
    d.line([W//2,470,W//2,900],fill=(216,211,202),width=3)
    base.save(out,quality=92,subsampling=0)

# ---------------------------------------------------------------- 07 注意書き
def img_notice(tag, out):
    base=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(base)
    f1=F(76,"Bold"); f2=F(42,"SemiBold"); f3=F(38,"Medium"); f4=F(34,"Medium")
    text(d,(W//2,70),"FLAG ONLY",f1,WARN,"ma")
    text(d,(W//2,170),"The metal stand in the photos is not included.",f2,INK,"ma")
    fh=1000
    c=flat_flag(f"named_r/{tag}_SMITHS_3900x5700.png",fh)
    base.paste(c,(196,270),c)
    x=196+c.width+120; y=318
    for line in ["Fits almost any standard","garden flag stand.","","2 inch sewn sleeve at the top."]:
        text(d,(x,y),line,f3,INK); y+=60
    y+=56; rule(d,y,x,W-150); y+=48
    text(d,(x,y),"CARE",F(38,"Bold"),ACC); y+=72
    for line in ["Hand wash in cool water.","Hang to dry.","Bring it indoors in storms","and heavy wind."]:
        text(d,(x,y),line,f4,SUB); y+=56
    base.save(out,quality=92,subsampling=0)

# ---------------------------------------------------------------- 03 拡大
def img_closeup(src, out, label="SOFT, FADE-RESISTANT FABRIC"):
    im=Image.open(src)
    cw,ch=int(W*0.75),int(H*0.75)
    L=(im.width-cw)//2; T=min(int(im.height*0.25), im.height-ch)
    c=im.crop((L,T,L+cw,T+ch)).resize((W,H),Image.LANCZOS)
    d=ImageDraw.Draw(c)
    bar=Image.new("RGBA",(W,132),(18,22,18,205)); c.paste(Image.alpha_composite(
        c.crop((0,H-132,W,H)).convert("RGBA"),bar).convert("RGB"),(0,H-132))
    d=ImageDraw.Draw(c); text(d,(W//2,H-66),label,F(40,"SemiBold"),(255,255,255),"mm")
    c.save(out,quality=92,subsampling=0)
