# -*- coding: utf-8 -*-
"""One detail page per in-person course on courses.html.

The 1-day and 1-month copy mirrors make_course_prospectus.py (the PDFs). The
four smaller courses only state what their courses.html card already says.
"""
from pages_a import banner

HUB = "in-person-brewing-courses-pune-delhi-gurugram-bengaluru.html"
CITIES = "Pune, Delhi, Gurugram and Bengaluru"

# Same terms as the in-person prospectuses.
TERMS = [("Payment", "The full fee is paid at sign-up to confirm your seat. Payment details are shared when you enrol."),
         ("Refunds", "Fees are not refundable. You may transfer your seat to another person with written notice and our approval."),
         ("Cancellation", "Tell us at least 14 days before the start date if you cannot attend."),
         ("Schedule", "Dates and timings may move with instructor or brewery availability. We tell you as early as we can."),
         ("Travel and stay", "Travel, accommodation, meals and personal costs are your own."),
         ("Safety", "Follow the brewery's safety rules at all times. Unsafe conduct means removal from the course without a refund."),
         ("Tasting", "Tasting is optional and only for those of legal drinking age in that state. Bring ID.")]

BRING = ["Closed-toe shoes and casual clothes you do not mind getting wet", "A notebook and pen", "Photo ID showing your age"]

COURSES = [
    dict(slug="1-day-super-intensive-craft-beer-course-in-person.html",
         name="1-Day Super Intensive Craft Beer Course", short="1-Day Craft Beer Course",
         eyebrow="In person · 4 cities",
         blurb="A full day inside a working microbrewery, from raw materials to a finished pour.",
         enrol="contact.html?course=1-Day%20Super%20Intensive%20Craft%20Beer%20Course#enroll",
         pdf="assets/craft-beer-school-1-day-course.pdf",
         facts=[("Format", "In person"), ("Duration", "1 day"), ("Cities", "Pune, Delhi, Gurugram, Bengaluru"),
                ("Batch", "Max 20"), ("Fee", "₹25,000")],
         plan_title="The day, step by step.",
         plan_lead="The order of sessions follows the brewery's own brew schedule on the day.",
         plan=[("Welcome and safety", "Brewery safety briefing, the plan for the day and the brew sheet you will follow."),
               ("Beer and its ingredients", "Malt, hops, water and yeast: handle and smell each one and learn what it brings to the glass."),
               ("Into the brewhouse", "Milling, mashing in and checking mash temperature and pH. Lautering and wort collection."),
               ("The boil", "Hop additions, hot break, whirlpool and cooling. Gravity readings and what they tell you."),
               ("Fermentation and the cellar", "Pitching yeast, fermentation temperature, maturation and carbonation in working tanks."),
               ("Quality and hygiene", "Cleaning versus sanitising, how CIP works and the simple lab checks a brewery runs every day."),
               ("Tasting and wrap-up", "A guided tasting from the brewery's taps, common off-flavours and your questions. Certificate.")],
         who=["Beer lovers who want to understand what is in the glass", "Homebrewers who have only brewed from kits",
              "Anyone weighing up a brewing career", "Hospitality and taproom staff who talk about beer every day"],
         gain=["A full brew day seen and done on professional kit", "The words and numbers brewers use: OG, FG, ABV, IBU and colour",
               "A tasting method you can use on any beer", "A certificate and a clear next step if you want to go further"],
         included="The brewery day, ingredients, safety kit, course notes, the guided tasting and your certificate. Meals, travel and accommodation are not included.",
         terms=True),
    dict(slug="1-month-intensive-brewing-excellence-course-in-person.html",
         name="1-Month Intensive Brewing Excellence Course", short="1-Month Brewing Course",
         eyebrow="In person · 4 cities",
         blurb="Four weeks of classes, online study, lab work and hands-on brewing in partner microbreweries.",
         enrol="contact.html?course=1-Month%20Intensive%20Brewing%20Excellence%20Course#enroll",
         pdf="assets/craft-beer-school-1-month-course.pdf",
         facts=[("Format", "In person + online"), ("Duration", "4 weeks"), ("Contact hours", "48, 2 to 3 a day"),
                ("Batch", "Max 20"), ("Fee", "₹1,25,000")],
         plan_title="Week by week.",
         plan_lead="Theory online and in class, then the lab, then the brewery. Dates are confirmed per batch.",
         plan=[("Week 1. Brewing fundamentals", "Beer basics, malt science, raw materials and beer styles. Lab: sensory evaluation and beer tasting."),
               ("Week 2. Brewhouse operations", "Hop chemistry, milling, mashing, lautering and wort boiling. Lab: quality control testing and water analysis."),
               ("Week 3. Fermentation and yeast management", "Fermentation science, yeast propagation, temperature control, maturation and filtration. Lab: micro analysis plus sanitation and hygiene (CIP)."),
               ("Week 4. Hands-on and quality control", "Quality control, special beer types and recipe development. Lab: advanced testing, packaging and labelling. A complete brew of your own and certification.")],
         who=["Homebrewers who want to fix recurring faults", "Professionals moving into brewing",
              "Anyone planning a brewery, a brewpub or a beer brand"],
         gain=["48 hours of intensive hands-on instruction", "Quality control lab access and testing protocols",
               "Course materials and a digital learning kit", "Certificate of completion (80% attendance needed)",
               "Internship recommendations and career guidance"],
         included="Instruction, brewery access, lab access, course materials and your certificate. No taxes are applicable. Meals, transport and accommodation are not included. If a student extends past one month, extra fees apply.",
         terms=True),
    dict(slug="home-visit-brewing-course-in-person.html",
         name="1-Day Home Visit Brewing Course", short="Home Visit Brewing Course",
         eyebrow="In person · At your home",
         blurb="Our brew master comes to your home with all the equipment and ingredients needed to brew your first batch, start to finish.",
         enrol="contact.html?course=In-person+workshop+%2F+tasting#enroll", pdf=None,
         facts=[("Format", "In person"), ("Duration", "1 day"), ("Where", "Your home"), ("Fee", "On enquiry")],
         who=["Beginners who want to brew a first batch at home", "Anyone who would rather learn on their own kitchen stove than in a brewery"],
         gain=["Your first batch, brewed start to finish", "Hands-on time with every step, guided by our brew master"],
         included="All the equipment and ingredients for the brew. Tell us your city when you enquire and we confirm the date and fee."),
    dict(slug="professional-beer-tasting-day-in-person.html",
         name="Professional Beer Tasting Day", short="Beer Tasting Day",
         eyebrow="In person · Bengaluru",
         blurb="Taste the way brewers, judges and buyers do.",
         enrol="contact.html?course=Professional%20Beer%20Tasting%20Day#enroll", pdf=None,
         facts=[("Format", "In person"), ("Duration", "1 day"), ("City", "Bengaluru"), ("Fee", "₹4,999")],
         who=["Beer lovers who want to taste with purpose", "Homebrewers who want to spot faults in their own beer",
              "Bar, taproom and sales staff who describe beer every day"],
         gain=["A guided flight across the main styles, from lager, wheat and pale ale to IPA, stout, sour and Belgian",
               "Spiked samples of the common off-flavours, so you know them on sight", "The professional tasting method",
               "Proper tasting notes and an industry scoresheet for every beer"],
         included="Beers, tasting kit and scoresheets. Tasting is only for those of legal drinking age. Bring ID."),
    dict(slug="brewery-business-tour-in-person.html",
         name="Brewery Business Tour", short="Brewery Business Tour",
         eyebrow="In person · Bengaluru",
         blurb="For anyone thinking about a brewery or brewpub business.",
         enrol="contact.html?course=Brewery%20Business%20Tour#enroll", pdf=None,
         facts=[("Format", "Guided tour"), ("Duration", "Half day"), ("City", "Bengaluru"), ("Fee", "On enquiry")],
         who=["Would-be founders weighing up a brewery or brewpub", "Investors and partners who want to see the business up close"],
         gain=["A walk through a working Bengaluru brewery with a brewer who runs one: brewhouse, cellar, cold room and taproom",
               "Straight answers on cost, licences, staffing and space", "What nobody tells you before you start"],
         included="The guided tour and time for your questions. Dates are confirmed when you enquire."),
    dict(slug="2-hour-craft-beer-tasting-course-in-person.html",
         name="2-Hour Craft Beer Tasting Course", short="2-Hour Beer Tasting Course",
         eyebrow="In person · Bengaluru",
         blurb="A guided tasting flight in Bengaluru. Learn to read aroma, flavour and style in two focused hours.",
         enrol="contact.html?course=In-person+workshop+%2F+tasting#enroll", pdf=None,
         facts=[("Format", "In person"), ("Duration", "2 hours"), ("City", "Bengaluru"), ("Fee", "On enquiry")],
         who=["Anyone new to craft beer", "Friends or teams looking for a tasting with real learning in it"],
         gain=["A guided tasting flight", "How to read aroma, flavour and style in any glass"],
         included="The tasting flight. Tasting is only for those of legal drinking age. Bring ID."),
]


def _ctas(c, tag):
    pdf = (f'<a href="{c["pdf"]}" class="btn btn-ghost" download data-cta="inperson-{tag}-prospectus">Download prospectus</a>'
           if c["pdf"] and tag != "bottom" else "")  # the ghost button vanishes on the dark CTA band
    return (f'<a href="{c["enrol"]}" class="btn btn-amber" data-cta="inperson-{tag}-enroll">Book a seat</a>'
            f'<a href="__WA__" class="btn btn-wa" target="_blank" rel="noopener" data-cta="inperson-{tag}-whatsapp">[[whatsapp]] Ask on WhatsApp</a>{pdf}')


def _list(items):
    return "".join(f"<li>{i}</li>" for i in items)


def _plan(c):
    if not c.get("plan"):
        return ""
    steps = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in c["plan"])
    return f"""<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">The plan</span><h2>{c["plan_title"]}</h2><p class="lead">{c["plan_lead"]}</p></div>
    <dl class="logistics">{steps}</dl>
  </div>
</section>"""


def render(c):
    facts = "".join(f"<div><span>{k}</span><b>{v}</b></div>" for k, v in c["facts"])
    terms = ("".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in TERMS)
             + f"<div><dt>Bring with you</dt><dd>{'. '.join(BRING)}.</dd></div>") if c.get("terms") else ""
    terms_block = f'<dl class="logistics">{terms}</dl>' if terms else ""
    return banner(f'<a href="courses.html">Courses</a> / {c["name"]}', c["eyebrow"], c["name"], c["blurb"]) + f"""
<section style="padding-block:0">
  <div class="wrap course-facts">{facts}<div class="cta-pair">{_ctas(c, "facts")}</div></div>
</section>

<section>
  <div class="wrap split" style="align-items:start">
    <div class="prose-block reveal"><span class="eyebrow">Who it is for</span><h2>Is this for you?</h2><ul class="checklist">{_list(c["who"])}</ul></div>
    <div class="prose-block reveal"><span class="eyebrow">What you get</span><h2>What you walk away with.</h2><ul class="checklist">{_list(c["gain"])}</ul></div>
  </div>
</section>

{_plan(c)}

<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Before you book</span><h2>Included and terms.</h2><p class="lead">{c["included"]}</p></div>
    {terms_block}
    <p style="margin-top:1.5rem;color:var(--ink-soft);font-size:.9rem">Compare every <a href="courses.html#in-person" style="color:var(--blue);text-decoration:underline">in-person course</a>, read <a href="{HUB}" style="color:var(--blue);text-decoration:underline">which one suits you</a> and check the <a href="refund.html" style="color:var(--blue);text-decoration:underline">refund policy</a> before you pay.</p>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Book the {c["name"]}.</h2><p>Tell us your city and dates. We reply within 24 hours.</p><div class="cta-pair" style="justify-content:center">{_ctas(c, "bottom")}</div></div></section>
"""


def pages():
    """slug -> (title, desc, active, body) for build.PAGES."""
    out = {}
    for c in COURSES:
        title = f"{c['name']} | Craft Beer School"
        if len(title) > 60:
            title = f"{c['short']} | Craft Beer School"
        fee = dict(c["facts"])["Fee"]
        where = dict(c["facts"]).get("City") or dict(c["facts"]).get("Where") or CITIES
        desc = f"{c['name']}: {dict(c['facts'])['Duration'].lower()} in person, {where}. Fee {fee.lower() if fee == 'On enquiry' else fee}. {c['blurb']}"
        if len(desc) > 160:
            desc = desc[:157].rsplit(" ", 1)[0] + "..."
        out[c["slug"]] = (title, desc, "courses", render(c))
    return out


SLUG = {c["name"]: c["slug"] for c in COURSES}
