#!/usr/bin/env python3
"""CTA invariants for the built site. Run: python3 test_ctas.py

Guards the things that silently break a conversion path: a dead anchor, an
enrol button that lands on the page top instead of the form, a course card
that forgets which course it was selling, or a contact form with no way out.
"""
import pathlib
import re
import sys

# Public, indexable pages only. The admin surface is deliberately noindex and
# carries no marketing metadata, and *_template.html files are build inputs.
def _is_public(path, html):
    return not path.name.endswith("_template.html") and "noindex" not in html


HTML = sorted(pathlib.Path(__file__).parent.glob("*.html"))
PAGES = {p.name: t for p in HTML if _is_public(p, (t := p.read_text()))}
assert PAGES, "no built HTML found, run build.py first"


def fail(msg):
    print("FAIL:", msg)
    return 1


errors = 0

# 1. No dead anchors anywhere. href="#" is a CTA that does nothing.
for name, html in PAGES.items():
    dead = html.count('href="#"')
    if dead:
        errors += fail(f"{name} has {dead} dead href=\"#\" link(s)")

# 2. Every page offers an enrol path that lands on the form itself.
for name, html in PAGES.items():
    if "contact.html#enroll" not in html and 'id="enroll"' not in html:
        errors += fail(f"{name} has no enrol CTA pointing at the form")

# 3. Every page offers a WhatsApp path (the highest-intent channel for India).
for name, html in PAGES.items():
    if "wa.me/" not in html:
        errors += fail(f"{name} has no WhatsApp CTA")

# 4. Course cards must carry their course into the form, otherwise the user
#    lands on a blank select and has to remember what they clicked.
courses = PAGES["courses.html"]
card_enrols = re.findall(r'href="contact\.html\?course=([^"#]+)#enroll"', courses)
if len(card_enrols) < 6:
    errors += fail(f"courses.html: only {len(card_enrols)} course-aware enrol links, expected >= 6")

# 5. Whatever a card passes must actually exist as an option in the form.
options = set(
    re.sub(r"\s+", " ", o).strip()
    for o in re.findall(r"<option[^>]*>([^<]*)</option>", PAGES["contact.html"])
)
options = {o.replace("&amp;", "&") for o in options}
for raw in set(card_enrols):
    from urllib.parse import unquote_plus
    want = unquote_plus(raw)
    if want not in options:
        errors += fail(f'course "{want}" has no matching <option> in the contact form')

# 6. The form must never dead-end: either a live endpoint or a mail fallback.
contact = PAGES["contact.html"]
if 'FORMSPREE_ID="YOUR_FORM_ID"' in contact and "mailto:" not in contact:
    errors += fail("contact form has no endpoint AND no mailto fallback")

# 7. Every CTA is labelled so click-through can be measured. Plain nav and
#    footer menu entries are navigation, not CTAs, so only styled buttons and
#    arrow links are in scope.
for name, html in PAGES.items():
    for tag in re.findall(r'<a href="contact\.html[^"]*"[^>]*>', html):
        is_cta = re.search(r'class="[^"]*(btn|link-arrow|nav-cta)', tag)
        if is_cta and "data-cta" not in tag:
            errors += fail(f"{name}: CTA missing data-cta -> {tag}")

if errors:
    print(f"\n{errors} CTA check(s) failed")
    sys.exit(1)
print(f"All CTA checks passed across {len(PAGES)} pages.")
