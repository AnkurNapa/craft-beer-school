#!/usr/bin/env python3
"""Downloadable course prospectus: assets/craft-beer-school-prospectus.pdf

Built from the same course list, tracks, team and photo records as the site,
then printed with headless Chrome (no PDF libraries needed). Run after any
course or photo change:  python3 make_prospectus.py
"""
import html
import pathlib
import re
import subprocess

import course_pages
import pages_a
import photos

HERE = pathlib.Path(__file__).parent
OUT = HERE / "assets/craft-beer-school-prospectus.pdf"
TMP = HERE / ".prospectus.html"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SITE = "craftbeerschool.in"
PHONE, EMAIL = "+91 98209 25347", "chatty@cheerschattyventures.com"
BY_NAME = {c["name"]: c for c in pages_a.COURSE_DATA}
PHOTOS = photos._all()
TRACK_SLOT = {"Brewing": "track:brewing", "Business &amp; tech": "track:business", "Spirits": "track:spirits",
              "Beyond beer": "track:beyond", "Free &amp; in Bengaluru": "track:bengaluru"}


def uri(rel):
    return (HERE / rel).resolve().as_uri()


def img(slot, cls=""):
    r = PHOTOS.get(slot)
    return f'<img class="{cls}" src="{uri(r["file"])}" alt="">' if r else ""


def course_block(c):
    d = course_pages.DETAIL[course_pages.plain(c["name"])]
    items = "".join(f"<li>{i}</li>" for i in c["items"])
    who = html.escape(re.sub("<[^>]+>", "", d["who"][0]))
    return f"""<article class="course">
  <div class="c-head"><h3>{c["name"]}</h3><span class="pill">{c["dur"]} · {c["price"]}</span></div>
  <p>{c["blurb"]}</p>
  <ul>{items}</ul>
  <p class="who">For: {who.lower()[0].upper() + who[1:]}</p>
</article>"""


def track_page(icon_title, line, names):
    courses = "".join(course_block(BY_NAME[n]) for n in names)
    extra = ""
    if icon_title == "Brewing":
        extra = '<article class="course note"><h3>WSET Beer exam prep</h3><p>Preparation for every WSET Beer level, in groups or one-to-one: syllabus, guided tastings and mock papers. You sit the exam through a WSET Approved Programme Provider.</p></article>'
    if icon_title.startswith("Free"):
        extra = ('<article class="course"><div class="c-head"><h3>Professional Beer Tasting Day</h3><span class="pill">1 day · ₹4,999</span></div>'
                 '<p>In person in Bengaluru. A guided flight across the main styles plus spiked off-flavour samples. The professional tasting method, written notes and an industry scoresheet. Beers and kit included.</p></article>'
                 '<article class="course"><div class="c-head"><h3>Brewery Business Tour</h3><span class="pill">Half day · On enquiry</span></div>'
                 '<p>For anyone thinking about a brewery or brewpub. Walk a working Bengaluru brewery with a brewer who runs one, then the questions on cost, licences, staffing and space.</p></article>')
    return f"""<section class="page track">
  <div class="t-hero">{img(TRACK_SLOT[icon_title], "t-img")}<div class="t-over"><span class="eyebrow">Track</span><h2>{icon_title}</h2><p>{line}</p></div></div>
  <div class="courses">{courses}{extra}</div>
  <footer class="pf">Craft Beer School · {SITE}</footer>
</section>"""


def build_html():
    tracks = "".join(track_page(t, line, names) for _, t, line, names in pages_a.TRACKS)
    n = len(pages_a.COURSE_DATA)
    return f"""<!doctype html><html lang="en-IN"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Hanken+Grotesk:wght@400;600;700;800&family=Space+Mono:wght@700&display=block" rel="stylesheet">
<style>
@page{{size:A4;margin:0}}
*{{box-sizing:border-box;margin:0}}
:root{{--navy:#123c4a;--deep:#0c2b35;--amber:#d9862a;--gold:#f3c34d;--mint:#cfeadb;--ink:#1d1d1f;--soft:#5f6368;--sand:#faf7f1;--line:#e8e8ed}}
body{{font-family:"Hanken Grotesk",sans-serif;color:var(--ink);font-size:10.5pt;line-height:1.5}}
.page{{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;padding:18mm 16mm 20mm}}
.eyebrow{{font-family:"Space Mono",monospace;font-size:8pt;letter-spacing:.2em;text-transform:uppercase;color:var(--amber)}}
h1,h2{{font-family:"Hanken Grotesk";font-weight:800;letter-spacing:-.02em;line-height:1.02}}
.pf{{position:absolute;left:16mm;right:16mm;bottom:9mm;font-size:7.5pt;color:var(--soft);border-top:1px solid var(--line);padding-top:3mm}}
/* cover */
.cover{{padding:0;background:var(--navy);color:#fff}}
.cover .c-img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.6}}
.cover .shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,43,53,.2),rgba(12,43,53,.92) 70%)}}
.cover .in{{position:absolute;left:18mm;right:18mm;bottom:24mm}}
.cover img.logo{{width:30mm;margin-bottom:12mm}}
.cover h1{{font-size:46pt;margin:4mm 0 6mm}}
.cover h1 em{{font-family:Fraunces,serif;font-style:italic;font-weight:600;color:var(--gold)}}
.cover p{{font-size:12.5pt;max-width:140mm;color:rgba(255,255,255,.85)}}
.cover .bar{{position:absolute;top:0;left:0;right:0;height:3mm;background:linear-gradient(90deg,var(--amber),var(--gold) 35%,#2f8f5f 65%,#0a6d84)}}
/* about */
.about h2{{font-size:26pt;margin:3mm 0 6mm;max-width:150mm}}
.lead{{font-size:12pt;color:var(--soft);max-width:160mm;margin-bottom:8mm}}
.facts{{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin:6mm 0 10mm}}
.fact{{background:var(--sand);border-radius:4mm;padding:5mm}}
.fact b{{display:block;font-size:20pt;color:var(--navy);line-height:1}}
.fact span{{font-size:8.5pt;color:var(--soft)}}
.team{{display:grid;grid-template-columns:repeat(4,1fr);gap:5mm}}
.member .ini{{width:100%;aspect-ratio:1;border-radius:4mm;background:#eee;display:grid;place-items:center;font-size:28pt;font-weight:700;color:#777}}
.member img{{width:100%;aspect-ratio:1;object-fit:cover;border-radius:4mm}}
.member h3{{font-size:11pt;margin-top:3mm}}
.member p{{font-size:9pt;color:var(--soft)}}
.how{{display:grid;grid-template-columns:repeat(2,1fr);gap:3mm 8mm;margin-top:8mm}}
.how div{{border-top:2px solid var(--amber);padding-top:2.5mm;font-size:9.5pt}}
.how b{{display:block;color:var(--navy)}}
/* tracks */
.track{{padding:0 0 20mm}}
.t-hero{{position:relative;height:62mm;background:var(--navy);margin-bottom:6mm}}
.t-img{{width:100%;height:100%;object-fit:cover;display:block}}
.t-over{{position:absolute;inset:0;padding:10mm 16mm;display:flex;flex-direction:column;justify-content:flex-end;background:linear-gradient(180deg,rgba(12,43,53,0) 20%,rgba(12,43,53,.88));color:#fff}}
.t-over h2{{font-size:28pt;margin:1mm 0 1.5mm}}
.t-over p{{font-size:11pt;color:rgba(255,255,255,.85)}}
.courses{{padding:0 16mm;display:grid;grid-template-columns:1fr 1fr;gap:4.5mm}}
.course{{border:1px solid var(--line);border-radius:4mm;padding:4.5mm 5mm;break-inside:avoid}}
.course.note{{background:var(--sand);border-color:var(--sand)}}
.c-head{{display:flex;justify-content:space-between;align-items:baseline;gap:3mm;margin-bottom:1.5mm}}
.course h3{{font-size:11.5pt;line-height:1.2;color:var(--navy)}}
.pill{{flex:none;font-size:8pt;font-weight:700;background:var(--mint);color:var(--navy);border-radius:10mm;padding:.6mm 2.5mm;white-space:nowrap}}
.course p{{font-size:9pt;color:var(--soft)}}
.course ul{{margin:2mm 0 0;padding-left:4mm;font-size:8.8pt}}
.course li{{margin:.4mm 0}}
.course .who{{margin-top:2mm;font-size:8.3pt;color:var(--navy)}}
/* services + contact */
.svc h2{{font-size:24pt;margin:3mm 0 5mm}}
.svcs{{display:grid;grid-template-columns:1fr 1fr;gap:5mm}}
.svc-card{{border-radius:4mm;overflow:hidden;border:1px solid var(--line)}}
.svc-card img{{width:100%;height:30mm;object-fit:cover;display:block}}
.svc-card div{{padding:3.5mm 4.5mm}}
.svc-card h3{{font-size:11pt;color:var(--navy)}}
.svc-card p{{font-size:8.8pt;color:var(--soft)}}
.contact{{background:var(--navy);color:#fff}}
.contact h2{{font-size:34pt;margin:4mm 0 6mm}}
.contact p{{color:rgba(255,255,255,.85);font-size:12pt;max-width:150mm}}
.cards{{display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:12mm}}
.cards div{{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);border-radius:4mm;padding:6mm}}
.cards b{{display:block;color:var(--gold);font-family:"Space Mono",monospace;font-size:8pt;letter-spacing:.15em;text-transform:uppercase;margin-bottom:2mm}}
.cards span{{font-size:12pt}}
.contact .pf{{color:rgba(255,255,255,.6);border-color:rgba(255,255,255,.2)}}
.credits{{font-size:6.5pt;color:rgba(255,255,255,.55);margin-top:12mm;max-width:178mm}}
</style></head><body>

<section class="page cover">{img("course:style-specialization", "c-img")}<div class="shade"></div><div class="bar"></div>
  <div class="in"><img class="logo" src="{uri("assets/footer-logo.png")}" alt="">
    <span class="eyebrow">Course prospectus · 2026</span>
    <h1>Brew like you <em>mean it.</em></h1>
    <p>{n} live online courses in brewing, business, spirits and the drinks beyond beer, hands-on days in Bengaluru, and services for drinks companies. Taught by people who do the work.</p></div>
</section>

<section class="page about"><span class="eyebrow">About the school</span>
  <h2>India's beer school, grain to glass and beyond.</h2>
  <p class="lead">We teach everything inside and outside the bottle: ingredients, brewing, tasting, branding and the business of beer, and now spirits, AI for breweries and the drinks beyond beer. Live online sessions, guided tastings and hands-on brewery days.</p>
  <div class="facts"><div class="fact"><b>{n}</b><span>Live online courses</span></div><div class="fact"><b>20</b><span>Students per batch, at most</span></div>
    <div class="fact"><b>Sat-Sun</b><span>12:00 to 2:00 PM IST</span></div><div class="fact"><b>Cert.</b><span>Certificate of completion</span></div></div>
  <div class="team">
    <div class="member"><img src="{uri("assets/team3.jpg")}" alt=""><h3>Ankur Napa</h3><p>Master Brewer and course instructor, with hands-on experience at global brewing companies.</p></div>
    <div class="member"><img src="{uri("assets/team5.jpg")}" alt=""><h3>Chatty Girija</h3><p>Beer podcaster and creative strategist, with more than 30 years in advertising.</p></div>
    <div class="member"><img src="{uri("assets/team4.jpg")}" alt=""><h3>Anu Rao</h3><p>Head of Strategy and Operations, with more than 15 years in education and operations.</p></div>
    <div class="member"><div class="ini">RB</div><h3>Rahul Baliyan</h3><p>Brewing science instructor for Delhi and North India. Weihenstephan-trained German-style Brewmaster.</p></div>
  </div>
  <div class="how"><div><b>Live, not recorded</b>Two live sessions every weekend, with recordings afterwards.</div>
    <div><b>Small batches</b>At most 20 students, so every question gets answered.</div>
    <div><b>Weekly assignments</b>Real tasks on your own recipes, data or brand.</div>
    <div><b>Certificate</b>Once every assignment is in and you have attended at least 80% of sessions.</div></div>
  <footer class="pf">Craft Beer School · {SITE}</footer>
</section>

{tracks}

<section class="page svc"><span class="eyebrow">For companies</span>
  <h2>Training, hiring and consulting for the drinks business.</h2>
  <div class="svcs">
    <div class="svc-card">{img("service:training")}<div><h3>Corporate training</h3><p>Beverage domain training for GCC teams in Bengaluru, Pune and Hyderabad: Beverage 101, operations, supply chain, regulation, sensory, data and AI.</p></div></div>
    <div class="svc-card">{img("service:hiring")}<div><h3>Hiring support</h3><p>The right people for every function in a brewery, winery or distillery, screened by people who do the job.</p></div></div>
    <div class="svc-card">{img("service:brand")}<div><h3>Brand and digital marketing</h3><p>Brand strategy, naming, packaging direction, launches and digital marketing that works within India's alcohol advertising rules.</p></div></div>
    <div class="svc-card">{img("service:india")}<div><h3>Market entry into India</h3><p>For beer brands, ingredient, raw material, packaging and equipment companies from abroad: the market, the rules by state, partners and launch.</p></div></div>
    <div class="svc-card">{img("service:digital")}<div><h3>Digital transformation</h3><p>Brew records, stock and batch tracking, dashboards, software choices and AI, with a 90-day plan.</p></div></div>
    <div class="svc-card" style="background:var(--sand);border-color:var(--sand)"><div><h3>Talk to us</h3><p>Every engagement starts with a conversation about how your business runs today. Legal and tax steps are done alongside your own advisers.</p></div></div>
  </div>
  <footer class="pf">Craft Beer School · {SITE}</footer>
</section>

<section class="page contact"><span class="eyebrow">Enrol</span>
  <h2>Pick a course. Save your seat.</h2>
  <p>Enrol online, ask a question on WhatsApp, or tell us about the team you want to train. We reply within 24 hours.</p>
  <div class="cards"><div><b>Website</b><span>{SITE}</span></div><div><b>WhatsApp and phone</b><span>{PHONE}</span></div>
    <div><b>Email</b><span>{EMAIL}</span></div><div><b>Based in</b><span>Bengaluru, teaching learners across India and the world</span></div></div>
  <p class="credits">Fees and dates are correct at the time of printing and may change; the website has the latest. Drink responsibly. Photos: Wikimedia Commons contributors under free licences; full credits at {SITE}/image-credits.html.</p>
  <footer class="pf">Craft Beer School · {SITE}</footer>
</section>
</body></html>"""


def main():
    TMP.write_text(build_html(), encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=15000", f"--print-to-pdf={OUT}", TMP.resolve().as_uri()],
                   check=True, capture_output=True)
    TMP.unlink()
    print("wrote", OUT, OUT.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
