#!/usr/bin/env python3
"""Corporate services brochure: assets/craft-beer-school-corporate-services.pdf

Same look as the course prospectus (make_prospectus.py), content taken from
companies.py so the brochure and the Corporate Services page never disagree.
Run after changing either:  python3 make_corporate.py
"""
import re
import subprocess

import companies
import make_prospectus as mp

OUT = mp.HERE / "assets/craft-beer-school-corporate-services.pdf"
TMP = mp.HERE / ".corporate.html"


def section(sid):
    """(eyebrow, h2, paragraphs, list items) from a Corporate Services section."""
    s = companies.BODY[companies.BODY.index(f'id="{sid}"'):]
    s = s[:s.index("</section>")]
    eyebrow = re.search(r'<span class="eyebrow">(.*?)</span>', s).group(1)
    h2 = re.search(r"<h2[^>]*>(.*?)</h2>", s).group(1)
    intro = s[:s.index("<ul")] if "<ul" in s else s
    paras = re.findall(r"<p>(.*?)</p>", intro, re.S)
    paras = [re.sub(r'<a [^>]*>(.*?)</a>', r"\1", p) for p in paras]
    return eyebrow, h2, paras, re.findall(r"<li>(.*?)</li>", s)


def lis(items):
    return "<ul class='tick'>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def service_page(sid, slot, extra=""):
    eyebrow, h2, paras, items = section(sid)
    body = "".join(f"<p>{p}</p>" for p in paras)
    return f"""<section class="page track">
  <div class="t-hero">{mp.img(slot, "t-img")}<div class="t-over"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2></div></div>
  <div class="svc-body"><div class="prose">{body}</div><div><h4>What we do</h4>{lis(items[:9])}</div></div>
  {extra}
  <footer class="pf">Craft Beer School · Corporate services · {mp.SITE}</footer>
</section>"""


def training_page():
    eyebrow, h2, paras, items = section("training")
    who, formats = companies.TRAINING_FOR, items[len(companies.TRAINING_FOR):]
    mods = "".join(f"<div class='mod'><h3>{t}</h3><p>{d}</p></div>" for _, t, d in companies.PROGRAMMES)
    return f"""<section class="page track">
  <div class="t-hero">{mp.img("service:training", "t-img")}<div class="t-over"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2></div></div>
  <div class="svc-body"><div class="prose">{"".join(f"<p>{p}</p>" for p in paras)}</div>
    <div><h4>Who it is for</h4>{lis(who)}<h4 style="margin-top:4mm">Formats</h4>{lis(formats)}</div></div>
  <div class="mods">{mods}</div>
  <footer class="pf">Craft Beer School · Corporate services · {mp.SITE}</footer>
</section>"""


def hiring_page():
    eyebrow, h2, paras, _ = section("hiring")
    steps = "".join(f"<div class='mod'><h3>{n:02d}. {t}</h3><p>{d}</p></div>" for n, (t, d) in enumerate(companies.HIRING_STEPS, 1))
    return f"""<section class="page track">
  <div class="t-hero plain"><div class="t-over"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2></div></div>
  <div class="svc-body"><div class="prose">{"".join(f"<p>{p}</p>" for p in paras)}</div><div><h4>Functions we hire for</h4>{lis(companies.FUNCTIONS)}</div></div>
  <h4 style="padding:0 16mm;margin:2mm 0 3mm">How it works</h4><div class="mods">{steps}</div>
  <footer class="pf">Craft Beer School · Corporate services · {mp.SITE}</footer>
</section>"""


EXTRA_CSS = """
.t-hero.plain{background:linear-gradient(135deg,var(--navy),#0a6d84)}
.t-over h2{font-size:22pt;max-width:170mm}
.svc-body{padding:0 16mm;display:grid;grid-template-columns:1.25fr 1fr;gap:8mm}
.prose p{font-size:10pt;color:var(--soft);margin-bottom:3mm}
h4{font-family:"Space Mono",monospace;font-size:7.5pt;letter-spacing:.15em;text-transform:uppercase;color:var(--amber);margin-bottom:2mm}
ul.tick{list-style:none;padding:0;font-size:9.3pt}
ul.tick li{padding:1.3mm 0 1.3mm 5mm;border-top:1px solid var(--line);position:relative}
ul.tick li::before{content:"";position:absolute;left:0;top:2.6mm;width:2mm;height:2mm;border-radius:50%;background:var(--mint)}
.mods{padding:0 16mm;margin-top:6mm;display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.mod{border:1px solid var(--line);border-radius:3mm;padding:3.5mm 4mm}
.mod h3{font-size:10.5pt;color:var(--navy);margin-bottom:1mm}
.mod p{font-size:8.6pt;color:var(--soft)}
.ov{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:6mm}
.ov div{background:var(--sand);border-radius:3mm;padding:4mm 5mm}
.ov b{display:block;color:var(--navy);font-size:11pt;margin-bottom:1mm}
.ov span{font-size:9pt;color:var(--soft)}
"""


def build_html():
    base = mp.build_html()
    head, css = base[:base.index("<style>")], base[base.index("<style>"):base.index("</style>")]
    about = base[base.index('<section class="page about">'):]
    about = about[:about.index("</section>") + len("</section>")]
    # Reuse the team block, swap the course facts for the five services.
    team = about[about.index('<div class="team">'):about.index('<div class="how">')]
    overview = "".join(f"<div><b>{t}</b><span>{d}</span></div>" for _, t, d, _ in companies.SERVICES)
    contact = base[base.index('<section class="page contact">'):]
    contact = contact[:contact.index("</section>") + len("</section>")]
    contact = (contact.replace("Pick a course. Save your seat.", "Start with a conversation.")
               .replace("Enrol online, ask a question on WhatsApp, or tell us about the team you want to train.",
                        "Tell us about your team, your brand or the market you want to enter.")
               .replace("Fees and dates are correct at the time of printing and may change; the website has the latest. ", ""))
    return f"""{head}{css}{EXTRA_CSS}</style></head><body>
<section class="page cover">{mp.img("course:craft-distilling", "c-img")}<div class="shade"></div><div class="bar"></div>
  <div class="in"><img class="logo" src="{mp.uri("assets/footer-logo.png")}" alt="">
    <span class="eyebrow">Corporate services · 2026</span>
    <h1>Training, hiring and <em>consulting</em> for the drinks business.</h1>
    <p>For breweries, wineries and distilleries, for beverage capability centres in Bengaluru, Pune and Hyderabad, and for companies bringing beer, ingredients or packaging to India.</p></div>
</section>
<section class="page about"><span class="eyebrow">Who we are</span>
  <h2>A team that has worked inside the industry.</h2>
  <p class="lead">Craft Beer School is India's beer school. Alongside our courses we work with companies: we consult for breweries, train their teams, help them hire and advise on brand, market entry and digital transformation.</p>
  {team}
  <span class="eyebrow" style="display:block;margin-top:8mm">Five services</span>
  <div class="ov">{overview}</div>
  <footer class="pf">Craft Beer School · Corporate services · {mp.SITE}</footer>
</section>
{training_page()}
{hiring_page()}
{service_page("brand", "service:brand")}
{service_page("india", "service:india")}
{service_page("digital", "track:brewing")}
{service_page("consultancy", "course:advanced-brewing-science")}
{contact}
</body></html>"""


def main():
    TMP.write_text(build_html(), encoding="utf-8")
    subprocess.run([mp.CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=15000", f"--print-to-pdf={OUT}", TMP.resolve().as_uri()],
                   check=True, capture_output=True)
    TMP.unlink()
    print("wrote", OUT, OUT.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
