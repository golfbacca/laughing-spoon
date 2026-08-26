#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2冊目の完成ページから Kindle 固定レイアウト EPUB を作る。
1冊目の build_epub.py と同じ機構。ORDER と ALT だけ差し替えてある。
出力: docs/絵本KDP_2冊目_入稿/トトンとはじめてのパンツ.epub
"""
import pathlib, zipfile, uuid, datetime, tempfile
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGES = ROOT/"docs"/"絵本KDP_2冊目_完成ページ"
OUT   = ROOT/"docs"/"絵本KDP_2冊目_入稿"; OUT.mkdir(exist_ok=True)

TITLE  = "トトンと はじめての パンツ"
AUTHOR = "はりま せいじ"     # HARIMA SEIJI
LANG   = "ja"
EPUB_PX = 1600
_TMP = pathlib.Path(tempfile.mkdtemp())

def fitted(name):
    src = PAGES/f"{name}.jpg"
    im = Image.open(src)
    if max(im.size) > EPUB_PX:
        r = EPUB_PX/max(im.size)
        im = im.resize((int(im.width*r), int(im.height*r)), Image.LANCZOS)
    out = _TMP/f"{name}.jpg"
    im.save(out, quality=88, optimize=True)
    return out

BOOKID = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "toton-hajimete-no-pantsu"))

COVER = "PB_表表紙_正方形"      # manifest の cover-image 用。本文には入れない
ORDER = ["S01_あさ","02_場面01_ふくろ","03_場面02_あける","S04_ならべる",
         "04_場面03_おむつがいい","05_場面04_だきしめる","06_場面05_どれにする",
         "07_場面06_えらんだ","S09_すわる","08_場面07_おむつをぬぐ",
         "09_場面08_かたあし","S13_かべにて","10_場面09_もういっぽう",
         "11_場面10_ひっぱる","S14_みおろす","12_場面11_はけた",
         "13_場面12_おでかけ","S18_つぎのあさ"]

# 代替テキスト（読み上げ用）。
# 固定レイアウトの絵本は本文も絵の中に焼き込まれているので、
# 代替テキストを入れないとスクリーンリーダーには何も届かない。
# 各ページ「そのページの本文」＋「絵の説明」を入れる。
ALT = {
 "PB_表表紙_正方形":
   "表紙。タイトル「トトンと はじめての パンツ」。"
   "サブタイトル「「じぶんで はく」が はじまる えほん 1さい 2さい 3さい」。"
   "みどりの シャツの ミオちゃんが きいろの パンツを りょうてで もち、"
   "よこに みずいろの ちいさな いきもの トトンが ならんで いる。",
 "S01_あさ":
   "きょうは とくべつな あさ。ミオちゃんが おきて きた。"
   "トトンは たなの したで まって いる。 ／ "
   "あさの へや。ミオちゃんが はいって きて、たなの したに トトンが いる。",
 "02_場面01_ふくろ":
   "たなの うえに、あたらしい ふくろ。きのう おみせで かって きた ふくろ。 ／ "
   "ひくい たなの うえに、ベージュの かみぶくろが ひとつ おいて ある。",
 "03_場面02_あける":
   "ふくろを あける。なかから パンツが でてきた。 ／ "
   "ミオちゃんが ゆかで かみぶくろを りょうてで あけて、なかを のぞいて いる。",
 "S04_ならべる":
   "ゆかに ならべる。3まい ならんだ。 ／ "
   "ゆかに きいろ・みずいろ・コーラルの パンツが 3まい ならんで いる。",
 "04_場面03_おむつがいい":
   "ミオちゃんは いっぽ さがった。「おむつが いい」 ／ "
   "ミオちゃんが パンツから いっぽ さがって、ためらって いる。"
   "トトンは リュックの ひもを にぎって いる。",
 "05_場面04_だきしめる":
   "おむつを むねに だいた。トトンが リュックの ひもを ぎゅっと にぎる。 ／ "
   "ミオちゃんが しろい おむつを むねに だいて いる。",
 "06_場面05_どれにする":
   "トトンが パンツを ひろげた。「どれに する」 ／ "
   "トトンが きいろい パンツを ひろげて、ミオちゃんに さしだして いる。",
 "07_場面06_えらんだ":
   "ミオちゃんが てを のばした。きいろの パンツを とった。えらんだ。 ／ "
   "ミオちゃんが きいろい パンツを りょうてで うけとって いる。",
 "S09_すわる":
   "ゆかに すわる。トトンが よこに くる。 ／ "
   "ミオちゃんが ゆかに すわり、ひざに パンツを のせて いる。よこに トトン。",
 "08_場面07_おむつをぬぐ":
   "おむつを ぬぐ。まるめて、ごみばこに いれる。"
   "トトンは パンツを もって まって いる。 ／ "
   "かごの なかに まるめた おむつが ひとつ。トトンが きいろい パンツを もって まって いる。"
   "ミオちゃんは この えには いない。",
 "09_場面08_かたあし":
   "かたほうの あしを いれる。ぐらぐら する。 ／ "
   "ミオちゃんが かたあしを パンツに いれて、バランスを とって いる。",
 "S13_かべにて":
   "かべに てを ついた。もう ぐらぐら しない。 ／ "
   "ミオちゃんが かべに てを ついて、からだを ささえて いる。",
 "10_場面09_もういっぽう":
   "もういっぽうの あしを いれる。ゆっくりで いい。 ／ "
   "ゆかの ちかくから みた え。しろい くつしたの あしが 2ほん。"
   "かたほうが すこし あがって いる。よこに トトンが いる。",
 "11_場面10_ひっぱる":
   "りょうてで もって、きゅっと ひっぱりあげる。 ／ "
   "ミオちゃんの かおの アップ。したを みて、くちを ぎゅっと むすんで いる。"
   "ちからを いれて いる しるしが りょうがわに ある。",
 "S14_みおろす":
   "ミオちゃんが したを みた。きいろが みえる。 ／ "
   "ミオちゃんの かおの アップ。あごを ひいて したを みおろし、"
   "すこし うれしそうに わらって いる。うしろに ちいさく トトンが いる。",
 "12_場面11_はけた":
   "じぶんで はけた。トトンの みみが ぴくっと うごいた。「じぶんで はけた」 ／ "
   "ミオちゃんが まっすぐ たって いる。トトンの みみが うごいて いる。",
 "13_場面12_おでかけ":
   "ベージュの ズボンを はいて、あかい くつを はく。きょうは こうえんへ いく ひ。 ／ "
   "げんかんで ミオちゃんが あかい くつを はいて いる。よこに リュックと トトン。",
 "S18_つぎのあさ":
   "つぎの あさ。ミオちゃんが じぶんで ふくろに てを のばした。「きょうも えらべる」 ／ "
   "つぎの あさ。ミオちゃんが たなの うえの ふくろに じぶんから てを のばして いる。",
}

def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))

def page_xhtml(img, w, h, alt):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{LANG}">
<head><meta charset="utf-8"/><title>{TITLE}</title>
<meta name="viewport" content="width={w}, height={h}"/>
<style>html,body{{margin:0;padding:0;height:100%;}}
img{{width:100%;height:100%;display:block;}}</style></head>
<body><div><img src="../images/{img}" alt="{esc(alt)}"/></div></body></html>'''

def main():
    epub = OUT/"トトンとはじめてのパンツ.epub"
    files = [(n, fitted(n)) for n in ORDER]
    cover_path = fitted(COVER)
    sizes = {n: Image.open(p).size for n, p in files}

    # 固定レイアウトの本は、全ページが同じ寸法でなければならない。
    # original-resolution は本1冊に1つしか無く、それと違う比率の
    # ページは端末側で引き伸ばされる（表紙1:1.6・本文1:1 で
    # 本文が縦に伸びる事故を起こした。2026-08-24）
    uniq = set(sizes.values())
    if len(uniq) != 1:
        for n in ORDER:
            print(f"  {sizes[n][0]}x{sizes[n][1]}  {n}")
        raise SystemExit(f"中止: ページの寸法がそろっていない {sorted(uniq)}")
    cw, ch = next(iter(uniq))          # 本1冊の基準寸法

    with zipfile.ZipFile(epub, "w") as z:
        z.writestr("mimetype", "application/epub+zip", zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
          '<?xml version="1.0"?>\n<container version="1.0" '
          'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
          '<rootfiles><rootfile full-path="OEBPS/content.opf" '
          'media-type="application/oebps-package+xml"/></rootfiles></container>')

        manifest, spine = [], []
        # 表紙は manifest だけに置く。本文ページとしては入れない。
        # KDPは登録画面でアップロードした表紙を1ページ目に差し込むので、
        # 本の中にも表紙を持たせると、表紙が2回続けて出てしまう。
        z.write(cover_path, f"OEBPS/images/{COVER}.jpg")
        manifest.append(f'<item id="cover" href="images/{COVER}.jpg" '
                        f'media-type="image/jpeg" properties="cover-image"/>')
        for i, (n, p) in enumerate(files):
            z.write(p, f"OEBPS/images/{n}.jpg")
            w, h = sizes[n]
            z.writestr(f"OEBPS/text/p{i:02d}.xhtml", page_xhtml(f"{n}.jpg", w, h, ALT[n]))
            manifest.append(f'<item id="img{i:02d}" href="images/{n}.jpg" '
                            f'media-type="image/jpeg"/>')
            manifest.append(f'<item id="p{i:02d}" href="text/p{i:02d}.xhtml" '
                            f'media-type="application/xhtml+xml"/>')
            spine.append(f'<itemref idref="p{i:02d}"/>')

        nav = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n'
               f'<html xmlns="http://www.w3.org/1999/xhtml" '
               f'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{LANG}">'
               '<head><meta charset="utf-8"/><title>もくじ</title></head><body>'
               '<nav epub:type="toc"><ol>'
               '<li><a href="text/p01.xhtml">ほんぶん</a></li>'
               '</ol></nav></body></html>')
        z.writestr("OEBPS/nav.xhtml", nav)
        manifest.append('<item id="nav" href="nav.xhtml" '
                        'media-type="application/xhtml+xml" properties="nav"/>')

        opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bid"
         prefix="rendition: http://www.idpf.org/vocab/rendition/# schema: http://schema.org/">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bid">{BOOKID}</dc:identifier>
<dc:title>{TITLE}</dc:title>
<dc:creator>{AUTHOR}</dc:creator>
<dc:language>{LANG}</dc:language>
<meta property="dcterms:modified">{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}</meta>
<meta property="rendition:layout">pre-paginated</meta>
<meta property="rendition:orientation">portrait</meta>
<meta property="rendition:spread">none</meta>
<meta name="original-resolution" content="{cw}x{ch}"/>
<meta name="fixed-layout" content="true"/>
<meta name="book-type" content="children"/>
<meta name="cover" content="cover"/>
<meta property="schema:accessMode">textual</meta>
<meta property="schema:accessMode">visual</meta>
<meta property="schema:accessModeSufficient">textual</meta>
<meta property="schema:accessibilityFeature">alternativeText</meta>
<meta property="schema:accessibilityHazard">none</meta>
<meta property="schema:accessibilitySummary">すべての絵に、本文と絵の内容を説明した代替テキストが入っています。</meta>
</metadata>
<manifest>{''.join(manifest)}</manifest>
<spine>{''.join(spine)}</spine>
</package>'''
        z.writestr("OEBPS/content.opf", opf)

    mb = epub.stat().st_size/1048576
    print(f"EPUB: {epub}  {mb:.1f}MB  {len(files)}ページ")

if __name__ == "__main__":
    main()
