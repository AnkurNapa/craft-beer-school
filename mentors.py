# -*- coding: utf-8 -*-
"""Mentor profiles: one page each, plus the cards on the About page.

Facts here must stay within what the mentor has given us or the site already
says. Do not add employers, numbers or claims that are not confirmed.
"""
MENTORS = [
    dict(slug="mentor-ganesh-ramu.html", name="A.V. Ganesh Ramu", first="Ganesh", img="assets/ganesh-ramu-portrait-2.jpg", page_img="assets/ganesh-ramu-headshot.jpg",
         role="Senior Mentor · Master Brewer",
         card="Our most senior mentor. A Master Brewer from the Institute of Brewing and Distilling with 38 years in brewing across Germany, the UK, New Zealand, Singapore and India.",
         lede="Thirty-eight years of brewing in five countries.",
         bio=["Ganesh is the most senior mentor at Craft Beer School. He has spent more than 38 years in brewing across Germany, the UK, New Zealand, Singapore and India. His last role was Assistant Vice President, Technical.",
              "He has run every stage of the brewery: brewhouse, fermentation, lagering, filtration and bottling. He has brewed ales, stouts, dark ales, festival brews and flavoured beers to the quality standards of leading global brands. He led brewery expansions, plant modernisations and restarts. He also brought production methods and quality benchmarks into line across sites.",
              "He led the project that developed and launched malt-based non-alcoholic drinks. He has worked on recipes and plant efficiency for flagship brands at international sites.",
              "Teaching has run through his whole career. He has designed technical programmes for brewers and pub teams. He has presented at CFTRI, HBTI and PES College. Today he mentors postgraduate students at VSI in Pune."],
         areas=["Brewery operations", "Fermentation and lagering", "Filtration and bottling", "Specialty and festival beers",
                "Non-alcoholic malt drinks", "Sensory evaluation", "Brewery expansions and restarts"],
         courses=[("advanced-brewing-science-course.html", "Advanced Brewing Science")],
         career=[("", "Assistant Vice President, Technical", "Last position"),
                 ("38+ years", "Brewing in Germany, the UK, New Zealand, Singapore and India", ""),
                 ("Now", "Mentor to postgraduate students", "VSI, Pune")],
         education=[("", "Master Brewer Examination", "The Institute of Brewing and Distilling, UK"),
                    ("", "Malting and Brewing course", "International Centre for Brewing and Distilling, Heriot-Watt University, held at CFTRI"),
                    ("", "Formal sensory training", "Brewing Research Foundation, UK"),
                    ("", "PG Diploma in Business Administration", "Bharatiya Vidya Bhavan, Bengaluru"),
                    ("", "Executive Development Programme", "IIM Bangalore"),
                    ("", "Developing Leaders Programme", "IIM Calcutta"),
                    ("", "German language, levels GI and GII", "Max Mueller Bhavan, Bengaluru")],
         linkedin=""),
    dict(slug="mentor-ankur-napa.html", name="Ankur Napa", img="assets/team3.jpg",
         role="Course Instructor · Master Brewer",
         card="A Master Brewer from R&amp;D at United Breweries, SABMiller and AB InBev who went on to build AI and GenAI as a data scientist for AB InBev's global business units.",
         lede="A Master Brewer who also works in data and AI.",
         bio=["Ankur built his brewing career in research and development at United Breweries, SABMiller and AB InBev, where he worked as a Master Brewer. He learned brewing where the numbers have to hold at scale. He teaches the way the brewhouse actually runs: what the numbers say and what the floor tells you when they are wrong.",
              "He then moved into data. After Mathesis Labs he returned to AB InBev as a data scientist, working on AI and GenAI for its global business units. He then worked in operations and digital transformation at iWort. Today he is Growth Officer at Disruptive Advantage.",
              "He holds an MSc in Brewing Science and Technology and an MSc in Data Science and AI. His sessions join classic brewing science to the tools a modern brewery uses to measure, predict and improve. He is a Microsoft Certified Fabric Analytics Engineer and has taught at Craft Beer School since 2021."],
         areas=["Brewing science", "Brewery operations", "Data and AI for breweries", "Digital transformation"],
         courses=[("advanced-brewing-science-course.html", "Advanced Brewing Science"),
                  ("ai-for-craft-breweries-course.html", "AI for Craft Breweries"),
                  ("power-bi-and-tableau-for-breweries-course.html", "Power BI and Tableau for Breweries"),
                  ("brewery-business-management-course.html", "Brewery Business Management"),
                  ("sensory-evaluation-course.html", "Sensory Evaluation"),
                  ("digital-transformation-basics-for-brewing-course.html", "Digital Transformation Basics for Brewing"),
                  ("esg-in-craft-brewing-course.html", "ESG in Craft Brewing"),
                  ("winemaking-course.html", "Winemaking"),
                  ("fortified-wine-course.html", "Fortified Wine"),
                  ("winery-business-course.html", "Winery Business"),
                  ("new-product-development-beer-whisky-and-wine-course.html", "New Product Development: Beer, Whisky and Wine")],
         career=[("2026 to now", "Growth Officer", "Disruptive Advantage"),
                 ("2023 to 2026", "Operations and Digital Transformation", "iWort"),
                 ("2022 to 2023", "Data Scientist, AI and GenAI", "AB InBev, global business units"),
                 ("2020 to 2022", "Senior Data Analyst", "Mathesis Labs"),
                 ("2011 to 2020", "R&amp;D Brewer and Master Brewer", "SABMiller and AB InBev"),
                 ("", "R&amp;D Brewer", "United Breweries")],
         education=[("2021 to 2023", "MSc Data Science and AI", "Liverpool John Moores University"),
                    ("", "PG Diploma in Data Analytics and Business Intelligence", "IIIT Bangalore"),
                    ("2013 to 2015", "MSc Brewing Science and Technology", "Savitribai Phule Pune University"),
                    ("", "BTech Biotechnology", "Maharshi Dayanand University"),
                    ("", "Microsoft Certified: Fabric Analytics Engineer Associate (DP-600)", "Microsoft")],
         linkedin="https://www.linkedin.com/in/ankur-napa/"),
    dict(slug="mentor-chatty-girija.html", name="Chatty Girija", img="assets/team5.jpg",
         role="Beer Podcaster · Creative Strategist",
         card="30+ years in advertising and a deep passion for craft beer. Brings the stories, the branding and the business of beer to every session.",
         lede="Thirty years in advertising, poured into beer.",
         bio=["Chatty spent more than 30 years in advertising before turning that craft to beer. She brings the stories, the branding and the business side of beer into every session.",
              "She hosts Cheers Chatty Ventures, a podcast where brewers, founders and sensory pros talk about what really happens between grain and glass."],
         areas=["Beer branding", "Storytelling", "The business of beer"],
         courses=[("beer-branding-packaging-course.html", "Beer Branding &amp; Packaging")],
         linkedin=""),
    dict(slug="mentor-anu-rao.html", name="Anu Rao", img="assets/team4.jpg",
         role="Head of Strategy &amp; Operations",
         card="15+ years across social responsibility, education and operations, keeping every cohort running smoothly, grain to glass.",
         lede="The reason every cohort runs on time.",
         bio=["Anu has more than 15 years across social responsibility, education and operations.",
              "At Craft Beer School she leads strategy and operations, so every cohort runs smoothly from the first session to the certificate."],
         areas=["Strategy", "Operations", "Education"],
         courses=[],
         linkedin=""),
    dict(slug="mentor-rahul-baliyan.html", name="Rahul Baliyan", img="assets/rahul-baliyan-portrait.jpg", page_img="assets/rahul-baliyan-headshot.jpg",
         role="Brewing Science Instructor · Delhi &amp; North India",
         card="German-style Brewmaster trained at Weihenstephan, TU Munich, with an M.Tech. in Food Biotechnology. A decade as Consultant Brew Master for JW Marriott Chandigarh and Rockmann Beer Island, India's first German brewery, from start-up and excise to yield and sourcing.",
         lede="German-style brewing, taught from Delhi.",
         bio=["Rahul is a certified German-style Brewmaster. He holds an M.Tech. in Food Biotechnology and earned his brewing certification at Weihenstephan, the historic brewery at the Technical University of Munich.",
              "His brewing rests on authentic German technique and consistent results, on 10 hl Caspary and Kaspar Schulz brewhouses. Over the past decade he has worked as Consultant Brew Master for venues including JW Marriott Chandigarh and Rockmann Beer Island, India's first German brewery.",
              "He covers the whole brewing process and the running of a brewery around it: start-ups, excise compliance, team supervision, yield and raw material sourcing. He teaches for Craft Beer School from Delhi, for students across North India."],
         areas=["Brewing science", "German lager brewing", "Brewery start-ups", "Excise compliance", "Yield optimisation", "Raw material sourcing"],
         courses=[("brewing-fundamentals-course.html", "Brewing Fundamentals"),
                  ("advanced-brewing-science-course.html", "Advanced Brewing Science"),
                  ("style-specialization-course.html", "Style Specialisation"),
                  ("safety-in-brewing-course.html", "Safety in Brewing"),
                  ("craft-distilling-course.html", "Craft Distilling"),
                  ("craft-gin-making-course.html", "Craft Gin Making"),
                  ("rtd-drinks-alcoholic-and-non-alcoholic-course.html", "RTD Drinks: Alcoholic and Non-Alcoholic"),
                  ("hop-water-course.html", "Hop Water"),
                  ("hard-seltzer-course.html", "Hard Seltzer"),
                  ("kombucha-course.html", "Kombucha"),
                  ("non-alcoholic-beer-course.html", "Non-Alcoholic Beer"),
                  ("winemaking-course.html", "Winemaking"),
                  ("fortified-wine-course.html", "Fortified Wine"),
                  ("winery-business-course.html", "Winery Business"),
                  ("new-product-development-beer-whisky-and-wine-course.html", "New Product Development: Beer, Whisky and Wine")],
         education=[("", "Brewing certification", "Weihenstephan, Technical University of Munich"),
                    ("", "M.Tech. Food Biotechnology", "")],
         linkedin="https://www.linkedin.com/in/rahul-baliyan-m-tech-40630a6b/",
         gallery=[("assets/rahul-tum-certificate.jpg", "Receiving his brewing certificate at TUM"),
                  ("assets/rahul-brewhouse.jpg", "In a copper brewhouse"),
                  ("assets/rahul-cohort-1.jpg", "With fellow brewers on the course in Germany"),
                  ("assets/rahul-cohort-2.jpg", "The course group in the classroom")]),
]


def card(m):
    return (f'      <article class="card mentor-card reveal"><a href="{m["slug"]}" tabindex="-1" aria-hidden="true"><img class="mentor-img" src="{m["img"]}" alt="{m["name"]}" loading="lazy" /></a>'
            f'<div class="card-body"><span class="cat">{m["role"]}</span><h3><a href="{m["slug"]}">{m["name"]}</a></h3>'
            f'<p>{m["card"]}</p><div style="display:flex;flex-wrap:wrap;gap:.4rem 1.4rem"><a href="{m["slug"]}" class="link-arrow">Full profile</a>{_linkedin(m)}</div></div></article>\n')


def _linkedin(m):
    if not m["linkedin"]:
        return ""
    return f'<a href="{m["linkedin"]}" target="_blank" rel="noopener" class="link-arrow">{m.get("first", m["name"].split()[0])} on LinkedIn</a>'


CONTACT = "mentor-chatty-girija.html"  # point of contact on every course page, reached on WhatsApp
WHATSAPP_NUMBER = "919820925347"      # school and Chatty WhatsApp, digits only, country code first


def _person(m, label, action):
    return (f'<article class="card person-card reveal"><img class="person-img" src="{m["img"]}" alt="{m["name"]}" '
            f'width="120" height="120" loading="lazy" /><div class="card-body"><span class="cat">{label}</span>'
            f'<h3><a href="{m["slug"]}">{m["name"]}</a></h3><p>{m["role"]}</p>{action}</div></article>')


def instructors(course_slug, course_name):
    """Instructor and point-of-contact cards for a course page. Instructors link to
    LinkedIn where we have it; the point of contact opens WhatsApp about this course."""
    by_slug = {m["slug"]: m for m in MENTORS}
    team = [m for m in MENTORS if any(s == course_slug for s, _ in m["courses"])]
    cards_html = []
    for m in team:
        if m["slug"] == CONTACT:
            continue  # shown once below, as instructor and contact
        action = (f'<a href="{m["linkedin"]}" target="_blank" rel="noopener" class="btn btn-ghost person-btn" '
                  f'data-cta="course-instructor-linkedin">Connect on LinkedIn</a>' if m["linkedin"]
                  else f'<a href="{m["slug"]}" class="link-arrow">Full profile</a>')
        cards_html.append(_person(m, "Instructor", action))
    c = by_slug[CONTACT]
    label = "Instructor and point of contact" if c in team else "Point of contact"
    from urllib.parse import quote
    wa = f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(f'Hi Chatty, I would like to know more about the {course_name} course.')}"
    cards_html.append(_person(c, label, f'<a href="{wa}" target="_blank" rel="noopener" class="btn btn-amber person-btn" '
                                        f'data-cta="course-contact-whatsapp">WhatsApp {c.get("first", c["name"].split()[0])}</a>'))
    head = "Your instructor and point of contact" if len(team) <= 1 else "Your instructors and point of contact"
    return f"""<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">{head}</span><h2>Who teaches this course, and who to ask.</h2></div>
    <div class="person-grid">{"".join(cards_html)}</div>
  </div>
</section>
"""

def cards():
    return "".join(card(m) for m in MENTORS)


def _timeline(title, rows):
    if not rows:
        return ""
    items = "".join(f'<li><span>{when}</span><b>{what}</b>{f"<em>{where}</em>" if where else ""}</li>' for when, what, where in rows)
    return f'<div class="prose-block reveal"><span class="eyebrow">{title}</span><ol class="timeline">{items}</ol></div>'


def _body(m):
    from pages_a import banner  # pages_a imports this module for the About cards
    bio = "".join(f"<p>{p}</p>" for p in m["bio"])
    areas = "".join(f"<li>{a}</li>" for a in m["areas"])
    courses = "".join(f'<li><a href="{s}">{n}</a></li>' for s, n in m["courses"])
    courses = f'<h3>Courses</h3><ul class="checklist">{courses}</ul>' if courses else ""
    li = (f'<p><a href="{m["linkedin"]}" target="_blank" rel="noopener" class="link-arrow">{m.get("first", m["name"].split()[0])} on LinkedIn</a></p>'
          if m["linkedin"] else "")
    others = "".join(card(o) for o in MENTORS if o is not m)
    history = "".join(_timeline(t, m.get(k)) for t, k in (("Career", "career"), ("Education", "education")))
    history = f'<section class="tint"><div class="wrap split" style="align-items:start">{history}</div></section>' if history else ""
    pics = "".join(f'<figure class="mentor-photo reveal"><img src="{src}" alt="{m["name"]}: {cap}" loading="lazy" /><figcaption>{cap}</figcaption></figure>'
                   for src, cap in m.get("gallery", []))
    gallery = (f'<section><div class="wrap"><div class="sec-head"><span class="eyebrow">In photos</span><h2>{m.get("first", m["name"].split()[0])} at work.</h2></div>'
               f'<div class="grid-2">{pics}</div></div></section>') if pics else ""
    return banner(f'<a href="about.html">About</a> / {m["name"]}', m["role"], m["name"], m["lede"]) + f"""
<section>
  <div class="wrap split">
    <div class="split-media reveal"><img class="mentor-img" src="{m.get("page_img", m["img"])}" alt="{m["name"]}" style="border-radius:var(--radius)" /></div>
    <div class="prose-block reveal">
      <span class="eyebrow">About {m.get("first", m["name"].split()[0])}</span>
      {bio}
      <h3>Teaches</h3><ul class="checklist">{areas}</ul>
      {courses}
      {li}
    </div>
  </div>
</section>

{history}
{gallery}
<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Your mentors</span><h2>Meet the rest of the team.</h2></div>
    <div class="grid-3">
{others}    </div>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Learn with {m.get("first", m["name"].split()[0])}.</h2><p>Pick a course, or ask us which one fits you.</p><a href="contact.html#enroll" class="btn btn-amber" data-cta="mentor-talk-to-us">Talk to us</a></div></section>
"""


def pages():
    return {m["slug"]: (f'{m["name"]} | Craft Beer School Mentor',
                        f'{m["name"]}: {m["lede"]} Meet this Craft Beer School mentor.',
                        "about", _body(m)) for m in MENTORS}
