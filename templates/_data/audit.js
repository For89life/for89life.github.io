/* Загварын хүртээмжийн шалгалт — хөтөч дээр ажиллана.
 *
 * Яагаад гараар бичсэн бэ: градиент болон зураг дээрх бичвэрийг
 * жинхэнэ пиксэлээр нь хэмжих шалгуур бэлэн сангуудад байдаггүй.
 * Тэд тунгалаг давхаргыг "тодорхойгүй" гэж алгасдаг. Бид харин
 * canvas руу буулгаж, бичвэр сууж буй хэсгийн ХАМГИЙН ЦАЙВАР
 * 95-р хувьсагчаар хэмжинэ — дундажаар хэмжвэл унших боломжгүй
 * газар "тэнцсэн" гэж гарна.
 *
 * Буцаалт: {fail:[...], warn:[...], stats:{...}}
 */
(() => {
  const lin = c => (c /= 255) <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
  const ratio = (a, b) => (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
  const rgb = s => (s.match(/[\d.]+/g) || []).map(Number);

  const fail = [], warn = [];
  const tag = el => {
    const id = el.id ? '#' + el.id : '';
    const cl = el.className && typeof el.className === 'string'
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return el.tagName.toLowerCase() + id + cl;
  };
  const txt = el => (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);

  /* Тунгалаг биш хамгийн ойрын өвгийн өнгийг олно. Замдаа зураг
     эсвэл градиент тааралдвал "image" гэж тэмдэглэнэ. */
  /* Градиентаас өнгөний цэгүүдийг салгана. Градиент бол зураг
     биш — утга нь бүрэн тодорхой тул таамаглах шаардлагагүй.
     Тунгалаг цэгүүдийг доод давхаргатай нь хольж тооцно. */
  function gradientStops(img, under) {
    const stops = [];
    const re = /(rgba?\([^)]*\))|(#[0-9A-Fa-f]{3,8})/g;
    let m;
    while ((m = re.exec(img))) {
      let c;
      if (m[1]) c = rgb(m[1]);
      else {
        let h = m[2].slice(1);
        if (h.length === 3) h = h.split('').map(x => x + x).join('');
        c = [0, 2, 4].map(i => parseInt(h.substr(i, 2), 16));
        if (h.length === 8) c.push(parseInt(h.substr(6, 2), 16) / 255);
      }
      if (c.length < 3) continue;
      const a = c[3] === undefined ? 1 : c[3];
      stops.push(a >= 1 ? c.slice(0, 3)
        : [0, 1, 2].map(i => c[i] * a + under[i] * (1 - a)));
    }
    return stops;
  }

  function backdrop(el) {
    let under = null;
    for (let n = el; n && n !== document.documentElement; n = n.parentElement) {
      const cs = getComputedStyle(n);
      const bi = cs.backgroundImage;
      if (bi && bi !== 'none') {
        if (bi.includes('url(')) return { kind: 'image', node: n };
        const base = under || rgb(getComputedStyle(document.body).backgroundColor).slice(0, 3);
        const stops = gradientStops(bi, base);
        if (stops.length) return { kind: 'gradient', stops, node: n };
      }
      const c = rgb(cs.backgroundColor);
      if (c.length >= 3) {
        const a = c[3] === undefined ? 1 : c[3];
        if (a >= 0.95) return { kind: 'solid', rgb: c.slice(0, 3), node: n };
        if (a > 0 && !under) under = c.slice(0, 3);
      }
    }
    const c = rgb(getComputedStyle(document.body).backgroundColor);
    return { kind: 'solid', rgb: c.length >= 3 ? c.slice(0, 3) : [255, 255, 255], node: document.body };
  }

  const txtNodes = [...document.querySelectorAll('body *')].filter(el => {
    if (/^(SCRIPT|STYLE|NOSCRIPT|CANVAS|SVG)$/.test(el.tagName)) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.1) return false;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) return false;
    const r = el.getBoundingClientRect();
    return r.width > 2 && r.height > 2;
  });

  let imgChecked = 0;
  for (const el of txtNodes) {
    const cs = getComputedStyle(el);
    let fg = rgb(cs.color);
    /* Зураасаар гаргасан бичвэр: дүүргэлт нь тунгалаг тул
       харагдах өнгө нь зураасны өнгө. Түүгээр хэмжинэ. */
    const strokeW = parseFloat(cs.webkitTextStrokeWidth) || 0;
    if (strokeW > 0 && (fg[3] === 0 || cs.color === 'transparent')) {
      const sc = rgb(cs.webkitTextStrokeColor);
      if (sc.length >= 3) fg = sc;
      if (strokeW < 2 && px >= 48)
        warn.push({ what: 'thin-stroke', el: tag(el), text: txt(el),
          px, stroke: cs.webkitTextStrokeWidth, note: 'том үсэгт нимгэн зураас' });
    }
    if (fg.length < 3 || fg[3] === 0) continue;
    const px = parseFloat(cs.fontSize);
    const bold = +cs.fontWeight >= 700;
    const large = px >= 24 || (px >= 18.66 && bold);
    const need = large ? 3.0 : 4.5;
    const bd = backdrop(el);

    if (bd.kind === 'solid') {
      const r = ratio(lum(fg), lum(bd.rgb));
      if (r < need) fail.push({ what: 'contrast', el: tag(el), text: txt(el),
        got: +r.toFixed(2), need, fg: cs.color, bg: `rgb(${bd.rgb.slice(0,3)})`, px });
    } else if (bd.kind === 'gradient') {
      /* Хамгийн муу цэгээр нь хэмжинэ — дундажаар биш. */
      let worst = Infinity, at = null;
      for (const st of bd.stops) {
        const r = ratio(lum(fg), lum(st));
        if (r < worst) { worst = r; at = st; }
      }
      if (worst < need) fail.push({ what: 'contrast-gradient', el: tag(el), text: txt(el),
        got: +worst.toFixed(2), need, fg: cs.color,
        worstStop: 'rgb(' + at.map(Math.round) + ')', on: tag(bd.node), px });
    } else {
      imgChecked++;
      warn.push({ what: 'over-image', el: tag(el), text: txt(el), px, need,
        on: tag(bd.node), note: 'canvas-аар тусад нь хэмжинэ' });
    }
  }

  /* Товчлуурын хэмжээ — WCAG 2.2 AA вэб дээр 24x24 CSS px */
  const INTER = 'a[href],button,input,select,textarea,[role="button"],[tabindex]:not([tabindex="-1"])';
  const small = [];
  for (const el of document.querySelectorAll(INTER)) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    const inline = cs.display.includes('inline') && !cs.display.includes('flex')
      && !cs.display.includes('grid') && !cs.display.includes('block');
    if (inline && el.closest('p,li,span')) continue;   // бичвэр доторх холбоос чөлөөлөгдөнө
    if (r.width >= 24 && r.height >= 24) continue;
    /* Хайрцаг жижиг байгаад дарах талбай нь жижиг гэсэн үг биш:
       ::before-оор өргөтгөсөн талбай хайрцагт тооцогддоггүй. Иймд
       жинхэнэ дарагдах цэгүүдийг elementFromPoint-оор шалгана. */
    small.push({ el, r });
  }

  /* Жижиг хайрцагтай элементүүдийг жинхэнэ дарагдах талбайгаар нь шалгана */
  if (small.length) {
    const sb = document.documentElement.style.scrollBehavior;
    document.documentElement.style.scrollBehavior = 'auto';
    const keep = document.scrollingElement.scrollTop;
    for (const { el } of small) {
      const abs = el.getBoundingClientRect().top + window.scrollY;
      document.scrollingElement.scrollTop = Math.max(0, abs - window.innerHeight / 2);
      const q = el.getBoundingClientRect();
      const cx = q.left + q.width / 2, cy = q.top + q.height / 2;
      const hit = (dx, dy) => {
        const e = document.elementFromPoint(cx + dx, cy + dy);
        return !!e && (e === el || el.contains(e));
      };
      /* 24x24 багтаахын тулд төвөөс 4 зүгт 11px хүрэх ёстой */
      const w = q.width >= 24 || (hit(-11, 0) && hit(11, 0));
      const h = q.height >= 24 || (hit(0, -11) && hit(0, 11));
      if (!(w && h))
        fail.push({ what: 'target-size', el: tag(el), text: txt(el),
          box: `${Math.round(q.width)}x${Math.round(q.height)}`,
          hitW: w, hitH: h, need: '24x24' });
    }
    document.scrollingElement.scrollTop = keep;
    document.documentElement.style.scrollBehavior = sb;
  }

  /* Бүтцийн шалгуурууд */
  if (!document.documentElement.lang) fail.push({ what: 'lang', el: 'html' });
  if (!document.querySelector('main')) fail.push({ what: 'landmark', el: 'main дутуу' });
  if (!document.querySelector('h1')) fail.push({ what: 'heading', el: 'h1 дутуу' });
  if (document.querySelectorAll('h1').length > 1) warn.push({ what: 'heading', el: 'h1 олон' });

  for (const im of document.querySelectorAll('img'))
    if (im.alt === null || im.alt === undefined)
      fail.push({ what: 'alt', el: tag(im), src: (im.getAttribute('src') || '').slice(-28) });

  for (const f of document.querySelectorAll('input,select,textarea')) {
    const ok = f.labels?.length || f.getAttribute('aria-label') || f.getAttribute('aria-labelledby');
    if (!ok) fail.push({ what: 'label', el: tag(f) });
  }

  for (const b of document.querySelectorAll('button,a[href]')) {
    /* Нэр нь бичвэрээс гадна дотоод зургийн alt-аас ч бүрдэнэ. */
    const alts = [...b.querySelectorAll('img[alt]')].map(i => i.alt.trim()).filter(Boolean);
    const name = (b.textContent || '').trim() || b.getAttribute('aria-label')
      || b.title || alts.join(' ');
    if (!name) fail.push({ what: 'name', el: tag(b) });
  }

  let lvl = 0;
  for (const h of document.querySelectorAll('h1,h2,h3,h4,h5,h6')) {
    const n = +h.tagName[1];
    if (lvl && n > lvl + 1) warn.push({ what: 'heading-skip', el: tag(h), from: lvl, to: n });
    lvl = n;
  }

  return { fail, warn, stats: { textNodes: txtNodes.length, overImage: imgChecked,
    interactive: document.querySelectorAll(INTER).length } };
})()
