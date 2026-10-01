# -*- coding: utf-8 -*-
"""One detail page per online course: who it is for, week-by-week syllabus,
logistics and terms.

Price, duration and the card bullets come from pages_a.COURSE_DATA so a detail
page can never quote a different fee than the courses grid. Logistics and terms
mirror the "CBS Online Courses 2026" brochure.
"""
import re

import article_render
import articles_all
import pages_a
from pages_a import banner, course_href as slug_for, enroll_href

# Shared across every course, straight from the 2026 brochure.
LOGISTICS = [
    ("Schedule", "Live on Saturdays and Sundays, 12:00 PM to 2:00 PM IST. Timings may shift by mutual agreement with the cohort."),
    ("Batch size", "Maximum 20 students, so every question gets answered."),
    ("Included", "Session recordings, presentation decks, weekly assignments and the learning kit."),
    ("Certificate", "Certificate of Completion once every assignment is in and you have attended at least 80% of live sessions."),
    ("Beyond the screen", "Recommended microbrewery visits, so you see the kit you are studying."),
    ("Fees", "Paid in full at sign-up. No discounts apply, and a package of courses cannot be changed once confirmed."),
]

ARTICLES_BY_SLUG = {a["slug"]: a for a in articles_all.ARTICLES}

# name (plain text, as in the contact form) -> detail
DETAIL = {
    "Brewing Fundamentals": dict(
        reading=['become-a-brewer-india', 'what-is-craft-beer', 'brewing-for-india'],
        who=["Homebrewers who want to know why a batch worked, not just that it did",
             "Beer lovers ready to brew their first real recipe",
             "Hospitality and sales people who talk about beer every day"],
        outcomes=["Explain every step from mill to package", "Build a 20 L recipe with target OG, IBU and colour",
                  "Clean and sanitise like a professional brewery", "Calculate ABV from your own gravity readings"],
        weeks=[
            ("Grain to glass", ["The four ingredients and what each one does", "The brewhouse map: mill, mash, lauter, boil, whirlpool, ferment, condition, package", "Reading a label: ABV, IBU and colour (EBC and SRM)"],
             "Taste three commercial beers and trace each one back to its ingredients."),
            ("Malt, water and the mash", ["Malting: steep, germinate, kiln", "Base malts versus speciality malts", "Enzymes and mash temperature: 62 to 65 °C for a drier beer, 68 to 70 °C for more body", "Water basics, and why mash pH should sit at 5.2 to 5.6"],
             "Work out the grist and strike water for a 20 L batch."),
            ("Hops, boil and yeast", ["Alpha acids, and why they need the boil to turn bitter", "Bittering, aroma and dry hop additions", "What the boil does: sterilise, isomerise, drive off DMS, form the hot break", "Ale versus lager yeast, pitch rates and temperature control"],
             "Calculate the IBU of your recipe."),
            ("Sanitation, kit and your first recipe", ["Cleaning versus sanitising, and the chemicals for each", "Homebrew kit versus a microbrewery brewhouse", "Original and final gravity, and ABV = (OG - FG) x 131.25", "Priming, carbonation and packaging"],
             "Present your first complete recipe to the cohort."),
        ]),
    "Advanced Brewing Science": dict(
        reading=['brewing-for-india', 'beer-off-flavours', 'become-a-brewer-india'],
        who=["Working brewers and assistant brewers", "Graduates of Brewing Fundamentals",
             "Serious homebrewers chasing consistency"],
        outcomes=["Turn a water lab report into a brewing water profile", "Measure and improve brewhouse efficiency",
                  "Control esters, fusels and diacetyl through fermentation", "Write a QA plan for a small brewery"],
        weeks=[
            ("Brewing water chemistry", ["Calcium, magnesium, sulphate, chloride and bicarbonate", "Residual alkalinity and the sulphate to chloride ratio", "Treating borewell and municipal water in India, and blending with RO water"],
             "Turn your local water report into a treatment plan for two styles."),
            ("Mash chemistry and advanced mashing", ["Step mashes, protein rests and decoction", "Rice and maize adjuncts, and cooking them", "Extract, lauter yield and brewhouse efficiency"],
             "Calculate brewhouse efficiency from a real brew log."),
            ("Hop chemistry", ["Alpha and beta acids, isomerisation and utilisation", "Hop oils: myrcene, linalool, geraniol", "Biotransformation and hop creep"],
             "Redesign a hop schedule for the same IBU with more aroma."),
            ("Yeast and fermentation microbiology", ["Lag, growth and stationary phases", "Esters and fusels versus fermentation temperature", "Diacetyl, the diacetyl rest and acetaldehyde", "Oxygenation, propagation and harvesting"],
             "Plot a fermentation from gravity and temperature logs and call the faults."),
            ("Contamination, stability and shelf life", ["Lactobacillus, Pediococcus and wild yeast", "Oxygen pickup and staling", "Haze, finings, filtration and pasteurisation units", "Keeping beer fresh through an Indian summer supply chain"],
             "Audit a packaging line for oxygen and infection risk."),
            ("Quality assurance and control", ["A QC lab on a small budget: hydrometer, pH meter, microscope, forcing tests", "Specs, tolerances, SOPs and brew logs", "HACCP basics and FSSAI"],
             "Write the QA plan for a 500 L brewery."),
        ]),
    "Brewery Business Management": dict(
        reading=['start-a-microbrewery-india', 'craft-beer-in-india', 'become-a-brewer-india'],
        who=["Founders planning a brewpub or microbrewery", "Investors sizing up a beer business",
             "Brewers stepping into management"],
        outcomes=["Choose between brewpub, microbrewery and contract brewing", "Build a cost per litre and a break-even",
                  "Map the licences your state requires", "Pick a route to market"],
        weeks=[
            ("Plan and finance", ["Brewpub, microbrewery or contract brewing", "Capex: brewhouse, cellar, cooling and utilities", "Opex, cost per litre, pricing and break-even", "Funding options"],
             "Build a simple P&amp;L for your concept."),
            ("Licensing and regulation in India", ["Excise is set state by state, and what that means for you", "Brewpub and microbrewery licences, FSSAI, pollution control consent", "Label registration, trademarks and realistic timelines"],
             "Draw up a licence checklist and timeline for your state."),
            ("Market, brand and distribution", ["Positioning and taproom economics", "On-trade versus off-trade, distributors and state rules", "Kegs versus cans, and when each makes sense"],
             "Present a one-page business plan to the cohort."),
        ]),
    "Style Specialisation": dict(
        reading=['beer-styles-guide', 'how-to-taste-beer', 'what-is-craft-beer'],
        who=["Brewers who want a broader portfolio", "Competition brewers and future judges",
             "Beer educators and servers preparing for Cicerone"],
        outcomes=["Read a style sheet and brew to it", "Brew seven style families with intent, from lagers to sours",
                  "Pick ingredients that fit the style", "Score and enter a competition beer"],
        weeks=[
            ("How styles work", ["BJCP and Brewers Association guidelines", "Reading a style sheet: OG, FG, IBU, colour and ABV ranges", "How history, water and tax shaped styles"],
             "Profile one style of your choice against its guideline."),
            ("Lagers", ["Helles, Pilsner, Märzen and Dunkel", "Cold fermentation, diacetyl rest and lagering"],
             "Write a Pilsner recipe with a full fermentation schedule."),
            ("Wheat beers", ["Hefeweizen and witbier", "The ferulic acid rest, clove and banana", "Coriander and orange peel without overdoing them"],
             "Design a wheat beer and justify every spice and yeast choice."),
            ("British ales", ["Bitters, milds and porters", "English yeast, crystal malts and cask conditioning"],
             "Build a best bitter at under 4% ABV that still has body."),
            ("IPAs", ["English, West Coast and New England", "Hop schedules and dry hopping", "Oxygen, haze and hop creep"],
             "Write two IPA recipes from the same base malt."),
            ("Stouts and dark beers", ["Dry, sweet and imperial stouts", "Roasted barley, coffee and chocolate", "Nitro dispense"],
             "Create a stout and plan how you would serve it."),
            ("Belgian ales", ["Saison, dubbel and tripel", "Warm fermentation, phenols and candi sugar"],
             "Write a saison fermentation plan and predict its flavour."),
            ("Sours and competition brewing", ["Kettle sours and mixed fermentation", "Judging sheets and how beers are scored", "Picking and entering a competition"],
             "Submit a competition brew plan and get it critiqued."),
        ]),
    "Beer Branding & Packaging": dict(
        reading=['craft-beer-in-india', 'start-a-microbrewery-india', 'what-is-craft-beer'],
        who=["Brewery founders before launch", "Marketing and design professionals entering beer",
             "Brewers relaunching a brand"],
        outcomes=["Define who your beer is for", "Choose a pack format and brief a designer",
                  "Meet Indian labelling rules", "Plan a launch that respects advertising restrictions"],
        weeks=[
            ("Brand identity", ["Who drinks your beer, where and why", "Name, story and tone of voice", "What Indian craft brands get right and wrong"],
             "Write a one-page brand brief."),
            ("Packaging that sells", ["Can, bottle or keg: cost and trade-offs", "Label design and shelf standout", "Mandatory label content under FSSAI and state excise"],
             "Mock up a label and check it against the rules."),
            ("Launch and promotion", ["A launch plan and taproom events", "Social media and working with creators", "India's alcohol advertising restrictions and how brands work within them"],
             "Present your brand deck to the cohort for feedback."),
        ]),
    "Sensory Evaluation": dict(
        reading=['how-to-taste-beer', 'beer-off-flavours', 'beer-styles-guide'],
        who=["Brewers and QC staff", "Bartenders and beer servers",
             "Enthusiasts preparing for judging or Cicerone"],
        outcomes=["Run a proper tasting", "Name the common off-flavours and their causes",
                  "Run a triangle test", "Score beer on a structured sheet"],
        weeks=[
            ("How tasting works", ["Aroma, appearance, flavour and mouthfeel", "Glassware, serving temperature and tasting order", "Flavour chemistry and the flavour wheel"],
             "Taste a flight at home and describe each beer in writing."),
            ("Off-flavours and scoring", ["Diacetyl, DMS, acetaldehyde, oxidation, light-struck, phenolic and sulphur", "Where each fault comes from and how to fix it", "Triangle tests and BJCP-style scoresheets"],
             "Score a flight and compare your sheet with the instructor's."),
        ]),
    "AI for Craft Breweries": dict(
        reading=['beer-social-media-marketing', 'beer-brand-storytelling', 'alcohol-advertising-rules-india'],
        who=["Brewery and brewpub owners who write their own posts at midnight",
             "Taproom, marketing and sales people who handle the copy and the admin",
             "Brewers who would rather brew than fill in spreadsheets"],
        outcomes=["Brief a GenAI tool with your brewery's real facts and get copy you can actually use",
                  "Plan and draft a month of on-brand social posts in one sitting",
                  "Hand one repetitive weekly task over to AI, with a human check at the end",
                  "Write a one-page responsible AI policy for your brewery"],
        weeks=[
            ("GenAI for your brewery's words",
             ["How large language models work, in plain English, and where they go wrong",
              "Briefing the tool properly: style, ABV, ingredients, tasting notes and your brewery's voice",
              "Tap list notes, menu cards, label copy and newsletters",
              "A month of social posts around launches, festivals and the monsoon",
              "AI images versus real photos of your beer, and when each one fits"],
             "Write tasting notes for your current tap list and a month of posts, then edit them until they sound like you."),
            ("Repetitive tasks and responsible AI",
             ["Drafting replies to common questions and reviews",
              "Turning brew logs and sales notes into short weekly reports",
              "Spreadsheet formulas, checklists and first drafts of SOPs",
              "Checking every fact: AI must never invent an ABV, an award or an ingredient",
              "Customer data, image rights, and India's rules on alcohol advertising, which vary by state and change",
              "Nothing aimed at minors, and no health claims"],
             "Hand one weekly task to AI from start to finish, and write your brewery's one-page AI policy."),
        ]),
    "Digital Transformation Basics for Brewing": dict(
        reading=['keeping-a-brew-log', 'brewing-software-and-calculators', 'brewery-qc-lab-on-a-budget'],
        who=["Brewery owners still running on paper, WhatsApp and memory",
             "Head brewers who want their numbers in one place",
             "Operations and finance people at small breweries and brewpubs"],
        outcomes=["Replace the paper brew log with a digital one the whole team fills in",
                  "Track stock and batches from malt sack to keg",
                  "Build a one-page dashboard for the numbers that matter each week",
                  "Leave with a 90-day plan you can afford"],
        weeks=[
            ("From paper to data",
             ["What digital transformation means for a 10 HL brewery, and what it does not",
              "Brew logs, cellar logs and cleaning records in shared spreadsheets",
              "Stock, batch and keg tracking, and why batch codes matter when a complaint comes in",
              "Brewery management software versus spreadsheets, and when to switch"],
             "Turn last month's paper brew sheets into one digital log and find three things you did not know."),
            ("Sensors, dashboards and your plan",
             ["Temperature and gravity loggers on fermenters",
              "Point of sale and sales data next to production data",
              "A simple dashboard: volume, yield, stock and what sold",
              "Data habits: one source of truth, backups and who can edit what",
              "Planning 90 days of change your team will actually keep doing"],
             "Build your weekly dashboard and write your 90-day digital plan."),
        ]),
    "ESG in Craft Brewing": dict(
        reading=['sustainability-in-brewing', 'brewery-waste-and-spent-grain', 'brewery-utilities-water-power'],
        who=["Founders asked about sustainability by investors, retailers or customers",
             "Brewers who want to cut water, power and waste costs",
             "Brand and marketing people who need a true story, not a green label"],
        outcomes=["Measure water and energy per litre of beer from your own bills and logs",
                  "Find a better route for spent grain, yeast and packaging waste",
                  "Cover the people and governance side, not just the environment",
                  "Build a simple ESG scorecard and talk about it without greenwashing"],
        weeks=[
            ("The E: water, energy and waste",
             ["Your water to beer ratio, and where the litres go: cleaning, cooling, the brewhouse",
              "Energy for heating, cooling and glycol, and what to measure first",
              "Spent grain and yeast as feed or food rather than waste",
              "Glass, cans, kegs and returnable packaging",
              "Wastewater and pollution control consent, which varies by state"],
             "Work out your brewery's water and energy per litre from last quarter's numbers."),
            ("The S and the G, and telling the story",
             ["Staff safety, fair work and training",
              "Responsible drinking, local sourcing and your neighbourhood",
              "Governance: licences, a compliance calendar and clean books",
              "A one-page ESG scorecard you can update every quarter",
              "Talking about it honestly: what to claim, what to leave out, and how to avoid greenwashing"],
             "Fill in your first ESG scorecard and draft one honest post about it."),
        ]),
    "Safety in Brewing": dict(
        reading=['cip-cleaning-in-place', 'cleaning-vs-sanitising-brewing', 'brewery-compliance-checklist'],
        who=["Anyone starting work in a brewery or brewpub",
             "Owners setting up a new brewhouse or training new staff",
             "Homebrewers moving up to bigger kit"],
        outcomes=["Spot the hazards that hurt people in breweries before they do",
                  "Handle CO2, cleaning chemicals and hot liquids safely",
                  "Know when a tank or vessel must never be entered",
                  "Leave with a safety checklist for your own brewery"],
        weeks=[
            ("The hazards and how to work around them",
             ["CO2 from fermenting beer: why it collects low down, and gas monitors in cellars and cold rooms",
              "Confined spaces: never climb into a tank, and why",
              "Caustic and acid for cleaning, the right protective kit, and eyewash",
              "Hot wort and steam, pressure vessels, kegs and relief valves",
              "Wet floors, electrics near water, and lifting heavy malt sacks",
              "What to do in an emergency, first aid and who to call. Rules vary by state, so check the ones that apply to you"],
             "Walk through your brewery or kitchen and fill in the safety checklist we give you."),
        ]),
    "Craft Distilling": dict(
        reading=['start-a-microbrewery-india', 'yeast-growth-phases', 'brewery-compliance-checklist'],
        who=["Brewers thinking about adding spirits",
             "Founders planning a craft distillery or a gin brand",
             "Bartenders and spirits lovers who want to know how it is really made"],
        outcomes=["Explain every step from wash to bottle",
                  "Read a still and explain how a distiller makes the cuts",
                  "Design a gin botanical recipe on paper",
                  "Understand the licences and costs behind a craft distillery in India"],
        weeks=[
            ("Wash, spirits and the law",
             ["How a wash differs from beer: no hops, and the fermentation is pushed for alcohol",
              "Grain, molasses, fruit and sugar as starting points",
              "Distilling in India needs its own excise licence, separate from brewing, and rules vary by state. Distilling at home is not legal",
              "The main spirit families: whisky, gin, rum, vodka and fruit spirits"],
             "Map the licences and approvals a craft distillery needs in your state."),
            ("Stills and the run",
             ["Pot stills, column stills and reflux",
              "Heads, hearts and tails, and why the cuts matter for flavour and safety",
              "Proof, ABV and measuring a spirit",
              "Ethanol vapour, fire risk and safe still operation"],
             "Read a sample run log and mark where you would make each cut, and why."),
            ("Gin and botanicals",
             ["Juniper first: what makes a gin a gin",
              "Maceration versus vapour infusion",
              "Building a botanical bill, including Indian botanicals",
              "Dilution, proofing and bottling strength"],
             "Design a gin botanical recipe and explain the role of each botanical."),
            ("Ageing, costs and getting to market",
             ["Oak, char and what a cask adds",
              "Why maturation runs faster in Indian heat, and the higher losses to evaporation",
              "Costing a bottle: raw materials, energy, duty and packaging",
              "Brand, route to market and the first year of a small distillery"],
             "Write a one-page business case for your first spirit."),
        ]),
    "Craft Gin Making": dict(
        reading=['brewing-with-indian-spices', 'start-a-microbrewery-india', 'brewery-compliance-checklist'],
        who=["Founders planning a craft gin brand",
             "Brewers and distillers adding a gin",
             "Bartenders who want to understand what is in the bottle"],
        outcomes=["Explain the difference between distilled, London dry and compound gin",
                  "Design a botanical bill and predict how each botanical will show",
                  "Plan a still run, the cuts and proofing to bottling strength",
                  "Cost a bottle and map the licences behind it"],
        weeks=[
            ("What gin is, and the law",
             ["Juniper has to lead: what makes a gin a gin",
              "Distilled, London dry and compound gin",
              "Neutral spirit as the base, and why many Indian craft gins redistil it with botanicals",
              "Licences and contract distilling. Rules vary by state, so check yours"],
             "Taste three gins and describe what each botanical brings."),
            ("Botanicals",
             ["The classic set: juniper, coriander seed, angelica, citrus peel and orris",
              "Indian spices, citrus and teas, and how to use them without losing the juniper",
              "Maceration versus the vapour basket",
              "Distilling single botanicals and blending them"],
             "Design a botanical bill for your own gin, with the role of each one."),
            ("The run and the finish",
             ["Charging the still and running it",
              "Heads, hearts and tails, and where flavour sits in the run",
              "Reducing to bottling strength, and why oils can cloud a gin",
              "Chill filtering and resting before bottling"],
             "Plan the cuts and the reduction for a sample run."),
            ("Brand, costing and market",
             ["Costing a bottle: spirit, botanicals, energy, glass and duty",
              "Positioning against imported and other Indian gins",
              "Label registration and excise. Rules vary by state",
              "Bars, retail and your first year"],
             "Write a one-page plan for launching your gin."),
        ]),
    "RTD Drinks: Alcoholic and Non-Alcoholic": dict(
        reading=['cans-vs-bottles', 'oxygen-pickup-in-packaging', 'fssai-rules-for-beer'],
        who=["Brewers and distillers looking at canned cocktails",
             "Founders planning a soft drink, iced tea or mocktail brand",
             "Bars and cafes that want their own bottled drinks"],
        outcomes=["Formulate a balanced drink with the right sweetness and acid",
                  "Choose a spirit, malt or sugar base for an alcoholic RTD",
                  "Carbonate, can and keep a drink stable on the shelf",
                  "Know which rules apply: excise for alcohol, FSSAI for soft drinks"],
        weeks=[
            ("Formulation",
             ["Sweetness and acid in balance, measured rather than guessed",
              "Flavours, juices, extracts and teas",
              "Alcoholic bases: spirit, malt and fermented sugar",
              "Non-alcoholic RTDs: craft sodas, iced teas and mocktails"],
             "Formulate one drink with and without alcohol, and note what changes."),
            ("Production, shelf life and the rules",
             ["Carbonation levels and how they change the taste",
              "Pasteurisation, preservatives and keeping oxygen out of the can",
              "Shelf-life testing on a small budget",
              "Alcoholic RTDs fall under state excise, non-alcoholic ones under FSSAI. Rules vary and change, so check before you launch"],
             "Write a production and shelf-life plan for your drink."),
        ]),
    "Hop Water": dict(
        reading=['dry-hopping-guide', 'hop-varieties-for-beginners', 'pasteurisation-units'],
        who=["Breweries that want a zero-alcohol drink on tap",
             "Brewers curious about hops without the malt",
             "Cafes and taprooms looking for a grown-up soft drink"],
        outcomes=["Choose hops for the aroma you want",
                  "Make hop water on brewery kit, cold or warm",
                  "Keep it stable with the right pH, carbonation and heat treatment",
                  "Price and sell a zero-alcohol line"],
        weeks=[
            ("Making hop water",
             ["What hop water is: carbonated water, hops and often a little acid",
              "Choosing hops for citrus, tropical, pine or floral aroma",
              "Cold steeping, short warm steeps, hop oils and extracts",
              "Water quality, because there is nothing else in the glass to hide behind"],
             "Make a small batch with two hop varieties and compare them."),
            ("Stability and selling it",
             ["Lowering pH with acid for a safer, brighter drink",
              "Carbonation, kegging and canning on brewery kit",
              "Heat treatment, because with no alcohol there is nothing to protect it",
              "Labelling under FSSAI, pricing and where it sells"],
             "Write a recipe and a stability plan for your hop water."),
        ]),
    "Hard Seltzer": dict(
        reading=['pitching-yeast-properly', 'yeast-growth-phases', 'carbonation-levels-by-style'],
        who=["Brewers with spare tank space",
             "Founders looking at light, low-calorie drinks",
             "Homebrewers who want a clean ferment to practise on"],
        outcomes=["Build a sugar base and feed the yeast properly",
                  "Run a clean, neutral fermentation without sulphur or off-flavours",
                  "Clarify, flavour and balance the finished seltzer",
                  "Know how seltzer is classed and taxed. It varies by state"],
        weeks=[
            ("Base and fermentation",
             ["Cane sugar or dextrose as the base",
              "Why a sugar wash starves yeast, and how to add nutrient in stages",
              "Yeast choice, temperature and pH for a clean ferment",
              "Sulphur and other faults, and how to avoid them"],
             "Plan a fermentation schedule with your nutrient additions."),
            ("Finish and the rules",
             ["Clarity: settling, fining and filtration",
              "Flavour, acid and a touch of sweetness",
              "Carbonation and canning",
              "How seltzer is classed and taxed in India, which varies by state"],
             "Design a flavour range of three seltzers from one base."),
        ]),
    "Kombucha": dict(
        reading=['cleaning-vs-sanitising-brewing', 'sour-infection-off-flavour', 'brettanomyces-explained'],
        who=["Cafe and taproom owners who want their own kombucha",
             "Home fermenters ready to brew consistently",
             "Brewers curious about mixed fermentation"],
        outcomes=["Brew kombucha from tea, sugar and a healthy culture",
                  "Keep it safe: pH, hygiene and telling mould from culture",
                  "Flavour and carbonate it in a second ferment",
                  "Scale up and label it, keeping alcohol in check"],
        weeks=[
            ("The first ferment",
             ["Tea, sugar and the culture of yeast and bacteria",
              "Starter liquid and getting pH down fast for safety",
              "Temperature, time and tasting for sourness",
              "Mould versus a healthy culture, and when to throw a batch away"],
             "Start a batch and log pH and taste every day."),
            ("Flavour, fizz and scaling up",
             ["Second ferment with fruit, spices and herbs",
              "Carbonation in the bottle, and how to keep bottles from bursting",
              "Alcohol can creep up in warm conditions, so measure it",
              "Scaling up, hygiene and FSSAI labelling. Rules change, so check the current ones"],
             "Plan a three-flavour range and a weekly brewing schedule."),
        ]),
}


N_COURSES = pages_a.COURSE_COUNT_WORD
TOTAL_WEEKS = sum(c["weeks"] for c in pages_a.COURSE_DATA)


FREE_FEES = "Free. Register to hold one of the 20 seats in the next batch."


def is_free(c):
    return c["amount"] == "0"


def plain(name):
    return name.replace("&amp;", "&")


def _week(i, title, topics, task):
    lis = "".join(f"<li>{t}</li>" for t in topics)
    return f"""<details class="reveal"{' open' if i == 1 else ''}><summary>Week {i:02d}. {title}</summary>
<div class="wk"><ul class="checklist">{lis}</ul>
<p class="wk-task"><b>Assignment:</b> {task}</p></div></details>"""


def _ctas(enrol, tag):
    return (f'<a href="{enrol}" class="btn btn-amber" data-cta="course-{tag}-enroll">Enrol now</a>'
            f'<a href="__WA__" class="btn btn-wa" target="_blank" rel="noopener" data-cta="course-{tag}-whatsapp">[[whatsapp]] Ask on WhatsApp</a>')


def render(c):
    d = DETAIL[plain(c["name"])]
    weeks = "".join(_week(i, *w) for i, w in enumerate(d["weeks"], 1))
    who = "".join(f"<li>{w}</li>" for w in d["who"])
    out = "".join(f"<li>{o}</li>" for o in d["outcomes"])
    logi = "".join(f"<div><dt>{k}</dt><dd>{FREE_FEES if k == 'Fees' and is_free(c) else v}</dd></div>" for k, v in LOGISTICS)
    enrol = enroll_href(c["name"])
    return banner(f'<a href="courses.html">Courses</a> / {c["name"]}', f'{c["no"]} / {c["tag"]}', c["name"], c["blurb"]) + f"""
<section style="padding-block:0">
  <div class="wrap course-facts">
    <div><span>Duration</span><b>{c["dur"]}</b></div>
    <div><span>Sessions</span><b>{c["weeks"] * 2} live, 2 hours each</b></div>
    <div><span>Batch</span><b>Max 20</b></div>
    <div><span>Fee</span><b>{c["price"]}</b></div>
    <div class="cta-pair">{_ctas(enrol, "facts")}</div>
  </div>
</section>

<section>
  <div class="wrap split" style="align-items:start">
    <div class="prose-block reveal"><span class="eyebrow">Who it is for</span><h2>Is this for you?</h2><ul class="checklist">{who}</ul></div>
    <div class="prose-block reveal"><span class="eyebrow">By the end</span><h2>What you walk away with.</h2><ul class="checklist">{out}</ul></div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Syllabus</span><h2>Week by week.</h2><p class="lead">{c["weeks"]} week{"s" if c["weeks"] != 1 else ""}. Two live sessions every weekend and one assignment a week.</p></div>
    <div class="faq syllabus">{weeks}</div>
    <aside class="cta-inline" style="margin-top:2.4rem">
      <div><h3>Questions about the syllabus?</h3><p>Ask us on WhatsApp before you commit, or enrol now to hold your seat.</p></div>
      <div class="cta-pair">{_ctas(enrol, "syllabus")}</div>
    </aside>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">How it runs</span><h2>Format and terms.</h2></div>
    <dl class="logistics">{logi}</dl>
    <p style="margin-top:1.5rem;color:var(--ink-soft);font-size:.9rem">Want the full flight? All {N_COURSES} courses together run to {TOTAL_WEEKS} weeks, and you choose your package when you enrol. Compare <a href="courses.html" style="color:var(--blue);text-decoration:underline">all {N_COURSES} courses</a>, and read the <a href="refund.html" style="color:var(--blue);text-decoration:underline">refund policy</a> before you pay.</p>
  </div>
</section>

{article_render._related({"related": d["reading"]}, ARTICLES_BY_SLUG).replace("Related guides", "Read before you start").replace('data-cta="related-article"', 'data-cta="course-reading"')}

<section class="cta"><div class="wrap"><h2>Save your seat in {c["name"]}.</h2><p>Cohorts cap at 20. Enrol now or ask us on WhatsApp.</p><div class="cta-pair" style="justify-content:center">{_ctas(enrol, "bottom")}</div></div></section>
"""


def pages():
    """slug -> (title, desc, active, body) for build.PAGES."""
    out = {}
    for c in pages_a.COURSE_DATA:
        name = plain(c["name"])
        title = f"{name} Course | Craft Beer School"
        if len(title) > 60:  # search results cut long titles; fall back to the short name
            title = f"{c.get('short', name)} | Craft Beer School"
        desc = (f"{name}: {c['dur'].lower()} of live weekend classes online, max 20 per batch, "
                f"{'free' if is_free(c) else c['price']}. Full week-by-week syllabus, assignments and certificate.")
        out[slug_for(c["name"])] = (title, desc, "courses", render(c))
    return out
