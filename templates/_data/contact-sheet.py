# -*- coding: utf-8 -*-
"""Pexels-ийн зургийн хувилбаруудыг нэг хуудсанд зэрэгцүүлнэ.

Яагаад: зургийг URL-ээр нь сохроор сонговол загварын чанар
унана. Хөтчийн самбар нарийн тул олон хувилбарыг зэрэг харах
боломжгүй. Иймд жижиг хувилбаруудыг татаж, шошготой тор болгож
нэг PNG болгоно — түүнийг бүтнээр нь харж сонгоно.

Хэрэглээ:
    python contact-sheet.py sheet-spec.json out.png

sheet-spec.json  =  {"нүүр": [11844304, 7653719], "p1": [...]}
"""
import io, json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

THUMB = (210, 266)       # нэг хувилбарын хэмжээ
GAP, PADL, HDR = 8, 10, 26
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0 Safari/537.36')
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.sheet-cache')


def grab(pid):
    """Жижиг хувилбарыг татаж кэшлэнэ."""
    os.makedirs(CACHE, exist_ok=True)
    dest = os.path.join(CACHE, '%s.jpg' % pid)
    if os.path.exists(dest):
        return dest
    url = ('https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg'
           '?auto=compress&cs=tinysrgb&w=%d&h=%d&fit=crop'
           % (pid, pid, THUMB[0] * 2, THUMB[1] * 2))
    subprocess.run(['curl', '-sL', '-A', UA, '-o', dest, url], check=True)
    if os.path.getsize(dest) < 2000:
        os.remove(dest)
        return None
    return dest


def font(sz):
    for p in (r'C:\Windows\Fonts\segoeui.ttf', r'C:\Windows\Fonts\arial.ttf'):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main():
    spec = json.load(io.open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2]
    cols = max(len(v) for v in spec.values())
    w = PADL * 2 + cols * THUMB[0] + (cols - 1) * GAP
    rowh = HDR + THUMB[1] + 16 + GAP
    im = Image.new('RGB', (w, PADL * 2 + rowh * len(spec)), (17, 17, 19))
    d = ImageDraw.Draw(im)
    fh, fs = font(17), font(13)

    y, missing = PADL, []
    for slot, ids in spec.items():
        d.text((PADL, y), slot, font=fh, fill=(254, 196, 58))
        y += HDR
        x = PADL
        for pid in ids:
            p = grab(pid)
            if p:
                t = Image.open(p).convert('RGB').resize(THUMB, Image.LANCZOS)
                im.paste(t, (x, y))
            else:
                missing.append(pid)
                d.rectangle([x, y, x + THUMB[0], y + THUMB[1]], fill=(60, 30, 30))
            d.text((x + 2, y + THUMB[1] + 2), str(pid), font=fs, fill=(200, 200, 200))
            x += THUMB[0] + GAP
        y += THUMB[1] + 16 + GAP

    im.save(out, 'PNG')
    print('sheet %s  %dx%d  slots=%d' % (out, im.width, im.height, len(spec)))
    if missing:
        print('MISSING:', missing)


if __name__ == '__main__':
    main()
