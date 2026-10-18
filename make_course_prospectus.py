#!/usr/bin/env python3
"""Prospectuses for the two in-person brewery courses, in the house prospectus look:
assets/craft-beer-school-1-day-course.pdf and assets/craft-beer-school-1-month-course.pdf.

The 1-month content follows Chatty's CBS_1-month_2026.pdf (October 2026). Bank details are left
out on purpose: these PDFs are public, payment details go out on enrolment.
Run: python3 make_course_prospectus.py
"""
import re
import subprocess

import make_prospectus as mp

PRICE_DAY, PRICE_MONTH = "₹25,000", "₹1,25,000"
CITIES = "Pune, Delhi, Gurugram and Bengaluru"

EXTRA_CSS = """
table.plan{width:100%;border-collapse:collapse;font-size:9pt;margin-top:4mm}
table.plan th{text-align:left;background:var(--navy);color:#fff;padding:2.2mm 3mm;font-size:8.5pt}
table.plan td{padding:2.4mm 3mm;border-bottom:1px solid var(--line);vertical-align:top}
table.plan td:first-child{font-weight:700;color:var(--navy);white-space:nowrap}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:6mm}
.box{background:var(--sand);border-radius:4mm;padding:5mm 6mm;break-inside:avoid}
.box h3{font-size:12pt;color:var(--navy);margin-bottom:2mm}
.box ul,.box ol{padding-left:4.5mm;font-size:9.4pt}
.box li{margin:.8mm 0}
.fee{background:var(--navy);color:#fff;border-radius:4mm;padding:6mm;margin-top:6mm;display:flex;justify-content:space-between;align-items:center;gap:6mm}
.fee b{font-size:30pt;color:var(--gold);line-height:1}
.fee span{font-size:10pt;color:rgba(255,255,255,.85)}
.terms ol{padding-left:5mm;font-size:9pt;columns:2;column-gap:8mm}
.terms li{margin:0 0 2mm;break-inside:avoid}
"""


def style():
    # The house CSS lives in make_prospectus's f-string; read it from source so this works even when that build does not.
    src = (mp.HERE / "make_prospectus.py").read_text(encoding="utf-8")
    css = re.search(r"<style>(.*?)</style>", src, re.S).group(1).replace("{{", "{").replace("}}", "}")
    return f'<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Hanken+Grotesk:wght@400;600;700;800&family=Space+Mono:wght@700&display=block" rel="stylesheet"><style>{css}{EXTRA_CSS}</style>'


def foot(name):
    return f'<footer class="pf">Craft Beer School · {name} · {mp.SITE}</footer>'


def cover(photo, kicker, title, line):
    return f"""<section class="page cover"><img class="c-img" src="{mp.uri(photo)}" alt=""><div class="shade"></div><div class="bar"></div>
  <div class="in"><img class="logo" src="{mp.uri("assets/footer-logo.png")}" alt="">
    <span class="eyebrow">{kicker}</span><h1>{title}</h1><p>{line}</p></div></section>"""


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def plan(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="plan"><tr>{th}</tr>{trs}</table>'


TERMS = ["<b>Payment.</b> The full fee is paid at sign-up to confirm your seat. Payment details are shared when you enrol.",
         "<b>Refunds.</b> Fees are not refundable. You may transfer your seat to another person with written notice and our approval.",
         "<b>Cancellation.</b> Tell us at least 14 days before the start date if you cannot attend.",
         "<b>Schedule.</b> Dates and timings may move with instructor or brewery availability. We tell you as early as we can.",
         "<b>Travel and stay.</b> Travel, accommodation, meals and personal costs are your own.",
         "<b>Conduct and safety.</b> Follow the brewery's safety rules at all times. Unsafe conduct means removal from the course without a refund.",
         "<b>Placement.</b> We give career guidance and internship recommendations where we can. A job is not guaranteed.",
         "<b>Tasting.</b> Tasting is optional and only for those of legal drinking age in that state. Bring ID."]


def terms_page(name):
    lis = "".join(f"<li>{t}</li>" for t in TERMS)
    return f"""<section class="page"><span class="eyebrow">Before you book</span>
  <h2 style="font-size:24pt;margin:3mm 0 6mm">Terms, safety and how to enrol.</h2>
  <div class="terms"><ol>{lis}</ol></div>
  <div class="cols"><div class="box"><h3>Bring with you</h3>{ul(["Closed-toe shoes and casual clothes you do not mind getting wet", "A notebook and pen", "Photo ID showing your age"])}</div>
  <div class="box"><h3>We provide</h3>{ul(["Safety kit and a safety briefing", "Malt, hops, yeast and all brewing kit", "Course notes and a certificate of completion"])}</div></div>
  <div class="cards" style="margin-top:8mm">
    <div style="background:var(--navy);color:#fff"><b>Website</b><span>{mp.SITE}</span></div>
    <div style="background:var(--navy);color:#fff"><b>WhatsApp and phone</b><span>{mp.PHONE}</span></div>
    <div style="background:var(--navy);color:#fff"><b>Email</b><span>{mp.EMAIL}</span></div>
    <div style="background:var(--navy);color:#fff"><b>Cities</b><span>{CITIES}</span></div></div>
  <p style="font-size:7.5pt;color:var(--soft);margin-top:6mm">Fees and dates are correct at the time of printing and may change; the website has the latest. Drink responsibly.</p>
  {foot(name)}</section>"""


# ---------------------------------------------------------------- 1 day
DAY = "1-Day Super Intensive Craft Beer Course"


def day_html():
    agenda = plan(["Time", "Session", "What you do"], [
        ["Morning", "Welcome and safety", "Brewery safety briefing, the plan for the day and the brew sheet you will follow."],
        ["", "Beer and its ingredients", "Malt, hops, water and yeast: handle and smell each one and learn what it brings to the glass."],
        ["", "Into the brewhouse", "Milling, mashing in and checking mash temperature and pH. Lautering and wort collection."],
        ["Midday", "The boil", "Hop additions, hot break, whirlpool and cooling. Gravity readings and what they tell you."],
        ["Afternoon", "Fermentation and the cellar", "Pitching yeast, fermentation temperature, maturation and carbonation in working tanks."],
        ["", "Quality and hygiene", "Cleaning versus sanitising, how CIP works and the simple lab checks a brewery runs every day."],
        ["Late afternoon", "Tasting and wrap-up", "A guided tasting from the brewery's taps, common off-flavours and your questions. Certificate."]])
    return f"""<!doctype html><html lang="en-IN"><head><meta charset="utf-8">{style()}</head><body>
{cover("assets/rahul-brewhouse.jpg", "In-person course · 2026", "One day. <em>Grain to glass.</em>",
       f"The {DAY}: a full day inside a working microbrewery in {CITIES}, from raw materials to a finished pour.")}

<section class="page about"><span class="eyebrow">The course</span>
  <h2>Brew a real batch with a brewer beside you.</h2>
  <p class="lead">Some brewing only makes sense with your hands on the kit. This course packs the whole process into one classroom-plus-brewery day,
  so you see every step on professional equipment instead of reading about it.</p>
  <div class="facts"><div class="fact"><b>1 day</b><span>Classroom plus brewery</span></div><div class="fact"><b>4</b><span>Cities: {CITIES}</span></div>
    <div class="fact"><b>20</b><span>Students per batch, at most</span></div><div class="fact"><b>Cert.</b><span>Certificate of completion</span></div></div>
  <span class="eyebrow">The day, step by step</span>{agenda}
  <p style="font-size:8.5pt;color:var(--soft);margin-top:3mm">The order of sessions follows the brewery's own brew schedule on the day.</p>
  {foot(DAY)}</section>

<section class="page"><span class="eyebrow">Who it suits</span>
  <h2 style="font-size:24pt;margin:3mm 0 5mm">Exploring brewing before you commit.</h2>
  <div class="cols" style="margin-top:0"><div class="box"><h3>Made for</h3>{ul(["Beer lovers who want to understand what is in the glass", "Homebrewers who have only brewed from kits", "Anyone weighing up a brewing career", "Hospitality and taproom staff who talk about beer every day"])}</div>
  <div class="box"><h3>You leave with</h3>{ul(["A full brew day seen and done on professional kit", "The words and numbers brewers use: OG, FG, ABV, IBU and colour", "A tasting method you can use on any beer", "A certificate and a clear next step if you want to go further"])}</div></div>
  <div class="box" style="margin-top:6mm"><h3>Going further</h3><p style="font-size:9.4pt">Plenty of people take the 1-day course first and come back for the 1-Month Intensive Brewing Excellence Course.
  If you would rather study first, the Brewing Fundamentals Study Book (₹1,999) covers the full syllabus as notes and crosswords.</p></div>
  <div class="fee"><div><span>Course fee per student</span><br><b>{PRICE_DAY}</b></div>
    <span style="max-width:95mm">Includes the brewery day, ingredients, safety kit, course notes, the guided tasting and your certificate. Meals, travel and accommodation are not included.</span></div>
  {foot(DAY)}</section>

{terms_page(DAY)}
</body></html>"""


# ---------------------------------------------------------------- 1 month
MONTH = "1-Month Intensive Brewing Excellence Course"


def month_html():
    weeks = plan(["Week", "Focus", "Key topics"], [
        ["Week 1 · Days 1-2", "Brewing fundamentals", "Beer basics, raw materials (malt, hops, water, yeast), beer styles"],
        ["Week 2 · Days 3-4", "Brewhouse operations", "Milling, mashing, lautering, wort boiling and hop utilisation"],
        ["Week 3 · Days 5-6", "Fermentation and yeast management", "Fermentation control, yeast propagation, maturation, filtration"],
        ["Week 4 · Days 7-8", "Hands-on and quality control", "A complete brew, sensory evaluation, micro control, hygiene (CIP)"]])
    schedule = plan(["Week", "In class and online", "Lab work", "At the brewery"], [
        ["Week 1", "Beer fundamentals, malt science, raw materials", "Sensory evaluation and beer tasting", "Brewing basics and beer styles"],
        ["Week 2", "Hop chemistry, brewhouse operations, mashing and lautering", "Quality control testing and water analysis", "Brewhouse operations and wort boiling"],
        ["Week 3", "Fermentation science, yeast biology, temperature control", "Micro analysis, sanitation and hygiene (CIP)", "Fermentation and maturation"],
        ["Week 4", "Quality control, special beer types, recipe development", "Advanced testing, packaging and labelling", "A complete brew and certification"]])
    topics = ["Basics of brewing technology and beer science", "Raw materials: malt types, hop selection, water chemistry and yeast strains",
              "Brewhouse operations: milling, mashing, lautering and wort collection", "Wort boiling, hop utilisation and wort treatment",
              "Fermentation science and by-product control", "Yeast management, propagation and storage",
              "Filtration, stabilisation and carbonation", "Micro control, hygiene and CIP (clean in place)",
              "Filling, dispensing and packaging quality", "Special beer types: lagers, ales, wheat beers and sour beers",
              "Sensory evaluation and professional tasting", "Recipe development and a hands-on brew from grain to glass"]
    return f"""<!doctype html><html lang="en-IN"><head><meta charset="utf-8">{style()}</head><body>
{cover("assets/rahul-cohort-1.jpg", "In-person course · 2026", "Four weeks to <em>brew for real.</em>",
       f"The {MONTH}: in class, online, in the lab and on site in working microbreweries. 48 contact hours, at most 20 students.")}

<section class="page about"><span class="eyebrow">Programme overview</span>
  <h2>From brewing fundamentals to a full brew of your own.</h2>
  <p class="lead">A hybrid programme for aspiring brewers, professionals, enthusiasts and beer business founders. You learn the theory online and in class,
  test it in the lab and then brew it in a working microbrewery, guided by experienced brewers and educators.</p>
  <div class="facts"><div class="fact"><b>4 weeks</b><span>Weekdays and weekends</span></div><div class="fact"><b>48</b><span>Contact hours, 2 to 3 a day</span></div>
    <div class="fact"><b>20</b><span>Students per batch, at most</span></div><div class="fact"><b>3</b><span>Brewery visits</span></div></div>
  <span class="eyebrow">Curriculum at a glance</span>{weeks}
  <div class="cols"><div class="box"><h3>Every topic covered</h3>{ul(topics[:6])}</div><div class="box"><h3>&nbsp;</h3>{ul(topics[6:])}</div></div>
  {foot(MONTH)}</section>

<section class="page"><span class="eyebrow">How you learn</span>
  <h2 style="font-size:24pt;margin:3mm 0 4mm">Theory first, then the lab, then the brewery.</h2>
  <div class="cols" style="grid-template-columns:1fr 1fr 1fr;margin-top:0">
    <div class="box"><h3>Online and in class</h3>{ul(["Brewing science and theory", "Video lectures and digital materials", "Self-paced study before each lab and brewery session"])}</div>
    <div class="box"><h3>Lab work</h3>{ul(["Quality control and sensory testing", "Micro analysis and brewery chemistry", "Hands-on lab technique with expert guidance"])}</div>
    <div class="box"><h3>At the brewery</h3>{ul(["Hands-on brewing in working microbreweries", "Full cycles from mashing to fermentation", "Real kit and professional recipes"])}</div></div>
  <span class="eyebrow" style="display:block;margin-top:7mm">Week by week</span>{schedule}
  <p style="font-size:8.5pt;color:var(--soft);margin-top:3mm">Online modules are open on weekdays and weekends. Student assignments fall mid-week. Dates are confirmed per batch.</p>
  {foot(MONTH)}</section>

<section class="page"><span class="eyebrow">What you receive</span>
  <h2 style="font-size:24pt;margin:3mm 0 5mm">Hands-on hours, lab access and a certificate.</h2>
  <div class="cols" style="margin-top:0"><div class="box"><h3>Included</h3>{ul(["48 hours of intensive hands-on instruction", "Professional brewery access and a full brewing experience", "Course materials and a digital learning kit", "Quality control lab access and testing protocols", "Certificate of completion (80% attendance needed)", "Internship recommendations and career guidance"])}</div>
  <div class="box"><h3>Not included</h3>{ul(["Meals and refreshments", "Transport", "Accommodation, which students arrange themselves"])}
  <h3 style="margin-top:4mm">Good to know</h3>{ul(["The course is designed to finish within one month. If a student extends it, extra fees apply.", "Timings can shift for faculty or student clashes. We tell you in advance."])}</div></div>
  <div class="fee"><div><span>Course fee per student</span><br><b>{PRICE_MONTH}</b></div>
    <span style="max-width:95mm">Rupees one lakh twenty five thousand only. No taxes are applicable. Paid in full at sign-up.</span></div>
  {foot(MONTH)}</section>

{terms_page(MONTH)}
</body></html>"""


def render(html, out):
    tmp = mp.HERE / f".{out.stem}.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([mp.CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=15000",
                    f"--print-to-pdf={out}", tmp.resolve().as_uri()], check=True, capture_output=True)
    tmp.unlink()
    import fitz
    doc = fitz.open(out)
    doc.set_metadata({"title": out.stem.replace("-", " ").title(), "author": "Ankur Napa", "creator": "Ankur Napa", "producer": "Craft Beer School"})
    doc.saveIncr()
    print("wrote", out.relative_to(mp.HERE), doc.page_count, "pages")


def main():
    render(day_html(), mp.HERE / "assets/craft-beer-school-1-day-course.pdf")
    render(month_html(), mp.HERE / "assets/craft-beer-school-1-month-course.pdf")


if __name__ == "__main__":
    main()
