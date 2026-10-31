/* Загвар бүрийн картын нүүрний зургийг Playwright-аар авна.
 *
 * Өмнө нь хөтчийн самбарын дэлгэцийн зургийг blob файлаас уншиж
 * байсан: самбарын өргөнөөс хамааран 555–800px хооронд хэлбэлзэж,
 * blob-ийн нэрийг гараар бичиж өгөх шаардлагатай байв. Энд бүгд
 * яг 1440px-ээр, давтагдах байдлаар гарна.
 *
 * Gerelt-ийн тууз нь загварын хэсэг биш тул нуусан.
 *
 * Хэрэглээ:
 *     node templates/_data/shots.mjs            # бүгд
 *     node templates/_data/shots.mjs --only fitness
 */
import { chromium } from 'playwright';
import { readdirSync, statSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = fileURLToPath(new URL('.', import.meta.url));
const TPL = join(HERE, '..');
const OUT = join(TPL, 'images', '_shots');
const BASE = process.env.GERELT_BASE || 'http://localhost:8741';

const W = 1440;
const H = Math.round(W / 1.6);          // 16:10 — картын харьцаа

const onlyIdx = process.argv.indexOf('--only');
const ONLY = onlyIdx > -1 ? process.argv[onlyIdx + 1] : null;

function targets() {
  const out = [];
  for (const dir of readdirSync(TPL)) {
    if (dir.startsWith('_') || dir === 'images') continue;
    const d = join(TPL, dir);
    if (!statSync(d).isDirectory()) continue;
    if (ONLY && dir !== ONLY) continue;
    for (const f of readdirSync(d)) {
      if (!f.endsWith('.html') || f === 'index.html') continue;
      out.push({ cat: dir, name: f.replace(/\.html$/, '') });
    }
  }
  return out;
}

async function main() {
  mkdirSync(OUT, { recursive: true });
  const list = targets();
  const browser = await chromium.launch();
  const ctx = await browser.newContext({
    viewport: { width: W, height: H + 200 },
    deviceScaleFactor: 1,
    locale: 'mn-MN',
    reducedMotion: 'reduce',           // илрэх хөдөлгөөн дуусахыг хүлээхгүй
  });

  for (const t of list) {
    const page = await ctx.newPage();
    const url = `${BASE}/templates/${t.cat}/${t.name}.html`;
    /* networkidle нь Google Fonts-ийн холболтыг хүлээж хуудас
       тутамд ~1 минут зарцуулдаг. Бидний хүлээх зүйл бол
       фонт ба зураг — тэднийг шууд хүлээвэл хавьгүй хурдан. */
    await page.goto(url, { waitUntil: 'load', timeout: 25000 });
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => Promise.all(
      [...document.images].filter(i => !i.complete)
        .map(i => new Promise(r => { i.onload = i.onerror = r; }))));
    await page.evaluate(() => {
      const r = document.querySelector('.gs');
      if (r) r.style.display = 'none';            // Gerelt-ийн тууз
      document.documentElement.style.scrollBehavior = 'auto';
      window.scrollTo(0, 0);
      /* Илрэх хөдөлгөөн JS-гүй үед 3 секунд хүлээдэг — шууд нээнэ */
      document.querySelectorAll('.rv').forEach(e => {
        e.style.opacity = '1'; e.style.transform = 'none';
      });
    });
    await page.waitForTimeout(450);
    const dest = join(OUT, `${t.name}.png`);
    await page.screenshot({ path: dest, clip: { x: 0, y: 0, width: W, height: H } });
    console.log(`${t.cat}/${t.name} → images/_shots/${t.name}.png`);
    await page.close();
  }

  await browser.close();
  console.log(`\n${list.length} дэлгэцийн зураг, ${W}×${H}`);
}

main();
