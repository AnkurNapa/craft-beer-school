# -*- coding: utf-8 -*-
"""One detail page per online course: who it is for, week-by-week syllabus,
logistics and terms.

Price, duration and the card bullets come from pages_a.COURSE_DATA so a detail
page can never quote a different fee than the courses grid. Logistics and terms
mirror the "CBS Online Courses 2026" brochure.
"""
import re

import pages_a
from pages_a import banner, course_href as slug_for, enroll_href

# Shared across every course, straight from the 2026 brochure.
LOGISTICS = [
    ("Schedule", "Live on Saturdays and Sundays, 12:00 PM to 2:00 PM IST. Timings may shift by mutual agreement with the cohort."),
    ("Batch size", "Maximum 20 students, so every question gets answered."),
    ("Included", "Session recordings, presentation decks, weekly assignments and the learning kit."),
    ("Certificate", "Certificate of Completion once every assignment is in and you have attended at least 80% of live sessions."),
    ("Beyond the screen", "Recommended microbrewery visits so you see the kit you are studying."),
    ("Fees", "100% at sign-up. No discounts apply, and a package of courses is fixed once confirmed."),
]

# name (plain text, as in the contact form) -> detail
DETAIL = {
    "Brewing Fundamentals": dict(
        who=["Homebrewers who want to know why a batch worked, not just that it did",
             "Beer lovers ready to brew their first real recipe",
             "Hospitality and sales people who talk about beer every day"],
        outcomes=["Explain every step from mill to package", "Build a 20 L recipe with target OG, IBU and colour",
                  "Clean and sanitise like a professional brewery", "Calculate ABV from your own gravity readings"],
        weeks=[
            ("Grain to glass", ["The four ingredients and what each one does", "The brewhouse map: mill, mash, lauter, boil, whirlpool, ferment, condition, package", "Reading a label: ABV, IBU and colour (EBC and SRM)"],
             "Taste three commercial beers and trace each one back to its ingredients."),
            ("Malt, water and the mash", ["Malting: steep, germinate, kiln", "Base malts versus speciality malts", "Enzymes and mash temperature: 62 to 65 °C for a dry beer, 68 to 70 °C for more body", "Water basics and a mash pH of 5.2 to 5.6"],
             "Work out the grist and strike water for a 20 L batch."),
            ("Hops, boil and yeast", ["Alpha acids and why they only bitter in the boil", "Bittering, aroma and dry hop additions", "What the boil does: sterilise, isomerise, drive off DMS, form the hot break", "Ale versus lager yeast, pitch rates and temperature control"],
             "Calculate the IBU of your recipe."),
            ("Sanitation, kit and your first recipe", ["Cleaning is not sanitising: the difference and the chemicals", "Homebrew kit versus a microbrewery brewhouse", "Original and final gravity, and ABV = (OG - FG) x 131.25", "Priming, carbonation and packaging"],
             "Present your first complete recipe to the cohort."),
        ]),
    "Advanced Brewing Science": dict(
        who=["Working brewers and assistant brewers", "Graduates of Brewing Fundamentals",
             "Serious homebrewers chasing consistency"],
        outcomes=["Build a brewing water profile from a lab report", "Measure and improve brewhouse efficiency",
                  "Control esters, fusels and diacetyl through fermentation", "Write a QA plan for a small brewery"],
        weeks=[
            ("Brewing water chemistry", ["Calcium, magnesium, sulphate, chloride and bicarbonate", "Residual alkalinity and the sulphate to chloride ratio", "Treating borewell and municipal water in India, RO blending"],
             "Turn your local water report into a treatment plan for two styles."),
            ("Mash chemistry and advanced mashing", ["Step mashes, protein rests and decoction", "Rice and maize adjuncts, and cooking them", "Extract, lauter yield and brewhouse efficiency"],
             "Calculate brewhouse efficiency from a real brew log."),
            ("Hop chemistry", ["Alpha and beta acids, isomerisation and utilisation", "Hop oils: myrcene, linalool, geraniol", "Biotransformation and hop creep"],
             "Redesign a hop schedule for the same IBU with more aroma."),
            ("Yeast and fermentation microbiology", ["Lag, growth and stationary phases", "Esters and fusels versus fermentation temperature", "Diacetyl, the diacetyl rest and acetaldehyde", "Oxygenation, propagation and harvesting"],
             "Plot a fermentation from gravity and temperature logs and call the faults."),
            ("Contamination, stability and shelf life", ["Lactobacillus, Pediococcus and wild yeast", "Oxygen pickup and staling", "Haze, finings, filtration and pasteurisation units", "Holding beer through an Indian summer supply chain"],
             "Audit a packaging line for oxygen and infection risk."),
            ("Quality assurance and control", ["A QC lab on a small budget: hydrometer, pH meter, microscope, forcing tests", "Specs, tolerances, SOPs and brew logs", "HACCP basics and FSSAI"],
             "Write the QA plan for a 500 L brewery."),
        ]),
    "Brewery Business Management": dict(
        who=["Founders planning a brewpub or microbrewery", "Investors sizing up a beer business",
             "Brewers stepping into management"],
        outcomes=["Choose between brewpub, microbrewery and contract brewing", "Build a cost per litre and a break-even",
                  "Map the licences your state requires", "Pick a route to market"],
        weeks=[
            ("Plan and finance", ["Brewpub, microbrewery or contract brewing", "Capex: brewhouse, cellar, cooling and utilities", "Opex, cost per litre, pricing and break-even", "Funding options"],
             "Build a simple P&amp;L for your concept."),
            ("Licensing and regulation in India", ["Excise is state by state: what that means for you", "Brewpub and microbrewery licences, FSSAI, pollution control consent", "Label registration, trademarks and realistic timelines"],
             "Draw up a licence checklist and timeline for your state."),
            ("Market, brand and distribution", ["Positioning and taproom economics", "On-trade versus off-trade, distributors and state rules", "Kegs versus cans"],
             "Present a one-page business plan to the cohort."),
        ]),
    "Style Specialization": dict(
        who=["Brewers who want a broader portfolio", "Competition brewers and future judges",
             "Beer educators and servers preparing for Cicerone"],
        outcomes=["Read a style sheet and brew to it", "Brew lagers, wheat beers, British ales, IPAs, stouts, Belgians and sours with intent",
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
        who=["Brewery founders before launch", "Marketing and design professionals entering beer",
             "Brewers relaunching a brand"],
        outcomes=["Define who your beer is for", "Choose a pack format and brief a designer",
                  "Meet Indian labelling rules", "Plan a launch that respects advertising restrictions"],
        weeks=[
            ("Brand identity", ["Who drinks it, where, and why", "Name, story and tone of voice", "What Indian craft brands get right and wrong"],
             "Write a one-page brand brief."),
            ("Packaging that sells", ["Can, bottle or keg: cost and trade-offs", "Label design and shelf standout", "Mandatory label content under FSSAI and state excise"],
             "Mock up a label and check it against the rules."),
            ("Launch and promotion", ["A launch plan and taproom events", "Social media and creators", "India's alcohol advertising restrictions and how brands work within them"],
             "Present your brand deck to the cohort."),
        ]),
    "Sensory Evaluation": dict(
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
}


def plain(name):
    return name.replace("&amp;", "&")


def _week(i, title, topics, task):
    lis = "".join(f"<li>{t}</li>" for t in topics)
    return f"""<details class="reveal"{' open' if i == 1 else ''}><summary>Week {i:02d}. {title}</summary>
<div class="wk"><p class="wk-meta">2 live sessions, Saturday and Sunday</p><ul class="checklist">{lis}</ul>
<p class="wk-task"><b>Assignment:</b> {task}</p></div></details>"""


def render(c):
    d = DETAIL[plain(c["name"])]
    weeks = "".join(_week(i, *w) for i, w in enumerate(d["weeks"], 1))
    who = "".join(f"<li>{w}</li>" for w in d["who"])
    out = "".join(f"<li>{o}</li>" for o in d["outcomes"])
    logi = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in LOGISTICS)
    enrol = enroll_href(c["name"])
    return banner(f'<a href="courses.html">Courses</a> / {c["name"]}', f'{c["no"]} / {c["tag"]}', c["name"], c["blurb"]) + f"""
<section style="padding-block:0">
  <div class="wrap course-facts">
    <div><span>Duration</span><b>{c["dur"]}</b></div>
    <div><span>Sessions</span><b>{c["weeks"] * 2} live, 2 hrs each</b></div>
    <div><span>Batch</span><b>Max 20</b></div>
    <div><span>Fee</span><b>{c["price"]}</b></div>
    <a href="{enrol}" class="btn btn-amber" data-cta="course-page-enroll">Enrol in this course</a>
  </div>
</section>

<section>
  <div class="wrap split" style="align-items:start">
    <div class="prose-block reveal"><span class="eyebrow">Who it is for</span><h2>Built for you if you are&hellip;</h2><ul class="checklist">{who}</ul></div>
    <div class="prose-block reveal"><span class="eyebrow">By the end</span><h2>You will be able to&hellip;</h2><ul class="checklist">{out}</ul></div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Syllabus</span><h2>Week by week.</h2><p class="lead">{c["weeks"]} weeks, two live sessions every weekend, one assignment a week.</p></div>
    <div class="faq syllabus">{weeks}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">How it runs</span><h2>Format and terms.</h2></div>
    <dl class="logistics">{logi}</dl>
    <p style="margin-top:1.5rem;color:var(--ink-soft);font-size:.9rem">Want the full flight? All six courses run to 26 weeks. Packages are chosen at enrolment. See the <a href="refund.html" style="color:var(--blue);text-decoration:underline">refund policy</a> and <a href="courses.html" style="color:var(--blue);text-decoration:underline">all courses</a>.</p>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Save your seat in {c["name"]}.</h2><p>Cohorts cap at 20. Enrol now or ask us on WhatsApp.</p><a href="{enrol}" class="btn btn-amber" data-cta="course-page-enroll-bottom">Enrol now</a></div></section>
"""


def pages():
    """slug -> (title, desc, active, body) for build.PAGES."""
    out = {}
    for c in pages_a.COURSE_DATA:
        name = plain(c["name"])
        title = f"{name} Course | Craft Beer School"
        desc = (f"{name}: {c['dur'].lower()} of live weekend classes online, max 20 per batch, "
                f"{c['price']}. Full week-by-week syllabus, assignments and certificate.")
        out[slug_for(c["name"])] = (title, desc, "courses", render(c))
    return out
