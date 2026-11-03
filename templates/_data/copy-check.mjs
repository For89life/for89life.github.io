/* Бичвэрийг _data/БИЧВЭРИЙН-ЖИШИГ.md-ийн дүрмээр шалгана.
 *
 * Зорилго нь «сайхан санагдаж байна» гэдгийг тоо болгох. Дүрэм бүр
 * тухайн баримт бичгийн хэсэгт заагдсан.
 *
 *     node templates/_data/copy-check.mjs
 *     node templates/_data/copy-check.mjs --only event
 */
import { chromium } from 'playwright';
import { readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = fileURLToPath(new URL('.', import.meta.url));
const TPL = join(HERE, '..');
const ROOT = join(TPL, '..');
const BASE = process.env.GERELT_BASE || 'http://localhost:8741';
const onlyIdx = process.argv.indexOf('--only');
const ONLY = onlyIdx > -1 ? process.argv[onlyIdx + 1] : null;

/* §2 — зөвшөөрөгдсөн товчны нэрс. Загвар бүр өөрийн салбарын
   үйлдэлтэй тул бүрэн хаалттай жагсаалт болгохгүй, харин
   «үзэх/авах/илгээх/захиалах/бүртгүүлэх/холбогдох» язгууртай
   байхыг шаардана. */
const CTA_STEMS = [
  'дэлгэрэнгүй', 'үзэх', 'харах', 'авах', 'илгээх', 'захиалах',
  'бүртгүүлэх', 'холбоо барих', 'холбогдох', 'нээх', 'сонгох',
  'шалгах', 'эхлэх', 'товлох', 'асуух', 'татах', 'хайх',
];

/* §9 — хориотой хэллэгүүд */
const BANNED = [
  { re: /юу хийж өгөх вэ/i, why: '§9 — «Үйлчилгээ» гэж бич' },
  { re: /хэлээд өгөөрэй/i, why: '§9 — «бичиж илгээгээрэй»' },
  { re: /баяртай байх болно|баяртай байна/i, why: '§9 — орчуулгын хэллэг' },
  { re: /хамгийн шилдэг|дээд зэргийн|хамгийн сайн компани/i, why: '§9 — нотолгоогүй хэтрүүлэг' },
  { re: /\bBasic\b|\bPro\b(?!\w)|\bEnterprise\b/, why: '§9 — багцын нэрийг монголоор' },
  { re: /ажиллдаг|үйлчилгээнүүд үзэх/i, why: 'үсгийн/найруулгын алдаа' },
];

/* §6 — хэлбэрийн шалгуур */
const FORMAT = [
  { re: /\d{1,3}(?: \d{3})+\s*₮/, why: '§6 — мянгатыг таслалаар: 120,000₮' },
  { re: /(?<![\d,₮])₮[ 	]*\d{1,3},\d{3}(?!\d)/, why: '§6 — энгийн үнэд тэмдэг ард: 120,000₮' },
  { re: /\b\d{8}\b(?!\s*(м²|он))/, why: '§6 — утсыг 7210-0262 хэлбэрээр' },
];

const WORDS = s => s.trim().split(/\s+/).filter(Boolean).length;

function pages() {
  const out = [];
  if (!ONLY) out.push('index.html');
  for (const dir of readdirSync(TPL)) {
    if (dir.startsWith('_') || dir === 'images') continue;
    const d = join(TPL, dir);
    if (!statSync(d).isDirectory()) continue;
    if (ONLY && dir !== ONLY) continue;
    for (const f of readdirSync(d)) {
      if (f.endsWith('.html')) out.push(relative(ROOT, join(d, f)).replace(/\\/g, '/'));
    }
  }
  return out;
}

async function main() {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: 'mn-MN' });
  const list = pages();
  let total = 0;
  const perRule = {};

  for (const p of list) {
    const page = await ctx.newPage();
    await page.goto(`${BASE}/${p}`, { waitUntil: 'load', timeout: 25000 });
    const found = await page.evaluate(({ CTA_STEMS }) => {
      const hits = [];
      const txt = e => (e.textContent || '').replace(/\s+/g, ' ').trim();

      /* Gerelt-ийн тууз нь загварын хэсэг биш — алгасна */
      const skip = e => e.closest('.gs') || e.closest('#adminBg') || e.closest('#reqModal');

      /* Хуудасны гарчгууд — хэсэг рүү үсрэх товчийг танихад */
      const heads = new Set([...document.querySelectorAll('h1,h2,h3')]
        .map(h => txt(h).toLowerCase()));

      for (const b of document.querySelectorAll('a.btn,button.btn,.act,.peek,.sbtn')) {
        if (skip(b)) continue;
        const href = b.getAttribute('href') || '';
        /* Утас, имэйл нь өөрөө үйлдэл — дугаар нь товчны нэр байж болно */
        if (/^(tel:|mailto:)/.test(href)) continue;
        const t = txt(b).replace(/[→←↑↓✕✓·…]+/g, '').trim();
        if (!t || t.length > 40) continue;
        const low = t.toLowerCase();
        /* Хэсгийн нэрийг давтсан үсрэх товч зүй зөв */
        if (heads.has(low)) continue;
        if (/^[A-Za-z][A-Za-z0-9 .@-]*$/.test(t)) continue;      // Instagram гэх мэт
        if (CTA_STEMS.some(s => low.includes(s))) continue;
        /* Нөхцөл үйл үгээр төгссөн — өгүүлбэр дуусаагүй */
        if (/(аад|ээд|оод|өөд)$/.test(low))
          { hits.push({ rule: 'cta-dangling', text: t }); continue; }
        hits.push({ rule: 'cta', text: t });
      }

      /* §1 — картын тайлбар богино байх */
      for (const d of document.querySelectorAll('.pc p,.sc p,.cc p,.lc p,.dc p,.mc p,.bc p,.tc p,.wc p,.hc p,.ac p')) {
        if (skip(d)) continue;
        const t = txt(d);
        const n = t.split(/\s+/).filter(Boolean).length;
        if (n > 16) hits.push({ rule: 'long-desc', text: `${n} үг · ${t.slice(0, 70)}` });
      }
      return hits;
    }, { CTA_STEMS });

    const body = await page.evaluate(() => document.body.innerText);
    const more = [];
    for (const b of BANNED) if (b.re.test(body)) more.push({ rule: 'banned', text: b.why });
    for (const f of FORMAT) { const m = body.match(f.re); if (m) more.push({ rule: 'format', text: `${f.why} — «${m[0]}»` }); }

    const all = [...found, ...more];
    if (all.length) {
      console.log(`\n${p}  — ${all.length}`);
      for (const h of all.slice(0, 8)) {
        console.log(`  [${h.rule}] ${h.text}`);
        perRule[h.rule] = (perRule[h.rule] || 0) + 1;
      }
      if (all.length > 8) console.log(`  … бас ${all.length - 8}`);
      total += all.length;
    }
    await page.close();
  }

  await browser.close();
  console.log('\n' + '─'.repeat(58));
  console.log(`${list.length} хуудас · ${total} тэмдэглэл`);
  console.log(Object.entries(perRule).map(([k, v]) => `${k}: ${v}`).join(' · ') || 'цэвэр');
}

main();
