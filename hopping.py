"""Brewery hopping trails: brewery-hopping-india.html plus one page per city.

Trails are built from the directory (breweries.load()): pinned venues only, closed
ones dropped when the history research has marked them. Each trail starts where
venues are densest and walks to the nearest unvisited stop, so a trail stays in
one part of town. Distances are straight-line, not road distance.
"""
import html
import json
import math

import breweries
from pages_a import banner

E = html.escape
MIN_VENUES = 5      # a city needs this many pinned venues to get its own page
STOPS = 4           # stops per trail
MAX_HOP_KM = 6.0    # never send people further than this between two stops
MAX_TRAILS = 3


def km(a, b):
    """Great-circle distance between two venues in km."""
    la1, lo1, la2, lo2 = map(math.radians, (a["lat"], a["lng"], b["lat"], b["lng"]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def trails(venues):
    """Greedy trails: seed at the venue with most neighbours within 3 km, then
    nearest neighbour until STOPS or no stop within MAX_HOP_KM."""
    left = list(venues)
    out = []
    while left and len(out) < MAX_TRAILS:
        seed = max(left, key=lambda v: (sum(km(v, w) <= 3 for w in left), v["name"]))
        trail = [seed]
        left.remove(seed)
        while len(trail) < STOPS and left:
            nxt = min(left, key=lambda w: km(trail[-1], w))
            if km(trail[-1], nxt) > MAX_HOP_KM:
                break
            trail.append(nxt)
            left.remove(nxt)
        if len(trail) >= 3:
            out.append(trail)
    return out


def _slug(city):
    return "brewery-hopping-" + city.lower().replace(" ", "-") + ".html"


def cities():
    rows = [r for r in breweries.load() if r.get("lat") is not None and r.get("city")
            and r.get("status") not in ("permanently closed", "temporarily closed")]
    by = {}
    for r in rows:
        by.setdefault(r["city"], []).append(r)
    return {c: v for c, v in sorted(by.items(), key=lambda kv: -len(kv[1]))
            if len(v) >= MIN_VENUES and trails(v)}  # spread-out cities with no walkable trail are skipped


def _area(trail):
    areas = [v.get("area") for v in trail if v.get("area")]
    return max(set(areas), key=areas.count).split(",")[0] if areas else trail[0]["city"]


def _stop(i, v, prev):
    hop = f'<span class="hop-km">{km(prev, v):.1f} km from the last stop</span>' if prev else '<span class="hop-km">Start here</span>'
    beers = ", ".join(f'{b["name"]} ({b["style"]})' for b in v["beers"][:4])
    maps = f'https://www.google.com/maps/search/?api=1&query={v["lat"]},{v["lng"]}'
    return (f'<li class="hop-stop"><span class="hop-n">{i}</span><div><h4>{E(v["name"])}</h4>'
            f'<p class="bd-place">{E(", ".join(x for x in (v.get("area"), v["city"]) if x))} · {breweries.KIND[v["kind"]]}</p>'
            f'{hop}{f"<p class=hop-beers>Try: {E(beers)}</p>" if beers else ""}'
            f'<p class="bd-links"><a href="{maps}" target="_blank" rel="noopener">Directions</a>'
            f'<a href="breweries.html?q={E(v["name"].split(" (")[0])}">In the directory</a></p></div></li>')


def city_page(city, venues):
    ts = trails(venues)
    blocks, geo = [], []
    for n, t in enumerate(ts, 1):
        total = sum(km(a, b) for a, b in zip(t, t[1:]))
        stops = "".join(_stop(i, v, t[i - 2] if i > 1 else None) for i, v in enumerate(t, 1))
        blocks.append(f'<section class="hop-trail" id="trail-{n}"><h3>Trail {n}: {E(_area(t))}</h3>'
                      f'<p class="hop-meta">{len(t)} stops · about {total:.1f} km between them, straight line</p><ol>{stops}</ol></section>')
        geo.append([[v["lat"], v["lng"], v["name"]] for v in t])
    state = breweries.STATE_OF.get(city, "")
    return banner(f'<a href="brewery-hopping-india.html">Brewery hopping</a> / {E(city)}', f"Brewery hopping · {E(state)}",
                  f"Brewery hopping in {E(city)}.",
                  f"{len(ts)} trail{'s' if len(ts) != 1 else ''} through {E(city)}'s {len(venues)} craft breweries and brewpubs, "
                  "grouped so each one stays in one part of town. Pick one trail per evening.") + f"""
<section style="padding-block:2rem">
  <div class="wrap bd-split hop-split">
    <div class="bd-map-wrap"><div id="bd-map" role="region" aria-label="Map of the {E(city)} trails"></div>
      <p class="bd-attrib">Numbers follow the trail order. Distances are straight-line; roads are longer.</p></div>
    <div>{"".join(blocks)}</div>
  </div>
</section>
{_safety()}
{_leaflet()}
<script>const TRAILS={json.dumps(geo, ensure_ascii=False)};{CITY_JS}</script>"""


def _safety():
    return """<section class="tint"><div class="wrap bd-two">
  <div><span class="eyebrow">Before you go</span><h2>Hop safely.</h2><ul class="checklist">
    <li>Never drive. Book a cab or use the metro between stops, and plan the ride home first.</li>
    <li>Order tasters or a sampler paddle, not full pints, at every stop.</li>
    <li>A glass of water between beers and food at the first stop.</li>
    <li>Carry ID: the legal drinking age differs between states.</li>
    <li>Call ahead: hours, holidays and dry days change, and venues open and close.</li></ul></div>
  <div><span class="eyebrow">Learn while you drink</span><h2>Taste like a brewer.</h2>
    <p>A hopping evening is the cheapest tasting class there is. Our <a href="how-to-taste-beer.html">tasting guide</a> gives you a method to use at each stop.</p>
    <aside class="cta-inline" style="margin-top:1rem"><div><h3>Hands-on courses in four cities</h3><p>Our 1-day and 1-month in-person courses run in Pune, Delhi, Gurugram and Bengaluru.</p></div>
    <a class="btn btn-amber" href="in-person-brewing-courses-pune-delhi-gurugram-bengaluru.html" data-cta="hopping-in-person">See the courses</a></aside></div>
</div></section>"""


def _leaflet():
    return breweries.LEAFLET


def hub():
    cs = cities()
    cards = "".join(f'<a class="hop-card" href="{_slug(c)}"><b>{E(c)}</b><span>{len(v)} breweries · '
                    f'{len(trails(v))} trail{"s" if len(trails(v)) != 1 else ""}</span></a>' for c, v in cs.items())
    return banner("Brewery hopping", "Brewery hopping · India", "Brewery hopping trails across India.",
                  "Walkable and short-cab trails through India's busiest craft beer cities, built from our brewery directory "
                  "and drawn on the map.") + f"""
<section style="padding-block:2rem">
  <div class="wrap"><div class="hop-cards">{cards}</div>
  <p class="bd-method">Only cities with at least {MIN_VENUES} mapped breweries get trails. Is your city missing a brewery?
  <a href="breweries.html">Check the directory</a> and tell us.</p></div>
</section>
{_safety()}"""


def pages():
    out = {"brewery-hopping-india.html": ("Brewery Hopping Trails in India | Craft Beer School",
                                         "Brewery hopping trails for India's craft beer cities, mapped stop by stop with distances and beers to try.",
                                         "", hub())}
    for c, v in cities().items():
        out[_slug(c)] = (f"Brewery Hopping in {c} | Craft Beer School",
                         f"Brewery hopping trails in {c}: craft breweries and brewpubs grouped by area, mapped stop by stop with beers to try.",
                         "", city_page(c, v))
    return out


CITY_JS = """(()=>{if(!window.L)return;
const map=L.map('bd-map',{scrollWheelZoom:false});
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'&copy; OpenStreetMap contributors'}).addTo(map);
const colours=['#d9862a','#0a6d84','#2f6b2a'],all=[];
TRAILS.forEach((t,ti)=>{const pts=t.map(s=>[s[0],s[1]]);all.push(...pts);
  L.polyline(pts,{color:colours[ti%3],weight:4,opacity:.8,dashArray:'6 6'}).addTo(map);
  t.forEach((s,i)=>{const m=L.marker([s[0],s[1]],{icon:L.divIcon({className:'hop-pin',html:'<span style=\"background:'+colours[ti%3]+'\">'+(i+1)+'</span>',iconSize:[28,28]})}).addTo(map);
    m.bindTooltip(document.createTextNode('Trail '+(ti+1)+', stop '+(i+1)+': '+s[2]).textContent)})});
if(all.length)map.fitBounds(all,{padding:[30,30]});
})();"""


if __name__ == "__main__":
    a = {"lat": 12.9716, "lng": 77.5946}
    b = {"lat": 12.9784, "lng": 77.6408}
    assert 4.9 < km(a, b) < 5.1, km(a, b)   # MG Road to Indiranagar, about 5 km
    pts = [{"lat": 12.97 + i * 0.005, "lng": 77.6, "name": str(i)} for i in range(5)] + \
          [{"lat": 13.30, "lng": 77.6, "name": "far"}]
    t = trails(pts)
    assert t and len(t[0]) == STOPS and all(v["name"] != "far" for v in t[0]), t
    print("hopping ok")
