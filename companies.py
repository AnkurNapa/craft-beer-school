# -*- coding: utf-8 -*-
"""Corporate services: training, hiring, brand and marketing consultancy,
market entry into India, and digital transformation, for drinks businesses.

Team facts here must match what the About page already says about the
mentors. Do not add employers, numbers or claims that are not on the site.
"""
from pages_a import banner, enroll_href
import photos

SLUG = "for-companies.html"
TRAINING_HREF = enroll_href("Corporate training")
HIRING_HREF = enroll_href("Hiring support")
BRAND_HREF = enroll_href("Brand and marketing consultancy")
ENTRY_HREF = enroll_href("Market entry into India")
DIGITAL_HREF = enroll_href("Digital transformation consulting")

SERVICES = [
    ("cap", "Corporate training", "Beverage domain training for GCC teams in Bengaluru, Pune and Hyderabad.", "#training"),
    ("users", "Hiring support", "The right people for every function in a brewery, winery or distillery.", "#hiring"),
    ("megaphone", "Brand and digital marketing", "Brand, packaging, content and digital marketing for beer and drinks brands.", "#brand"),
    ("globe", "Market entry into India", "For beer brands, ingredient, raw material and packaging companies from abroad.", "#india"),
    ("sliders", "Digital transformation", "Data, dashboards, software and AI for breweries and drinks businesses.", "#digital"),
]

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


def _service(icon, title, text, href):
    return (f'<a class="feature service reveal" href="{href}"><div class="ic">[[{icon}]]</div>'
            f'<h3>{title}</h3><p>{text}</p><span class="link-arrow">How it works</span></a>')


BODY = banner(
    "Corporate services", "Corporate services",
    "Training, hiring and consulting for the drinks business.",
    "For breweries, wineries, distilleries, beverage GCCs and companies bringing beer, ingredients "
    "or packaging to India. Five services, one team that has worked inside the industry."
) + f"""
<section style="padding-bottom:1rem">
  <div class="wrap">
    <div class="features services">{"".join(_service(*x) for x in SERVICES)}</div>
  </div>
</section>

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
      {photos.figure("service:training", "A guided tasting session")}
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
      {photos.figure("service:hiring", "A brewer at work")}
      <span class="eyebrow">How it works</span>
      <ol class="co-steps">{"".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in HIRING_STEPS)}</ol>
    </div>
  </div>
</section>

<section class="tint" id="brand">
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Brand and digital marketing consultancy</span>
      <h2>A beer brand people remember, marketed within the rules.</h2>
      <p>Most craft beer in India is sold by word of mouth, a label on a shelf and a social feed. We help breweries and drinks brands get those right: who the brand is for, what it is called, how it looks on the shelf and in a feed, and how it reaches people.</p>
      <p>Alcohol advertising in India is restricted, and the rules vary by state and change, so every plan we write works inside them. Where a formal opinion is needed, we work alongside your legal advisers.</p>
      <div class="cta-pair" style="margin-top:1.4rem"><a class="btn btn-amber" href="{BRAND_HREF}" data-cta="companies-brand">Talk about your brand</a></div>
    </div>
    <div class="prose-block reveal">
      {photos.figure("service:brand", "Beer bottles on a shelf")}
      <span class="eyebrow">What we do</span>
      <ul class="checklist"><li>Brand strategy, positioning and naming</li><li>Label and packaging direction</li><li>Launch plans for a new beer or brand</li><li>Social media and content, including GenAI workflows</li><li>Digital marketing that respects alcohol advertising rules</li><li>Taproom marketing, events and community</li></ul>
    </div>
  </div>
</section>

<section id="india">
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Market entry into India</span>
      <h2>Bringing beer, ingredients or packaging to India.</h2>
      <p>For companies outside India who want to sell here: beer brands, maltsters, hop and yeast suppliers, adjunct and ingredient makers, can, glass, keg and label suppliers, and equipment makers.</p>
      <p>India is not one market. Licences, excise, labelling and distribution change from state to state, and the brewers you want to sell to are spread across a handful of cities. We help you work out where to start and who to start with, and we work alongside your legal and tax advisers on the formal steps.</p>
      <div class="cta-pair" style="margin-top:1.4rem"><a class="btn btn-amber" href="{ENTRY_HREF}" data-cta="companies-india">Plan your entry</a></div>
    </div>
    <div class="prose-block reveal">
      {photos.figure("service:india", "A barley field")}
      <span class="eyebrow">What we do</span>
      <ul class="checklist"><li>A read of the market for your product: who buys it, where and why</li><li>A state-by-state map of the rules that apply to you</li><li>Finding partners: contract brewers, importers, distributors and agents</li><li>Introductions to breweries, maltsters and buyers</li><li>Pricing and route to market</li><li>Launch support and training for your local team</li></ul>
    </div>
  </div>
</section>

<section class="tint" id="digital">
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Digital transformation</span>
      <h2>Data, software and AI that a brewery will actually use.</h2>
      <p>We help breweries and drinks businesses move from paper, WhatsApp and memory to systems the whole team uses: brew and cellar records, stock and batch tracking, dashboards for the numbers that matter, and AI where it saves real time.</p>
      <p>We start with how the business runs today, not with a software catalogue, and leave you with a plan you can afford and keep doing. If your team wants to learn it themselves, the <a href="digital-transformation-basics-for-brewing-course.html" style="color:var(--blue);text-decoration:underline">Digital Transformation</a> and <a href="ai-for-craft-breweries-course.html" style="color:var(--blue);text-decoration:underline">AI for Craft Breweries</a> courses cover the basics.</p>
      <div class="cta-pair" style="margin-top:1.4rem"><a class="btn btn-amber" href="{DIGITAL_HREF}" data-cta="companies-digital">Start with a conversation</a></div>
    </div>
    <div class="prose-block reveal">
      {photos.figure("service:digital", "Brewery tanks")}
      <span class="eyebrow">What we do</span>
      <ul class="checklist"><li>Mapping how production, stock and sales run today</li><li>Choosing brewery management or ERP software, or staying with spreadsheets</li><li>Dashboards for production, quality, stock and sales</li><li>Sensors and logging on fermenters and cold rooms</li><li>AI use cases worth doing, and the ones to skip</li><li>A 90-day roadmap and help delivering it</li></ul>
    </div>
  </div>
</section>

<section class="sand">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Why us</span><h2>Taught and screened by people who have done the work.</h2>
      <p class="lead">Our mentors include a Master Brewer with hands-on experience at global brewing companies who also works in data and AI, a creative strategist with more than 30 years in advertising, and an operations lead with more than 15 years in education and operations. We teach what we have done, and we hire the way we would want to be hired.</p></div>
    <div class="cta-pair"><a class="btn btn-amber" href="contact.html#enroll" data-cta="companies-bottom-enquire">Talk to us</a><a class="btn btn-wa" href="__WA__" target="_blank" rel="noopener" data-cta="companies-bottom-whatsapp">[[whatsapp]] WhatsApp us</a></div>
  </div>
</section>
"""

PAGE = ("Corporate Services | Craft Beer School",
        "Training for beverage GCCs, hiring, brand and digital marketing, market entry into India and digital transformation for drinks businesses.",
        "", BODY)
