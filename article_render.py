# -*- coding: utf-8 -*-
"""Renders long-form articles and the blog index from article records.

Every article gets the same furniture without the writer having to remember it:
breadcrumbs, an inline CTA roughly a third of the way down, a closing CTA, an
FAQ block that doubles as FAQPage schema, and links to sibling articles. The
CTA is part of the template, so no article can ship without a way to enrol.
"""

import pathlib

THUMB_DIR = pathlib.Path(__file__).parent / "assets/og/thumb"


def thumb(slug, alt):
    """Card image: the article's own share card, scaled down. Empty if not made yet."""
    if not (THUMB_DIR / f"{slug}.jpg").exists():
        return ""
    return (f'<img class="thumb" src="assets/og/thumb/{slug}.jpg" srcset="{SRCSET.format(slug=slug)}" '
            f'sizes="{SIZES}" alt="{alt}" width="600" height="315" loading="lazy" decoding="async" />')


# Sharp on high-density phones: they pick the full share card, desktops the 600px copy.
SRCSET = "assets/og/thumb/{slug}.jpg 600w, assets/og/{slug}.jpg 1200w"
SIZES = "(max-width: 680px) 92vw, 360px"


BREADCRUMB = ('<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>'
              ' / <a href="blog.html">Blog</a> / <span>{title}</span></nav>')


def _cta(cta, variant="inline"):
    """Conversion block. `variant` inline sits mid-article, band closes it."""
    cls = "cta-inline" if variant == "inline" else "cta-band"
    return f"""
<aside class="{cls}">
  <div>
    <h3>{cta['title']}</h3>
    <p>{cta['body']}</p>
  </div>
  <a class="btn btn-amber" href="{cta['href']}" data-cta="article-{variant}">{cta['label']}</a>
</aside>"""


def _byline(people):
    """Who the story is about and who wrote it, each with a photo when we have one."""
    cards = "".join(f"""<div class="byline">
      {f'<img src="{p["photo"]}" alt="{p["name"]}" width="64" height="64" loading="eager">' if p.get("photo") else ""}
      <div><span>{label}</span><strong>{p['name']}</strong><span>{p.get('role', '')}</span></div>
    </div>""" for label, p in people if p)
    return f'<div class="bylines">{cards}</div>' if cards else ""


def _faqs(faqs):
    if not faqs:
        return ""
    items = "".join(
        f'<details class="reveal"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in faqs)
    return f"""
<section class="faq-block">
  <h2 id="faq">Common questions</h2>
  {items}
</section>"""


def _related(article, by_slug):
    links = [by_slug[s] for s in article.get("related", []) if s in by_slug]
    if not links:
        return ""
    cards = "".join(f"""
      <article class="card reveal">{thumb(a['slug'], a['h1'])}<div class="card-body">
        <span class="cat">{a['cat']}</span>
        <h3>{a['h1']}</h3>
        <p>{a['teaser']}</p>
        <div class="foot"><a href="{a['slug']}.html" class="link-arrow" data-cta="related-article">Read</a></div>
      </div></article>""" for a in links)
    return f"""
<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Keep reading</span><h2>Related guides</h2></div>
    <div class="grid-3">{cards}</div>
  </div>
</section>"""


def render(article, by_slug):
    """Full page body for one article."""
    secs = article["sections"]
    # Drop the inline CTA after the first third, where a reader is engaged but
    # has not yet finished. Never after the last section, that is the band's job.
    cut = max(1, min(len(secs) - 1, round(len(secs) / 3)))

    parts = []
    for i, (heading, body) in enumerate(secs):
        anchor = heading.lower().replace(" ", "-").replace(",", "").replace("?", "")
        parts.append(f'<h2 id="{anchor}">{heading}</h2>\n{body}')
        # Guest stories run uninterrupted; only the closing band sells.
        if i + 1 == cut and not article.get("author"):
            parts.append(_cta(article["cta"], "inline"))
    article_body = "\n".join(parts)

    toc = "".join(
        f'<li><a href="#{h.lower().replace(" ", "-").replace(",", "").replace("?", "")}">{h}</a></li>'
        for h, _ in secs)

    return f"""
<article class="post">
  <div class="wrap post-head">
    {BREADCRUMB.format(title=article['h1'])}
    <span class="eyebrow">{article['cat']}</span>
    <h1 class="post-title">{article['h1']}</h1>
    <p class="lead">{article['standfirst']}</p>
    <p class="post-meta">
      <span>{article['read']} read</span> ·
      <span>Updated <time datetime="{article['updated']}">{article['updated_label']}</time></span> ·
      <span>{'By ' + article['author']['name'] if article.get('author') else 'Craft Beer School'}</span>
    </p>{_byline([('The story of', article.get('subject')), ('Written by', article.get('author'))])}
  </div>

  <div class="wrap post-body">
    <nav class="toc" aria-label="On this page">
      <h2>On this page</h2>
      <ol>{toc}</ol>
    </nav>

    {article_body}

    {_faqs(article.get('faqs'))}

    {_cta(article['cta'], 'band')}
  </div>
</article>

{_related(article, by_slug)}
"""


def _card(a):
    return f"""
      <article class="card reveal">{thumb(a['slug'], a['h1'])}
        <div class="card-body">
          <span class="cat">{a['cat']}</span>
          <h3>{a['h1']}</h3>
          <p>{a['teaser']}</p>
          <div class="foot">
            <a href="{a['slug']}.html" class="link-arrow" data-cta="blog-card">Read</a>
            <span class="read">{a['read']}</span>
          </div>
        </div>
      </article>"""


SHOWN = 6  # per segment before the rest fold away


def _seg_id(name):
    return name.lower().replace(" ", "-")


def blog_index(articles, banner, segment_of, segments):
    """The blog as a set of doors, one per reader segment, each ending at the
    course that segment is most likely to buy."""
    jump = "".join(f'<a href="#{_seg_id(name)}" class="seg-chip" data-cta="blog-segment">{name}</a>'
                   for name, *_ in segments)
    blocks = []
    for name, who, course_href, course_name in segments:
        mine = [a for a in articles if segment_of.get(a["slug"]) == name]
        if not mine:
            continue
        head, rest = mine[:SHOWN], mine[SHOWN:]
        head_cards = "".join(_card(a) for a in head)
        rest_cards = "".join(_card(a) for a in rest)
        more = (f'<details class="more"><summary>Show all {len(mine)} {name.lower()} guides</summary>'
                f'<div class="grid-3">{rest_cards}</div></details>') if rest else ""
        blocks.append(f"""
<section id="{_seg_id(name)}" class="seg">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">For {name.lower()}</span><h2>{who}</h2></div>
    <div class="grid-3">{head_cards}</div>
    {more}
    <aside class="cta-inline" style="margin-top:2rem">
      <div><h3>Ready to go further?</h3><p>{course_name} turns these guides into a structured course, live every weekend with a mentor.</p></div>
      <a class="btn btn-amber" href="{course_href}" data-cta="blog-segment-course">See {course_name}</a>
    </aside>
  </div>
</section>""")
    blocks_html = "".join(blocks)
    return banner + f"""
<section style="padding-bottom:0">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">The Journal</span>
      <h2>{len(articles)} guides from the brewhouse floor.</h2>
      <p class="lead">Written by brewers who actually run the numbers, for people
      learning beer in India. Start with the door that fits you.</p>
    </div>
    <nav class="seg-nav" aria-label="Guides by reader">{jump}</nav>
  </div>
</section>
{blocks_html}
<section class="cta">
  <div class="wrap" style="text-align:center">
    <h2>Reading is a start. Brewing is better.</h2>
    <p class="lead" style="margin-inline:auto">Every guide here is a slice of what
    we teach properly, with mentors, tastings and real brewhouse time.</p>
    <a class="btn btn-amber" href="courses.html" data-cta="blog-courses">See the courses</a>
  </div>
</section>
"""
