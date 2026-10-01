# -*- coding: utf-8 -*-
"""Free-licence photos (Wikimedia Commons) with the credit each licence asks for.

content/images.json is written by fetch_images.py. A slot with no picked image
renders nothing, so pages never show a broken or uncredited photo.
"""
import html
import json
import pathlib

HERE = pathlib.Path(__file__).parent
RECORD = HERE / "content/images.json"
CREDITS = "image-credits.html"


def _all():
    return json.loads(RECORD.read_text()) if RECORD.exists() else {}


def _short_author(a):
    a = " ".join(a.split())
    return a if len(a) <= 40 else a[:38].rsplit(" ", 1)[0] + "..."


def credit(r):
    return (f'Photo: {html.escape(_short_author(r["author"]))}, '
            f'<a href="{r["page"]}" target="_blank" rel="noopener nofollow">{html.escape(r["licence"])}</a>, Wikimedia Commons')


SHOW_ON_SITE = False  # photos are used in the prospectus PDF only, by request


def figure(slot, alt, cls="photo", eager=False):
    if not SHOW_ON_SITE:
        return ""
    r = _all().get(slot)
    if not r:
        return ""
    src, sm = r["file"], r["file"].replace(".jpg", "-sm.jpg")
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<figure class="{cls}"><img src="{src}" srcset="{sm} 600w, {src} 1200w" '
            f'sizes="(max-width: 680px) 92vw, 1100px" alt="{html.escape(alt)}" width="1200" height="750" {load} decoding="async" />'
            f'<figcaption>{credit(r)}</figcaption></figure>')


def _licence(r):
    lic = html.escape(r["licence"])
    return f'<a href="{r["licence_url"]}" target="_blank" rel="noopener">{lic}</a>' if r.get("licence_url") else lic


def credits_page():
    rows = "".join(
        f'<tr><td><img src="{r["file"].replace(".jpg", "-sm.jpg")}" alt="" width="120" height="75" loading="lazy" /></td>'
        f'<td><a href="{r["page"]}" target="_blank" rel="noopener nofollow">{html.escape(r["title"].removeprefix("File:"))}</a></td>'
        f'<td>{html.escape(" ".join(r["author"].split()))}</td><td>{_licence(r)}</td></tr>'
        for r in _all().values())
    return f"""
<section class="banner"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a> / Image credits</div>
  <span class="eyebrow">Image credits</span>
  <h1 class="display">Photos in our prospectus.</h1>
  <p>The photographs in the Craft Beer School prospectus come from Wikimedia Commons under free licences. Thank you to the photographers.</p>
</div></section>
<section><div class="wrap">
  <p style="max-width:62ch;color:var(--ink-soft)">Each photo has been cropped and resized for the web. Photos under a Creative Commons ShareAlike licence remain under that licence as modified; the licence link for each is below. Beer glass illustrations and course share images are our own.</p>
  <div style="overflow-x:auto"><table class="credits"><thead><tr><th></th><th>Image</th><th>Author</th><th>Licence</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>
"""
