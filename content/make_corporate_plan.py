"""One-off: the corporate-teams seed plan, appended to plan.json. Every CTA sells
corporate training on for-companies.html#training. Rerun is safe: it replaces
its own rows and leaves the original 200 alone."""
import datetime, json, pathlib

COURSE = "contact.html?course=Corporate%20training#enroll"
# Second, smaller link for a reader learning for themselves. Wine has no course yet.
ALSO = {"Beer for teams": ("brewing-fundamentals-course.html", "Brewing Fundamentals"),
        "Whisky": ("craft-distilling-course.html", "Craft Distilling"),
        "Drinks business": ("courses.html", "all our courses")}
SEGMENT = "Corporate teams"
# cat -> rows of slug|h1|stage (a = awareness, c = consideration, d = decision)
PLAN = {
"Beer for teams": """beer-industry-explained-for-gcc-teams|The beer business explained for GCC teams|c
brewhouse-kpis-for-analysts|Brewhouse KPIs every beverage analyst should know|c
beer-supply-chain-explained|The beer supply chain, from barley field to bar|a
beer-production-planning-basics|Beer production planning for supply chain teams|c
beer-cost-of-goods-explained|Beer cost of goods, line by line, for finance teams|c
beer-quality-data-for-data-teams|Beer quality data: what the lab measures and why|c
packaging-line-efficiency-oee|Packaging line efficiency and OEE in a brewery|c
beer-brand-portfolio-explained|How beer companies build a brand portfolio|a
shipments-vs-depletions-beer-sales-data|Shipments versus depletions: reading beer sales data|c
beer-glossary-for-new-joiners|A beer glossary for new joiners in drinks companies|a
beer-styles-for-marketing-teams|Lager, ale and the styles big brewers sell|a
beer-demand-forecasting-indian-seasons|Forecasting beer demand around Indian seasons|c""",
"Whisky": """how-whisky-is-made|How whisky is made, from grain to cask|a
malt-grain-and-blended-whisky|Malt, grain and blended whisky explained|a
whisky-styles-of-the-world|Scotch, bourbon, Irish, Japanese and Indian whisky|a
whisky-maturation-and-casks|Whisky maturation: what the cask actually does|a
angels-share-whisky-in-indian-heat|The angels' share: why whisky ages faster in India|a
whisky-inventory-planning|Whisky inventory: planning stock you cannot sell for years|c
indian-whisky-market-for-new-joiners|The Indian whisky business for new joiners|a
whisky-label-terms-explained|Whisky label terms: age statements, single cask and cask strength|a
whisky-tasting-for-beginners|Tasting whisky properly, for teams new to spirits|a
distillery-kpis-for-analysts|Distillery KPIs: yield, litres of pure alcohol and losses|c
molasses-vs-grain-spirit-india|Molasses spirit versus grain spirit in India|a
how-whisky-blenders-keep-brands-consistent|How whisky blenders keep a brand consistent|a""",
"Wine": """how-wine-is-made|How wine is made, from vineyard to bottle|a
red-white-rose-and-sparkling-wine|Red, white, rosé and sparkling: how each wine is made|a
grape-varieties-for-beginners|Grape varieties every new joiner should know|a
indian-wine-regions|India's wine regions: Nashik, Nandi Hills and beyond|a
wine-harvest-and-vintage-planning|Harvest and vintage: why wine planning runs on one crop a year|c
wine-tasting-for-beginners|Tasting wine without the jargon|a
reading-a-wine-label|Reading a wine label|a
winery-kpis-for-analysts|Winery KPIs: yield per tonne, losses and cellar stock|c
wine-storage-and-cold-chain-india|Wine storage and the cold chain in Indian heat|c
wine-and-indian-food-pairing|Pairing wine with Indian food|a
old-world-vs-new-world-wine|Old World and New World wine|a
wine-faults-for-quality-teams|Common wine faults, for quality and supply teams|c""",
"Drinks business": """beer-wine-and-whisky-compared|Beer, wine and whisky compared, for people joining the drinks business|a
alcohol-regulation-india-for-corporate-teams|Alcohol regulation in India, for corporate teams|c
running-responsible-tastings-at-work|Running responsible tastings at work|d
data-and-ai-in-breweries-wineries-distilleries|Where data and AI help breweries, wineries and distilleries|c
product-training-for-beverage-gcc-teams|Why beverage GCC teams need product training|d
onboarding-new-joiners-in-a-drinks-company|Onboarding new joiners in a drinks company|d
water-energy-packaging-beer-wine-spirits|Water, energy and packaging across beer, wine and spirits|a
excise-for-finance-teams-beer-wine-spirits|Excise basics for finance teams in beer, wine and spirits|c""",
}
STAGE = {"a": "awareness", "c": "consideration", "d": "decision"}

here = pathlib.Path(__file__).parent


def append_segment(segment, course, blocks, start, end, extra=lambda cat: {}):
    """Replace this segment's rows in plan.json. A row is slug|h1|stage, optionally |author mentor slug."""
    plan = [p for p in json.loads((here / "plan.json").read_text()) if p["segment"] != segment]
    rows = [(cat, *line.split("|")) for cat, block in blocks.items() for line in block.splitlines()]
    step = (end - start) / (len(rows) - 1)
    for i, (cat, slug, h1, st, *by) in enumerate(rows):
        same = [r[1] for r in rows if r[0] == cat and r[1] != slug]
        nxt = rows[(i + 1) % len(rows)][1]
        k = same.index(nxt) if nxt in same else i % len(same)
        plan.append({"slug": slug, "h1": h1, "cat": cat, "course": course,
                     "related": [same[(k + j) % len(same)] for j in range(3)], "segment": segment,
                     "stage": STAGE[st], **extra(cat), **({"by": by[0]} if by else {}),
                     "date": (start + step * i).isoformat()})
    assert len({p["slug"] for p in plan}) == len(plan), "duplicate slug"
    (here / "plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))
    print(len(rows), segment, "rows,", len(plan), "total")


if __name__ == "__main__":
    append_segment(SEGMENT, COURSE, PLAN, datetime.date(2026, 6, 1), datetime.date(2026, 10, 1),
                   lambda cat: {"also": ALSO[cat]} if cat in ALSO else {})
