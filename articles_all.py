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
_seeded = [{**a, **{k: _PLAN[a["slug"]][k] for k in ("also", "wheel", "malt") if _PLAN.get(a["slug"], {}).get(k)}}
           for a in _seeded]

# Byline for every guide that is not a guest story: Chatty on the creative
# side (brand, packaging, marketing), Ankur on everything technical.
import mentors
_PEOPLE = {m["slug"]: {"name": m["name"], "role": m["role"], "photo": m["img"], "href": m["slug"]}
           for m in mentors.MENTORS}
_CREATIVE = {"brand", "design", "social", "influencers", "storytelling", "naming", "merchandise", "events",
             "marketing", "positioning", "launching"}


def expert(a):
    if _PLAN.get(a["slug"], {}).get("by"):
        return _PEOPLE[_PLAN[a["slug"]]["by"]]
    creative = a["cat"] == "Branding" or bool(_CREATIVE & set(a["slug"].split("-")))
    return _PEOPLE["mentor-chatty-girija.html" if creative else "mentor-ankur-napa.html"]


_seeded = [{**a, "expert": expert(a)} for a in _seeded]
_hand = [a if a.get("author") else {**a, "expert": expert(a)}
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
