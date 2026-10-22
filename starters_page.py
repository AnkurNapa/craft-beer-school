# -*- coding: utf-8 -*-
"""Beer for Starters: the ₹199 one-hour online taster course.

A single landing page, built like the in-person pages, because a one-hour
session does not fit the week-by-week template in course_pages.py. The copy
follows the Beer for Starters concept note and poster (22 Oct 2026).
"""
from pages_a import banner, course_href
from inperson_pages import _ctas, _list

SLUG = "beer-for-starters-online-course.html"
NAME = "Beer for Starters"
FEE = "₹199"
ENROL = "contact.html?course=Beer%20for%20Starters#enroll"
UPSELL = "Brewing Fundamentals"

COURSE = dict(
    name=NAME, enrol=ENROL, pdf=None,
    facts=[("Format", "Online"), ("Duration", "1 hour"), ("Level", "No beer knowledge needed"), ("Fee", FEE)],
)

# The four glasses on the poster's tasting tray.
TRAY = [
    ("#f2b632", "The Curious Beer Drinkers", "You like beer and have always wondered what is actually in the glass."),
    ("#d9771e", "The Beer Braggers", "You want the facts behind the opinions you share at the table."),
    ("#9c3a1a", "The Craft Beer Explorers", "You have started ordering beyond the usual lager and want to know what you are tasting."),
    ("#2b160c", "The Beer Aspiring Professionals", "You are weighing up a job in beer and want a first, low-cost look."),
]

QUESTIONS = ["What exactly is beer?", "Why do some beers taste bitter and others sweet?",
             "What makes a beer craft beer?", "What is the difference between a lager and an ale?",
             "Why does beer have foam?", "How is beer made?",
             "Why does one beer feel light and another rich and full-bodied?",
             "Is beer really different from wine and spirits?",
             "What do beer experts know that regular drinkers do not?"]

HOUR = [("0 to 10 min. What beer is", "Malt, hops, water and yeast: what each one brings to the glass."),
        ("10 to 20 min. How beer is made", "Grain to glass in one picture: mash, boil, ferment, condition, package."),
        ("20 to 32 min. Lager, ale and the main styles", "Why yeast decides the family, then a quick tour from pale lager to stout."),
        ("32 to 42 min. Craft and commercial beer", "What the word craft means and why two pale lagers can taste nothing alike."),
        ("42 to 52 min. How to taste a beer", "Look, smell, sip: bitterness, sweetness, body and why the foam matters."),
        ("52 to 60 min. Your questions and what next", "Beer next to wine and spirits, your questions answered live and where to go from here.")]

GAIN = ["A plain-English picture of what beer is and how it is made",
        "The difference between lager and ale plus the main styles by name",
        "A simple tasting method you can use on the next beer you order",
        "Something worth saying at the table besides which brand you like"]

READING = [("what-is-craft-beer.html", "What is craft beer?"), ("beer-styles-guide.html", "The beer styles guide"),
           ("how-to-taste-beer.html", "How to taste beer"), ("beer-foam-science.html", "Why beer has foam")]


def _tray():
    cards = "".join(
        f'<div class="bfs-glass reveal"><span class="bfs-pint" style="--beer:{c}" aria-hidden="true"></span>'
        f'<h3>{t}</h3><p>{d}</p></div>' for c, t, d in TRAY)
    return f'<div class="bfs-tray">{cards}</div>'


STYLE = """<style>
.bfs-hero{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(1.5rem,4vw,3rem);align-items:center}
.bfs-hero img{width:100%;height:auto;border-radius:14px;box-shadow:0 18px 40px -18px rgba(59,36,20,.45)}
.bfs-price{font-family:var(--serif);font-weight:900;font-size:clamp(3rem,8vw,4.6rem);line-height:1;color:var(--amber,#e0912f);margin:.3rem 0}
.bfs-hamper{display:inline-block;margin-top:1rem;background:#fbf3e2;border:1px solid #ead9b8;border-radius:999px;padding:.4rem 1rem;color:#3b2414;font-weight:600}
.bfs-tray{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;padding:1.4rem 1.2rem 1.6rem;background:linear-gradient(#8a5a33,#6b4224);border-radius:16px}
.bfs-glass{background:#fffaf1;border-radius:12px;padding:1.1rem 1rem;text-align:center}
.bfs-glass h3{font-size:1.05rem;margin:.6rem 0 .3rem}
.bfs-glass p{margin:0;font-size:.92rem;color:var(--ink-soft)}
.bfs-pint{display:block;margin:0 auto;width:46px;height:64px;border-radius:4px 4px 8px 8px;background:linear-gradient(#fffaf1 0 22%,var(--beer) 22%);border:2px solid rgba(59,36,20,.25)}
.bfs-qs{columns:2;column-gap:2.5rem}
.bfs-qs li{break-inside:avoid;margin-bottom:.5rem}
@media(max-width:820px){.bfs-hero{grid-template-columns:1fr}.bfs-tray{grid-template-columns:1fr 1fr}.bfs-qs{columns:1}}
@media(max-width:420px){.bfs-tray{grid-template-columns:1fr}}
</style>"""


def render():
    facts = "".join(f"<div><span>{k}</span><b>{v}</b></div>" for k, v in COURSE["facts"])
    hour = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in HOUR)
    reading = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in READING)
    return STYLE + banner(f'<a href="courses.html">Courses</a> / {NAME}', "Online · 1 hour · " + FEE,
                          f"{NAME}. You drink it. Now get to know it.",
                          "A one-hour introduction to the world of beer for people who love drinking it. No prior knowledge, no complicated terms, no intimidating lectures.") + f"""
<section style="padding-block:0">
  <div class="wrap course-facts">{facts}<div class="cta-pair">{_ctas(COURSE, "facts")}</div></div>
</section>

<section>
  <div class="wrap bfs-hero">
    <div class="prose-block reveal">
      <span class="eyebrow">Ready for a beer tasting tray?</span>
      <h2>Learn about what you love.</h2>
      <p>Most people know which beer they like. Few know why. In one hour we cover what beer is, how it is made, the main styles, what makes a beer craft and how to taste what is in your glass, so you can talk about beer instead of just ordering one.</p>
      <p class="bfs-price">{FEE}</p>
      <p style="margin:0">for the full hour, online.</p>
      <span class="bfs-hamper">A Happy Hour Hamper awaits our first batch.</span>
      <div class="cta-pair" style="margin-top:1.4rem"><a href="{ENROL}" class="btn btn-amber" data-cta="starters-hero-enroll">Enrol for {FEE} [[arrow-right]]</a></div>
    </div>
    <img src="assets/beer-for-starters.jpg" width="1080" height="1080" loading="eager" fetchpriority="high"
         alt="Beer for Starters poster: a tasting tray of four beers from pale to dark, a one-hour online course for ₹199">
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Who it is for</span><h2>Which glass are you?</h2>
      <p class="lead">Four kinds of beer drinker sign up. All four leave knowing more than when they came in.</p></div>
    {_tray()}
  </div>
</section>

<section>
  <div class="wrap split" style="align-items:start">
    <div class="prose-block reveal"><span class="eyebrow">The questions</span><h2>Things you always wanted to ask.</h2><ul class="checklist bfs-qs">{_list(QUESTIONS)}</ul></div>
    <div class="prose-block reveal"><span class="eyebrow">What you get</span><h2>What you walk away with.</h2><ul class="checklist">{_list(GAIN)}</ul></div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">The hour</span><h2>Sixty minutes, start to finish.</h2>
      <p class="lead">Live and visual, with time for your questions at the end. Session dates for each batch are shared when you enrol.</p></div>
    <dl class="logistics">{hour}</dl>
  </div>
</section>

<section>
  <div class="wrap split" style="align-items:start">
    <div class="prose-block reveal"><span class="eyebrow">Next step</span><h2>Caught the bug?</h2>
      <p>Beer for Starters is the first sip. <a href="{course_href(UPSELL)}" style="color:var(--blue);text-decoration:underline">{UPSELL}</a> is the next one: four weeks of live classes that take you from the four ingredients to a recipe of your own.</p></div>
    <div class="prose-block reveal"><span class="eyebrow">Read before you join</span><h2>Free guides to start with.</h2><ul class="checklist">{reading}</ul>
      <p style="color:var(--ink-soft);font-size:.9rem">This course is for adults of legal drinking age. Read the <a href="refund.html" style="color:var(--blue);text-decoration:underline">refund policy</a> before you pay.</p></div>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>One hour. {FEE}. A lot more to talk about.</h2><p>Enrol now and we send you the session details. We reply within 24 hours.</p><div class="cta-pair" style="justify-content:center">{_ctas(COURSE, "bottom")}</div></div></section>
"""


def pages():
    """slug -> (title, desc, active, body) for build.PAGES."""
    desc = (f"{NAME}: a one-hour online beer course for {FEE}. What beer is, how it is made, "
            "lager versus ale, craft beer and how to taste. No prior knowledge needed.")
    return {SLUG: (f"{NAME}: 1-Hour Beer Course | Craft Beer School", desc, "courses", render())}


# Home page band and promo strip entry, so every CTA points at the same page.
HOME_BAND = f"""
<section class="okt-band" aria-label="{NAME}" style="background:#fbf3e2;border-bottom:1px solid #ead9b8">
  <div class="wrap" style="display:flex;align-items:center;gap:clamp(1rem,3vw,2.5rem);flex-wrap:wrap;padding-block:clamp(1.4rem,3vw,2.2rem)">
    <a href="{SLUG}" data-cta="home-starters-poster" style="flex:0 1 280px;max-width:100%;display:block">
      <img src="assets/beer-for-starters-560.jpg" width="560" height="560" loading="eager" style="width:100%;height:auto;border-radius:12px;box-shadow:0 14px 30px -14px rgba(59,36,20,.5)"
           alt="Beer for Starters poster: a tasting tray of four beers, a one-hour online course for ₹199"></a>
    <div style="flex:1 1 320px">
      <span class="eyebrow">New · 1 hour online</span>
      <h2 style="margin:.3rem 0">{NAME}, just {FEE}.</h2>
      <p style="margin:0">You drink it. Now get to know it. A Happy Hour Hamper awaits our first batch.</p>
    </div>
    <a href="{SLUG}" class="btn btn-amber" data-cta="home-starters">See the course [[arrow-right]]</a>
  </div>
</section>
"""

OFFER = dict(key="starters",
             banner=f"New: {NAME}, a one-hour online beer course for {FEE}.",
             link="Enrol now",
             article=SLUG,
             title=f"New to beer? Start with one hour for {FEE}",
             body="What beer is, how it is made, lager versus ale and how to taste it. Online, no prior knowledge needed.",
             href=ENROL,
             label=f"Enrol for {FEE}",
             words=["beginner", "starter", "new to beer", "what is beer", "basics", "lager", "ale", "taste", "199"],
             guides=["what-is-craft-beer", "beer-styles-guide", "how-to-taste-beer", "beer-foam-science"])
