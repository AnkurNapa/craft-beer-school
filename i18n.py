"""Hindi, Marathi, Telugu and Kannada versions of the site.

Run after build.py:   python3 i18n.py build     (writes hi/, mr/, te/, kn/)
                      python3 i18n.py todo      (writes translation work packs)
                      python3 i18n.py merge     (pulls finished packs into memory)

How it works: every built English page is split into leaf text blocks (headings,
paragraphs, list items, labels, buttons). Each block's inner HTML is a segment,
keyed by a hash, and each language keeps one translation memory
(content/i18n/<lang>.json). A page is published in a language only when every
one of its segments is translated, so no half-English page goes live. Internal
links point at the translated page when it exists and at English when not.
"""
import glob
import hashlib
import json
import os
import pathlib
import re
import sys

from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).parent
I18N = ROOT / "content" / "i18n"
SITE = "https://craftbeerschool.in"
FONTS = {"hi": "Noto+Sans+Devanagari", "mr": "Noto+Sans+Devanagari", "te": "Noto+Sans+Telugu", "kn": "Noto+Sans+Kannada"}
LANGS = {"hi": ("हिन्दी", "Hindi"), "mr": ("मराठी", "Marathi"), "te": ("తెలుగు", "Telugu"), "kn": ("ಕನ್ನಡ", "Kannada")}
BLOCK = {"h1", "h2", "h3", "h4", "h5", "p", "li", "dt", "dd", "summary", "figcaption", "th", "td", "label",
         "option", "button", "blockquote", "title"}
SKIP = ["admin.html", "admin_template.html"]
# Phase 1: the pages that sell, plus the tools. Guides follow in later phases.
PHASE1 = (["index.html", "about.html", "courses.html", "contact.html", "faq.html", "resources.html", "careers.html",
           "for-companies.html", "breweries.html", "brewing-glossary.html", "yeast-strains-guide.html", "hops-guide.html",
           "malt-guide.html", "brewery-hopping-india.html", "wset-level-1-beer-last-minute-training.html",
           "brewing-fundamentals-and-beer-crosswords-bundle.html", "in-person-brewing-courses-pune-delhi-gurugram-bengaluru.html",
           "mentor-ankur-napa.html", "mentor-rahul-baliyan.html", "mentor-chatty-girija.html", "mentor-anu-rao.html"]
          + sorted(p.name for p in ROOT.glob("*-course.html"))
          + sorted(p.name for p in ROOT.glob("brewery-hopping-*.html") if p.name != "brewery-hopping-india.html"))


def key(seg):
    return hashlib.sha1(seg.encode("utf-8")).hexdigest()[:16]


def _segments(soup):
    """Leaf blocks whose text has at least one English word, plus the meta description."""
    for el in soup.find_all(BLOCK):
        if el.find(BLOCK) or el.find_parent(["script", "style", "svg", "noscript"]):
            continue
        inner = el.decode_contents().strip()
        if inner and re.search(r"[A-Za-z]{2}", el.get_text(" ", strip=True)):
            yield el, inner


def _parse(path):
    return BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")


def memory(lang):
    f = I18N / f"{lang}.json"
    return json.loads(f.read_text()) if f.exists() else {}


def pages():
    return sorted(p.name for p in ROOT.glob("*.html") if p.name not in SKIP)


def page_segments(name):
    soup = _parse(ROOT / name)
    out = {key(inner): inner for _, inner in _segments(soup)}
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        out[key(meta["content"])] = meta["content"]
    for inp in soup.find_all(attrs={"placeholder": True}):
        out[key(inp["placeholder"])] = inp["placeholder"]
    return out


def translated(lang, mem=None, names=None):
    """Pages fully covered by the memory for this language."""
    mem = mem if mem is not None else memory(lang)
    return {n for n in (names or pages()) if all(k in mem for k in page_segments(n))}


# ---------------------------------------------------------------- build

LINK_ATTRS = (("a", "href"), ("link", "href"), ("img", "src"), ("img", "srcset"), ("script", "src"), ("source", "srcset"), ("form", "action"))


def _rel(url, ready):
    """Rewrite a link from a /<lang>/ page: translated pages stay local, the rest go up a level."""
    if not url or url.startswith(("http:", "https:", "//", "/", "#", "mailto:", "tel:", "data:", "javascript:")):
        return url
    path = url.split("#")[0].split("?")[0]
    if path.endswith(".html") and path in ready:
        return url
    return "../" + url


def _switcher(name, current, ready_by_lang):
    def href(lang):
        if lang == "en":
            return ("../" if current != "en" else "") + name
        if current == "en":
            return f"{lang}/{name}"
        return f"../{lang}/{name}"
    items = [("en", "English")] + [(l, v[0]) for l, v in LANGS.items()]
    links = []
    for l, label in items:
        avail = l == "en" or name in ready_by_lang.get(l, set())
        if l == current:
            links.append(f'<span class="lang-on" lang="{l}">{label}</span>')
        elif avail:
            links.append(f'<a href="{href(l)}" lang="{l}" hreflang="{l}">{label}</a>')
    if len(links) < 2:
        return ""
    return f'<nav class="lang-switch" aria-label="Language">{"".join(links)}</nav>'


def _hreflang(name, ready_by_lang):
    tags = [f'<link rel="alternate" hreflang="en" href="{SITE}/{name}"/>',
            f'<link rel="alternate" hreflang="x-default" href="{SITE}/{name}"/>']
    tags += [f'<link rel="alternate" hreflang="{l}" href="{SITE}/{l}/{name}"/>' for l in LANGS if name in ready_by_lang.get(l, set())]
    return "".join(tags)


def _insert_head_and_switcher(html, name, current, ready_by_lang):
    head = _hreflang(name, ready_by_lang)
    html = re.sub(r'<link rel="alternate" hreflang=[^>]*>', "", html)
    html = html.replace("</head>", head + "</head>", 1)
    sw = _switcher(name, current, ready_by_lang)
    html = re.sub(r'<nav class="lang-switch"[^>]*>.*?</nav>', "", html, flags=re.S)
    if sw:
        html = html.replace('<div class="navlinks" id="navlinks">', '<div class="navlinks" id="navlinks">' + sw, 1)
    return html


def build():
    mems = {l: memory(l) for l in LANGS}
    names = pages()
    ready = {l: translated(l, mems[l], names) for l in LANGS}
    for l in LANGS:
        out_dir = ROOT / l
        out_dir.mkdir(exist_ok=True)
        for old in out_dir.glob("*.html"):
            if old.name not in ready[l]:
                old.unlink()
        for name in sorted(ready[l]):
            soup = _parse(ROOT / name)
            for el, inner in list(_segments(soup)):
                el.clear()
                el.append(BeautifulSoup(mems[l][key(inner)], "html.parser"))
            meta = soup.find("meta", attrs={"name": "description"})
            if meta and meta.get("content") and key(meta["content"]) in mems[l]:
                meta["content"] = mems[l][key(meta["content"])]
                for og in soup.find_all("meta", attrs={"property": "og:description"}) + soup.find_all("meta", attrs={"name": "twitter:description"}):
                    og["content"] = meta["content"]
            for inp in soup.find_all(attrs={"placeholder": True}):
                inp["placeholder"] = mems[l].get(key(inp["placeholder"]), inp["placeholder"])
            if soup.html:
                soup.html["lang"] = l
            for tag, attr in LINK_ATTRS:
                for el in soup.find_all(tag, attrs={attr: True}):
                    if attr == "srcset":
                        el[attr] = ", ".join(_rel(part.strip().split(" ")[0], ready[l]) + (" " + part.strip().split(" ", 1)[1] if " " in part.strip() else "")
                                             for part in el[attr].split(","))
                    else:
                        el[attr] = _rel(el[attr], ready[l])
            canon = soup.find("link", rel="canonical")
            if canon:
                canon["href"] = f"{SITE}/{l}/{name}"
            html = str(soup)
            # inline scripts and styles that point at site files
            html = html.replace("fetch('assets/", "fetch('/assets/").replace('url(assets/', 'url(/assets/')
            html = html.replace("</head>", f'<link href="https://fonts.googleapis.com/css2?family={FONTS[l]}:wght@400;600;800&display=swap" rel="stylesheet" />' + "</head>", 1)
            html = _insert_head_and_switcher(html, name, l, ready)
            (out_dir / name).write_text(html, encoding="utf-8")
    # English pages get the switcher and hreflang too
    for name in names:
        p = ROOT / name
        html = _insert_head_and_switcher(p.read_text(encoding="utf-8"), name, "en", ready)
        p.write_text(html, encoding="utf-8")
    # Translated pages join the sitemap.
    sm = ROOT / "sitemap.xml"
    if sm.exists():
        xml = re.sub(r"\s*<url>\s*<loc>[^<]*/(?:hi|mr|te|kn)/[^<]*</loc>.*?</url>", "", sm.read_text(), flags=re.S)
        extra = "".join(f"\n  <url>\n    <loc>{SITE}/{l}/{n}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>"
                        for l in LANGS for n in sorted(ready[l]))
        sm.write_text(xml.replace("</urlset>", extra + "\n</urlset>", 1))
    for l in LANGS:
        print(l, len(ready[l]), "pages published")
    return ready


# ---------------------------------------------------------------- work packs

PACK_WORDS = 3500


def todo(only=None):
    """Write untranslated segments of the chosen pages as packs for translators."""
    names = only or PHASE1
    todo_dir = I18N / "todo"
    todo_dir.mkdir(parents=True, exist_ok=True)
    for f in todo_dir.glob("*.json"):
        f.unlink()
    segs = {}
    for n in names:
        segs.update(page_segments(n))
    for l in LANGS:
        mem = memory(l)
        missing = [(k, v) for k, v in segs.items() if k not in mem]
        pack, words, n = {}, 0, 1
        for k, v in missing:
            pack[k] = v
            words += len(re.sub(r"<[^>]+>", " ", v).split())
            if words >= PACK_WORDS:
                (todo_dir / f"{l}-{n:03d}.json").write_text(json.dumps(pack, ensure_ascii=False, indent=0))
                pack, words, n = {}, 0, n + 1
        if pack:
            (todo_dir / f"{l}-{n:03d}.json").write_text(json.dumps(pack, ensure_ascii=False, indent=0))
        print(l, len(missing), "segments to translate in", n if pack else n - 1, "packs")


def _tags(s):
    return sorted(re.findall(r"<(/?[a-z0-9]+)", s)), sorted(re.findall(r'href="([^"]*)"', s))


def merge():
    """Merge finished packs (content/i18n/done/<lang>-NNN.json) after checking markup survived."""
    done = I18N / "done"
    for l in LANGS:
        mem = memory(l)
        added = rejected = 0
        for f in sorted(done.glob(f"{l}-*.json")):
            src = json.loads((I18N / "todo" / f.name).read_text()) if (I18N / "todo" / f.name).exists() else {}
            for k, v in json.loads(f.read_text()).items():
                if k in src and _tags(src[k]) != _tags(v):
                    rejected += 1
                    continue
                if re.search("[\u2013\u2014\u201c\u201d\u2018\u2019]", v):
                    v = v.replace("\u2014", ", ").replace("\u2013", " to ").replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")
                mem[k] = v
                added += 1
        (I18N / f"{l}.json").write_text(json.dumps(mem, ensure_ascii=False, indent=0, sort_keys=True))
        print(l, "added", added, "rejected", rejected, "memory", len(mem))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    {"build": build, "todo": todo, "merge": merge}[cmd]()
