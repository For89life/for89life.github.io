# -*- coding: utf-8 -*-
"""Загвар бүрийн дэлгэцийн зургийг картын нүүр болгож боловсруулна.

Хөтчийн цонхноос авсан зургийг blob файлаас уншина. Дээд талын
Gerelt-ийн тууз нь урьдчилан харахад хэрэггүй тул тайрна.
"""
import io, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'images')
BLOBS = ('C:/Users/For89/.claude/projects/C--D-General-Web-gerelt-site/'
         'f0f11d57-9155-46a2-b282-3c1491b84864/tool-results')

# (гаралтын нэр, blob-ийн сүүлийн хэсэг)
SHOTS = [
 ('pv-tulga',   '066993-cqitsq'), ('pv-hurd',    '066993-ihsjaf'),
 ('pv-tsamhag', '066993-h2g2st'), ('pv-egnee',   '066993-ico2it'),
 ('pv-zah',     '100647-55hh6l'), ('pv-sav',     '100647-v1l4iq'),
 ('pv-tulhuur', '110985-8k3gi2'), ('pv-horshoo', '110985-rz7hvz'),
 ('pv-guurs',   '116207-28w8bq'), ('pv-utaa',    '116207-fa39gn'),
 ('pv-navch',   '121548-zcn8dt'), ('pv-togoo',   '121548-9tutsm'),
 ('pv-or',      '126753-ujwpgr'), ('pv-huudas',  '126753-v272kd'),
 ('pv-zurag',   '131837-uz7y29'), ('pv-suljee',  '131837-91tc97'),
 # 5 дэх багц — катигор бүрийн 5 дэх загвар
 ('pv-guur',    '973877-fh0w16'), ('pv-torgon',  '973877-wl56w0'),
 ('pv-zoolon',  '978473-l1vie1'), ('pv-duu',     '978474-tta07w'),
 # Боловсрол
 ('pv-surah',      '923669-ef0yw7'), ('pv-mergejil',   '923669-mkad7f'),
 ('pv-onlain',     '923669-dbfd3b'), ('pv-tsetserleg', '930535-3oln89'),
 ('pv-ihsurguuli', '930535-381h5n'),
]

RIBBON = 0.072      # дээд туузны эзлэх хувь
TARGET = 16 / 10.0  # картын харьцаа

def main():
    os.makedirs(OUT, exist_ok=True)
    rows, missing = [], []
    for name, tag in SHOTS:
        hits = [f for f in os.listdir(BLOBS) if tag in f]
        if not hits:
            missing.append(name); continue
        im = Image.open(os.path.join(BLOBS, hits[0])).convert('RGB')
        w, h = im.size
        im = im.crop((0, int(h * RIBBON), w, h))      # тууз тайрна
        w, h = im.size
        if w / h > TARGET:                            # 16:10 болгоно
            nw = int(h * TARGET); im = im.crop(((w - nw)//2, 0, (w - nw)//2 + nw, h))
        else:
            nh = int(w / TARGET); im = im.crop((0, 0, w, nh))
        if im.width > 760:
            im = im.resize((760, int(760 / TARGET)), Image.LANCZOS)
        dest = os.path.join(OUT, name + '.webp')
        im.save(dest, 'WEBP', quality=76, method=6)
        rows.append((name, '%dx%d' % im.size, os.path.getsize(dest)//1024))
    print('%-14s %-10s %s' % ('name', 'size', 'KB'))
    for r in rows:
        print('%-14s %-10s %d' % r)
    if missing:
        print('MISSING:', ', '.join(missing))
    tot = sum(r[2] for r in rows)
    print('total %d KB for %d previews' % (tot, len(rows)))

if __name__ == '__main__':
    main()
