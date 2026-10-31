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
 dict(slug='education', name='Боловсрол',
      lead='Сургууль, цэцэрлэг, сургалтын төв, онлайн курс — элсэлт, хөтөлбөр, төлбөрийн хэсэгтэй.',
      items=[
        dict(f='surah',      n='Сурах',     d='Ерөнхий боловсролын сургууль. Гэрэлтэй, найрсаг, элсэлт онцолсон.',
             tags='Сургууль · Цэнхэр · Найрсаг', p='₮350,000', g='linear-gradient(140deg,#0C2A52,#1D63C9 58%,#9CC4F5)'),
        dict(f='mergejil',   n='Мэргэжил',  d='Мэргэжлийн сургалт. Хатуу бүтэц, дадлага, ажлын байр онцолсон.',
             tags='Мэргэжил · Ногоон · Сериф', p='₮380,000', g='linear-gradient(140deg,#0B1C14,#1F6B45 58%,#9BD9B5)'),
        dict(f='onlain',     n='Онлайн',    d='Цахим сургалтын платформ. Харанхуй, тоглуулагч, явцын мөр, үнийн багц.',
             tags='Платформ · Харанхуй · Нил ягаан', p='₮450,000', g='linear-gradient(140deg,#0B0C14,#2E2F55 58%,#8B8CFB)'),
        dict(f='tsetserleg', n='Цэцэрлэг',  d='Цэцэрлэг, өдөр өнжүүлэх. Дулаан, бөөрөнхий, өдрийн хуваарьтай.',
             tags='Цэцэрлэг · Улбар · Дулаан', p='₮350,000', g='linear-gradient(140deg,#3A2416,#C2561B 58%,#FFD9B3)'),
        dict(f='ihsurguuli', n='Дээд',      d='Их сургууль, коллеж. Албан ёсны, сериф, мэдээ, элсэлтийн хэсэгтэй.',
             tags='Их сургууль · Час улаан · Сериф', p='₮420,000', g='linear-gradient(140deg,#2A1013,#8E1F2B 58%,#D4A843)'),
      ]),
 dict(slug='health', name='Эрүүл мэнд',
      lead='Эмнэлэг, лаборатори, эмийн сан, зөвлөгөөний төв — цаг авах, үнэ, бэлтгэлийн хэсэгтэй.',
      items=[
        dict(f='emneleg', n='Эмнэлэг', d='Поликлиник, эрүүл мэндийн төв. Хурдан цаг авах маягт, эмч нарын хэсэг.',
             tags='Клиник · Номин цэнхэр · Тайван', p='₮420,000', g='linear-gradient(140deg,#0A2B31,#0E6E7D 58%,#A8DCE4)'),
        dict(f='shud', n='Шүд', d='Шүдний эмнэлэг. Бүрэн үнийн жагсаалт, түгээмэл асуулт, ариутгалын тайлбар.',
             tags='Шүд · Ногоон · Цэвэрхэн', p='₮380,000', g='linear-gradient(140deg,#0A2E27,#0F7A68 58%,#A8DFD4)'),
        dict(f='lab', n='Лаборатори', d='Оношилгооны төв. Шинжилгээний хүснэгт, хариу хүлээх хугацаа, бэлтгэл.',
             tags='Лаборатори · Техник · Хүснэгт', p='₮450,000', g='linear-gradient(140deg,#0C1A22,#105C87 58%,#9BC8E0)'),
        dict(f='setgel', n='Сэтгэл', d='Сэтгэл зүйн зөвлөгөө. Дулаан сериф, нууцлалын дэлгэрэнгүй тайлбар.',
             tags='Зөвлөгөө · Дулаан · Сериф', p='₮380,000', g='linear-gradient(140deg,#2C2621,#7A5A3A 58%,#E2D3BF)'),
        dict(f='emsan', n='Эмийн сан', d='Эмийн сан. Бэлэн байдал шалгах хайлт, хүргэлт, жор хүлээн авах.',
             tags='Эмийн сан · Ногоон · Практик', p='₮400,000', g='linear-gradient(140deg,#0E2317,#1B6B3A 58%,#A9D9BC)'),
      ]),
 dict(slug='fitness', name='Фитнес & гоо сайхан',
      lead='Заал, йог студи, салон, спа, үсчин — хуваарь, үнэ, гишүүнчлэл, цаг захиалгын хэсэгтэй.',
      items=[
        dict(f='zaal', n='Заал', d='Фитнес төв. Харанхуй, эрч хүчтэй. Хуваарийн хүснэгт, гишүүнчлэлийн багц.',
             tags='Фитнес · Харанхуй · Шохойн ногоон', p='₮420,000', g='linear-gradient(140deg,#0A0B0D,#2A3318 58%,#C6F24E)'),
        dict(f='yog', n='Йог', d='Йог, пилатес студи. Агаартай, амгалан. Анхан шатныханд зориулсан зөвлөмж.',
             tags='Йог · Цайвар · Сериф', p='₮350,000', g='linear-gradient(140deg,#262821,#4F6148 58%,#D8DFD2)'),
        dict(f='goo', n='Гоо сайхан', d='Салон. Дэгжин, цэгэн тасархайтай бүрэн үнийн жагсаалт.',
             tags='Салон · Ягаан · Дэгжин', p='₮380,000', g='linear-gradient(140deg,#2B1E1C,#9E4257 58%,#F2D4DB)'),
        dict(f='spa', n='Спа', d='Массажны төв. Дулаан харанхуй, алтлаг. Багц, чимээгүй байдлын журам.',
             tags='Спа · Харанхуй · Алтлаг', p='₮400,000', g='linear-gradient(140deg,#17130F,#5C4526 58%,#C79A5B)'),
        dict(f='barber', n='Үсчин', d='Эрэгтэй үсчин. Хуваасан дэлгэцтэй нүүр, үнийн самбар, гурван дүрэм.',
             tags='Үсчин · Хүрэн · Хуваасан', p='₮350,000', g='linear-gradient(140deg,#13100D,#5A4322 58%,#D0954A)'),
      ]),
 dict(slug='travel', name='Аялал & зочид буудал',
      lead='Жуулчны бааз, зочид буудал, аялал зохион байгуулагч, амралтын газар — захиалга, багц, улирал.',
      items=[
        dict(f='ger', n='Гэр бааз', d='Жуулчны бааз. Байгалийн өнгө, улирлын хүснэгт, ирэхээс өмнө мэдэх зүйлс.',
             tags='Бааз · Хүрэн шар · Сериф', p='₮400,000', g='linear-gradient(140deg,#2A2419,#6B5A2A 58%,#E0D3AC)'),
        dict(f='buudal', n='Зочид буудал', d='Хотын буудал. Огноо сонгох мөр, өрөөний зэрэглэл, шууд захиалгын хөнгөлөлт.',
             tags='Буудал · Ногоон · Дэгжин', p='₮480,000', g='linear-gradient(140deg,#1F1D1A,#1C4C4A 58%,#B9D6D3)'),
        dict(f='ayalal', n='Аялал', d='Аялал зохион байгуулагч. Өдөр тутмын хөтөлбөр, үнийн задаргаа.',
             tags='Аялал · Ногоон · Хөтөлбөр', p='₮450,000', g='linear-gradient(140deg,#141A16,#2F6B3F 58%,#A9D3B6)'),
        dict(f='amralt', n='Амралт', d='Нуурын амралтын газар. Агаартай, байшингийн төрөл, үйл ажиллагаа.',
             tags='Амралт · Номин · Агаартай', p='₮420,000', g='linear-gradient(140deg,#0F2A2D,#15666E 58%,#B5DEE1)'),
        dict(f='agent', n='Агентлаг', d='Аялалын агентлаг. Чиглэл хайх мөр, визийн үйлчилгээ, байнгын асуулт.',
             tags='Агентлаг · Хөх · Практик', p='₮420,000', g='linear-gradient(140deg,#15192B,#2B4BA8 58%,#B7C6EC)'),
      ]),
 dict(slug='realestate', name='Үл хөдлөх & барилга',
      lead='Зуучлал, барилгын компани, дотоод засал, түрээс, газар — зар, төсөл, эрх зүйн тайлбар.',
      items=[
        dict(f='oron', n='Орон сууц', d='Үл хөдлөхийн зуучлал. Шүүлтүүр, зарын жагсаалт, ипотекийн тооцоолуур.',
             tags='Зуучлал · Хөх · Жагсаалт', p='₮480,000', g='linear-gradient(140deg,#16191C,#1B4FA0 58%,#B5C8EA)'),
        dict(f='barilga', n='Барилга', d='Барилгын компани. Харанхуй, нарийсгасан үсэг, төсөл, аюулгүй байдал.',
             tags='Барилга · Харанхуй · Шар', p='₮500,000', g='linear-gradient(140deg,#0F1113,#5E4409 58%,#E8A317)'),
        dict(f='inter', n='Интерьер', d='Дотоод засалын студи. Нам гүм, өргөн зураг, үнийн хоёр зарчим.',
             tags='Интерьер · Саарал · Сериф', p='₮450,000', g='linear-gradient(140deg,#1E1C19,#5C4A36 58%,#DED5C7)'),
        dict(f='turees', n='Түрээс', d='Түрээсийн зуучлал. Зар, нөхцөл, түрээслэгчийн эрх, залилангийн анхааруулга.',
             tags='Түрээс · Ногоон · Ойлгомжтой', p='₮400,000', g='linear-gradient(140deg,#191B18,#3E6B2E 58%,#BEDAB2)'),
        dict(f='gazar', n='Газар', d='Газрын зуучлал. Талбайн хүснэгт, өмчлөх/эзэмших ялгаа, шалгах жагсаалт.',
             tags='Газар · Хөх ногоон · Хүснэгт', p='₮420,000', g='linear-gradient(140deg,#1B2017,#5C6B2A 58%,#CBD5A8)'),
      ]),
 dict(slug='event', name='Арга хэмжээ & хурим',
      lead='Хуримын төлөвлөлт, корпорейт эвент, танхим, цэцэг, баярын зохион байгуулалт.',
      items=[
        dict(f='hurim', n='Хурим', d='Хуримын төлөвлөлт. Дэгжин сериф, гурван багц, нэг жилийн цагийн хуваарь.',
             tags='Хурим · Зэс · Дэгжин', p='₮450,000', g='linear-gradient(140deg,#2A221E,#8A5A4A 58%,#EBD6CD)'),
        dict(f='arga', n='Арга хэмжээ', d='Байгууллагын эвент. Харанхуй, тохиолдлын жагсаалт, хариуцлагын блок.',
             tags='Эвент · Харанхуй · Ягаан хөх', p='₮500,000', g='linear-gradient(140deg,#0B0C10,#2E3470 58%,#6E7BFF)'),
        dict(f='tanhim', n='Танхим', d='Танхим түрээс. Багтаамжийн хүснэгт, чөлөөт огноо, тодорхой үнэ.',
             tags='Танхим · Хүрэн · Хүснэгт', p='₮400,000', g='linear-gradient(140deg,#201D17,#6B4E2A 58%,#DCCBAE)'),
        dict(f='tsetseg', n='Цэцэг', d='Цэцгийн дэлгүүр. Зөөлөн ягаан, баглаа, арга хэмжээний чимэглэл, хүргэлт.',
             tags='Цэцэг · Ягаан · Зөөлөн', p='₮380,000', g='linear-gradient(140deg,#2A2124,#9C3D5C 58%,#F0D2DC)'),
        dict(f='bayar', n='Баяр', d='Төрсөн өдөр, ёслол. Тод, бөөрөнхий, багц, дөрвөн алхамт үйл явц.',
             tags='Баяр · Улбар · Тод', p='₮380,000', g='linear-gradient(140deg,#2B2118,#B5531A 58%,#FFD9B8)'),
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
/* Нүүр дээр бичвэр тавихаа больсон. Шалтгаан: нүүр нь загварын
   жинхэнэ дэлгэцийн зураг бөгөөд ихэнх нь цайвар сайт. Хэмжихэд
   цагаан гарчиг 25 картын 12 дээр 2.0:1 хүртэл унаж байв. Далд
   давхаргыг хүчтэй болговол дэлгэцийн зураг нь харагдахаа болино —
   тэгвэл нүүрний утга алга. Нэр, шошго нь доорх цул хэсэгт аль
   хэдийн бичигддэг тул давхардлыг нь авлаа. */
.cover{{position:relative;display:block;
  aspect-ratio:16/10;border-radius:var(--r);overflow:hidden;
  border:1px solid var(--line);transition:transform .32s ease,border-color .32s ease;}}
.card:hover .cover{{transform:translateY(-5px);border-color:var(--line2);}}
/* «Загвар нээх» нь өөрийн цул дэвсгэртэй тул доорх зургаас үл хамаарч
   уншигдана — 14.7:1. */
.cover .peek{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) scale(.94);
  display:inline-flex;align-items:center;min-height:38px;padding:0 1.1rem;border-radius:999px;
  background:rgba(10,10,11,.93);
  font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;font-weight:600;color:#fff;
  white-space:nowrap;opacity:0;transition:opacity .26s,transform .26s;}}
.cover:hover .peek,.cover:focus-visible .peek{{opacity:1;transform:translate(-50%,-50%) scale(1);}}
@media(hover:none){{.cover .peek{{opacity:1;transform:translate(-50%,-50%) scale(1);}}}}
.row{{display:flex;align-items:baseline;gap:.8rem;padding-top:var(--s3);}}
.card .tg{{margin-top:.35rem;font-size:11.5px;letter-spacing:.11em;text-transform:uppercase;
  color:var(--mut2);font-weight:500;}}
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
      <a class="cover" href="{f}.html" aria-label="{n} загварыг нээх"
         style="background-image:url('../images/pv-{f}.webp');background-size:cover;background-position:top center">
        <span class="peek" aria-hidden="true">Загвар нээх →</span>
      </a>
      <div class="row"><h2>{n}</h2><span class="amt">{p}</span></div>
      <p class="tg">{tags}</p>
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
