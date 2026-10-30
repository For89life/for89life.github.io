# -*- coding: utf-8 -*-
"""Загварын зургийг татаж, тайрч, WebP болгоод, бичвэрийн
уншигдацыг шалгана.

Pexels API шинэ түлхүүр олгохоо зогсоосон тул зургийг шууд
images.pexels.com-оос татна. Лиценз хэвээр зөвшөөрнө: сайтаас
татахад attribution шаардахгүй, «a template you sell» нь
зөвшөөрөгдсөн хэрэглээнд багтдаг.

Юу хийдэг вэ:
  1. Зургийг татна (w=1800 хүртэл)
  2. Зорилтот харьцаанд төвөөс тайрна
  3. Өргөнийг багасгаж WebP болгоно
  4. Бичвэр сууж буй ЗУРВАСЫН гэрэлтүүлгийг хэмжиж, одоогийн
     далд давхарга хангалттай эсэхийг тооцно

4-р алхам нь гол нь: градиент дээр хийсэнтэй адил, зураг дээрх
бичвэрийг хамгийн цайвар хэсгээр нь хэмжинэ. Хангалтгүй бол
шаардагдах далд давхаргын хүчийг хэлж өгнө.
"""
import io, json, math, os, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.dirname(HERE)
OUT = os.path.join(TPL, 'images')
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0 Safari/537.36')

RATIO = {'landscape': 16/10.0, 'wide': 16/9.0, 'square': 1.0,
         'portrait': 3/4.0, 'tall': 3/5.0}

def srgb_to_lin(c):
    c = c / 255.0
    return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055) ** 2.4

def luminance(rgb):
    r, g, b = (srgb_to_lin(v) for v in rgb)
    return 0.2126*r + 0.7152*g + 0.0722*b

def contrast(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)

def band_luminance(im, band):
    """Бичвэр сууж буй зурвасын хамгийн цайвар хэсгийг олно.
    Дунджаар биш — 90-р хувьсагчаар, учир нь цөөхөн цайвар пиксэл
    ч бичвэрийг уншихгүй болгоно."""
    w, h = im.size
    if band == 'top':    box = (0, 0, w, int(h*0.34))
    elif band == 'bottom': box = (0, int(h*0.66), w, h)
    elif band == 'center': box = (int(w*0.1), int(h*0.3), int(w*0.9), int(h*0.7))
    else:                box = (0, 0, w, h)
    crop = im.crop(box).convert('RGB').resize((64, 64))
    lums = sorted(luminance(p) for p in crop.getdata())
    return lums[int(len(lums)*0.90)]          # 90-р хувьсагч

def fetch(url, dest):
    sep = '&' if '?' in url else '?'
    full = url + sep + 'auto=compress&cs=tinysrgb&w=1800'
    r = subprocess.run(['curl', '-sL', '-A', UA, '-o', dest, '-w', '%{http_code}'],
                       input=full, capture_output=True, text=True)
    code = subprocess.run(['curl', '-sL', '-A', UA, '-o', dest,
                           '-w', '%{http_code}', full],
                          capture_output=True, text=True).stdout.strip()
    return code == '200' and os.path.getsize(dest) > 10000

def process(spec):
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for item in spec:
        name = item['name']
        tmp = os.path.join(OUT, name + '.src')
        if not fetch(item['url'], tmp):
            rows.append((name, 'DOWNLOAD FAILED', '', '', ''))
            continue
        im = Image.open(tmp).convert('RGB')
        # Зорилтот харьцаанд төвөөс тайрна
        target = RATIO[item['shape']]
        w, h = im.size
        if w / h > target:
            nw = int(h * target); x = (w - nw)//2
            im = im.crop((x, 0, x+nw, h))
        else:
            nh = int(w / target); y = int((h - nh) * item.get('focus', 0.5))
            im = im.crop((0, y, w, y+nh))
        maxw = item.get('maxw', 1400)
        if im.width > maxw:
            im = im.resize((maxw, int(maxw / target)), Image.LANCZOS)
        dest = os.path.join(OUT, name + '.webp')
        im.save(dest, 'WEBP', quality=item.get('q', 80), method=6)
        os.remove(tmp)

        band = item.get('band')
        verdict = '-'
        if band:
            l = band_luminance(im, band)
            scrim = item.get('scrim', 0.0)
            l_s = l * (1 - scrim) ** 2.2        # ойролцоогоор далдалсны дараа
            need = item.get('need', 4.5)
            r = contrast(1.0, l_s)              # цагаан бичвэр
            if r >= need:
                verdict = 'ok %.2f' % r
            else:
                # шаардагдах далд давхаргыг хайна
                k = scrim
                while k < 0.95 and contrast(1.0, l*(1-k)**2.2) < need:
                    k += 0.01
                verdict = 'NEED scrim %.2f (now %.2f -> %.2f)' % (k, scrim, r)
        kb = os.path.getsize(dest)//1024
        rows.append((name, '%dx%d' % im.size, '%dKB' % kb,
                     item['shape'], verdict))
    print('%-22s %-11s %-7s %-10s %s' % ('name','size','weight','shape','text band'))
    for r in rows:
        print('%-22s %-11s %-7s %-10s %s' % r)
    total = sum(os.path.getsize(os.path.join(OUT, f))
                for f in os.listdir(OUT) if f.endswith('.webp'))
    print('\ntotal in templates/images: %d KB' % (total//1024))

if __name__ == '__main__':
    spec = json.load(io.open(sys.argv[1], encoding='utf-8'))
    process(spec)
