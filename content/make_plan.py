"""One-off: the 200-article seed plan. Each topic names the course its CTA sells."""
import json
C = {"F": "brewing-fundamentals-course.html", "A": "advanced-brewing-science-course.html",
     "B": "brewery-business-management-course.html", "S": "style-specialization-course.html",
     "P": "beer-branding-packaging-course.html", "E": "sensory-evaluation-course.html"}
PLAN = {
"Brewing basics": ("F", """how-beer-is-made-step-by-step|How beer is made, step by step
homebrewing-starter-kit-india|A homebrewing starter kit for India
extract-vs-all-grain-brewing|Extract or all-grain: which way to start
brew-in-a-bag-method|Brew in a bag, the easiest all-grain method
first-homebrew-mistakes|Ten mistakes almost every first homebrew makes
cleaning-vs-sanitising-brewing|Cleaning versus sanitising in brewing
how-to-use-a-hydrometer|How to use a hydrometer properly
original-gravity-final-gravity-explained|Original and final gravity explained
how-to-calculate-abv|How to calculate ABV from gravity readings
what-is-ibu|What IBU really tells you about bitterness
beer-colour-srm-ebc|Beer colour: SRM and EBC in plain English
mash-temperature-guide|Mash temperature and what it does to your beer
what-happens-during-the-boil|What actually happens during the boil
how-to-chill-wort-fast|How to chill wort fast, and why it matters
pitching-yeast-properly|Pitching yeast properly
fermentation-temperature-control-at-home|Controlling fermentation temperature at home
how-long-does-beer-take-to-ferment|How long does beer take to ferment?
bottle-conditioning-and-priming-sugar|Bottle conditioning and priming sugar
kegging-homebrew|Kegging your homebrew
carbonation-levels-by-style|Carbonation levels by beer style
reading-a-beer-recipe|How to read a beer recipe
scaling-a-beer-recipe|How to scale a beer recipe up or down
brewing-software-and-calculators|Brewing software and calculators worth using
keeping-a-brew-log|Keeping a brew log that actually helps
brewing-in-a-small-indian-apartment|Brewing in a small Indian apartment"""),
"Ingredients": ("F", """barley-malting-process|How barley becomes malt|F
base-malts-explained|Base malts explained|F
crystal-and-caramel-malts|Crystal and caramel malts|F
roasted-malts-guide|Roasted malts: chocolate, black and roasted barley|S
wheat-malt-in-brewing|Wheat malt in brewing|F
rice-and-maize-adjuncts-india|Rice and maize adjuncts in Indian brewing|A
oats-in-beer|Oats in beer: body, haze and silk|S
brewing-sugars-explained|Brewing sugars explained|F
hop-varieties-for-beginners|Hop varieties for beginners|F
alpha-acids-explained|Alpha acids and hop bitterness|A
noble-hops-explained|Noble hops and the European classics|S
american-hops-guide|A guide to American hops|S
new-world-hops-nz-australia|New Zealand and Australian hops|S
hop-pellets-vs-whole-cone|Hop pellets or whole cone?|F
hop-storage-and-freshness|Hop storage and freshness|A
dry-hopping-guide|Dry hopping: timing, dose and contact|A
hop-extracts-and-cryo-hops|Hop extracts and cryo hops|A
brewing-water-basics|Brewing water basics|F
water-hardness-and-beer|Water hardness and beer|A
sulphate-chloride-ratio|The sulphate to chloride ratio|A
treating-borewell-water-for-brewing|Treating borewell water for brewing|A
ro-water-for-brewing|Brewing with RO water|A
ale-vs-lager-yeast|Ale yeast versus lager yeast|F
dry-yeast-vs-liquid-yeast|Dry yeast or liquid yeast?|F
making-a-yeast-starter|Making a yeast starter|A
yeast-harvesting-and-reuse|Harvesting and reusing yeast|A
kveik-yeast-for-hot-climates|Kveik yeast for hot climates|A
brettanomyces-explained|Brettanomyces explained|S
adding-fruit-to-beer|Adding fruit to beer|S
brewing-with-indian-spices|Brewing with Indian spices|S"""),
"Brewing science": ("A", """mash-ph-explained|Mash pH explained
enzymes-in-the-mash|The enzymes at work in your mash
step-mashing|Step mashing and when it is worth it
decoction-mashing|Decoction mashing
lautering-and-sparging|Lautering and sparging
stuck-mash-fixes|How to prevent and fix a stuck mash
brewhouse-efficiency|Brewhouse efficiency, measured honestly
boil-chemistry-hot-break|Boil chemistry and the hot break
whirlpool-hopping|Whirlpool hopping
wort-aeration-and-oxygen|Wort aeration and oxygen for yeast
yeast-growth-phases|The phases of yeast growth
esters-and-fusel-alcohols|Esters and fusel alcohols
diacetyl-rest|The diacetyl rest
lagering-explained|Lagering explained
cold-crashing|Cold crashing
clarifying-beer-finings|Clarifying beer with finings
beer-filtration-basics|Beer filtration basics
pasteurisation-units|Pasteurisation units explained
beer-foam-science|The science of beer foam
beer-haze-causes|What causes haze in beer
hop-creep|Hop creep and how to manage it
oxygen-pickup-in-packaging|Oxygen pickup in packaging
beer-shelf-life|Beer shelf life
beer-staling-chemistry|The chemistry of stale beer
infection-bacteria-in-brewing|Bacteria and infection in brewing
cip-cleaning-in-place|Cleaning in place for small breweries
brewery-qc-lab-on-a-budget|A brewery QC lab on a budget
measuring-dissolved-oxygen|Measuring dissolved oxygen
beer-stability-in-indian-heat|Keeping beer stable in Indian heat
glycol-cooling-systems|Glycol cooling systems"""),
"Styles": ("S", """pilsner-style-guide|Pilsner: the style guide
helles-style-guide|Munich Helles
marzen-and-oktoberfest|Märzen and Oktoberfest beer
vienna-lager|Vienna lager
bock-and-doppelbock|Bock and doppelbock
dunkel-and-schwarzbier|Dunkel and schwarzbier
american-light-lager|American light lager
hefeweizen-guide|Hefeweizen
witbier-guide|Witbier
berliner-weisse|Berliner weisse
gose-guide|Gose
kolsch-guide|Kölsch
altbier-guide|Altbier
english-bitter|English bitter
english-mild|English mild
english-brown-ale|English brown ale
porter-guide|Porter
dry-stout-guide|Dry stout
imperial-stout-guide|Imperial stout
milk-and-oatmeal-stout|Milk stout and oatmeal stout
west-coast-ipa|West Coast IPA
new-england-ipa|New England IPA
english-ipa|English IPA
double-ipa|Double IPA
session-ipa|Session IPA
pale-ale-guide|Pale ale
amber-and-red-ales|Amber and red ales
saison-guide|Saison
belgian-dubbel|Belgian dubbel
belgian-tripel|Belgian tripel
belgian-strong-dark-ale|Belgian strong dark ale
lambic-and-gueuze|Lambic and gueuze
flanders-red-ale|Flanders red ale
barleywine-guide|Barleywine
smoked-beer-rauchbier|Rauchbier and smoked beer"""),
"Tasting": ("E", """setting-up-a-beer-tasting|How to set up a beer tasting
beer-glassware-guide|Beer glassware, and why shape matters
beer-serving-temperature|Beer serving temperature by style
how-to-pour-beer|How to pour beer
beer-aroma-vocabulary|Building your beer aroma vocabulary
beer-flavour-wheel|Using the beer flavour wheel
mouthfeel-and-body|Mouthfeel and body
bitterness-perception|How we perceive bitterness
beer-and-food-pairing-basics|Beer and food pairing basics
indian-food-and-beer-pairing|Pairing beer with Indian food
beer-and-cheese-pairing|Beer and cheese pairing
beer-and-dessert-pairing|Beer and dessert pairing
how-beer-judges-score|How beer judges score a beer
bjcp-scoresheet-explained|The BJCP scoresheet explained
triangle-test|Running a triangle test
training-your-palate|Training your palate
off-flavour-spiking-kits|Off-flavour spiking kits
diacetyl-off-flavour|Diacetyl: the butter fault
dms-off-flavour|DMS: the sweetcorn fault
acetaldehyde-off-flavour|Acetaldehyde: the green apple fault
oxidised-beer|Oxidised beer
lightstruck-skunky-beer|Lightstruck, or skunked, beer
phenolic-off-flavours|Phenolic off-flavours
sour-infection-off-flavour|When sourness is an infection
metallic-off-flavour|Metallic off-flavours
running-a-sensory-panel|Running a sensory panel
fresh-vs-stale-ipa|Fresh IPA versus stale IPA
draught-line-cleaning|Draught line cleaning
how-to-store-beer-at-home|How to store beer at home
reading-a-beer-label|How to read a beer label"""),
"Business": ("B", """microbrewery-licence-india|Getting a microbrewery licence in India
brewpub-vs-microbrewery|Brewpub or microbrewery?
contract-brewing-india|Contract brewing in India
gypsy-brewing-explained|Gypsy brewing explained
microbrewery-cost-india|What a microbrewery costs in India
brewhouse-size-guide|Choosing your brewhouse size
cost-per-litre-beer|Working out your cost per litre
beer-pricing-strategy|Pricing craft beer
taproom-economics|Taproom economics
brewery-business-plan|Writing a brewery business plan
beer-excise-duty-india|Excise duty on beer in India
fssai-rules-for-beer|FSSAI and beer
brewery-equipment-buying-guide|Buying brewery equipment
brewery-compliance-checklist|A brewery compliance checklist
beer-distribution-india|Beer distribution in India
on-trade-vs-off-trade|On-trade versus off-trade
kegs-vs-cans-business|Kegs or cans: the business case
brewery-staffing|Staffing a small brewery
brewery-utilities-water-power|Brewery utilities: water, power and steam
brewery-waste-and-spent-grain|Brewery waste and spent grain
sustainability-in-brewing|Sustainability in brewing
craft-beer-market-india-trends|Craft beer market trends in India
brewery-funding-options|Funding a brewery
brewery-location-choice|Choosing a brewery location
brewery-failure-reasons|Why breweries fail"""),
"Branding": ("P", """naming-a-beer-brand|Naming a beer brand
beer-label-design|Beer label design that works
beer-label-rules-india|Beer label rules in India
cans-vs-bottles|Cans versus bottles
can-design-tips|Designing a beer can
beer-brand-storytelling|Storytelling for beer brands
alcohol-advertising-rules-india|Alcohol advertising rules in India
beer-social-media-marketing|Social media for breweries
launching-a-new-beer|Launching a new beer
taproom-events|Taproom events that bring people back
beer-merchandise|Brewery merchandise
beer-brand-positioning|Positioning a beer brand
seasonal-and-limited-releases|Seasonal and limited releases
beer-packaging-costs|What beer packaging costs
working-with-beer-influencers|Working with beer creators"""),
"Careers": ("F", """brewing-certifications-guide|Brewing certifications, compared|F
cicerone-certification-guide|The Cicerone certification|E
wset-beer-course|WSET Level 1 Award in Beer|E
beer-judge-bjcp-exam|Becoming a BJCP beer judge|E
brewing-degree-vs-short-course|Brewing degree or short course?|F
jobs-in-a-brewery|The jobs inside a brewery|F
assistant-brewer-job|What an assistant brewer really does|F
beer-sommelier-career|A career as a beer sommelier|E
homebrewer-to-pro-brewer|From homebrewer to professional brewer|A
brewery-sales-career|A career in brewery sales|B"""),
}
out = []
for cat, (default, block) in PLAN.items():
    rows = [l.split("|") for l in block.strip().splitlines()]
    slugs = [r[0] for r in rows]
    for i, r in enumerate(rows):
        n = len(slugs)
        rel = [slugs[(i + k) % n] for k in (1, 2, n - 1)]
        out.append({"slug": r[0], "h1": r[1], "cat": cat,
                    "course": C[r[2] if len(r) > 2 else default], "related": rel})
assert len(out) == 200 and len({o["slug"] for o in out}) == 200, len(out)
json.dump(out, open("content/plan.json", "w"), indent=1, ensure_ascii=False)
print(len(out))

# ---- segments, funnel stage and a five-year publishing history --------------
import datetime, itertools
SEGMENT = {"Brewing basics": "Homebrewers", "Ingredients": "Homebrewers", "Brewing science": "Professional brewers",
           "Styles": "Beer lovers", "Tasting": "Beer lovers", "Business": "Founders",
           "Branding": "Brand builders", "Careers": "Career changers"}
PRO = {"alpha-acids-explained", "hop-storage-and-freshness", "dry-hopping-guide", "hop-extracts-and-cryo-hops",
       "water-hardness-and-beer", "sulphate-chloride-ratio", "treating-borewell-water-for-brewing", "ro-water-for-brewing",
       "making-a-yeast-starter", "yeast-harvesting-and-reuse", "kveik-yeast-for-hot-climates", "rice-and-maize-adjuncts-india",
       "how-beer-judges-score", "bjcp-scoresheet-explained", "triangle-test", "off-flavour-spiking-kits",
       "running-a-sensory-panel", "draught-line-cleaning"}
# awareness: curious readers, soft CTA. consideration: how-to, point at the course
# that goes deeper. decision: planning or career intent, ask for the enrolment.
STAGE = {"Styles": "awareness", "Tasting": "awareness", "Brewing basics": "consideration",
         "Ingredients": "consideration", "Brewing science": "consideration", "Branding": "consideration",
         "Business": "decision", "Careers": "decision"}
DECISION = {"homebrewing-starter-kit-india", "first-homebrew-mistakes", "training-your-palate", "running-a-sensory-panel",
            "homebrewer-to-pro-brewer", "brewery-qc-lab-on-a-budget", "launching-a-new-beer"}
for o in out:
    o["segment"] = "Professional brewers" if o["slug"] in PRO else SEGMENT[o["cat"]]
    o["stage"] = "decision" if o["slug"] in DECISION else STAGE[o["cat"]]

# Round-robin across categories so every stretch of the archive is mixed, then
# spread evenly from October 2021 to September 2026.
by_cat = [[o for o in out if o["cat"] == c] for c in PLAN]
order = [o for group in itertools.zip_longest(*by_cat) for o in group if o]
start, end = datetime.date(2021, 10, 4), datetime.date(2026, 9, 21)
step = (end - start).days / (len(order) - 1)
for i, o in enumerate(order):
    d = start + datetime.timedelta(days=round(i * step))
    o["date"] = d.isoformat()
json.dump(order, open("content/plan.json", "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(o["segment"] for o in order)); print(Counter(o["stage"] for o in order)); print(order[0]["date"], order[-1]["date"])
