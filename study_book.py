# -*- coding: utf-8 -*-
"""Brewing Fundamentals Study Book: the paid ₹1,999 study material (not a course), A4 PDF.

One chapter per topic of the 1-month Intensive Brewing Excellence Course, grouped by its four weeks,
from content/study_book/NN.json. Each chapter ends with check questions and a crossword; answers at the back.
The book is sold, so it is written outside the site (default ~/Downloads) and never into assets/.
Run: python3 study_book.py [out.pdf]
"""
import json
import pathlib
import subprocess
import sys
import tempfile

import fitz

from game_art import COPPER, icon
from games_crossword import grid_svg, solve
from make_games import CHROME, CSS, FONTS, HERE, LOGO, TEAL

TITLE = "Brewing Fundamentals Study Book"
OUT = pathlib.Path.home() / "Downloads/Brewing-Fundamentals-Study-Book.pdf"
WEEKS = [("Week one", "Brewing fundamentals", "barley", "Beer basics and the raw materials: malt, hops, water and yeast, then the beer styles they make."),
         ("Week two", "Brewhouse operations", "kettle", "Milling, mashing, lautering and the boil: turning grain into hopped, cooled wort."),
         ("Week three", "Fermentation and yeast management", "yeast", "Fermentation control, yeast care, maturation, filtration and carbonation."),
         ("Week four", "Quality control and grain to glass", "magnifier", "Hygiene and CIP, the lab, packaging, sensory evaluation and your own recipe.")]

BOOK_CSS = f"""<style>
@page{{size:A4;margin:16mm 17mm 20mm}}
@page full{{margin:0}}
.sheet{{page:full}}
.book{{padding:16mm 16mm 20mm}}
.chap{{break-before:page}}
.chap h1{{font-size:26pt;margin:1mm 0 2mm}}
.chap h2{{break-after:avoid}}
.lede{{font-size:11.5pt;color:#4a5a60;margin-bottom:4mm}}
.box{{background:#eef4f2;border-left:1.2mm solid #b8662f;border-radius:0 2mm 2mm 0;padding:3mm 5mm;margin:4mm 0;break-inside:avoid}}
.box h3{{font-family:"Alfa Slab One",serif;font-weight:400;font-size:11pt;color:{TEAL};margin-bottom:1.5mm}}
.box.warm{{background:#fbf3df}}
table.nums{{width:100%;border-collapse:collapse;font-size:9.5pt}}
table.nums td{{padding:1.3mm 2mm;border-bottom:.3mm solid #d8d2c4;vertical-align:top}}
table.nums td:first-child{{font-weight:700;width:45%}}
dl.terms{{display:grid;grid-template-columns:32mm 1fr;gap:1.2mm 4mm;font-size:9.5pt}}
dl.terms dt{{font-weight:700;color:#b8662f}}
.puzzle{{break-before:page;break-inside:avoid}}
.toc li{{display:flex;gap:2mm;font-size:10pt;margin-bottom:1.4mm}}
.toc li i{{flex:1;border-bottom:.3mm dotted #9aa5a9;margin-bottom:1.2mm}}
.ans p{{font-size:9.5pt;margin-bottom:1.6mm}}
</style>"""


def load():
    chapters = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((HERE / "content/study_book").glob("[0-9][0-9].json"))]
    assert [c["no"] for c in chapters] == list(range(1, len(chapters) + 1)), "chapter numbers must run 1, 2, 3..."
    for c in chapters:
        assert len(c["crossword"]) == 12 and len(c["check"]) == 5, c["title"]
        words = [dict(word=a.replace(" ", ""), clue=q, enum=",".join(str(len(p)) for p in a.split()) if " " in a else "")
                 for a, q in c["crossword"]]
        c["puzzle"] = solve(dict(title=c["title"], words=words))
    return chapters


def felt(body):
    return f'<section class="sheet book felt">{body}</section>'


def divider(kicker, title, sub, ic):
    return felt(f'<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:6mm">'
                f'<div style="width:34mm;height:34mm;border-radius:50%;background:{COPPER};display:flex;align-items:center;justify-content:center;'
                f'box-shadow:0 0 0 1.2mm #e9b949">{icon(ic, "20mm", "#fff8ec")}</div>'
                f'<div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:#e9b949">{kicker}</div>'
                f'<div class="badge"><b>{title}</b></div><p style="max-width:120mm;font-size:12pt">{sub}</p></div>')


def cover(n):
    return felt(f"""<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:7mm">
<img src="{LOGO}" alt="" style="height:34mm;filter:brightness(0) invert(1);opacity:.95">
<div style="font-size:11pt;letter-spacing:.22em;text-transform:uppercase;color:#e9b949">Study book</div>
<div class="badge"><b>Brewing Fundamentals</b><span>{n} chapters, {n} crosswords, every answer at the back</span></div>
<p style="max-width:135mm;font-size:12.5pt;line-height:1.6">Everything the 1-month Intensive Brewing Excellence Course covers,
written up as study notes you can work through at your own pace. From malt and water to fermentation, CIP, the lab, packaging and tasting.</p>
<p style="margin-top:14mm;font-size:10pt;color:#e9b949">craftbeerschool.in</p></div>""")


def back_cover(n):
    return felt(f"""<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8mm">
<div class="badge"><b>Brewing Fundamentals</b><span>Study book from Craft Beer School</span></div>
<p style="max-width:130mm;font-size:12pt;line-height:1.6">{n} chapters of study notes in the order of our four-week programme. Each one ends
with key numbers, the words to know, five questions to check yourself and a crossword. Made for brewing students, homebrewers,
new brewery staff and anyone preparing for a brewing exam.</p>
<img src="{LOGO}" alt="" style="height:22mm;filter:brightness(0) invert(1);opacity:.9">
<p style="font-size:10pt;color:#e9b949">craftbeerschool.in</p></div>""")


def title_page():
    return f"""<div style="height:255mm;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
<img src="{LOGO}" alt="" style="height:30mm;margin-bottom:10mm">
<div style="font-family:Alfa Slab One,serif;font-size:34pt;color:{TEAL};line-height:1.05">Brewing Fundamentals</div>
<p style="font-size:14pt;color:#b8662f;margin-top:4mm">Study book with crosswords</p>
<p style="margin-top:26mm;font-size:12pt">Ankur Napa</p><p style="font-size:10pt;color:#6b7a80">Craft Beer School</p>
<p style="margin-top:auto;font-size:8.5pt;color:#6b7a80">First edition, October 2026. craftbeerschool.in<br>
This is study material, not a course. It is for the buyer's own study: please do not copy, share or resell it.</p></div>"""


def howto_page(chapters):
    weeks = "".join(f"<li><b>{k}, {t}.</b> Chapters {', '.join(str(c['no']) for c in chapters if c['week'] == i + 1)}.</li>"
                    for i, (k, t, _, _) in enumerate(WEEKS))
    return f"""<div class="chap"><h1>How to use this book</h1>
<p>This book holds the full syllabus of our 1-month Intensive Brewing Excellence Course as study notes. It does not include
classes, lab sessions or brewery visits. If you want those, the course itself runs in person. This book is a good way to prepare for it.</p>
<h2>The four weeks</h2><ol>{weeks}</ol>
<h2>Each chapter</h2><ol>
<li>Starts with what you will be able to do by the end.</li>
<li>Teaches the topic in short sections with the numbers brewers actually use.</li>
<li>Ends with a table of key numbers, the words to know and five questions to check yourself.</li>
<li>Closes with a twelve-clue crossword on the same chapter.</li></ol>
<h2>A week at a time</h2><p>Read one chapter a day, answer the questions without looking back, then do the crossword the next
morning as a recap. Answers to both are at the back of the book.</p>
<h2>Units</h2><p>Temperatures are in °C with °F in brackets. Gravity is shown as specific gravity (1.048) with degrees Plato where it helps.
Spellings are British.</p></div>"""


def contents(chapters, pages):
    blocks = ""
    for i, (k, t, _, _) in enumerate(WEEKS):
        lis = "".join(f'<li><span>{c["no"]}. {c["title"]}</span><i></i><span>{pages.get(c["no"], "")}</span></li>'
                      for c in chapters if c["week"] == i + 1)
        blocks += f'<h2>{k}: {t}</h2><ul class="toc" style="list-style:none;padding:0">{lis}</ul>'
    tail = (f'<ul class="toc" style="list-style:none;padding:0;margin-top:5mm"><li><b>Answers</b><i></i>'
            f'<span>{pages.get("answers", "")}</span></li></ul>')
    return f'<div class="chap"><h1>Contents</h1>{blocks}{tail}</div>'


def chapter(c, total):
    goals = "".join(f"<li>{g}</li>" for g in c["goals"])
    secs = "".join(f"<h2>{h}</h2>{body}" for h, body in c["sections"])
    nums = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in c["numbers"])
    terms = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in c["terms"])
    checks = "".join(f"<li>{q}</li>" for q, _ in c["check"])
    p = c["puzzle"]
    clues = ""
    for head, items in p["clues"].items():
        lis = "".join(f'<li><b>{n}</b> {w["clue"]} ({w["enum"] or len(w["word"])})</li>' for n, w in items)
        clues += f'<div><h2 style="margin-top:0">{head}</h2><ul style="list-style:none;padding:0">{lis}</ul></div>'
    return f"""<div class="chap">
<div class="eyebrow">Chapter {c["no"]} of {total}</div><h1>{c["title"]}</h1><p class="lede">{c["intro"]}</p>
<div class="box"><h3>By the end of this chapter you can</h3><ul>{goals}</ul></div>
{secs}
<div class="box warm"><h3>Key numbers</h3><table class="nums">{nums}</table></div>
<div class="box"><h3>Words to know</h3><dl class="terms">{terms}</dl></div>
<div class="box warm"><h3>Check yourself</h3><ol>{checks}</ol></div>
</div>
<div class="puzzle"><div class="eyebrow">Crossword for chapter {c["no"]}</div><h1>{c["title"]}</h1>
<div style="display:flex;justify-content:center;margin-top:4mm">{grid_svg(p, 176, 132)}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8mm;margin-top:5mm">{clues}</div></div>"""


def answers(chapters):
    checks = "".join(f'<h2>{c["no"]}. {c["title"]}</h2>' + "".join(f"<p><b>{i + 1}.</b> {a}</p>" for i, (_, a) in enumerate(c["check"]))
                     for c in chapters)
    grids = ""
    for k in range(0, len(chapters), 6):
        tiles = "".join(f'<div style="break-inside:avoid"><div class="eyebrow">{c["no"]}. {c["title"]}</div>'
                        f'<div style="display:flex;justify-content:center">{grid_svg(c["puzzle"], 82, 68, answers=True)}</div></div>'
                        for c in chapters[k:k + 6])
        grids += f'<div class="chap"><h1 style="font-size:18pt">Crossword answers</h1><div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm 8mm;margin-top:3mm">{tiles}</div></div>'
    return f'<div class="chap ans"><div class="eyebrow">Answers</div><h1>Check yourself: answers</h1>{checks}</div>{grids}'


def notes():
    lines = "".join('<div style="border-bottom:.3mm solid #d8d2c4;height:9mm"></div>' for _ in range(26))
    return f'<div class="chap"><h1>Notes</h1>{lines}</div>'


def render(parts, pdf):
    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp) / "book.html"
        src.write_text(f"<!doctype html><html><head><meta charset='utf-8'>{FONTS}<style>{CSS}</style>{BOOK_CSS}</head>"
                       f"<body>{''.join(parts)}</body></html>", encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=20000",
                        f"--print-to-pdf={pdf}", src.as_uri()], check=True, capture_output=True)
    return fitz.open(pdf)


def build(chapters, pages, pdf, with_notes=False):
    n = len(chapters)
    parts = [cover(n), title_page(), howto_page(chapters), contents(chapters, pages)]
    for i, (k, t, ic, sub) in enumerate(WEEKS):
        parts.append(divider(k, t, sub, ic))
        parts += [chapter(c, n) for c in chapters if c["week"] == i + 1]
    parts.append(divider("The back of the book", "Answers", "Check your answers and your grids. Only after you have tried, of course.", "check"))
    parts.append(answers(chapters))
    if with_notes:
        parts.append(notes())
    parts.append(back_cover(n))
    return render(parts, pdf)


def find_pages(doc, chapters):
    pages = {}
    for i, pg in enumerate(doc):
        text = pg.get_text()
        for c in chapters:
            if c["no"] not in pages and f'Chapter {c["no"]} of {len(chapters)}' in text:
                pages[c["no"]] = i + 1
        if "answers" not in pages and "Check yourself: answers" in text:
            pages["answers"] = i + 1
    return pages


def is_felt(pg):
    px = pg.get_pixmap(clip=fitz.Rect(2, 2, 6, 6)).pixel(0, 0)
    return sum(px[:3]) < 300


def main():
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else OUT
    chapters = load()
    first = build(chapters, {}, out)
    pages = find_pages(first, chapters)
    first.close()
    doc = build(chapters, pages, out)
    if doc.page_count % 2:  # even page count for printing: add a notes page before the back cover
        doc.close()
        doc = build(chapters, pages, out, with_notes=True)
    assert find_pages(doc, chapters) == pages, "page numbers moved between passes"
    for i, pg in enumerate(doc):
        if is_felt(pg):
            continue
        y = pg.rect.height - 28
        pg.draw_line((48, y - 8), (pg.rect.width - 48, y - 8), color=(0.85, 0.82, 0.77), width=0.8)
        pg.insert_text((48, y + 4), f"{TITLE}, Craft Beer School", fontsize=7.5, color=(0.42, 0.48, 0.5))
        pg.insert_text((pg.rect.width - 60, y + 4), str(i + 1), fontsize=7.5, color=(0.42, 0.48, 0.5))
    doc.set_metadata({"title": TITLE, "author": "Ankur Napa", "subject": f"Brewing Fundamentals study notes and {len(chapters)} crosswords",
                      "creator": "Ankur Napa", "producer": "Craft Beer School"})
    doc.save(str(out) + ".tmp", garbage=3, deflate=True)
    doc.close()
    pathlib.Path(str(out) + ".tmp").replace(out)
    print(out, fitz.open(out).page_count, "pages,", len(chapters), "chapters")


if __name__ == "__main__":
    main()
