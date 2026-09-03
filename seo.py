# -*- coding: utf-8 -*-
"""SEO and AEO layer: canonicals, social cards, structured data, crawler files.

AEO (answer engine optimization) is the reason the JSON-LD here is generated
from the same records that render the page. An assistant answering "what does
a brewing course cost in India" can only cite a price it can parse, and it will
not cite one that contradicts the visible page.
"""
import json

import pages_a
import pages_b

SITE_URL = "https://craftbeerschool.in"      # apex is canonical, www redirects
SITE_NAME = "Craft Beer School"
TAGLINE = "Grain to Glass. India's beer school."
LOGO = f"{SITE_URL}/assets/logo.png"
OG_IMAGE = f"{SITE_URL}/assets/og-default.png"
EMAIL = "chatty@cheerschattyventures.com"
PHONE = "+91-98209-25347"
CITY = "Bengaluru"
COUNTRY = "IN"
TWITTER = ""   # set to "@handle" when one exists

# Crawl priority and change cadence. Legal pages stay indexable but low value.
PAGE_WEIGHT = {
    "index.html": ("1.0", "weekly"),
    "courses.html": ("0.9", "weekly"),
    "contact.html": ("0.8", "monthly"),
    "resources.html": ("0.8", "weekly"),
    "about.html": ("0.7", "monthly"),
    "faq.html": ("0.7", "monthly"),
    "blog.html": ("0.6", "weekly"),
    "careers.html": ("0.5", "monthly"),
    "privacy.html": ("0.2", "yearly"),
    "refund.html": ("0.2", "yearly"),
}

BREADCRUMB_LABEL = {
    "about.html": "About",
    "courses.html": "Courses",
    "resources.html": "Resources",
    "blog.html": "Blog",
    "careers.html": "Careers",
    "contact.html": "Contact",
    "faq.html": "FAQ",
    "privacy.html": "Privacy",
    "refund.html": "Refunds",
}


def url_for(slug):
    """Canonical URL. The homepage canonicalises to the bare domain."""
    return SITE_URL + "/" if slug == "index.html" else f"{SITE_URL}/{slug}"


def _strip(text):
    """Plain text for metadata, entities decoded, quotes made safe."""
    return (text.replace("&amp;", "and").replace("&", "and")
                .replace('"', "'").strip())


# --------------------------------------------------------------------------
# Structured data
# --------------------------------------------------------------------------
def _organization():
    return {
        "@type": ["EducationalOrganization", "LocalBusiness"],
        "@id": f"{SITE_URL}/#organization",
        "name": SITE_NAME,
        "url": SITE_URL,
        "logo": {"@type": "ImageObject", "url": LOGO},
        "image": OG_IMAGE,
        "description": ("India's online and in-person beer school teaching brewing, "
                        "tasting, branding and the business of beer, grain to glass."),
        "email": EMAIL,
        "telephone": PHONE,
        "address": {"@type": "PostalAddress", "addressLocality": CITY,
                    "addressCountry": COUNTRY},
        "areaServed": {"@type": "Country", "name": "India"},
        "knowsAbout": ["Brewing", "Craft beer", "Beer sensory evaluation",
                       "Brewery business management", "Beer styles", "WSET", "Cicerone"],
    }


def _website():
    return {
        "@type": "WebSite",
        "@id": f"{SITE_URL}/#website",
        "url": SITE_URL,
        "name": SITE_NAME,
        "publisher": {"@id": f"{SITE_URL}/#organization"},
        "inLanguage": "en-IN",
    }


def _breadcrumbs(slug):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"}]
    label = BREADCRUMB_LABEL.get(slug)
    if label:
        items.append({"@type": "ListItem", "position": 2, "name": label,
                      "item": url_for(slug)})
    return {"@type": "BreadcrumbList", "itemListElement": items}


def _courses():
    """One Course node per real course, priced in INR.

    hasCourseInstance is required for Course rich results; without it the
    markup validates but earns no enhanced listing.
    """
    out = []
    for c in pages_a.COURSE_DATA:
        name = _strip(c["name"])
        out.append({
            "@type": "Course",
            "@id": f"{SITE_URL}/courses.html#{name.lower().replace(' ', '-')}",
            "name": name,
            "description": _strip(c["blurb"]),
            "provider": {"@id": f"{SITE_URL}/#organization"},
            "url": f"{SITE_URL}/courses.html",
            "inLanguage": "en-IN",
            "teaches": [_strip(i) for i in c["items"]],
            "educationalLevel": c["tag"],
            "hasCourseInstance": [{
                "@type": "CourseInstance",
                "courseMode": "Online",
                "courseWorkload": f"P{c['weeks']}W",
                "instructor": {"@id": f"{SITE_URL}/#organization"},
            }],
            "offers": {
                "@type": "Offer",
                "price": c["amount"],
                "priceCurrency": "INR",
                "category": "Paid",
                "availability": "https://schema.org/InStock",
                "url": f"{SITE_URL}/contact.html#enroll",
            },
        })
    return out


def _faq():
    return {
        "@type": "FAQPage",
        "@id": f"{SITE_URL}/faq.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": _strip(q),
             "acceptedAnswer": {"@type": "Answer", "text": _strip(a)}}
            for q, a in pages_b.FAQ_ITEMS
        ],
    }


def jsonld(slug, title, desc):
    graph = [_organization(), _website(), _breadcrumbs(slug), {
        "@type": "WebPage",
        "@id": url_for(slug) + "#webpage",
        "url": url_for(slug),
        "name": _strip(title),
        "description": _strip(desc),
        "isPartOf": {"@id": f"{SITE_URL}/#website"},
        "about": {"@id": f"{SITE_URL}/#organization"},
        "inLanguage": "en-IN",
    }]
    if slug == "courses.html":
        graph.extend(_courses())
    if slug == "faq.html":
        graph.append(_faq())
    if slug == "contact.html":
        graph.append({"@type": "ContactPage", "@id": url_for(slug) + "#contact",
                      "url": url_for(slug)})
    payload = {"@context": "https://schema.org", "@graph": graph}
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/ld+json">{body}</script>'


# --------------------------------------------------------------------------
# Head metadata
# --------------------------------------------------------------------------
def head_meta(slug, title, desc):
    canonical = url_for(slug)
    safe_title, safe_desc = _strip(title), _strip(desc)
    tw = f'\n<meta name="twitter:site" content="{TWITTER}" />' if TWITTER else ""
    return f"""<link rel="canonical" href="{canonical}" />
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="{SITE_NAME}" />
<meta property="og:locale" content="en_IN" />
<meta property="og:url" content="{canonical}" />
<meta property="og:title" content="{safe_title}" />
<meta property="og:description" content="{safe_desc}" />
<meta property="og:image" content="{OG_IMAGE}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{SITE_NAME}, {TAGLINE}" />
<meta name="twitter:card" content="summary_large_image" />{tw}
<meta name="twitter:title" content="{safe_title}" />
<meta name="twitter:description" content="{safe_desc}" />
<meta name="twitter:image" content="{OG_IMAGE}" />
<link rel="icon" href="/favicon.ico" sizes="32x32" />
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
<link rel="manifest" href="/site.webmanifest" />
<meta name="theme-color" content="#123c4a" />
<meta name="geo.region" content="IN-KA" />
<meta name="geo.placename" content="{CITY}" />"""


# --------------------------------------------------------------------------
# Crawler files
# --------------------------------------------------------------------------
def sitemap_xml(slugs, lastmod):
    urls = []
    for slug in slugs:
        priority, freq = PAGE_WEIGHT.get(slug, ("0.5", "monthly"))
        urls.append(f"""  <url>
    <loc>{url_for(slug)}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>""")
    body = "\n".join(urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""


def robots_txt():
    return f"""# {SITE_NAME}
User-agent: *
Allow: /

# Answer engines are welcome to read and cite this site.
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""


def llms_txt():
    """Plain-language site summary for answer engines (llmstxt.org)."""
    lines = [
        f"# {SITE_NAME}",
        "",
        f"> {SITE_NAME} is an India-based beer school teaching brewing, tasting, "
        "branding and the business of beer, online and in person. Based in "
        f"{CITY}, serving learners across India and worldwide.",
        "",
        "## Courses",
        "",
    ]
    for c in pages_a.COURSE_DATA:
        lines.append(f"- [{_strip(c['name'])}]({SITE_URL}/courses.html): "
                     f"{_strip(c['blurb'])} Duration {c['dur']}. Price INR {c['amount']}.")
    lines += [
        "",
        "## Key pages",
        "",
        f"- [Courses]({SITE_URL}/courses.html): all six online courses and in-person workshops.",
        f"- [Resources]({SITE_URL}/resources.html): free Beer 101, styles primer, glossary and brewing calculators.",
        f"- [FAQ]({SITE_URL}/faq.html): experience needed, format, class size, certification, payment and refunds.",
        f"- [About]({SITE_URL}/about.html): mentors, mission and teaching method.",
        f"- [Contact]({SITE_URL}/contact.html): enrolment form, phone and WhatsApp.",
        "",
        "## Facts",
        "",
        "- Format: live online sessions plus hands-on in-person brewery workshops.",
        "- Certification support: WSET and Cicerone preparation.",
        "- Cohorts are deliberately small, with one-to-one mentorship.",
        f"- Contact: {EMAIL}, {PHONE}.",
        "",
    ]
    return "\n".join(lines)


def webmanifest():
    return json.dumps({
        "name": SITE_NAME,
        "short_name": "CBS",
        "description": TAGLINE,
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#123c4a",
        "icons": [
            {"src": "/assets/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
            {"src": "/assets/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
        ],
    }, indent=2)
