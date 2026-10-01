# -*- coding: utf-8 -*-
"""Style Library: one card page per beer style plus a filterable index.

Facts (family, ranges, similar styles, linked long guide) come from
content/styles_plan.json; every word of prose comes from content/styles/*.json.
"""
import json
import pathlib

from article_render import _byline
from urllib.parse import quote

HERE = pathlib.Path(__file__).parent
PLAN = json.loads((HERE / "content/styles_plan.json").read_text())
INDEX = "style-library.html"
COURSE = "style-specialization-course.html"

# Approximate SRM to on-screen colour, 1 to 40.
SRM_HEX = ["#FFE699", "#FFD878", "#FFCA5A", "#FFBF42", "#FBB123", "#F8A600", "#F39C00", "#EA8F00",
           "#E58500", "#DE7C00", "#D77200", "#CF6900", "#CB6200", "#C35900", "#BB5100", "#B54C00",
           "#B04500", "#A63E00", "#A13700", "#9B3200", "#952D00", "#8E2900", "#882300", "#821E00",
           "#7B1A00", "#771900", "#701400", "#6A0E00", "#660D00", "#5E0B00", "#5A0A02", "#600903",
           "#520907", "#4C0505", "#470606", "#440607", "#3F0708", "#3B0607", "#3A070B", "#36080A"]
SCALE = {"srm": (40, "Colour", "SRM"), "ibu": (100, "Bitterness", "IBU"), "abv": (14, "Strength", "ABV")}


# Glass silhouettes on a 24x36 grid, rim at y=2. "bowl" holds the beer; "stem" is drawn as glass only.
_STEM = "M11.2 20.5V31h1.6V20.5ZM8 31h8v2H8Z"
GLASS_SHAPES = {
    "Pint": ("M5 2H19L17 34H7Z", ""),
    "Nonic pint": ("M5 2H19L18.4 8Q19.6 10 18.5 12L17 34H7L5.5 12Q4.4 10 5.6 8Z", ""),
    "Pilsner glass": ("M6 2H18L13.6 30H10.4Z", "M8 30h8v3H8Z"),
    "Stange": ("M7.5 2H16.5V34H7.5Z", ""),
    "Weizen glass": ("M7 2Q4 8 7 14Q9.5 20 8.5 34H15.5Q14.5 20 17 14Q20 8 17 2Z", ""),
    "Willi becher": ("M6.5 2H17.5L18.3 12Q18.8 13 18.2 14L16.5 34H7.5L5.8 14Q5.2 13 5.7 12Z", ""),
    "Tulip": ("M7 2Q5 8 6 13.5Q7 20 12 20.5Q17 20 18 13.5Q19 8 17 2Z", _STEM),
    "Snifter": ("M8 3Q3 11 5.5 16.5Q8 20.5 12 20.5Q16 20.5 18.5 16.5Q21 11 16 3Z", _STEM),
    "Goblet": ("M4.5 2Q4.5 17 12 19Q19.5 17 19.5 2Z", "M11.2 19V31h1.6V19ZM8 31h8v2H8Z"),
    "Teku": ("M6 2L8 11Q8 20.5 12 20.5Q16 20.5 16 11L18 2Z", _STEM),
    "Thistle": ("M5 2Q8 10 9 12.5Q5.5 15 7 18.5Q9 20.5 12 20.5Q15 20.5 17 18.5Q18.5 15 15 12.5Q16 10 19 2Z", _STEM),
    "Stemmed glass": ("M6 2L7 16.5Q8 20 12 20Q16 20 17 16.5L18 2Z", _STEM),
}


def glass_svg(glass, srm, size=36, uid="g"):
    """The style's own glass, filled with an approximation of its colour under a foam head."""
    bowl, stem = GLASS_SHAPES.get(glass, GLASS_SHAPES["Pint"])
    w = round(size * 24 / 36)
    stem_el = f'<path d="{stem}" fill="#e9eef0" stroke="currentColor" stroke-width="1.2"/>' if stem else ""
    return (f'<svg class="glassico" viewBox="0 0 24 36" width="{w}" height="{size}" aria-hidden="true">'
            f'<clipPath id="c-{uid}"><path d="{bowl}"/></clipPath>'
            f'<g clip-path="url(#c-{uid})"><rect width="24" height="36" fill="{srm_hex(srm)}"/>'
            f'<rect width="24" height="7" y="0" fill="#fff8ec"/><rect width="24" height="1" y="7" fill="#000" opacity=".08"/></g>'
            f'{stem_el}<path d="{bowl}" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>')


def _range(s):
    if s.endswith("+"):
        return float(s[:-1]), 99.0
    try:
        lo, hi = s.rstrip("%").split("-")
        return float(lo), float(hi)
    except ValueError:
        return None


def srm_hex(srm):
    r = _range(srm)
    mid = 12 if not r else (r[0] + r[1]) / 2
    return SRM_HEX[max(1, min(40, round(mid))) - 1]


def _bar(key, value):
    top, label, unit = SCALE[key]
    r = _range(value)
    if not r:
        return f'<div class="sbar"><span class="sbar-l">{label}</span><span class="sbar-v">Varies</span><div class="sbar-t"></div></div>'
    lo, hi = (min(100, v / top * 100) for v in r)
    shown = value if key == "abv" else f"{value} {unit}"
    return (f'<div class="sbar"><span class="sbar-l">{label}</span><span class="sbar-v">{shown}</span>'
            f'<div class="sbar-t"><i style="left:{lo:.0f}%;width:{max(3, hi - lo):.0f}%"></i></div></div>')


def load_cards():
    out = {}
    for p in PLAN:
        f = HERE / f"content/styles/{p['slug']}.json"
        if f.exists():
            out[p["slug"]] = {**p, **json.loads(f.read_text())}
    return out


AUTHORS = [
    ("Written by", dict(name="Ankur Napa", role="Master Brewer and course instructor", photo="assets/ankur-napa.jpg")),
    ("Written by", dict(name="Chatty Girija", role="Beer podcaster and creative strategist", photo="assets/chatty-girija.jpg")),
]
PAIRING_BY = dict(name="Anuradha Rao", role="Head of Strategy and Operations", photo="assets/anu-rao.jpg")
READ_KEY = "cbs-styles-read"  # localStorage: slugs this reader has opened


def credit_strip(with_pairing=False):
    """Phone-sized credits: overlapping faces and one line of names."""
    people = [a for _, a in AUTHORS] + ([PAIRING_BY] if with_pairing else [])
    faces = "".join(f'<img src="{x["photo"]}" alt="" width="30" height="30" loading="lazy">' for x in people)
    text = "By Ankur Napa and Chatty Girija" + (", food pairings by Anuradha Rao" if with_pairing else "")
    return f'<p class="credit-strip"><span class="faces">{faces}</span><span>{text}</span></p>'


def _nav(card, cards):
    """Where this card sits: family position, overall position, prev and next in library order."""
    order = list(cards)
    i = order.index(card["slug"])
    fam = [s for s in order if cards[s]["family"] == card["family"]]
    prev_c, next_c = (cards[order[i - 1]] if i else None), (cards[order[i + 1]] if i + 1 < len(order) else None)
    return i, len(order), fam.index(card["slug"]) + 1, len(fam), prev_c, next_c


def _fam_href(family):
    return f"{INDEX}#fam={quote(family)}"


def render(card, cards, guide_title):
    i, total, fpos, ftotal, prev_c, next_c = _nav(card, cards)
    back = f"{INDEX}#{card['slug']}"
    step = lambda c, rel, label: (
        f'<a class="style-step {rel}" rel="{rel}" href="{c["slug"]}.html" data-key="{rel}">'
        f'<span>{label}</span><strong>{c["name"]}</strong><em>{c["family"]}</em></a>') if c else "<span></span>"
    prof = card["profile"]
    pairs = "".join(f"<li><strong>{x['food']}</strong><span>{x['why']}</span></li>" for x in card["pairings"])
    if card["examples"]:
        ex = "".join(f'<li><strong>{e["beer"]}</strong>, {e["brewery"]} '
                     f'<a href="{e["source"]}" target="_blank" rel="noopener nofollow">source</a></li>'
                     for e in card["examples"])
        ex = f"<ul class='style-ex'>{ex}</ul>"
    else:
        ex = f"<p>{card['examples_note']}</p>"
    similar = "".join(f'<a class="seg-chip" href="{s}.html">{cards[s]["name"]}</a>'
                      for s in card["similar"] if s in cards)
    guide = (f'<p class="style-guide-link">Want the long read? <a href="{card["guide"]}.html" class="link-arrow">'
             f'{guide_title}</a></p>') if card.get("guide") and guide_title else ""
    return f"""
<article class="post style-card">
  <div class="wrap post-head">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <a href="{back}">Style Library</a> / <span>{card['name']}</span></nav>
    <div class="style-where">
      <a class="style-back" href="{back}" data-cta="style-back">[[arrow-left]] All {total} styles</a>
      <a class="eyebrow" href="{_fam_href(card['family'])}">{card['family']}, {fpos} of {ftotal}</a>
      <span class="style-pos">Style {i + 1} of {total}</span>
    </div>
    <h1 class="post-title style-h1"><span class="glass-fig">{glass_svg(card['glass'], card['srm'], 88, 'h')}<small>{card['glass']}</small></span><span>{card['name']}</span></h1>
    <p class="lead">{card['tagline']}</p>
    {_byline(AUTHORS)}{credit_strip()}
  </div>
  <div class="wrap post-body">
    <section class="style-stats" aria-label="Style numbers">
      {_bar('srm', card['srm'])}{_bar('ibu', card['ibu'])}{_bar('abv', card['abv'])}
      <p class="style-serve">Serve in a <strong>{card['glass'].lower()}</strong> at <strong>{card['serve_c']} °C</strong></p>
    </section>
    <nav class="style-jump" aria-label="On this page"><a href="#taste">Taste</a><a href="#profile">Profile</a><a href="#india">In India</a><a href="#pairing">Food</a><a href="#examples">Brewed here</a></nav>
    <h2 id="taste">What it tastes like</h2>
    {card['tastes']}
    <h2 id="profile">Style profile</h2>
    <dl class="style-prof">
      <dt>Look</dt><dd>{prof['look']}</dd>
      <dt>Aroma and flavour</dt><dd>{prof['aroma_flavour']}</dd>
      <dt>Mouthfeel</dt><dd>{prof['mouthfeel']}</dd>
      <dt>Ingredients</dt><dd>{prof['ingredients']}</dd>
    </dl>
    <h2 id="india">In India</h2>
    {card['in_india']}
    <h2 id="pairing">At the Indian table</h2>
    <p class="pair-credit"><img src="{PAIRING_BY['photo']}" alt="{PAIRING_BY['name']}" width="36" height="36" loading="lazy">
      <span>Food pairings contributed by <strong>{PAIRING_BY['name']}</strong></span></p>
    <ul class="style-pairs">{pairs}</ul>
    <h2 id="examples">Brewed in India</h2>
    {ex}
    {guide}
    <h2 id="similar">If you like this, try</h2>
    <nav class="seg-nav">{similar}</nav>
    <nav class="style-steps" aria-label="Next and previous style">
      {step(prev_c, "prev", "Previous style")}
      {step(next_c, "next", "Next style")}
    </nav>
    <p class="style-backline"><a href="{back}" class="style-back" data-cta="style-back-bottom">[[arrow-left]] Back to the Style Library</a> <span class="style-readcount"></span></p>
    <aside class="cta-band">
      <div><h3>Learn to taste and brew styles properly</h3>
      <p>Style Specialization walks through every major family with live tastings and a mentor, eight weekends, online.</p></div>
      <a class="btn btn-amber" href="{COURSE}" data-cta="style-card">See the full syllabus</a>
    </aside>
  </div>
</article>
<script>
(()=>{{const K="{READ_KEY}";let r=[];try{{r=JSON.parse(localStorage.getItem(K)||"[]")}}catch(_){{}}
if(!r.includes("{card['slug']}"))r.push("{card['slug']}");try{{localStorage.setItem(K,JSON.stringify(r))}}catch(_){{}}
const c=document.querySelector(".style-readcount");if(c)c.textContent="You have read "+r.length+" of {total}.";
document.addEventListener("keydown",e=>{{if(e.target.closest("input,textarea")||e.altKey||e.metaKey||e.ctrlKey)return;
const a=document.querySelector('.style-step[data-key="'+(e.key==="ArrowLeft"?"prev":e.key==="ArrowRight"?"next":"")+'"]');if(a)location.href=a.href}});}})();
</script>
"""


def index(cards):
    fams = list(dict.fromkeys(c["family"] for c in cards.values()))
    chips = '<button class="seg-chip on" data-fam="">All</button>' + "".join(
        f'<button class="seg-chip" data-fam="{f}">{f}</button>' for f in fams)
    tile = lambda c: f"""
      <a class="style-tile" id="{c['slug']}" href="{c['slug']}.html" data-fam="{c['family']}" data-name="{c['name'].lower()}">
        <span class="glass-fig">{glass_svg(c['glass'], c['srm'], 60, c['slug'])}<small>{c['glass']}</small></span>
        <strong>{c['name']}</strong>
        <span class="style-nums">{c['abv']} ABV · {c['ibu']} IBU</span>
      </a>"""
    tiles = "".join(f"""
    <section class="fam-group" data-fam="{f}">
      <h2 class="fam-head">{f} <span>{sum(1 for c in cards.values() if c['family'] == f)} styles</span></h2>
      <div class="style-grid">{"".join(tile(c) for c in cards.values() if c["family"] == f)}</div>
    </section>""" for f in fams)
    return f"""
<section class="style-lib" style="padding:0">
  <div class="wrap"><div class="post-head">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span>Style Library</span></nav>
    <span class="eyebrow">Style Library</span>
    <h1 class="post-title">{len(cards)} beer styles, explained for India</h1>
    <p class="lead">Colour, bitterness and strength at a glance, what each beer tastes like, how it holds up in our heat, and what to eat with it, from dal makhani to Goan prawn curry.</p>
    {_byline(AUTHORS + [("Food pairings by", PAIRING_BY)])}{credit_strip(True)}
    <input class="style-search" type="search" placeholder="Search styles, e.g. stout, wheat, sour" aria-label="Search styles">
    <nav class="seg-nav style-filter" aria-label="Filter by family">{chips}</nav>
    <p class="style-progress" hidden><span></span> <a class="link-arrow" href="{next(iter(cards))}.html">Continue reading</a></p>
  </div></div>
</section>
<section style="padding-top:1rem"><div class="wrap">{tiles}</div></section>
<script>
(()=>{{const t=[...document.querySelectorAll('.style-tile')],q=document.querySelector('.style-search'),
btns=[...document.querySelectorAll('.style-filter button')];let fam='';
const save=()=>{{const h=new URLSearchParams();if(fam)h.set('fam',fam);if(q.value.trim())h.set('q',q.value.trim());
history.replaceState(null,'',h.toString()?'#'+h:location.pathname)}};
const go=()=>{{const s=q.value.trim().toLowerCase();btns.forEach(x=>x.classList.toggle('on',x.dataset.fam===fam));
t.forEach(e=>e.hidden=!((!fam||e.dataset.fam===fam)&&(!s||e.dataset.name.includes(s)||e.dataset.fam.toLowerCase().includes(s))));
document.querySelectorAll('.fam-group').forEach(g=>g.hidden=!g.querySelector('.style-tile:not([hidden])'))}};
q.addEventListener('input',()=>{{go();save()}});
btns.forEach(b=>b.addEventListener('click',()=>{{fam=b.dataset.fam;go();save()}}));
const h=location.hash.slice(1);
if(h.includes('=')){{const p=new URLSearchParams(h);fam=p.get('fam')||'';q.value=p.get('q')||'';go()}}
else if(h){{const tile=document.getElementById(h);if(tile){{tile.scrollIntoView({{block:'center',behavior:'instant'}});tile.classList.add('flash')}}}}
let r=[];try{{r=JSON.parse(localStorage.getItem("{READ_KEY}")||"[]")}}catch(_){{}}
t.forEach(e=>e.classList.toggle('read',r.includes(e.id)));
const pr=document.querySelector('.style-progress'),nxt=t.find(e=>!r.includes(e.id));
if(r.length&&pr){{pr.hidden=false;pr.querySelector('span').textContent='You have read '+r.filter(x=>document.getElementById(x)).length+' of '+t.length+' styles.';
const a=pr.querySelector('a');if(nxt){{a.href=nxt.getAttribute('href');a.textContent='Continue with '+nxt.querySelector('strong').textContent}}else a.remove()}}
}})();
</script>
"""


SHOWCASE = ["style-german-style-pilsner", "style-german-style-hefeweizen", "style-new-england-ipa",
            "style-belgian-style-tripel", "style-belgian-style-saison", "style-irish-style-dry-stout",
            "style-german-style-kolsch", "style-british-style-barley-wine-ale"]


def home_teaser():
    """Home page strip: a row of real glasses that each open their style."""
    cards = load_cards()
    glasses = "".join(
        f'<a class="shelf-glass" href="{s}.html" data-cta="home-style-glass">'
        f'<span class="shelf-slot">{glass_svg(cards[s]["glass"], cards[s]["srm"], 76, "home-" + s)}</span>'
        f'<span class="shelf-name">{cards[s]["name"]}</span></a>'
        for s in SHOWCASE if s in cards)
    return f"""
<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">New · Free Style Library</span>
      <h2>{len(cards)} beer styles, explained for India.</h2>
      <p class="lead">Colour, bitterness and strength at a glance, the right glass, and what to eat with each one, from vada pav to Goan prawn curry. Pick a glass to start.</p></div>
    <div class="shelf">{glasses}</div>
    <div style="margin-top:2rem"><a href="{INDEX}" class="btn btn-amber" data-cta="home-style-library">Browse all {len(cards)} styles</a></div>
  </div>
</section>
"""


def pages(articles_by_slug):
    """(filename -> (title, desc, active, body)) for build.py."""
    cards = load_cards()
    if not cards:
        return {}
    out = {INDEX: ("Beer Style Library, 80 Styles for India | Craft Beer School",
                   "Every major beer style at a glance: colour, bitterness, strength, taste, and Indian food pairings, written by working brewers.",
                   "styles", index(cards))}
    for c in cards.values():
        g = articles_by_slug.get(c.get("guide") or "")
        out[f"{c['slug']}.html"] = (c["title"], c["desc"], "styles", render(c, cards, g and g["h1"]))
    return out
