# -*- coding: utf-8 -*-
"""UI UX Pro Max-ийн colors.csv-ээс бидний дөрвөн категорт тохирох
палитруудыг салгаж, WCAG контрастыг нь тооцоод palettes.json болгоно.

Зорилго: өнгө сонгохдоо нүдээр таамаглахаа болих. Палитр бүрийн
гол хосуудыг урьдчилан хэмжиж, аль нь тэнцэж байгааг тэмдэглэнэ.
"""
import csv, io, json, os, re

SRC = ("C:/Users/For89/.claude/plugins/cache/ui-ux-pro-max-skill/"
       "ui-ux-pro-max/2.15.0/.claude/skills/ui-ux-pro-max/data/colors.csv")

# Категор → тухайн категорт утга төгөлдөр бүтээгдэхүүний төрлүүд
CATS = {
 'corporate':  ['Legal Services','Banking/Traditional Finance',
                'Construction/Architecture','Logistics/Delivery',
                'Real Estate/Property','SaaS (General)'],
 'shop':       ['E-commerce','E-commerce Luxury','Grocery & Shopping List',
                'Food Delivery / On-Demand','Luxury/Premium Brand'],
 'restaurant': ['Restaurant/Food Service','Bakery/Cafe',
                'Food Delivery / On-Demand'],
 'portfolio':  ['Portfolio/Personal','Photography Studio','Creative Agency',
                'Freelancer Platform'],
}

def lin(v):
    v = v / 255.0
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

def lum(h):
    h = h.lstrip('#')
    if len(h) != 6:
        return None
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    if la is None or lb is None:
        return None
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)

rows = list(csv.DictReader(io.open(SRC, encoding='utf-8')))
by_type = {r['Product Type']: r for r in rows}

out = {}
for cat, types in CATS.items():
    items = []
    for t in types:
        r = by_type.get(t)
        if not r:
            continue
        # Шалгах ёстой гол хосууд. Нэр → (урд, ар, шаардлага)
        pairs = {
            'body':        (r['Foreground'],        r['Background'], 4.5),
            'muted':       (r['Muted Foreground'],  r['Background'], 4.5),
            'on_card':     (r['Card Foreground'],   r['Card'],       4.5),
            'on_primary':  (r['On Primary'],        r['Primary'],    4.5),
            'on_accent':   (r['On Accent'],         r['Accent'],     4.5),
            'border':      (r['Border'],            r['Background'], 3.0),
        }
        checks, fails = {}, []
        for name, (fg, bg, need) in pairs.items():
            v = ratio(fg, bg)
            ok = v is not None and v >= need
            checks[name] = {'fg': fg, 'bg': bg, 'ratio': v,
                            'need': need, 'ok': ok}
            if not ok:
                fails.append(name)
        items.append({
            'product_type': t,
            'tokens': {k: r[v] for k, v in [
                ('bg','Background'), ('fg','Foreground'),
                ('card','Card'), ('card_fg','Card Foreground'),
                ('primary','Primary'), ('on_primary','On Primary'),
                ('accent','Accent'), ('on_accent','On Accent'),
                ('muted','Muted'), ('muted_fg','Muted Foreground'),
                ('border','Border'), ('ring','Ring'),
            ]},
            'contrast': checks,
            'failing_pairs': fails,
            'notes': r['Notes'],
        })
    out[cat] = items

base = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base, 'palettes.json')
io.open(path, 'w', encoding='utf-8', newline='').write(
    json.dumps(out, ensure_ascii=False, indent=1))

# ASCII тайлан — консолын кодчилолд унахгүй
total = sum(len(v) for v in out.values())
bad = sum(1 for v in out.values() for i in v if i['failing_pairs'])
print('palettes: %d, with failing pairs: %d' % (total, bad))
for cat, items in out.items():
    for i in items:
        mark = 'FAIL ' + ','.join(i['failing_pairs']) if i['failing_pairs'] else 'ok'
        print('  %-11s %-30s %s' % (cat, i['product_type'], mark))
