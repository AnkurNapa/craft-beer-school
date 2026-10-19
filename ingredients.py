"""Ingredient reference guides: yeast strains, hops and malts.

Each dataset in content/ingredients/*.json was compiled from the makers' own
datasheets, one source URL per row. One renderer draws all three as a filterable
list; every row is static HTML so search and answer engines can read it.
"""
import html
import json
import pathlib

from pages_a import banner

DATA = pathlib.Path(__file__).parent / "content" / "ingredients"
SITE = "https://craftbeerschool.in"
E = html.escape


def _f(c):
    return round(c * 9 / 5 + 32)


def temp(c_range):
    """'18-26' -> '18-26 °C (64-79 °F)'."""
    if not c_range:
        return None
    parts = [float(p) for p in str(c_range).split("-")]
    c = "-".join(f"{p:g}" for p in parts)
    return f"{c} °C ({'-'.join(str(_f(p)) for p in parts)} °F)"


def ebc(e_range):
    """'5-6' EBC -> '5-6 EBC (2.5-3 °L)', using °L = (EBC x 0.508 + 0.76) / 1.3546."""
    if not e_range:
        return None
    try:
        parts = [float(p) for p in str(e_range).replace(",", "").split("-")]
    except ValueError:
        return f"{e_range} EBC"
    lov = "-".join(f"{(p * 0.508 + 0.76) / 1.3546:.1f}".rstrip("0").rstrip(".") for p in parts)
    return f"{e_range} EBC ({lov} °L)"


# Per guide: file, page, filters (key, label), the spec lines shown on each row,
# the chips, the row title and the copy around the list.
GUIDES = {
    "yeast": dict(
        file="yeast.json", slug="yeast-strains-guide.html", noun="strains",
        title="Brewing Yeast Strains Guide | Craft Beer School",
        desc="Popular dry and liquid brewing yeasts compared: attenuation, temperature, flocculation and styles, from each maker's datasheet.",
        h1="Brewing yeast strains guide.", eyebrow="Ingredients · Yeast",
        lead="The yeasts craft brewers in India actually pitch, compared on the numbers that decide a beer: attenuation, "
             "fermentation temperature, flocculation and alcohol tolerance. Every figure comes from the maker's own datasheet.",
        filters=[("family", "All families"), ("maker", "All makers"), ("format", "Dry or liquid")],
        head=lambda r: (r["name"], r["maker"]),
        chips=lambda r: [r["family"], r["format"].capitalize()] + (["STA1 positive"] if r.get("sta1") else []),
        specs=lambda r: [("Attenuation", r.get("attenuation")), ("Temperature", temp(r.get("temp_c"))),
                         ("Flocculation", r.get("flocculation")), ("Alcohol tolerance", r.get("alcohol_tolerance")),
                         ("Species", r.get("species"))],
        course=("advanced-brewing-science-course.html", "Advanced Brewing Science",
                "Fermentation, yeast health and pitching rates are a full module of Advanced Brewing Science, 6 weeks, live online."),
        related=["dry-yeast-vs-liquid-yeast", "kveik-yeast-for-hot-climates", "pitching-yeast-properly", "ale-vs-lager-yeast"],
    ),
    "hops": dict(
        file="hops.json", slug="hops-guide.html", noun="varieties",
        title="Hop Varieties Guide for Brewers | Craft Beer School",
        desc="Popular hop varieties compared: alpha and beta acids, oil, aroma, styles and substitutes, from grower and merchant datasheets.",
        h1="Hop varieties guide.", eyebrow="Ingredients · Hops",
        lead="The hops craft brewers reach for most, from Saaz to Citra, compared on alpha acid, oil and aroma. "
             "Numbers come from grower and merchant datasheets and shift a little with every crop year.",
        filters=[("origin", "All origins"), ("purpose", "Any purpose")],
        head=lambda r: (r["name"], r["origin"]),
        chips=lambda r: [r["purpose"]],
        specs=lambda r: [("Alpha acid", r.get("alpha")), ("Beta acid", r.get("beta")),
                         ("Cohumulone", r.get("cohumulone")), ("Total oil", r.get("oil")),
                         ("Substitutes", ", ".join(r.get("substitutes") or []) or None)],
        course=("advanced-brewing-science-course.html", "Advanced Brewing Science",
                "Hop chemistry, timing and dry hopping are taught in Advanced Brewing Science, 6 weeks, live online."),
        related=["hop-varieties-for-beginners", "alpha-acids-explained", "dry-hopping-guide", "noble-hops-explained"],
    ),
    "malts": dict(
        file="malts.json", slug="malt-guide.html", noun="malts",
        title="Brewing Malt Guide for Brewers | Craft Beer School",
        desc="Base, caramel, kilned and roasted brewing malts compared: colour in EBC and Lovibond, usage rates and flavour, from maltster datasheets.",
        h1="Brewing malt guide.", eyebrow="Ingredients · Malt",
        lead="Base, caramel, kilned and roasted malts from the maltsters Indian brewers buy from, compared on colour, "
             "how much you can use and what each one tastes like. Every figure comes from the maltster's own spec sheet.",
        filters=[("family", "All families"), ("maltster", "All maltsters"), ("country", "All countries")],
        head=lambda r: (r["name"], r["maltster"]),
        chips=lambda r: [r["family"], r["country"]] + (["Has enzymes"] if r.get("diastatic") == "has enzymes" else []),
        specs=lambda r: [("Colour", ebc(r.get("colour_ebc"))), ("Usage", r.get("max_pct")), ("Note", r.get("note") or None)],
        course=("advanced-brewing-science-course.html", "Advanced Brewing Science",
                "Grist design, balancing base, caramel and roasted malts on purpose, is taught in Advanced Brewing Science, 6 weeks, live online."),
        related=["weyermann-malts-guide", "base-malts-explained", "crystal-and-caramel-malts", "roasted-malts-guide"],
    ),
}


def load(key):
    path = DATA / GUIDES[key]["file"]
    return json.loads(path.read_text()) if path.exists() else []


def _row(g, r):
    name, by = g["head"](r)
    chips = "".join(f'<span class="ig-chip">{E(c)}</span>' for c in g["chips"](r) if c)
    specs = "".join(f"<div><dt>{k}</dt><dd>{E(str(v))}</dd></div>" for k, v in g["specs"](r) if v)
    styles = ", ".join(r.get("styles") or [])
    extra = (f'<p class="ig-styles"><b>Styles:</b> {E(styles)}</p>' if styles else "")
    wey = (f' <a href="{E(r["weyermann_slug"])}.html">Full guide</a>' if r.get("weyermann_slug") else "")
    data = " ".join(f'data-{k}="{E(str(r.get(k) or ""))}"' for k, _ in g["filters"])
    q = " ".join(str(x) for x in [name, by, r.get("flavour") or r.get("aroma") or "", styles, *g["chips"](r)]).lower()
    return (f'<li class="ig-row" id="{E(r["id"])}" {data} data-q="{E(q)}">'
            f'<div class="ig-head"><h3>{E(name)} <span>{E(by)}</span></h3><div class="ig-chips">{chips}</div></div>'
            f'<p class="ig-desc">{E(r.get("flavour") or r.get("aroma") or "")}</p>'
            f'<dl class="ig-specs">{specs}</dl>{extra}'
            f'<p class="ig-src"><a href="{E(r["source"])}" rel="noopener nofollow" target="_blank">Datasheet</a>'
            f'<span>Checked {E(r.get("checked", ""))}</span>{wey}</p></li>')


def faqs(key, rows):
    if key == "yeast":
        hot = [r for r in rows if r.get("temp_c") and float(str(r["temp_c"]).split("-")[-1]) >= 35]
        names = ", ".join(f'{r["name"]} ({r["maker"]}, up to {str(r["temp_c"]).split("-")[-1]} °C)' for r in hot[:4])
        return [
            ("Which brewing yeast copes best with Indian heat?",
             f"Kveik strains are the ones whose makers publish ranges above 30 °C. In this guide: {names}. "
             "Clean American ale strains such as US-05 still need controlled fermentation around 18 to 22 °C for a clean result."),
            ("Dry or liquid yeast for brewing in India?",
             "Dry yeast tolerates shipping and storage far better, which matters when the cold chain is uncertain. "
             "Liquid yeast offers more strains but should travel and stay cold. Use it quickly."),
            ("What does STA1 positive mean?",
             "The strain carries a gene that lets it break down dextrins most yeasts leave behind, so it can ferment drier "
             "and keep fermenting in the package. Keep it on separate equipment from your other beers."),
        ]
    if key == "hops":
        return [
            ("Why do alpha acid figures vary?",
             "Alpha acid changes with variety, farm and crop year, so datasheets give a range. Use the figure on your own "
             "lot's certificate of analysis when you calculate bitterness."),
            ("How should hops be stored in India?",
             "Cold, dark and sealed without oxygen: vacuum or nitrogen-flushed packs in a freezer. Warm storage loses "
             "alpha acid and aroma fast."),
        ]
    return [
        ("What do EBC and Lovibond mean?",
         "Both measure malt colour. EBC is the European scale and Lovibond the American one. This guide shows both; "
         "beer colour itself is measured in EBC or SRM."),
        ("Which malts have their own enzymes?",
         "Base malts such as Pilsner, pale ale, Vienna and Munich carry the enzymes that convert starch in the mash. "
         "Most caramel and roasted malts do not, so they need a base malt alongside them."),
    ]


def graph_nodes(key):
    g, rows = GUIDES[key], load(key)
    url = f"{SITE}/{g['slug']}"
    return [{"@type": "ItemList", "@id": f"{url}#list", "name": g["h1"].rstrip("."), "numberOfItems": len(rows),
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": g["head"](r)[0],
                                  "url": f"{url}#{r['id']}"} for i, r in enumerate(rows)]},
            {"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs(key, rows)]}]


def page(key, titles):
    """titles: slug -> h1 of live guides, for the 'read next' links."""
    g, rows = GUIDES[key], load(key)
    selects = ""
    for k, label in g["filters"]:
        vals = sorted({str(r.get(k)) for r in rows if r.get(k)})
        opts = "".join(f'<option value="{E(v)}">{E(v.capitalize() if k == "format" else v)}</option>' for v in vals)
        selects += f'<label class="sr-only" for="ig-{k}">{label}</label><select id="ig-{k}" name="{k}"><option value="">{label}</option>{opts}</select>'
    faq_html = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs(key, rows))
    reads = "".join(f'<li><a href="{s}.html">{E(titles[s])}</a></li>' for s in g["related"] if s in titles)
    others = " · ".join(f'<a href="{o["slug"]}">{o["h1"].rstrip(".")}</a>' for k2, o in GUIDES.items() if k2 != key)
    href, cname, cbody = g["course"]
    return banner("Ingredients", g["eyebrow"], g["h1"], g["lead"]) + f"""
<section style="padding-block:2rem 0">
  <div class="wrap">
    <form class="finder ig-finder" id="ig-finder" role="search" action="{g['slug']}">
      {selects}
      <label class="sr-only" for="ig-q">Search</label>
      <input id="ig-q" name="q" type="search" placeholder="Name, flavour or style" autocomplete="off" />
      <button type="submit" class="btn btn-navy">Search</button>
    </form>
    <p class="f-count bd-count" id="ig-count" aria-live="polite">Showing all {len(rows)} {g['noun']}</p>
    <ol class="ig-list" id="ig-list">{"".join(_row(g, r) for r in rows)}</ol>
    <p class="bd-method">Figures are the maker's published values on the date checked and change with each crop or batch.
    Check the certificate of analysis that comes with your own lot. Also see: {others}.</p>
  </div>
</section>
<section class="tint">
  <div class="wrap bd-two">
    <div><span class="eyebrow">Questions</span><h2>Before you buy.</h2><div class="faq">{faq_html}</div></div>
    <div><span class="eyebrow">Read next</span><h2>Go deeper.</h2><ul class="checklist">{reads}</ul>
      <aside class="cta-inline" style="margin-top:1.5rem"><div><h3>{cname}</h3><p>{cbody}</p></div>
      <a class="btn btn-amber" href="{href}" data-cta="ingredients-{key}-course">See the syllabus</a></aside></div>
  </div>
</section>
<script>{JS.replace("FILTERS", json.dumps([k for k, _ in g["filters"]])).replace("NOUN", g["noun"]).replace("SLUG", g["slug"])}</script>"""


JS = """(()=>{
const f=document.getElementById('ig-finder'),rows=[...document.querySelectorAll('.ig-row')],count=document.getElementById('ig-count'),keys=FILTERS;
function apply(){
  const u=new URLSearchParams(location.search),q=(u.get('q')||'').trim().toLowerCase(),terms=q.split(/\\s+/).filter(Boolean);
  keys.forEach(k=>f[k].value=u.get(k)||'');f.q.value=u.get('q')||'';let n=0;
  rows.forEach(r=>{const ok=keys.every(k=>!u.get(k)||r.dataset[k]===u.get(k))&&terms.every(t=>r.dataset.q.includes(t));r.hidden=!ok;if(ok)n++});
  count.textContent=n===rows.length?`Showing all ${n} NOUN`:n?`Showing ${n} of ${rows.length} NOUN`:'Nothing matches. Try fewer words or another filter.';
}
f.addEventListener('submit',e=>{e.preventDefault();const x=new URLSearchParams();keys.forEach(k=>f[k].value&&x.set(k,f[k].value));f.q.value.trim()&&x.set('q',f.q.value.trim());history.replaceState(null,'','SLUG'+(x.toString()?'?'+x:''));apply()});
keys.forEach(k=>f[k].addEventListener('change',()=>f.requestSubmit()));apply();
})();"""
