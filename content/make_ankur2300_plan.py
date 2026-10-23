"""One-off: Ankur's 2,300 (2,000 beer guides plus 300 whisky guides), all bylined to Ankur Napa alone.

Reads the topic files (segment|stage|course|h1 under "## <cat>" headings), drops any topic whose slug
or wording repeats a live guide, picks three related guides by shared words and appends the rows to
plan.json in batches of 20. Rerunning skips rows already in the plan.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATE = "2026-10-23"
BY = "mentor-ankur-napa.html"
BATCH_SIZE = 20
WHISKY_CAP = 300
BEER_CAP = 2000
SEG = {"BL": "Beer lovers", "HB": "Homebrewers", "PB": "Professional brewers", "FO": "Founders",
       "CT": "Corporate teams", "DP": "Drinks producers", "CC": "Career changers"}
STAGE = {"a": "awareness", "c": "consideration", "d": "decision"}
COURSE = {"F": "brewing-fundamentals-course.html", "A": "advanced-brewing-science-course.html",
          "Y": "style-specialization-course.html", "S": "sensory-evaluation-course.html",
          "M": "brewery-business-management-course.html", "D": "craft-distilling-course.html",
          "C": "contact.html?course=Corporate%20training#enroll", "N": "non-alcoholic-beer-course.html"}
STOP = set("a an and the of in on for to with at from by or is it its your you how what why when "
           "which versus explained guide beer beers brewing brew".split())
NEAR_DUP = 0.75  # shared share of all significant words in two titles before one counts as a repeat


def slugify(h1, limit=60):
    s = re.sub(r"[^a-z0-9]+", "-", h1.lower().replace("°c", "c")).strip("-")
    if len(s) <= limit:
        return s
    return s[:limit].rsplit("-", 1)[0]


def words(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP}


def read_topics(paths):
    rows = []
    for path in paths:
        cat = None
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line.startswith("## "):
                cat = line[3:].strip()
            elif line.count("|") == 3 and cat:
                seg, stage, course, h1 = (x.strip() for x in line.split("|"))
                if seg not in SEG or stage not in STAGE or course not in COURSE:
                    sys.exit(f"bad line in {path}: {line}")
                rows.append({"cat": cat, "segment": SEG[seg], "stage": STAGE[stage],
                             "course": COURSE[course], "h1": h1})
    return rows


def is_near_dup(w, seen):
    return any(w and len(w & s) / len(w | s) >= NEAR_DUP for s in seen if s)


def related_for(row, pool):
    w = words(row["h1"])
    same = [p for p in pool if p["cat"] == row["cat"] and p["slug"] != row["slug"]]
    ranked = sorted(same, key=lambda p: -len(w & words(p["h1"])))
    return [p["slug"] for p in ranked[:3]]


def main():
    plan_path = os.path.join(HERE, "plan.json")
    plan = json.load(open(plan_path, encoding="utf-8"))
    taken = {p["slug"] for p in plan} | {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, "*.html"))}
    seen = [words(p["h1"]) for p in plan]
    # The style reference pages are not in plan.json; a Styles guide naming every core word of one repeats it.
    styles = [words(re.sub(r"\b(style|german|english|american|belgian|british|irish|french|contemporary|european)\b", "",
                           os.path.basename(f)[6:-5].replace("-", " ")))
              for f in glob.glob(os.path.join(HERE, "styles", "style-*.json"))]
    paths = [os.path.join(HERE, "new600_topics.txt")] + sorted(glob.glob(os.path.join(HERE, "new_beer_topics_*.txt")))
    ours = {p["slug"] for p in plan if p.get("batch", "").startswith("ankur2300")}
    whisky = sum(p["cat"] == "Whisky" for p in plan if p["slug"] in ours)
    beer = len(ours) - whisky
    added, dropped = [], []
    for row in read_topics(paths):
        if row["cat"] == "Whisky" and whisky >= WHISKY_CAP or row["cat"] != "Whisky" and beer >= BEER_CAP:
            continue
        slug = slugify(row["h1"])
        if slug in ours:
            continue
        w = words(row["h1"])
        repeats_style = row["cat"] == "Styles" and any(core and (core == w or (len(core) > 1 and core <= w)) for core in styles)
        if slug in taken or is_near_dup(w, seen) or repeats_style:
            dropped.append(row["h1"])
            continue
        whisky += row["cat"] == "Whisky"
        beer += row["cat"] != "Whisky"
        taken.add(slug)
        seen.append(w)
        added.append({"slug": slug, **row})
    # Related cards stay inside the category, so whisky guides point at whisky guides.
    pool = [p for p in plan] + added
    first = len([p for p in plan if p.get("batch", "").startswith("ankur2300")])
    for i, row in enumerate(added):
        row["related"] = related_for(row, pool)
        row["batch"] = f"ankur2300-{(first + i) // BATCH_SIZE + 1:03d}"
        row["date"] = DATE
        row["by"] = BY
    if "--dry" not in sys.argv:
        json.dump(plan + added, open(plan_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"added {len(added)} (beer total {beer}, whisky total {whisky}), dropped {len(dropped)} repeats")
    for h in dropped:
        print("  dropped:", h)


if __name__ == "__main__":
    main()
