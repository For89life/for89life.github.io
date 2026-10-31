/* Категорын хуудасны картын нүүрэн дээрх бичвэрийг шалгана.
 *
 * Нүүрний зураг бүр өөр өөр тул далд давхарга хангалттай эсэх нь
 * зураг тус бүрээр ялгаатай. Градиент далд давхаргын нягтыг
 * бичвэрийн байрлалд тооцож, доорх зургийн ХАМГИЙН ЦАЙВАР
 * 95-р хувьсагчтай нийлүүлж хэмжинэ.
 *
 * Image.decode() нь далд табад гацдаг тул createImageBitmap
 * ашиглана.
 */
(async () => {
  const lin = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };

  /* .cover-ийн далд давхаргын цэгүүд (_build-cat.py-тай тааруулсан) */
  const STOPS = [[0, .8], [.38, .2], [.60, .26], [1, .84]];
  const alphaAt = fy => {
    for (let i = 1; i < STOPS.length; i++) {
      const [p0, a0] = STOPS[i - 1], [p1, a1] = STOPS[i];
      if (fy <= p1) return a0 + (a1 - a0) * ((fy - p0) / (p1 - p0));
    }
    return STOPS[STOPS.length - 1][1];
  };

  const out = [];
  for (const cov of document.querySelectorAll('.cover')) {
    const cr = cov.getBoundingClientRect();
    const url = getComputedStyle(cov).backgroundImage.slice(5, -2);
    let bm;
    try { bm = await createImageBitmap(await (await fetch(url)).blob()); }
    catch (e) { out.push({ card: url.split('/').pop(), error: String(e) }); continue; }

    /* background-size:cover; background-position:top center */
    const s = Math.max(cr.width / bm.width, cr.height / bm.height);
    const dw = bm.width * s, ox = (cr.width - dw) / 2, oy = 0;
    const name = (cov.querySelector('.nm') || {}).textContent || url;

    for (const el of cov.querySelectorAll('.nm,.tg,.peek')) {
      const tr = el.getBoundingClientRect();
      if (tr.width < 2 || tr.height < 2) continue;
      /* Өөрийн цул дэвсгэртэй элемент доорх зургаас хамаарахгүй —
         тухайн дэвсгэр дээр нь шууд хэмжинэ. */
      const ecs = getComputedStyle(el);
      const ob = (ecs.backgroundColor.match(/[\d.]+/g) || []).map(Number);
      if (ob.length >= 3) {
        const oa = ob[3] === undefined ? 1 : ob[3];
        if (oa >= 0.9) {
          const bl = 0.2126 * lin(ob[0]) + 0.7152 * lin(ob[1]) + 0.0722 * lin(ob[2]);
          const eff = bl * oa + 1 * (1 - oa);          // хамгийн цагаан зураг доор
          const fc = (ecs.color.match(/[\d.]+/g) || []).map(Number);
          const fl = 0.2126 * lin(fc[0]) + 0.7152 * lin(fc[1]) + 0.0722 * lin(fc[2]);
          const rr = (Math.max(fl, eff) + 0.05) / (Math.min(fl, eff) + 0.05);
          const pxo = parseFloat(ecs.fontSize);
          const needo = (pxo >= 24 || (pxo >= 18.66 && +ecs.fontWeight >= 700)) ? 3 : 4.5;
          out.push({ card: (cov.getAttribute('aria-label') || url).trim(), part: el.className,
            px: pxo, ownBg: ecs.backgroundColor, ratio: +rr.toFixed(2), need: needo, ok: rr >= needo });
          continue;
        }
      }
      const c = document.createElement('canvas');
      c.width = Math.ceil(tr.width); c.height = Math.ceil(tr.height);
      const x = c.getContext('2d', { willReadFrequently: true });
      x.drawImage(bm, (tr.left - cr.left - ox) / s, (tr.top - cr.top - oy) / s,
                  tr.width / s, tr.height / s, 0, 0, c.width, c.height);
      const d = x.getImageData(0, 0, c.width, c.height).data;
      const L = [];
      for (let i = 0; i < d.length; i += 4)
        L.push(0.2126 * lin(d[i]) + 0.7152 * lin(d[i + 1]) + 0.0722 * lin(d[i + 2]));
      L.sort((a, b) => a - b);
      const p95 = L[Math.floor(L.length * 0.95)];

      const fy = (tr.top + tr.height / 2 - cr.top) / cr.height;
      const a = alphaAt(fy);
      const ratio = 1.05 / (p95 * (1 - a) + 0.05);   // цагаан бичвэр
      const cs = getComputedStyle(el);
      const px = parseFloat(cs.fontSize);
      const need = (px >= 24 || (px >= 18.66 && +cs.fontWeight >= 700)) ? 3 : 4.5;
      out.push({ card: name.trim(), part: el.className, px,
        p95: +p95.toFixed(3), scrim: +a.toFixed(2),
        ratio: +ratio.toFixed(2), need, ok: ratio >= need });
    }
  }
  const bad = out.filter(o => o.ok === false || o.error);
  return { total: out.length, failing: bad, worst: out.filter(o => o.ratio)
    .sort((x, y) => x.ratio - y.ratio).slice(0, 3) };
})()
