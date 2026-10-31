# -*- coding: utf-8 -*-
"""Бүх хуудсанд canonical, Open Graph нэмж, sitemap.xml, robots.txt үүсгэнэ.

Яагаад: og: тэг огт байхгүй байсан тул Messenger, Facebook дээр
холбоос зураггүй, гарчиггүй хоосон харагддаг байв. Монголд холбоос
голдуу тэдгээрээр тархдаг тул дизайн студийн хувьд энэ нь шууд
алдагдал.

Мөн 61 хуудастай атлаа sitemap байхгүй байсан тул Google бүгдийг
өөрөө мөлхөж олох шаардлагатай байв.

Давтан ажиллуулахад аюулгүй: өмнө нь нэмсэн блокоо олж солино.

    python templates/_data/seo.py
"""
import glob
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.dirname(HERE)
ROOT = os.path.dirname(TPL)

SITE = 'https://gerelt-solutuions.com'
OG_IMAGE = SITE + '/images/og.jpg'

MARK_OPEN = '<!-- SEO:BEGIN -->'
MARK_CLOSE = '<!-- SEO:END -->'


def pages():
    """(файлын зам, сайт дотрох зам) хосуудыг буцаана."""
    out = [(os.path.join(ROOT, 'index.html'), '/')]
    for p in sorted(glob.glob(os.path.join(TPL, '*', '*.html'))):
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        if '/_' in '/' + rel:
            continue
        url = '/' + rel
        if url.endswith('/index.html'):
            url = url[:-len('index.html')]
        out.append((p, url))
    return out


def meta(title, desc, url):
    t = title.replace('"', '&quot;')
    d = desc.replace('"', '&quot;')
    return (
        MARK_OPEN + '\n'
        '<link rel="canonical" href="%s">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:site_name" content="Gerelt Solutions Studio">\n'
        '<meta property="og:locale" content="mn_MN">\n'
        '<meta property="og:url" content="%s">\n'
        '<meta property="og:title" content="%s">\n'
        '<meta property="og:description" content="%s">\n'
        '<meta property="og:image" content="%s">\n'
        '<meta property="og:image:width" content="1200">\n'
        '<meta property="og:image:height" content="630">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="twitter:title" content="%s">\n'
        '<meta name="twitter:description" content="%s">\n'
        '<meta name="twitter:image" content="%s">\n'
        % (url, url, t, d, OG_IMAGE, t, d, OG_IMAGE)
        + MARK_CLOSE
    )


SCHEMA = u'''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Gerelt Solutions Studio",
  "url": "%s/",
  "logo": "%s/images/logo.webp",
  "image": "%s",
  "description": "Вэб хөгжүүлэлт, мобайл аппликейшн, онлайн дэлгүүр, төлбөрийн холболт. 50 бэлэн загвар.",
  "telephone": "+976-7210-0262",
  "email": "gereltsolutions01@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Улаанбаатар",
    "addressCountry": "MN"
  },
  "areaServed": { "@type": "Country", "name": "Монгол Улс" },
  "knowsLanguage": ["mn", "en"],
  "priceRange": "₮₮"
}
</script>'''


def head_of(src):
    m = re.search(r'<title>(.*?)</title>', src, re.S)
    title = m.group(1).strip() if m else 'Gerelt Solutions Studio'
    m = re.search(r'<meta name="description" content="(.*?)"', src, re.S)
    desc = m.group(1).strip() if m else ''
    return title, desc


def main():
    changed = 0
    urls = []
    for path, url in pages():
        s = io.open(path, encoding='utf-8').read()
        title, desc = head_of(s)
        block = meta(title, desc, SITE + url)

        if MARK_OPEN in s:                       # давтан ажиллуулалт
            s = re.sub(re.escape(MARK_OPEN) + '.*?' + re.escape(MARK_CLOSE),
                       block, s, flags=re.S)
        else:
            anchor = '<link rel="icon"'
            i = s.index(anchor)
            j = s.index('>', i) + 1
            s = s[:j] + '\n' + block + s[j:]

        # Schema зөвхөн нүүр хуудсанд
        if url == '/' and 'application/ld+json' not in s:
            s = s.replace('</head>', (SCHEMA % (SITE, SITE, OG_IMAGE)) + '\n</head>', 1)

        io.open(path, 'w', encoding='utf-8').write(s)
        changed += 1
        urls.append(url)

    # sitemap.xml — нүүр хамгийн чухал, категор дараа нь, загвар сүүлд
    def prio(u):
        if u == '/':
            return '1.0'
        return '0.8' if u.endswith('/') else '0.6'

    body = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        body.append('  <url><loc>%s%s</loc><priority>%s</priority></url>' % (SITE, u, prio(u)))
    body.append('</urlset>')
    io.open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(body) + '\n')

    io.open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8').write(
        'User-agent: *\n'
        'Allow: /\n'
        '\n'
        'Sitemap: %s/sitemap.xml\n' % SITE)

    print('%d pages given canonical + Open Graph' % changed)
    print('sitemap.xml: %d urls' % len(urls))
    print('robots.txt written')


if __name__ == '__main__':
    main()
