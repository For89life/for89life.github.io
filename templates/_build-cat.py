# -*- coding: utf-8 -*-
"""Категорын хуудсуудыг нэг эх загвараас үүсгэнэ.
Эдгээр нь үйлчлүүлэгчийн загвар биш, Gerelt-ийн өөрийн хуудас тул
нүүр хуудасны брэнд (Golos Text, #0A0A0B, улбар шар) -ыг дагана."""
import io, os

CATS = [
 dict(slug='corporate', name='Байгууллагын танилцуулга',
      lead='Компани, байгууллагаа танилцуулах, үйлчилгээгээ харуулах, холбоо барих урсгалтай сайтууд.',
      items=[
        dict(f='tulga',   n='Тулга',   d='Швейцарь маягийн цэгц. Цайвар дэвсгэр, цэнхэр өргөлт, тоон үзүүлэлт онцолсон.',
             tags='Цэгцтэй · Цэнхэр · Тоо баримт', p='₮300,000', g='linear-gradient(140deg,#0B1B3A,#1D4ED8 60%,#7CA7F5)'),
        dict(f='hurd',    n='Хүрд',    d='Хар дэвсгэр, сериф гарчиг. Нэр хүнд, туршлага онцолсон нягт дүр төрх.',
             tags='Харанхуй · Сериф · Алтлаг', p='₮350,000', g='linear-gradient(140deg,#14110C,#4A3A1C 58%,#C9A227)'),
        dict(f='tsamhag', n='Цамхаг',  d='Хуваасан дэлгэц, зоригтой том үсэг. Хурдан ойлгогдох, цөөн үгтэй.',
             tags='Хуваасан · Зоригтой · Ногоон', p='₮350,000', g='linear-gradient(140deg,#06201C,#0F766E 58%,#5EEAD4)'),
        dict(f='egnee',   n='Эгнээ',   d='Зөөлөн булантай картууд, цайвар өнгө. Жижиг, дунд бизнест ээлтэй.',
             tags='Зөөлөн · Цайвар · Найрсаг', p='₮300,000', g='linear-gradient(140deg,#2A1A3E,#7C5BAF 58%,#C9B6E8)'),
        dict(f='guur',    n='Гүүр',    d='Албан ёсны, тэгш хэмтэй. Хууль, зөвлөх, санхүүгийн үйлчилгээнд.',
             tags='Албан ёсны · Хүрэн шар · Сериф', p='₮350,000', g='linear-gradient(140deg,#0E1B2E,#3A4D6B 58%,#C7B388)'),
      ]),
 dict(slug='shop', name='Онлайн дэлгүүр',
      lead='Бараа, сагс, захиалга, төлбөрийн холболттой худалдааны сайтууд.',
      items=[
        dict(f='zah',     n='Зах',     d='Блок бүтэц, эрч хүчтэй улбар. Олон ангилал, хямдрал онцолсон.',
             tags='Блок · Улбар · Олон бараа', p='₮500,000', g='linear-gradient(140deg,#5A1F0B,#C2410C 58%,#EA8C4E)'),
        dict(f='sav',     n='Сав',     d='Цагаан бутик. Том зураг, задгай зай, цөөн бараа онцолсон.',
             tags='Бутик · Цагаан · Задгай', p='₮500,000', g='linear-gradient(140deg,#242420,#6E6A60 58%,#E8E4DB)'),
        dict(f='tulhuur', n='Түлхүүр', d='Харанхуй, техникийн. Цахилгаан бараа, тодорхойлолт, харьцуулалт.',
             tags='Харанхуй · Техник · Неон', p='₮550,000', g='linear-gradient(140deg,#070B14,#13304F 58%,#22D3EE)'),
        dict(f='horshoo', n='Хоршоо',  d='Органик, дулаан ногоон. Хүнс, гар урлал, жижиг үйлдвэрлэлд.',
             tags='Органик · Ногоон · Дулаан', p='₮500,000', g='linear-gradient(140deg,#1B2A14,#4D7C0F 58%,#BBF7A0)'),
        dict(f='torgon',  n='Торгон',  d='Хувцасны lookbook. Бүтэн дэлгэцийн зураг, өндөр эсрэгцэл, хар цагаан.',
             tags='Хувцас · Эсрэгцэл · Lookbook', p='₮550,000', g='linear-gradient(140deg,#0B0B0B,#3D3D3D 58%,#E6E4E0)'),
      ]),
 dict(slug='restaurant', name='Ресторан & кафе',
      lead='Цэс, ажиллах цаг, байршил, ширээний захиалгатай хоолны газрын сайтууд.',
      items=[
        dict(f='guurs',   n='Гуурс',   d='Дэгжин сериф, цөцгий өнгө. Уламжлалт хоол, тайван уур амьсгал.',
             tags='Дэгжин · Цөцгий · Сериф', p='₮350,000', g='linear-gradient(140deg,#3A2212,#A33B0F 60%,#D98E4A)'),
        dict(f='utaa',    n='Утаа',    d='Харанхуй бистро. Орой, бар, уур амьсгал онцолсон.',
             tags='Харанхуй · Бар · Алтлаг', p='₮380,000', g='linear-gradient(140deg,#0E0C0A,#3B2E1E 58%,#B8903F)'),
        dict(f='navch',   n='Навч',    d='Гэрэлтэй кафе, талх нарийн боов. Агаартай, цайвар, эелдэг.',
             tags='Гэрэлтэй · Кафе · Цайвар', p='₮350,000', g='linear-gradient(140deg,#1C3326,#4F8A5F 58%,#C9E8C4)'),
        dict(f='togoo',   n='Тогоо',   d='Гудамжны хоол. Тод өнгө, том үнэ, хурдан захиалга.',
             tags='Тод · Хурдан · Улаан', p='₮350,000', g='linear-gradient(140deg,#4A0E0E,#C21807 55%,#F5B301)'),
        dict(f='zoolon',  n='Зөөлөн',  d='Бялуу, нарийн боов. Зөөлөн ягаан, бөөрөнхий хэлбэр, захиалгын урсгал.',
             tags='Нарийн боов · Ягаан · Зөөлөн', p='₮350,000', g='linear-gradient(140deg,#5A2338,#B23A62 58%,#FCE4EC)'),
      ]),
 dict(slug='portfolio', name='Хувийн портфолио',
      lead='Ажлын сан, туршлага, холбоо барих — хувь хүн, чөлөөт мэргэжилтэнд.',
      items=[
        dict(f='or',      n='Ор',      d='Бруталист. Том шахсан үсэг, хатуу эсрэгцэл, хүчиллэг өргөлт.',
             tags='Бруталист · Хар · Хүчиллэг', p='₮300,000', g='linear-gradient(140deg,#0D0D0E,#2A2A2E 58%,#D8FF47)'),
        dict(f='huudas',  n='Хуудас',  d='Редакторын. Сериф бичвэр, цаасан цагаан, уншихад тухтай.',
             tags='Редактор · Сериф · Цаасан', p='₮300,000', g='linear-gradient(140deg,#2B2824,#7A7066 58%,#F2EDE4)'),
        dict(f='zurag',   n='Зураг',   d='Гэрэл зурагчдад. Бүтэн дэлгэцийн ажил, хамгийн бага чимэглэл.',
             tags='Зураг · Бүтэн дэлгэц · Харанхуй', p='₮320,000', g='linear-gradient(140deg,#09090B,#27272A 58%,#A1A1AA)'),
        dict(f='suljee',  n='Сүлжээ',  d='Хөгжүүлэгчдэд. Моно фонт, сүлжээн бүтэц, терминал аяс.',
             tags='Хөгжүүлэгч · Моно · Сүлжээ', p='₮320,000', g='linear-gradient(140deg,#031A12,#0B5E42 58%,#34D399)'),
        dict(f='duu',     n='Дуу',     d='Хөгжимчин, продюсерт. Дуу долгионы хэлбэр, бичлэгийн жагсаалт, харанхуй.',
             tags='Хөгжим · Харанхуй · Долгион', p='₮320,000', g='linear-gradient(140deg,#08090C,#1C2027 58%,#4ADE80)'),
      ]),
]

HEAD = u'''<!DOCTYPE html>
<html lang="mn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} — бэлэн загварууд | Gerelt Solutions</title>
<meta name="description" content="{lead}">
<link rel="icon" href="../../images/logo.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{
  --bg:#0A0A0B; --bg2:#101013; --surf:#17171B;
  --fg:#F5F5F3; --mut:#9A9BA1; --mut2:#83848C;
  --line:rgba(245,245,243,.10); --line2:rgba(245,245,243,.18);
  --acc:#FEC43A; --ink:#0A0A0B;
  --ff:'Golos Text',system-ui,-apple-system,sans-serif;
  --pad:clamp(1.25rem,5vw,5rem);
  --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem;
  --r:14px;
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html{{scroll-behavior:smooth;-webkit-text-size-adjust:100%;}}
body{{font-family:var(--ff);background:var(--bg);color:var(--fg);font-size:15px;line-height:1.65;-webkit-font-smoothing:antialiased;}}
a{{color:inherit;text-decoration:none;}}
img{{display:block;max-width:100%;}}
h1,h2,h3{{font-weight:600;letter-spacing:-.025em;line-height:1.08;}}
.wrap{{max-width:1320px;margin:0 auto;padding:0 var(--pad);}}
.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;}}
.skip{{position:absolute;left:var(--pad);top:-100px;z-index:400;background:var(--acc);color:var(--ink);font-weight:600;font-size:13px;padding:.85rem 1.3rem;border-radius:0 0 10px 10px;transition:top .18s;}}
.skip:focus{{top:0;}}
:focus-visible{{outline:2px solid var(--acc);outline-offset:3px;border-radius:3px;}}

.bar{{position:sticky;top:0;z-index:100;display:flex;align-items:center;gap:var(--s3);height:4.5rem;padding:0 var(--pad);background:rgba(10,10,11,.88);backdrop-filter:blur(16px);border-bottom:1px solid var(--line);}}
.brand{{display:flex;align-items:center;gap:.65rem;min-height:44px;white-space:nowrap;}}
.brand img{{height:26px;width:auto;}}
.brand span{{font-size:14px;font-weight:600;letter-spacing:-.01em;}}
.brand span i{{font-style:normal;color:var(--mut);}}
.back{{margin-left:auto;display:inline-flex;align-items:center;gap:.45rem;min-height:44px;padding:0 1rem;border-radius:999px;border:1px solid var(--line2);font-size:13px;font-weight:600;transition:border-color .2s,color .2s;}}
.back:hover{{border-color:var(--fg);}}

.crumb{{display:flex;align-items:center;gap:.55rem;padding-top:var(--s5);font-size:12.5px;color:var(--mut2);}}
.crumb a{{color:var(--mut);display:inline-block;padding:.45rem 0;}}
.crumb a:hover{{color:var(--acc);}}

.top{{padding:var(--s3) 0 var(--s5);border-bottom:1px solid var(--line);}}
.top h1{{font-size:clamp(2rem,4.4vw,3.4rem);margin-top:var(--s3);}}
.top p{{margin-top:var(--s3);font-size:17px;color:var(--mut);max-width:58ch;}}
.count{{display:inline-flex;align-items:center;gap:.5rem;margin-top:var(--s3);font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut2);}}
.count b{{color:var(--acc);font-weight:600;}}

.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:var(--s4);padding:var(--s5) 0 var(--s6);}}
.card{{display:flex;flex-direction:column;}}
.cover{{position:relative;display:flex;flex-direction:column;justify-content:space-between;
  aspect-ratio:16/10;border-radius:var(--r);overflow:hidden;padding:var(--s4);
  border:1px solid var(--line);transition:transform .32s ease,border-color .32s ease;}}
/* Градиентын цайвар үзүүрт цагаан бичвэр 1.2:1 хүртэл унадаг тул
   бичвэр байрлах дээд, доод зурвасыг далдална. Дунд нь өнгөө хадгална. */
.cover::before{{content:'';position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(rgba(0,0,0,.8),rgba(0,0,0,.2) 38%,rgba(0,0,0,.26) 60%,rgba(0,0,0,.84));}}
.cover .nm,.cover .tg{{position:relative;z-index:2;}}
.card:hover .cover{{transform:translateY(-5px);border-color:var(--line2);}}
.cover .nm{{font-size:clamp(1.5rem,3vw,2.3rem);font-weight:600;letter-spacing:-.03em;color:#fff;}}
.cover .tg{{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.88);}}
.cover .peek{{position:absolute;left:0;right:0;bottom:0;padding:.85rem var(--s4);
  background:linear-gradient(transparent,rgba(0,0,0,.75));
  font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:600;color:#fff;
  opacity:0;transform:translateY(8px);transition:opacity .28s,transform .28s;}}
.cover:hover .peek,.cover:focus-visible .peek{{opacity:1;transform:none;}}
.row{{display:flex;align-items:baseline;gap:.8rem;padding-top:var(--s3);}}
.row h2{{flex:1;font-size:18px;font-weight:600;}}
.row .amt{{font-size:15px;font-weight:600;white-space:nowrap;}}
.card p.d{{padding-top:.4rem;font-size:14px;color:var(--mut);max-width:48ch;}}
.act{{position:relative;align-self:flex-start;margin-top:.9rem;font-family:inherit;
  font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:600;
  color:var(--mut);background:none;border:none;padding:0;cursor:pointer;
  border-bottom:1px solid var(--mut2);transition:color .2s,border-color .2s;}}
.act::before{{content:'';position:absolute;left:0;right:0;top:50%;height:44px;transform:translateY(-50%);}}
.act:hover{{color:var(--fg);border-color:var(--fg);}}

.other{{border-top:1px solid var(--line);padding:var(--s5) 0;}}
.other h2{{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut2);font-weight:600;margin-bottom:var(--s3);}}
.olist{{display:flex;flex-wrap:wrap;gap:.6rem;}}
.olist a{{display:inline-flex;align-items:center;min-height:44px;padding:0 1.1rem;border-radius:999px;border:1px solid var(--line2);font-size:14px;font-weight:500;color:var(--mut);transition:border-color .2s,color .2s;}}
.olist a:hover{{border-color:var(--acc);color:var(--acc);}}

.foot{{border-top:1px solid var(--line);padding:var(--s4) 0;display:flex;justify-content:space-between;flex-wrap:wrap;gap:var(--s2);font-size:13px;color:var(--mut2);}}
.foot a{{color:var(--mut);display:inline-block;padding:.4rem 0;}}
.foot a:hover{{color:var(--acc);}}

@media(max-width:820px){{.grid{{grid-template-columns:1fr;}}}}
@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto;}}*{{transition-duration:.01ms!important;}}}}
</style>
</head>
<body>
<a href="#main" class="skip">Шууд агуулга руу</a>

<header class="bar">
  <a href="../../index.html" class="brand">
    <img src="../../images/logo.webp" alt="">
    <span>Gerelt<i> Solutions</i> Studio</span>
  </a>
  <a class="back" href="../../index.html#templates">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>
    Бүх загвар
  </a>
</header>

<main id="main">
<div class="wrap">
  <nav class="crumb" aria-label="Замчлал">
    <a href="../../index.html">Нүүр</a><span aria-hidden="true">/</span>
    <a href="../../index.html#templates">Бэлэн загвар</a><span aria-hidden="true">/</span>
    <span>{name}</span>
  </nav>
</div>

<section class="top">
  <div class="wrap">
    <h1>{name}</h1>
    <p>{lead}</p>
    <p class="count"><b>{n}</b> загвар · бүгд мобайл нийцтэй · агуулгыг тань руу тааруулна</p>
  </div>
</section>

<div class="wrap">
  <div class="grid">
{cards}
  </div>
</div>

<section class="other">
  <div class="wrap">
    <h2>Бусад категор</h2>
    <nav class="olist" aria-label="Бусад категор">
{others}
    </nav>
  </div>
</section>
</main>

<footer class="wrap">
  <div class="foot">
    <span>© 2026 Gerelt Solutions Studio</span>
    <span><a href="../../index.html#contact">Холбоо барих</a> · <a href="../../index.html#templates">Бүх загвар</a></span>
  </div>
</footer>

<script>
// Хүсэлт илгээх товч нүүр хуудасны формыг тэр загварын нэртэйгээр нээнэ
function ask(name){{
  location.href='../../index.html?tpl='+encodeURIComponent(name)+'#templates';
}}
</script>
</body>
</html>
'''

CARD = u'''    <article class="card">
      <a class="cover" href="{f}.html" style="background-image:url('../images/pv-{f}.webp');background-size:cover;background-position:top center">
        <span class="nm">{n}</span>
        <span class="tg">{tags}</span>
        <span class="peek">Загвар нээх →</span>
      </a>
      <div class="row"><h2>{n}</h2><span class="amt">{p}</span></div>
      <p class="d">{d}</p>
      <button class="act" onclick="ask('{cat} — {n}')">Хүсэлт илгээх →</button>
    </article>'''

base = os.path.dirname(os.path.abspath(__file__))
for c in CATS:
    cards = '\n\n'.join(CARD.format(cat=c['name'], **it) for it in c['items'])
    others = '\n'.join(
        '      <a href="../%s/index.html">%s</a>' % (o['slug'], o['name'])
        for o in CATS if o['slug'] != c['slug'])
    html = HEAD.format(name=c['name'], lead=c['lead'], n=len(c['items']),
                       cards=cards, others=others)
    path = os.path.join(base, c['slug'], 'index.html')
    io.open(path, 'w', encoding='utf-8', newline='').write(html)
    print('wrote', c['slug'])
