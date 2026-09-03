#!/usr/bin/env python3
"""SEO and AEO invariants for the built site. Run: python3 test_seo.py

Catches the failures that are invisible in a browser but cost rankings and
citations: a canonical pointing at the wrong host, structured data that
contradicts the visible price, a sitemap listing a page that does not exist.
"""
import json
import pathlib
import re
import sys

import seo

HERE = pathlib.Path(__file__).parent
PAGES = {p.name: p.read_text() for p in sorted(HERE.glob("*.html"))}
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


# --- head metadata ---------------------------------------------------------
for name, html in PAGES.items():
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    check(canonical, f"{name}: no canonical")
    if canonical:
        check(canonical.group(1) == seo.url_for(name),
              f"{name}: canonical is {canonical.group(1)}, expected {seo.url_for(name)}")
        check(canonical.group(1).startswith(seo.SITE_URL),
              f"{name}: canonical does not use the live domain")

    title = re.search(r"<title>(.*?)</title>", html)
    check(title and len(title.group(1)) <= 60,
          f"{name}: title missing or over 60 chars")
    desc = re.search(r'<meta name="description" content="([^"]*)"', html)
    check(desc and 50 <= len(desc.group(1)) <= 165,
          f"{name}: meta description missing or outside 50-165 chars")

    for tag in ("og:title", "og:description", "og:image", "og:url"):
        check(f'property="{tag}"' in html, f"{name}: missing {tag}")
    check('name="twitter:card"' in html, f"{name}: missing twitter:card")
    check('rel="icon"' in html, f"{name}: missing favicon link")
    check('lang="en-IN"' in html, f"{name}: html lang is not en-IN")

# --- structured data -------------------------------------------------------
for name, html in PAGES.items():
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    check(len(blocks) == 1, f"{name}: expected exactly 1 JSON-LD block, got {len(blocks)}")
    if not blocks:
        continue
    try:
        graph = json.loads(blocks[0])["@graph"]
    except Exception as exc:
        errors.append(f"{name}: JSON-LD does not parse ({exc})")
        continue
    types = {t for n in graph for t in ([n["@type"]] if isinstance(n["@type"], str) else n["@type"])}
    check("WebPage" in types, f"{name}: no WebPage node")
    check("BreadcrumbList" in types, f"{name}: no BreadcrumbList")

# Course markup must match the price shown on the page, or it is a rich-result
# penalty rather than a boost.
courses_graph = json.loads(
    re.search(r'<script type="application/ld\+json">(.*?)</script>',
              PAGES["courses.html"], re.S).group(1))["@graph"]
course_nodes = [n for n in courses_graph if n.get("@type") == "Course"]
check(len(course_nodes) == 6, f"courses.html: {len(course_nodes)} Course nodes, expected 6")
for node in course_nodes:
    price = node["offers"]["price"]
    check(f"₹{int(price):,}" in PAGES["courses.html"],
          f"courses.html: schema price {price} for '{node['name']}' is not shown on the page")
    check(node["offers"]["priceCurrency"] == "INR", f"{node['name']}: price not in INR")
    check(node.get("hasCourseInstance"), f"{node['name']}: no hasCourseInstance, no rich result")

faq_graph = json.loads(
    re.search(r'<script type="application/ld\+json">(.*?)</script>',
              PAGES["faq.html"], re.S).group(1))["@graph"]
faq = [n for n in faq_graph if n.get("@type") == "FAQPage"]
check(faq, "faq.html: no FAQPage node")
if faq:
    qs = faq[0]["mainEntity"]
    check(len(qs) >= 5, f"faq.html: only {len(qs)} questions in schema")
    for q in qs:
        check(q["name"][:40] in PAGES["faq.html"],
              f"faq.html: schema question not visible on page: {q['name'][:50]}")

# --- crawler files ---------------------------------------------------------
sitemap = (HERE / "sitemap.xml").read_text()
check(sitemap.lstrip().startswith("<?xml"), "sitemap.xml: missing XML declaration")
check('xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' in sitemap,
      "sitemap.xml: wrong or missing namespace")
locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
check(len(locs) == len(PAGES), f"sitemap lists {len(locs)} urls for {len(PAGES)} pages")
for loc in locs:
    slug = loc.replace(seo.SITE_URL, "").lstrip("/") or "index.html"
    check(slug in PAGES, f"sitemap lists {loc} but {slug} does not exist")

robots = (HERE / "robots.txt").read_text()
check(f"Sitemap: {seo.SITE_URL}/sitemap.xml" in robots, "robots.txt: sitemap line wrong")
for bot in ("GPTBot", "ClaudeBot", "PerplexityBot", "OAI-SearchBot"):
    check(bot in robots, f"robots.txt: {bot} not addressed (AEO)")

llms = (HERE / "llms.txt").read_text()
check(llms.startswith("# "), "llms.txt: must open with an H1")
for c in __import__("pages_a").COURSE_DATA:
    check(c["amount"] in llms, f"llms.txt: missing price for {c['name']}")

check((HERE / "CNAME").read_text().strip() == seo.SITE_URL.split("//")[1],
      "CNAME does not match SITE_URL")
check((HERE / ".nojekyll").exists(), "missing .nojekyll")
for asset in ("favicon.ico", "assets/favicon.svg", "assets/og-default.png",
              "assets/apple-touch-icon.png"):
    check((HERE / asset).exists(), f"missing {asset}")

if errors:
    for e in errors:
        print("FAIL:", e)
    print(f"\n{len(errors)} SEO check(s) failed")
    sys.exit(1)
print(f"All SEO/AEO checks passed across {len(PAGES)} pages.")
