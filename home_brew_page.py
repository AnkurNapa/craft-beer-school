# -*- coding: utf-8 -*-
"""1 Month Home Brewing Course: online lessons with live video call tutorials, ₹65,000.

Built like starters_page.py because it runs alongside the in-person 1-month course
and does not fit the online template in course_pages.py. The copy follows Chatty's
course notes (14 Nov 2026) and the syllabus PDF built in ~/Documents/cbs-home-brewing-syllabus.
"""
from pages_a import banner
from inperson_pages import _list

SLUG = "1-month-home-brewing-online-course.html"
NAME = "1 Month Home Brewing Course"
FEE = "₹65,000"
PDF = "assets/craft-beer-school-home-brewing-course.pdf"
ENROL = "contact.html?course=1%20Month%20Home%20Brewing%20Course#enroll"

FACTS = [("Format", "Online + video call tutorials"), ("Duration", "1 month"),
         ("Hands on", "One beer brewed at home"), ("Fee", FEE + " + GST, paid in full")]

WEEKS = [
    ("Week 1. Beer fundamentals",
     "What beer is, the four ingredients, the main types of beer and how beer is made, before you buy a single piece of kit. Live tutorial: grain to glass."),
    ("Week 2. Set up, recipe and brew day",
     "Commercial against home brewing, what qualifies as home brew, ingredients, equipment and hygiene. You write a basic recipe, then brew one chosen beer at home with a mentor guiding you on a video call. Mid course assignment."),
    ("Week 3. Fermentation and quality control",
     "Temperature, timing and gravity readings, a fermentation log, common faults plus the dos and don'ts most first batches miss. Live tutorial: your log reviewed."),
    ("Week 4. Packaging, tasting and your next batch",
     "Bottling and carbonation, tasting your own beer honestly and changing a recipe for your second brew. Final assignment: a full brew report."),
]

INCLUDED = ["Online lessons and recorded videos for every topic",
            "Live video call tutorials, including the guided brew day",
            "Course notes, a recipe sheet, a brew day log and a tasting sheet",
            "Mentor feedback on both assignments",
            "4 brewing video calls after the course",
            "Certificate of completion"]

NOT_INCLUDED = ["Home brewing equipment and ingredients, bought from the list we share in week 2",
                "Bottles, caps and cleaning supplies",
                "Delivery charges for anything you order"]


def _ctas(tag):
    pdf = (f'<a href="{PDF}" class="btn btn-ghost" download data-cta="homebrew-{tag}-syllabus">Download syllabus</a>'
           if tag != "bottom" else "")  # the ghost button vanishes on the dark CTA band
    return (f'<a href="{ENROL}" class="btn btn-amber" data-cta="homebrew-{tag}-enroll">Enrol now</a>'
            f'<a href="__WA__" class="btn btn-wa" target="_blank" rel="noopener" data-cta="homebrew-{tag}-whatsapp">[[whatsapp]] Ask on WhatsApp</a>{pdf}')


def render():
    facts = "".join(f"<div><span>{k}</span><b>{v}</b></div>" for k, v in FACTS)
    weeks = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in WEEKS)
    return banner(f'<a href="courses.html">Courses</a> / {NAME}', "Online · 1 month · " + FEE,
                  f"{NAME}. Brew your first beer at home.",
                  "Four weeks online, with live video call tutorials and a mentor beside you on brew day. You finish with a beer you made yourself.") + f"""
<section style="padding-block:0">
  <div class="wrap course-facts">{facts}<div class="cta-pair">{_ctas("facts")}</div></div>
</section>

<section>
  <div class="wrap split" style="align-items:start">
    <div class="prose-block reveal"><span class="eyebrow">How it works</span><h2>Learn online. Brew at home.</h2>
      <p>You learn at your own pace from online lessons, then join live video calls where a mentor teaches, answers your questions and guides you through your first brew day in your own kitchen.</p>
      <p>No brewing experience needed. You buy your own kit and ingredients from the list we share in week 2.</p></div>
    <div class="prose-block reveal"><span class="eyebrow">After the course</span><h2>Help with your next batches.</h2>
      <p>Your beer keeps conditioning after week 4, so support carries on. You get 4 brewing video calls with a mentor to taste your first batch together, fix any problems and plan your next brews.</p></div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Syllabus</span><h2>Four weeks, week by week.</h2>
      <p class="lead">Session dates for each batch are shared when you enrol. <a href="{PDF}" download style="color:var(--blue);text-decoration:underline">Download the full syllabus</a>.</p></div>
    <dl class="logistics">{weeks}</dl>
  </div>
</section>

<section>
  <div class="wrap split" style="align-items:start">
    <div class="prose-block reveal"><span class="eyebrow">What is included</span><h2>In the fee.</h2><ul class="checklist">{_list(INCLUDED)}</ul></div>
    <div class="prose-block reveal"><span class="eyebrow">What is not included</span><h2>Bought by you.</h2><ul class="checklist">{_list(NOT_INCLUDED)}</ul>
      <p style="color:var(--ink-soft);font-size:.9rem">The certificate needs at least 60% attendance at the live sessions plus both assignments. The fee of {FEE} plus GST is paid in full at enrolment. Read the <a href="refund.html" style="color:var(--blue);text-decoration:underline">refund policy</a> before you pay. This course is for adults of legal drinking age.</p></div>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>One month. One beer you made yourself.</h2><p>Enrol now and we send you the batch dates. We reply within 24 hours.</p><div class="cta-pair" style="justify-content:center">{_ctas("bottom")}</div></div></section>
"""


def pages():
    """slug -> (title, desc, active, body) for build.PAGES."""
    desc = (f"{NAME}: four weeks online with live video call tutorials. Brew one beer at home "
            f"with a mentor guiding you, then 4 follow-up calls. {FEE}.")
    return {SLUG: (f"{NAME} Online | Craft Beer School", desc, "courses", render())}


# First card in the online grid on courses.html, in the same tile style as the online courses.
CARD = (f'<article class="card course-card reveal" data-type="online" data-subject="brewing">'
        f'<img class="tile-img" src="assets/stock/track-brewing.jpg" srcset="assets/stock/track-brewing-sm.jpg 640w, assets/stock/track-brewing.jpg 1024w" '
        f'sizes="(max-width: 680px) 92vw, 400px" alt="{NAME}" width="1024" height="683" loading="lazy" decoding="async" />\n'
        f'  <div class="top"><span class="course-no">New / Home brewing</span><span class="course-dur">1 Month</span></div>\n'
        f'  <div class="card-body">\n'
        f'    <span class="mode mode-online">Online + video tutorials</span>\n'
        f'    <h3><a href="{SLUG}">{NAME}</a></h3>\n'
        f'    <p>Learn online, then brew your first beer at home with a mentor guiding you on a video call. '
        f'Four weeks, two assignments and 4 brewing calls after the course.</p>\n'
        f'    <ul><li>Beer fundamentals and ingredients</li><li>Home brewing kit, hygiene and a recipe</li>'
        f'<li>One beer brewed at home with a mentor</li><li>Fermentation, bottling and tasting</li></ul>\n'
        f'    <a href="{SLUG}" class="link-arrow" data-cta="homebrew-card-details">Full syllabus</a>\n'
        f'    <div class="foot"><span class="price">{FEE}</span><a href="{ENROL}" class="btn btn-ghost" style="padding:.55rem 1.1rem" '
        f'data-cta="homebrew-card-enroll" aria-label="Enrol in {NAME}">Enrol</a></div>\n'
        f'  </div>\n</article>')
