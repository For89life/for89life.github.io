# -*- coding: utf-8 -*-
"""_shots/ доторх PNG-үүдийг картын нүүрний WebP болгоно.

Өмнө нь хөтчийн blob файлыг нэрээр нь хайдаг байсан: blob-ийн нэрийг
гараар бичиж өгөх шаардлагатай, самбарын өргөнөөс хамааран хэмжээ
555–800px хооронд хэлбэлздэг байв. Одоо shots.mjs яг 1440×900-аар
авч, энэ скрипт зөвхөн багасгаж WebP болгоно.

Урсгал:
    node templates/_data/shots.mjs --only fitness
    python templates/_data/make-previews.py

(Хуучин хувилбарыг make-previews-blob.py.bak нэрээр хадгалсан.)
"""
import glob
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(os.path.dirname(HERE), 'images')
SHOTS = os.path.join(IMAGES, '_shots')

TARGET_W = 760          # картын харуулагдах өргөнөөс 2 дахин том
QUALITY = 78


def main():
    if not os.path.isdir(SHOTS):
        print('_shots/ alga - ehleed shots.mjs ajillahuul.')
        return 1
    only = sys.argv[1] if len(sys.argv) > 1 else None

    rows = []
    for src in sorted(glob.glob(os.path.join(SHOTS, '*.png'))):
        name = os.path.splitext(os.path.basename(src))[0]
        if only and only not in name:
            continue
        im = Image.open(src).convert('RGB')
        if im.width > TARGET_W:
            h = round(im.height * TARGET_W / im.width)
            im = im.resize((TARGET_W, h), Image.LANCZOS)
        dest = os.path.join(IMAGES, 'pv-%s.webp' % name)
        im.save(dest, 'WEBP', quality=QUALITY, method=6)
        rows.append((name, '%dx%d' % im.size, os.path.getsize(dest) // 1024))

    print('%-14s %-10s %s' % ('name', 'size', 'KB'))
    for r in rows:
        print('%-14s %-10s %d' % r)
    total = sum(os.path.getsize(f)
                for f in glob.glob(os.path.join(IMAGES, 'pv-*.webp')))
    print('\n%d previews written; pv-* total %d KB' % (len(rows), total // 1024))
    return 0


if __name__ == '__main__':
    sys.exit(main())
