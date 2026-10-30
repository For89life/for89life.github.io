# -*- coding: utf-8 -*-
"""Татсан зургуудыг загваруудад холбоно.

Загвар бүрт барааны/хоолны картын зургийн хайрцаг нь одоогоор
градиент бөгөөд дотроо орлуулагч бичвэртэй. Зураг орсны дараа
тэр бичвэр илүүдэнэ — нэр нь доор аль хэдийн бий. Тиймээс:
  · градиентийг зургаар солино (шинэ ангиар)
  · орлуулагч бичвэрийг устгана
  · шошго (.tagp .st .tg .mk) хэвээр үлдээнэ

Тайлбар бичвэр нь утга агуулсан хэсгүүдэд (hero, түүх) бичвэр
хэвээр үлдэж, зөвхөн дэвсгэр нь зураг болно.
"""
import io, os, re

TPL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = '../images/'

# Карт: (файл, хайрцгийн анги, градиентийн угтвар, зургийн нэрс)
CARDS = [
 ('shop/zah.html',        'p-img',   'g', ['zah-p%d' % i for i in range(1, 9)]),
 ('shop/tulhuur.html',    'p-im',    'q', ['tul-p%d' % i for i in range(1, 5)]),
 ('shop/horshoo.html',    'p-im',    'n', ['hor-p%d' % i for i in range(1, 5)]),
 ('restaurant/navch.html','c-im',    'b', ['navch-b%d' % i for i in range(1, 4)]),
 ('restaurant/togoo.html','item-im', 'f', ['togoo-m%d' % i for i in range(1, 7)]),
]

# Дэвсгэр: (файл, хуучин мөр, шинэ мөр)
BACKDROPS = [
 ('shop/zah.html',
  "linear-gradient(135deg,#7C2D12,#C2410C 55%,#EA8C4E);",
  "url('%szah-hero.webp') center/cover,#7C2D12;" % IMG),

 ('shop/horshoo.html',
  ".basket{border-radius:26px;aspect-ratio:1/1;background:linear-gradient(rgba(0,0,0,.22),rgba(0,0,0,.3)),linear-gradient(150deg,#243214,#4D7C0F 58%,#9BC96B);display:grid;place-items:center;}",
  ".basket{border-radius:26px;aspect-ratio:1/1;display:grid;place-items:center;\n"
  "  background:linear-gradient(rgba(0,0,0,.3),rgba(0,0,0,.3)),url('%shor-hero.webp') center/cover,#243214;}" % IMG),

 ('restaurant/guurs.html',
  "linear-gradient(145deg,#4A2C18,#A33B0F 60%,#D98E4A);}",
  "url('%sguurs-plate.webp') center/cover,#4A2C18;}" % IMG),

 ('restaurant/utaa.html',
  "linear-gradient(145deg,#1A1510,#4A3A24 55%,#8A6A33);",
  "url('%sutaa-hero.webp') center/cover,#1A1510;" % IMG),
 ('restaurant/utaa.html',
  ".glass{aspect-ratio:4/5;border-radius:4px;background:linear-gradient(rgba(0,0,0,.3),rgba(0,0,0,.42)),linear-gradient(150deg,#241B10,#6B4D22 60%,#B8903F);display:grid;place-items:center;}",
  ".glass{aspect-ratio:4/5;border-radius:4px;display:grid;place-items:center;\n"
  "  background:linear-gradient(rgba(0,0,0,.42),rgba(0,0,0,.42)),url('%sutaa-glass.webp') center/cover,#241B10;}" % IMG),

 ('restaurant/navch.html',
  ".photo{border-radius:28px;aspect-ratio:5/4;background:linear-gradient(rgba(0,0,0,.2),rgba(0,0,0,.3)),linear-gradient(150deg,#22361F,#4F8A5F 58%,#A8D4A0);display:grid;place-items:center;}",
  ".photo{border-radius:28px;aspect-ratio:5/4;display:grid;place-items:center;\n"
  "  background:linear-gradient(rgba(0,0,0,.34),rgba(0,0,0,.34)),url('%snavch-hero.webp') center/cover,#22361F;}" % IMG),

 ('restaurant/togoo.html',
  ".bowl{aspect-ratio:1/1;background:linear-gradient(rgba(0,0,0,.2),rgba(0,0,0,.32)),linear-gradient(150deg,#5B0A04,#C21807 55%,#F5B301);display:grid;place-items:center;border:4px solid var(--deep);}",
  ".bowl{aspect-ratio:1/1;display:grid;place-items:center;border:4px solid var(--deep);\n"
  "  background:linear-gradient(rgba(0,0,0,.45),rgba(0,0,0,.45)),url('%stogoo-hero.webp') center/cover,#5B0A04;}" % IMG),
]

def wire_cards(rel, box, pref, names):
    path = os.path.join(TPL, rel.replace('/', os.sep))
    s = io.open(path, encoding='utf-8').read()
    # Дарааллаар нь зураг оноож, орлуулагч бичвэрийг устгана
    pat = re.compile(r'class="%s %s\d"\s*>\s*<span>[^<]*</span>' % (box, pref))
    idx = [0]
    def rep(m):
        i = idx[0]
        idx[0] += 1
        if i >= len(names):
            return m.group(0)
        return 'class="%s im-%s">' % (box, names[i])
    s2, n = pat.subn(rep, s)
    if n == 0:
        return rel, 0
    # Шинэ ангиудыг CSS-д нэмнэ
    css = '\n/* Татсан зураг — _data/fetch-images.py үүсгэсэн */\n'
    for nm in names[:n]:
        css += ".im-%s{background:url('%s%s.webp') center/cover;}\n" % (nm, IMG, nm)
    s2 = s2.replace('</style>', css + '</style>', 1)
    io.open(path, 'w', encoding='utf-8', newline='').write(s2)
    return rel, n

def main():
    print('--- cards')
    for rel, box, pref, names in CARDS:
        r, n = wire_cards(rel, box, pref, names)
        print('  %-26s %d images' % (r, n))
    print('--- backdrops')
    for rel, old, new in BACKDROPS:
        path = os.path.join(TPL, rel.replace('/', os.sep))
        s = io.open(path, encoding='utf-8').read()
        if old not in s:
            print('  %-26s NOT FOUND' % rel); continue
        io.open(path, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
        print('  %-26s ok' % rel)

if __name__ == '__main__':
    main()
