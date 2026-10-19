"""India craft brewery directory: breweries.html.

Data is copied from the Tap List India project (~/Documents/india-craft-beer/data),
where every venue carries its sources and a last-checked date. Refresh with
`cp ~/Documents/india-craft-beer/data/{venues,beers}.json content/breweries/`.

The whole list is rendered as static HTML so search and answer engines can read it;
the script on top only filters rows and drives the map.
"""
import collections
import html
import json
import pathlib

from pages_a import banner

DATA = pathlib.Path(__file__).parent / "content" / "breweries"
SITE = "https://craftbeerschool.in"

STATE_OF = {
    "Bengaluru": "Karnataka", "Mysuru": "Karnataka", "Mangaluru": "Karnataka",
    "Pune": "Maharashtra", "Mumbai": "Maharashtra", "Nashik": "Maharashtra", "Nagpur": "Maharashtra",
    "Chhatrapati Sambhajinagar": "Maharashtra", "Hyderabad": "Telangana", "Vijayawada": "Andhra Pradesh",
    "Visakhapatnam": "Andhra Pradesh", "Puducherry": "Puducherry", "Gurugram": "Haryana", "Faridabad": "Haryana",
    "Chandigarh": "Chandigarh", "Delhi": "Delhi", "Noida": "Uttar Pradesh", "Lucknow": "Uttar Pradesh",
    "Jaipur": "Rajasthan", "Udaipur": "Rajasthan", "Amritsar": "Punjab", "Ludhiana": "Punjab",
    "Shimla": "Himachal Pradesh", "Dehradun": "Uttarakhand", "Kolkata": "West Bengal", "Bhubaneswar": "Odisha",
    "Guwahati": "Assam", "Shillong": "Meghalaya", "Gangtok": "Sikkim", "Goa": "Goa",
}
KIND = {"brewpub": "Brewpub", "microbrewery": "Microbrewery", "taproom": "Taproom", "packaged": "Packaged brand", "unknown": "Brewery"}
E = html.escape

# Pinned Leaflet 1.9.4 + markercluster 1.5.3 with SRI, shared with hopping.py.
LEAFLET = """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" integrity="sha384-c6Rcwz4e4CITMbu/NBmnNS8yN2sC3cUElMEMfP3vqqKFp7GOYaaBBCqmaWBjmkjb" crossorigin="anonymous">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/MarkerCluster.css" integrity="sha384-pmjIAcz2bAn0xukfxADbZIb3t8oRT9Sv0rvO+BR5Csr6Dhqq+nZs59P0pPKQJkEV" crossorigin="anonymous">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/MarkerCluster.Default.css" integrity="sha384-wgw+aLYNQ7dlhK47ZPK7FRACiq7ROZwgFNg0m04avm4CaXS+Z9Y7nMu8yNjBKYC+" crossorigin="anonymous">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js" integrity="sha384-NElt3Op+9NBMCYaef5HxeJmU4Xeard/Lku8ek6hoPTvYkQPh3zLIrJP7KiRocsxO" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/leaflet.markercluster.js" integrity="sha384-eXVCORTRlv4FUUgS/xmOyr66XBVraen8ATNLMESp92FKXLAMiKkerixTiBvXriZr" crossorigin="anonymous"></script>"""


def load():
    venues = json.loads((DATA / "venues.json").read_text())
    beers = json.loads((DATA / "beers.json").read_text())
    on_tap = collections.defaultdict(list)
    for b in beers:
        for vid in b["venues"]:
            on_tap[vid].append(b)
    hist = _history()
    rows = []
    for v in venues:
        city = v.get("city")
        rows.append({**v, **hist.pop(v["id"], {}), "state": STATE_OF.get(city, "") if city else "",
                     "where": city or ", ".join(v.get("cities", [])),
                     "beers": sorted(on_tap[v["id"]], key=lambda b: b["name"])})
    for h in hist.values():  # closed breweries found by the research, not in the live list
        if h["id"].startswith("closed-") and h.get("city"):
            rows.append({**h, "kind": "unknown", "state": STATE_OF.get(h["city"], ""), "where": h["city"], "beers": []})
    return sorted(rows, key=lambda r: (r["where"], r["name"]))


HISTORY_KEYS = ("founded", "status", "closed", "group", "outlets", "lineage")


def _history():
    """History research (content/breweries/research/out-*.json), keyed by venue id.
    A row with no source is ignored entirely: we print nothing we cannot cite."""
    out = {}
    for f in sorted((DATA / "research").glob("out-*.json")):
        for h in json.loads(f.read_text()):
            if not h.get("sources"):
                continue
            keep = {k: h.get(k) for k in HISTORY_KEYS if h.get(k) not in (None, "", "unknown")}
            out[h["id"]] = {**({k: h[k] for k in ("id", "name", "city", "area") if h.get(k)}),
                            **keep, "history_sources": h["sources"]}
    return out


def is_closed(r):
    return r.get("status") == "permanently closed"


def _row(r):
    beers = "".join(f'<li>{E(b["name"])} <span>{E(b["style"])}</span></li>' for b in r["beers"])
    beer_block = (f'<details class="bd-beers"><summary>{len(r["beers"])} beer{"s" if len(r["beers"]) != 1 else ""} listed</summary>'
                  f'<ul>{beers}</ul></details>') if r["beers"] else '<p class="bd-none">No beers listed yet.</p>'
    place = E(", ".join(x for x in (r.get("area"), r["where"]) if x))
    sold = "Sold in " if not r.get("city") else ""
    maps = (f'<a href="https://www.google.com/maps/search/?api=1&query={r["lat"]},{r["lng"]}" rel="noopener" target="_blank">Directions</a>'
            if r.get("lat") is not None else "")
    src = r["sources"][0] if r.get("sources") else ""
    src_link = f'<a href="{E(src)}" rel="noopener nofollow" target="_blank">Source</a>' if src else ""
    checked = f'<span>Checked {E(r["checked"])}</span>' if r.get("checked") else ""
    search = " ".join([r["name"], r["where"], r.get("area") or "", r["state"], KIND[r["kind"]]]
                      + [b["name"] + " " + b["style"] for b in r["beers"]]).lower()
    closed = is_closed(r)
    geo = f' data-lat="{r["lat"]}" data-lng="{r["lng"]}"' if r.get("lat") is not None and not closed else ""
    status = ("closed" if closed else "temporarily closed" if r.get("status") == "temporarily closed"
              else "open" if r.get("status") == "open" else "unverified")
    badge = {"closed": '<span class="bd-status bd-st-closed">Reported closed</span>',
             "temporarily closed": '<span class="bd-status bd-st-temp">Temporarily closed</span>'}.get(status, "")
    bits = []
    if r.get("founded"):
        bits.append(f'Opened {E(str(r["founded"]))}')
    if closed:
        bits.append(f'Closed {E(str(r["closed"]))}' if r.get("closed") else "Reported closed")
    if r.get("group") and r["group"] != r["name"]:
        bits.append(f'Part of {E(r["group"])}' + (f' ({r["outlets"]} outlets)' if r.get("outlets") else ""))
    elif r.get("outlets"):
        bits.append(f'{r["outlets"]} outlets')
    hist_src = (r.get("history_sources") or [None])[0]
    history = (f'<p class="bd-hist">{" · ".join(bits)}'
               + (f'. {E(r["lineage"])}' if r.get("lineage") else "")
               + (f' <a href="{E(hist_src)}" rel="noopener nofollow" target="_blank">Source</a>' if hist_src else "")
               + "</p>") if bits or r.get("lineage") else ""
    if closed:
        beer_block = ""
    return (f'<li class="bd-row{" bd-closed" if closed else ""}" id="b-{E(r["id"])}" data-state="{E(r["state"])}" data-kind="{r["kind"]}" '
            f'data-status="{status}" data-q="{E(search + " " + (r.get("group") or "").lower())}"{geo}>'
            f'<div class="bd-head"><h3>{E(r["name"])}</h3><span>{badge}<span class="bd-kind bd-{r["kind"]}">{KIND[r["kind"]]}</span></span></div>'
            f'<p class="bd-place">{sold}{place}</p>{history}'
            f'{beer_block}<p class="bd-links">{maps}{src_link}{checked}</p></li>')


def _jsonld(rows, faqs):
    items = [{"@type": "ListItem", "position": i + 1, "item": {
        "@type": "Brewery", "name": r["name"],
        **({"address": {"@type": "PostalAddress", "streetAddress": r["address"], "addressLocality": r["city"],
                        "addressRegion": r["state"], "addressCountry": "IN"}} if r.get("address") else {}),
        **({"geo": {"@type": "GeoCoordinates", "latitude": r["lat"], "longitude": r["lng"]}} if r.get("lat") is not None else {}),
        **({"sameAs": r["sources"][0]} if r.get("sources") else {})}} for i, r in enumerate([x for x in rows if not is_closed(x)])]
    graph = [{"@type": "ItemList", "@id": f"{SITE}/breweries.html#list", "name": "Craft breweries in India",
              "numberOfItems": len(items), "itemListElement": items},
             {"@type": "FAQPage", "@id": f"{SITE}/breweries.html#faq", "mainEntity": [
                 {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]
    return graph


def stats(rows):
    rows = [r for r in rows if not is_closed(r)]
    cities = collections.Counter(r["city"] for r in rows if r.get("city"))
    states = {r["state"] for r in rows if r["state"]}
    beers = {b["id"] for r in rows for b in r["beers"]}
    kinds = collections.Counter(r["kind"] for r in rows)
    newest = max((r["checked"] for r in rows if r.get("checked")), default="")
    return cities, states, beers, kinds, newest


def _faqs(rows, cities, states, top):
    return [
        ("How many craft breweries are there in India?",
         f"This directory lists {sum(not is_closed(r) for r in rows)} craft breweries, brewpubs, taprooms and packaged craft beer brands in "
         f"{len(cities)} cities across {len(states)} states and union territories, each with a source and a last-checked date. "
         "Venues open and close often, so treat any count as a snapshot."),
        ("Which Indian city has the most craft breweries?",
         f"Bengaluru, with {cities['Bengaluru']} venues in this directory. The next cities are {', '.join(f'{c} ({n})' for c, n in top[1:])}."),
        ("What is the difference between a brewpub and a microbrewery?",
         "A brewpub brews beer on site and serves it there, usually with food. A microbrewery is a small brewery that may "
         "package or supply beer beyond its own premises. Licence categories and names differ by state."),
        ("How do I get a brewery added or corrected?",
         "Send us the brewery name, city and a public source such as its website or menu through the contact form. We "
         "will check it and update the listing."),
    ]


def graph_nodes():
    """ItemList of Brewery entities plus the FAQ, merged into the page's single JSON-LD block by seo.py."""
    rows = load()
    cities, states, _, _, _ = stats(rows)
    return _jsonld(rows, _faqs(rows, cities, states, cities.most_common(5)))


def page():
    rows = load()
    cities, states, beers, kinds, newest = stats(rows)
    top = cities.most_common(5)
    top_txt = ", ".join(f"{c} ({n})" for c, n in top)
    faqs = _faqs(rows, cities, states, top)
    states_opts = "".join(f'<option value="{E(s)}">{E(s)}</option>' for s in sorted(states))
    kind_opts = "".join(f'<option value="{k}">{v}</option>' for k, v in KIND.items())
    city_rows = "".join(f'<tr><th scope="row"><button type="button" class="bd-city" data-city="{E(c)}">{E(c)}</button></th>'
                        f'<td>{E(STATE_OF.get(c, ""))}</td><td>{n}</td></tr>' for c, n in cities.most_common())
    faq_html = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs)
    return f"""
{banner("Breweries", "Directory · India", "India craft brewery directory.",
         "Every craft brewery, brewpub and taproom we can verify, on one map. Search by brewery, beer, style or city. "
         f"The busiest beer cities are {E(top_txt)}.")}
<section class="bd-stats-wrap" style="padding-block:1.5rem 0">
  <div class="wrap bd-stats">
    <div><b>{sum(not is_closed(r) for r in rows)}</b><span>Breweries and brands</span></div>
    <div><b>{len(cities)}</b><span>Cities</span></div>
    <div><b>{len(states)}</b><span>States and UTs</span></div>
    <div><b>{len(beers)}</b><span>Beers listed</span></div>
    <div><b>{sum(is_closed(r) for r in rows)}</b><span>Reported closed</span></div>
  </div>
</section>
<section style="padding-block:2rem 0">
  <div class="wrap">
    <form class="finder ig-finder" id="bd-finder" role="search" action="breweries.html">
      <label class="sr-only" for="bd-state">State</label>
      <select id="bd-state" name="state"><option value="">All states</option>{states_opts}</select>
      <label class="sr-only" for="bd-kind">Type</label>
      <select id="bd-kind" name="kind" class="bd-kind-select"><option value="">All types</option>{kind_opts}</select>
      <label class="sr-only" for="bd-status">Status</label>
      <select id="bd-status" name="status"><option value="">Open and unverified</option><option value="closed">Reported closed</option><option value="all">All, including closed</option></select>
      <label class="sr-only" for="bd-q">Search breweries</label>
      <input id="bd-q" name="q" type="search" placeholder="Brewery, beer, style or city" autocomplete="off" />
      <button type="submit" class="btn btn-navy">Search</button>
    </form>
    <p class="f-count bd-count" id="bd-count" aria-live="polite">Showing all {sum(not is_closed(r) for r in rows)} open and unverified breweries</p>
    <div class="bd-split">
      <div class="bd-map-wrap"><div id="bd-map" role="region" aria-label="Map of breweries"></div>
        <p class="bd-attrib">Pins from each brewery's public listing. Packaged brands have no pin. Planning a night out? <a href="brewery-hopping-india.html">See the brewery hopping trails</a>.</p></div>
      <ol class="bd-list" id="bd-list">{"".join(_row(r) for r in rows)}</ol>
    </div>
  </div>
</section>
<section class="tint">
  <div class="wrap bd-two">
    <div>
      <span class="eyebrow">City by city</span>
      <h2>Where India brews.</h2>
      <table class="bd-table"><thead><tr><th scope="col">City</th><th scope="col">State</th><th scope="col">Venues</th></tr></thead>
      <tbody>{city_rows}</tbody></table>
    </div>
    <div>
      <span class="eyebrow">Questions</span>
      <h2>About the directory.</h2>
      <div class="faq">{faq_html}</div>
      <p class="bd-method">Compiled from brewery websites, menus and public listings, each linked from its row.
      Last checked {E(newest)}. Spotted something out of date? <a href="contact.html#enroll">Tell us</a>.</p>
    </div>
  </div>
</section>
<section class="cta">
  <div class="wrap" style="text-align:center">
    <h2>Want to brew at one of these one day?</h2>
    <p class="lead" style="margin-inline:auto">Our in-person courses run in Pune, Delhi, Gurugram and Bengaluru, four of the busiest beer cities on this map.</p>
    <a class="btn btn-amber" href="in-person-brewing-courses-pune-delhi-gurugram-bengaluru.html" data-cta="breweries-in-person">See the in-person courses</a>
  </div>
</section>
{LEAFLET}
<script>{JS}</script>"""


JS = """(()=>{
const f=document.getElementById('bd-finder'),rows=[...document.querySelectorAll('.bd-row')],count=document.getElementById('bd-count');
const pins=new Map();let map,layer;
if(window.L){
  map=L.map('bd-map',{scrollWheelZoom:false}).setView([22.5,79],5);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'&copy; OpenStreetMap contributors'}).addTo(map);
  layer=L.markerClusterGroup({showCoverageOnHover:false});map.addLayer(layer);
  rows.forEach(r=>{if(!r.dataset.lat)return;const m=L.marker([+r.dataset.lat,+r.dataset.lng]);
    const h=r.querySelector('h3').textContent,p=r.querySelector('.bd-place').textContent;
    m.bindPopup(Object.assign(document.createElement('div'),{innerHTML:'<b></b><br><span></span>'}));
    m.on('popupopen',e=>{const d=e.popup.getContent();d.querySelector('b').textContent=h;d.querySelector('span').textContent=p});
    m.on('click',()=>r.scrollIntoView({block:'nearest',behavior:'smooth'}));pins.set(r,m)});
  rows.forEach(r=>r.querySelector('h3').addEventListener('click',()=>{const m=pins.get(r);if(m)layer.zoomToShowLayer(m,()=>m.openPopup())}));
}
function apply(){
  const u=new URLSearchParams(location.search),s=u.get('state')||'',k=u.get('kind')||'',st=u.get('status')||'',q=(u.get('q')||'').trim().toLowerCase();
  f.state.value=s;f.kind.value=k;f.status.value=st;f.q.value=u.get('q')||'';
  const terms=q.split(/\\s+/).filter(Boolean);let n=0;const shown=[];
  rows.forEach(r=>{const c=r.dataset.status==='closed',ok=(st==='all'||(st==='closed'?c:!c))&&(!s||r.dataset.state===s)&&(!k||r.dataset.kind===k)&&terms.every(t=>r.dataset.q.includes(t));r.hidden=!ok;if(ok){n++;if(pins.has(r))shown.push(pins.get(r))}});
  const none=!(s||k||q||st);count.textContent=none?`Showing all ${n} open and unverified breweries`:n?`Showing ${n} breweries`:'No breweries match. Try a city, a style such as IPA or fewer words.';
  if(layer){layer.clearLayers();layer.addLayers(shown);if(shown.length&&(s||k||q))map.fitBounds(L.featureGroup(shown).getBounds(),{padding:[30,30],maxZoom:13});else if(!(s||k||q))map.setView([22.5,79],5)}
}
function go(x){history.replaceState(null,'','breweries.html'+(x.toString()?'?'+x:''));apply()}
f.addEventListener('submit',e=>{e.preventDefault();const x=new URLSearchParams();['state','kind','status'].forEach(n=>f[n].value&&x.set(n,f[n].value));f.q.value.trim()&&x.set('q',f.q.value.trim());go(x)});
f.state.addEventListener('change',()=>f.requestSubmit());f.kind.addEventListener('change',()=>f.requestSubmit());f.status.addEventListener('change',()=>f.requestSubmit());
document.querySelectorAll('.bd-city').forEach(b=>b.addEventListener('click',()=>{go(new URLSearchParams({q:b.dataset.city}));f.scrollIntoView({behavior:'smooth'})}));
apply();
})();"""
