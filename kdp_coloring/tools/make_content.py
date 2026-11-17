"""解説文のMarkdown（docs/05_…）と本の基本情報から、組版用の content.json を作る。

使い方: python3 make_content.py <解説文.md> <ページ画像フォルダ> <book.json> <出力content.json>
  book.json: {"title","subtitle","author","howto":[...],"colophon":[...]}
解説文.md の形式: 「## 第n章 …」→「**章の導入文**」の次の行が導入文 →「### n. 題名」の次の行から本文。
「- 確認」「- ※」で始まる行は制作メモなので紙面に出さない。
"""
import glob, json, os, re, sys

md, pages, book, out = sys.argv[1:5]
imgs = sorted(os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(pages, '*.png')))
B = json.load(open(book, encoding='utf-8'))
chapters, cur, item, want_intro = [], None, None, False
for ln in open(md, encoding='utf-8'):
    ln = ln.rstrip('\n')
    m = re.match(r'^## (第\d+章 .+)$', ln)
    if m:
        cur = {'name': m.group(1), 'intro': '', 'items': []}; chapters.append(cur); item = None; continue
    if ln.startswith('## '):
        cur = item = None; continue
    if ln == '**章の導入文**':
        want_intro = True; continue
    if want_intro and ln.strip():
        cur['intro'] = ln.strip(); want_intro = False; continue
    m = re.match(r'^### (\d+)\. (.+)$', ln)
    if m and cur is not None:
        n = int(m.group(1))
        item = {'no': n, 'title': m.group(2), 'text': '', 'image': imgs[n - 1]}
        assert imgs[n - 1].startswith(f'{n:02d}_'), imgs[n - 1]
        cur['items'].append(item); continue
    if item is not None and ln.strip() and not ln.startswith(('- ', '---')):
        item['text'] += ln.strip()
n = sum(len(c['items']) for c in chapters)
assert n == len(imgs), (n, len(imgs))
B['chapters'] = chapters
json.dump(B, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('章', len(chapters), '項目', n)
