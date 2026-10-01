"""Build content/styles_plan.json: the facts (names, families, ranges) for the Style Library.
Ranges are industry-standard numbers; every word of prose is written fresh in content/styles/*.json.
Source facts: vault Beer/CraftBeer.com Beer Styles/craftbeer_styles.json."""
import json, math, pathlib, re

SRC = pathlib.Path.home() / "Documents/obsidian/Beer/CraftBeer.com Beer Styles/craftbeer_styles.json"
FAMILY = {"Pale Ales": "Pale ales", "India Pale Ales": "IPAs", "Pilseners and Pale Lagers": "Pale lagers",
          "Dark Lagers": "Amber and dark lagers", "Wheat Beers": "Wheat beers", "Belgian Styles": "Belgian ales",
          "Bocks": "Bocks", "Brown Ales": "Brown ales", "Porters": "Porters", "Stouts": "Stouts",
          "Strong Ales": "Strong ales", "Scottish-Style Ales": "Scottish ales", "Hybrid Beers": "Hybrids",
          "Wild/Sour Beers": "Sours and wild beers", "Specialty Beers": "Speciality beers"}
GUIDE = {  # style name -> existing long guide slug on the site
    "German-Style Pilsner": "pilsner-style-guide", "Bohemian-Style Pilsener": "pilsner-style-guide",
    "German-Style Helles": "helles-style-guide", "German-Style Marzen / Oktoberfest": "marzen-and-oktoberfest",
    "Vienna-Style Lager": "vienna-lager", "German-Style Bock": "bock-and-doppelbock",
    "German-Style Doppelbock": "bock-and-doppelbock", "German-Style Maibock": "bock-and-doppelbock",
    "German-Style Dunkel": "dunkel-and-schwarzbier", "German-Style Schwarzbier": "dunkel-and-schwarzbier",
    "American Lager": "american-light-lager", "German-Style Hefeweizen": "hefeweizen-guide",
    "Belgian-Style Witbier": "witbier-guide", "Berliner-Style Weisse": "berliner-weisse",
    "Contemporary Gose": "gose-guide", "German-Style Kolsch": "kolsch-guide", "German-Style Altbier": "altbier-guide",
    "English-Style Bitter": "english-bitter", "English-Style Pale Ale (ESB)": "english-bitter",
    "English-Style Mild": "english-mild", "English-Style Brown Ale": "english-brown-ale",
    "English-Style Brown Porter": "porter-guide", "Robust Porter": "porter-guide",
    "Irish-Style Dry Stout": "dry-stout-guide", "American Imperial Stout": "imperial-stout-guide",
    "English-Style Sweet Stout (Milk Stout)": "milk-and-oatmeal-stout", "English-Style Oatmeal Stout": "milk-and-oatmeal-stout",
    "American IPA": "west-coast-ipa", "New England IPA": "new-england-ipa", "English-Style IPA": "english-ipa",
    "Imperial India Pale Ale": "double-ipa", "Session Beer": "session-ipa", "American Pale Ale": "pale-ale-guide",
    "American Amber Ale": "amber-and-red-ales", "Irish-Style Red Beer": "amber-and-red-ales",
    "Belgian-Style Saison": "saison-guide", "Belgian-Style Dubbel": "belgian-dubbel", "Belgian-Style Tripel": "belgian-tripel",
    "Belgian-Style Quadrupel": "belgian-strong-dark-ale", "Belgian-Style Lambic/Gueuze": "lambic-and-gueuze",
    "Belgian-Style Fruit Lambic": "lambic-and-gueuze", "Belgian-Style Flanders": "flanders-red-ale",
    "British-Style Barley Wine Ale": "barleywine-guide", "American Barley Wine": "barleywine-guide",
    "Smoke Beer": "smoked-beer-rauchbier", "Smoke Porter": "smoked-beer-rauchbier",
}


def slug(n):
    return "style-" + re.sub(r"[^a-z0-9]+", "-", n.lower().replace("/", " ")).strip("-")


def vec(r):  # normalised position for "similar styles"
    f = lambda a, b, s: ((a + b) / 2 / s) if a is not None and b is not None else 0.5
    return (f(r["srm_min"], r["srm_max"], 40), f(r["ibu_min"], r["ibu_max"], 100), f(r["abv_min"], r["abv_max"], 12))


rows = json.loads(SRC.read_text())
plan = []
for r in rows:
    near = sorted((x for x in rows if x is not r),
                  key=lambda x: math.dist(vec(r), vec(x)) - (0.15 if x["category"] == r["category"] else 0))
    rng = lambda k, u: f"{r[k + '_min']:g}-{r[k + '_max']:g}{u}" if r[k + "_min"] is not None else "Varies"
    plan.append({"slug": slug(r["name"]), "name": r["name"], "family": FAMILY[r["category"]],
                 "srm": rng("srm", ""), "ibu": rng("ibu", ""), "abv": rng("abv", "%"),
                 "guide": GUIDE.get(r["name"]), "similar": [slug(x["name"]) for x in near[:3]]})
# Source quirks: session beer colour follows its base style; very dark stouts are open-ended at the top.
FIX = {"Session Beer": {"srm": "Varies"}, "English-Style Sweet Stout (Milk Stout)": {"srm": "40+"},
       "American Imperial Stout": {"srm": "40+"}, "American Imperial Porter": {"srm": "40+"},
       "Smoke Porter": {"srm": "20+"},
       "Baltic-Style Porter": {"srm": "17-30"}}  # source "39-40" is a slider artefact; BJCP 2021 range
for row in plan:
    row.update(FIX.get(row["name"], {}))
plan.sort(key=lambda p: (p["family"], p["name"]))
out = pathlib.Path(__file__).parent / "styles_plan.json"
out.write_text(json.dumps(plan, indent=1, ensure_ascii=False))
assert len(plan) == 80 and len({p["slug"] for p in plan}) == 80
print(len(plan), "styles,", sum(1 for p in plan if p["guide"]), "with a long guide")
