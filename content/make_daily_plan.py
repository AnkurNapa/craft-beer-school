"""The daily drip: 90 guides dated one a day from 3 October to 31 December 2026.
articles_all.py hides any guide dated after today (IST) and the daily-publish
workflow rebuilds each morning, so each one goes live on its own date.
Rerun is safe: it replaces its own rows and leaves every other row alone."""
import collections, datetime, json, pathlib, re

from make_corporate_plan import ALSO

here = pathlib.Path(__file__).parent
START, DAYS = datetime.date(2026, 10, 3), 90
R, A = "mentor-rahul-baliyan.html", "mentor-ankur-napa.html"
STAGE = {"a": "awareness", "c": "consideration", "d": "decision"}

# segment -> rows of slug|h1|cat|stage, optionally |author mentor slug
PLAN = {
"Beer lovers": """beer-and-biryani-pairing|Which beer goes with biryani|Tasting|a
beer-with-south-indian-food|Beer with dosa, appam and Chettinad food|Tasting|a
beer-with-street-food|Beer and Indian street food: chaat, pav bhaji and momos|Tasting|a
beer-and-tandoori-pairing|Beer with tandoori food and kebabs|Tasting|a
beer-and-pizza-burger-pairing|Beer with pizza and burgers|Tasting|a
diwali-beer-pairing|Beer with Diwali snacks and sweets|Tasting|a
winter-beers-guide|Warming beers for an Indian winter|Styles|a
christmas-and-new-year-beers|Christmas and New Year beers worth seeking out|Styles|a
craft-beer-gift-guide|Gifting craft beer: what to buy a beer lover|Tasting|a
reading-a-taproom-menu|How to read a taproom menu|Tasting|a
beer-flight-guide|How to order and taste a beer flight|Tasting|c
why-craft-beer-costs-more|Why craft beer costs more than mass-market lager|Tasting|a
low-alcohol-craft-beer|Low alcohol craft beer: what to look for|Styles|a
sour-beer-for-beginners|Sour beer for beginners|Styles|a
hazy-vs-clear-beer|Hazy or clear: what cloudiness tells you about a beer|Tasting|c
growlers-and-crowlers|Growlers and crowlers: taking taproom beer home|Tasting|a
beer-and-spicy-food-heat|Why some beers make spicy food hotter|Tasting|c
how-hops-change-aroma|Why one hop smells of mango and another of pine|Ingredients|a""",
"Homebrewers": """brewing-with-packaged-drinking-water|Brewing with packaged drinking water in India|Ingredients|c
first-all-grain-brew-day|Your first all-grain brew day, hour by hour|Brewing basics|c
brewing-a-lager-at-home|Brewing a lager at home without a cellar|Brewing basics|c
small-batch-brewing|Small batch brewing: 3 to 5 litre batches|Brewing basics|c
designing-your-first-ipa-recipe|Designing your first IPA recipe|Brewing basics|c
water-salts-for-homebrewers|Gypsum, calcium chloride and other water salts for homebrewers|Ingredients|c
reading-a-hop-packet|Reading a hop packet: alpha acids, oils and harvest year|Ingredients|c
fixing-homebrew-carbonation|Flat or gushing homebrew: fixing carbonation|Brewing science|c
brewing-a-wheat-beer-at-home|Brewing a wheat beer at home|Brewing basics|c
brewing-a-stout-at-home|Brewing a stout at home|Brewing basics|c
entering-a-homebrew-competition|Entering your first homebrew competition|Brewing basics|d
fermenting-through-an-indian-summer|Fermenting through an Indian summer|Brewing science|c
adding-coffee-to-beer|Adding coffee to beer|Ingredients|c
brewing-with-jaggery|Brewing with jaggery|Ingredients|c
kettle-souring-at-home|Kettle souring at home|Brewing science|c""",
"Professional brewers": """yeast-viability-and-vitality|Yeast viability and vitality: counting cells properly|Brewing science|c
co2-in-the-brewery|CO2 in the brewery: buying, using and recovering it|Brewing science|c
bright-beer-tank-management|Running bright beer tanks well|Brewing science|c
centrifuge-vs-filtration|Centrifuge or filter: clarifying beer at scale|Brewing science|c
measuring-carbonation|Measuring carbonation in tank and package|Brewing science|c
boil-evaporation-rate|Setting the right boil evaporation rate|Brewing science|c
malt-certificate-of-analysis|Reading a malt certificate of analysis|Ingredients|c
hop-oil-chemistry|Hop oils: myrcene, linalool and geraniol in the glass|Ingredients|c
reading-a-fermentation-curve|Reading a fermentation gravity curve|Brewing science|c
sulphur-in-lager-fermentation|Sulphur in lager fermentation|Brewing science|c
biotransformation-in-hazy-ipa|Biotransformation in hazy IPA|Brewing science|c
microbiology-plating-small-brewery|Microbiology plating in a small brewery lab|Brewing science|c
high-gravity-brewing-and-dilution|High gravity brewing and dilution|Brewing science|c
keg-washing-and-filling|Keg washing and filling done properly|Brewing science|c
lager-yeast-strains-compared|Lager yeast strains compared|Ingredients|c""",
"Founders": """brewpub-food-menu-and-margins|Food at a brewpub: menu design and margins|Business|c
brewpub-layout-kitchen-brewhouse-bar|Laying out a brewpub: kitchen, brewhouse and bar|Business|c
insuring-a-brewery-india|Insuring a brewery in India|Business|c
planning-a-brewpub-opening-month|Planning a brewpub's opening month|Business|d
pos-and-inventory-software-for-brewpubs|POS and inventory software for brewpubs|Business|c
brewery-partner-agreements|Co-founder and partner agreements for a brewery|Business|d
leasing-space-for-a-brewpub|Leasing space for a brewpub|Business|d
takeaway-beer-rules-india|Takeaway beer and growler rules in India|Business|c
brewery-cash-flow-first-year|Cash flow in a brewery's first year|Business|c
hiring-your-first-head-brewer|Hiring your first head brewer|Business|d""",
"Brand builders": """photographing-beer-for-instagram|Photographing beer for Instagram|Branding|c
taproom-design-that-sells|Taproom design that sells beer|Branding|c
collaboration-brews|Collaboration brews: why breweries brew together|Branding|a
building-a-beer-community|Building a beer club and community|Branding|c
writing-tasting-notes-that-sell|Writing tasting notes that sell|Branding|c
what-a-brewery-website-needs|What a brewery website needs|Branding|c
festive-season-beer-marketing|Festive season marketing for breweries|Branding|c
entering-beer-awards-as-a-brand|Entering beer awards as a brand|Branding|d""",
"Career changers": """brewery-internship-india|Getting a brewery internship in India|Careers|d
brewery-quality-control-career|A career in brewery quality control|Careers|c
cellar-and-packaging-jobs|Cellar and packaging jobs: where most brewers start|Careers|c
studying-brewing-abroad-or-in-india|Studying brewing abroad or in India|Careers|d
writing-about-beer-for-a-living|Writing about beer for a living|Careers|a
brewer-cv-and-interview|A brewer's CV and interview: what gets you hired|Careers|d
working-in-an-indian-distillery|Working in an Indian distillery|Careers|c
women-in-indian-brewing|Women in Indian brewing: getting in and getting on|Careers|c""",
"Drinks producers": f"""planning-a-brewpub-year-around-indian-seasons|Planning a brewpub's year around Indian seasons|Consultancy|c|{A}
reducing-beer-loss-at-the-bar|Reducing beer loss at the bar and taproom|Consultancy|c|{A}
setting-up-a-yeast-management-programme|Setting up a yeast management programme|Consultancy|c|{R}
writing-brewhouse-sops|Writing brewhouse SOPs that people follow|Consultancy|c|{R}
training-a-new-assistant-brewer|Training a new assistant brewer in 30 days|Consultancy|c|{R}
cutting-power-and-water-in-a-brewpub|Cutting power and water use in a brewpub|Consultancy|c|{A}
costing-a-recipe-before-you-brew|Costing a recipe before you brew it|Consultancy|c|{A}
preparing-a-brewery-for-inspection|Preparing a brewery for an excise or safety inspection|Consultancy|d|{R}""",
"Corporate teams": """beer-seasonality-for-demand-planners|Beer seasonality explained for demand planners|Beer for teams|c
barley-and-malt-for-procurement-teams|Barley and malt for procurement teams|Beer for teams|c
how-a-beer-batch-is-released|How a batch of beer is released for sale|Beer for teams|a
whisky-age-statements-explained|Whisky age statements explained|Whisky|a
peat-and-smoke-in-whisky|Peat and smoke in whisky|Whisky|a
how-sparkling-wine-gets-its-bubbles|How sparkling wine gets its bubbles|Wine|a
sweetness-acidity-and-tannin-in-wine|Sweetness, acidity and tannin in wine|Wine|a
gin-vodka-and-rum-for-new-joiners|Gin, vodka and rum for new joiners|Drinks business|a""",
}
# Seasonal pieces land on the right week; everything else fills round-robin.
PIN = {"festive-season-beer-marketing": "2026-10-12", "diwali-beer-pairing": "2026-11-02",
       "winter-beers-guide": "2026-12-01", "craft-beer-gift-guide": "2026-12-10",
       "christmas-and-new-year-beers": "2026-12-18"}
# Hand-picked related guides where headline words do not overlap enough.
RELATED = {
 "beer-with-south-indian-food": ["indian-food-and-beer-pairing", "beer-and-food-pairing-basics", "brewing-with-indian-spices"],
 "beer-with-street-food": ["indian-food-and-beer-pairing", "beer-and-food-pairing-basics", "beer-serving-temperature"],
 "beer-and-tandoori-pairing": ["indian-food-and-beer-pairing", "beer-and-food-pairing-basics", "bitterness-perception"],
 "beer-and-spicy-food-heat": ["indian-food-and-beer-pairing", "bitterness-perception", "carbonation-levels-by-style"],
 "diwali-beer-pairing": ["beer-and-dessert-pairing", "indian-food-and-beer-pairing", "beer-and-food-pairing-basics"],
 "beer-and-pizza-burger-pairing": ["beer-and-food-pairing-basics", "beer-and-cheese-pairing", "pale-ale-guide"],
 "co2-in-the-brewery": ["carbonation-levels-by-style", "glycol-cooling-systems", "oxygen-pickup-in-packaging"],
 "bright-beer-tank-management": ["cold-crashing", "carbonation-levels-by-style", "oxygen-pickup-in-packaging"],
 "boil-evaporation-rate": ["boil-chemistry-hot-break", "what-happens-during-the-boil", "dms-off-flavour"],
 "measuring-carbonation": ["carbonation-levels-by-style", "measuring-dissolved-oxygen", "beer-foam-science"],
 "fixing-homebrew-carbonation": ["bottle-conditioning-and-priming-sugar", "kegging-homebrew", "carbonation-levels-by-style"],
 "brewing-a-lager-at-home": ["lagering-explained", "diacetyl-rest", "fermentation-temperature-control-at-home"],
 "small-batch-brewing": ["brew-in-a-bag-method", "brewing-in-a-small-indian-apartment", "scaling-a-beer-recipe"],
 "brewing-a-wheat-beer-at-home": ["hefeweizen-guide", "wheat-malt-in-brewing", "witbier-guide"],
 "brewing-a-stout-at-home": ["dry-stout-guide", "roasted-malts-guide", "milk-and-oatmeal-stout"],
 "reading-a-fermentation-curve": ["how-long-does-beer-take-to-ferment", "yeast-growth-phases", "original-gravity-final-gravity-explained"],
 "sulphur-in-lager-fermentation": ["lagering-explained", "ale-vs-lager-yeast", "diacetyl-rest"],
 "biotransformation-in-hazy-ipa": ["new-england-ipa", "dry-hopping-guide", "hop-creep"],
 "fermenting-through-an-indian-summer": ["kveik-yeast-for-hot-climates", "fermentation-temperature-control-at-home", "esters-and-fusel-alcohols"],
 "high-gravity-brewing-and-dilution": ["brewhouse-efficiency", "original-gravity-final-gravity-explained", "ro-water-for-brewing"],
 "keg-washing-and-filling": ["cip-cleaning-in-place", "draught-line-cleaning", "oxygen-pickup-in-packaging"],
 "kettle-souring-at-home": ["berliner-weisse", "gose-guide", "sour-infection-off-flavour"],
 "yeast-viability-and-vitality": ["pitching-yeast-properly", "yeast-harvesting-and-reuse", "yeast-growth-phases"],
 "craft-beer-gift-guide": ["beer-glassware-guide", "how-to-store-beer-at-home", "beer-styles-guide"],
 "beer-flight-guide": ["how-to-taste-beer", "setting-up-a-beer-tasting", "beer-glassware-guide"],
 "why-craft-beer-costs-more": ["what-is-craft-beer", "beer-excise-duty-india", "cost-per-litre-beer"],
 "reading-a-taproom-menu": ["reading-a-beer-label", "what-is-ibu", "beer-styles-guide"],
 "hazy-vs-clear-beer": ["beer-haze-causes", "new-england-ipa", "clarifying-beer-finings"],
 "growlers-and-crowlers": ["how-to-store-beer-at-home", "oxidised-beer", "cans-vs-bottles"],
 "winter-beers-guide": ["imperial-stout-guide", "barleywine-guide", "bock-and-doppelbock"],
 "christmas-and-new-year-beers": ["belgian-strong-dark-ale", "imperial-stout-guide", "belgian-tripel"],
 "low-alcohol-craft-beer": ["session-ipa", "english-mild", "berliner-weisse"],
 "sour-beer-for-beginners": ["berliner-weisse", "gose-guide", "lambic-and-gueuze"],
 "how-hops-change-aroma": ["hop-varieties-for-beginners", "new-world-hops-nz-australia", "noble-hops-explained"],
 "hiring-your-first-head-brewer": ["brewery-staffing", "when-to-hire-a-consultant-brewmaster", "brewery-failure-reasons"],
 "insuring-a-brewery-india": ["brewery-compliance-checklist", "brewery-business-plan", "brewery-funding-options"],
 "brewery-partner-agreements": ["brewery-funding-options", "brewery-business-plan", "brewery-failure-reasons"],
 "pos-and-inventory-software-for-brewpubs": ["taproom-economics", "brewing-software-and-calculators", "weekly-numbers-for-brewpub-owners"],
 "leasing-space-for-a-brewpub": ["brewery-location-choice", "brewpub-vs-microbrewery", "microbrewery-cost-india"],
 "planning-a-brewpub-opening-month": ["first-100-days-of-a-new-brewpub", "taproom-events", "microbrewery-licence-india"],
 "brewpub-food-menu-and-margins": ["taproom-economics", "indian-food-and-beer-pairing", "beer-pricing-strategy"],
 "brewery-cash-flow-first-year": ["brewery-funding-options", "microbrewery-cost-india", "taproom-economics"],
 "photographing-beer-for-instagram": ["beer-social-media-marketing", "working-with-beer-influencers", "alcohol-advertising-rules-india"],
 "collaboration-brews": ["seasonal-and-limited-releases", "beer-brand-storytelling", "launching-a-new-beer"],
 "building-a-beer-community": ["taproom-events", "beer-social-media-marketing", "beer-merchandise"],
 "writing-tasting-notes-that-sell": ["beer-aroma-vocabulary", "beer-brand-storytelling", "beer-label-design"],
 "what-a-brewery-website-needs": ["beer-brand-positioning", "beer-social-media-marketing", "alcohol-advertising-rules-india"],
 "working-in-an-indian-distillery": ["how-whisky-is-made", "jobs-in-a-brewery", "molasses-vs-grain-spirit-india"],
 "writing-about-beer-for-a-living": ["beer-sommelier-career", "beer-judge-bjcp-exam", "cicerone-certification-guide"],
 "brewery-quality-control-career": ["brewery-qc-lab-on-a-budget", "jobs-in-a-brewery", "brewing-certifications-guide"],
 "women-in-indian-brewing": ["become-a-brewer-india", "jobs-in-a-brewery", "brewing-certifications-guide"],
 "planning-a-brewpub-year-around-indian-seasons": ["tap-list-planning-with-sales-data", "beer-demand-forecasting-indian-seasons", "weekly-numbers-for-brewpub-owners"],
 "setting-up-a-yeast-management-programme": ["yeast-harvesting-and-reuse", "beer-tastes-different-every-batch", "quality-system-for-a-small-brewery"],
 "cutting-power-and-water-in-a-brewpub": ["brewery-utilities-water-power", "sustainability-in-brewing", "glycol-cooling-systems"],
 "costing-a-recipe-before-you-brew": ["cost-per-litre-beer", "beer-cost-of-goods-explained", "scaling-a-pilot-recipe-to-production"],
 "how-a-beer-batch-is-released": ["quality-system-for-a-small-brewery", "beer-quality-data-for-data-teams", "beer-shelf-life"],
 "barley-and-malt-for-procurement-teams": ["barley-malting-process", "sourcing-malt-and-hops-in-india", "beer-supply-chain-explained"],
}
SEG_COURSE = {"Drinks producers": "contact.html?course=Brewery%20consultancy#enroll",
              "Corporate teams": "contact.html?course=Corporate%20training#enroll"}


STOP = {"a", "an", "and", "the", "of", "to", "in", "for", "with", "at", "on", "your", "how", "what", "why",
        "is", "it", "or", "you", "from", "beer", "beers", "india", "indian", "guide", "explained"}


def keywords(text):
    return {w.rstrip("s") for w in re.findall(r"[a-z0-9]+", text.lower())} - STOP


def main():
    plan = [p for p in json.loads((here / "plan.json").read_text()) if not p.get("daily")]
    old = [p for p in plan if p["date"] < START.isoformat()]
    # Course per (segment, cat) as the existing library already assigns it.
    course = collections.defaultdict(collections.Counter)
    for p in old:
        course[(p["segment"], p["cat"])][p["course"]] += 1
        course[(p["segment"], None)][p["course"]] += 1

    queues = {seg: [(seg, *line.split("|")) for line in block.splitlines()] for seg, block in PLAN.items()}
    rows = [r for q in queues.values() for r in q]
    assert len(rows) == DAYS, len(rows)
    order = []
    while any(queues.values()):  # one from each segment in turn, biggest segments first
        for seg in sorted(queues, key=lambda s: -len(queues[s])):
            if queues[seg]:
                r = queues[seg].pop(0)
                if r[1] not in PIN:
                    order.append(r)
    dates = [(START + datetime.timedelta(d)).isoformat() for d in range(DAYS)]
    free = iter(d for d in dates if d not in PIN.values())
    dated = {r[1]: PIN.get(r[1]) or next(free) for r in rows if r[1] in PIN} | {r[1]: next(free) for r in order}

    for seg, slug, h1, cat, st, *by in rows:
        # Related guides are always already live: same segment and category from the old library.
        words = keywords(slug + " " + h1)
        pool = [p for p in old if p["cat"] == cat] or [p for p in old if p["segment"] == seg]
        pool.sort(key=lambda p: (-len(words & keywords(p["slug"] + " " + p["h1"])), p["segment"] != seg, p["slug"]))
        c = SEG_COURSE.get(seg) or (course[(seg, cat)] or course[(seg, None)]).most_common(1)[0][0]
        row = {"slug": slug, "h1": h1, "cat": cat, "course": c, "related": RELATED.get(slug) or [p["slug"] for p in pool[:3]],
               "segment": seg, "stage": STAGE[st], "date": dated[slug], "daily": True}
        if seg == "Corporate teams" and cat in ALSO:
            row["also"] = ALSO[cat]
        if by:
            row["by"] = by[0]
        plan.append(row)
    assert len({p["slug"] for p in plan}) == len(plan), "duplicate slug"
    assert sorted(p["date"] for p in plan if p.get("daily")) == dates, "one guide per day"
    (here / "plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))
    print(DAYS, "daily rows,", len(plan), "total")


if __name__ == "__main__":
    main()
