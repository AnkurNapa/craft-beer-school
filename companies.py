# -*- coding: utf-8 -*-
"""For Companies: corporate training for beverage GCCs, and hiring support.

Team facts here must match what the About page already says about the
mentors. Do not add employers, numbers or claims that are not on the site.
"""
from pages_a import banner, enroll_href

SLUG = "for-companies.html"
TRAINING_HREF = enroll_href("Corporate training")
HIRING_HREF = enroll_href("Hiring support")

PROGRAMMES = [
    ("beer", "Beverage 101",
     "How beer, wine and whisky are made, from grain and grape to glass, with the words the business uses every day. The right first week for new joiners."),
    ("flask", "Brewing and distilling operations",
     "The brewhouse, cellar, still and bottling line as numbers: yield, losses, quality checks and the KPIs analysts are asked to explain."),
    ("globe", "Raw materials and supply chain",
     "Barley and malt, hops, grapes, casks, glass and cans, and the cold chain, so planners and buyers know what sits behind each line item."),
    ("briefcase", "Route to market and regulation in India",
     "Excise, state-by-state rules, labels and distribution, explained for commercial and finance teams. A briefing, not legal advice."),
    ("award", "Guided sensory sessions",
     "Tasting the portfolio the team supports, with the vocabulary to talk about it, run responsibly and within your company's policy."),
    ("sliders", "Data and AI in beverages",
     "Where data and GenAI actually help a brewery, winery or distillery, so tech and analytics teams build things the business will use."),
]

TRAINING_FOR = ["New joiners in their first month", "Analytics, data science and BI teams",
                "Supply chain, planning and procurement", "Commercial, marketing and brand teams",
                "Finance, tax and compliance", "Technology and product teams"]

FUNCTIONS = ["Brewing and production", "Quality assurance and the lab", "Packaging and maintenance",
             "Distilling and winemaking", "Sales and distribution", "Marketing and brand",
             "Taproom and hospitality", "Finance, excise and compliance", "Data, digital and AI"]

HIRING_STEPS = [
    ("Scope the role", "We help you write a job description that matches the work, the kit and the size of your operation."),
    ("Find people", "We reach into our network of course alumni, working brewers and industry contacts."),
    ("Screen by people who do the job", "Brewers screen brewers. Candidates get a practical assessment and, for technical roles, a tasting test."),
    ("Train after they join", "New hires can join the right course, so they are productive sooner."),
]


def _programme(icon, title, text):
    return f'<article class="feature reveal"><div class="ic">[[{icon}]]</div><h3>{title}</h3><p>{text}</p></article>'


BODY = banner(
    "For companies", "For companies",
    "Training and hiring for the drinks business.",
    "Domain training for beer, wine and spirits capability centres in Bengaluru, Pune and Hyderabad, "
    "and help finding the right people for every role in a brewery, winery or distillery."
) + f"""
<nav class="wrap co-jump" aria-label="On this page"><a class="seg-chip" href="#training">Corporate training</a><a class="seg-chip" href="#hiring">Hiring support</a></nav>

<section id="training">
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Corporate training</span>
      <h2>Your GCC team supports brands it has never seen made.</h2>
      <p>Beer, wine and spirits companies are building global capability centres in Bengaluru, Pune and Hyderabad. The people in them run analytics, supply chain, finance, marketing and technology for brands brewed and bottled somewhere else.</p>
      <p>The work gets better when they know the product. An analyst who knows what brewhouse yield means asks better questions of the data. A planner who knows why whisky matures faster in Indian heat plans stock better. A marketer who has tasted the range writes better briefs.</p>
      <p>We teach that domain knowledge, built around your portfolio and your teams.</p>
      <div class="cta-pair" style="margin-top:1.4rem"><a class="btn btn-amber" href="{TRAINING_HREF}" data-cta="companies-training">Plan a programme</a><a class="btn btn-wa" href="__WA__" target="_blank" rel="noopener" data-cta="companies-whatsapp">[[whatsapp]] WhatsApp us</a></div>
    </div>
    <div class="prose-block reveal">
      <span class="eyebrow">Who it is for</span>
      <ul class="checklist">{"".join(f"<li>{w}</li>" for w in TRAINING_FOR)}</ul>
      <span class="eyebrow" style="display:block;margin-top:1.6rem">Formats</span>
      <ul class="checklist"><li>Half-day onboarding sessions</li><li>Multi-week programmes for a cohort</li><li>At your office in Bengaluru, Pune or Hyderabad, or live online</li><li>Built around your own brands and processes</li></ul>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Programmes</span><h2>Pick the modules your teams need.</h2></div>
    <div class="features">{"".join(_programme(*p) for p in PROGRAMMES)}</div>
  </div>
</section>

<section id="hiring">
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Hiring support</span>
      <h2>The right people for every function.</h2>
      <p>Breweries, wineries, distilleries and other drinks businesses come to us when they need someone who already knows the work. A CV rarely tells you whether a candidate can run a brew day, hold a cellar at temperature or sell into a state they have never worked.</p>
      <p>We help you find and screen people across the business.</p>
      <ul class="checklist">{"".join(f"<li>{f}</li>" for f in FUNCTIONS)}</ul>
      <div class="cta-pair" style="margin-top:1.4rem"><a class="btn btn-amber" href="{HIRING_HREF}" data-cta="companies-hiring">Tell us the role</a></div>
    </div>
    <div class="prose-block reveal">
      <span class="eyebrow">How it works</span>
      <ol class="co-steps">{"".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in HIRING_STEPS)}</ol>
    </div>
  </div>
</section>

<section class="sand">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Why us</span><h2>Taught and screened by people who have done the work.</h2>
      <p class="lead">Our mentors include a Master Brewer with hands-on experience at global brewing companies who also works in data and AI, a creative strategist with more than 30 years in advertising, and an operations lead with more than 15 years in education and operations. We teach what we have done, and we hire the way we would want to be hired.</p></div>
    <div class="cta-pair"><a class="btn btn-amber" href="{TRAINING_HREF}" data-cta="companies-bottom-training">Corporate training</a><a class="btn btn-ghost" href="{HIRING_HREF}" data-cta="companies-bottom-hiring">Hiring support</a></div>
  </div>
</section>
"""

PAGE = ("For Companies: Training and Hiring | Craft Beer School",
        "Beer, wine and spirits domain training for GCC teams in Bengaluru, Pune and Hyderabad, and hiring support for drinks businesses.",
        "", BODY)
