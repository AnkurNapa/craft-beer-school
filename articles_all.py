# -*- coding: utf-8 -*-
"""Every article on the site: the eight hand-written guides plus the seeded
library in content/articles/*.json. build.py and seo.py both read from here so
the pages, sitemap and JSON-LD can never disagree about what exists.
"""
import json
import pathlib

import articles_a
import articles_b
import stories

HERE = pathlib.Path(__file__).parent
_PLAN = {p["slug"]: p for p in json.loads((HERE / "content/plan.json").read_text())}

_seeded = [json.loads(f.read_text()) for f in sorted((HERE / "content/articles").glob("*.json"))]

# Newest first, the way a reader expects a journal to run.
ARTICLES = sorted(articles_a.ARTICLES_A + articles_b.ARTICLES_B + stories.STORIES + _seeded,
                  key=lambda a: a["updated"], reverse=True)

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
]
