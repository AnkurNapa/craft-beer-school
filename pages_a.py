# -*- coding: utf-8 -*-
"""Page bodies: Home, About, Courses, Resources, Blog."""

import re

import style_render
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
def course(no, tag, dur, name, blurb, items, price, ph):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f"""<article class="card course-card reveal">
  <div class="top"><span class="course-no">{no} / {tag}</span><span class="course-dur">{dur}</span></div>
  <div class="card-body">
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
         items=["Brewing science &amp; theory","Raw materials &amp; quality","Equipment &amp; sanitation","Recipe formulation basics"],
         price="₹5,999", amount="5999"),
    dict(no="02", tag="Deep Craft", dur="6 Weeks", weeks=6, name="Advanced Brewing Science",
         blurb="Go deeper into chemistry, microbiology and advanced fermentation for serious brewers and pros.",
         items=["Microbiology &amp; fermentation","Water chemistry optimisation","Advanced mashing techniques","Quality assurance &amp; control"],
         price="₹12,999", amount="12999"),
    dict(no="03", tag="Business", dur="3 Weeks", weeks=3, name="Brewery Business Management",
         blurb="The business behind the brew: plan, launch and grow a brewery, from finance to distribution.",
         items=["Business planning &amp; finance","Licensing &amp; regulations","Marketing &amp; branding","Distribution strategies"],
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
         blurb="Put GenAI to work on your brewery's copy, social posts and weekly admin, and use it responsibly. No coding needed.",
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
         blurb="From wash to bottle: stills, cuts, gin botanicals, ageing in Indian heat, and the licences a craft distillery needs.",
         items=["Wash, stills and the run","Heads, hearts and tails","Gin and botanicals","Ageing, costs and licensing"],
         price="₹9,999", amount="9999"),
    dict(no="12", tag="New · Spirits", dur="4 Weeks", weeks=4, name="Craft Gin Making",
         blurb="Design and make a gin of your own: juniper and botanicals, the still run, proofing, and getting a bottle to market in India.",
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
         blurb="Beer that still tastes like beer, without the alcohol: limited fermentation, special yeasts, body and aroma, and keeping it safe on the shelf.",
         items=["Limited fermentation and special yeasts","Dealcoholisation, and when it makes sense","Body, aroma and avoiding a worty taste","Pasteurisation, testing and labelling"],
         price="₹5,000", amount="5000"),
]

COURSE_CARDS = [
    course(c["no"], c["tag"], c["dur"], c["name"], c["blurb"], c["items"], c["price"], "")
    for c in COURSE_DATA
]
C1, C2, C3 = COURSE_CARDS[:3]

# Home page tracks. Every course must sit in exactly one, so a new course can
# never go missing from the home page: the assert below stops the build.
TRACKS = [
    ("beer", "Brewing", "From your first batch to judging-level palate.",
     ["Brewing Fundamentals", "Advanced Brewing Science", "Style Specialisation", "Sensory Evaluation"]),
    ("briefcase", "Business &amp; tech", "Run, market and modernise a brewery.",
     ["Brewery Business Management", "Beer Branding &amp; Packaging", "AI for Craft Breweries",
      "Digital Transformation Basics for Brewing", "ESG in Craft Brewing"]),
    ("martini", "Spirits", "Distilling and gin, from wash to bottle.",
     ["Craft Distilling", "Craft Gin Making"]),
    ("glass-water", "Beyond beer", "Low, no and other ferments people are buying now.",
     ["Non-Alcoholic Beer", "RTD Drinks: Alcoholic and Non-Alcoholic", "Hop Water", "Hard Seltzer", "Kombucha"]),
    ("map-pin", "Free &amp; in Bengaluru", "Start free, or learn in the room with us.",
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
            items += '<li><a href="courses.html#wset">WSET Beer exam prep</a><span>Group or 1-to-1</span></li>'
        if title.startswith("Free"):
            items += ('<li><a href="courses.html#in-person">Professional Beer Tasting Day</a><span>1 Day · ₹4,999</span></li>'
                      '<li><a href="courses.html#in-person">Brewery Business Tour</a><span>Half day · On enquiry</span></li>'
                      '<li><a href="courses.html#in-person">More hands-on workshops</a><span>Bengaluru</span></li>')
        slot = {"Brewing": "track:brewing", "Business &amp; tech": "track:business", "Spirits": "track:spirits",
                "Beyond beer": "track:beyond"}.get(title, "track:bengaluru")
        tiles.append(f"""<article class="track reveal">{photos.figure(slot, title, "photo track-photo")}
        <div class="track-head"><span class="ic">[[{icon}]]</span><div><h3>{title}</h3><p>{line}</p></div></div>
        <ul class="track-list">{items}</ul>
      </article>""")
    return f"""
<section class="sand" id="tracks">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Every course</span>
      <h2>Find your track.</h2>
      <p class="lead">{len(COURSE_DATA)} live online courses across brewing, business, spirits and the drinks beyond beer, plus a free safety course and hands-on days in Bengaluru.</p></div>
    <div class="tracks">{"".join(tiles)}</div>
    <div style="margin-top:2rem"><a href="prospectus.html" class="btn btn-ghost" data-cta="prospectus-download">Read the prospectus</a></div>
  </div>
</section>
"""
_WORDS = {6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
          14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"}
COURSE_COUNT_WORD = _WORDS.get(len(COURSE_DATA), str(len(COURSE_DATA)))

# ============================================================================
HOME = f"""
<section class="hero">
  <div class="wrap hero-offset">
    <div class="hero-copy reveal">
      <span class="eyebrow">India · Online &amp; In-Person</span>
      <h1 class="display">Brew like<br>you <span class="script">mean it.</span></h1>
      <p class="lead">India's trusted beer school. We teach everything inside and outside the bottle: brewing, tasting, branding and the business of beer, and now spirits, AI for breweries and the drinks beyond beer. Live online sessions, guided tastings and hands-on days in Bengaluru.</p>
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
      <p class="lead">Each course blends theory with real practice, small groups, one-on-one mentorship, industry experts.</p>
    </div>
    <div class="grid-3">{C1}{C2}{C3}</div>
    <div style="margin-top:2rem"><a href="#tracks" class="link-arrow">See all {COURSE_COUNT_WORD} courses by track</a></div>
  </div>
</section>
{tracks_section()}
<section class="navy-sec" id="companies">
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Corporate services</span>
      <h2 style="color:#fff">Training, hiring and consulting for the drinks business.</h2>
      <p style="color:rgba(255,255,255,.75)">For breweries, wineries and distilleries, for beverage GCCs in Bengaluru, Pune and Hyderabad, and for companies bringing beer, ingredients or packaging to India.</p>
      <div class="cta-pair" style="margin-top:1.2rem"><a class="btn btn-amber" href="for-companies.html" data-cta="home-companies">See our services</a><a class="btn btn-ghost on-dark" href="corporate-brochure.html" data-cta="home-companies-brochure">Corporate brochure</a></div>
    </div>
    <ul class="checklist on-dark reveal"><li>Corporate training for beverage GCCs</li><li>Hiring support for every function</li><li>Brand and digital marketing consultancy</li><li>Market entry into India for beer, ingredient and packaging companies</li><li>Digital transformation and AI</li></ul>
  </div>
</section>
{style_render.home_teaser()}

<section class="navy-sec">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Why Craft Beer School</span><h2>Better beer education brews better beer.</h2></div>
    <div class="features">
      <div class="feature reveal" style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)"><div class="ic">[[flask]]</div><h3 style="color:#fff">Small batches, big learning</h3><p style="color:rgba(255,255,255,.7)">Tiny cohorts so every question gets answered and every batch gets tasted.</p></div>
      <div class="feature reveal" style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)"><div class="ic">[[cap]]</div><h3 style="color:#fff">One-on-one mentorship</h3><p style="color:rgba(255,255,255,.7)">Learn directly from working brewers, sensory pros and founders.</p></div>
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
      <p>Beer 101, a styles primer, a working brewing glossary and calculators, everything you need to sharpen your palate and your process, on the house.</p>
      <ul class="checklist"><li>Beer 101 crash course</li><li>Beer styles &amp; off-flavour guides</li><li>Brewing calculators &amp; tasting tools</li></ul>
      <a href="resources.html" class="link-arrow">Browse the resource library</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">The Journal · Blog &amp; Podcasts</span><h2>Insights from the brewing world.</h2></div>
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
    <h2>Join the Craft Beer School &amp; brew your future.</h2>
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

<section class="tint">
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow">What makes us different</span><h2>From passion to profession.</h2></div>
    <div class="features">
      <div class="feature reveal"><div class="ic">[[flask]]</div><h3>Small batches, big learning</h3><p>Tiny cohorts so every question gets answered and every batch gets tasted.</p></div>
      <div class="feature reveal"><div class="ic">[[cap]]</div><h3>One-on-one mentorship</h3><p>Learn directly from working brewers, sensory pros and founders who've built brands in India.</p></div>
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

# ============================================================================
COURSES = banner("Courses","Basics to Business","Learn the art, science &amp; business of brewing.",
    "From your first pint to your professional journey. Simple, clear and full of real-world learning, online and in person.") + f"""
<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Online courses</span><h2>{COURSE_COUNT_WORD.capitalize()} pours from grain to glass.</h2><div style="margin-top:1.2rem"><a href="prospectus.html" class="btn btn-amber" data-cta="prospectus-download">Read the prospectus</a></div></div>
    <div class="grid-3">{"".join(COURSE_CARDS)}</div>
  </div>
</section>

<section id="wset" style="padding-block:2rem 0">
  <div class="wrap"><aside class="cta-inline"><div><h3>Preparing for a WSET Beer exam?</h3><p>We prepare candidates for every WSET Beer level, in group cohorts or one-to-one: the syllabus, guided tastings with the systematic approach, and mock papers. You sit the exam itself through a WSET Approved Programme Provider. <a href="wset-beer-course.html" style="color:var(--blue);text-decoration:underline">How the WSET Beer route works</a>.</p></div><a class="btn btn-amber" href="contact.html?course=WSET%20Beer%20exam%20prep#enroll" data-cta="courses-wset">Ask about exam prep</a></aside></div>
</section>
<section style="padding-block:2rem 0">
  <div class="wrap"><aside class="cta-inline"><div><h3>Training a whole team, or need more than a course?</h3><p>Corporate training for beverage GCCs, hiring support, brand and digital marketing, market entry into India and digital transformation.</p></div><a class="btn btn-amber" href="for-companies.html" data-cta="courses-companies">Corporate services</a></aside></div>
</section>
<section class="tint" id="in-person">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">In person</span><h2>Hands-on workshops &amp; tastings.</h2><p class="lead">Prefer to learn at the bench? Join us in the room.</p></div>
    <div class="grid-2">
      <article class="card reveal"><div class="card-body"><span class="cat">1 Day · Intensive</span><h3>1-Day Super Intensive Craft Beer Course</h3><p>Step into a real microbrewery for a full day, from raw materials to a finished pour, condensed into one focused classroom-plus-brewery session.</p><div class="foot"><a href="contact.html?course=In-person+workshop+%2F+tasting#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="workshop-enquire">Enquire</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="cat">1 Month · Advanced</span><h3>1-Month Advanced Craft Beer Brewing Course</h3><p>Homebrewer to beer founder, an advanced, hands-on programme with focused mentorship over four weeks.</p><div class="foot"><a href="contact.html?course=In-person+workshop+%2F+tasting#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="workshop-enquire">Enquire</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="cat">1 Day · At Home</span><h3>1-Day Home Visit Brewing Course</h3><p>Our brew master comes to your home with all the equipment and ingredients needed to brew your first batch, start to finish.</p><div class="foot"><a href="contact.html?course=In-person+workshop+%2F+tasting#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="workshop-enquire">Enquire</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="cat">1 Day · Bengaluru · ₹4,999</span><h3>Professional Beer Tasting Day</h3><p>Taste the way brewers, judges and buyers do. A guided flight across the main styles, from lager, wheat and pale ale to IPA, stout, sour and Belgian, plus spiked samples of the common off-flavours. You learn the professional tasting method, write proper tasting notes and score every beer on an industry scoresheet. Beers, tasting kit and scoresheets included.</p><div class="foot"><a href="contact.html?course=Professional%20Beer%20Tasting%20Day#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="workshop-enquire">Book a seat</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="cat">Half day · Bengaluru · Guided tour</span><h3>Brewery Business Tour</h3><p>For anyone thinking about a brewery or brewpub business. Walk a working Bengaluru brewery with a brewer who runs one: brewhouse, cellar, cold room and taproom. Then the questions every would-be founder asks, about cost, licences, staffing, space and what nobody tells you before you start.</p><div class="foot"><a href="contact.html?course=Brewery%20Business%20Tour#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="workshop-enquire">Enquire</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="cat">2 Hours · Tasting</span><h3>2-Hour Craft Beer Tasting Course</h3><p>A guided tasting flight in Bengaluru. Learn to read aroma, flavour and style in two focused hours.</p><div class="foot"><a href="contact.html?course=In-person+workshop+%2F+tasting#enroll" class="btn btn-ghost" style="padding:.55rem 1.1rem" data-cta="workshop-enquire">Enquire</a></div></div></article>
    </div>
  </div>
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

<section class="cta"><div class="wrap"><h2>Not sure which course fits?</h2><p>Tell us where you are and where you want to go. We'll point you to the right pour.</p><a href="contact.html#enroll" class="btn btn-amber" data-cta="get-a-recommendation">Get a recommendation</a></div></section>
"""

# ============================================================================
RESOURCES = banner("Resources","Free beer education","Start learning today, on the house.",
    "Beer 101, a styles primer, a working glossary, calculators and tasting tools. No enrolment required.") + """
<section>
  <div class="wrap">
    <div class="grid-3">
      <article class="card reveal"><div class="card-body"><span class="ic">[[book-open]]</span><span class="cat">Start here</span><h3>Beer 101</h3><p>What is craft beer? Ingredients, the four pillars, and how a beer is actually made, grain to glass in plain English.</p><div class="foot"><a href="contact.html#enroll" class="link-arrow" data-cta="get-the-crash-course">Get the crash course</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="ic">[[beer]]</span><span class="cat">Reference</span><h3>Beer Style Library</h3><p>80 styles from pilsner to barley wine: colour, bitterness, strength, the right glass, and Indian food pairings for each.</p><div class="foot"><a href="style-library.html" class="link-arrow" data-cta="resources-style-library">Open the Style Library</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="ic">[[book]]</span><span class="cat">Reference</span><h3>Brewing Glossary</h3><p>ABV, IBU, OG/FG, attenuation, lauter, dry hop, the words brewers use, defined clearly.</p><div class="foot"><a href="#glossary" class="link-arrow">Jump to glossary</a></div></div></article>
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
    <p style="margin-top:1.5rem"><a href="courses.html" class="link-arrow">Go deeper in Brewing Fundamentals</a></p>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Ready to move from reading to brewing?</h2><p>Turn these fundamentals into a finished pour with a mentor beside you.</p><a href="courses.html" class="btn btn-amber">See the courses</a></div></section>
"""

# ============================================================================
BLOG = banner("Blog","The Journal · Blog &amp; Podcasts","Insights from the brewing world.",
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
      <span class="eyebrow">Cheers Chatty Ventures</span>
      <h2>The podcast.</h2>
      <p>Every episode we sit down with brewers, founders and sensory pros to talk about what really happens between grain and glass, the wins, the off-flavours and the business of building a beer brand in India.</p>
      <a href="contact.html#enroll" class="link-arrow" data-cta="suggest-a-guest-or-topic">Suggest a guest or topic</a>
    </div>
    <div class="split-media reveal"><div class="offset-img"><img src="assets/team5.jpg" alt="Chatty Girija, host of the Cheers Chatty Ventures beer podcast" loading="lazy" /></div></div>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Never miss a pour.</h2><p>Get new articles, podcast episodes and course dates in your inbox.</p><a href="contact.html#enroll" class="btn btn-amber" data-cta="join-the-list">Join the list</a></div></section>
"""
