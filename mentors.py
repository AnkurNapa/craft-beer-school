# -*- coding: utf-8 -*-
"""Mentor profiles: one page each, plus the cards on the About page.

Facts here must stay within what the mentor has given us or the site already
says. Do not add employers, numbers or claims that are not confirmed.
"""
MENTORS = [
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
                  ("power-bi-and-tableau-for-breweries-course.html", "Power BI and Tableau for Breweries")],
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
    dict(slug="mentor-rahul-baliyan.html", name="Rahul Baliyan", img="assets/rahul-baliyan.jpg",
         role="Brewing Science Instructor · Delhi &amp; North India",
         card="German-style Brewmaster trained at Weihenstephan, TU Munich, with an M.Tech. in Food Biotechnology. A decade as Consultant Brew Master for JW Marriott Chandigarh and Rockmann Beer Island, India's first German brewery, from start-up and excise to yield and sourcing.",
         lede="German-style brewing, taught from Delhi.",
         bio=["Rahul is a certified German-style Brewmaster. He holds an M.Tech. in Food Biotechnology and earned his brewing certification at Weihenstephan, the historic brewery at the Technical University of Munich.",
              "His brewing rests on authentic German technique and consistent results, on 10 hl Caspary and Kaspar Schulz brewhouses. Over the past decade he has worked as Consultant Brew Master for venues including JW Marriott Chandigarh and Rockmann Beer Island, India's first German brewery.",
              "He covers the whole brewing process and the running of a brewery around it: start-ups, excise compliance, team supervision, yield and raw material sourcing. He teaches for Craft Beer School from Delhi, for students across North India."],
         areas=["Brewing science", "German lager brewing", "Brewery start-ups", "Excise compliance", "Yield optimisation", "Raw material sourcing"],
         courses=[("brewing-fundamentals-course.html", "Brewing Fundamentals"),
                  ("advanced-brewing-science-course.html", "Advanced Brewing Science")],
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
    return f'<a href="{m["linkedin"]}" target="_blank" rel="noopener" class="link-arrow">{m["name"].split()[0]} on LinkedIn</a>'


def instructors(course_slug):
    """'Your instructors' section for a course page, empty if nobody is mapped to it."""
    team = [m for m in MENTORS if any(s == course_slug for s, _ in m["courses"])]
    if not team:
        return ""
    return f"""<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Your instructor{"s" if len(team) > 1 else ""}</span><h2>Who teaches this course.</h2></div>
    <div class="grid-3">
{"".join(card(m) for m in team)}    </div>
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
    li = (f'<p><a href="{m["linkedin"]}" target="_blank" rel="noopener" class="link-arrow">{m["name"].split()[0]} on LinkedIn</a></p>'
          if m["linkedin"] else "")
    others = "".join(card(o) for o in MENTORS if o is not m)
    history = "".join(_timeline(t, m.get(k)) for t, k in (("Career", "career"), ("Education", "education")))
    history = f'<section class="tint"><div class="wrap split" style="align-items:start">{history}</div></section>' if history else ""
    pics = "".join(f'<figure class="mentor-photo reveal"><img src="{src}" alt="{m["name"]}: {cap}" loading="lazy" /><figcaption>{cap}</figcaption></figure>'
                   for src, cap in m.get("gallery", []))
    gallery = (f'<section><div class="wrap"><div class="sec-head"><span class="eyebrow">In photos</span><h2>{m["name"].split()[0]} at work.</h2></div>'
               f'<div class="grid-2">{pics}</div></div></section>') if pics else ""
    return banner(f'<a href="about.html">About</a> / {m["name"]}', m["role"], m["name"], m["lede"]) + f"""
<section>
  <div class="wrap split">
    <div class="split-media reveal"><img class="mentor-img" src="{m["img"]}" alt="{m["name"]}" style="border-radius:var(--radius)" /></div>
    <div class="prose-block reveal">
      <span class="eyebrow">About {m["name"].split()[0]}</span>
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

<section class="cta"><div class="wrap"><h2>Learn with {m["name"].split()[0]}.</h2><p>Pick a course, or ask us which one fits you.</p><a href="contact.html#enroll" class="btn btn-amber" data-cta="mentor-talk-to-us">Talk to us</a></div></section>
"""


def pages():
    return {m["slug"]: (f'{m["name"]} | Craft Beer School Mentor',
                        f'{m["name"]}: {m["lede"]} Meet this Craft Beer School mentor.',
                        "about", _body(m)) for m in MENTORS}
