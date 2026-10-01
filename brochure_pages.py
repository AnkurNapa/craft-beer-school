# -*- coding: utf-8 -*-
"""Read-online pages for the two PDFs (prospectus and corporate brochure).

Each PDF page is rasterised to a JPEG (pymupdf, no poppler needed) and stacked
on an ordinary page, so it reads the same on every phone; a PDF iframe shows
only page one on iOS. Images regenerate when the PDF is newer than them.
"""
import pathlib

import fitz
from PIL import Image

HERE = pathlib.Path(__file__).parent
DOCS = {
    "prospectus.html": dict(
        pdf="assets/craft-beer-school-prospectus.pdf", key="prospectus",
        title="Course Prospectus | Craft Beer School",
        desc="Read the Craft Beer School prospectus online: every course, fee and format, the team, and how to enrol.",
        eyebrow="Course prospectus", h1="Every course, in one place.",
        sub="Read it here, or download the PDF to share."),
    "corporate-brochure.html": dict(
        pdf="assets/craft-beer-school-corporate-services.pdf", key="corporate",
        title="Corporate Services Brochure | Craft Beer School",
        desc="Read our corporate services brochure online: GCC training, hiring, brand and marketing, market entry into India and digital transformation.",
        eyebrow="Corporate brochure", h1="Training, hiring and consulting.",
        sub="Read it here, or download the PDF to share with your team."),
}
DPI = 130
ZOOM_DPI = 220  # tap-to-zoom copy, sharp enough to read A4 text on a phone


def _images(doc):
    pdf = HERE / doc["pdf"]
    out = HERE / "assets/brochures" / doc["key"]
    out.mkdir(parents=True, exist_ok=True)
    stale = not any(out.glob("p*-zoom.jpg")) or min(f.stat().st_mtime for f in out.glob("p*.jpg")) < pdf.stat().st_mtime
    d = fitz.open(pdf)
    if stale:
        for f in out.glob("p*.jpg"):
            f.unlink()
        for i, page in enumerate(d, 1):
            pix = page.get_pixmap(dpi=DPI)
            Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(out / f"p{i}.jpg", quality=82, optimize=True, progressive=True)
            big = page.get_pixmap(dpi=ZOOM_DPI)
            Image.frombytes("RGB", (big.width, big.height), big.samples).save(out / f"p{i}-zoom.jpg", quality=80, optimize=True, progressive=True)
    pix = d[0].get_pixmap(dpi=DPI)
    return [f"assets/brochures/{doc['key']}/p{i}.jpg" for i in range(1, d.page_count + 1) if True], pix.width, pix.height


def _body(doc):
    imgs, w, h = _images(doc)
    pages = "".join(
        f'<a class="bro-link" href="{src.replace(".jpg", "-zoom.jpg")}" target="_blank" rel="noopener" aria-label="Page {i}, open full size">'
        f'<img class="bro-page" src="{src}" alt="{doc["eyebrow"]}, page {i}" width="{w}" height="{h}" '
        f'loading="{"eager" if i == 1 else "lazy"}" decoding="async" /></a>'
        for i, src in enumerate(imgs, 1))
    return f"""
<section class="banner"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a> / {doc["eyebrow"]}</div>
  <span class="eyebrow">{doc["eyebrow"]}</span>
  <h1 class="display">{doc["h1"]}</h1>
  <p>{doc["sub"]}</p>
  <div class="cta-pair" style="margin-top:1.4rem"><a class="btn btn-amber" href="{doc["pdf"]}" download data-cta="brochure-download-top">[[download]] Download the PDF</a></div>
</div></section>
<section class="bro-sec"><div class="wrap bro"><p class="bro-hint">Tap any page to open it full size and zoom in.</p>{pages}
  <div class="cta-pair" style="justify-content:center;margin-top:2rem"><a class="btn btn-amber" href="{doc["pdf"]}" download data-cta="brochure-download-bottom">[[download]] Download the PDF</a><a class="btn btn-wa" href="__WA__" target="_blank" rel="noopener" data-cta="brochure-whatsapp">[[whatsapp]] Ask on WhatsApp</a></div>
</div></section>
"""


def pages():
    return {slug: (d["title"], d["desc"], "", _body(d)) for slug, d in DOCS.items() if (HERE / d["pdf"]).exists()}
