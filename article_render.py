# -*- coding: utf-8 -*-
"""Renders long-form articles and the blog index from article records.

Every article gets the same furniture without the writer having to remember it:
breadcrumbs, an inline CTA roughly a third of the way down, a closing CTA, an
FAQ block that doubles as FAQPage schema, and links to sibling articles. The
CTA is part of the template, so no article can ship without a way to enrol.
"""

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
      <article class="card reveal"><div class="card-body">
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
        if i + 1 == cut:
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
      <span>Craft Beer School</span>
    </p>
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


def blog_index(articles, banner):
    """The blog listing, built from the real articles rather than placeholders."""
    cards = "".join(f"""
      <article class="card reveal">
        <div class="card-body">
          <span class="cat">{a['cat']}</span>
          <h3>{a['h1']}</h3>
          <p>{a['teaser']}</p>
          <div class="foot">
            <a href="{a['slug']}.html" class="link-arrow" data-cta="blog-card">Read</a>
            <span class="read">{a['read']}</span>
          </div>
        </div>
      </article>""" for a in articles)
    return banner + f"""
<section>
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">The Journal</span>
      <h2>Guides from the brewhouse floor.</h2>
      <p class="lead">Written by brewers who actually run the numbers, for people
      learning beer in India. No filler, no borrowed listicles.</p>
    </div>
    <div class="grid-3">{cards}</div>
  </div>
</section>

<section class="cta">
  <div class="wrap" style="text-align:center">
    <h2>Reading is a start. Brewing is better.</h2>
    <p class="lead" style="margin-inline:auto">Every guide here is a slice of what
    we teach properly, with mentors, tastings and real brewhouse time.</p>
    <a class="btn btn-amber" href="courses.html" data-cta="blog-courses">See the courses</a>
  </div>
</section>
"""
