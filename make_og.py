#!/usr/bin/env python3
"""Per-page social share images (1200x630) in the house look. Run: python3 make_og.py [--force]

Each page gets assets/og/<page>.jpg with its own headline and context: a style
page shows its glass in the beer's colour, an article its category and read
time, a course its format. seo.py points og:image at the file when it exists
and falls back to assets/og-default.png when it does not, so a page added
before this script reruns still shares cleanly.

Images are only re-rendered when their content changes (manifest of hashes).
Needs Playwright with Chromium, and network for Google Fonts.
"""
import base64
import hashlib
import html
import json
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

import articles_all
import build
import game_art
import mentors
import pages_a
import style_render

HERE = pathlib.Path(__file__).parent
OUT = HERE / "assets/og"
MANIFEST = OUT / "manifest.json"
SKIP = {"index.html"}  # the home page keeps the hand-made og-default.png
TEMPLATE_VERSION = "3"

ARTICLES = {a["slug"]: a for a in articles_all.ARTICLES}
CARDS = style_render.load_cards()
COURSES = {pages_a.course_href(c["name"]): c for c in pages_a.COURSE_DATA}
MENTORS = {m["slug"]: m for m in mentors.MENTORS}


from article_art import CAT_COLOUR, topic_icon


def article_art(slug, cat):
    """Tilted colour tile with a big white line icon, a gold outline offset behind it for depth."""
    colour = CAT_COLOUR.get(cat, "#d9862a")
    ic = game_art.icon(topic_icon(slug, cat), "200px", "#fff8ec", 2.2)
    return ('<div style="position:relative;width:300px;height:300px;margin:0 -70px 20px 0">'
            '<div style="position:absolute;inset:0;border:5px solid #f3c34d;border-radius:44px;transform:translate(22px,22px) rotate(4deg)"></div>'
            f'<div style="position:absolute;inset:0;background:{colour};border-radius:44px;transform:rotate(-3deg);'
            'display:flex;align-items:center;justify-content:center;box-shadow:0 30px 60px rgba(0,0,0,.35)">'
            f'{ic}</div></div>')


def og_file(slug):
    return OUT / (slug[:-5] + ".jpg")


def spec(slug, title):
    """(eyebrow, headline, pill, glass_svg) for one page."""
    name = re.sub(r"\s*\|\s*Craft Beer School\s*$", "", html.unescape(title)).strip()
    key = slug[:-5]
    if key in CARDS:
        c = CARDS[key]
        glass = style_render.glass_svg(c["glass"], c["srm"], 330, "og").replace('stroke-width="2"', 'stroke-width="5"')
        return (f"Style Library · {c['family']}", c["name"], f"{c['abv']} ABV · {c['ibu']} IBU", glass)
    if key in ARTICLES:
        a = ARTICLES[key]
        return (a["cat"], html.unescape(a["h1"]), f"{a['read']} read", article_art(key, a["cat"]))
    if slug in COURSES:
        c = COURSES[slug]
        return ("Course · Live online", html.unescape(re.sub("<[^>]+>", "", c["name"])), f"{c['dur']} · {c['price']}", "")
    if slug in MENTORS:
        m = MENTORS[slug]
        face = "data:image/jpeg;base64," + base64.b64encode((HERE / m["img"]).read_bytes()).decode()
        # inline styles so the shared template (and every other page's hash) stays unchanged
        photo = f'<img src="{face}" alt="" style="width:360px;height:360px;object-fit:cover;border-radius:28px;border:6px solid #f3c34d;margin-right:-60px">'
        return (html.unescape(m["role"].split(" · ")[0]), m["name"], "Meet the mentor", photo)
    if slug == style_render.INDEX:
        return ("Free Style Library", f"{len(CARDS)} beer styles, explained for India", "Free to read", "")
    return ("Craft Beer School", name, "Grain to glass", "")


PAGE = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Hanken+Grotesk:wght@600;700&family=Space+Mono:wght@700&display=block" rel="stylesheet">
<style>
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#123c4a;color:#fff;font-family:"Hanken Grotesk",sans-serif;position:relative;overflow:hidden}
.bar{position:absolute;top:0;left:0;right:0;height:10px;background:linear-gradient(90deg,#d9862a,#f3c34d 30%,#2f8f5f 60%,#0a6d84)}
.glow{position:absolute;right:-180px;top:-120px;width:760px;height:760px;border-radius:50%;background:radial-gradient(circle,rgba(217,134,42,.45),rgba(217,134,42,0) 68%)}
.eyebrow{position:absolute;left:80px;top:80px;right:80px;font-family:"Space Mono",monospace;font-size:22px;letter-spacing:.28em;text-transform:uppercase;color:#f3c34d}
h1{position:absolute;left:80px;top:150px;width:__W__px;height:300px;display:flex;align-items:center;font-family:"Fraunces",serif;font-weight:600;line-height:1.08;letter-spacing:-.01em}
.glass{position:absolute;right:150px;top:70px;height:360px;display:flex;align-items:flex-end;color:#dfe9ec}
.glass svg{height:340px;width:auto}
.foot{position:absolute;left:80px;right:80px;bottom:62px;display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:20px;font-size:26px;font-weight:700;line-height:1.3}
.brand img{width:72px;height:80px;object-fit:contain}
.brand span{display:block;font-weight:600;color:rgba(255,255,255,.75)}
.pill{background:#d9862a;color:#fff;font-weight:700;font-size:25px;padding:16px 30px;border-radius:999px;white-space:nowrap}
</style></head><body>
<div class="bar"></div>__GLOW__
<div class="eyebrow">__EYEBROW__</div>
<h1 style="font-size:__SIZE__px">__TITLE__</h1>
__GLASS__
<div class="foot"><div class="brand"><img src="__LOGO__" alt=""><div>Craft Beer School<span>craftbeerschool.in</span></div></div>
<div class="pill">__PILL__</div></div>
</body></html>"""


LOGO_URI = "data:image/png;base64," + base64.b64encode((HERE / "assets/footer-logo.png").read_bytes()).decode()


def render_html(eyebrow, title, pill, glass):
    width = 660 if glass else 1000
    # Long headlines step down so every one fits three lines.
    size = 84 if len(title) <= 22 else 72 if len(title) <= 40 else 60 if len(title) <= 60 else 50
    esc = lambda s: html.escape(s, quote=False)
    return (PAGE.replace("__W__", str(width)).replace("__SIZE__", str(size))
            .replace("__EYEBROW__", esc(eyebrow)).replace("__TITLE__", esc(title)).replace("__PILL__", esc(pill))
            .replace("__GLASS__", f'<div class="glass">{glass}</div>' if glass else "")
            .replace("__GLOW__", "" if glass else '<div class="glow"></div>')
            .replace("__LOGO__", LOGO_URI))


THUMBS = OUT / "thumb"


def make_thumbs():
    """600px copies of each share card, used as card images on the blog."""
    from PIL import Image
    THUMBS.mkdir(exist_ok=True)
    for src in OUT.glob("*.jpg"):
        dst = THUMBS / src.name
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            Image.open(src).resize((600, 315), Image.LANCZOS).save(dst, quality=82, optimize=True)
    for dst in THUMBS.glob("*.jpg"):
        if not (OUT / dst.name).exists():
            dst.unlink()


def main(force=False):
    OUT.mkdir(parents=True, exist_ok=True)
    seen = json.loads(MANIFEST.read_text()) if MANIFEST.exists() and not force else {}
    jobs = []
    for slug, (title, *_rest) in build.PAGES.items():
        if slug in SKIP:
            continue
        doc = render_html(*spec(slug, title))
        digest = hashlib.sha1((TEMPLATE_VERSION + doc).encode()).hexdigest()
        if seen.get(slug) != digest or not og_file(slug).exists():
            jobs.append((slug, doc, digest))
    print(f"{len(jobs)} of {len(build.PAGES) - len(SKIP)} images to render")
    if jobs:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1200, "height": 630})
            for i, (slug, doc, digest) in enumerate(jobs, 1):
                page.set_content(doc, wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                h1 = page.locator("h1")
                if h1.evaluate("e => e.scrollHeight > e.clientHeight + 2"):
                    raise SystemExit(f"headline overflows on {slug}")
                page.screenshot(path=str(og_file(slug)), type="jpeg", quality=86)
                seen[slug] = digest
                if i % 25 == 0:
                    print(f"  {i}/{len(jobs)}")
            browser.close()
    make_thumbs()
    live = {s for s in build.PAGES if s not in SKIP}
    for f in OUT.glob("*.jpg"):  # drop images for pages that no longer exist
        if f.stem + ".html" not in live:
            f.unlink()
    MANIFEST.write_text(json.dumps({k: v for k, v in sorted(seen.items()) if k in live}, indent=1))


if __name__ == "__main__":
    main(force="--force" in sys.argv)
