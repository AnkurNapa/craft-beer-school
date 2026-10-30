"""Global series: 100 guides for readers outside India, to bring in enquiries
from the UK, US, Africa, the Middle East and Southeast Asia (Ankur's request,
31 Oct 2026). Rows are appended to plan.json as batch "global-1"; rerunning
replaces that batch only. A row is slug|h1|stage|cat|segment|course code|by."""
import json
import pathlib

here = pathlib.Path(__file__).parent
DATE = "2026-10-31"
BATCH = "global-1"
STAGE = {"a": "awareness", "c": "consideration", "d": "decision"}
R, A = "mentor-rahul-baliyan.html", "mentor-ankur-napa.html"
COURSE = {
    "BF": "brewing-fundamentals-course.html", "ABS": "advanced-brewing-science-course.html",
    "BBM": "brewery-business-management-course.html", "BBP": "beer-branding-packaging-course.html",
    "SE": "sensory-evaluation-course.html", "NA": "non-alcoholic-beer-course.html",
    "DM": "digital-marketing-for-breweries-course.html", "BS": "brand-strategy-and-positioning-for-breweries-course.html",
    "TM": "taproom-marketing-and-community-course.html", "NT": "naming-and-trademarks-for-drinks-brands-course.html",
    "PBI": "power-bi-and-tableau-for-breweries-course.html", "CD": "craft-distilling-course.html",
    "SS": "style-specialization-course.html", "WSET": "wset-beer-course.html",
    "BFS": "beer-for-starters-online-course.html", "HS": "hard-seltzer-course.html", "KOM": "kombucha-course.html",
    "ESG": "esg-in-craft-brewing-course.html",
    "CONS": "contact.html?course=Brewery%20consultancy#enroll",
    "CORP": "contact.html?course=Corporate%20training#enroll",
}

ROWS = """homebrewing-in-a-hot-climate|Homebrewing in a hot climate: keeping fermentation cool without a cellar|c|Brewing basics|Homebrewers|BF|
brewing-beer-at-high-altitude|Brewing beer at high altitude: boiling point, hops and evaporation|c|Brewing science|Homebrewers|BF|
homebrewing-with-desalinated-water|Homebrewing with desalinated or RO water: building the minerals back up|c|Brewing science|Homebrewers|ABS|
homebrewing-in-the-humid-tropics|Homebrewing in the humid tropics: mould, malt storage and sanitation|c|Brewing basics|Homebrewers|BF|
fermenting-lager-style-beer-without-a-fridge|Fermenting a lager-style beer without a fridge in a warm country|c|Brewing science|Homebrewers|BF|
choosing-yeast-for-a-warm-room|Choosing yeast for a warm room you cannot cool|c|Ingredients|Homebrewers|BF|
homebrewing-in-a-small-apartment|Homebrewing in a small apartment: a small-batch setup that works|a|Brewing basics|Homebrewers|BF|
buying-homebrew-ingredients-with-no-shop-nearby|Buying homebrew ingredients when there is no shop nearby|c|Ingredients|Homebrewers|BF|
storing-hops-in-hot-weather|Storing hops in hot weather so they keep their aroma|c|Ingredients|Homebrewers|BF|
brewing-with-local-adjuncts|Brewing with local adjuncts: rice, sorghum, cassava and maize|c|Ingredients|Homebrewers|ABS|
brewing-with-sorghum|Brewing with sorghum: a gluten-free grain with African roots|a|Ingredients|Homebrewers|BF|
brewing-with-tropical-fruit|Brewing with tropical fruit: mango, passion fruit and pineapple|c|Brewing basics|Homebrewers|BF|
converting-brewing-recipes-metric-and-us-units|Converting brewing recipes between metric and US units|c|Brewing basics|Homebrewers|BF|
homebrewing-in-singapore-and-malaysia|Homebrewing in Singapore and Malaysia: heat, humidity and ingredients|c|Brewing basics|Homebrewers|BF|
learning-to-brew-online-from-anywhere|Learning to brew online from anywhere: what a live course gives you|d|Brewing basics|Homebrewers|BF|
bottle-conditioning-in-hot-weather|Bottle conditioning in hot weather without gushers|c|Brewing basics|Homebrewers|BF|
reading-your-city-water-report-for-brewing|Reading your city water report for brewing, wherever you live|c|Brewing science|Homebrewers|ABS|
scaling-a-homebrew-recipe|Scaling a homebrew recipe up or down without changing the beer|c|Brewing basics|Homebrewers|BF|
brewing-a-clean-pale-ale-in-warm-weather|Brewing a clean pale ale in warm weather|c|Brewing basics|Homebrewers|BF|
brew-day-with-power-cuts|Planning a brew day around power cuts and unreliable gas|c|Brewing basics|Homebrewers|BF|
reviving-liquid-yeast-that-arrived-warm|Liquid yeast that arrived warm: what to do before you pitch|c|Ingredients|Homebrewers|BF|
designing-your-first-beer-recipe|Designing your first beer recipe with a simple spreadsheet|c|Brewing basics|Homebrewers|BF|
glycol-cooling-for-breweries-in-the-tropics|Sizing glycol cooling for a brewery in the tropics|c|Brewing science|Professional brewers|ABS|
brewery-water-from-desalination|Brewery water from desalination: remineralising for beer|c|Brewing science|Professional brewers|ABS|
beer-cold-chain-in-hot-countries|Protecting beer through a hot-country cold chain|c|Brewing science|Professional brewers|ABS|
dissolved-oxygen-and-shelf-life-in-warm-markets|Dissolved oxygen and shelf life in warm markets|c|Brewing science|Professional brewers|ABS|
designing-a-lager-for-hot-countries|Designing a lager for drinkers in hot countries|c|Styles|Professional brewers|SS|
sorghum-and-cassava-in-commercial-brewing|Sorghum and cassava in commercial brewing: what changes in the brewhouse|c|Ingredients|Professional brewers|ABS|
rice-in-the-brewhouse-cereal-cooking|Rice in the brewhouse: cereal cooking and mash schedules|c|Brewing science|Professional brewers|ABS|
non-alcoholic-beer-where-alcohol-is-restricted|Non-alcoholic beer for markets where alcohol is restricted|c|Brewing science|Professional brewers|NA|
importing-malt-for-a-small-brewery|Importing malt for a small brewery: lead times, storage and moisture|c|Ingredients|Professional brewers|ABS|
hop-freshness-across-long-supply-chains|Hop freshness across long supply chains|c|Ingredients|Professional brewers|ABS|
yeast-health-in-a-hot-brewery|Managing yeast health in a hot brewery|c|Brewing science|Professional brewers|ABS|
cleaning-in-place-with-hard-water|Cleaning in place with hard water: scale, caustic and acid|c|Brewing science|Professional brewers|ABS|
cutting-energy-use-in-a-small-brewery|Cutting energy use in a small brewery|c|Business|Professional brewers|ESG|
water-use-per-litre-of-beer|Water use per litre of beer: measuring it and bringing it down|c|Business|Professional brewers|ESG|
upskilling-a-brewery-team-online|Upskilling a brewery team with live online classes|d|Careers|Professional brewers|ABS|
beer-qualifications-compared-bjcp-wset-cicerone|BJCP, WSET and Cicerone: beer qualifications compared|c|Careers|Professional brewers|WSET|
logging-brewery-data-you-will-use|Logging brewery data you will actually use|c|Business|Professional brewers|PBI|
forecasting-demand-for-a-small-brewery|Forecasting beer demand for a small brewery|c|Business|Professional brewers|PBI|
opening-a-brewpub-in-a-new-country|Opening a brewpub in a country you did not grow up in|c|Business|Founders|BBM|
starting-a-brewpub-in-southeast-asia|Starting a brewpub in Southeast Asia: what founders plan for|c|Business|Founders|BBM|
brewpub-or-production-brewery|Brewpub or production brewery: choosing your model|c|Business|Founders|BBM|
brewery-licensing-steps-most-countries-share|Brewery licensing: the steps most countries share|c|Business|Founders|BBM|
microbrewery-start-up-costs-founders-forget|Microbrewery start-up costs: the lines founders forget|c|Business|Founders|BBM|
starting-a-microbrewery-in-africa|Starting a microbrewery in Africa: grain, water and power|c|Business|Founders|BBM|
importing-brewing-equipment|Importing brewing equipment: shipping, duties and installation|c|Business|Founders|BBM|
starting-a-beer-brand-with-contract-brewing|Starting a beer brand with contract brewing|c|Business|Founders|BBM|
starting-a-non-alcoholic-beer-brand|Starting a non-alcoholic beer brand|c|Business|Founders|NA|
starting-a-hard-seltzer-brand|Starting a hard seltzer brand: production and positioning|c|Business|Founders|HS|
starting-a-kombucha-business|Starting a kombucha business: from kitchen to commercial|c|Business|Founders|KOM|
planning-a-craft-distillery-first-decisions|Planning a craft distillery: the first decisions|c|Whisky|Founders|CD|
pricing-a-pint-in-a-brewpub|Pricing a pint in a brewpub: cost, margin and local habits|c|Business|Founders|BBM|
choosing-a-brewery-site|Choosing a brewery site: water, power, drains and neighbours|c|Business|Founders|BBM|
writing-a-head-brewer-job-description|Writing a head brewer job description that attracts the right people|d|Business|Founders|BBM|
what-investors-ask-a-brewery-founder|What investors ask a brewery founder|d|Business|Founders|BBM|
selling-craft-beer-to-hotels-and-restaurants|Selling craft beer to hotels and restaurants|c|Business|Founders|BBM|
learn-the-brewery-business-before-you-sign-a-lease|Learning the brewery business before you sign a lease|d|Business|Founders|BBM|
launching-a-beer-brand-in-a-new-market|Launching a beer brand in a new market|c|Branding|Brand builders|BS|
what-a-beer-label-must-show|What a beer label must show: the rules most markets share|c|Branding|Brand builders|BBP|
marketing-beer-where-alcohol-ads-are-restricted|Marketing beer where alcohol advertising is restricted|c|Branding|Brand builders|DM|
instagram-for-breweries|Instagram for breweries: what to post and how often|c|Branding|Brand builders|DM|
brewery-website-that-brings-taproom-visits|A brewery website that brings people to the taproom|c|Branding|Brand builders|DM|
naming-a-beer-for-more-than-one-language|Naming a beer that works in more than one language|c|Branding|Brand builders|NT|
protecting-a-beer-name-in-more-than-one-country|Protecting a beer name in more than one country|c|Branding|Brand builders|NT|
can-or-bottle-for-hot-markets|Can or bottle for hot markets|c|Branding|Brand builders|BBP|
marketing-non-alcoholic-beer-in-the-gulf|Marketing non-alcoholic beer in the Gulf|c|Branding|Brand builders|DM|
brewery-brand-that-tourists-remember|Building a brewery brand that tourists remember|c|Branding|Brand builders|TM|
become-a-brewer-without-a-brewing-degree|How to become a brewer without a brewing degree|c|Careers|Career changers|BF|
changing-career-to-brewing-in-your-30s-or-40s|Changing career to brewing in your 30s or 40s|d|Careers|Career changers|BF|
working-as-a-brewer-abroad|Working as a brewer abroad: the skills that travel|c|Careers|Career changers|BF|
learning-to-brew-while-working-full-time|Learning to brew while working full time|d|Careers|Career changers|BF|
working-in-beer-sales|Working in beer sales: what the job involves|a|Careers|Career changers|BBM|
careers-in-non-alcoholic-drinks|Careers in non-alcoholic and low-alcohol drinks|a|Careers|Career changers|NA|
homebrewer-to-assistant-brewer-first-year-plan|From homebrewer to assistant brewer: a first-year plan|d|Careers|Career changers|BF|
becoming-a-beer-judge|Becoming a beer judge: training and practice|c|Careers|Career changers|SE|
starting-in-a-taproom-to-learn-the-trade|Starting in a taproom to learn the beer trade|a|Careers|Career changers|WSET|
working-in-brewery-supply-chain-and-planning|Working in brewery supply chain and planning|a|Careers|Career changers|BBM|
tasting-beer-in-hot-weather|Tasting beer in hot weather: serving temperature and glassware|a|Tasting|Beer lovers|SE|
beginners-map-of-world-beer-styles|A beginner's map of world beer styles|a|Styles|Beer lovers|BFS|
pairing-beer-with-southeast-asian-food|Pairing beer with Southeast Asian food|a|Tasting|Beer lovers|SE|
pairing-beer-with-middle-eastern-food|Pairing beer and non-alcoholic beer with Middle Eastern food|a|Tasting|Beer lovers|SE|
pairing-beer-with-west-african-food|Pairing beer with West African food|a|Tasting|Beer lovers|SE|
traditional-african-beers|Traditional African beers: sorghum, millet and banana|a|Styles|Beer lovers|BFS|
asian-rice-lagers-explained|Asian rice lagers explained|a|Styles|Beer lovers|BFS|
non-alcoholic-beer-styles-explained|Non-alcoholic beer styles explained: from lager to IPA|a|Styles|Beer lovers|NA|
learning-about-beer-online-where-to-start|Learning about beer online: where a beginner should start|d|Tasting|Beer lovers|BFS|
getting-the-most-out-of-a-beer-festival|Getting the most out of a beer festival|a|Tasting|Beer lovers|SE|
how-remote-brewery-consultancy-works|How remote brewery consultancy works|d|Consultancy|Drinks producers|CONS|A
troubleshooting-beer-faults-over-video-call|Troubleshooting beer faults over a video call|c|Consultancy|Drinks producers|CONS|R
commissioning-a-brewhouse-with-an-overseas-supplier|Commissioning a brewhouse when the supplier is overseas|c|Consultancy|Drinks producers|CONS|R
developing-a-core-range-for-a-new-market|Developing a core beer range for a new market|c|Consultancy|Drinks producers|CONS|R
one-page-dashboard-for-brewery-owners|A one-page dashboard for brewery owners|c|Consultancy|Drinks producers|CONS|A
remote-quality-audit-for-a-brewery|A remote quality audit for a brewery: what we review|c|Consultancy|Drinks producers|CONS|A
adding-non-alcoholic-beer-to-a-brewery|Adding a non-alcoholic beer to an existing brewery|c|Consultancy|Drinks producers|CONS|A
beverage-training-for-global-drinks-teams|Beverage training for global drinks company teams|d|Beer for teams|Corporate teams|CORP|
beer-basics-for-shared-service-teams|Beer basics for shared service and GCC teams|a|Beer for teams|Corporate teams|CORP|
sensory-training-for-drinks-sales-teams|Sensory training for drinks sales teams|c|Beer for teams|Corporate teams|CORP|
beer-knowledge-for-drinks-marketing-teams|Beer knowledge for drinks marketing teams|c|Beer for teams|Corporate teams|CORP|
explaining-brewery-kpis-to-non-brewers|Explaining brewery KPIs to colleagues who never brewed|c|Beer for teams|Corporate teams|CORP|"""


def rows():
    out = []
    for line in ROWS.splitlines():
        slug, h1, st, cat, seg, course, by = line.split("|")
        out.append({"slug": slug, "h1": h1, "cat": cat, "course": COURSE[course], "segment": seg,
                    "stage": STAGE[st], "batch": BATCH, "date": DATE, **({"by": {"A": A, "R": R}[by]} if by else {})})
    for r in out:  # three related guides from the same category inside this batch
        same = [o["slug"] for o in out if o["cat"] == r["cat"] and o["slug"] != r["slug"]]
        k = [o["slug"] for o in out].index(r["slug"])
        r["related"] = [same[(k + j) % len(same)] for j in range(min(3, len(same)))]
    return out


if __name__ == "__main__":
    path = here / "plan.json"
    plan = [p for p in json.loads(path.read_text()) if p.get("batch") != BATCH]
    new = rows()
    assert len(new) == 100, len(new)
    plan += new
    assert len({p["slug"] for p in plan}) == len(plan), "duplicate slug"
    path.write_text(json.dumps(plan, indent=1, ensure_ascii=False))
    print(len(new), "global rows,", len(plan), "total")
