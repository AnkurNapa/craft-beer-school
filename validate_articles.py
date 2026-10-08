#!/usr/bin/env python3
"""Gate for seeded articles in content/articles/*.json. Run: python3 validate_articles.py [slug ...]

Checks what a reviewer would otherwise catch by hand: schema, SEO lengths,
banned punctuation, American spellings, stray tags, dead internal links and a
CTA that does not point at the course the plan assigned.
"""
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
TODAY = __import__("datetime").date.today().isoformat()
PLAN = {p["slug"]: p for p in json.load(open(HERE / "content/plan.json"))}
EXISTING = {"what-is-craft-beer", "beer-styles-guide", "how-to-taste-beer", "beer-off-flavours",
            "craft-beer-in-india", "start-a-microbrewery-india", "become-a-brewer-india", "brewing-for-india"}
PAGES = {"courses.html", "contact.html", "resources.html", "faq.html", "about.html", "blog.html", "for-companies.html",
         *[p["course"] for p in PLAN.values()]}
KEYS = {"slug", "cat", "h1", "title", "desc", "teaser", "standfirst", "read", "updated", "updated_label",
        "sections", "faqs", "cta", "related"}
BANNED = {"—": "em dash", "–": "en dash", "“": "curly quote", "”": "curly quote",
          "‘": "curly quote", "’": "curly quote", "  ": "double space"}
US = re.compile(r"\b(colou?r(?<!colour)|flavor\w*|favor\w*|center|fiber|liter|analyz\w+|optimiz\w+|"
                r"organiz\w+|recogniz\w+|realiz\w+|minimiz\w+|maximiz\w+|sanitiz\w+|stabiliz\w+|pasteuriz\w+|caramelize\w*|"
                r"characterize\w*|specializ\w+|carbonization|oxidiz\w+|standardiz\w+|utiliz\w+|catalog|gray|aluminum|"
                r"program(?!me)\b|mold|odor|behavior|labeled|traveled)\b", re.I)
AI_TELLS = re.compile(r"\b(delve|tapestry|landscape|seamless\w*|unlock\w*|empower\w*|leverag\w+|pivotal|crucial|"
                      r"embark|elevate|game.changer|in conclusion|it's important to note|testament|realm|"
                      r"navigat(e|ing) the (world|complexities))\b", re.I)
ALLOWED_TAGS = {"p", "strong", "em", "ul", "ol", "li", "a", "br"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December"]


def text_of(a):
    parts = [a["h1"], a["title"], a["desc"], a["teaser"], a["standfirst"], a["cta"]["title"], a["cta"]["body"]]
    if "cta_inline" in a:
        parts += [a["cta_inline"]["title"], a["cta_inline"]["body"]]
    parts += [h + " " + b for h, b in a["sections"]] + [q + " " + ans for q, ans in a["faqs"]]
    return "\n".join(parts)


def check(path):
    errs = []
    try:
        a = json.loads(path.read_text())
    except Exception as e:
        return [f"bad JSON: {e}"]
    slug = path.stem
    p = PLAN.get(slug)
    if not p:
        return ["slug not in plan"]
    if not KEYS <= set(a) <= KEYS | {"cta_inline"}:
        errs.append(f"keys differ: missing {KEYS - set(a)}, extra {set(a) - KEYS - {'cta_inline'}}")
        return errs
    if "cta_inline" in a and set(a["cta_inline"]) != {"title", "body", "href", "label"}:
        errs.append("cta_inline keys must be title, body, href, label")
    if a["slug"] != slug: errs.append("slug field does not match file name")
    if a["cat"] != p["cat"]: errs.append(f"cat should be {p['cat']}")
    if a["updated"] != p["date"]: errs.append(f"updated should be {p['date']}")
    y, m, _ = p["date"].split("-")
    if a["updated_label"] != f"{MONTHS[int(m) - 1]} {y}": errs.append("updated_label does not match date")
    if not a["title"].endswith(" | Craft Beer School") or len(a["title"]) > 60:
        errs.append(f"title must end ' | Craft Beer School' and be <= 60 chars (is {len(a['title'])})")
    if not 50 <= len(a["desc"]) <= 160: errs.append(f"desc is {len(a['desc'])} chars, need 50-160")
    if not 5 <= len(a["sections"]) <= 8: errs.append(f"{len(a['sections'])} sections, need 5-8")
    if not 3 <= len(a["faqs"]) <= 4: errs.append(f"{len(a['faqs'])} faqs, need 3-4")
    body = " ".join(b for _, b in a["sections"])
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    if not 650 <= words <= 1200: errs.append(f"body is {words} words, need 650-1200")
    if a["read"] != f"{max(3, round(words / 200))} min": errs.append(f"read should be '{max(3, round(words / 200))} min'")
    if set(a["cta"]) != {"title", "body", "href", "label"}: errs.append("cta keys must be title, body, href, label")
    elif a["cta"]["href"] != p["course"]: errs.append(f"cta href must be {p['course']}")
    if a["related"] != p["related"]: errs.append(f"related must be {p['related']}")
    for tag in set(re.findall(r"</?([a-z0-9]+)", body + " ".join(x for _, x in a["faqs"]))):
        if tag not in ALLOWED_TAGS: errs.append(f"tag <{tag}> not allowed")
    for href in re.findall(r'href="([^"]+)"', body):
        target = href.split("#")[0]
        if target.startswith("http"): continue
        if target not in PAGES and target[:-5] not in PLAN and target[:-5] not in EXISTING:
            errs.append(f"dead internal link {href}")
        # A guide goes live on its plan date, so a link only breaks if its target publishes after the
        # linking guide does. Backdated archive guides may link to anything already live today.
        elif target[:-5] in PLAN and PLAN[target[:-5]]["date"] > max(p["date"], TODAY):
            errs.append(f"link {href} is not live yet on {max(p['date'], TODAY)}")
    t = text_of(a)
    for ch, name in BANNED.items():
        if ch in t: errs.append(f"banned {name}")
    for w in sorted({m.group(0) for m in US.finditer(t)}): errs.append(f"US spelling: {w}")
    for w in sorted({m.group(0).lower() for m in AI_TELLS.finditer(t)}): errs.append(f"AI tell: {w}")
    return errs


def main(slugs):
    files = [HERE / f"content/articles/{s}.json" for s in slugs] if slugs else sorted((HERE / "content/articles").glob("*.json"))
    bad = 0
    for f in files:
        if not f.exists():
            print(f"MISSING {f.stem}"); bad += 1; continue
        errs = check(f)
        if errs:
            bad += 1
            print(f"FAIL {f.stem}: " + "; ".join(errs))
    print(f"{len(files) - bad}/{len(files)} articles pass")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
