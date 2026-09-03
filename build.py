#!/usr/bin/env python3
"""Static site generator for Craft Beer School.

One shared shell (nav + footer + scripts) stamped around per-page bodies
defined in pages_a.py / pages_b.py. Run `python3 build.py` to regenerate
every .html file in this folder. Edit the shell here once; all pages update.
"""
import datetime
import os
import re
from urllib.parse import quote
import pages_a
import pages_b
import seo

# --- Consistent inline icon set (Lucide, MIT). Use [[name]] in page bodies. ---
ICONS = {
    "flask": '<path d="M14 2v6a2 2 0 0 0 .245.96l5.51 10.08A2 2 0 0 1 18 22H6a2 2 0 0 1-1.755-2.96l5.51-10.08A2 2 0 0 0 10 8V2"/><path d="M6.453 15h11.094"/><path d="M8.5 2h7"/>',
    "cap": '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
    "briefcase": '<rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "beer": '<path d="M17 11h1a3 3 0 0 1 0 6h-1"/><path d="M9 12v6"/><path d="M13 12v6"/><path d="M14 7.5c-1 0-1.44.5-3 .5s-2-.5-3-.5-1.72.5-2.5.5a2.5 2.5 0 0 1 0-5c.78 0 1.57.5 2.5.5S9.44 3 11 3s2 .5 3 .5 1.72-.5 2.5-.5a2.5 2.5 0 0 1 0 5c-.78 0-1.5-.5-2.5-.5Z"/><path d="M5 8v10a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V8"/>',
    "book-open": '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
    "book": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/>',
    "calculator": '<rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><line x1="16" x2="16" y1="14" y2="18"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/>',
    "wind": '<path d="M12.8 19.6A2 2 0 1 0 14 16H2"/><path d="M17.5 8a2.5 2.5 0 1 1 2 4H2"/><path d="M9.8 4.4A2 2 0 1 1 11 8H2"/>',
    "whatsapp": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22z"/>',
    "sliders": '<line x1="21" x2="14" y1="4" y2="4"/><line x1="10" x2="3" y1="4" y2="4"/><line x1="21" x2="12" y1="12" y2="12"/><line x1="8" x2="3" y1="12" y2="12"/><line x1="21" x2="16" y1="20" y2="20"/><line x1="12" x2="3" y1="20" y2="20"/><line x1="14" x2="14" y1="2" y2="6"/><line x1="8" x2="8" y1="10" y2="14"/><line x1="16" x2="16" y1="18" y2="22"/>',
}


def expand_icons(html):
    def sub(m):
        inner = ICONS.get(m.group(1), "")
        return (f'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>')
    return re.sub(r"\[\[([a-z-]+)\]\]", sub, html)

# Paste your Formspree form id here (e.g. "xdkzabcd") to activate all forms.
# Until it is set, forms fall back to a prefilled email so no enquiry is ever lost.
FORMSPREE_ID = os.environ.get("FORMSPREE_ID", "YOUR_FORM_ID")

# Single source of truth for every contact CTA on the site.
ENQUIRY_EMAIL = "chatty@cheerschattyventures.com"
WHATSAPP_NUMBER = "919820925347"      # digits only, country code first
WHATSAPP_TEXT = "Hi Craft Beer School, I'd like to know more about your courses."
ENROLL_HREF = "contact.html#enroll"   # lands on the form, not the top of the page


def whatsapp_href(text=WHATSAPP_TEXT):
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(text)}"


def enroll_href(course=None):
    """Enrol link that carries the chosen course into the contact form."""
    if not course:
        return ENROLL_HREF
    return f"contact.html?course={quote(course)}#enroll"

NAV_ITEMS = [
    ("Home", "index.html", "home"),
    ("About", "about.html", "about"),
    ("Courses", "courses.html", "courses"),
    ("Resources", "resources.html", "resources"),
    ("Blog", "blog.html", "blog"),
    ("Careers", "careers.html", "careers"),
    ("Contact", "contact.html", "contact"),
]

ANNOUNCE = ('<div class="announce">Now enrolling, the ₹999 intro session is open. '
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
    <a href="index.html" class="brand" aria-label="Craft Beer School home"><img src="assets/logo.png" alt="Craft Beer School" class="brand-logo" width="118" height="146" /></a>
    <div class="navlinks" id="navlinks">
      {links}
      <a href="{ENROLL_HREF}" class="nav-cta" data-cta="nav-enroll">Enroll</a>
    </div>
    <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="navlinks" onclick="const n=document.getElementById('navlinks');const o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)">☰</button>
  </nav>
</header>
<div class="mobile-cta">
  <a class="btn btn-amber" href="{ENROLL_HREF}" data-cta="mobile-enroll">Enroll now</a>
  <a class="btn btn-wa" href="{whatsapp_href()}" target="_blank" rel="noopener" data-cta="mobile-whatsapp">[[whatsapp]] WhatsApp</a>
</div>"""


FOOTER = """
<footer class="site">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <a href="index.html" aria-label="Craft Beer School home"><img src="assets/footer-logo.png" alt="Craft Beer School" class="foot-logo" width="113" height="126" /></a>
      <p>India's trusted online and in-person beer school. Grain to glass and beyond, brewing, tasting, branding and the business of beer.</p>
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
      <li><a href="__ENROLL__" data-cta="footer-enroll">Enroll</a></li>
    </ul></div>
    <div><h4>Contact</h4><ul>
      <li><a href="__WA__" target="_blank" rel="noopener" data-cta="footer-whatsapp">WhatsApp us</a></li>
      <li><a href="tel:+919820925347">+91 98209 25347</a></li>
      <li><a href="tel:+919082256507">+91 90822 56507</a></li>
      <li><a href="mailto:__EMAIL__" data-cta="footer-email">__EMAIL__</a></li>
      <li><a href="privacy.html">Privacy</a> · <a href="refund.html">Refunds</a></li>
    </ul></div>
  </div>
  <div class="wrap foot-bottom">
    <span>© 2026 Craft Beer School. All rights reserved.</span>
    <span>Drink knowledge responsibly.</span>
  </div>
</footer>"""


SCRIPTS = """
<script>
document.documentElement.classList.add('js');
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

const FORMSPREE_ID="__FID__";
const ENQUIRY_EMAIL="__EMAIL__";

// Pre-select the course when arriving from a course card: contact.html?course=...
const wanted=new URLSearchParams(location.search).get('course');
if(wanted){
  const sel=document.querySelector('select[name=course]');
  if(sel){
    const hit=[...sel.options].find(o=>o.value===wanted||o.textContent.trim()===wanted);
    if(hit){sel.value=hit.value||hit.textContent;sel.dispatchEvent(new Event('change'));}
  }
}

// Every CTA is measurable the moment an analytics tag is added. No-op without one.
document.addEventListener('click',e=>{
  const a=e.target.closest('[data-cta]');
  if(a)(window.dataLayer=window.dataLayer||[]).push({event:'cta_click',cta:a.dataset.cta,href:a.getAttribute('href')||''});
});

document.querySelectorAll('form[data-formspree]').forEach(form=>{
  const msg=form.querySelector('.form-msg');
  const btn=form.querySelector('button[type=submit]');
  function show(t,ok){if(!msg)return;msg.textContent=t;msg.style.color=ok?'#2f7a46':'#c1701a';msg.style.display='block';}
  // No endpoint configured yet: hand the enquiry to the user's mail app rather
  // than dead-ending them. Losing a lead beats no lead.
  function mailtoFallback(){
    const d=new FormData(form);
    const subject=d.get('_subject')||'Craft Beer School enquiry';
    const body=[...d.entries()]
      .filter(([k,v])=>!k.startsWith('_')&&k!=='_gotcha'&&String(v).trim())
      .map(([k,v])=>k.replace(/^./,c=>c.toUpperCase())+': '+v).join('\\n');
    location.href='mailto:'+ENQUIRY_EMAIL+'?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
    show("Opening your email app. If nothing happens, write to "+ENQUIRY_EMAIL+" or tap WhatsApp above.",true);
  }
  form.addEventListener('submit',async e=>{
    e.preventDefault();
    if(!form.reportValidity())return;
    if(FORMSPREE_ID==="YOUR_FORM_ID"){mailtoFallback();return;}
    const orig=btn.textContent;btn.disabled=true;btn.textContent="Sending…";
    try{
      const r=await fetch("https://formspree.io/f/"+FORMSPREE_ID,{method:'POST',body:new FormData(form),headers:{Accept:'application/json'}});
      if(r.ok){form.reset();show("Cheers! We'll be in touch within 24 hours.",true);}
      else{const d=await r.json().catch(()=>({}));show((d.errors?d.errors.map(x=>x.message).join(', '):'Something went wrong.')+" Email "+ENQUIRY_EMAIL+".",false);}
    }catch(_){mailtoFallback();}
    finally{btn.disabled=false;btn.textContent=orig;}
  });
});
</script>"""


def fill_ctas(html):
    """Resolve the shared CTA placeholders used in FOOTER and SCRIPTS."""
    return (html.replace("__ENROLL__", ENROLL_HREF)
                .replace("__WA__", whatsapp_href())
                .replace("__EMAIL__", ENQUIRY_EMAIL)
                .replace("__FID__", FORMSPREE_ID))


def page(slug, title, desc, active, body):
    return expand_icons(fill_ctas(f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
{seo.head_meta(slug, title, desc)}
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;1,9..144,500;1,9..144,600&family=Hanken+Grotesk:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="styles.css" />
{seo.jsonld(slug, title, desc)}
</head>
<body>
{nav(active)}
<main>
{body}
</main>
{FOOTER}
{SCRIPTS}
</body>
</html>"""))


PAGES = {
    "index.html":     ("Craft Beer School | Brewing Courses in India, Grain to Glass",
                        "India's trusted online and in-person beer school. Learn brewing, tasting, branding and the business of beer, grain to glass. WSET & Cicerone prep.",
                        "home", pages_a.HOME),
    "about.html":     ("About Us | Craft Beer School",
                        "Better beer education brews better beer. Meet Craft Beer School, India's grain-to-glass beer school, our mentors, mission and method.",
                        "about", pages_a.ABOUT),
    "courses.html":   ("Beer Brewing Courses in India | Craft Beer School",
                        "Six online courses from basics to business, plus hands-on in-person workshops. Brewing, science, business, styles, branding and sensory.",
                        "courses", pages_a.COURSES),
    "resources.html": ("Free Beer Education Resources | Craft Beer School",
                        "Free beer education: Beer 101, styles primer, a brewing glossary, calculators and tasting tools to sharpen your palate and your process.",
                        "resources", pages_a.RESOURCES),
    "blog.html":      ("Blog and Podcasts | Craft Beer School",
                        "Insights from the brewing world, quality, marketing, tasting and the business of beer, plus our podcast conversations with industry voices.",
                        "blog", pages_a.BLOG),
    "careers.html":   ("Careers and Mentors | Craft Beer School",
                        "Become a CBS mentor or join the team. Help India learn beer, grain to glass. Open roles and the mentor application.",
                        "careers", pages_b.CAREERS),
    "contact.html":   ("Contact and Enrol | Craft Beer School",
                        "Enrol, ask a question, or book a tasting. Reach Craft Beer School by phone, email or the form, we reply within 24 hours.",
                        "contact", pages_b.CONTACT),
    "faq.html":       ("Frequently Asked Questions | Craft Beer School",
                        "Answers on courses, format, certification, payment, refunds and getting started at Craft Beer School.",
                        "faq", pages_b.FAQ),
    "privacy.html":   ("Privacy Policy | Craft Beer School",
                        "How Craft Beer School collects, uses and protects your information.",
                        "", pages_b.PRIVACY),
    "refund.html":    ("Refund and Cancellation Policy | Craft Beer School",
                        "Craft Beer School's refund and cancellation policy for online and in-person courses.",
                        "", pages_b.REFUND),
}


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", path)


def main():
    for slug, (title, desc, active, body) in PAGES.items():
        write(slug, page(slug, title, desc, active, body))

    today = datetime.date.today().isoformat()
    write("sitemap.xml", seo.sitemap_xml(list(PAGES), today))
    write("robots.txt", seo.robots_txt())
    write("llms.txt", seo.llms_txt())
    write("site.webmanifest", seo.webmanifest())
    # Custom domain for GitHub Pages. Without this file every deploy reverts
    # the repo back to the github.io host.
    write("CNAME", seo.SITE_URL.split("//")[1] + "\n")
    # Pages runs Jekyll by default, which ignores files starting with _ and
    # can rewrite output. This site is already built HTML.
    write(".nojekyll", "")


if __name__ == "__main__":
    main()
