# -*- coding: utf-8 -*-
"""Renders long-form articles and the blog index from article records.

Every article gets the same furniture without the writer having to remember it:
breadcrumbs, an inline CTA roughly a third of the way down, a closing CTA, an
FAQ block that doubles as FAQPage schema and links to sibling articles. The
CTA is part of the template, so no article can ship without a way to enrol.
"""

import sponsors
import article_art
import json
import pathlib

THUMB_DIR = pathlib.Path(__file__).parent / "assets/og/thumb"


def thumb(slug, alt):
    """Card image: the article's own share card, scaled down. Empty if not made yet."""
    if not (THUMB_DIR / f"{slug}.jpg").exists():
        return ""
    return (f'<img class="thumb" src="assets/og/thumb/{slug}.jpg" srcset="{SRCSET.format(slug=slug)}" '
            f'sizes="{SIZES}" alt="{alt}" width="600" height="315" loading="lazy" decoding="async" />')


# Sharp on high-density phones: they pick the full share card, desktops the 600px copy.
SRCSET = "assets/og/thumb/{slug}.jpg 600w, assets/og/{slug}.jpg 1200w"
SIZES = "(max-width: 680px) 92vw, 360px"


BREADCRUMB = ('<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>'
              ' / <a href="blog.html">Blog</a> / <span>{title}</span></nav>')


def _cta(cta, variant="inline"):
    """Conversion block. `variant` inline sits mid-article, band closes it."""
    cls = "cta-inline" if variant == "inline" else "cta-band"
    return f"""
<aside class="{cls}">
  <div>
    <h3>{cta['title']}</h3>
    <p>{cta['body']}</p>
  </div>
  <a class="btn btn-amber" href="{cta['href']}" data-cta="article-{variant}">{cta['label']}</a>
</aside>"""


def _also(also):
    """Quiet second route for a reader who wants the course, not the team programme."""
    if not also:
        return ""
    href, name = also
    return (f'\n<p class="cta-also">Learning for yourself? '
            f'<a href="{href}" data-cta="article-also">See {name}</a></p>')


def _ext(href):
    return ' target="_blank" rel="noopener"' if href.startswith("http") else ""


def _byline(people):
    """Who the story is about and who wrote it, each with a photo when we have one.
    A person listed twice (a writer who is also the point of contact) gets one card."""
    merged = {}
    for label, p in people:
        if not p:
            continue
        if p["name"] in merged:
            first, _ = merged[p["name"]]
            merged[p["name"]] = (f"{first} and {label[0].lower()}{label[1:]}", p)
        else:
            merged[p["name"]] = (label, p)
    def card(label, p):
        img = f'<img src="{p["photo"]}" alt="{p["name"]}" width="64" height="64" loading="eager">' if p.get("photo") else ""
        body = f'{img}<div><span>{label}</span><strong>{p["name"]}</strong><span>{p.get("role", "")}</span></div>'
        if not p.get("href"):
            return f'<div class="byline">{body}</div>'
        cta = "article-contact-whatsapp" if label.endswith("oint of contact") else "article-byline"
        return f'<a class="byline" href="{p["href"]}"{_ext(p["href"])} data-cta="{cta}">{body}</a>'
    cards = "".join(card(label, p) for label, p in merged.values())
    return f'<div class="bylines">{cards}</div>' if cards else ""


def _by_names(article):
    people = [article.get("author") or article.get("expert"), article.get("co_expert")]
    names = [p["name"] for p in people if p] or ["Craft Beer School"]
    return " and ".join(names)


def _contact(article):
    """Chatty as point of contact, opening WhatsApp about this guide."""
    c = article.get("contact")
    if not c or article.get("author"):
        return None
    import mentors
    from urllib.parse import quote
    text = f"Hi Chatty, I read '{article['h1']}' on Craft Beer School and have a question."
    return {**c, "role": "Questions about this guide? WhatsApp her", "href": f"https://wa.me/{mentors.WHATSAPP_NUMBER}?text={quote(text)}"}


def _faqs(faqs):
    if not faqs:
        return ""
    items = "".join(
        f'<details class="reveal"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in faqs)
    return f"""
<section class="faq-block">
  <h2 id="faq">Common questions</h2>
  {items}
</section>"""


def _related(article, by_slug):
    links = [by_slug[s] for s in article.get("related", []) if s in by_slug]
    if not links:
        return ""
    cards = "".join(f"""
      <article class="card reveal">{thumb(a['slug'], a['h1'])}<div class="card-body">
        <span class="cat">{a['cat']}</span>
        <h3>{a['h1']}</h3>
        <p>{a['teaser']}</p>
        <div class="foot"><a href="{a['slug']}.html" class="link-arrow" data-cta="related-article">Read</a></div>
      </div></article>""" for a in links)
    return f"""
<section class="tint related">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Keep reading</span><h2>Related guides</h2></div>
    <div class="grid-3">{cards}</div>
  </div>
</section>"""


def _wheel(a):
    """Weyermann's own Malt Aroma Wheel for the malt, credited to them."""
    return (f'<figure class="malt-wheel"><img src="{a["wheel"]}" alt="Weyermann Malt Aroma Wheel for {a["malt"]}, '
            f'showing the aroma attributes found in its wort" width="900" height="900" loading="lazy">'
            f'<figcaption>Malt Aroma Wheel (wort) for {a["malt"]}. Image: '
            f'<a href="https://www.weyermann.de/en-gb/" rel="noopener">Weyermann Specialty Malts</a>, from their published '
            f'product documents. Craft Beer School is not affiliated with Weyermann.</figcaption></figure>')


def _banner(article):
    """A photo banner when the plan row names one, otherwise the drawn topic banner."""
    b = article.get("banner")
    if not b:
        return article_art.banner_svg(article['slug'], article['cat'])
    return (f'<img src="{b["src"]}" alt="{b["alt"]}" width="1200" height="500" loading="eager" fetchpriority="high" '
            f'style="object-position:50% {b.get("focus", 50)}%">')


def _photo(ph):
    """A credited photo from the plan row, shown after section ph["after"]."""
    return (f'<figure class="malt-wheel post-photo" style="max-width:{min(ph["w"], 640 if ph["w"] >= ph["h"] else 460)}px"><img src="{ph["src"]}" alt="{ph["alt"]}" width="{ph["w"]}" '
            f'height="{ph["h"]}" loading="lazy"><figcaption>{ph["caption"]}</figcaption></figure>')


def render(article, by_slug):
    """Full page body for one article."""
    secs = article["sections"]
    # Drop the inline CTA after the first third, where a reader is engaged but
    # has not yet finished. Never after the last section, that is the band's job.
    cut = max(1, min(len(secs) - 1, round(len(secs) / 3)))

    parts = []
    for i, (heading, body) in enumerate(secs):
        anchor = heading.lower().replace(" ", "-").replace(",", "").replace("?", "")
        parts.append(f'<h2 id="{anchor}">{heading}</h2>\n{body}')
        if i == 0 and article.get("wheel"):
            parts.append(_wheel(article))
        parts += [_photo(ph) for ph in article.get("photos", []) if ph["after"] == i]
        # Guest stories run uninterrupted; only the closing band sells.
        if i + 1 == cut and not article.get("author"):
            # Optional cta_inline lets a guide sell a different route mid-article (e.g. consultancy).
            parts.append(_cta(article.get("cta_inline", article["cta"]), "inline"))
    article_body = "\n".join(parts)

    toc = "".join(
        f'<li><a href="#{h.lower().replace(" ", "-").replace(",", "").replace("?", "")}">{h}</a></li>'
        for h, _ in secs)

    return f"""
<article class="post">
  <div class="wrap post-head">
    {BREADCRUMB.format(title=article['h1'])}
    <figure class="post-banner">{_banner(article)}</figure>
    <span class="eyebrow">{article['cat']}</span>
    <h1 class="post-title">{article['h1']}</h1>
    <p class="lead">{article['standfirst']}</p>
    <p class="post-meta">
      <span>{article['read']} read</span> ·
      <span>Updated <time datetime="{article['updated']}">{article['updated_label']}</time></span> ·
      <span>By {_by_names(article)}</span>
    </p>{_byline([('The story of', article.get('subject')), ('Written by', article.get('author') or article.get('expert')),
                  ('Written by', article.get('co_expert')), ('Point of contact', _contact(article))])}
  </div>

  <div class="wrap post-body">
    <nav class="toc" aria-label="On this page">
      <h2>On this page</h2>
      <ol>{toc}</ol>
    </nav>

    {article_body}

    {_faqs(article.get('faqs'))}

    {sponsors.card(article)}

    {_cta(article['cta'], 'band')}{_also(article.get('also'))}
  </div>
</article>

{_related(article, by_slug)}
"""


def _card(a):
    return f"""
      <article class="card reveal">{thumb(a['slug'], a['h1'])}
        <div class="card-body">
          <span class="cat">{a['cat']}</span>
          <h3>{a['h1']}</h3>
          <p>{a['teaser']}</p>
          <div class="foot">
            <a href="{a['slug']}.html" class="link-arrow" data-cta="blog-card">Read</a>
            <span class="read">{a['read']}</span>
          </div>
        </div>
      </article>"""


PER_PAGE = 10  # rows per results page, as on the Brewers Association hub


def _finder(articles, segment_of):
    """Brewers Association style finder: category, keywords, a count and a pager.
    State lives in the URL (?cat=&q=&page=) so a filtered list can be shared."""
    cats = sorted({a["cat"] for a in articles})
    opts = "".join(f'<option value="{c}">{c}</option>' for c in cats)
    rows = [{"s": a["slug"], "t": a["h1"], "c": a["cat"], "d": a["teaser"], "r": a["read"],
             "u": a["updated"], "g": segment_of.get(a["slug"], ""),
             "b": _by_names(a) if (a.get("author") or a.get("expert")) else "",
             "i": (THUMB_DIR / f"{a['slug']}.jpg").exists()} for a in articles]
    data = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    recs = json.dumps(_recommendations(articles), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f"""
<section class="finder-wrap" aria-labelledby="finder-h">
  <div class="wrap">
    <h2 id="finder-h" class="sr-only">Find a guide</h2>
    <form class="finder" id="finder" role="search" action="blog.html">
      <label class="sr-only" for="f-cat">Category</label>
      <select id="f-cat" name="cat"><option value="">Choose category</option>{opts}</select>
      <label class="sr-only" for="f-q">Search the guides</label>
      <input id="f-q" name="q" type="search" placeholder="Search {len(articles)} guides" autocomplete="off" />
      <button type="submit" class="btn btn-navy">Search</button>
    </form>
    <p class="finder-all"><a href="blog.html?cat=all" id="f-all">Browse all {len(articles)} guides, newest first</a></p>
    <div id="f-results" hidden>
      <aside class="cta-inline f-rec" id="f-rec" hidden><div><span class="eyebrow">Recommended for this search</span><h3></h3><p></p></div><a class="btn btn-amber" data-cta="blog-finder-rec"></a></aside>
      <div class="f-bar"><p class="f-count" id="f-count" aria-live="polite"></p><nav class="f-pager" aria-label="Results pages"></nav></div>
      <ol class="f-list" id="f-list"></ol>
      <div class="f-bar"><a href="blog.html" class="f-clear">Clear filters</a><nav class="f-pager" aria-label="Results pages"></nav></div>
    </div>
  </div>
</section>
<script id="f-data" type="application/json">{data}</script>
<script id="f-recs" type="application/json">{recs}</script>
<script>{FINDER_JS.replace("PER_PAGE", str(PER_PAGE))}</script>"""


def _recommendations(articles):
    """What the finder recommends: an offer when the search words match one, else
    the course most guides in the chosen category already sell."""
    import collections
    import pages_a
    import promos

    def course_card(href):
        for c in pages_a.COURSE_DATA:
            if pages_a.course_href(c["name"]) == href:
                name = c["name"].replace("&amp;", "&")
                return dict(t=name, d=f'{c["dur"]}, live online, {c["price"]}. {c["blurb"]}', h=href, l=f"See {name}")
        if "Corporate" in href:
            return dict(t="Training for your team", d="Beverage training for drinks companies and GCC teams, on site or live online.", h=href, l="Ask about team training")
        if "consultancy" in href:
            return dict(t="Talk to a consultant brewer", d="Our consultant brewers work with breweries and brewpubs on site or remotely.", h=href, l="Book a consultation")
        return None

    by_cat = collections.defaultdict(collections.Counter)
    for a in articles:
        by_cat[a["cat"]][a["cta"]["href"]] += 1
    cats = {c: course_card(n.most_common(1)[0][0]) for c, n in by_cat.items()}
    offers = [dict(w=o["words"], t=o["title"], d=o["body"], h=o["href"], l=o["label"]) for o in promos.OFFERS]
    return dict(cats={c: v for c, v in cats.items() if v}, offers=offers)


FINDER_JS = """(()=>{
const D=JSON.parse(document.getElementById('f-data').textContent),P=PER_PAGE;
const f=document.getElementById('finder'),cat=f.cat,q=f.q,box=document.getElementById('f-results'),
  list=document.getElementById('f-list'),count=document.getElementById('f-count');
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
function render(){
  const u=new URLSearchParams(location.search),c=u.get('cat')||'',w=(u.get('q')||'').trim().toLowerCase();
  cat.value=c==='all'?'':c;q.value=u.get('q')||'';
  const on=!!(c||w),doors=document.getElementById('doors');box.hidden=!on;if(doors)doors.hidden=on;if(!on)return;
  const terms=w.split(/\\s+/).filter(Boolean);
  const hits=D.filter(a=>(!c||c==='all'||a.c===c)&&terms.every(t=>(a.t+' '+a.d+' '+a.c+' '+a.g+' '+a.b).toLowerCase().includes(t)));
  const pages=Math.max(1,Math.ceil(hits.length/P)),pg=Math.min(pages,Math.max(1,+u.get('page')||1)),from=(pg-1)*P;
  count.textContent=hits.length?`Displaying results ${from+1}-${Math.min(from+P,hits.length)} of ${hits.length}`:'No guides match. Try a broader word or another category.';
  const R=JSON.parse(document.getElementById('f-recs').textContent),box2=document.getElementById('f-rec');
  const rec=R.offers.find(o=>o.w.some(x=>w.includes(x)))||R.cats[c]||R.offers[1];
  box2.hidden=!rec;if(rec){box2.querySelector('h3').textContent=rec.t;box2.querySelector('p').textContent=rec.d;const b=box2.querySelector('a');b.textContent=rec.l;b.href=rec.h}
  list.replaceChildren(...hits.slice(from,from+P).map(a=>{
    const li=el('li','f-row'),txt=el('div','f-txt'),h=el('h3'),l=el('a',null,a.t);l.href=a.s+'.html';h.append(l);
    const meta=el('p','f-meta');meta.append(el('span','f-cat',a.c),el('span',null,a.r+(a.b?' · By '+a.b:'')));
    const d=el('p','f-desc',a.d+' '),m=el('a','link-arrow','Read more');m.href=a.s+'.html';m.tabIndex=-1;d.append(m);
    txt.append(h,meta,d);li.append(txt);
    if(a.i){const im=el('img','f-img');im.src='assets/og/thumb/'+a.s+'.jpg';im.alt='';im.width=600;im.height=315;im.loading='lazy';li.append(im)}
    return li}));
  document.querySelectorAll('.f-pager').forEach(n=>{n.replaceChildren();if(pages<2)return;
    const go=(p,t,cur)=>{const x=new URLSearchParams(u);x.set('page',p);const a=el('a',cur?'cur':null,t);a.href='?'+x;if(cur)a.setAttribute('aria-current','page');n.append(a)};
    if(pg>1)go(pg-1,'Prev');
    [...new Set([1,pg-1,pg,pg+1,pages])].filter(p=>p>=1&&p<=pages).sort((a,b)=>a-b).forEach((p,i,arr)=>{if(i&&p-arr[i-1]>1)n.append(el('span',null,'...'));go(p,p,p===pg)});
    if(pg<pages)go(pg+1,'Next')});
}
function nav(params){history.pushState(null,'','blog.html'+(params.toString()?'?'+params:''));render();box.scrollIntoView({block:'start'})}
f.addEventListener('submit',e=>{e.preventDefault();const x=new URLSearchParams();if(cat.value)x.set('cat',cat.value);if(q.value.trim())x.set('q',q.value.trim());if(!x.toString())x.set('cat','all');nav(x)});
cat.addEventListener('change',()=>f.requestSubmit());
document.addEventListener('click',e=>{const a=e.target.closest('.f-pager a,#f-all,.f-clear');if(!a)return;e.preventDefault();nav(new URL(a.href).searchParams)});
addEventListener('popstate',render);document.readyState==='loading'?document.addEventListener('DOMContentLoaded',render):render();
})();"""


SHOWN = 12  # per shelf before the rest fold away


def _seg_id(name):
    return name.lower().replace(" ", "-")


SEG_ICON = {"Beer lovers": "beer", "Homebrewers": "flask", "Professional brewers": "award", "Founders": "briefcase",
            "Brand builders": "megaphone", "Career changers": "cap", "Drinks producers": "wine",
            "Corporate teams": "users"}


TABS_JS = """(()=>{const nav=document.getElementById('topic-tabs');if(!nav)return;
const tabs=[...nav.querySelectorAll('a.topic')],panels=tabs.map(t=>document.getElementById(t.hash.slice(1)));
const show=(id,move)=>{const i=Math.max(0,panels.findIndex(p=>p&&p.id===id));
tabs.forEach((t,j)=>{t.classList.toggle('on',j===i);t.setAttribute('aria-selected',j===i);});
panels.forEach((p,j)=>{if(p)p.hidden=j!==i;});
if(move)nav.scrollIntoView({block:'start',behavior:'smooth'});};
tabs.forEach(t=>t.addEventListener('click',e=>{e.preventDefault();history.replaceState(null,'',t.hash);show(t.hash.slice(1),false);}));
addEventListener('hashchange',()=>show(location.hash.slice(1),true));
show(location.hash.slice(1),!!location.hash);})();"""


def _panel(pid, head, who, cards, more, cta):
    return f"""
<section id="{pid}" class="seg" role="tabpanel">
  <div class="wrap">
    <h2 class="rail-head"><b>{head}</b> <span>{who}</span></h2>
    <div class="rail">
      <button type="button" class="rail-btn prev" aria-label="Previous guides" disabled>[[arrow-left]]</button>
      <div class="rail-track">{cards}</div>
      <button type="button" class="rail-btn next" aria-label="More guides">[[arrow-right]]</button>
    </div>
    {more}
    {cta}
  </div>
</section>"""


def blog_index(articles, banner, segment_of, segments):
    """The blog laid out for the reader: title and search first, then one tab per
    reader group (Latest opens by default), so a visitor sees one shelf at a time
    instead of scrolling past eight. Without JavaScript every shelf shows."""
    tab = lambda pid, label, icon: (f'<a href="#{pid}" class="topic" role="tab" data-cta="blog-segment">'
                                    f'<span class="topic-ico">[[{icon}]]</span>{label}</a>')
    jump = tab("latest", "Latest", "book-open") + "".join(
        tab(_seg_id(name), name, SEG_ICON.get(name, "book-open")) for name, *_ in segments)
    newest = sorted(articles, key=lambda a: a["updated"], reverse=True)[:SHOWN]
    blocks = [_panel("latest", "Latest.", "The newest guides from the brewhouse floor.",
                     "".join(_card(a) for a in newest), "",
                     '<p class="finder-all" style="margin-top:1rem"><a href="blog.html?cat=all">Browse every guide, newest first</a></p>')]
    for name, who, course_href, course_name in segments:
        mine = [a for a in articles if segment_of.get(a["slug"]) == name]
        if not mine:
            continue
        head, rest = mine[:SHOWN], mine[SHOWN:]
        more = (f'<details class="more"><summary>Show all {len(mine)} {name.lower()} guides</summary>'
                f'<div class="grid-3">{"".join(_card(a) for a in rest)}</div></details>') if rest else ""
        cta = (f'<aside class="cta-inline" style="margin-top:2rem">'
               f'<div><h3>Ready to go further?</h3><p>{course_name} turns these guides into a structured course, live every weekend with a mentor.</p></div>'
               f'<a class="btn btn-amber" href="{course_href}" data-cta="blog-segment-course">See {course_name}</a></aside>')
        blocks.append(_panel(_seg_id(name), f"For {name.lower()}.", who, "".join(_card(a) for a in head), more, cta))
    return banner + f"""
<section class="guides-head">
  <div class="wrap">
    <div class="store-head">
      <h1>Guides</h1>
      <p>{len(articles):,} guides from the brewhouse floor. Search, or pick who you are.</p>
    </div>
  </div>
</section>""" + _finder(articles, segment_of) + f"""
<div id="doors">
<div class="wrap"><nav class="topic-row" id="topic-tabs" role="tablist" aria-label="Guides by reader">{jump}</nav></div>
{"".join(blocks)}
</div>
<script>{TABS_JS}</script>
<section class="cta">
  <div class="wrap" style="text-align:center">
    <h2>Reading is a start. Brewing is better.</h2>
    <p class="lead" style="margin-inline:auto">Every guide here is a slice of what
    we teach properly, with mentors, tastings and real brewhouse time.</p>
    <a class="btn btn-amber" href="courses.html" data-cta="blog-courses">See the courses</a>
  </div>
</section>
"""
