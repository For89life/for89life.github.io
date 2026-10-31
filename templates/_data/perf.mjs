/* Lighthouse-аар гүйцэтгэл, SEO, шилдэг туршлагын оноо гаргана.
 *
 * Яагаад: вэбдээ «хурдан» гэж бичихийн оронд жинхэнэ тоо тавих.
 * Мөн 50 загварын аль нь хүндэрч байгааг олох.
 *
 *     node templates/_data/perf.mjs            # түүвэр (нүүр + 10)
 *     node templates/_data/perf.mjs --all      # бүгд
 */
import { chromium } from 'playwright';
import lighthouse from 'lighthouse';
import { readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = fileURLToPath(new URL('.', import.meta.url));
const TPL = join(HERE, '..');
const BASE = process.env.GERELT_BASE || 'http://localhost:8741';
const ALL = process.argv.includes('--all');

function targets() {
  const out = ['index.html'];
  for (const dir of readdirSync(TPL)) {
    if (dir.startsWith('_') || dir === 'images') continue;
    if (!statSync(join(TPL, dir)).isDirectory()) continue;
    const files = readdirSync(join(TPL, dir)).filter(f => f.endsWith('.html'));
    /* Түүвэр горимд категор бүрээс нэгийг — 50 хуудас Lighthouse-оор
       үзэхэд 20+ минут болдог. */
    const pick = ALL ? files : files.filter(f => f !== 'index.html').slice(0, 1);
    for (const f of pick) out.push(`templates/${dir}/${f}`);
  }
  return out;
}

const pad = (s, n) => String(s).padEnd(n);
const col = v => (v >= 90 ? ' ok ' : v >= 50 ? 'warn' : 'FAIL');

async function main() {
  const browser = await chromium.launch({ args: ['--remote-debugging-port=9222'] });
  const list = targets();
  const rows = [];

  for (const p of list) {
    let r;
    try {
      r = await lighthouse(`${BASE}/${p}`, {
        port: 9222,
        output: 'json',
        logLevel: 'error',
        /* Утасны хувилбараар — Монголд хандалтын дийлэнх нь гар утас */
        formFactor: 'mobile',
        screenEmulation: { mobile: true, width: 412, height: 823, deviceScaleFactor: 1.75 },
        onlyCategories: ['performance', 'seo', 'best-practices', 'accessibility'],
      });
    } catch (e) {
      rows.push([p, '—', '—', '—', '—', e.message.split('\n')[0].slice(0, 40)]);
      continue;
    }
    const c = r.lhr.categories;
    const a = r.lhr.audits;
    rows.push([
      p,
      Math.round(c.performance.score * 100),
      Math.round(c.accessibility.score * 100),
      Math.round(c['best-practices'].score * 100),
      Math.round(c.seo.score * 100),
      `LCP ${a['largest-contentful-paint'].displayValue || '—'} · CLS ${a['cumulative-layout-shift'].displayValue || '—'}`,
    ]);
    const last = rows[rows.length - 1];
    console.log(`${col(last[1])} ${pad(p, 38)} perf ${pad(last[1], 4)} a11y ${pad(last[2], 4)} bp ${pad(last[3], 4)} seo ${pad(last[4], 4)} ${last[5]}`);
  }

  await browser.close();

  const nums = rows.filter(r => typeof r[1] === 'number');
  const avg = i => Math.round(nums.reduce((s, r) => s + r[i], 0) / nums.length);
  console.log('\n' + '─'.repeat(70));
  console.log(`${nums.length} хуудас (гар утас) · дундаж: perf ${avg(1)} · a11y ${avg(2)} · best-practices ${avg(3)} · seo ${avg(4)}`);
  const worst = [...nums].sort((a, b) => a[1] - b[1]).slice(0, 3);
  console.log('хамгийн удаан:', worst.map(r => `${r[0]} (${r[1]})`).join(', '));
}

main();
