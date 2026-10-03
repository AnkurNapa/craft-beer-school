# -*- coding: utf-8 -*-
"""Search and recommendations, all built at build time from the same records
as the pages, so nothing here can point at a page that does not exist.

- search_index(): assets/search.json, one row per course, guide, style and
  mentor. search.html scores it in the browser, no server and no library.
- recommended(article): three guides a reader of this one is likely to want
  next, picked by shared reader segment, category and vocabulary. Fills the
  gap the hand-picked "related" list leaves.
- course_guides(course): every live guide whose call to action sells this
  course, so a course page shows the reading that already points at it.
- finder(): the "which course fits me?" picker on courses.html. Static HTML
  plus a few lines of script, driven by the same segment table as the blog.
"""
import json
import re

import articles_all
import pages_a

_STOP = set("the a an and or of to in for on with your you is are it its at by from how what why "
            "when where which this that these those as be can do we our not into guide guides beer brewing brew brewery "
            "breweries india indian first every one get make making works does need needs here really right".split())


def _tokens(text):
    return {w for w in re.findall(r"[a-z0-9]+", re.sub(r"<[^>]+>", " ", text.lower())) if w not in _STOP and len(w) > 2}


def _plain(s):
    return re.sub(r"<[^>]+>", " ", s or "").replace("&amp;", "&").strip()


# ---- search index ----------------------------------------------------------
def search_index(articles, styles, mentors):
    rows = []
    for c in pages_a.COURSE_DATA:
        name = _plain(c["name"])
        rows.append({"u": pages_a.course_href(c["name"]), "k": "Course", "t": name,
                     "d": _plain(c["blurb"]), "x": " ".join(_plain(i) for i in c["items"]) + f" {c['dur']} {c['price']}"})
    for a in articles:
        heads = " ".join(h for h, _ in a["sections"]) + " " + " ".join(q for q, _ in a.get("faqs", []))
        rows.append({"u": f"{a['slug']}.html", "k": "Guide", "t": _plain(a["h1"]), "d": _plain(a["teaser"]),
                     "c": a["cat"], "s": articles_all.SEGMENT.get(a["slug"], ""), "x": _plain(heads)})
    for s in styles.values():
        rows.append({"u": f"{s['slug']}.html", "k": "Style", "t": s["name"], "d": _plain(s.get("tagline", "")),
                     "c": s.get("family", ""), "x": " ".join(s.get("tastes", [])) if isinstance(s.get("tastes"), list) else _plain(str(s.get("tastes", "")))})
    for m in mentors:
        rows.append({"u": m["slug"], "k": "Mentor", "t": m["name"], "d": _plain(m["role"]), "x": " ".join(m.get("areas", []))})
    for u, t, d in [("courses.html", "All courses", "Every online course and in-person workshop."),
                    ("for-companies.html", "Corporate services", "Training, consultancy and hiring for drinks companies."),
                    ("resources.html", "Free resources", "Beer 101, glossary, calculators and tasting tools."),
                    ("faq.html", "FAQ", "Format, certificates, payment and refunds."),
                    ("contact.html", "Contact and enrol", "Enrol, ask a question or book a tasting.")]:
        rows.append({"u": u, "k": "Page", "t": t, "d": d, "x": ""})
    return json.dumps(rows, ensure_ascii=False, separators=(",", ":"))


SEARCH_FORM = ('<form class="search-form" action="search.html" role="search">'
               '<input type="search" name="q" placeholder="Search guides, courses, styles" aria-label="Search the site" />'
               '<button type="submit" aria-label="Search">[[arrow-right]]</button></form>')

POPULAR = ["IPA", "yeast", "mash temperature", "microbrewery licence", "off-flavours", "Power BI", "whisky", "kombucha"]


def search_page():
    chips = "".join(f'<a href="search.html?q={q.replace(" ", "+")}" class="seg-chip" data-cta="search-popular">{q}</a>' for q in POPULAR)
    return pages_a.banner("Search", "Find it", "Search the school.",
                          "Every guide, course, beer style and mentor on the site, from one box.") + f"""
<section>
  <div class="wrap search-wrap">
    {SEARCH_FORM.replace('class="search-form"', 'class="search-form search-big" id="search-form"')}
    <p class="search-status" id="search-status" aria-live="polite">Popular right now:</p>
    <nav class="seg-nav" id="search-popular" aria-label="Popular searches">{chips}</nav>
    <div id="search-results" class="search-results"></div>
    <aside class="cta-inline" id="search-miss" hidden style="margin-top:2rem">
      <div><h3>Not finding it?</h3><p>Ask us. A brewer answers on WhatsApp, usually the same day.</p></div>
      <a href="__WA__" class="btn btn-wa" target="_blank" rel="noopener" data-cta="search-whatsapp">[[whatsapp]] Ask on WhatsApp</a>
    </aside>
  </div>
</section>
<script>
(async()=>{{
const form=document.getElementById('search-form'),box=form.q,out=document.getElementById('search-results'),
status=document.getElementById('search-status'),pop=document.getElementById('search-popular'),miss=document.getElementById('search-miss');
const ORDER={{Course:0,Guide:1,Style:2,Mentor:3,Page:4}};
const esc=s=>s.replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
let rows=null;
const load=async()=>rows||(rows=(await (await fetch('assets/search.json')).json()).map(r=>({{...r,_t:r.t.toLowerCase(),_d:(r.d||'').toLowerCase(),_x:((r.x||'')+' '+(r.c||'')+' '+(r.s||'')).toLowerCase()}})));
const terms=q=>q.toLowerCase().match(/[a-z0-9]+/g)||[];
function score(r,ts){{let s=0;for(const t of ts){{let h=0;
 if(r._t.includes(t)){{h+=r._t.startsWith(t)?8:6}}if(r._d.includes(t))h+=3;if(r._x.includes(t))h+=1;
 if(!h)return 0;s+=h}}if(r.k==='Course')s+=2;return s}}
function render(q){{const ts=terms(q);history.replaceState(null,'',q?'?q='+encodeURIComponent(q):'search.html');
 if(!ts.length){{out.innerHTML='';status.textContent='Popular right now:';pop.hidden=false;miss.hidden=true;return}}
 pop.hidden=true;
 const hits=rows.map(r=>[score(r,ts),r]).filter(([s])=>s>0).sort((a,b)=>b[0]-a[0]||ORDER[a[1].k]-ORDER[b[1].k]).slice(0,40);
 status.textContent=hits.length?`${{hits.length}} result${{hits.length===1?'':'s'}} for "${{q}}"`:`Nothing matched "${{q}}". Try a shorter word.`;
 miss.hidden=hits.length>3;
 out.innerHTML=hits.map(([,r])=>`<a class="search-hit" href="${{r.u}}" data-cta="search-hit"><span class="cat">${{r.k}}${{r.c?' · '+esc(r.c):''}}</span><strong>${{esc(r.t)}}</strong><span>${{esc(r.d||'')}}</span></a>`).join('');}}
await load();
const q0=new URLSearchParams(location.search).get('q')||'';box.value=q0;render(q0);
let t;box.addEventListener('input',()=>{{clearTimeout(t);t=setTimeout(()=>render(box.value.trim()),120)}});
form.addEventListener('submit',e=>{{e.preventDefault();render(box.value.trim())}});
box.focus();
}})();
</script>
"""


# ---- recommendations --------------------------------------------------------
def recommended(article, articles, n=3):
    """Guides a reader of this one is likely to want next, beyond the hand-picked related list."""
    me = _tokens(article["h1"] + " " + article["teaser"] + " " + article["standfirst"])
    seg = articles_all.SEGMENT.get(article["slug"])
    skip = {article["slug"], *article.get("related", [])}
    scored = []
    for a in articles:
        if a["slug"] in skip:
            continue
        same_seg = articles_all.SEGMENT.get(a["slug"]) == seg
        same_cat = a["cat"] == article["cat"]
        if not (same_seg or same_cat):
            continue  # a pairing reader does not want glycol, however many words overlap
        s = 3 * same_seg + 3 * same_cat + (a["cta"]["href"] == article["cta"]["href"])
        s += 2 * min(4, len(me & _tokens(a["h1"] + " " + a["teaser"] + " " + a["standfirst"])))
        scored.append((s, a["updated"], a))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [a for _, _, a in scored[:n]]


def _cards(items, cta):
    return "".join(f"""
      <article class="card reveal"><div class="card-body">
        <span class="cat">{a['cat']}</span>
        <h3>{a['h1']}</h3>
        <p>{a['teaser']}</p>
        <div class="foot"><a href="{a['slug']}.html" class="link-arrow" data-cta="{cta}">Read</a><span class="read">{a['read']}</span></div>
      </div></article>""" for a in items)


def recommended_section(article, articles):
    picks = recommended(article, articles)
    if not picks:
        return ""
    return f"""
<section class="related">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Recommended for you</span><h2>Readers of this guide go on to these.</h2></div>
    <div class="grid-3">{_cards(picks, "recommended-article")}</div>
    <p style="margin-top:1.4rem"><a href="search.html" class="link-arrow" data-cta="recommended-search">Search every guide</a></p>
  </div>
</section>"""


def course_guides(course, articles, skip, n=6):
    """Live guides whose CTA sells this course, newest first, minus the reading list."""
    href = pages_a.course_href(course["name"])
    return [a for a in articles if a["cta"]["href"] == href and a["slug"] not in skip][:n]


def course_guides_section(course, articles, skip):
    picks = course_guides(course, articles, skip)
    if not picks:
        return ""
    return f"""
<section class="tint related">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Free reading</span><h2>Guides that lead here.</h2><p class="lead">A taste of the course, written by the people who teach it.</p></div>
    <div class="grid-3">{_cards(picks, "course-guide")}</div>
  </div>
</section>"""


# ---- course finder ----------------------------------------------------------
# segment -> (primary course name, [also consider]). Primary follows the blog's
# segment table so the two can never disagree; the alternates are ours.
_ALSO = {
    "Beer lovers": ["Brewing Fundamentals", "Style Specialisation"],
    "Homebrewers": ["Advanced Brewing Science", "Style Specialisation"],
    "Professional brewers": ["Power BI and Tableau for Breweries", "ESG in Craft Brewing"],
    "Founders": ["Beer Branding &amp; Packaging", "Digital Transformation Basics for Brewing"],
    "Brand builders": ["AI for Craft Breweries", "Brewery Business Management"],
    "Career changers": ["Sensory Evaluation", "Safety in Brewing"],
    "Drinks producers": ["Craft Distilling", "Non-Alcoholic Beer"],
    "Corporate teams": ["Sensory Evaluation", "Power BI and Tableau for Breweries"],
}
_BY_NAME = {c["name"]: c for c in pages_a.COURSE_DATA}


def _course_link(name):
    c = _BY_NAME.get(name)
    if not c:
        return f'<a href="{name}">{name}</a>'
    return f'<a href="{pages_a.course_href(c["name"])}">{c["name"]}</a> <small>{c["dur"]} · {c["price"]}</small>'


def finder():
    opts = []
    panels = []
    for i, (seg, who, href, name) in enumerate(articles_all.SEGMENTS):
        c = _BY_NAME.get(name)
        primary = (f'<a href="{href}" class="btn btn-amber" data-cta="finder-course">See {name}</a>' if not c else
                   f'<a href="{href}" class="btn btn-amber" data-cta="finder-course">See {c["name"]} · {c["dur"]} · {c["price"]}</a>')
        blurb = c["blurb"] if c else "Tell us about the team or the brewery and we will shape it around you."
        also = "".join(f"<li>{_course_link(n)}</li>" for n in _ALSO.get(seg, []))
        sid = seg.lower().replace(" ", "-")
        opts.append(f'<label class="finder-opt"><input type="radio" name="finder" value="{sid}"{" checked" if i == 0 else ""} />'
                    f'<span><strong>{seg}</strong><em>{who}</em></span></label>')
        panels.append(f"""<div class="finder-panel" data-seg="{sid}"{'' if i == 0 else ' hidden'}>
        <span class="eyebrow">Start here</span><h3>{c["name"] if c else name}</h3><p>{blurb}</p>
        <div class="cta-pair">{primary}</div>
        <p class="finder-also">Also worth a look:</p><ul class="checklist">{also}</ul>
      </div>""")
    return f"""
<section class="tint" id="finder">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Course finder</span><h2>Not sure which course fits?</h2><p class="lead">Pick the line that sounds most like you. We will point you at the right pour, and two others worth a look.</p></div>
    <div class="finder">
      <fieldset class="finder-opts"><legend class="sr-only">Who are you?</legend>{"".join(opts)}</fieldset>
      <div class="finder-out">{"".join(panels)}</div>
    </div>
    <p style="margin-top:1.4rem;color:var(--ink-soft);font-size:.92rem">Still torn? <a href="contact.html#enroll" style="color:var(--blue);text-decoration:underline" data-cta="finder-ask">Ask us</a> and a mentor will reply within a day.</p>
  </div>
</section>
<script>
document.querySelectorAll('#finder input[name=finder]').forEach(r=>r.addEventListener('change',()=>{{
  document.querySelectorAll('#finder .finder-panel').forEach(p=>p.hidden=p.dataset.seg!==r.value);}}));
</script>
"""
