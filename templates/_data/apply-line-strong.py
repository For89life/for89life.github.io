# -*- coding: utf-8 -*-
"""--line-strong токеныг нэмж, элементийн хүрээнд хэрэглэнэ.

Яагаад: --line / --line2 токенууд 1.5–2.2:1 өгдөг. Тэдгээр нь
тусгаарлах зураасанд зориулагдсан. Харин товч, input, chip зэргийн
хүрээ нь элементийг таниулах цорын ганц дохио учраас WCAG 1.4.11-ээр
3:1 шаардагдана.

Зөвхөн доорх ангиудад хэрэглэнэ. Зураас, картын хүрээ хэвээр —
тэдгээрийг агуулга нь (зураг, дүүргэлт) өөрөө таниулдаг.

Дахин ажиллуулахад аюулгүй: токен байвал дахин нэмэхгүй, зөвхөн
үлдсэн хүрээг сольно.
"""
import io, json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # templates/
ROOT = os.path.dirname(BASE)

# Хүрээ нь элементийг таниулдаг ангиуд
CLASSES = {
    'btn', 'btn-s', 'back', 'olist', 'icb', 'ib', 'cat', 'mtab',
    'add', 'srv-act', 'chip', 'tpl-act', 'mbtn', 'nf',
}
# Хүрээ нь заавал хэрэгтэй элементүүд
ELEMENTS = {'input', 'textarea', 'select'}

RULE = re.compile(r'([^{}]+)\{([^{}]*)\}', re.S)
# --line, --line2, --line-2 бүгдийг барина
BORDER = re.compile(
    r'(border(?:-(?:top|right|bottom|left))?(?:-color)?\s*:[^;]*?)'
    r'var\(--line-?2?\)')
CLS = re.compile(r'\.([a-zA-Z][\w-]*)')
EL = re.compile(r'(?:^|[\s,>+~])([a-z]+)(?=[\s,:\[{]|$)')

def wants(sel):
    s = sel.strip()
    if s.startswith('@') or s.startswith(':root') or not s:
        return False
    for part in s.split(','):
        p = part.strip().lower()
        if CLASSES & set(c.lower() for c in CLS.findall(p)):
            return True
        if ELEMENTS & set(EL.findall(p)):
            return True
    return False

def main():
    data = json.load(io.open(os.path.join(BASE, '_data', 'line-strong.json'),
                             encoding='utf-8'))
    report = []
    for rel, info in sorted(data.items()):
        path = os.path.join(ROOT, rel.replace('/', os.sep))
        s = io.open(path, encoding='utf-8').read()

        if '--line-strong' in s:
            # Утгыг шинэчилнэ — гадаргуу бүрээр дахин тооцсон
            s = re.sub(r'--line-strong\s*:\s*#[0-9A-Fa-f]{3,8}\s*;',
                       '--line-strong:%s;' % info['line_strong'], s, count=1)
        else:
            m = re.search(r'(:root\{)', s)
            if not m:
                report.append((rel, 'NO :root', 0)); continue
            token = ('\n  /* Элементийн хүрээ. --line нь зураасанд, энэ нь\n'
                     '     товч, input, chip-д. Загварын хамгийн таагүй\n'
                     '     гадаргуу дээр ч %s:1 — WCAG 1.4.11. */\n'
                     '  --line-strong:%s;' % (info['ratio'], info['line_strong']))
            s = s[:m.end(1)] + token + s[m.end(1):]

        changed = [0]
        def repl_rule(mo):
            sel, body = mo.group(1), mo.group(2)
            if not wants(sel):
                return mo.group(0)
            new, n = BORDER.subn(r'\1var(--line-strong)', body)
            changed[0] += n
            return sel + '{' + new + '}'

        head, sep, rest = s.partition('<style>')
        css, sep2, tail = rest.partition('</style>')
        css = RULE.sub(repl_rule, css)
        s = head + sep + css + sep2 + tail

        io.open(path, 'w', encoding='utf-8', newline='').write(s)
        report.append((rel, info['line_strong'], changed[0]))

    print('%-34s %-10s %s' % ('file', 'token', 'swapped'))
    for rel, tok, n in report:
        print('%-34s %-10s %s' % (rel[-34:], tok, n))
    print('total swaps this run: %d' % sum(n for _, _, n in report))

if __name__ == '__main__':
    main()
