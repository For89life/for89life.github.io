# -*- coding: utf-8 -*-
"""Нийгмийн сүлжээнд хуваалцахад гарах зургийг (1200x630) үүсгэнэ.

Монголд холбоос голдуу Messenger, Facebook-аар тархдаг. Зураггүй
холбоос нь дизайн студийн хувьд өөрийгөө няцаасан хэрэг тул энд
загваруудын ЖИНХЭНЭ дэлгэцийн зургаас мозайк хийж, дээр нь студийн
нэрийг тавина.

Хэрэглээ:
    python templates/_data/make-og.py
"""
import glob
import io
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.dirname(HERE)
ROOT = os.path.dirname(TPL)
IMAGES = os.path.join(TPL, 'images')
OUT = os.path.join(ROOT, 'images', 'og.jpg')

W, H = 1200, 630
BG = (10, 10, 11)
ACC = (254, 196, 58)

# Мозайкт хамгийн ялгаатай харагдах загваруудыг гараар сонгов
PICKS = ['tulga', 'utaa', 'torgon', 'onlain', 'zaal', 'guurs',
         'ihsurguuli', 'lab', 'ayalal', 'hurim', 'barilga', 'tsetseg']


def font(size, bold=False):
    names = [r'C:\Windows\Fonts\segoeuib.ttf' if bold else r'C:\Windows\Fonts\segoeui.ttf',
             r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf']
    for p in names:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def main():
    im = Image.new('RGB', (W, H), BG)

    # Дээд 58% — загваруудын мозайк
    cols, rows = 4, 2
    band_h = int(H * 0.58)
    cw, ch = W // cols, band_h // rows
    used = 0
    for r in range(rows):
        for c in range(cols):
            while used < len(PICKS):
                src = os.path.join(IMAGES, 'pv-%s.webp' % PICKS[used])
                used += 1
                if os.path.exists(src):
                    break
            else:
                continue
            t = Image.open(src).convert('RGB')
            # cover
            s = max(cw / t.width, ch / t.height)
            t = t.resize((int(t.width * s), int(t.height * s)), Image.LANCZOS)
            x = (t.width - cw) // 2
            t = t.crop((x, 0, x + cw, ch))
            im.paste(t, (c * cw, r * ch))

    # Мозайкийг доош нь бүдгэрүүлж, бичвэрийн зай гаргана
    grad = Image.new('L', (1, band_h))
    for y in range(band_h):
        f = y / band_h
        grad.putpixel((0, y), int(255 * min(1.0, max(0.0, (f - 0.45) / 0.55))))
    grad = grad.resize((W, band_h))
    im.paste(Image.new('RGB', (W, band_h), BG), (0, 0), grad)

    d = ImageDraw.Draw(im)
    f_big = font(62, bold=True)
    f_mid = font(30)
    f_sm = font(25)

    y = int(H * 0.56)
    d.text((64, y), 'Gerelt Solutions Studio', font=f_big, fill=(255, 255, 255))
    y += 84
    d.text((64, y), u'50 \u0431\u044d\u043b\u044d\u043d \u0437\u0430\u0433\u0432\u0430\u0440 \u00b7 10 \u043a\u0430\u0442\u0435\u0433\u043e\u0440',
           font=f_mid, fill=ACC)
    y += 46
    d.text((64, y), u'\u0412\u044d\u0431, \u043c\u043e\u0431\u0430\u0439\u043b, \u043e\u043d\u043b\u0430\u0439\u043d \u0434\u044d\u043b\u0433\u04af\u04af\u0440 \u2014 \u0423\u043b\u0430\u0430\u043d\u0431\u0430\u0430\u0442\u0430\u0440',
           font=f_sm, fill=(170, 172, 180))

    # Баруун доод буланд домэйн
    dom = 'gerelt-solutuions.com'
    bb = d.textbbox((0, 0), dom, font=f_sm)
    d.text((W - 64 - (bb[2] - bb[0]), H - 64 - (bb[3] - bb[1])), dom,
           font=f_sm, fill=(140, 142, 150))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    im.save(OUT, 'JPEG', quality=86, optimize=True)
    print('og.jpg %dx%d  %d KB  (%d previews used)'
          % (im.width, im.height, os.path.getsize(OUT) // 1024, min(used, len(PICKS))))


if __name__ == '__main__':
    main()
