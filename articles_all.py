# -*- coding: utf-8 -*-
"""Every article on the site: the eight hand-written guides plus the seeded
library in content/articles/*.json. build.py and seo.py both read from here so
the pages, sitemap and JSON-LD can never disagree about what exists.
"""
import datetime
import json
import os
import pathlib

import articles_a
import articles_b
import stories

HERE = pathlib.Path(__file__).parent
_PLAN = {p["slug"]: p for p in json.loads((HERE / "content/plan.json").read_text())}

_seeded = [json.loads(f.read_text()) for f in sorted((HERE / "content/articles").glob("*.json"))]
# A plan row may name a second course for readers learning for themselves.
# Weyermann malt guides carry the malt's aroma wheel image.
_seeded = [{**a, **{k: _PLAN[a["slug"]][k] for k in ("also", "wheel", "malt", "photos", "banner") if _PLAN.get(a["slug"], {}).get(k)}}
           for a in _seeded]

# Byline for every guide that is not a guest story: Chatty on the creative
# side (brand, packaging, marketing), Ankur on everything technical.
import mentors
_PEOPLE = {m["slug"]: {"name": m["name"], "role": m["role"], "photo": m["img"], "href": m["slug"]}
           for m in mentors.MENTORS}
_CREATIVE = {"brand", "design", "social", "influencers", "storytelling", "naming", "merchandise", "events",
             "marketing", "positioning", "launching"}


# Bylines (Ankur's rule, 12 October 2026): Ankur leads every beer guide, because
# Craft Beer School is his school and his idea.
#   food and pairing guides       Ankur Napa and Anu Rao
#   beer with AI, data or digital Ankur Napa
#   brand and marketing guides    Ankur Napa and Chatty Girija
#   consultancy guides            Rahul Baliyan only
#   every other beer guide        Ankur Napa and Rahul Baliyan
# A plan row's "by" set to Chatty (pieces about Ankur) still wins. Chatty is the
# point of contact on every guide.
ANKUR, RAHUL, ANU, CHATTY = ("mentor-ankur-napa.html", "mentor-rahul-baliyan.html",
                             "mentor-anu-rao.html", "mentor-chatty-girija.html")
_FOOD = {"pairing", "food", "biryani", "dosa", "cheese", "dessert", "menu", "chettinad", "dishes", "cuisine"}
_TECH = {"ai", "data", "power", "bi", "tableau", "dashboard", "dashboards", "digital", "analytics", "analysts",
         "kpi", "kpis", "sensors", "software", "calculators", "forecasting", "machine", "copilot"}


def authors(a):
    """Byline slugs for a guide, first author first."""
    plan = _PLAN.get(a["slug"], {})
    if plan.get("by") == CHATTY:
        return [CHATTY]
    words = set(a["slug"].split("-")) | set(a["h1"].lower().replace(",", " ").replace(":", " ").split())
    if _FOOD & words:
        return [ANKUR, ANU]
    if _TECH & words:
        return [ANKUR]
    if a["cat"] == "Consultancy":
        return [RAHUL]
    if a["cat"] == "Branding" or _CREATIVE & set(a["slug"].split("-")):
        return [ANKUR, CHATTY]
    return [ANKUR, RAHUL]


def expert(a):
    return _PEOPLE[authors(a)[0]]


def _with_bylines(a):
    names = authors(a)
    return {**a, "expert": _PEOPLE[names[0]], "co_expert": _PEOPLE[names[1]] if len(names) > 1 else None,
            "contact": _PEOPLE[CHATTY]}

_seeded = [_with_bylines(a) for a in _seeded]
_hand = [a if a.get("author") else _with_bylines(a)
         for a in articles_a.ARTICLES_A + articles_b.ARTICLES_B + stories.STORIES]

# Newest first, the way a reader expects a journal to run.
ALL_ARTICLES = sorted(_hand + _seeded,
                      key=lambda a: a["updated"], reverse=True)

# Guides dated in the future are written but not live: each one appears on its
# own date (India time) when the daily-publish workflow rebuilds the site.
# PUBLISH_DATE=YYYY-MM-DD previews the site as it will look on that day.
TODAY = os.environ.get("PUBLISH_DATE") or datetime.datetime.now(
    datetime.timezone(datetime.timedelta(hours=5, minutes=30))).date().isoformat()
ARTICLES = [a for a in ALL_ARTICLES if a["updated"] <= TODAY]

# Reader segment per article, which drives the blog index and the funnel.
SEGMENT = {p["slug"]: p["segment"] for p in _PLAN.values()}
SEGMENT.update({
    "what-is-craft-beer": "Beer lovers", "beer-styles-guide": "Beer lovers",
    "how-to-taste-beer": "Beer lovers", "beer-off-flavours": "Professional brewers",
    "craft-beer-in-india": "Founders", "start-a-microbrewery-india": "Founders",
    "become-a-brewer-india": "Career changers", "brewing-for-india": "Professional brewers",
    "the-man-who-took-off-his-tie": "Career changers",
})

# (segment, who it is for, course it feeds). Order is the order on the blog.
SEGMENTS = [
    ("Beer lovers", "New to craft beer? Styles, tasting and pairing in plain English.", "sensory-evaluation-course.html", "Sensory Evaluation"),
    ("Homebrewers", "Brewing at home and want every batch better than the last.", "brewing-fundamentals-course.html", "Brewing Fundamentals"),
    ("Professional brewers", "Running a brewhouse and chasing consistency.", "advanced-brewing-science-course.html", "Advanced Brewing Science"),
    ("Founders", "Planning a brewery or brewpub in India.", "brewery-business-management-course.html", "Brewery Business Management"),
    ("Brand builders", "Naming, packaging and selling beer people remember.", "beer-branding-packaging-course.html", "Beer Branding &amp; Packaging"),
    ("Career changers", "Turning a love of beer into a job.", "brewing-fundamentals-course.html", "Brewing Fundamentals"),
    ("Drinks producers", "Running a brewery, cidery, distillery or winery and want it to do better.", "contact.html?course=Brewery%20consultancy#enroll", "Brewery consultancy"),
    ("Corporate teams", "Working in a beer, wine or spirits company and want to know the product.", "for-companies.html#training", "Corporate training"),
]
