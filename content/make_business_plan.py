"""Business series: 120 guides on brewery, wine and gin business, project and
business reports, market research, SEO, consultancy and India entry,
written to bring in enquiries for our services (Ankur's request, 31 Oct 2026). Appended to plan.json as batch
"business-1"; rerunning replaces that batch only.
A row is slug|h1|stage|cat|segment|course code|by."""
import json
import pathlib

here = pathlib.Path(__file__).parent
DATE = "2026-10-31"
BATCH = "business-1"
STAGE = {"a": "awareness", "c": "consideration", "d": "decision"}
R, A = "mentor-rahul-baliyan.html", "mentor-ankur-napa.html"
COURSE = {
    "BBM": "brewery-business-management-course.html", "WB": "winery-business-course.html",
    "WM": "winemaking-course.html", "GIN": "craft-gin-making-course.html", "CD": "craft-distilling-course.html",
    "RTD": "rtd-drinks-alcoholic-and-non-alcoholic-course.html", "DM": "digital-marketing-for-breweries-course.html",
    "TM": "taproom-marketing-and-community-course.html", "PBI": "power-bi-and-tableau-for-breweries-course.html",
    "BRAND": "brand-consultancy.html#enquire",
    "CONS": "contact.html?course=Brewery%20consultancy#enroll",
    "REP": "contact.html?course=Project%20and%20business%20reports#enroll",
    "MR": "contact.html?course=Market%20research#enroll",
    "WCONS": "contact.html?course=Winery%20consultancy#enroll",
    "DCONS": "contact.html?course=Distillery%20consultancy#enroll",
    "TURN": "contact.html?course=Turnkey%20and%20contract%20projects#enroll",
    "ENTRY": "contact.html?course=Market%20entry%20into%20India#enroll",
}

ROWS = """brewery-break-even-explained|Brewery break-even explained: the volume you need each month|c|Business|Founders|BBM|
brewpub-food-and-beer-margins|Brewpub margins: balancing food and beer sales|c|Business|Founders|BBM|
brewery-working-capital|Working capital for a brewery: stock, duty and the cash gap|c|Business|Founders|BBM|
bank-loan-for-a-brewery|Getting a bank loan for a brewery: what the bank looks at|d|Business|Founders|REP|A
microbrewery-capital-costs|Microbrewery capital costs: where the money goes|c|Business|Founders|REP|A
unit-economics-of-a-keg-can-and-pint|Unit economics of a keg, a can and a pint|c|Business|Founders|BBM|
franchise-partnership-or-own-brewpub|Franchise, partnership or your own brewpub|c|Business|Founders|BBM|
expand-your-brewery-or-buy-contract-capacity|Expand your brewery or buy contract capacity|d|Business|Founders|CONS|A
how-breweries-are-valued|How breweries are valued when they are sold|a|Business|Founders|BBM|
craft-beer-distribution-models|Craft beer distribution models: direct, distributor or both|c|Business|Founders|BBM|
taproom-only-brewery-model|The taproom-only brewery model|c|Business|Founders|BBM|
contract-brewing-economics-for-the-host|Contract brewing economics for the host brewery|c|Business|Founders|BBM|
pricing-beer-for-retail-shelves|Pricing beer for retail shelves|c|Business|Founders|BBM|
cash-flow-forecast-for-a-new-brewery|A 12-month cash flow forecast for a new brewery|c|Business|Founders|REP|A
funding-a-brewery|Funding a brewery: savings, loans, investors and grants|c|Business|Founders|BBM|
selling-your-brewery-getting-the-numbers-ready|Selling your brewery: getting the numbers ready|d|Business|Founders|REP|A
planning-a-brewpub-for-seasonal-demand|Planning a brewpub for seasonal demand|c|Business|Founders|BBM|
which-of-your-beers-make-money|Which of your beers make money: portfolio profitability|c|Business|Founders|PBI|
cutting-cost-of-goods-without-changing-the-beer|Cutting cost of goods without changing the beer|c|Business|Founders|CONS|R
business-model-canvas-for-a-craft-brewery|A business model canvas for a craft brewery|a|Business|Founders|BBM|
starting-a-winery-business|Starting a winery: the business decisions before the vines|c|Wine|Founders|WB|
winery-business-plan|What goes into a winery business plan|c|Wine|Founders|REP|A
winery-project-report|Writing a project report for a winery|d|Wine|Founders|REP|A
buy-grapes-or-grow-your-own|Buy grapes or grow your own: a new winery's first big choice|c|Wine|Founders|WB|
boutique-winery-economics|Boutique winery economics: volume, price and cash|c|Wine|Founders|WB|
why-wine-ageing-ties-up-cash|Wine and cash: why ageing ties up money|c|Wine|Founders|WB|
winery-tasting-room-as-a-business|Running a winery tasting room as a business|c|Wine|Founders|WB|
getting-wine-into-shops-and-restaurants|Getting wine into shops and restaurants|c|Wine|Founders|WB|
starting-a-wine-brand-without-a-winery|Starting a wine brand without a winery|c|Wine|Founders|WB|
pricing-wine-cost-positioning-and-shelf|Pricing wine: cost, positioning and the shelf|c|Wine|Founders|WB|
planning-winery-equipment-for-a-first-vintage|Planning winery equipment for a first vintage|c|Wine|Founders|WM|
wine-tourism-as-a-second-income|Wine tourism as a second income for a winery|a|Wine|Founders|WB|
starting-a-fruit-wine-business|Starting a fruit wine business|c|Wine|Founders|WM|
market-research-for-a-new-wine-brand|Market research for a new wine brand|c|Wine|Founders|MR|A
winery-licensing-steps|Winery licensing: the steps most places share|c|Wine|Founders|WB|
exporting-wine-basics|Exporting wine: labels, partners and shelf life|c|Wine|Founders|WB|
wine-clubs-for-small-wineries|Wine clubs and subscriptions for small wineries|c|Wine|Founders|WB|
cost-per-bottle-in-a-small-winery|Working out cost per bottle in a small winery|c|Wine|Founders|WB|
when-to-hire-a-consultant-winemaker|When a new winery should hire a consultant winemaker|d|Wine|Founders|WCONS|A
funding-a-winery|Funding a winery: what investors and banks ask|d|Wine|Founders|REP|A
starting-a-gin-brand-distil-or-contract|Starting a gin brand: distil it yourself or contract it|c|Drinks business|Founders|GIN|
gin-distillery-business-plan|What goes into a gin distillery business plan|c|Drinks business|Founders|REP|A
gin-distillery-project-report|Writing a project report for a gin distillery|d|Drinks business|Founders|REP|A
cost-of-a-bottle-of-craft-gin|Working out the cost of a bottle of craft gin|c|Drinks business|Founders|GIN|
contract-distilled-gin|Contract-distilled gin: how it works and what to check|c|Drinks business|Founders|GIN|
sourcing-gin-botanicals-commercially|Sourcing botanicals for a commercial gin|c|Drinks business|Founders|GIN|
gin-packaging-costs-founders-underestimate|Gin bottles and packaging: the costs founders underestimate|c|Drinks business|Founders|GIN|
pricing-and-positioning-a-craft-gin|Pricing and positioning a craft gin|c|Drinks business|Founders|GIN|
planning-production-capacity-for-a-gin-brand|Planning production capacity for a gin brand|c|Drinks business|Founders|CD|
gin-distillery-licensing-steps|Gin distillery licensing: the steps most places share|c|Drinks business|Founders|GIN|
a-gin-brand-story-that-is-true|Building a gin brand story that is true|c|Drinks business|Brand builders|BRAND|
getting-craft-gin-into-bars-and-shops|Getting craft gin into bars, shops and hotels|c|Drinks business|Founders|GIN|
market-research-before-launching-a-gin|Market research before launching a gin|c|Drinks business|Founders|MR|A
selling-gin-direct|Selling gin direct: online, events and the distillery shop|c|Drinks business|Founders|GIN|
flavoured-gin-business-case|Flavoured gin: the business case and the risks|c|Drinks business|Founders|GIN|
canned-gin-and-tonic-as-a-product-line|Canned gin and tonic as a product line|c|Drinks business|Founders|RTD|
buying-neutral-spirit-for-gin|Buying neutral spirit for gin: quality and contracts|c|Drinks business|Founders|CD|
exporting-craft-gin|Exporting craft gin: labels, partners and markets|c|Drinks business|Founders|GIN|
scaling-a-gin-brand|Scaling a gin brand from hundreds to thousands of cases|d|Drinks business|Founders|CONS|A
funding-a-gin-brand|Funding a gin brand: what investors look for|d|Drinks business|Founders|REP|A
what-is-a-detailed-project-report|What a detailed project report is and when you need one|a|Consultancy|Founders|REP|A
what-a-brewery-dpr-should-contain|What a brewery DPR should contain|c|Consultancy|Founders|REP|A
feasibility-study-for-a-brewery|A feasibility study for a brewery: the questions it must answer|c|Consultancy|Founders|REP|A
a-dpr-a-bank-will-accept|Writing a DPR a bank will accept|d|Consultancy|Founders|REP|A
defensible-assumptions-in-a-project-report|Financial assumptions in a project report: making them defensible|c|Consultancy|Founders|REP|A
sensitivity-analysis-for-a-drinks-project|Sensitivity analysis for a drinks project|c|Consultancy|Founders|REP|A
project-report-or-business-plan|Project report or business plan: which one you need|a|Consultancy|Founders|REP|A
feasibility-study-for-a-craft-distillery|A feasibility study for a craft distillery|c|Consultancy|Founders|REP|A
project-report-for-a-brewpub|A project report for a brewpub|c|Consultancy|Founders|REP|A
capacity-planning-in-a-project-report|Capacity planning in a project report|c|Consultancy|Founders|REP|A
market-section-of-a-project-report|Writing the market section of a project report|c|Consultancy|Founders|REP|A
investor-pack-for-a-drinks-start-up|An investor pack for a drinks start-up|d|Consultancy|Founders|REP|A
npv-irr-and-payback-for-a-brewery-project|NPV, IRR and payback for a brewery project, explained|c|Consultancy|Founders|REP|A
project-report-for-a-brewery-expansion|A project report for expanding an existing brewery|c|Consultancy|Founders|REP|A
independent-review-of-a-project-report|Getting an independent review of your project report|d|Consultancy|Founders|REP|A
project-report-for-a-non-alcoholic-drinks-plant|A project report for a non-alcoholic drinks plant|c|Consultancy|Founders|REP|A
what-goes-into-preparing-a-project-report|How a project report is prepared, step by step|d|Consultancy|Founders|REP|A
mistakes-in-brewery-project-reports|Common mistakes in brewery project reports|c|Consultancy|Founders|REP|A
business-health-report-for-a-brewery|A business health report for an existing brewery|d|Consultancy|Founders|REP|A
project-report-for-a-cidery|A project report for a cidery|c|Consultancy|Founders|REP|A
market-research-for-a-new-beer-brand|Market research for a new beer brand: what to find out first|c|Branding|Brand builders|MR|A
consumer-survey-for-a-drinks-brand|Running a consumer survey for a drinks brand|c|Branding|Brand builders|MR|A
retail-audit-for-craft-beer|A retail audit for craft beer: what is on the shelf and why|c|Branding|Brand builders|MR|A
competitor-analysis-for-a-brewery|Competitor analysis for a brewery|c|Branding|Brand builders|MR|A
sizing-a-local-beer-market|Sizing a local beer market without inventing numbers|c|Branding|Brand builders|MR|A
taste-panels-and-focus-groups-for-a-new-drink|Taste panels and focus groups for a new drink|c|Branding|Brand builders|MR|A
market-research-for-a-taproom-location|Market research for a taproom location|c|Branding|Brand builders|MR|A
researching-drinks-trends-without-chasing-fads|Researching drinks trends without chasing fads|a|Branding|Brand builders|MR|A
price-research-for-a-new-drink|Price research for a new drink|c|Branding|Brand builders|MR|A
when-to-commission-market-research|When to commission market research and what to ask for|d|Branding|Brand builders|MR|A
seo-for-breweries|SEO for breweries: getting found by drinkers searching nearby|c|Branding|Brand builders|DM|
google-business-profile-for-a-taproom|A Google Business Profile for a taproom|c|Branding|Brand builders|DM|
seo-for-a-winery-website|SEO for a winery website|c|Branding|Brand builders|DM|
seo-for-a-gin-brand|SEO for a gin brand|c|Branding|Brand builders|DM|
content-that-brings-visitors-to-a-drinks-website|Content that brings visitors to a drinks brand's website|c|Branding|Brand builders|DM|
keyword-research-for-a-brewery-website|Keyword research for a brewery website|c|Branding|Brand builders|DM|
website-calls-to-action-for-taproom-bookings|Website calls to action that bring taproom bookings|c|Branding|Brand builders|DM|
measuring-website-leads-for-a-drinks-business|Measuring website leads for a drinks business|c|Branding|Brand builders|PBI|
managing-reviews-and-ratings-for-a-brewery|Reviews and ratings: managing them for a brewery|c|Branding|Brand builders|TM|
seo-mistakes-drinks-websites-make|SEO mistakes drinks websites make|c|Branding|Brand builders|DM|
turnkey-brewery-projects-what-the-contract-covers|Turnkey brewery projects: what the contract should cover|c|Consultancy|Drinks producers|TURN|R
brewery-consultancy-for-a-brewpub-or-a-large-plant|Brewery consultancy for a brewpub and for a large plant: what changes|a|Consultancy|Drinks producers|CONS|R
what-winery-consultancy-covers|What winery consultancy covers, from grapes to bottle|d|Consultancy|Drinks producers|WCONS|A
what-distillery-consultancy-covers|What distillery consultancy covers, from still to bottle|d|Consultancy|Drinks producers|DCONS|A
contract-manufacturing-for-drinks-brands|Contract manufacturing for drinks brands: beer, wine and spirits|c|Consultancy|Drinks producers|TURN|A
owners-engineer-for-a-brewery-project|An owner's engineer for a brewery project|c|Consultancy|Drinks producers|TURN|R
moving-a-recipe-to-a-new-plant|Moving a recipe and process to a new plant|c|Consultancy|Drinks producers|CONS|R
trial-runs-before-a-distillery-launches|Trial runs before a distillery launches its first spirit|c|Consultancy|Drinks producers|DCONS|A
support-for-a-new-winerys-first-vintage|Support for a new winery's first vintage|c|Consultancy|Drinks producers|WCONS|A
building-the-team-for-a-new-brewery-plant|Building the team for a new brewery plant|c|Consultancy|Drinks producers|CONS|R
setting-up-a-brewery-in-india-as-a-foreign-company|Setting up a brewery in India as a foreign company|c|Business|Founders|ENTRY|A
bringing-a-foreign-beer-brand-to-india|Bringing a foreign beer brand to India|c|Business|Founders|ENTRY|A
importing-wine-into-india|Importing wine into India: how the process works|c|Wine|Founders|ENTRY|A
launching-a-spirits-brand-in-india-from-abroad|Launching a spirits brand in India from abroad|c|Drinks business|Founders|ENTRY|A
finding-an-indian-partner-for-a-drinks-brand|Finding an Indian partner for a drinks brand|d|Business|Founders|ENTRY|A
contract-brewing-in-india-for-international-brands|Contract brewing in India for international brands|c|Business|Founders|ENTRY|R
selling-brewing-equipment-and-ingredients-in-india|Selling brewing equipment and ingredients in India|c|Business|Founders|ENTRY|A
choosing-an-indian-state-for-a-brewery-or-distillery|Choosing an Indian state for a brewery or distillery|c|Business|Founders|ENTRY|A
market-research-in-india-for-a-foreign-drinks-brand|Market research in India for a foreign drinks brand|c|Branding|Brand builders|MR|A
why-drinks-companies-look-at-india|Why international drinks companies look at India|a|Business|Founders|ENTRY|A"""


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
    assert len(new) == 120, len(new)
    plan += new
    assert len({p["slug"] for p in plan}) == len(plan), "duplicate slug"
    path.write_text(json.dumps(plan, indent=1, ensure_ascii=False))
    print(len(new), "business rows,", len(plan), "total")
