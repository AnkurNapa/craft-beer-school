#!/usr/bin/env python3
"""Static site generator for Craft Beer School.

One shared shell (nav + footer + scripts) stamped around per-page bodies
defined in pages_a.py / pages_b.py. Run `python3 build.py` to regenerate
every .html file in this folder. Edit the shell here once; all pages update.
"""
import datetime
import html
import os
import pathlib
import re
from urllib.parse import quote
import article_render
import course_pages
import articles_all
import pages_a
import pages_b
import seo
import style_render
import companies
import mentors
import photos
import brochure_pages
import discover
import podcast

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
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "martini": '<path d="M8 22h8"/><path d="M12 11v11"/><path d="m19 3-7 8-7-8Z"/>',
    "glass-water": '<path d="M5.116 4.104A1 1 0 0 1 6.11 3h11.78a1 1 0 0 1 .994 1.105L17.19 20.21A2 2 0 0 1 15.2 22H8.8a2 2 0 0 1-2-1.79z"/><path d="M6 12a5 5 0 0 1 6 0 5 5 0 0 0 6 0"/>',
    "map-pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "download": '<path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-left": '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
    "menu": '<line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/>',
    "whatsapp": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22z"/>',
    "sliders": '<line x1="21" x2="14" y1="4" y2="4"/><line x1="10" x2="3" y1="4" y2="4"/><line x1="21" x2="12" y1="12" y2="12"/><line x1="8" x2="3" y1="12" y2="12"/><line x1="21" x2="16" y1="20" y2="20"/><line x1="12" x2="3" y1="20" y2="20"/><line x1="14" x2="14" y1="2" y2="6"/><line x1="8" x2="8" y1="10" y2="14"/><line x1="16" x2="16" y1="18" y2="22"/>',
}


def expand_icons(html):
    def sub(m):
        inner = ICONS.get(m.group(1), "")
        return (f'<svg class="ico ico-{m.group(1)}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>')
    return re.sub(r"\[\[([a-z-]+)\]\]", sub, html)

# Paste your Formspree form id here (e.g. "xdkzabcd") to activate all forms.
# Until it is set, forms fall back to a prefilled email so no enquiry is ever lost.
FORMSPREE_ID = os.environ.get("FORMSPREE_ID", "YOUR_FORM_ID")

# Supabase stores course applications so they can be triaged in admin.html.
# The anon key is a public, publishable key and is meant to ship in the page:
# row level security (supabase/schema.sql) lets it INSERT and nothing else.
# Never put the service_role key here, that one bypasses RLS entirely.
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "")

# Google Analytics 4 measurement ID (GA > Admin > Data streams, "G-..."). Empty
# means no tag is emitted at all, so a missing ID never ships a broken loader.
GA_ID = os.environ.get("GA_ID", "G-1ZHW47YJDC")  # shared with the Beverage-AI Radar property


def ga_tag():
    if not GA_ID:
        return ""
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
            f"gtag('js',new Date());gtag('config','{GA_ID}');</script>")

# Single source of truth for every contact CTA on the site.
ENQUIRY_EMAIL = "chatty@cheerschattyventures.com"
WHATSAPP_NUMBER = "919820925347"      # digits only, country code first
WHATSAPP_TEXT = "Hi Craft Beer School, I'd like to know more about your courses."
ENROLL_HREF = "contact.html#enroll"   # lands on the form, not the top of the page


def whatsapp_href(text=WHATSAPP_TEXT):
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(text)}"


def whatsapp_text(slug, title):
    """Opening message that tells us which page the person tapped WhatsApp on."""
    name = re.sub(r"\s*\|\s*Craft Beer School\s*$", "", html.unescape(title)).strip()
    url = seo.url_for(slug)
    if slug == "index.html":
        return f"{WHATSAPP_TEXT} (from {url})"
    if slug in COURSE_SLUGS:
        return f"Hi Craft Beer School, I'd like to know more about the {name.replace(' Course', '')} course. ({url})"
    if slug.startswith("style-") and slug != "style-library.html":
        return f"Hi Craft Beer School, I was reading about {name.split(':')[0]} in your Style Library and have a question. ({url})"
    if slug[:-5] in articles_all.SEGMENT or slug[:-5] in {a['slug'] for a in articles_all.ARTICLES}:
        return f"Hi Craft Beer School, I was reading \"{name}\" and have a question. ({url})"
    return f"Hi Craft Beer School, I was on your {name} page and have a question. ({url})"


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
    ("Styles", "style-library.html", "styles"),
    ("Blog", "blog.html", "blog"),
    ("Podcast", "podcast.html", "podcast"),
    ("Careers", "careers.html", "careers"),
    ("Contact", "contact.html", "contact"),
]

ANNOUNCE = ('<div class="announce">Now enrolling: the ₹999 intro session is open. '
            '<a href="courses.html">See all courses [[arrow-right]]</a>'
            '<span class="announce-sep">·</span><a href="prospectus.html" data-cta="announce-prospectus">Read the prospectus</a></div>')


def course_ticker():
    """Running strip of every course under the nav, like the Beverage-AI Radar's
    events line. The sequence is emitted twice and slides exactly -50%, so the
    loop is seamless; the copy is aria-hidden and out of the tab order."""
    def item(c, copy):
        tab = ' tabindex="-1"' if copy else ""
        badge = ("Free" if c["amount"] == "0" else "New" if c["tag"].startswith("New") else "")
        badge_html = f'<span class="tick-badge">{badge}</span>' if badge else ""
        return (f'<span class="tick-item"><a href="{pages_a.course_href(c["name"])}"{tab}>{c["name"]}</a>'
                f'<span class="tick-meta">{c["dur"]} · {c["price"]}</span>{badge_html}</span>')
    seq = lambda copy: "".join(item(c, copy) for c in pages_a.COURSE_DATA)
    return f"""<aside class="ticker" aria-label="Our courses">
  <div class="wrap ticker-inner">
    <a class="ticker-label" href="courses.html">Courses</a>
    <div class="ticker-viewport"><p class="ticker-track"><span class="ticker-seq">{seq(False)}</span><span class="ticker-seq" aria-hidden="true">{seq(True)}</span></p></div>
  </div>
</aside>"""


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
      {discover.SEARCH_FORM}
      <a href="{ENROLL_HREF}" class="nav-cta" data-cta="nav-enroll">Enrol</a>
    </div>
    <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="navlinks" onclick="const n=document.getElementById('navlinks');const o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)">[[menu]]</button>
  </nav>
</header>
{course_ticker()}
<div class="mobile-cta">
  <a class="btn btn-amber" href="{ENROLL_HREF}" data-cta="mobile-enroll">Enrol now</a>
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
      <li><a href="style-library.html">Style Library</a></li>
      <li><a href="prospectus.html" data-cta="footer-prospectus">Prospectus</a></li>
      <li><a href="blog.html">Blog</a></li>
      <li><a href="podcast.html">Podcast</a></li>
      <li><a href="faq.html">FAQ</a></li>
    </ul></div>
    <div><h4>School</h4><ul>
      <li><a href="about.html">About us</a></li>
      <li><a href="for-companies.html">Corporate services</a></li>
      <li><a href="corporate-brochure.html" data-cta="footer-brochure">Corporate brochure</a></li>
      <li><a href="careers.html">Careers and mentors</a></li>
      <li><a href="contact.html">Contact</a></li>
      <li><a href="__ENROLL__" data-cta="footer-enroll">Enrol</a></li>
    </ul></div>
    <div><h4>Contact</h4><ul>
      <li><a href="__WA__" target="_blank" rel="noopener" data-cta="footer-whatsapp">WhatsApp us</a></li>
      <li><a href="tel:+919820925347">+91 98209 25347</a></li>
      <li><a href="tel:+919082256507">+91 90822 56507</a></li>
      <li><a href="mailto:__EMAIL__" data-cta="footer-email">__EMAIL__</a></li>
      <li><a href="privacy.html">Privacy</a> · <a href="refund.html">Refunds</a> · <a href="image-credits.html">Image credits</a></li>
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
const SUPABASE_URL="__SBURL__";
const SUPABASE_ANON_KEY="__SBKEY__";

// Course ticker: about 60px a second whatever the number of courses.
(()=>{const t=document.querySelector('.ticker-track');if(!t)return;
requestAnimationFrame(()=>{const w=t.querySelector('.ticker-seq').getBoundingClientRect().width;
t.style.setProperty('--ticker-duration',Math.min(160,Math.max(25,Math.round(w/60)))+'s');});})();

// Remember the last page read before the enquiry form, so a lead arrives
// with "came from the Irish Dry Stout page", not just "contact.html".
const here=location.pathname.replace(/^\//,'')||'index.html';
let cameFrom=here;
try{
  if(here!=='contact.html')sessionStorage.setItem('cbs-from',here);
  else cameFrom=sessionStorage.getItem('cbs-from')||(document.referrer.startsWith(location.origin)?new URL(document.referrer).pathname.replace(/^\//,''):'')||here;
}catch(_){}
document.querySelectorAll('form[data-formspree]').forEach(f=>{
  const h=document.createElement('input');h.type='hidden';h.name='came_from';h.value=location.origin+'/'+cameFrom;f.appendChild(h);
});

// Pre-select the course when arriving from a course card: contact.html?course=...
const wanted=new URLSearchParams(location.search).get('course');
if(wanted){
  const sel=document.querySelector('select[name=course]');
  if(sel){
    const hit=[...sel.options].find(o=>o.value===wanted||o.textContent.trim()===wanted);
    if(hit){sel.value=hit.value||hit.textContent;sel.dispatchEvent(new Event('change'));}
  }
}

// Every CTA becomes a GA4 event. gtag.js ignores plain objects pushed to
// dataLayer, so it has to go through gtag(). No-op when GA is not configured.
document.addEventListener('click',e=>{
  const a=e.target.closest('[data-cta]');
  if(a&&window.gtag)gtag('event','cta_click',{cta:a.dataset.cta,link_url:a.getAttribute('href')||''});
});

// "WhatsApp instead" on a form carries whatever the person already typed,
// so nobody has to repeat their name, course or question in the chat.
document.querySelectorAll('form .btn-wa').forEach(a=>{
  const base=a.getAttribute('href');
  a.addEventListener('click',()=>{
    const d=new FormData(a.closest('form'));
    const lines=[['name','Name'],['course','Course'],['city','City'],['phone','Phone'],['email','Email'],['message','Message'],['came_from','Came from']]
      .map(([k,l])=>[l,String(d.get(k)||'').trim()]).filter(([,v])=>v).map(([l,v])=>l+': '+v);
    if(!lines.length){a.href=base;return}
    const [url,q]=base.split('?text=');
    a.href=url+'?text='+encodeURIComponent(decodeURIComponent(q||'')+'\\n\\n'+lines.join('\\n'));
  });
});

document.querySelectorAll('form[data-formspree]').forEach(form=>{
  const msg=form.querySelector('.form-msg');
  const btn=form.querySelector('button[type=submit]');
  // Successful submissions are the conversion to mark as a key event in GA4.
  function lead(){if(window.gtag)gtag('event','generate_lead',{course:new FormData(form).get('course')||'',form_page:location.pathname});}
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
    if(form.querySelector('[name=_gotcha]')?.value){show("Thanks!",true);return;}  // bot
    const orig=btn.textContent;btn.disabled=true;btn.textContent="Sending…";
    try{
      if(SUPABASE_URL&&SUPABASE_ANON_KEY&&form.dataset.store!=="off"){
        const d=new FormData(form);
        const row={
          name:d.get('name'), phone:d.get('phone'), email:d.get('email'),
          course:d.get('course')||null, city:d.get('city')||null,
          promo:d.get('promo')||null, message:d.get('message')||null,
          source_page:(cameFrom===here?here:cameFrom+' > '+here).slice(0,200)
        };
        const r=await fetch(SUPABASE_URL+"/rest/v1/applications",{
          method:'POST',
          headers:{'apikey':SUPABASE_ANON_KEY,'Authorization':'Bearer '+SUPABASE_ANON_KEY,
                   'Content-Type':'application/json','Prefer':'return=minimal'},
          body:JSON.stringify(row)});
        if(r.ok){lead();form.reset();show("Cheers! Your application is in. We'll be in touch within 24 hours.",true);return;}
        console.warn('application store failed',r.status,await r.text().catch(()=>''));
      }
      if(FORMSPREE_ID!=="YOUR_FORM_ID"){
        const r=await fetch("https://formspree.io/f/"+FORMSPREE_ID,{method:'POST',body:new FormData(form),headers:{Accept:'application/json'}});
        if(r.ok){lead();form.reset();show("Cheers! We'll be in touch within 24 hours.",true);return;}
      }
      mailtoFallback();
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
                .replace("__FID__", FORMSPREE_ID)
                .replace("__SBURL__", SUPABASE_URL)
                .replace("__SBKEY__", SUPABASE_ANON_KEY))


# Changes whenever styles.css changes, so browsers never pair new HTML with a cached old stylesheet.
CSS_VERSION = __import__("hashlib").sha1(pathlib.Path(__file__).with_name("styles.css").read_bytes()).hexdigest()[:10]


def page(slug, title, desc, active, body):
    return _with_page_whatsapp(slug, title, expand_icons(fill_ctas(f"""<!DOCTYPE html>
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
<link rel="stylesheet" href="styles.css?v={CSS_VERSION}" />
{seo.jsonld(slug, title, desc)}
{ga_tag()}
</head>
<body>
{nav(active)}
<main>
{body}
</main>
{FOOTER}
{SCRIPTS}
</body>
</html>""")))


def page_course(slug):
    """The course a reader on this page most likely wants, or None."""
    by_href = {pages_a.course_href(c["name"]): c["name"] for c in pages_a.COURSE_DATA}
    if slug in by_href:
        return by_href[slug]
    if slug.startswith("style-"):
        return by_href.get(style_render.COURSE)
    art = BY_SLUG.get(slug[:-5])
    return by_href.get(art["cta"]["href"]) if art else None


def _with_page_whatsapp(slug, title, html_out):
    """Every WhatsApp link opens with a message naming this page, and every
    generic Enrol button carries the course this page is about."""
    html_out = html_out.replace(whatsapp_href(), whatsapp_href(whatsapp_text(slug, title)))
    course = page_course(slug)
    if course:
        html_out = html_out.replace(f'href="{ENROLL_HREF}"', f'href="{pages_a.enroll_href(course)}"')
    return html_out


ARTICLES = articles_all.ARTICLES


def _course_cta(article):
    """Send an article's course CTA to that course's own page, not the grid."""
    cta = article["cta"]
    hit = next((c for c in pages_a.COURSE_DATA
                if cta["body"].startswith(c["name"].replace("&amp;", "&"))), None)
    if not hit or cta["href"] != "courses.html":
        return article
    return {**article, "cta": {**cta, "href": pages_a.course_href(hit["name"])}}


ARTICLES = [_course_cta(a) for a in ARTICLES]
BY_SLUG = {a["slug"]: a for a in ARTICLES}

# Reuse the existing blog banner, then list the real guides underneath it.
_BLOG_BANNER = pages_a.BLOG.split("<section", 1)[0]

PAGES = {
    "index.html":     ("Craft Beer School | Brewing Courses in India, Grain to Glass",
                        "India's online and in-person beer school. Brewing, tasting, branding and business, plus spirits, AI for breweries, kombucha and hop water.",
                        "home", pages_a.HOME),
    "about.html":     ("About Us | Craft Beer School",
                        "Better beer education brews better beer. Meet Craft Beer School, India's grain-to-glass beer school, our mentors, mission and method.",
                        "about", pages_a.ABOUT),
    "courses.html":   ("Beer Brewing Courses in India | Craft Beer School",
                        f"{pages_a.COURSE_COUNT_WORD.capitalize()} online courses plus in-person workshops in Bengaluru. Brewing, business, styles, sensory, AI, ESG, distilling and free safety.",
                        "courses", pages_a.COURSES),
    "resources.html": ("Free Beer Education Resources | Craft Beer School",
                        "Free beer education: Beer 101, styles primer, a brewing glossary, calculators and tasting tools to sharpen your palate and your process.",
                        "resources", pages_a.RESOURCES),
    "blog.html":      ("Blog and Podcasts | Craft Beer School",
                        "Insights from the brewing world, quality, marketing, tasting and the business of beer, plus our podcast conversations with industry voices.",
                        "blog", article_render.blog_index(ARTICLES, _BLOG_BANNER, articles_all.SEGMENT, articles_all.SEGMENTS)),
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


PAGES.update(course_pages.pages())
COURSE_SLUGS = set(course_pages.pages())
# Every course page ends with the free guides that already sell it.
for _c in pages_a.COURSE_DATA:
    _slug = pages_a.course_href(_c["name"])
    _t, _d, _a, _b = PAGES[_slug]
    _skip = set(course_pages.DETAIL[course_pages.plain(_c["name"])]["reading"])
    PAGES[_slug] = (_t, _d, _a, _b + discover.course_guides_section(_c, ARTICLES, _skip))
# The course finder replaces the "ask us" band on the courses page.
_t, _d, _a, _b = PAGES["courses.html"]
PAGES["courses.html"] = (_t, _d, _a, re.sub(r'<section class="cta"><div class="wrap"><h2>Not sure which course fits\?.*?</section>', lambda m: discover.finder(), _b, count=1, flags=re.S))
PAGES["search.html"] = ("Search | Craft Beer School",
                        "Search every guide, course, beer style and mentor on Craft Beer School from one box.",
                        "", discover.search_page())
PAGES.update(style_render.pages(BY_SLUG))
PAGES[companies.SLUG] = companies.PAGE
PAGES.update(mentors.pages())
PAGES.update(brochure_pages.pages())
PAGES[podcast.SLUG] = podcast.page(pages_a.banner)
PAGES[photos.CREDITS] = ("Image Credits | Craft Beer School",
                         "Credits and licences for the free-licence photographs used on Craft Beer School.",
                         "", photos.credits_page())

for _a in ARTICLES:
    PAGES[f"{_a['slug']}.html"] = (
        _a["title"], _a["desc"], "blog",
        article_render.render(_a, BY_SLUG) + discover.recommended_section(_a, ARTICLES))


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", path)


def main():
    for slug, (title, desc, active, body) in PAGES.items():
        write(slug, page(slug, title, desc, active, body))

    today = datetime.date.today().isoformat()
    write("assets/search.json", discover.search_index(ARTICLES, style_render.load_cards(), mentors.MENTORS))
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

    # Admin surface. Kept out of PAGES so it never lands in the nav, the
    # sitemap or the JSON-LD graph. Its data is protected by row level
    # security, not by being hard to find.
    write("admin.html", fill_ctas(pathlib.Path("admin_template.html").read_text()))


if __name__ == "__main__":
    main()
