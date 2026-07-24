#!/usr/bin/env python3
"""Static site generator for Craft Beer School.

One shared shell (nav + footer + scripts) stamped around per-page bodies
defined in pages_a.py / pages_b.py. Run `python3 build.py` to regenerate
every .html file in this folder. Edit the shell here once; all pages update.
"""
import pages_a
import pages_b

# Paste your Formspree form id here (e.g. "xdkzabcd") to activate all forms.
FORMSPREE_ID = "YOUR_FORM_ID"

NAV_ITEMS = [
    ("Home", "index.html", "home"),
    ("About", "about.html", "about"),
    ("Courses", "courses.html", "courses"),
    ("Resources", "resources.html", "resources"),
    ("Blog", "blog.html", "blog"),
    ("Careers", "careers.html", "careers"),
    ("Contact", "contact.html", "contact"),
]

ANNOUNCE = ('<div class="announce">Now enrolling — the ₹999 intro session is open. '
            '<a href="courses.html">See all courses →</a></div>')


def nav(active):
    def item(label, href, key):
        cls = ' class="active"' if key == active else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    links = "".join(item(*i) for i in NAV_ITEMS)
    return f"""{ANNOUNCE}
<div class="rainbow"></div>
<header>
  <nav class="wrap">
    <a href="index.html" class="brand"><span class="mark">🍺</span>Craft Beer School</a>
    <div class="navlinks" id="navlinks">
      {links}
      <a href="contact.html" class="nav-cta">Enroll</a>
    </div>
    <button class="burger" aria-label="Menu" onclick="document.getElementById('navlinks').classList.toggle('open')">☰</button>
  </nav>
</header>"""


FOOTER = """
<footer class="site">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <a href="index.html" class="brand" style="color:#fff"><span class="mark">🍺</span>Craft Beer School</a>
      <p>India's trusted online and in-person beer school. Grain to glass and beyond — brewing, tasting, branding and the business of beer.</p>
    </div>
    <div><h4>Learn</h4><ul>
      <li><a href="courses.html">Courses</a></li>
      <li><a href="resources.html">Resources</a></li>
      <li><a href="blog.html">Blog &amp; Podcasts</a></li>
      <li><a href="faq.html">FAQ</a></li>
    </ul></div>
    <div><h4>School</h4><ul>
      <li><a href="about.html">About us</a></li>
      <li><a href="careers.html">Careers &amp; Mentors</a></li>
      <li><a href="contact.html">Contact</a></li>
      <li><a href="contact.html">Enroll</a></li>
    </ul></div>
    <div><h4>Contact</h4><ul>
      <li><a href="tel:+919820925347">+91 98209 25347</a></li>
      <li><a href="tel:+919082256507">+91 90822 56507</a></li>
      <li><a href="mailto:chatty@cheerschattyventures.com">chatty@cheers…</a></li>
      <li><a href="privacy.html">Privacy</a> · <a href="refund.html">Refunds</a></li>
    </ul></div>
  </div>
  <div class="wrap foot-bottom">
    <span>© 2026 Craft Beer School. All rights reserved.</span>
    <span>Drink knowledge responsibly. 🍻</span>
  </div>
</footer>"""


SCRIPTS = """
<script>
document.documentElement.classList.add('js');
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

const FORMSPREE_ID="__FID__";
document.querySelectorAll('form[data-formspree]').forEach(form=>{
  const msg=form.querySelector('.form-msg');
  const btn=form.querySelector('button[type=submit]');
  function show(t,ok){if(!msg)return;msg.textContent=t;msg.style.color=ok?'#2f7a46':'#c1701a';msg.style.display='block';}
  form.addEventListener('submit',async e=>{
    e.preventDefault();
    if(FORMSPREE_ID==="YOUR_FORM_ID"){show("Form not configured yet — add your Formspree ID in build.py.",false);return;}
    const orig=btn.textContent;btn.disabled=true;btn.textContent="Sending…";
    try{
      const r=await fetch("https://formspree.io/f/"+FORMSPREE_ID,{method:'POST',body:new FormData(form),headers:{Accept:'application/json'}});
      if(r.ok){form.reset();show("Cheers! We'll be in touch within 24 hours. 🍻",true);}
      else{const d=await r.json().catch(()=>({}));show((d.errors?d.errors.map(x=>x.message).join(', '):'Something went wrong.')+" Email chatty@cheerschattyventures.com.",false);}
    }catch(_){show("Network error — please email chatty@cheerschattyventures.com.",false);}
    finally{btn.disabled=false;btn.textContent=orig;}
  });
});
</script>"""


def page(title, desc, active, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;1,9..144,500;1,9..144,600&family=Poppins:wght@600;700;800&family=Hanken+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="styles.css" />
</head>
<body>
{nav(active)}
<main>
{body}
</main>
{FOOTER}
{SCRIPTS.replace("__FID__", FORMSPREE_ID)}
</body>
</html>"""


PAGES = {
    "index.html":     ("Craft Beer School — Grain to Glass. India's beer school.",
                        "India's trusted online and in-person beer school. Learn brewing, tasting, branding and the business of beer — grain to glass. WSET & Cicerone prep.",
                        "home", pages_a.HOME),
    "about.html":     ("About — Craft Beer School",
                        "Better beer education brews better beer. Meet Craft Beer School — India's grain-to-glass beer school, our mentors, mission and method.",
                        "about", pages_a.ABOUT),
    "courses.html":   ("Courses — Craft Beer School",
                        "Six online courses from basics to business, plus hands-on in-person workshops. Brewing, science, business, styles, branding and sensory.",
                        "courses", pages_a.COURSES),
    "resources.html": ("Resources — Craft Beer School",
                        "Free beer education: Beer 101, styles primer, a brewing glossary, calculators and tasting tools to sharpen your palate and your process.",
                        "resources", pages_a.RESOURCES),
    "blog.html":      ("Blog & Podcasts — Craft Beer School",
                        "Insights from the brewing world — quality, marketing, tasting and the business of beer, plus our podcast conversations with industry voices.",
                        "blog", pages_a.BLOG),
    "careers.html":   ("Careers & Mentors — Craft Beer School",
                        "Become a CBS mentor or join the team. Help India learn beer, grain to glass. Open roles and the mentor application.",
                        "careers", pages_b.CAREERS),
    "contact.html":   ("Contact & Enroll — Craft Beer School",
                        "Enrol, ask a question, or book a tasting. Reach Craft Beer School by phone, email or the form — we reply within 24 hours.",
                        "contact", pages_b.CONTACT),
    "faq.html":       ("FAQ — Craft Beer School",
                        "Answers on courses, format, certification, payment, refunds and getting started at Craft Beer School.",
                        "faq", pages_b.FAQ),
    "privacy.html":   ("Privacy Policy — Craft Beer School",
                        "How Craft Beer School collects, uses and protects your information.",
                        "", pages_b.PRIVACY),
    "refund.html":    ("Refund & Cancellation — Craft Beer School",
                        "Craft Beer School's refund and cancellation policy for online and in-person courses.",
                        "", pages_b.REFUND),
}


def main():
    for slug, (title, desc, active, body) in PAGES.items():
        with open(slug, "w", encoding="utf-8") as f:
            f.write(page(title, desc, active, body))
        print("wrote", slug)


if __name__ == "__main__":
    main()
