# -*- coding: utf-8 -*-
"""Sponsored slots on guides and the advertise page (Ankur's request, 31 Oct 2026).

Suppliers of malt, hops, yeast, equipment, packaging and services sponsor the
guides their buyers read. One card per guide, clearly marked "Sponsored", never
inside the article text. Until a topic has a live sponsor, its guides carry a
small house card that points suppliers at advertise.html.

To add a sponsor, append to SPONSORS and rebuild. Audience figures stay None
until they are read from Google Analytics; the page never shows a guessed number.
"""
import datetime
import html

SLUG = "advertise.html"
ENQUIRY = "contact.html?course=Advertising%20and%20sponsorship#enroll"

# Topic groups a supplier can sponsor: (key, label, who buys it).
GROUPS = [
    ("packaging", "Packaging", "Can, bottle, label, keg and closure suppliers"),
    ("ingredients", "Malt, hops and yeast", "Maltsters, hop merchants, yeast labs and ingredient distributors"),
    ("brewing", "Brewing process and equipment", "Brewhouse, cellar, lab, cleaning and cooling equipment makers"),
    ("distilling", "Distilling", "Still makers, cask and botanical suppliers, neutral spirit producers"),
    ("wine", "Wine", "Winery equipment, barrel, yeast and packaging suppliers"),
    ("business", "Drinks business", "Software, finance, legal, logistics and insurance providers for drinks businesses"),
]
PACKAGING_WORDS = ("can-", "-can", "bottl", "label", "keg", "packag", "closure", "crown-cap", "glass")
CAT_GROUP = {"Ingredients": "ingredients", "Brewing science": "brewing", "Brewing basics": "brewing",
             "Whisky": "distilling", "Wine": "wine", "Business": "business", "Consultancy": "business",
             "Drinks business": "business"}

# Live sponsors. Each: {"name", "url", "line", "groups": [keys], "until": "YYYY-MM-DD", "label": button text}.
SPONSORS = []

# Read from Google Analytics before filling in, e.g. {"users": "...", "views": "...", "period": "last 90 days"}.
AUDIENCE = None


def group_of(article):
    slug = article["slug"]
    if any(w in slug for w in PACKAGING_WORDS):
        return "packaging"
    return CAT_GROUP.get(article["cat"])


def _live(today=None):
    today = today or datetime.date.today().isoformat()
    return [s for s in SPONSORS if s["until"] >= today]


def card(article):
    """The one sponsor card for a guide, or the house card, or nothing."""
    g = group_of(article)
    if not g:
        return ""
    hit = next((s for s in _live() if g in s["groups"]), None)
    if hit:
        return (f'<aside class="sponsor-card" aria-label="Sponsored"><span class="sponsor-tag">Sponsored</span>'
                f'<div><h3>{html.escape(hit["name"])}</h3><p>{html.escape(hit["line"])}</p></div>'
                f'<a class="btn btn-ghost" href="{html.escape(hit["url"])}" target="_blank" rel="sponsored noopener" '
                f'data-cta="sponsor-{g}">{html.escape(hit.get("label", "Visit the website"))}</a></aside>')
    label = dict((k, l) for k, l, _ in GROUPS)[g]
    return (f'<aside class="sponsor-card house" aria-label="Advertise with us"><span class="sponsor-tag">Advertise</span>'
            f'<div><h3>Reach the people reading this guide</h3><p>Suppliers in {label.lower()} can sponsor the guides their buyers read.</p></div>'
            f'<a class="btn btn-ghost" href="{SLUG}" data-cta="sponsor-house-{g}">See advertising options</a></aside>')


def page(articles):
    """advertise.html: who reads the guides, the slots on offer and how to enquire."""
    from pages_a import banner
    counts = {k: 0 for k, *_ in GROUPS}
    for a in articles:
        g = group_of(a)
        if g:
            counts[g] += 1
    rows = "".join(f'<tr><th scope="row">{label}</th><td>{counts[k]:,}</td><td>{who}</td></tr>'
                   for k, label, who in GROUPS)
    if AUDIENCE:
        audience = (f'<p class="lead">{AUDIENCE["users"]} readers and {AUDIENCE["views"]} page views in the '
                    f'{AUDIENCE["period"]}, from Google Analytics.</p>')
    else:
        audience = '<p class="lead">Visitor and page view figures from Google Analytics are available on request.</p>'
    body = banner("Advertise", "Advertise with us", "Reach the people who brew, distil and buy.",
                  f"{len(articles):,} free guides read by brewers, distillers, winemakers, founders and drinks teams in India and around the world.") + f"""
<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Audience</span><h2>Who reads the guides</h2>
    {audience}
    <p>Readers come to learn a job: homebrewers moving up, professional brewers and distillers, founders planning a brewery, winery or distillery. Teams inside drinks companies read them too. These are the people who choose malt, hops, yeast, equipment and packaging.</p></div>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Topics you can sponsor</span><h2>One sponsor per topic, on every guide in it</h2></div>
    <div class="table-wrap"><table class="ad-table">
      <thead><tr><th scope="col">Topic</th><th scope="col">Guides</th><th scope="col">Who it suits</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    <p style="margin-top:1rem">Your card sits near the end of each guide in the topic, marked "Sponsored", with your name, one line and a link. We never place sponsors inside the article text. Guides stay independent: a sponsor does not change what we write.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Also available</span><h2>Other ways to work with us</h2></div>
    <ul class="checklist">
      <li>Sponsoring a guide series, for example a set of guides on one ingredient or process</li>
      <li>Sponsoring a free course or a tasting session</li>
      <li>Market entry into India for ingredient, equipment and packaging companies</li>
    </ul>
    <aside class="cta-inline" style="margin-top:2rem">
      <div><h3>Ask about advertising</h3><p>Tell us what you sell and who you want to reach. We will reply with the topics, the reach and the terms.</p></div>
      <a class="btn btn-amber" href="{ENQUIRY}" data-cta="advertise-enquiry">Ask about advertising</a>
    </aside>
  </div>
</section>"""
    return ("Advertise with us | Craft Beer School",
            "Sponsor the Craft Beer School guides read by brewers, distillers, winemakers and drinks founders. Topics, reach and how to enquire.",
            "about", body)
