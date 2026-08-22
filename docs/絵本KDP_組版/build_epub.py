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

def page_xhtml(img, w, h):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{LANG}">
<head><meta charset="utf-8"/><title>{TITLE}</title>
<meta name="viewport" content="width={w}, height={h}"/>
<style>html,body{{margin:0;padding:0;height:100%;}}
img{{width:100%;height:100%;display:block;}}</style></head>
<body><div><img src="../images/{img}" alt=""/></div></body></html>'''

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
            z.writestr(f"OEBPS/text/p{i:02d}.xhtml", page_xhtml(f"{n}.jpg", w, h))
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
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
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
</metadata>
<manifest>{''.join(manifest)}</manifest>
<spine>{''.join(spine)}</spine>
</package>'''
        z.writestr("OEBPS/content.opf", opf)

    mb = epub.stat().st_size/1048576
    print(f"EPUB: {epub}  {mb:.1f}MB  {len(files)}ページ")

if __name__ == "__main__":
    main()
