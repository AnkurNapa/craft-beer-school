#!/usr/bin/env python3
"""Gate for Style Library cards in content/styles/*.json. Run: python3 validate_styles.py [slug ...]

Same house rules as validate_articles.py, plus an originality check: no run of
7+ words may match the CraftBeer.com source text we researched from.
"""
import json, pathlib, re, sys

from validate_articles import AI_TELLS, BANNED, US

HERE = pathlib.Path(__file__).parent
PLAN = {p["slug"]: p for p in json.load(open(HERE / "content/styles_plan.json"))}
SRC = pathlib.Path.home() / "Documents/obsidian/Beer/CraftBeer.com Beer Styles/craftbeer_styles.json"
KEYS = {"slug", "name", "family", "title", "desc", "tagline", "tastes", "profile", "glass", "serve_c",
        "in_india", "pairings", "examples", "examples_note"}
PROFILE = {"look", "aroma_flavour", "mouthfeel", "ingredients"}
GLASSES = {"Pint", "Nonic pint", "Tulip", "Snifter", "Pilsner glass", "Stange", "Weizen glass", "Goblet",
           "Teku", "Willi becher", "Thistle", "Stemmed glass"}
NGRAM = 7


def words(s):
    return re.findall(r"[a-z0-9']+", re.sub(r"<[^>]+>", " ", s).lower())


def grams(ws):
    return {tuple(ws[i:i + NGRAM]) for i in range(len(ws) - NGRAM + 1)}


SOURCE_GRAMS = set()
if SRC.exists():
    for r in json.loads(SRC.read_text()):
        SOURCE_GRAMS |= grams(words(" ".join(str(v) for k, v in r.items() if isinstance(v, str))))


def text_of(s):
    parts = [s["name"], s["title"], s["desc"], s["tagline"], s["tastes"], s["in_india"], s["examples_note"]]
    parts += list(s["profile"].values()) + [p["food"] + " " + p["why"] for p in s["pairings"]]
    parts += [e["beer"] + " " + e["brewery"] for e in s["examples"]]
    return "\n".join(parts)


def check(path):
    try:
        s = json.loads(path.read_text())
    except Exception as e:
        return [f"bad JSON: {e}"]
    p = PLAN.get(path.stem)
    if not p:
        return ["slug not in styles_plan"]
    if set(s) != KEYS:
        return [f"keys differ: missing {KEYS - set(s)}, extra {set(s) - KEYS}"]
    errs = []
    if s["slug"] != path.stem: errs.append("slug does not match file name")
    if s["family"] != p["family"]: errs.append(f"family should be {p['family']}")
    if not s["title"].endswith(" | Craft Beer School") or len(s["title"]) > 60:
        errs.append(f"title must end ' | Craft Beer School' and be <= 60 chars (is {len(s['title'])})")
    if not 50 <= len(s["desc"]) <= 160: errs.append(f"desc is {len(s['desc'])} chars, need 50-160")
    if len(s["tagline"]) > 120: errs.append("tagline over 120 chars")
    n = len(words(s["tastes"]))
    if not 120 <= n <= 220: errs.append(f"tastes is {n} words, need 120-220")
    n = len(words(s["in_india"]))
    if not 50 <= n <= 120: errs.append(f"in_india is {n} words, need 50-120")
    if not isinstance(s["profile"], dict) or set(s["profile"]) != PROFILE:
        errs.append(f"profile keys must be {sorted(PROFILE)}")
    elif any(len(words(v)) > 40 or not v.strip() for v in s["profile"].values()):
        errs.append("each profile line must be 1-40 words")
    if s["glass"] not in GLASSES: errs.append(f"glass must be one of {sorted(GLASSES)}")
    if not re.fullmatch(r"\d{1,2}-\d{1,2}", s["serve_c"]): errs.append("serve_c must look like '7-10'")
    if not 3 <= len(s["pairings"]) <= 4 or any(set(x) != {"food", "why"} for x in s["pairings"]):
        errs.append("pairings: 3-4 items of {food, why}")
    if len(s["examples"]) > 3 or any(set(x) != {"beer", "brewery", "source"} or not x["source"].startswith("http")
                                     for x in s["examples"]):
        errs.append("examples: 0-3 items of {beer, brewery, source(url)}")
    if not s["examples"] and not s["examples_note"].strip(): errs.append("no examples, so examples_note is required")
    for tag in set(re.findall(r"</?([a-z0-9]+)", s["tastes"] + s["in_india"])):
        if tag not in {"p", "strong", "em", "br"}: errs.append(f"tag <{tag}> not allowed")
    t = text_of(s)
    for ch, name in BANNED.items():
        if ch in t: errs.append(f"banned {name}")
    for w in sorted({m.group(0) for m in US.finditer(t)}): errs.append(f"US spelling: {w}")
    for w in sorted({m.group(0).lower() for m in AI_TELLS.finditer(t)}): errs.append(f"AI tell: {w}")
    copied = grams(words(t)) & SOURCE_GRAMS
    if copied: errs.append(f"copied from source: {' '.join(sorted(copied)[0])!r} (+{len(copied) - 1} more)")
    return errs


def main(slugs):
    files = [HERE / f"content/styles/{s}.json" for s in slugs] if slugs else [
        HERE / f"content/styles/{s}.json" for s in PLAN]
    bad = 0
    for f in files:
        if not f.exists():
            print(f"MISSING {f.stem}"); bad += 1; continue
        errs = check(f)
        if errs:
            bad += 1
            print(f"FAIL {f.stem}: " + "; ".join(errs))
    print(f"{len(files) - bad}/{len(files)} styles pass")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
