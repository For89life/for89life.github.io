# -*- coding: utf-8 -*-
"""Нүүр хуудасны загварын жагсаалтыг _build-cat.py-ийн CATS-аас үүсгэнэ.

Категор нэмэх болгонд index.html-ийг гараар засах нь алдаа
дагуулдаг: тайл, гарчиг, тоо дөрвөн өөр газарт давхардаж
бичигдэнэ. Эндээс нэг эх сурвалжаас бүгдийг нь үүсгэнэ.

Бүтэц нь нугалдаг (accordion): категор бүр хаалттай мөр,
дарахад доороо таван тайл дэлгэнэ. Тавин тайлыг нэг дор асгах
нь (а) хуудсыг хэмжээгүй урт болгож, (б) сонголтыг хүндрүүлж,
(в) 50 зураг ачаалдаг байв.

index.html дотор дараах тэмдэглэгээнүүдийн хооронд бичнэ:
    <!-- WALL:BAR -->   ... <!-- /WALL:BAR -->
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

# Мөрний богино нэр (категорын бүтэн нэр хэт урт)
SHORT = {
    'corporate': u'Танилцуулга', 'shop': u'Дэлгүүр',
    'restaurant': u'Ресторан', 'portfolio': u'Портфолио',
    'education': u'Боловсрол', 'health': u'Эрүүл мэнд',
    'fitness': u'Фитнес', 'travel': u'Аялал',
    'realestate': u'Үл хөдлөх', 'event': u'Арга хэмжээ',
}

# Мөрний тайлбар. §1-ийн дагуу өгүүлбэр биш, зэрэгцүүлсэн
# нэрлэсэн холбоо үг — нэг харцаар уншигдана.
DESC = {
    'corporate': u'Компани, байгууллагын нүүр',
    'shop': u'Сагс, захиалга, төлбөр',
    'restaurant': u'Цэс, байршил, ширээний захиалга',
    'portfolio': u'Ажлын сан, хувь хүн',
    'education': u'Элсэлт, хөтөлбөр, төлбөр',
    'health': u'Цаг авах, үнэ, бэлтгэл',
    'fitness': u'Хуваарь, гишүүнчлэл, цаг захиалга',
    'travel': u'Багц, улирал, захиалга',
    'realestate': u'Зар, төсөл, түрээс',
    'event': u'Хурим, корпорейт, танхим',
}

# 16:10 харьцаатай хоосон SVG. src-гүй <img> нь хүчингүй HTML тул
# хараахан ачаалаагүй тайлуудад үүнийг түр тавина — сүлжээнд хүсэлт
# үүсгэхгүй, зургийн байрыг барина.
BLANK = (u"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'"
         u" width='16' height='10'%3E%3C/svg%3E")

MN_NUM = {
    10: u'Арван', 15: u'Арван таван', 20: u'Хорин', 25: u'Хорин таван',
    30: u'Гучин', 35: u'Гучин таван', 40: u'Дөчин', 45: u'Дөчин таван',
    50: u'Тавин',
}
MN_CAT = {4: u'дөрвөн', 5: u'таван', 6: u'зургаан', 7: u'долоон',
          8: u'найман', 9: u'есөн', 10: u'арван'}


def tile(cat, it, eager):
    """Нэг загварын тайл.

    Шинэ цонхонд нээнэ — доорх тайлбар яг үүнийг амлаж байгаа
    бөгөөд 50 загвар үзэж буй хүн болгонд Буцах дарахгүй.

    Хаалттай категорын зургийг src биш data-src-д хадгална.
    loading="lazy" энд тус болохгүй: хаалттай хавтас тэг
    өндөртэй тул хөтөч түүнийг «дэлгэц дээр байна» гэж үзээд
    бүгдийг татдаг — хэмжихэд 50-аас 36 нь, 645KB татагдаж байв.
    """
    tags = it['tags'].split(u' · ')
    # src нь <img>-ийн заавал байх шинж. data-src дээр үлдээвэл
    # HTML хүчингүй болно, иймд 16:10 хоосон SVG тавина —
    # сүлжээнд хүсэлт үүсгэхгүй, харьцааг нь барина.
    src = (u'src="templates/images/pv-%s.webp" loading="lazy"' % it['f']
           if eager else
           u'src="%s" data-src="templates/images/pv-%s.webp"' % (BLANK, it['f']))
    return (
        u'          <a class="tile" href="templates/%s/%s.html"'
        u' target="_blank" rel="noopener">\n'
        u'            <img %s alt="%s — %s загвар">\n'
        u'            <span class="tn">%s<s>%s</s></span>\n'
        u'          </a>\n'
        % (cat['slug'], it['f'], src, it['n'], cat['name'],
           it['n'], tags[0] + u', ' + tags[1].lower()))


def acc():
    out = []
    for i, c in enumerate(CATS):
        slug = c['slug']
        first = (i == 0)
        out.append(
            u'      <div class="wcat" data-open="%s">\n'
            u'        <h3 class="wcat-h"><button type="button" class="wcat-b"'
            u' id="wb-%s" aria-expanded="%s" aria-controls="wc-%s">\n'
            u'          <span class="wcat-x">%02d</span>\n'
            u'          <span class="wcat-n">%s</span>\n'
            u'          <span class="wcat-d">%s</span>\n'
            u'          <span class="wcat-c">%d загвар</span>\n'
            u'          <span class="wcat-i" aria-hidden="true"></span>\n'
            u'        </button></h3>\n'
            # Нэртэй <section> нь region-ийн утгыг аль хэдийн өгдөг тул
            # role="region" давхар бичих шаардлагагүй
            u'        <section class="wcat-p" id="wc-%s"'
            u' aria-labelledby="wb-%s"><div class="wcat-in">\n'
            u'          <div class="wall">\n'
            % (u'true' if first else u'false', slug,
               u'true' if first else u'false', slug, i + 1,
               SHORT.get(slug, c['name']), DESC.get(slug, u''),
               len(c['items']), slug, slug))
        for it in c['items']:
            out.append(tile(c, it, first))
        out.append(u'          </div>\n'
                   u'        </div></section>\n'
                   u'      </div>\n')
    return u''.join(out)


def bar(total):
    return (u'      <p class="wall-sum">%d категор · %d загвар</p>\n'
            u'      <button type="button" class="wchip" id="wallAll" aria-pressed="false">'
            u'Бүгдийг нээх</button>\n' % (len(CATS), total))


def between(s, tag, body):
    a, b = u'<!-- %s -->' % tag, u'<!-- /%s -->' % tag
    i, j = s.index(a) + len(a), s.index(b)
    return s[:i] + u'\n' + body + u'    ' + s[j:]


def main():
    total = sum(len(c['items']) for c in CATS)
    f = os.path.join(ROOT, 'index.html')
    s = io.open(f, encoding='utf-8').read()
    s = between(s, 'WALL:TILES', acc())
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
    print('home synced: %d categories, %d tiles, heading "%s"'
          % (len(CATS), total, head.encode('ascii', 'backslashreplace').decode()))


if __name__ == '__main__':
    main()
