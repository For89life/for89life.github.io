# -*- coding: utf-8 -*-
"""Нүүр хуудасны загварын ханыг _build-cat.py-ийн CATS-аас үүсгэнэ.

Категор нэмэх болгонд index.html-ийг гараар засах нь алдаа
дагуулдаг: тайл, шүүлтүүрийн товч, тоо, гарчиг дөрвөн өөр
газарт давхардаж бичигдэнэ. Эндээс нэг эх сурвалжаас бүгдийг
нь үүсгэнэ.

index.html дотор дараах тэмдэглэгээнүүдийн хооронд бичнэ:
    <!-- WALL:BAR --> ... <!-- /WALL:BAR -->
    <!-- WALL:TILES --> ... <!-- /WALL:TILES -->
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location('buildcat', os.path.join(HERE, '_build-cat.py'))
buildcat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(buildcat)
CATS = buildcat.CATS

# Хананы товчны богино нэр (категорын бүтэн нэр хэт урт)
SHORT = {
    'corporate': u'Танилцуулга', 'shop': u'Дэлгүүр',
    'restaurant': u'Ресторан', 'portfolio': u'Портфолио',
    'education': u'Боловсрол', 'health': u'Эрүүл мэнд',
    'fitness': u'Фитнес', 'travel': u'Аялал',
    'realestate': u'Үл хөдлөх', 'event': u'Арга хэмжээ',
}

MN_NUM = {
    10: u'Арван', 15: u'Арван таван', 20: u'Хорин', 25: u'Хорин таван',
    30: u'Гучин', 35: u'Гучин таван', 40: u'Дөчин', 45: u'Дөчин таван',
    50: u'Тавин',
}
MN_CAT = {4: u'дөрвөн', 5: u'таван', 6: u'зургаан', 7: u'долоон',
          8: u'найман', 9: u'есөн', 10: u'арван'}


def tiles():
    out = []
    for c in CATS:
        for it in c['items']:
            out.append(
                u'      <a class="tile" href="templates/%s/%s.html" data-cat="%s">\n'
                u'        <img src="templates/images/pv-%s.webp" alt="%s — %s загвар" loading="lazy">\n'
                u'        <span class="tn">%s<s>%s</s></span>\n'
                u'      </a>\n'
                % (c['slug'], it['f'], c['slug'], it['f'], it['n'], c['name'],
                   it['n'], it['tags'].split(u' · ')[0] + u', '
                   + it['tags'].split(u' · ')[1].lower()))
    return u''.join(out)


def bar(total):
    out = [u'      <button class="wchip" data-cat="all" aria-pressed="true">'
           u'Бүгд<span class="n">%d</span></button>\n' % total]
    for c in CATS:
        out.append(u'      <button class="wchip" data-cat="%s" aria-pressed="false">'
                   u'%s<span class="n">%d</span></button>\n'
                   % (c['slug'], SHORT.get(c['slug'], c['name']), len(c['items'])))
    return u''.join(out)


def between(s, tag, body):
    a, b = u'<!-- %s -->' % tag, u'<!-- /%s -->' % tag
    i, j = s.index(a) + len(a), s.index(b)
    return s[:i] + u'\n' + body + u'    ' + s[j:]


def main():
    total = sum(len(c['items']) for c in CATS)
    f = os.path.join(ROOT, 'index.html')
    s = io.open(f, encoding='utf-8').read()
    s = between(s, 'WALL:TILES', tiles())
    s = between(s, 'WALL:BAR', bar(total))

    # Гарчиг ба тоонууд
    head = u'%s загвар, %s категор' % (
        MN_NUM.get(total, str(total)), MN_CAT.get(len(CATS), str(len(CATS))))
    s = re.sub(u'<h2 class="h-lg">[^<]*загвар, [^<]*категор</h2>',
               u'<h2 class="h-lg">%s</h2>' % head, s)
    s = re.sub(u'\\d+ бэлэн загвар, эсвэл',
               u'%d бэлэн загвар, эсвэл' % total, s)
    s = re.sub(u'<div><b>\\d+</b><span>Бэлэн загвар</span></div>',
               u'<div><b>%d</b><span>Бэлэн загвар</span></div>' % total, s)

    io.open(f, 'w', encoding='utf-8').write(s)
    print('home synced: %d tiles, %d categories, heading "%s"'
          % (total, len(CATS), head.encode('ascii', 'backslashreplace').decode()))


if __name__ == '__main__':
    main()
