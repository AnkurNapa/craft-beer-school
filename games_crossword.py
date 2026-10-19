# -*- coding: utf-8 -*-
"""Beer Crosswords: a printable book of crosswords with answers, assets/games/beer-crosswords.pdf (A4).

Parts one to five: 50 topic puzzles from content/crosswords.txt. Part six, the course companion:
one puzzle per course lesson from content/crosswords_lessons_*.txt (course order, "### COURSE:" groups). Grids are laid out here: greedy placement over
many seeds, keeping the most compact grid that fits every word.
Run: python3 games_crossword.py
"""
import random

from game_art import COPPER, icon
from make_games import HERE, LOGO, TEAL, felt_board, write_pdf

GAME = "Beer Crosswords"
MAX_SIDE = 19
SEEDS = 400


def load(path="content/crosswords.txt"):
    puzzles, course, lesson = [], None, 0
    for line in (HERE / path).read_text(encoding="utf-8").splitlines():
        if line.startswith("### COURSE:"):
            course, lesson = line.split(":", 1)[1].strip(), 0
        elif line.startswith("## "):
            title, ic, intro = (s.strip() for s in line[3:].split("|"))
            lesson += 1
            puzzles.append(dict(title=title, icon=ic, intro=intro, words=[], course=course, lesson=lesson))
        elif "|" in line and not line.startswith("#"):
            ans, clue = (s.strip() for s in line.split("|", 1))
            parts = ans.split()
            puzzles[-1]["words"].append(dict(word="".join(parts), clue=clue,
                                             enum=",".join(str(len(p)) for p in parts)))
    return puzzles


def fits(grid, word, r, c, dr, dc):
    """Crossing count if word fits at (r, c) going (dr, dc), else None."""
    if grid.get((r - dr, c - dc)) or grid.get((r + dr * len(word), c + dc * len(word))):
        return None
    cross = 0
    for k, ch in enumerate(word):
        cell = (r + dr * k, c + dc * k)
        have = grid.get(cell)
        if have:
            if have[0] != ch or (dr, dc) in have[1]:
                return None
            cross += 1
        elif grid.get((cell[0] + dc, cell[1] + dr)) or grid.get((cell[0] - dc, cell[1] - dr)):
            return None
    return cross or None


def bounds(cells):
    rs, cs = [r for r, _ in cells], [c for _, c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def layout(words, seed):
    """Place every word or return None. grid: cell -> (letter, set of directions)."""
    rng = random.Random(seed)
    order = sorted(words, key=lambda w: (-len(w), rng.random()))
    grid, placed = {}, []

    def put(word, r, c, dr, dc):
        for k, ch in enumerate(word):
            cell = (r + dr * k, c + dc * k)
            grid[cell] = (ch, grid.get(cell, (ch, set()))[1] | {(dr, dc)})
        placed.append((word, r, c, dr, dc))

    put(order[0], 0, 0, 0, 1)
    todo = order[1:]
    while todo:
        progress = False
        for word in list(todo):
            options = []
            for (r0, c0), (ch0, _) in list(grid.items()):
                for i, ch in enumerate(word):
                    if ch != ch0:
                        continue
                    for dr, dc in ((0, 1), (1, 0)):
                        r, c = r0 - dr * i, c0 - dc * i
                        cross = fits(grid, word, r, c, dr, dc)
                        if cross is None:
                            continue
                        top, left, bot, right = bounds([*grid, (r, c), (r + dr * len(word), c + dc * len(word))])
                        h, w = bot - top + 1, right - left + 1
                        if max(h, w) > MAX_SIDE:
                            continue
                        options.append((cross * 4 - max(h, w) - abs(h - w) / 2 + rng.random(), r, c, dr, dc))
            if options:
                _, r, c, dr, dc = max(options)
                put(word, r, c, dr, dc)
                todo.remove(word)
                progress = True
        if not progress:
            return None
    top, left, bot, right = bounds(grid)
    return [(w, r - top, c - left, dr, dc) for w, r, c, dr, dc in placed], bot - top + 1, right - left + 1


def best_layout(words):
    tries = filter(None, (layout(words, s) for s in range(SEEDS)))
    return min(tries, key=lambda t: (max(t[1], t[2]), t[1] * t[2]))


def solve(p):
    placed, rows, cols = best_layout([w["word"] for w in p["words"]])
    letters = {}
    for word, r, c, dr, dc in placed:
        for k, ch in enumerate(word):
            assert letters.setdefault((r + dr * k, c + dc * k), ch) == ch, (p["title"], word)
    starts = sorted({(r, c) for _, r, c, _, _ in placed})
    num = {cell: i + 1 for i, cell in enumerate(starts)}
    info = {w["word"]: w for w in p["words"]}
    clues = {"Across": [], "Down": []}
    for word, r, c, dr, dc in placed:
        clues["Across" if dc else "Down"].append((num[(r, c)], info[word]))
    for k in clues:
        clues[k].sort(key=lambda t: t[0])
    return dict(p, letters=letters, num=num, rows=rows, cols=cols, clues=clues)


def grid_svg(s, width_mm, height_mm, answers=False):
    cell = min(width_mm / s["cols"], height_mm / s["rows"])
    w, h = cell * s["cols"], cell * s["rows"]
    out = []
    for (r, c), ch in s["letters"].items():
        x, y = c * cell, r * cell
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{cell:.2f}" height="{cell:.2f}" fill="#fff" stroke="{TEAL}" stroke-width="{cell * .045:.2f}"/>')
        if (r, c) in s["num"]:
            out.append(f'<text x="{x + cell * .08:.2f}" y="{y + cell * .3:.2f}" font-size="{cell * .27:.2f}" fill="#4a5a60">{s["num"][(r, c)]}</text>')
        if answers:
            out.append(f'<text x="{x + cell / 2:.2f}" y="{y + cell * .74:.2f}" font-size="{cell * .55:.2f}" text-anchor="middle" '
                       f'font-weight="700" fill="{COPPER}">{ch}</text>')
    pad = cell * .05
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad:.2f} {-pad:.2f} {w + 2 * pad:.2f} {h + 2 * pad:.2f}" '
            f'style="width:{w:.1f}mm;height:{h:.1f}mm;font-family:Hanken Grotesk,sans-serif">{"".join(out)}</svg>')


def clue_list(s):
    cols = ""
    for head, items in s["clues"].items():
        lis = "".join(f'<li><b>{n}</b> {w["clue"]} ({w["enum"] or len(w["word"])})</li>' for n, w in items)
        cols += f'<div><h2 style="margin-top:0">{head}</h2><ul style="list-style:none;padding:0">{lis}</ul></div>'
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8mm;margin-top:5mm">{cols}</div>'


PARTS = [
    ("Ingredients", "barley", "Malt, hops, yeast and water, plus the chemistry that binds them.",
     ["Malt basics", "Malt varieties", "Hops", "Hop varieties", "Hop farming", "Yeast", "Brewing water", "Adjuncts",
      "Brewing chemistry", "Recipe design"]),
    ("The brewhouse", "kettle", "From mash tun to bright tank, plus the plant that keeps it running.",
     ["Mashing", "The boil", "Brew day in order", "Brewhouse kit", "Fermentation", "Cellar and conditioning",
      "Cleaning and hygiene", "Utilities and the plant", "Brewing numbers", "Quality control"]),
    ("Beer styles", "star", "Lagers, ales, sours and everything brewed in between.",
     ["Lagers", "British ales", "Belgian beers", "Wheat beers", "Stouts and porters", "India pale ale", "Sour beers",
      "Farmhouse traditions", "Low and no alcohol", "Barrel ageing"]),
    ("In the glass", "glass", "Tasting, faults, serving and the food on the table.",
     ["Off-flavours", "Tasting and sensory", "Colour and clarity", "Foam and fizz", "Glassware", "Draught and serving",
      "Kegs, casks and bottles", "Packaging", "Beer and food", "Judging and competitions"]),
    ("People, places and history", "people", "Seven thousand years of beer, from Sumer to Bengaluru.",
     ["Beer history", "Beer in India", "Famous breweries", "American craft", "German beer words",
      "Festivals and culture", "Other fermented drinks", "The business of beer", "Homebrewing", "Schools and careers"]),
]
ORDINAL = ["One", "Two", "Three", "Four", "Five"]
BOOK_CSS = f"""<style>
.bfoot{{position:absolute;left:16mm;right:16mm;bottom:8mm;display:flex;justify-content:space-between;font-size:8pt;color:#6b7a80;
  border-top:.3mm solid #d8d2c4;padding-top:2mm}}
.felt .bfoot{{color:rgba(255,248,236,.7);border-color:rgba(233,185,73,.4)}}
.bhead{{font-size:8pt;letter-spacing:.08em;text-transform:uppercase;color:#b8662f;margin-bottom:5mm}}
.book{{padding:16mm 16mm 20mm}}
.toc li{{display:flex;gap:2mm;font-size:9.5pt;margin-bottom:1.2mm}}
.toc li i{{flex:1;border-bottom:.3mm dotted #9aa5a9;margin-bottom:1.2mm}}
</style>"""


def page(body, n=None, head="", felt=False):
    num = f'<span>{n}</span>' if n else "<span></span>"
    foot = f'<div class="bfoot"><span>Beer Crosswords, Craft Beer School</span>{num}</div>' if n else ""
    top = f'<div class="bhead">{head}</div>' if head else ""
    return f'<section class="sheet book{" felt" if felt else ""}">{top}{body}{foot}</section>'


COMPANION = ("Course companion", "pencil", "One crossword for every lesson of every Craft Beer School course, to use as a recap.")


def puzzle_page(i, s, n, head):
    kicker = f"Crossword {i}" + (f'. {s["course"]}, lesson {s["lesson"]}' if s.get("course") else "")
    body = (f'<div class="eyebrow">{kicker}</div><h1>{s["title"]}</h1>'
            f'<p style="margin:1mm 0 4mm;color:#4a5a60">{s["intro"]}</p>'
            f'<div style="display:flex;justify-content:center">{grid_svg(s, 178, 136)}</div>{clue_list(s)}')
    return page(body, n, head)


def answer_page(chunk, first, n):
    tiles = "".join(f'<div><div class="eyebrow">{first + k}. {s["title"]} <span style="color:#6b7a80;font-weight:400">'
                    f'(page {s["page"]})</span></div><div style="display:flex;justify-content:center">'
                    f'{grid_svg(s, 84, 70, answers=True)}</div></div>' for k, s in enumerate(chunk))
    return page(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm 8mm">{tiles}</div>', n,
                f"Answers {first} to {first + len(chunk) - 1}")


def divider(kicker, title, sub, ic, items=""):
    body = (f'<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:6mm">'
            f'<div style="width:34mm;height:34mm;border-radius:50%;background:{COPPER};display:flex;align-items:center;justify-content:center;'
            f'box-shadow:0 0 0 1.2mm #e9b949">{icon(ic, "20mm", "#fff8ec")}</div>'
            f'<div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:#e9b949">{kicker}</div>'
            f'<div class="badge"><b>{title}</b></div><p style="max-width:120mm;font-size:12pt">{sub}</p>{items}</div>')
    return page(body, felt=True)


def title_page(total):
    return page(f"""<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
<img src="{LOGO}" alt="" style="height:30mm;margin-bottom:10mm">
<div style="font-family:Alfa Slab One,serif;font-size:40pt;color:{TEAL};line-height:1">Beer Crosswords</div>
<p style="font-size:14pt;color:#b8662f;margin-top:4mm">{total} puzzles for brewers and beer lovers</p>
<p style="margin-top:30mm;font-size:12pt">Ankur Napa</p><p style="font-size:10pt;color:#6b7a80">Craft Beer School, Bengaluru</p>
<p style="margin-top:auto;font-size:8.5pt;color:#6b7a80">First edition, October 2026. craftbeerschool.in<br>
Free to print and share for teaching. Please do not sell it.</p></div>""")


def howto_page(n, total, lessons, courses):
    return page(f"""<h1>How to use this book</h1>
<p style="margin-top:3mm">There are {total} crosswords here. The first 50 cover every corner of brewing in five parts:
ingredients, the brewhouse, beer styles, what happens in the glass and the people, places and history behind it all.
Part six is the course companion: {lessons} more puzzles, one for each lesson of the {courses} Craft Beer School courses.
Each puzzle has twelve clues and fits on a single page, so you can print just the one you need.</p>
<h2>Reading the clues</h2><ol>
<li>The number in brackets is the length of the answer. Two numbers, such as (3,3), mean two words written together in the grid.</li>
<li>A ___ in a clue stands for the missing answer.</li>
<li>Spellings are British, temperatures are in °C with °F in brackets and umlauts are dropped in the grid, so Märzen is MARZEN.</li></ol>
<h2>In the classroom or the taproom</h2><ol>
<li>Hand out the course companion puzzle at the end of each lesson as a ten-minute recap.</li>
<li>Race in teams: the first team with a full, correct grid wins the round.</li>
<li>Read one clue aloud at a tasting and let the table shout the answer.</li></ol>
<h2>Answers</h2><p>Every grid is solved at the back of the book, six to a page, with the page number of its puzzle.
Try not to peek.</p>""", n, "Before you start")


def toc(items):
    lis = "".join(f'<li><span>{s["no"]}. {s["title"]}</span><i></i><span>{s["page"]}</span></li>' for s in items)
    return f'<ul class="toc" style="list-style:none;padding:0">{lis}</ul>'


def contents_pages(parts, companion, answers_at, n):
    cols = "".join(f'<div style="break-inside:avoid;margin-bottom:4mm"><h2 style="margin-top:0">Part {ORDINAL[k].lower()}: {name}</h2>'
                   f'{toc(items)}</div>' for k, (name, _, _, items, _) in enumerate(parts))
    cols += (f'<div style="break-inside:avoid;margin-bottom:4mm"><h2 style="margin-top:0">Part six: {COMPANION[0]}</h2>'
             f'<ul class="toc" style="list-style:none;padding:0"><li><span>{len(companion)} lesson puzzles, listed overleaf</span><i></i>'
             f'<span>{companion[0]["page"] - 1}</span></li></ul></div>'
             f'<ul class="toc" style="list-style:none;padding:0"><li><b>Answers</b><i></i><span>{answers_at}</span></li></ul>')
    first = page(f'<h1 style="margin-bottom:5mm">Contents</h1><div style="columns:2;column-gap:10mm">{cols}</div>', n)
    courses = list(dict.fromkeys(s["course"] for s in companion))
    groups = "".join(f'<div style="break-inside:avoid;margin-bottom:3mm"><h2 style="margin:0 0 1mm;font-size:10.5pt">{c}</h2>'
                     f'{toc([s for s in companion if s["course"] == c])}</div>' for c in courses)
    second = page(f'<div style="columns:2;column-gap:10mm;font-size:9pt">{groups}</div>', n + 1, f"Contents, part six: {COMPANION[0]}")
    return [first, second]


def back_cover(total):
    body = f"""<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8mm">
<div class="badge"><b>Beer Crosswords</b><span>{total} puzzles from Craft Beer School</span></div>
<p style="max-width:130mm;font-size:12pt;line-height:1.6">Malt and hops, mash tuns and foeders, Helles and handia. {total} crosswords
that test what you know about beer, from the barley field to the bar, plus one for every lesson of every Craft Beer School
course. Every answer is at the back. Made for brewing students, homebrewers, taproom teams and anyone who likes a pint and a pencil.</p>
<img src="{LOGO}" alt="" style="height:22mm;filter:brightness(0) invert(1);opacity:.9">
<p style="font-size:10pt;color:#e9b949">craftbeerschool.in</p></div>"""
    return page(body, felt=True)


def notes_page(n):
    lines = "".join('<div style="border-bottom:.3mm solid #d8d2c4;height:9mm"></div>' for _ in range(24))
    return page(f"<h1>Notes</h1>{lines}", n)


def main():
    by_title = {p["title"]: p for p in load()}
    assert sorted(by_title) == sorted(t for *_, ts in PARTS for t in ts), "PARTS must list every puzzle once"
    lessons = [p for f in sorted(HERE.glob("content/crosswords_lessons_*.txt")) for p in load(str(f.relative_to(HERE)))]
    # physical pages: 1 cover, 2 title, 3 how to, 4 and 5 contents, then a divider before each part
    no, pg, parts = 0, 6, []
    for name, ic, sub, titles in PARTS:
        items = []
        divider_at, pg = pg, pg + 1
        for t in titles:
            no += 1
            items.append(dict(solve(by_title[t]), no=no, page=pg))
            pg += 1
        parts.append((name, ic, sub, items, divider_at))
    pg += 1  # course companion divider
    companion = []
    for p in lessons:
        no += 1
        companion.append(dict(solve(p), no=no, page=pg))
        pg += 1
    answers_at = pg
    solved = [s for *_, items, _ in parts for s in items] + companion
    total, courses = len(solved), len({s["course"] for s in companion})
    assert len(solved) == 50 + len(lessons) and all(len(s["words"]) == 12 for s in solved)

    sheets = [felt_board(GAME, f"{total} puzzles for brewers and beer lovers",
                         f'<div style="background:#fbf3df;padding:4mm">{grid_svg(solved[0], 140, 125, answers=True)}</div>',
                         "Malt, hops, yeast, lagers, sours, the brewhouse, the bar and India's own beer story, plus a puzzle "
                         "for every Craft Beer School lesson, with answers at the back."),
              title_page(total), howto_page(3, total, len(companion), courses), *contents_pages(parts, companion, answers_at, 4)]
    for k, (name, ic, sub, items, at) in enumerate(parts):
        listing = f'<p style="font-size:10pt;opacity:.85;max-width:140mm">{", ".join(s["title"] for s in items)}</p>'
        sheets.append(divider(f"Part {ORDINAL[k].lower()}", name, sub, ic, listing))
        sheets += [puzzle_page(s["no"], s, s["page"], f"Part {ORDINAL[k].lower()}: {name}") for s in items]
    course_list = ", ".join(dict.fromkeys(s["course"] for s in companion))
    sheets.append(divider("Part six", COMPANION[0], COMPANION[2], COMPANION[1],
                          f'<p style="font-size:10pt;opacity:.85;max-width:150mm">{course_list}</p>'))
    sheets += [puzzle_page(s["no"], s, s["page"], f"Part six: {s['course']}") for s in companion]
    sheets.append(divider("The back of the book", "Answers", "Every grid, solved. Only for checking, of course.", "check"))
    sheets += [answer_page(solved[i:i + 6], i + 1, answers_at + 1 + i // 6) for i in range(0, total, 6)]
    if len(sheets) % 2 == 0:  # with the back cover added the total must be even
        sheets.append(notes_page(len(sheets) + 1))
    sheets.append(back_cover(total))
    write_pdf("beer-crosswords", [BOOK_CSS, *sheets])
    pdf = HERE / "assets/games/beer-crosswords.pdf"
    import fitz
    doc = fitz.open(pdf)
    doc.set_metadata({"title": "Beer Crosswords", "author": "Ankur Napa", "subject": f"{total} beer crosswords from Craft Beer School",
                      "creator": "Ankur Napa", "producer": "Craft Beer School"})
    doc.saveIncr()
    print(doc.page_count, "pages,", total, "puzzles")


if __name__ == "__main__":
    main()
