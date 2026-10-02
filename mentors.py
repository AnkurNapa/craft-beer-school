# -*- coding: utf-8 -*-
"""Mentor profiles: one page each, plus the cards on the About page.

Facts here must stay within what the mentor has given us or the site already
says. Do not add employers, numbers or claims that are not confirmed.
"""
MENTORS = [
    dict(slug="mentor-ankur-napa.html", name="Ankur Napa", img="assets/team3.jpg",
         role="Course Instructor · Master Brewer",
         card="A Master Brewer with hands-on experience at global brewing giants. Bridges the science of the mash tun with the reality of the brewery floor.",
         lede="A Master Brewer who also works in data and AI.",
         bio=["Ankur has brewed at global brewing companies, and he teaches the way the brewhouse actually runs: what the numbers say, and what the floor tells you when they are wrong.",
              "He also works in data and AI for breweries, so his sessions connect classic brewing science with the tools a modern brewery uses to measure, predict and improve."],
         areas=["Brewing science", "Brewery operations", "Data and AI for breweries"],
         courses=[("advanced-brewing-science-course.html", "Advanced Brewing Science"),
                  ("ai-for-craft-breweries-course.html", "AI for Craft Breweries")],
         linkedin=""),
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
         linkedin="https://www.linkedin.com/in/rahul-baliyan-m-tech-40630a6b/"),
]


def card(m):
    return (f'      <article class="card reveal"><a href="{m["slug"]}"><img class="mentor-img" src="{m["img"]}" alt="{m["name"]}" loading="lazy" /></a>'
            f'<div class="card-body"><span class="cat">{m["role"]}</span><h3><a href="{m["slug"]}">{m["name"]}</a></h3>'
            f'<p>{m["card"]}</p><a href="{m["slug"]}" class="link-arrow">Full profile</a></div></article>\n')


def cards():
    return "".join(card(m) for m in MENTORS)


def _body(m):
    from pages_a import banner  # pages_a imports this module for the About cards
    bio = "".join(f"<p>{p}</p>" for p in m["bio"])
    areas = "".join(f"<li>{a}</li>" for a in m["areas"])
    courses = "".join(f'<li><a href="{s}">{n}</a></li>' for s, n in m["courses"])
    courses = f'<h3>Related courses</h3><ul class="checklist">{courses}</ul>' if courses else ""
    li = (f'<p><a href="{m["linkedin"]}" target="_blank" rel="noopener" class="link-arrow">{m["name"].split()[0]} on LinkedIn</a></p>'
          if m["linkedin"] else "")
    others = "".join(card(o) for o in MENTORS if o is not m)
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
