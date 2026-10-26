# -*- coding: utf-8 -*-
"""Page bodies: Home, About, Courses, Resources, Blog."""

import re

import style_render
import brew_floor
import photos
from urllib.parse import quote


def enroll_href(course_name):
    """Enrol link that pre-selects this course in the contact form."""
    plain = course_name.replace("&amp;", "&")
    return f"contact.html?course={quote(plain)}#enroll"


def course_href(course_name):
    """Detail page for a course, e.g. brewing-fundamentals-course.html."""
    # British display name, but the live URL keeps its original z spelling.
    plain = course_name.replace("&amp;", "&").lower().replace("specialisation", "specialization")
    return re.sub(r"[^a-z0-9]+", "-", plain).strip("-") + "-course.html"


# ---- shared course card snippets -------------------------------------------
# How each course is taught. Online unless listed: Brewing Fundamentals also
# has an in-person version too.
MODE = {"Brewing Fundamentals": "Both", "Winemaking": "Both", "Fortified Wine": "Both", "Winery Business": "Both",
        "New Product Development: Beer, Whisky and Wine": "Both", "Wine Consultation": "Both"}
MODE_LABEL = {"Online": "Online", "In person": "In person", "Both": "Online + in person"}


# Course finder on courses.html: every card carries a type (online, in-person, study, free, exam)
# and a subject, so readers can cut 30-odd cards down to the kind they want (Ankur, 18 Oct 2026).
SUBJECTS = [("brewing", "Brewing"), ("tasting", "Tasting"), ("business", "Business and brand"),
            ("data", "Data and AI"), ("spirits-wine", "Spirits and wine"), ("other-drinks", "Other drinks")]
SUBJECT = {"Brewing Fundamentals": "brewing", "Advanced Brewing Science": "brewing", "Style Specialisation": "brewing",
           "Safety in Brewing": "brewing", "Sensory Evaluation": "tasting", "Brewery Business Management": "business",
           "Beer Branding &amp; Packaging": "business", "ESG in Craft Brewing": "business",
           "New Product Development: Beer, Whisky and Wine": "business", "Digital Marketing for Breweries": "business",
           "Brand Strategy and Positioning for Breweries": "business", "Rebranding a Brewery": "business",
           "Naming and Trademarks for Drinks Brands": "business", "Taproom Marketing and Community": "business",
           "AI for Craft Breweries": "data", "Digital Transformation Basics for Brewing": "data",
           "Power BI and Tableau for Breweries": "data", "Craft Distilling": "spirits-wine", "Craft Gin Making": "spirits-wine", "Whisky Appreciation": "spirits-wine", "Wine Consultation": "spirits-wine",
           "Winemaking": "spirits-wine", "Fortified Wine": "spirits-wine", "Winery Business": "spirits-wine",
           "RTD Drinks: Alcoholic and Non-Alcoholic": "other-drinks", "Hop Water": "other-drinks",
           "Hard Seltzer": "other-drinks", "Kombucha": "other-drinks", "Non-Alcoholic Beer": "other-drinks"}


def course_types(name, price):
    mode = MODE.get(name, "Online")
    types = {"Online": "online", "In person": "in-person", "Both": "online in-person"}[mode]
    return types + (" free" if price == "Free" else "")


def mode_tag(mode):
    return f'<span class="mode mode-{mode.lower().replace(" ", "-")}">{MODE_LABEL[mode]}</span>'


def course(no, tag, dur, name, blurb, items, price, ph):
    lis = "".join(f"<li>{i}</li>" for i in items)
    tile = photos.stock_img("course:" + course_href(name)[:-len("-course.html")], name, "tile-img")
    return f"""<article class="card course-card reveal" data-type="{course_types(name, price)}" data-subject="{SUBJECT[name]}">{tile}
  <div class="top"><span class="course-no">{no} / {tag}</span><span class="course-dur">{dur}</span></div>
  <div class="card-body">
    {mode_tag(MODE.get(name, "Online"))}
    <h3><a href="{course_href(name)}">{name}</a></h3>
    <p>{blurb}</p>
    <ul>{lis}</ul>
    <a href="{course_href(name)}" class="link-arrow" data-cta="course-syllabus">Full syllabus</a>
    <div class="foot"><span class="price">{price}</span><a href="{enroll_href(name)}" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="course-enroll" aria-label="Enrol in {name}">Enrol</a></div>
  </div>
</article>"""

# Course records drive both the cards and the Course JSON-LD in seo.py, so the
# structured data can never drift from what is on the page.
COURSE_DATA = [
    dict(no="01", tag="Foundations", dur="4 Weeks", weeks=4, name="Brewing Fundamentals",
         blurb="The science of brewing: ingredients, equipment and technique. Live online sessions, plus your first real recipe.",
         items=["Brewing science and theory","Raw materials and quality","Equipment and sanitation","Recipe formulation basics"],
         price="₹5,999", amount="5999"),
    dict(no="02", tag="Deep Craft", dur="6 Weeks", weeks=6, name="Advanced Brewing Science",
         blurb="Go deeper into brewing chemistry, microbiology and fermentation. For serious homebrewers and professionals.",
         items=["Microbiology and fermentation","Water chemistry optimisation","Advanced mashing techniques","Quality assurance and control"],
         price="₹12,999", amount="12999"),
    dict(no="03", tag="Business", dur="3 Weeks", weeks=3, name="Brewery Business Management",
         blurb="The business behind the brew: plan, launch and grow a brewery, from finance to distribution.",
         items=["Business planning and finance","Licensing and regulations","Marketing and branding","Distribution strategies"],
         price="₹8,999", amount="8999"),
    dict(no="04", tag="Mastery", dur="8 Weeks", weeks=8, name="Style Specialisation",
         blurb="Master IPAs, stouts, lagers, sours and Belgian ales: their history, technique and award-winning examples.",
         items=["Style guidelines &amp; origins","Specialised techniques","Ingredient selection &amp; pairing","Competition brewing skills"],
         price="₹18,999", amount="18999"),
    dict(no="05", tag="Brand", dur="3 Weeks", weeks=3, name="Beer Branding &amp; Packaging",
         blurb="Build a beer brand that stands out and packaging that sells. Made for aspiring brewers and founders.",
         items=["Build your brand identity","Design packaging that pops","Launch planning &amp; promotion","Certificate &amp; community access"],
         price="₹4,999", amount="4999"),
    dict(no="06", tag="Palate", dur="2 Weeks", weeks=2, name="Sensory Evaluation",
         blurb="Train your palate like a pro: taste, identify off-flavours and score beer with real sensory methods.",
         items=["Flavour chemistry","Tasting techniques","Off-flavour identification","Quality scoring systems"],
         price="₹5,999", amount="5999"),
    dict(no="07", tag="New · AI", dur="2 Weeks", weeks=2, name="AI for Craft Breweries",
         blurb="Put GenAI to work on your brewery's copy, social posts and weekly admin and use it responsibly. No coding needed.",
         items=["GenAI for beer copy &amp; social","Prompting with your brewery's facts","Automating repetitive tasks","Responsible AI &amp; alcohol ad rules"],
         price="₹5,000", amount="5000"),
    dict(no="08", tag="New · Digital", dur="2 Weeks", weeks=2, name="Digital Transformation Basics for Brewing",
         short="Digital Transformation for Brewing",
         blurb="Move your brewery off paper and into simple digital tools: brew logs, stock, batch tracking and a dashboard you will actually open.",
         items=["Paper to digital brew logs","Stock and batch tracking","Sensors and dashboards","A 90-day digital plan"],
         price="₹5,000", amount="5000"),
    dict(no="09", tag="New · ESG", dur="2 Weeks", weeks=2, name="ESG in Craft Brewing",
         blurb="Water, energy, spent grain, packaging, people and governance: measure what your brewery does and tell the story honestly.",
         items=["Water and energy per litre","Spent grain, waste and packaging","People, safety and community","A simple ESG scorecard"],
         price="₹5,000", amount="5000"),
    dict(no="10", tag="Free · Safety", dur="1 Week", weeks=1, name="Safety in Brewing",
         blurb="The hazards that hurt people in breweries and how to work around them: CO2, chemicals, heat, pressure and confined spaces.",
         items=["CO2 and confined spaces","Caustic, acid and hot liquids","Pressure, kegs and lifting","Your brewery safety checklist"],
         price="Free", amount="0"),
    dict(no="11", tag="New · Spirits", dur="4 Weeks", weeks=4, name="Craft Distilling",
         blurb="From wash to bottle: stills, cuts, gin botanicals, ageing in Indian heat and the licences a craft distillery needs.",
         items=["Wash, stills and the run","Heads, hearts and tails","Gin and botanicals","Ageing, costs and licensing"],
         price="₹9,999", amount="9999"),
    dict(no="12", tag="New · Spirits", dur="4 Weeks", weeks=4, name="Craft Gin Making",
         blurb="Design and make a gin of your own: juniper and botanicals, the still run, proofing and getting a bottle to market in India.",
         items=["What makes a gin a gin","Botanicals, including Indian ones","Distilling, cuts and proofing","Brand, costing and licences"],
         price="₹9,999", amount="9999"),
    dict(no="13", tag="New · RTD", dur="2 Weeks", weeks=2, name="RTD Drinks: Alcoholic and Non-Alcoholic",
         short="RTD Drinks Course",
         blurb="Ready-to-drink cans and bottles, with and without alcohol: formulation, sweetness and acid, carbonation, shelf life and the rules.",
         items=["Formulating for flavour and balance","Spirit, malt and sugar bases","Carbonation, canning and shelf life","Excise and FSSAI labelling"],
         price="₹5,000", amount="5000"),
    dict(no="14", tag="New · Non-alcoholic", dur="2 Weeks", weeks=2, name="Hop Water",
         blurb="Sparkling water with all the aroma of hops and none of the alcohol. Make it on brewery kit and keep it stable on the shelf.",
         items=["Choosing hops for aroma","Cold steeping, oils and extracts","pH, carbonation and stability","Selling a zero-alcohol line"],
         price="₹5,000", amount="5000"),
    dict(no="15", tag="New · Seltzer", dur="2 Weeks", weeks=2, name="Hard Seltzer",
         blurb="A clean, dry sugar ferment turned into a light, fruity seltzer: base, yeast nutrition, clarity, flavour and the rules in India.",
         items=["Sugar base and yeast nutrition","A clean, neutral fermentation","Clarity, flavour and acid","Packaging and excise"],
         price="₹5,000", amount="5000"),
    dict(no="16", tag="New · Ferments", dur="2 Weeks", weeks=2, name="Kombucha",
         blurb="Brew kombucha safely and consistently, from tea, sugar and culture to flavoured, sparkling bottles for a cafe or taproom.",
         items=["Tea, sugar and the culture","Safe pH and clean brewing","Second ferment and flavour","Scaling up and labelling"],
         price="₹5,000", amount="5000"),
    dict(no="17", tag="New · Non-alcoholic", dur="2 Weeks", weeks=2, name="Non-Alcoholic Beer",
         blurb="Beer that still tastes like beer, without the alcohol: limited fermentation, special yeasts, body and aroma, plus keeping it safe on the shelf.",
         items=["Limited fermentation and special yeasts","Dealcoholisation and when it makes sense","Body, aroma and avoiding a worty taste","Pasteurisation, testing and labelling"],
         price="₹5,000", amount="5000"),
    dict(no="18", tag="New · Data", dur="2 Weeks", weeks=2, name="Power BI and Tableau for Breweries",
         short="Power BI and Tableau for Breweries",
         blurb="Build the dashboards a brewery actually opens: brew logs, yield, losses, stock and sales in Power BI or Tableau, from your own spreadsheets.",
         items=["Brewery data model from your logs","Yield, loss and KPI dashboards","Power BI and Tableau side by side","A dashboard your team will keep"],
         price="₹5,000", amount="5000"),
    dict(no="19", tag="New · Wine", dur="2 Weeks", weeks=2, name="Winemaking",
         blurb="Grape to bottle: harvest numbers, crushing and pressing, red and white fermentation, malolactic, clarifying and bottling, for Indian vineyards and climate.",
         items=["Grapes, sugar and acid at harvest","Red and white fermentation","Malolactic, clarifying and ageing","Bottling and stability"],
         price="₹5,000", amount="5000"),
    dict(no="20", tag="New · Wine", dur="2 Weeks", weeks=2, name="Fortified Wine",
         blurb="How port-style, sherry-style and other fortified wines are made: fortifying with grape spirit, sweetness, oxidative ageing and blending.",
         items=["Fortifying with grape spirit","Sweet and dry styles","Oxidative and barrel ageing","Blending, costing and the rules"],
         price="₹5,000", amount="5000"),
    dict(no="21", tag="New · Wine", dur="2 Weeks", weeks=2, name="Winery Business",
         blurb="Run a small winery as a business: costing a bottle, licences and excise, route to market, cellar door and wine tourism in India.",
         items=["Costing a bottle of wine","Licences, excise and labels","Route to market and pricing","Cellar door and wine tourism"],
         price="₹5,000", amount="5000"),
    dict(no="22", tag="New · Product", dur="2 Weeks", weeks=2, name="New Product Development: Beer, Whisky and Wine",
         short="New Product Development",
         blurb="Take a new beer, whisky or wine from idea to launch: consumer insight, formulation, pilot batches, sensory testing, costing, labels and launch.",
         items=["Finding the gap and the drinker","Formulation and pilot batches","Sensory testing and costing","Labels, approvals and launch"],
         price="₹5,000", amount="5000"),
    dict(no="23", tag="New · Marketing", dur="2 Weeks", weeks=2, name="Digital Marketing for Breweries",
         short="Digital Marketing for Breweries Course",
         blurb="Market a brewery online inside India's alcohol advertising rules: Instagram, WhatsApp, Google listings and content that fills a taproom.",
         items=['What the ad rules allow online', 'Instagram, reels and creators', 'WhatsApp, Google listings and reviews', 'A content calendar and the numbers to watch'],
         price="₹5,000", amount="5000"),
    dict(no="24", tag="New · Brand", dur="2 Weeks", weeks=2, name="Brand Strategy and Positioning for Breweries",
         short="Brand Strategy and Positioning Course",
         blurb="Work out who your brewery is for and why it is different, then write it down so every label, post and pint says the same thing.",
         items=['Positioning against your real competition', 'Values a team will actually use', 'Drinker personas without stereotypes', 'A one-line brand essence'],
         price="₹5,000", amount="5000"),
    dict(no="25", tag="New · Brand", dur="2 Weeks", weeks=2, name="Rebranding a Brewery",
         blurb="Plan a rebrand that keeps the drinkers you have: audit, goals, budget, the design brief and a roll-out timed to new labels and approvals.",
         items=['Refresh or full rebrand', 'Brand audit and what drinkers remember', 'Goals, team and budget', 'Roll-out, labels and launch day'],
         price="₹5,000", amount="5000"),
    dict(no="26", tag="New · Brand", dur="2 Weeks", weeks=2, name="Naming and Trademarks for Drinks Brands",
         short="Naming and Trademarks Course",
         blurb="Find a brewery or beer name people can say, spell and remember, then check it is free to use before you print a single label.",
         items=['What makes a name work', 'Testing a shortlist', 'Trade mark searches in India', 'Filing with an attorney, step by step'],
         price="₹5,000", amount="5000"),
    dict(no="27", tag="New · Marketing", dur="2 Weeks", weeks=2, name="Taproom Marketing and Community",
         short="Taproom Marketing Course",
         blurb="Turn first visits into regulars: events, beer clubs, staff who live the brand and local partnerships for a taproom or brewpub.",
         items=['Events that bring people back', 'Beer clubs and regulars', 'Staff as the brand', 'Local partners and collaborations'],
         price="₹5,000", amount="5000"),
    dict(no="28", tag="New · Whisky", dur="2 Weeks", weeks=2, name="Whisky Appreciation",
         blurb="Learn whisky the way a blender tastes it: how it is made, the main styles of the world and a tasting method you can use on any glass, with Indian whisky in the mix.",
         items=["How whisky is made", "Styles of the world, India included", "Tasting with a method", "Serving, food and buying well"],
         price="₹5,000", amount="5000"),
    dict(no="29", tag="New · One to one", dur="2 Weeks", weeks=2, name="Wine Consultation",
         blurb="One-to-one sessions on wine, online or in person in Pune, Delhi, Gurugram or Bengaluru, built around your own questions or project.",
         items=["Built around your own questions", "Making, tasting, buying or selling wine", "Online or in person in 4 cities", "A plan for your next step"],
         price="₹25,000", amount="25000"),
]

COURSE_CARDS = [
    course(c["no"], c["tag"], c["dur"], c["name"], c["blurb"], c["items"], c["price"], "")
    for c in COURSE_DATA
]

# Home page tracks. Every course must sit in exactly one, so a new course can
# never go missing from the home page: the assert below stops the build.
TRACKS = [
    ("beer", "Brewing", "From your first batch to a judge's palate.",
     ["Brewing Fundamentals", "Advanced Brewing Science", "Style Specialisation", "Sensory Evaluation"]),
    ("briefcase", "Business and tech", "Run, market and modernise a brewery.",
     ["Brewery Business Management", "AI for Craft Breweries",
      "Digital Transformation Basics for Brewing", "ESG in Craft Brewing", "Power BI and Tableau for Breweries"]),
    ("megaphone", "Brand and marketing", "Build, name and market a brewery brand people remember.",
     ["Beer Branding &amp; Packaging", "Digital Marketing for Breweries", "Brand Strategy and Positioning for Breweries", "Rebranding a Brewery", "Naming and Trademarks for Drinks Brands", "Taproom Marketing and Community"]),
    ("martini", "Spirits", "Whisky, distilling and gin, from wash to glass.",
     ["Whisky Appreciation", "Craft Distilling", "Craft Gin Making"]),
    ("glass-water", "Beyond beer", "Alcohol-free, low-alcohol and the other ferments people are buying now.",
     ["Non-Alcoholic Beer", "RTD Drinks: Alcoholic and Non-Alcoholic", "Hop Water", "Hard Seltzer", "Kombucha"]),
    ("wine", "Wine and new products", "Make wine, run a winery and launch new drinks.",
     ["Winemaking", "Fortified Wine", "Winery Business", "Wine Consultation", "New Product Development: Beer, Whisky and Wine"]),
    ("map-pin", "Free and in Bengaluru", "Start free, or learn in the room with us.",
     ["Safety in Brewing"]),
]
_by_name = {c["name"]: c for c in COURSE_DATA}
_placed = [n for *_, names in TRACKS for n in names]
assert sorted(_placed) == sorted(_by_name), f"courses missing from TRACKS: {set(_by_name) - set(_placed)}"


def _track_course(c):
    return (f'<li><a href="{course_href(c["name"])}">{c["name"]}</a>'
            f'<span>{c["dur"]} · {c["price"]}</span></li>')


def tracks_section():
    tiles = []
    for icon, title, line, names in TRACKS:
        items = "".join(_track_course(_by_name[n]) for n in names)
        if title == "Brewing":
            items += '<li><a href="courses.html#wset">WSET Beer exam prep</a><span>In person, group or one-to-one</span></li>'
        if title.startswith("Free"):
            items += ('<li><a href="professional-beer-tasting-day-in-person.html">Professional Beer Tasting Day</a><span>1 Day · ₹4,999</span></li>'
                      '<li><a href="brewery-business-tour-in-person.html">Brewery Business Tour</a><span>Half day · On enquiry</span></li>'
                      '<li><a href="in-person-brewing-courses-pune-delhi-gurugram-bengaluru.html">1-day and 1-month brewing courses</a><span>Pune, Delhi, Gurugram, Bengaluru</span></li>')
        slot = {"Brewing": "track:brewing", "Business and tech": "track:business", "Spirits": "track:spirits",
                "Beyond beer": "track:beyond", "Wine and new products": "track:wine",
                "Brand and marketing": "track:brand"}.get(title, "track:bengaluru")
        tiles.append(f"""<article class="track reveal">{photos.figure(slot, title, "photo track-photo")}
        <div class="track-head"><span class="ic">[[{icon}]]</span><div><h3>{title}</h3><p>{line}</p></div></div>
        <ul class="track-list">{items}</ul>
      </article>""")
    return f"""
<section class="sand" id="tracks">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Every course</span>
      <h2>Find your track.</h2>
      <p class="lead">{len(COURSE_DATA)} courses across brewing, business, spirits, wine and the drinks beyond beer, live online and in person in Pune, Delhi, Gurugram and Bengaluru, plus a free safety course.</p></div>
    <div class="tracks">{"".join(tiles)}</div>
    <div style="margin-top:2rem"><a href="prospectus.html" class="btn btn-ghost" data-cta="prospectus-download">Read the prospectus</a></div>
  </div>
</section>
"""
_WORDS = {6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
          14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"}
COURSE_COUNT_WORD = _WORDS.get(len(COURSE_DATA), str(len(COURSE_DATA)))

# ============================================================================
# Oktoberfest dressing for the home page: bunting, a hat on the logo and a festival
# band. festive.MASCOT (on every page) sets the .okt class that switches it on.
OKT_RAUTE = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='26' height='44'%3E"
             "%3Cpath d='M13 0 26 22 13 44 0 22Z' fill='%232f7fc6' fill-opacity='.85'/%3E%3C/svg%3E")
OKT = """
<style>
.okt-only{display:none}
.okt .okt-only{display:block}
.okt-bunting{height:30px;background:
  conic-gradient(from 150deg at 50% 0,#2f7fc6 60deg,transparent 0) 0 0/88px 30px repeat-x,
  conic-gradient(from 150deg at 50% 0,var(--amber,#e0912f) 60deg,transparent 0) 44px 0/88px 30px repeat-x;
  border-top:2px solid #7a5a2b;transform-origin:top;animation:okt-sway 4s ease-in-out infinite alternate}
@keyframes okt-sway{to{transform:skewX(2deg)}}
@media (prefers-reduced-motion:reduce){.okt-bunting{animation:none}}
.okt-band{padding-block:0;background:#fbf3e2 url("RAUTE") right top/18px 30px repeat-y;border-bottom:1px solid #ead9b8}
.okt-band .wrap{display:flex;align-items:center;gap:clamp(1rem,3vw,2.5rem);flex-wrap:wrap;padding-block:clamp(1.4rem,3vw,2.2rem);padding-right:clamp(2.5rem,5vw,4rem)}
.okt-ribbon{display:inline-block;background:#3b2414;color:#fbf3e2;font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:.78rem;padding:.35rem .9rem;clip-path:polygon(0 0,100% 0,96% 50%,100% 100%,0 100%,4% 50%)}
.okt-title{font-family:var(--serif);font-weight:900;font-size:clamp(2.4rem,6vw,4rem);line-height:1;color:#3b2414;margin:.5rem 0 .3rem;letter-spacing:-.01em}
.okt-title em{color:var(--amber,#e0912f);font-style:italic}
.okt-copy{flex:1 1 320px}
.okt-copy p{margin:0;color:#5a4330;font-size:1.05rem}
.okt-facts{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.9rem}
.okt-facts span{background:#fff;border:1px solid #ead9b8;border-radius:999px;padding:.3rem .85rem;font-size:.9rem;color:#3b2414}
@media(max-width:680px){.okt-band .wrap{gap:1rem;padding-block:1.4rem 1.6rem}.okt-title{font-size:2.1rem}.okt-copy p{font-size:.98rem}.okt-facts span{font-size:.85rem}.okt-band .btn{width:100%;justify-content:center}.okt-bunting{height:22px;background-size:64px 22px,64px 22px;background-position:0 0,32px 0}}
</style>
<div class="okt-only" aria-hidden="true"><div class="okt-bunting"></div></div>
<section class="okt-only okt-band" aria-label="Oktoberfest batch">
  <div class="wrap">
    <div class="okt-copy">
      <span class="okt-ribbon">Learn. Brew. Cheer. Repeat.</span>
      <h2 class="okt-title">Oktoberfest at <em>Craft Beer School</em></h2>
      <p>Raise a stein and learn to brew it. Online Brewing Fundamentals, live with our brewers.</p>
      <div class="okt-facts"><span>Next online batch starts 17 October</span><span>Take home a happy gift</span></div>
    </div>
    <a href="contact.html?course=Brewing%20Fundamentals#enroll" class="btn btn-amber" data-cta="home-oktoberfest">Enrol now [[arrow-right]]</a>
  </div>
</section>
""".replace("RAUTE", OKT_RAUTE)

HOME = f"""{OKT}
<section class="hero">
  <div class="wrap hero-offset">
    <div class="hero-copy reveal">
      <span class="eyebrow">India · Online and in person</span>
      <h1 class="display">Brew like<br>you <span class="script">mean it.</span></h1>
      <p class="lead">India's trusted beer school. We teach everything inside and outside the bottle: brewing, tasting, branding and the business of beer. Now we teach spirits, AI for breweries and the drinks beyond beer too. Live online sessions, guided tastings and hands-on days in Pune, Delhi, Gurugram and Bengaluru.</p>
      <div class="hero-cta">
        <a href="courses.html" class="btn btn-amber">Explore courses [[arrow-right]]</a>
        <a href="prospectus.html" class="btn btn-ghost" data-cta="hero-prospectus">Read the prospectus</a>
        <div class="sticker"><b>₹999</b><small>Intro session · all in</small></div>
      </div>
    </div>
    <div class="hero-media reveal">
      <div class="offset-img"><img src="assets/hero.jpg" alt="A craft beer tasting flight, grain to glass at Craft Beer School" width="1200" height="900" loading="eager" fetchpriority="high" /></div>
    </div>
  </div>
</section>


<section style="padding-block:0">
  <div class="wrap">
    <div class="statband reveal">
      <a class="sb" href="courses.html" data-cta="stat-courses"><span class="ic">[[cap]]</span><div><b>{len(COURSE_DATA)}</b><span>Live online courses</span><em>Brewing, business, spirits and more</em></div></a>
      <a class="sb" href="style-library.html" data-cta="stat-styles"><span class="ic">[[beer]]</span><div><b>80</b><span>Beer styles explained</span><em>Free in the Style Library</em></div></a>
      <a class="sb" href="courses.html" data-cta="stat-batch"><span class="ic">[[users]]</span><div><b>Max 20</b><span>Students per batch</span><em>Live weekend classes, mentor-led</em></div></a>
      <a class="sb" href="courses.html#wset" data-cta="stat-wset"><span class="ic">[[award]]</span><div><b>WSET</b><span>+ Cicerone exam prep</span><em>Group or one-to-one</em></div></a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Basics to Business</span>
      <h2>{COURSE_COUNT_WORD.capitalize()} pours, one path from grain to glass.</h2>
      <p class="lead">Every course pairs theory with real practice. Classes are small, taught by working brewers and backed by one-to-one mentorship.</p>
    </div>
    <div class="grid-3" data-shuffle="3">{"".join(COURSE_CARDS)}</div>
    <div style="margin-top:2rem"><a href="#tracks" class="link-arrow">See all {COURSE_COUNT_WORD} courses by track</a></div>
  </div>
</section>
{photos.band("band:brewhouse", "Copper brew kettles in a working brewhouse")}
{tracks_section()}
{photos.band("band:hops", "Fresh hop cones on the bine")}
<section class="navy-sec" id="companies">
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Corporate services</span>
      <h2 style="color:#fff">Training, hiring and consulting for the drinks business.</h2>
      <p style="color:rgba(255,255,255,.75)">For breweries, wineries and distilleries. For beverage GCCs in Bengaluru, Pune and Hyderabad. For companies bringing beer, ingredients or packaging to India.</p>
      <div class="cta-pair" style="margin-top:1.2rem"><a class="btn btn-amber" href="for-companies.html" data-cta="home-companies">See our services</a><a class="btn btn-ghost on-dark" href="corporate-brochure.html" data-cta="home-companies-brochure">Corporate brochure</a></div>
    </div>
    <ul class="checklist on-dark reveal"><li>Consultancy for beer, cider, spirits and wine, from start-up to new products</li><li>Corporate training for beverage GCCs</li><li>Hiring support for every function</li><li>Brand and digital marketing consultancy</li><li>Market entry into India for beer, ingredient and packaging companies</li><li>Digital transformation and AI</li></ul>
  </div>
</section>
{style_render.home_teaser()}

<section class="navy-sec">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Why Craft Beer School</span><h2>Better beer education brews better beer.</h2></div>
    <div class="features">
      <div class="feature reveal" style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)"><div class="ic">[[flask]]</div><h3 style="color:#fff">Small batches, big learning</h3><p style="color:rgba(255,255,255,.7)">Tiny cohorts so every question gets answered and every batch gets tasted.</p></div>
      <div class="feature reveal" style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)"><div class="ic">[[cap]]</div><h3 style="color:#fff">One-to-one mentorship</h3><p style="color:rgba(255,255,255,.7)">Learn directly from working brewers, sensory pros and founders.</p></div>
      <div class="feature reveal" style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)"><div class="ic">[[globe]]</div><h3 style="color:#fff">Learn anywhere</h3><p style="color:rgba(255,255,255,.7)">Flexible live online sessions you can join from any city, plus in-person workshops.</p></div>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap split">
    <div class="split-media reveal"><div class="offset-img"><img src="assets/team1.jpg" alt="The Craft Beer School team" loading="lazy" /></div></div>
    <div class="prose-block reveal">
      <span class="eyebrow">Free Resources</span>
      <h2>Start learning before you enrol.</h2>
      <p>Beer 101, a styles primer, a working brewing glossary and calculators. Everything you need to sharpen your palate and your process, free.</p>
      <ul class="checklist"><li>Beer 101 crash course</li><li>Beer style and off-flavour guides</li><li>Brewing calculators and tasting tools</li></ul>
      <a href="resources.html" class="link-arrow">Browse the resource library</a>
    </div>
  </div>
</section>

{brew_floor.home_section()}
<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">The Journal · Blog and podcast</span><h2>Insights from the brewing world.</h2></div>
    <div class="grid-3">
      <article class="card reveal"><img class="thumb" src="assets/og/thumb/craft-beer-in-india.jpg" srcset="assets/og/thumb/craft-beer-in-india.jpg 600w, assets/og/craft-beer-in-india.jpg 1200w" sizes="(max-width: 680px) 92vw, 360px" alt="How craft beer actually grew in India" width="600" height="315" loading="lazy" decoding="async" /><div class="card-body"><span class="cat">India</span><h3>How craft beer actually grew in India</h3><p>A licence change in one state started it. Everything after that was taprooms, heat and a generation that wanted choice.</p><div class="foot"><a href="craft-beer-in-india.html" class="link-arrow" data-cta="home-journal">Read</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/og/thumb/start-a-microbrewery-india.jpg" srcset="assets/og/thumb/start-a-microbrewery-india.jpg 600w, assets/og/start-a-microbrewery-india.jpg 1200w" sizes="(max-width: 680px) 92vw, 360px" alt="How to start a microbrewery in India" width="600" height="315" loading="lazy" decoding="async" /><div class="card-body"><span class="cat">Business</span><h3>How to start a microbrewery in India</h3><p>The brewhouse is the easy part. Licensing, cooling and working capital are what decide whether you open.</p><div class="foot"><a href="start-a-microbrewery-india.html" class="link-arrow" data-cta="home-journal">Read</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/og/thumb/how-to-taste-beer.jpg" srcset="assets/og/thumb/how-to-taste-beer.jpg 600w, assets/og/how-to-taste-beer.jpg 1200w" sizes="(max-width: 680px) 92vw, 360px" alt="How to taste beer like a professional" width="600" height="315" loading="lazy" decoding="async" /><div class="card-body"><span class="cat">Tasting</span><h3>How to taste beer like a professional</h3><p>Drinking is not tasting. A method turns a vague impression into something you can name and repeat.</p><div class="foot"><a href="how-to-taste-beer.html" class="link-arrow" data-cta="home-journal">Read</a></div></div></article>
    </div>
  </div>
</section>

<section class="sand">
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow">Beer Stories</span><h2>Spreading the cheer.</h2></div>
    <div class="grid-2">
      <blockquote class="quote reveal"><p>"I recently completed the Brewing Fundamentals course, hosted by Ankur and Chatty, and it was an outstanding experience."</p><div class="who"><span class="av">S</span><div><b>Sunil Prakash Rao</b><span>Singapore</span></div></div></blockquote>
      <blockquote class="quote reveal"><p>"I'm from Ratnagiri, with an M.Sc. in Nutrition and Food Processing. Despite no prior brewing background, this online class made it click."</p><div class="who"><span class="av">P</span><div><b>Poorva Shinde</b><span>Ratnagiri</span></div></div></blockquote>
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <h2>Join Craft Beer School and brew your future.</h2>
    <p>Open to beer lovers, professionals and future brewery founders, in India and across the world.</p>
    <a href="contact.html#enroll" class="btn btn-amber" data-cta="enroll-now">Enrol now</a>
  </div>
</section>
"""

# ============================================================================
def banner(crumb, eyebrow, title, sub):
    return f"""<section class="banner"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a> / {crumb}</div>
  <span class="eyebrow">{eyebrow}</span>
  <h1 class="display">{title}</h1>
  <p>{sub}</p>
</div></section>"""

import mentors
ABOUT = banner("About","About Craft Beer School","We teach the whole bottle.",
    "India's trusted online and in-person beer school, grain to glass and everything around it.") + """
<section>
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Our story</span>
      <h2>Better beer education brews better beer.</h2>
      <p>We are Craft Beer School, India's trusted beer school, online and in person. We teach everything inside and outside the bottle: from ingredients and brewing to tasting, branding and the business of beer.</p>
      <p>Our learning goes grain to glass and beyond through live sessions, guided tastings and hands-on brewery workshops. We also support WSET and Cicerone certification exam preparation, helping you build global beer knowledge and real industry confidence.</p>
      <p>Our courses are open to beer lovers, professionals and future brewery founders in India and across the world. Learn from industry experts through flexible online sessions and practical insights you can use anywhere.</p>
    </div>
    <div class="split-media reveal"><div class="offset-img"><img src="assets/team2.jpg" alt="Craft Beer School recognised at an industry awards ceremony" loading="lazy" /></div></div>
  </div>
</section>

""" + photos.band("band:pour", "Beer taps along a bar") + """
<section class="tint">
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow">What makes us different</span><h2>From passion to profession.</h2></div>
    <div class="features">
      <div class="feature reveal"><div class="ic">[[flask]]</div><h3>Small batches, big learning</h3><p>Tiny cohorts so every question gets answered and every batch gets tasted.</p></div>
      <div class="feature reveal"><div class="ic">[[cap]]</div><h3>One-to-one mentorship</h3><p>Learn directly from working brewers, sensory pros and founders who've built brands in India.</p></div>
      <div class="feature reveal"><div class="ic">[[globe]]</div><h3>Learn anywhere</h3><p>Flexible live online sessions you can join from any city, plus in-person brewery days.</p></div>
      <div class="feature reveal"><div class="ic">[[award]]</div><h3>Certification ready</h3><p>Structured WSET and Cicerone exam prep so your knowledge travels beyond the classroom.</p></div>
      <div class="feature reveal"><div class="ic">[[briefcase]]</div><h3>Passion to profession</h3><p>Curricula built to turn a hobby into a career or a business.</p></div>
      <div class="feature reveal"><div class="ic">[[beer]]</div><h3>Hands-on workshops</h3><p>Guided tastings and real brewery days, grain to glass, in person.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow">Your mentors</span><h2>Taught by people who brew.</h2></div>
    <div class="grid-2">
""" + mentors.cards() + """    </div>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Ready to go grain to glass?</h2><p>Pick a course, book a tasting, or ask us anything.</p><a href="contact.html#enroll" class="btn btn-amber" data-cta="talk-to-us">Talk to us</a></div></section>
"""

CF_TYPE_LIST = [("all", "All"), ("in-person", "In person"), ("online", "Online"), ("study", "Study material"),
                ("free", "Free"), ("exam", "Exam prep")]


def _cf_buttons(key, items, first_label):
    return "".join(f'<button type="button" class="cf-btn" data-k="{key}" data-v="{v}" aria-pressed="{str(i == 0).lower()}">{l}</button>'
                   for i, (v, l) in enumerate([("all", first_label)] + list(items)))


CF_TYPES = _cf_buttons("type", CF_TYPE_LIST[1:], "All types")
CF_SUBJECTS = _cf_buttons("subject", SUBJECTS, "All subjects")
# Reads and writes ?type=&subject= so menu links and shared links open a filtered view.
CF_SCRIPT = """<script>(()=>{const q=new URLSearchParams(location.search),st={type:q.get('type')||'all',subject:q.get('subject')||'all'};
const cards=[...document.querySelectorAll('main [data-type]')],groups=[...document.querySelectorAll('.cf-group')],out=document.querySelector('.cf-count');
function run(){let n=0;cards.forEach(c=>{const ok=(st.type==='all'||c.dataset.type.split(' ').includes(st.type))&&(st.subject==='all'||c.dataset.subject===st.subject);c.hidden=!ok;if(ok)n++;});
groups.forEach(g=>{const own=g.querySelectorAll('[data-type]');g.hidden=own.length>0&&![...own].some(c=>!c.hidden);});
document.querySelectorAll('.cf-btn').forEach(b=>b.setAttribute('aria-pressed',st[b.dataset.k]===b.dataset.v));
out.textContent=n?n+(n===1?' match':' matches'):'Nothing matches both. Try All subjects.';}
document.querySelectorAll('.cf-btn').forEach(b=>b.addEventListener('click',()=>{st[b.dataset.k]=b.dataset.v;run();
const u=new URL(location);['type','subject'].forEach(k=>st[k]==='all'?u.searchParams.delete(k):u.searchParams.set(k,st[k]));history.replaceState(null,'',u);}));
run();if(q.get('type')||q.get('subject'))document.getElementById('course-filter').scrollIntoView();})()</script>"""

# ============================================================================
COURSES = banner("Courses","Basics to Business","Learn the art, science &amp; business of brewing.",
    "From your first pint to your professional journey. Simple, clear and full of real-world learning, online and in person.") + f"""

<section id="course-filter" class="cf-sec"><div class="wrap">
  <h2 class="cf-title">Find the right kind of course</h2>
  <div class="cf" role="group" aria-label="Course type">{CF_TYPES}</div>
  <div class="cf" role="group" aria-label="Subject">{CF_SUBJECTS}</div>
  <p class="cf-count" aria-live="polite"></p>
  <div class="cf-docs"><a href="assets/craft-beer-school-1-day-course.pdf" download data-cta="courses-prospectus-1day">[[download]] 1-day course prospectus</a><a href="assets/craft-beer-school-1-month-course.pdf" download data-cta="courses-prospectus-1month">[[download]] 1-month course prospectus</a><a href="prospectus.html" data-cta="courses-prospectus-all">All online courses prospectus</a></div>
</div></section>

<section class="tint cf-group" id="in-person">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">In person</span><h2>Brew in a real brewery.</h2><p class="lead">Hands-on courses in working microbreweries in Pune, Delhi, Gurugram and Bengaluru. <a href="in-person-brewing-courses-pune-delhi-gurugram-bengaluru.html" style="color:var(--blue);text-decoration:underline">Which one suits you</a>.</p></div>
    <div class="grid-2" data-shuffle>
      <article class="card reveal" data-type="in-person" data-subject="brewing"><div class="card-body"><span class="mode mode-in-person">In person</span><span class="cat">1 Day · 4 cities · ₹25,000</span><h3>1-Day Super Intensive Craft Beer Course</h3><p>A full day inside a working microbrewery, from raw materials to a finished pour: ingredients, mash, lauter, boil, fermentation, CIP and a guided tasting, with a certificate.</p><div class="foot"><a href="contact.html?course=1-Day%20Super%20Intensive%20Craft%20Beer%20Course#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="workshop-1day">Save your seat</a> <a href="assets/craft-beer-school-1-day-course.pdf" download class="link-arrow" data-cta="workshop-1day-prospectus">Prospectus</a> <a href="1-day-super-intensive-craft-beer-course-in-person.html" class="link-arrow" data-cta="workshop-details">Course details</a></div></div></article>
      <article class="card reveal" data-type="in-person" data-subject="brewing"><div class="card-body"><span class="mode mode-in-person">In person</span><span class="cat">1 Month · 48 hours · ₹1,25,000</span><h3>1-Month Intensive Brewing Excellence Course</h3><p>Four weeks of classes, online study, lab work and hands-on brewing in partner microbreweries: fundamentals, brewhouse, fermentation and quality control, at most 20 students.</p><div class="foot"><a href="contact.html?course=1-Month%20Intensive%20Brewing%20Excellence%20Course#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="workshop-1month">Save your seat</a> <a href="assets/craft-beer-school-1-month-course.pdf" download class="link-arrow" data-cta="workshop-1month-prospectus">Prospectus</a> <a href="1-month-intensive-brewing-excellence-course-in-person.html" class="link-arrow" data-cta="workshop-details">Course details</a></div></div></article>
      <article class="card reveal" data-type="in-person" data-subject="brewing"><div class="card-body"><span class="mode mode-in-person">In person</span><span class="cat">1 Day · At Home</span><h3>1-Day Home Visit Brewing Course</h3><p>Our brew master comes to your home with all the equipment and ingredients needed to brew your first batch, start to finish.</p><div class="foot"><a href="contact.html?course=In-person+workshop+%2F+tasting#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="workshop-enquire">Enquire</a> <a href="home-visit-brewing-course-in-person.html" class="link-arrow" data-cta="workshop-details">Course details</a></div></div></article>
      <article class="card reveal" data-type="in-person" data-subject="tasting"><div class="card-body"><span class="mode mode-in-person">In person</span><span class="cat">1 Day · Bengaluru · ₹4,999</span><h3>Professional Beer Tasting Day</h3><p>Taste the way brewers, judges and buyers do. A guided flight across the main styles, from lager, wheat and pale ale to IPA, stout, sour and Belgian, plus spiked samples of the common off-flavours. You learn the professional tasting method, write proper tasting notes and score every beer on an industry scoresheet. Beers, tasting kit and scoresheets included.</p><div class="foot"><a href="contact.html?course=Professional%20Beer%20Tasting%20Day#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="workshop-enquire">Book a seat</a> <a href="professional-beer-tasting-day-in-person.html" class="link-arrow" data-cta="workshop-details">Course details</a></div></div></article>
      <article class="card reveal" data-type="in-person" data-subject="business"><div class="card-body"><span class="mode mode-in-person">In person</span><span class="cat">Half day · Bengaluru · Guided tour</span><h3>Brewery Business Tour</h3><p>For anyone thinking about a brewery or brewpub business. Walk a working Bengaluru brewery with a brewer who runs one: brewhouse, cellar, cold room and taproom. Then the questions every would-be founder asks, about cost, licences, staffing, space and what nobody tells you before you start.</p><div class="foot"><a href="contact.html?course=Brewery%20Business%20Tour#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="workshop-enquire">Enquire</a> <a href="brewery-business-tour-in-person.html" class="link-arrow" data-cta="workshop-details">Course details</a></div></div></article>
      <article class="card reveal" data-type="in-person" data-subject="tasting"><div class="card-body"><span class="mode mode-in-person">In person</span><span class="cat">2 Hours · Tasting</span><h3>2-Hour Craft Beer Tasting Course</h3><p>A guided tasting flight in Bengaluru. Learn to read aroma, flavour and style in two focused hours.</p><div class="foot"><a href="contact.html?course=In-person+workshop+%2F+tasting#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="workshop-enquire">Enquire</a> <a href="2-hour-craft-beer-tasting-course-in-person.html" class="link-arrow" data-cta="workshop-details">Course details</a></div></div></article>
    </div>
  </div>
</section>

<section class="cf-group" id="study">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Study material</span><h2>Learn from the book.</h2><p class="lead">Not a course: notes you work through on your own. Pay and we email it to you.</p></div>
    <div class="grid-2">
      <article class="card reveal" data-type="study" data-subject="brewing"><div class="card-body"><span class="mode mode-online">Study material</span><span class="cat">PDF by email · ₹1,999</span><h3>Brewing Fundamentals Study Book</h3><p>The full syllabus of our 1-month course as 17 chapters of study notes, each with key numbers, check questions and a crossword. Every answer is at the back.</p><div class="foot"><a href="contact.html?course=Brewing%20Fundamentals%20Study%20Book#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="study-book-order">Order the book</a> <a href="brewing-fundamentals-and-beer-crosswords-bundle.html" class="link-arrow" data-cta="study-book-read">What's in it</a></div></div></article>
      <article class="card reveal" data-type="study free" data-subject="brewing"><div class="card-body"><span class="mode mode-both">Free</span><span class="cat">Printable PDF · Free</span><h3>Beer Crosswords</h3><p>103 crosswords on ingredients, the brewhouse, styles, tasting and beer history, with a puzzle for every lesson of our courses and answers at the back.</p><div class="foot"><a href="resources.html" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="study-crosswords">Get it free</a></div></div></article>
    </div>
  </div>
</section>

<section class="cf-group" id="online">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Online courses</span><h2>{COURSE_COUNT_WORD.capitalize()} pours from grain to glass.</h2><div style="margin-top:1.2rem"><a href="prospectus.html" class="btn btn-amber" data-cta="prospectus-download">Read the prospectus</a></div></div>
    <div class="grid-3" data-shuffle>{"".join(COURSE_CARDS)}</div>
  </div>
</section>

<section id="wset" class="cf-group" style="padding-block:2rem 0">
  <div class="wrap"><aside class="cta-inline" data-type="exam online in-person" data-subject="tasting"><div><span class="mode mode-both">Online + in person</span><h3>Preparing for a WSET Beer exam?</h3><p>We prepare candidates for every WSET Beer level, in group cohorts or one-to-one, including last-minute in-person prep for Level 1 in Pune, Delhi, Gurugram and Bengaluru: the syllabus, guided tastings with the systematic approach and mock papers. You sit the exam itself through a WSET Approved Programme Provider. <a href="wset-level-1-beer-last-minute-training.html" style="color:var(--blue);text-decoration:underline">Exam soon? Read about last-minute prep</a>.</p></div><a class="btn btn-amber" href="contact.html?course=WSET%20Beer%20exam%20prep#enroll" data-cta="courses-wset">Ask about exam prep</a></aside></div>
</section>
<section style="padding-block:2rem 0">
  <div class="wrap"><aside class="cta-inline"><div><h3>Training a whole team, or need more than a course?</h3><p>Brewery consultancy, corporate training for beverage GCCs, hiring support, brand and digital marketing, market entry into India and digital transformation.</p></div><a class="btn btn-amber" href="for-companies.html" data-cta="courses-companies">Corporate services</a></aside></div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow">How enrolment works</span><h2>From enquiry to first pour.</h2></div>
    <div class="steps">
      <div class="step reveal"><h3>Pick a course</h3><p>Choose a single pour or the full flight, online or in person.</p></div>
      <div class="step reveal"><h3>Reach out</h3><p>Submit the form or WhatsApp us. We confirm dates and answer questions.</p></div>
      <div class="step reveal"><h3>Confirm &amp; pay</h3><p>Secure your seat. Small cohorts fill quickly.</p></div>
      <div class="step reveal"><h3>Start brewing</h3><p>Join live sessions, get 1:1 mentorship and build your first recipe.</p></div>
    </div>
    <p style="text-align:center;margin-top:2rem;color:var(--ink-soft);font-size:.9rem">Enrolment is subject to our <a href="refund.html" style="color:var(--blue);text-decoration:underline">terms &amp; refund policy</a>.</p>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Not sure which course fits?</h2><p>Tell us where you are and where you want to go. We'll point you to the right pour.</p><a href="courses.html#finder" class="btn btn-amber" data-cta="get-a-recommendation">Find my course</a></div></section>
"""
COURSES += CF_SCRIPT

# ============================================================================
RESOURCES = banner("Resources","Free beer education","Start learning today, on the house.",
    "Beer 101, a styles primer, a working glossary, calculators and tasting tools. No enrolment required.") + """
<section>
  <div class="wrap">
    <div class="grid-3">
      <article class="card reveal"><div class="card-body"><span class="ic">[[book-open]]</span><span class="cat">Start here</span><h3>Beer 101</h3><p>What is craft beer? Ingredients, the four pillars and how a beer is actually made, grain to glass in plain English.</p><div class="foot"><a href="contact.html#enroll" class="link-arrow" data-cta="get-the-crash-course">Get the crash course</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="ic">[[beer]]</span><span class="cat">Reference</span><h3>Beer Style Library</h3><p>80 styles from pilsner to barley wine: colour, bitterness, strength, the right glass and Indian food pairings for each.</p><div class="foot"><a href="style-library.html" class="link-arrow" data-cta="resources-style-library">Open the Style Library</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="ic">[[book]]</span><span class="cat">Reference</span><h3>Brewing Glossary</h3><p>ABV, IBU, OG/FG, attenuation, lauter, dry hop, the words brewers use, defined clearly.</p><div class="foot"><a href="brewing-glossary.html" class="link-arrow">Open the full glossary</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="ic">[[calculator]]</span><span class="cat">Tool · App</span><h3>Indian Brewing Calculator</h3><p>ABV, attenuation and recipe math built for Indian brewing, check your numbers before you brew.</p><div class="foot"><a href="https://ankurnapa.github.io/indian-brewing-calculator/" class="link-arrow" target="_blank" rel="noopener">Open the calculator</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="ic">[[wind]]</span><span class="cat">Tool · App</span><h3>Aroma Forge</h3><p>Predict a beer's aroma by superimposing digitised Weyermann malt aroma wheels, see how your grain bill smells before you brew.</p><div class="foot"><a href="https://ankurnapa.github.io/aroma-forge/" class="link-arrow" target="_blank" rel="noopener">Open Aroma Forge</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="ic">[[sliders]]</span><span class="cat">Tool · App</span><h3>Advanced Brewing Calculator</h3><p>Pro-tier formulation, spec sheets and recipe comparison, for serious brewers who want the full picture.</p><div class="foot"><a href="https://ankurnapa.github.io/advanced-brewing-calc/" class="link-arrow" target="_blank" rel="noopener">Open the pro suite</a></div></div></article>
    </div>
  </div>
</section>

<section class="tint" id="glossary">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Quick reference</span><h2>Brewing glossary.</h2></div>
    <div class="grid-2">
      <div class="prose-block reveal">
        <p><b>ABV</b>, Alcohol by volume, the percentage of alcohol in the finished beer.</p>
        <p><b>OG / FG</b>, Original and final gravity, measured before and after fermentation to track sugar converted to alcohol.</p>
        <p><b>IBU</b>, International Bitterness Units, a measure of hop bitterness.</p>
        <p><b>Attenuation</b>, How much of the sugar the yeast fermented; higher means a drier beer.</p>
      </div>
      <div class="prose-block reveal">
        <p><b>Mash</b>, Steeping crushed malt in hot water to convert starch to fermentable sugar.</p>
        <p><b>Lauter / Sparge</b>, Separating and rinsing the sweet wort from the grain.</p>
        <p><b>Dry hop</b>, Adding hops after the boil for aroma without added bitterness.</p>
        <p><b>Lagering</b>, Cold conditioning that gives lagers their clean, crisp finish.</p>
      </div>
    </div>
    <p style="margin-top:1.5rem"><a href="brewing-glossary.html" class="link-arrow">See every term in the full brewing glossary</a></p>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Ready to move from reading to brewing?</h2><p>Turn these fundamentals into a finished pour with a mentor beside you.</p><a href="courses.html" class="btn btn-amber">See the courses</a></div></section>
"""

# ============================================================================
BLOG = banner("Blog","The Journal · Blog and podcast","Insights from the brewing world.",
    "Quality, marketing, tasting and the business of beer, plus podcast conversations with the people making it.") + """
<section>
  <div class="wrap">
    <div class="grid-3">
      <article class="card reveal"><img class="thumb" src="assets/blog-01.png" alt="What is Craft Beer? A Beginner's Guide" loading="lazy" /><div class="card-body"><span class="cat">Start here</span><h3>What is Craft Beer? A Beginner's Guide</h3><p>The ingredients, the four pillars and what actually makes a beer "craft", in plain English.</p><div class="foot"><a href="resources.html" class="link-arrow" data-cta="blog-card">Start free</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/blog-02.png" alt="Types of Craft Beer: A Complete Style Guide" loading="lazy" /><div class="card-body"><span class="cat">Styles</span><h3>Types of Craft Beer: A Complete Style Guide</h3><p>IPAs, stouts, lagers, sours and Belgian ales, how to tell them apart in the glass.</p><div class="foot"><a href="resources.html" class="link-arrow" data-cta="blog-card">Start free</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/blog-03.png" alt="The Rise of Craft Beer in India" loading="lazy" /><div class="card-body"><span class="cat">India</span><h3>The Rise of Craft Beer in India</h3><p>How a young, thirsty market is turning into one of the world's most exciting beer scenes.</p><div class="foot"><a href="resources.html" class="link-arrow" data-cta="blog-card">Start free</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/blog-04.png" alt="How to Start a Microbrewery in India" loading="lazy" /><div class="card-body"><span class="cat">Business</span><h3>How to Start a Microbrewery in India</h3><p>Licensing, capital and the role of real brewing education in getting it right.</p><div class="foot"><a href="resources.html" class="link-arrow" data-cta="blog-card">Start free</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/blog-05.png" alt="Top Indian Craft Beer Brands You Must Try" loading="lazy" /><div class="card-body"><span class="cat">Culture</span><h3>Top Indian Craft Beer Brands You Must Try</h3><p>A tour of the breweries putting Indian craft beer on the map.</p><div class="foot"><a href="resources.html" class="link-arrow" data-cta="blog-card">Start free</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/blog-06.png" alt="How to Taste Craft Beer Like a Pro" loading="lazy" /><div class="card-body"><span class="cat">Tasting</span><h3>How to Taste Craft Beer Like a Pro</h3><p>Aroma, flavour and mouthfeel, a simple framework to read any beer.</p><div class="foot"><a href="resources.html" class="link-arrow" data-cta="blog-card">Start free</a></div></div></article>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Cheers Chatty Beer Podcast</span>
      <h2>The podcast.</h2>
      <p>Every episode we sit down with brewers, founders and sensory pros to talk about what really happens between grain and glass, the wins, the off-flavours and the business of building a beer brand in India.</p>
      <a href="podcast.html" class="link-arrow" data-cta="blog-listen-podcast">Listen to every episode</a>
    </div>
    <div class="split-media reveal"><div class="offset-img"><img src="assets/team5.jpg" alt="Chatty Girija, host of the Cheers Chatty Ventures beer podcast" loading="lazy" /></div></div>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Never miss a pour.</h2><p>Get new articles, podcast episodes and course dates in your inbox.</p><a href="contact.html#enroll" class="btn btn-amber" data-cta="join-the-list">Join the list</a></div></section>
"""
