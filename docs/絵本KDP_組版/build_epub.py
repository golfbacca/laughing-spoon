#!/usr/bin/env python3
"""完成ページから Kindle 固定レイアウト EPUB を作る。
出力: docs/絵本KDP_入稿/トトンとおでかけトイレ.epub
"""
import pathlib, zipfile, uuid, datetime, tempfile
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGES = ROOT/"docs"/"絵本KDP_完成ページ"
OUT   = ROOT/"docs"/"絵本KDP_入稿"; OUT.mkdir(exist_ok=True)

TITLE  = "トトンと おでかけトイレ"
AUTHOR = "はりま せいじ"     # HARIMA SEIJI
LANG   = "ja"
EPUB_PX = 1600   # Kindleの表示に十分。配信コストはMB単位で引かれる
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

BOOKID = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "toton-odekake-toilet"))

ORDER = ["01_表表紙_Kindle_1600x2560",
         "S01_いえをでる","02_場面01_バス","03_場面02_公園であそぶ","S04_きづく",
         "04_場面03_もじもじ","05_場面04_言えない","06_場面05_いまいこう","07_場面06_言えた",
         "S09_トイレがみえる","08_場面07_知らないドア","09_場面08_ノック","10_場面09_トイレの中",
         "S13_ドアがあく","S14_レバー","11_場面10_おわりの音","12_場面11_手をあらう",
         "13_場面12_公園にもどる","S18_つぎのおでかけ"]

# 代替テキスト（読み上げ用）。
# 固定レイアウトの絵本は本文も絵の中に焼き込まれているので、
# 代替テキストを入れないとスクリーンリーダーには何も届かない。
# 各ページ「そのページの本文」＋「絵の説明」を入れる。
ALT = {
 "01_表表紙_Kindle_1600x2560":
   "表紙。タイトル「トトンと おでかけトイレ」。"
   "サブタイトル「2さい 3さい 4さいの『いま いきたい』が いえるように なる えほん」。"
   "みどりの シャツの ミオちゃんと、みずいろの ちいさな いきもの トトンが ならんで いる。",
 "S01_いえをでる":
   "きょうは こうえんへ いく ひ。ミオちゃんが くつを はく。"
   "トトンは リュックの よこで まって いる。 ／ "
   "げんかんで ミオちゃんが あかい くつを はいて いる。よこに トトンが いる。",
 "02_場面01_バス":
   "バスに のって、こうえんへ。ミオちゃんの となりに トトンが すわって いる。 ／ "
   "バスの ざせき。まどの そとは あかるい。",
 "03_場面02_公園であそぶ":
   "すべりだいも ブランコも たのしい。トトンも いっしょに はしる。 ／ "
   "こうえんで ミオちゃんが りょうてを ひろげて はしり、トトンが あしもとを はしって いる。",
 "S04_きづく":
   "あれ。ミオちゃんの あしが とまった。 ／ "
   "はしって いた ミオちゃんが きゅうに たちどまり、したを むいて いる。",
 "04_場面03_もじもじ":
   "おなかの したの ほうが むずむず する。 ／ "
   "ミオちゃんが もじもじ して いる。トトンが あしもとから みあげて いる。",
 "05_場面04_言えない":
   "でも、まだ あそびたい。ミオちゃんは なにも いわなかった。"
   "トトンが リュックの ひもを ぎゅっと にぎる。 ／ "
   "ミオちゃんは くちを むすんで いる。トトンが リュックの ひもを にぎって いる。",
 "06_場面05_いまいこう":
   "トトンが ちいさな こえで いった。「いま、いこう」 ／ "
   "トトンが ミオちゃんの みみの ちかくで そっと はなして いる。",
 "07_場面06_言えた":
   "ミオちゃんは かおを あげた。「トイレ、いきたい」 いえた。 ／ "
   "ミオちゃんが かおを あげて いって いる。",
 "S09_トイレがみえる":
   "こうえんの トイレが みえてきた。 ／ "
   "こうえんの おくに トイレの たてものが みえる。",
 "08_場面07_知らないドア":
   "しらない ドア。なかは すこし くらい。 ／ "
   "しろい ドアの まえで ミオちゃんが たちどまって いる。",
 "09_場面08_ノック":
   "トトンが せのびして ドアを たたく。トン、トン。"
   "だれも いない。はいって いいよ。 ／ "
   "トトンが せのびして ドアを たたいて いる。よこに ミオちゃんが たって いる。",
 "10_場面09_トイレの中":
   "ドアを しめる。パンツを おろす。よいしょ と すわる。"
   "あしが とどかない ときは、だいに のせる。 ／ "
   "しまった ドアの そと。ドアの したの すきまから、だいに のった あかい くつが みえる。"
   "トトンは そとで まって いる。",
 "S13_ドアがあく":
   "ドアが あいた。ミオちゃんが でてきた。 ／ "
   "ドアが ひらいて、ミオちゃんが わらって でてくる。トトンが まって いる。",
 "S14_レバー":
   "よこの レバーに てを のばす。 ／ "
   "ミオちゃんが タンクの よこの レバーに てを のばして いる。",
 "11_場面10_おわりの音":
   "ジャーッ。おおきな おと。「これは おわりの おと」トトンが いった。 ／ "
   "みずが ながれる おとに ミオちゃんが すこし びっくりして いる。トトンが よこに いる。",
 "12_場面11_手をあらう":
   "てを あらう。トトンが リュックから タオルを だす。 ／ "
   "ミオちゃんが てあらいで てを あらい、トトンが タオルを だして いる。",
 "13_場面12_公園にもどる":
   "また はしれる。トトンの みみが ぴくっと うごいた。「つぎも いえるよ」 ／ "
   "こうえんに もどって ミオちゃんが また はしって いる。",
 "S18_つぎのおでかけ":
   "つぎの おでかけの ひ。ミオちゃんが じぶんから いった。「トイレ、いきたい」 ／ "
   "つぎの おでかけの ひ。ミオちゃんが かおを あげて じぶんから いって いる。",
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
    epub = OUT/"トトンとおでかけトイレ.epub"
    files = [(n, fitted(n)) for n in ORDER]
    sizes = {n: Image.open(p).size for n, p in files}
    cw, ch = sizes[ORDER[0]]           # 表紙の寸法をビューポートの基準にする

    with zipfile.ZipFile(epub, "w") as z:
        z.writestr("mimetype", "application/epub+zip", zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
          '<?xml version="1.0"?>\n<container version="1.0" '
          'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
          '<rootfiles><rootfile full-path="OEBPS/content.opf" '
          'media-type="application/oebps-package+xml"/></rootfiles></container>')

        manifest, spine = [], []
        for i, (n, p) in enumerate(files):
            z.write(p, f"OEBPS/images/{n}.jpg")
            w, h = sizes[n]
            z.writestr(f"OEBPS/text/p{i:02d}.xhtml", page_xhtml(f"{n}.jpg", w, h, ALT[n]))
            props = ' properties="cover-image"' if i == 0 else ""
            manifest.append(f'<item id="img{i:02d}" href="images/{n}.jpg" '
                            f'media-type="image/jpeg"{props}/>')
            manifest.append(f'<item id="p{i:02d}" href="text/p{i:02d}.xhtml" '
                            f'media-type="application/xhtml+xml"/>')
            spine.append(f'<itemref idref="p{i:02d}"/>')

        nav = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n'
               f'<html xmlns="http://www.w3.org/1999/xhtml" '
               f'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{LANG}">'
               '<head><meta charset="utf-8"/><title>もくじ</title></head><body>'
               '<nav epub:type="toc"><ol>'
               '<li><a href="text/p00.xhtml">ひょうし</a></li>'
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
<meta name="cover" content="img00"/>
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
