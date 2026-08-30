#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3冊目の完成ページから Kindle 固定レイアウト EPUB を作る。
1冊目の build_epub.py と同じ機構。ORDER と ALT だけ差し替えてある。
出力: docs/絵本KDP_3冊目_入稿/トトンとはじめてのパンツ.epub
"""
import pathlib, zipfile, uuid, datetime, tempfile
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGES = ROOT/"docs"/"絵本KDP_3冊目_完成ページ"
OUT   = ROOT/"docs"/"絵本KDP_3冊目_入稿"; OUT.mkdir(exist_ok=True)

TITLE  = "トトンと よるの トイレ"
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

BOOKID = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "toton-yoru-no-toilet"))

COVER = "PB_表表紙_正方形"      # manifest の cover-image 用。本文には入れない
ORDER = ["S01_ねるまえ","02_場面01_めがさめる","03_場面02_むずむず","S04_ふとんのふち",
         "04_場面03_でられない","05_場面04_ここにある","06_場面05_てをのばす",
         "07_場面06_ついた","S09_じぶんでついた","08_場面07_ふとんからでる",
         "09_場面08_ろうか","S13_トイレのドア","10_場面09_トイレのなか",
         "11_場面10_おわりのおと","S14_てをあらう","12_場面11_もどる",
         "13_場面12_またねる","S18_つぎのよる"]

# 代替テキスト（読み上げ用）。
# 固定レイアウトの絵本は本文も絵の中に焼き込まれているので、
# 代替テキストを入れないとスクリーンリーダーには何も届かない。
# 各ページ「そのページの本文」＋「絵の説明」を入れる。
ALT = {
 "PB_表表紙_正方形":
   "表紙。タイトル「トトンと よるの トイレ」。"
   "サブタイトル「「じぶんで あかりを つける」が はじまる えほん 3さい 4さい 5さい」。"
   "くらい へやで、みどりの シャツの ミオちゃんが ちいさな あかりを"
   "りょうてで もって いる。あかりが かおを あたたかく てらす。"
   "よこに みずいろの ちいさな いきもの トトンが いる。トトンは ひからない。",
 "S01_ねるまえ":
   "ねる まえ。ミオちゃんが ふとんに はいる。まくらもとに ちいさな あかり。 ／ "
   "よるの へや。ミオちゃんが ふとんに はいろうと して いる。"
   "まくらもとの ちいさな だいの うえで あかりが ついて いる。",
 "02_場面01_めがさめる":
   "よなかに めが さめた。へやが くらい。 ／ "
   "あかりの ついて いない くらい へや。ミオちゃんが ふとんの なかで"
   "めを あけて いる。あかりは まだ ついて いない。",
 "03_場面02_むずむず":
   "おなかの したの ほうが むずむず する。 ／ "
   "ミオちゃんが ふとんの なかで ひざを まげて、おなかに てを あてて いる。",
 "S04_ふとんのふち":
   "いかなきゃ。ミオちゃんは ふとんの ふちを にぎった。 ／ "
   "ふとんの ふちを ぎゅっと にぎって いる ちいさな て。よこに トトンが いる。",
 "04_場面03_でられない":
   "でも、くらい。ふとんから でられない。"
   "トトンが リュックの ひもを ぎゅっと にぎる。 ／ "
   "ミオちゃんが ふとんの うえに すわったまま、くらい へやの ほうを みて"
   "うごけずに いる。トトンは リュックの ひもを にぎって いる。",
 "05_場面04_ここにある":
   "トトンが まくらもとを みた。「ここに ある」 ／ "
   "トトンが まくらもとの だいの うえを みあげて いる。"
   "そこに あかりが おいて ある。まだ ついて いない。",
 "06_場面05_てをのばす":
   "ミオちゃんが てを のばした。ゆびが あかりに とどいた。 ／ "
   "ミオちゃんの てが、だいの うえの あかりに とどく ところ。",
 "07_場面06_ついた":
   "カチッ。つけた。あかりが ついた。 ／ "
   "ミオちゃんが あかりの うえの ボタンを おして、あかりが ついた しゅんかん。"
   "あたたかい ひかりが ミオちゃんの かおと ゆかを てらして いる。",
 "S09_じぶんでついた":
   "トトンの みみが ぴくっと うごいた。「じぶんで ついた」 ／ "
   "あかりの ついた へやで、ミオちゃんが すわって いる。"
   "トトンの みみが うごいて いる。",
 "08_場面07_ふとんからでる":
   "ふとんから でる。ゆかは つめたい。 ／ "
   "ミオちゃんが ふとんから かたあしを ゆかに おろして いる。",
 "09_場面08_ろうか":
   "あかりを もって、ろうかを あるく。まえが すこし みえる。 ／ "
   "うしろから みた え。ミオちゃんが あかりを りょうてで もって"
   "ろうかを あるいて いる。あしもとが あかるい。よこに トトン。",
 "S13_トイレのドア":
   "トイレの ドア。ノブに てを かける。 ／ "
   "とじた ドアの まえで、ミオちゃんが ノブに てを のばして いる。"
   "もう かたほうの てには あかりを もって いる。",
 "10_場面09_トイレのなか":
   "ドアを しめる。パンツを おろす。よいしょ と すわる。"
   "あかりは ドアの したから もれて いる。 ／ "
   "とじた トイレの ドア。ドアの したの すきまから あたたかい ひかりが"
   "ろうかに もれて いる。そとで トトンが まって いる。"
   "ミオちゃんは この えには いない。",
 "11_場面10_おわりのおと":
   "ジャーッ。よるの おとは おおきい。でも、おわりの おと。 ／ "
   "とじた ドアの そと。ドアの したから ひかりが もれて いる。"
   "おとを あらわす まるい せんが ドアの りょうがわに ある。",
 "S14_てをあらう":
   "てを あらう。みずも つめたい。 ／ "
   "ちいさな てあらいばで、りょうての した に みずが ながれて いる。"
   "よこに あかりが おいて ある。",
 "12_場面11_もどる":
   "あかりを もって、ふとんに もどる。ろうかは もう ながく ない。 ／ "
   "ミオちゃんが あかりを もって、こちらへ あるいて くる。かおが あかるい。",
 "13_場面12_またねる":
   "ふとんに もぐる。あかりを けす。ミオちゃんは また ねむった。 ／ "
   "ふとんの なかで めを とじて いる ミオちゃん。"
   "まくらもとの あかりは けして ある。よこで トトンも めを とじて すわって いる。",
 "S18_つぎのよる":
   "つぎの よる。ミオちゃんが じぶんで あかりに てを のばした。"
   "「つぎの よるも つけられる」 ／ "
   "つぎの よる。ミオちゃんが ためらわずに あかりへ てを のばして いる。",
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
    epub = OUT/"toton03-ebook.epub"   # 入稿物は英数字名（日本語名は弾かれる）
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
