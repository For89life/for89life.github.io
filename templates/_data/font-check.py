# -*- coding: utf-8 -*-
"""Google Fonts дээрх фонт монгол кирилл үсгийг бүрэн дэмжих эсэх.

Яагаад «cyrillic байна» гэдэг хангалтгүй вэ: Google Fonts-ийн
`cyrillic` дэд олонлог нь U+0400–045F-ийг хамардаг. Монгол хэлний
хоёр гол үсэг үүнд БАГТАХГҮЙ:

    Ө ө  = U+04E8 / U+04E9   →  cyrillic-ext дотор
    Ү ү  = U+04AE / U+04AF   →  cyrillic дотор (U+04B0-04B1 биш!)

Иймд cyrillic-ext байхгүй фонт сонговол Ө үсэг өөр фонтоор орлогдож,
бичвэр жигд бус харагдана. Энэ скрипт unicode-range-уудыг задалж,
шаардлагатай кодууд үнэхээр багтаж байгааг шалгана.

Хэрэглээ:
    python font-check.py "Lora" "Jost" "Golos Text"
"""
import re
import subprocess
import sys

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0 Safari/537.36')

# Монгол хэлэнд зайлшгүй шаардлагатай кирилл үсгүүд
NEED = {
    0x04E8: u'Ө', 0x04E9: u'ө',
    0x04AE: u'Ү', 0x04AF: u'ү',
    0x0401: u'Ё', 0x0451: u'ё',
    0x042D: u'Э', 0x044D: u'э',
    0x0419: u'Й', 0x0439: u'й',
}


def ranges_for(css):
    """@font-face бүрийн unicode-range-ийг (эхлэл, төгсгөл) болгон задална."""
    out = []
    for m in re.finditer(r'unicode-range:\s*([^;]+);', css):
        for part in m.group(1).split(','):
            part = part.strip()
            mm = re.match(r'U\+([0-9A-Fa-f]+)(?:-([0-9A-Fa-f]+))?$', part)
            if not mm:
                continue
            lo = int(mm.group(1), 16)
            hi = int(mm.group(2), 16) if mm.group(2) else lo
            out.append((lo, hi))
    return out


def check(family):
    url = ('https://fonts.googleapis.com/css2?family=%s:wght@400&display=swap'
           % family.replace(' ', '+'))
    css = subprocess.run(['curl', '-s', '-A', UA, url],
                         capture_output=True, text=True).stdout
    if '@font-face' not in css:
        return family, None, [u'фонт олдсонгүй']
    rs = ranges_for(css)
    missing = [ch for cp, ch in sorted(NEED.items())
               if not any(lo <= cp <= hi for lo, hi in rs)]
    subsets = re.findall(r'/\*\s*([a-z-]+)\s*\*/', css)
    return family, sorted(set(subsets)), missing


def main():
    fams = sys.argv[1:]
    if not fams:
        print(__doc__)
        return
    bad = 0
    for f in fams:
        name, subsets, missing = check(f)
        if missing:
            bad += 1
            print('FAIL  %-20s missing: %s   subsets: %s'
                  % (name, ' '.join(missing).encode('ascii', 'backslashreplace').decode(),
                     ','.join(subsets or [])))
        else:
            print('ok    %-20s subsets: %s' % (name, ','.join(subsets)))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
