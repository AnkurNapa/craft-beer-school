"""Brewing glossary: brewing-glossary.html.

Terms live in content/glossary/terms-*.json ({term, aka, cat, def, link}). The page
is static HTML (every definition readable without JS) with an A to Z bar, a
category filter and search on top, plus DefinedTermSet structured data so search
and answer engines can quote a definition with its source.
"""
import html
import json
import pathlib

from pages_a import banner

DATA = pathlib.Path(__file__).parent / "content" / "glossary"
SITE = "https://craftbeerschool.in"
SLUG = "brewing-glossary.html"
E = html.escape


def _id(term):
    return "t-" + "".join(ch if ch.isalnum() else "-" for ch in term.lower()).strip("-")


def load():
    seen, out = set(), []
    for f in sorted(DATA.glob("terms-*.json")):
        for t in json.loads(f.read_text()):
            key = t["term"].lower()
            if key in seen:
                continue
            seen.add(key)
            out.append(t)
    return sorted(out, key=lambda t: t["term"].lower())


def _link(t):
    s = t.get("link") or ""
    if not s:
        return ""
    href = s if s.endswith(".html") else s + ".html"
    return href if (pathlib.Path(__file__).parent / href).exists() else ""


def graph_nodes():
    terms = load()
    return [{"@type": "DefinedTermSet", "@id": f"{SITE}/{SLUG}#set", "name": "Craft Beer School brewing glossary",
             "hasDefinedTerm": [{"@type": "DefinedTerm", "@id": f"{SITE}/{SLUG}#{_id(t['term'])}", "name": t["term"],
                                 **({"alternateName": t["aka"]} if t.get("aka") else {}),
                                 "description": t["def"], "inDefinedTermSet": f"{SITE}/{SLUG}#set"} for t in terms]}]


def page():
    terms = load()
    cats = sorted({t["cat"] for t in terms})
    letters = sorted({t["term"][0].upper() for t in terms if t["term"][0].isalpha()})
    az = "".join(f'<a href="#letter-{l}">{l}</a>' for l in letters)
    opts = "".join(f'<option value="{E(c)}">{E(c)}</option>' for c in cats)
    blocks, current = [], None
    for t in terms:
        first = t["term"][0].upper() if t["term"][0].isalpha() else "#"
        if first != current:
            if current is not None:
                blocks.append("</dl></section>")
            blocks.append(f'<section class="gl-letter" id="letter-{first}"><h2>{first}</h2><dl>')
            current = first
        aka = f'<span class="gl-aka">Also: {E(", ".join(t["aka"]))}</span>' if t.get("aka") else ""
        more = f' <a href="{_link(t)}" class="gl-more">Read the guide</a>' if _link(t) else ""
        q = " ".join([t["term"], *t.get("aka", []), t["def"]]).lower()
        blocks.append(f'<div class="gl-term" id="{_id(t["term"])}" data-cat="{E(t["cat"])}" data-q="{E(q)}">'
                      f'<dt>{E(t["term"])} <span class="gl-cat">{E(t["cat"])}</span></dt>'
                      f'<dd>{E(t["def"])}{more}{aka}</dd></div>')
    if current is not None:
        blocks.append("</dl></section>")
    return banner("Brewing glossary", "Learn · Reference", "Brewing glossary.",
                  f"{len(terms)} brewing, tasting, packaging, business and wine terms, defined in plain English for brewers "
                  "and drinkers in India. Search, filter by topic or jump to a letter.") + f"""
<section style="padding-block:2rem 0">
  <div class="wrap">
    <form class="finder ig-finder" id="gl-finder" role="search" action="{SLUG}">
      <label class="sr-only" for="gl-cat">Topic</label>
      <select id="gl-cat" name="cat"><option value="">All topics</option>{opts}</select>
      <label class="sr-only" for="gl-q">Search the glossary</label>
      <input id="gl-q" name="q" type="search" placeholder="Search {len(terms)} terms" autocomplete="off" />
      <button type="submit" class="btn btn-navy">Search</button>
    </form>
    <nav class="gl-az" aria-label="Jump to letter">{az}</nav>
    <p class="f-count bd-count" id="gl-count" aria-live="polite">Showing all {len(terms)} terms</p>
    <div class="gl-list">{"".join(blocks)}</div>
  </div>
</section>
<section class="cta"><div class="wrap" style="text-align:center">
  <h2>Know the words. Now learn the craft.</h2>
  <p class="lead" style="margin-inline:auto">Brewing Fundamentals turns these terms into a working brew day, online or in person.</p>
  <a class="btn btn-amber" href="brewing-fundamentals-course.html" data-cta="glossary-course">See Brewing Fundamentals</a>
</div></section>
<script>{JS}</script>"""


JS = """(()=>{
const f=document.getElementById('gl-finder'),rows=[...document.querySelectorAll('.gl-term')],secs=[...document.querySelectorAll('.gl-letter')],count=document.getElementById('gl-count');
function apply(){
  const u=new URLSearchParams(location.search),c=u.get('cat')||'',q=(u.get('q')||'').trim().toLowerCase(),terms=q.split(/\\s+/).filter(Boolean);
  f.cat.value=c;f.q.value=u.get('q')||'';let n=0;
  rows.forEach(r=>{const ok=(!c||r.dataset.cat===c)&&terms.every(t=>r.dataset.q.includes(t));r.hidden=!ok;if(ok)n++});
  secs.forEach(s=>s.hidden=!s.querySelector('.gl-term:not([hidden])'));
  count.textContent=n===rows.length?`Showing all ${n} terms`:n?`Showing ${n} of ${rows.length} terms`:'No term matches. Try a shorter word.';
}
f.addEventListener('submit',e=>{e.preventDefault();const x=new URLSearchParams();f.cat.value&&x.set('cat',f.cat.value);f.q.value.trim()&&x.set('q',f.q.value.trim());history.replaceState(null,'','brewing-glossary.html'+(x.toString()?'?'+x:''));apply()});
f.cat.addEventListener('change',()=>f.requestSubmit());
f.q.addEventListener('input',()=>{clearTimeout(f._t);f._t=setTimeout(()=>f.requestSubmit(),200)});
apply();
})();"""
