/* Бүх хуудсыг axe-core-оор шалгана (Deque-ийн үйлдвэрлэлийн хөдөлгүүр).
 *
 * Яагаад гар бичсэн audit.js-ийг халаагүй вэ: axe нь тунгалаг давхарга,
 * градиент, зураг дээрх бичвэрийг «тодорхойлох боломжгүй» гэж алгасдаг.
 * Манай загваруудын хамгийн эрсдэлтэй хэсэг яг тэр. Иймд хоёулаа:
 *
 *   axe-core   — ARIA, нэршил, гарчгийн бүтэц, landmark, хэлбэр,
 *                цул өнгөний тодрол. 90+ дүрэм, миний мэдэхгүйг нь.
 *   audit.js   — зураг/градиент дээрх бичвэрийг canvas-аар 95-р
 *                хувьсагчаар хэмжих, жинхэнэ дарагдах талбай.
 *
 * Хэрэглээ (dev server 8741 дээр ажиллаж байх ёстой):
 *     node templates/_data/a11y.mjs
 *     node templates/_data/a11y.mjs --only fitness
 */
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import { readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = fileURLToPath(new URL('.', import.meta.url));
const TPL = join(HERE, '..');
const ROOT = join(TPL, '..');
const BASE = process.env.GERELT_BASE || 'http://localhost:8741';

const onlyIdx = process.argv.indexOf('--only');
const ONLY = onlyIdx > -1 ? process.argv[onlyIdx + 1] : null;

/* WCAG 2.1 AA + 2.2 AA-гийн шошгууд. best-practice-ийг оруулахгүй —
   тэдгээр нь стандартын шаардлага биш, дүгнэлтийн асуудал. */
const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];

const VIEWPORTS = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'mobile', width: 375, height: 812 },
];

function pages() {
  const out = [];
  if (!ONLY) out.push('index.html');
  for (const dir of readdirSync(TPL)) {
    if (dir.startsWith('_')) continue;
    const d = join(TPL, dir);
    if (!statSync(d).isDirectory() || dir === 'images') continue;
    if (ONLY && dir !== ONLY) continue;
    for (const f of readdirSync(d)) {
      if (f.endsWith('.html')) out.push(relative(ROOT, join(d, f)).replace(/\\/g, '/'));
    }
  }
  return out;
}

const pad = (s, n) => String(s).padEnd(n);

async function main() {
  const list = pages();
  if (!existsSync(join(ROOT, 'index.html'))) {
    console.error('index.html олдсонгүй — төслийн үндсэн хавтаснаас ажиллуул.');
    process.exit(2);
  }

  const browser = await chromium.launch();
  let total = 0, failedPages = 0;
  const rows = [];

  for (const p of list) {
    const url = `${BASE}/${p}`;
    let pageViolations = 0;
    const detail = [];

    for (const vp of VIEWPORTS) {
      const ctx = await browser.newContext({ viewport: vp, locale: 'mn-MN' });
      const page = await ctx.newPage();
      try {
        const res = await page.goto(url, { waitUntil: 'load', timeout: 25000 });
        await page.evaluate(() => document.fonts.ready);
        if (!res || !res.ok()) {
          detail.push(`  [${vp.name}] ХУУДАС АЧААЛАГДСАНГҮЙ (${res ? res.status() : 'no response'})`);
          pageViolations++;
          await ctx.close();
          continue;
        }
        const r = await new AxeBuilder({ page }).withTags(TAGS).analyze();
        for (const v of r.violations) {
          pageViolations += v.nodes.length;
          detail.push(`  [${vp.name}] ${v.id} (${v.impact}) × ${v.nodes.length}`);
          detail.push(`      ${v.help}`);
          for (const n of v.nodes.slice(0, 3))
            detail.push(`      → ${n.target.join(' ')}`);
          if (v.nodes.length > 3) detail.push(`      → … бас ${v.nodes.length - 3}`);
        }
      } catch (e) {
        detail.push(`  [${vp.name}] АЛДАА: ${e.message.split('\n')[0]}`);
        pageViolations++;
      }
      await ctx.close();
    }

    total += pageViolations;
    if (pageViolations) failedPages++;
    rows.push([p, pageViolations]);
    if (pageViolations) {
      console.log(`\n${p}  — ${pageViolations} зөрчил`);
      detail.forEach(d => console.log(d));
    }
  }

  await browser.close();

  console.log('\n' + '─'.repeat(56));
  for (const [p, n] of rows) console.log(`${n ? 'FAIL' : ' ok '}  ${pad(p, 42)} ${n || ''}`);
  console.log('─'.repeat(56));
  console.log(`${list.length} хуудас · ${failedPages} алдаатай · ${total} зөрчил нийт`);
  process.exit(total ? 1 : 0);
}

main();
