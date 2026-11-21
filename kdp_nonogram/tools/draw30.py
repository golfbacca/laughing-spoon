"""30×30の絵柄を図形から作る。1マス＝20ピクセルで描き、マスごとに半分以上黒なら黒にする。
座標はマス単位（0〜30、yは下向き）。出力は puzzles30/*.txt。"""
import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from nonogram import check

N, S = 30, 20


class Art:
    def __init__(self, n=N):
        self.n = n                        # 絵は常に30単位の座標で描き、n×n のマス目に落とす
        self.im = Image.new("L", (N * S, N * S), 255)
        self.d = ImageDraw.Draw(self.im)

    def _p(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def poly(self, pts, black=True):
        self.d.polygon(self._p(pts), fill=0 if black else 255)

    def rect(self, x0, y0, x1, y1, black=True):
        self.d.rectangle([x0 * S, y0 * S, x1 * S - 1, y1 * S - 1], fill=0 if black else 255)

    def oval(self, x0, y0, x1, y1, black=True):
        self.d.ellipse([x0 * S, y0 * S, x1 * S - 1, y1 * S - 1], fill=0 if black else 255)

    def circle(self, cx, cy, r, black=True):
        self.oval(cx - r, cy - r, cx + r, cy + r, black)

    def clipped(self, mask_fn, draw_fn):
        """mask_fn で描いた形の内側にだけ draw_fn の絵を写す"""
        m = Art(); m.im.paste(0, (0, 0, N * S, N * S)); m.d = ImageDraw.Draw(m.im)
        mm = Image.new("L", (N * S, N * S), 0); md = ImageDraw.Draw(mm)
        mask_fn(md, S)
        layer = Art(); layer.im = self.im.copy(); layer.d = ImageDraw.Draw(layer.im)
        draw_fn(layer)
        self.im.paste(layer.im, (0, 0), mm); self.d = ImageDraw.Draw(self.im)

    def grid(self):
        px = self.im.load(); n = self.n; c = N * S // n
        return [[sum(px[x * c + i, y * c + j] < 128 for i in range(c) for j in range(c)) * 2 >= c * c
                 for x in range(n)] for y in range(n)]


def fuji(a):
    a.circle(23.5, 4.5, 3.5)                                         # 太陽
    a.poly([(12.5, 8), (17.5, 8), (29, 24), (1, 24)])                # 山
    # 雪。輪郭を細くすると論理で解けなくなった（42マス残り）ので、山の縁から1.2マス内側に取る
    a.poly([(13, 9.2), (17, 9.2), (19.3, 13), (18, 12.2), (16.5, 14.5),
            (15, 12.2), (13.5, 14.5), (12, 12.2), (10.7, 13)], black=False)
    a.rect(0, 24, 30, 25)
    for y, segs in ((26, [(2, 13), (15, 22), (25, 29)]), (28, [(0, 5), (8, 12), (14, 27)])):   # 湖の波（左右非対称にして解を1つにする）
        for x0, x1 in segs:
            a.rect(x0, y, x1, y + 1)


def torii(a):
    # 柱の間に太陽（黒い丸）を置いていたが、本人が「何か分からない」と指摘。宙に浮いた黒い塊に見えるので外した
    a.poly([(0.5, 3.5), (3, 5), (27, 5), (29.5, 3.5), (30, 6), (27.5, 8), (2.5, 8), (0, 6)])  # 笠木
    a.rect(4, 11, 26, 13.5)                                          # 貫
    a.rect(14, 8, 16, 11)                                            # 額束
    a.rect(6.5, 8, 9.5, 28); a.rect(20.5, 8, 23.5, 28)               # 柱
    a.rect(5, 27, 11, 29.5); a.rect(19, 27, 25, 29.5)                # 台


def daruma(a):
    a.oval(2, 1, 28, 29.5)
    a.oval(6.5, 4.5, 23.5, 17.5, black=False)                        # 顔
    a.poly([(8, 7.5), (13.5, 6.5), (13.5, 8), (8.5, 9.2)])           # 眉
    a.poly([(22, 7.5), (16.5, 6.5), (16.5, 8), (21.5, 9.2)])
    a.circle(11, 11.5, 2); a.circle(19, 11.5, 2)                     # 目
    a.rect(13.5, 14, 16.5, 15.2)                                     # 口
    for x in (9, 14, 19):                                            # おなかの筋（マス目に合わせて2マス幅）
        a.rect(x, 20, x + 2, 27, black=False)


def maneki(a):
    # 第1版は挙げた手が頭とくっついて「手」に見えなかった（本人指摘）。
    # 頭を左へ寄せ、腕を頭から離して立て、先に丸い手をつけた。
    a.poly([(3, 9), (3.5, 1.5), (10, 5)]); a.poly([(19, 9), (18.5, 1.5), (12, 5)])   # 耳
    a.oval(1, 4, 21, 18.5)                                           # 頭
    a.oval(2, 15, 21, 30)                                            # 体
    a.poly([(18, 19), (24, 16), (27, 16), (27, 20), (20, 24)])       # 肩
    a.rect(24, 7, 27, 18)                                            # 腕
    a.oval(21, 1, 29, 8)                                             # 手
    a.rect(23, 1, 24, 4, black=False); a.rect(26, 1, 27, 4, black=False)   # 指の切れ目
    a.oval(5, 8.5, 8, 12.5, black=False); a.oval(14, 8.5, 17, 12.5, black=False)   # 目
    a.rect(6, 9.5, 7, 12.5); a.rect(15, 9.5, 16, 12.5)               # 瞳
    a.poly([(10, 13), (12, 13), (11, 14.3)], black=False)            # 鼻
    a.rect(4, 17, 18, 18.3, black=False)                             # 首輪
    a.circle(11, 19.6, 1.3, black=False)                             # 鈴
    a.oval(7.5, 21.5, 14.5, 29, black=False)                         # 小判
    a.oval(9, 23, 13, 27.5)


def lantern(a):
    a.rect(10, 0.5, 20, 4); a.rect(10, 26, 20, 29.5)                 # 上下の輪
    a.oval(2, 3, 28, 27)
    def inner(md, S):
        md.ellipse([3.2 * S, 4.2 * S, 26.8 * S, 25.8 * S], fill=255)
    def stripes(l):
        for y in range(5, 26, 2):
            l.rect(0, y, 30, y + 1, black=False)
    a.clipped(inner, stripes)
    a.rect(10, 3, 20, 5); a.rect(10, 25, 20, 27)


def sakura(a):
    """15×15用。細かいしべは潰れるので、花びら5枚・切れ込み・中心の丸だけにする"""
    for k in range(5):
        t = math.radians(-90 + 72 * k)
        a.circle(15 + 8 * math.cos(t), 15.5 + 8 * math.sin(t), 5.6)
    a.circle(15, 15.5, 6)
    for k in range(5):                                               # 花びらの切れ込み
        t = math.radians(-90 + 72 * k)
        ux, uy = math.cos(t), math.sin(t)
        tip = (15 + 9.5 * ux, 15.5 + 9.5 * uy)
        a.poly([tip, (15 + 15 * ux - 3 * uy, 15.5 + 15 * uy + 3 * ux),
                (15 + 15 * ux + 3 * uy, 15.5 + 15 * uy - 3 * ux)], black=False)
    a.rect(13, 13, 17, 17, black=False); a.rect(14, 14, 16, 16)      # 中心


def pagoda(a):
    """五重塔。屋根5枚（下ほど広い）＋相輪。15×15では三重にしか描けなかった（本人指摘）"""
    a.rect(14, 0, 16, 5)                                             # 相輪
    a.rect(13, 1, 17, 2); a.rect(13, 3, 17, 4)
    for i in range(5):
        y = 5 + 5 * i; h = 6 + 2 * i                                 # h：屋根の半分の幅
        a.rect(15 - h + 2, y, 15 + h - 2, y + 1)                     # 屋根の上の段
        a.rect(15 - h - 1, y + 1, 15 + h + 1, y + 2)                 # 屋根の下の段（軒）
        a.rect(15 - h - 1, y, 15 - h, y + 1); a.rect(15 + h, y, 15 + h + 1, y + 1)   # 反り上がった軒先（軒の真上に置く。離すと浮いた点になる）
        w = round(2 + 1.5 * i)                                       # 壁は屋根よりずっと細く。近い幅だと木に見えた
        a.rect(15 - w, y + 2, 15 + w, y + 5)                         # 各層の壁
    a.rect(14, 27, 16, 30, black=False)                              # 入口


# (ファイル名, 題, 描く関数, マス数, 出力フォルダ)
ARTS = [("01_fuji", "Fuji-san 富士山 (Mount Fuji)", fuji, 30, "puzzles30"),
        ("02_torii", "Torii 鳥居 (shrine gate)", torii, 30, "puzzles30"),
        ("03_daruma", "Daruma だるま (wishing doll)", daruma, 30, "puzzles30"),
        # 04_maneki_neko は本人が手で直した絵（puzzles30/04_maneki_neko.txt）を使う。ここでは上書きしない
        ("05_chochin", "Chōchin 提灯 (paper lantern)", lantern, 30, "puzzles30"),
        ("06_goju_no_to", "Gojū-no-tō 五重塔 (five-story pagoda)", pagoda, 30, "puzzles30")]
# 15×15の桜は手描き（puzzles/06_sakura.txt）。図形から落とすと花びらがつながって塊になった

if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "..")
    for name, title, fn, n, folder in ARTS:
        a = Art(n); fn(a); g = a.grid(); r = check(g)
        with open(os.path.join(root, folder, name + ".txt"), "w", encoding="utf-8") as f:
            f.write(f"; {title}\n" + "\n".join("".join("#" if c else "." for c in row) for row in g) + "\n")
        print(f"{folder}/{name:16s} {n}x{n} 論理だけ={r['logic_only']} 解の数={r['solutions']} 残り={r['stuck_cells']} 黒率={r['fill']:.0%} 空行列={r['empty_lines']}")
