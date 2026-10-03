# -*- coding: utf-8 -*-
"""Print-and-play beer board games: assets/games/*.pdf (A4).

  brew-ludo.pdf                    Malt, Hops, Yeast and Water race to the glass
  grain-to-glass-snakes-ladders.pdf  good habits climb, brewing faults slide
  brewery-tycoon.pdf               property trading with taprooms across India

Each pack is self-contained: board, rules, cut-out pieces and a fold-up die.
Run: python3 make_games.py  (also builds games_party.py and games_strategy.py)
"""
import math
import pathlib
import subprocess

from game_art import ART_CSS, COPPER, FOAM, backs, board_page, gcard, icon, side_strip, svg_icon

HERE = pathlib.Path(__file__).parent
OUT = HERE / "assets/games"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOGO = (HERE / "assets/logo.png").resolve().as_uri()

TEAL, AMBER, GOLD, GREEN, BLUE, CREAM = "#123c4a", "#d9862a", "#f3c34d", "#2f8f5f", "#0a6d84", "#fbf3df"

CSS = f"""
@page{{size:A4;margin:0}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:"Hanken Grotesk",sans-serif;color:#1d2b30;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.sheet{{width:210mm;height:297mm;padding:12mm;position:relative;page-break-after:always;overflow:hidden}}
.sheet:last-child{{page-break-after:auto}}
h1{{font-family:"Alfa Slab One",serif;font-weight:400;font-size:24pt;color:{TEAL};line-height:1.1}}
h2{{font-family:"Alfa Slab One",serif;font-weight:400;font-size:13pt;color:#b8662f;margin:5mm 0 2mm}}
.eyebrow{{font-size:9pt;font-weight:700;color:#b8662f;margin-bottom:2mm}}
p,li{{font-size:10pt;line-height:1.45}}
ol,ul{{padding-left:5mm}}
li{{margin-bottom:1.4mm}}
.foot{{position:absolute;left:12mm;right:12mm;bottom:7mm;display:flex;justify-content:space-between;align-items:center;font-size:7.5pt;color:#6b7a80}}
.foot img{{height:9mm}}
.cut{{border:.3mm dashed #9aa5a9}}
.grid{{display:grid;gap:3mm}}
.note{{background:#eef4f2;border-left:1.2mm solid #b8662f;border-radius:0 2mm 2mm 0;padding:3mm 4mm;margin-top:4mm;font-size:9.5pt}}
""" + ART_CSS
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One'
         '&family=Hanken+Grotesk:wght@400;600;700&display=block" rel="stylesheet">')
# game -> (emblem icon, players, minutes) for the rules page side strip
META = {"Brew Ludo": ("glass", "2 to 4 players", "30 minutes"),
        "Grain to Glass Snakes and Ladders": ("barley", "2 to 6 players", "20 minutes"),
        "Brewery Tycoon": ("kettle", "2 to 6 players", "90 minutes"),
        "Beer Style Bingo": ("star", "3 to 12 players", "20 minutes"),
        "Hop and Style Trumps": ("hop", "2 to 6 players", "15 minutes"),
        "Pairing Dominoes": ("plate", "2 to 4 players", "20 minutes"),
        "Brewery Quiz Trail": ("question", "2 to 6 players", "45 minutes"),
        "Off-Flavour Detective": ("magnifier", "3 to 6 players", "45 minutes"),
        "Brew Day Dash": ("flame", "2 to 5 players", "20 minutes"),
        "Tank Planner": ("tank", "1 to 4 players", "40 minutes")}


def foot(game):
    return (f'<div class="foot"><span><img src="{LOGO}" alt="" style="vertical-align:middle;margin-right:2mm">'
            f'{game}, a free print-and-play game from Craft Beer School</span><span>craftbeerschool.in</span></div>')


def sheet(game, body, felt=False):
    return f'<section class="sheet{" felt" if felt else ""}">{body}{foot(game)}</section>'


def rules_sheet(game, body):
    emblem, players, minutes = META[game]
    return f'<section class="sheet">{side_strip(game, emblem, players, minutes)}<div class="ruled">{body}</div>{foot(game)}</section>'


TITLES = {"Grain to Glass Snakes and Ladders": ("Grain to Glass", "Snakes and ladders for brewers")}


def felt_board(game, sub, board, intro):
    emblem, players, minutes = META[game]
    title, tag = TITLES.get(game, (game, ""))
    chips = (("check", players), ("clock", minutes), ("star", "Ages 12+"), (emblem, "Free from Craft Beer School"))
    return sheet(game, board_page(title, tag or sub, board, intro, chips), felt=True)


def write_pdf(name, sheets):
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / f"_{name}.html"
    tmp.write_text(f"<!doctype html><html><head><meta charset='utf-8'>{FONTS}<style>{CSS}</style></head><body>{''.join(sheets)}</body></html>", encoding="utf-8")
    pdf = OUT / f"{name}.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=15000",
                    f"--print-to-pdf={pdf}", tmp.resolve().as_uri()], check=True, capture_output=True)
    tmp.unlink()
    print("wrote", pdf.relative_to(HERE))


# ---------------------------------------------------------------- shared pieces
PIPS = {1: [(1, 1)], 2: [(0, 0), (2, 2)], 3: [(0, 0), (1, 1), (2, 2)], 4: [(0, 0), (2, 0), (0, 2), (2, 2)],
        5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)], 6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]}


def die_net(size=22):
    """Cross-shaped cube net (mm) with glue tabs; opposite faces add to 7."""
    faces = {(1, 0): 2, (0, 1): 3, (1, 1): 1, (2, 1): 4, (1, 2): 5, (1, 3): 6}
    s = size
    out = []
    for (cx, cy), n in faces.items():
        x, y = cx * s, cy * s
        out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="#fff" stroke="#333" stroke-width=".3"/>')
        for px, py in PIPS[n]:
            out.append(f'<circle cx="{x + s * (.25 + .25 * px)}" cy="{y + s * (.25 + .25 * py)}" r="{s * .08}" fill="{TEAL if n != 1 else AMBER}"/>')
    tabs = [(0, 1, "up"), (2, 1, "up"), (0, 1, "down"), (2, 1, "down"), (1, 3, "left"), (1, 3, "right"), (1, 0, "left")]
    t = s * .22
    for cx, cy, side in tabs:
        x, y = cx * s, cy * s
        pts = {"up": [(x, y), (x + t, y - t), (x + s - t, y - t), (x + s, y)],
               "down": [(x, y + s), (x + t, y + s + t), (x + s - t, y + s + t), (x + s, y + s)],
               "left": [(x, y), (x - t, y + t), (x - t, y + s - t), (x, y + s)],
               "right": [(x + s, y), (x + s + t, y + t), (x + s + t, y + s - t), (x + s, y + s)]}[side]
        out.append(f'<polygon points="{" ".join(f"{a},{b}" for a, b in pts)}" fill="#eee" stroke="#999" stroke-width=".3" stroke-dasharray="1 .8"/>')
    return (f'<svg width="{3 * s + 2 * t}mm" height="{4 * s + 2 * t}mm" viewBox="{-t} {-t} {3 * s + 2 * t} {4 * s + 2 * t}">'
            + "".join(out) + "</svg>")


def cap(colour, letter, mm=18):
    """Crown bottle cap token with a crimped edge."""
    pts = []
    for i in range(42):
        a = i * math.pi / 21
        r = 50 if i % 2 == 0 else 45
        pts.append(f"{50 + r * math.cos(a):.1f},{50 + r * math.sin(a):.1f}")
    return (f'<svg width="{mm}mm" height="{mm}mm" viewBox="0 0 100 100"><polygon points="{" ".join(pts)}" fill="{colour}" stroke="#333" stroke-width="1.2"/>'
            f'<circle cx="50" cy="50" r="33" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="3"/>'
            f'<text x="50" y="62" text-anchor="middle" font-family="Alfa Slab One,serif" font-size="34" fill="#fff">{letter}</text></svg>')


def pieces_sheet(game, teams, per_team, extra=""):
    caps = "".join(f'<div style="text-align:center"><div style="display:flex;gap:2mm;justify-content:center">'
                   f'{"".join(cap(c, l) for _ in range(per_team))}</div><p style="font-size:8.5pt;margin-top:1mm">{name}</p></div>'
                   for name, c, l in teams)
    return sheet(game, f"""<div class="eyebrow">Cut out</div><h1>Pieces and die</h1>
<p style="margin-top:2mm">Print on thick paper or card. Cut out the caps and glue each onto a coin or a real bottle cap so it sits flat.
Fold the die along the lines and glue the grey tabs inside. Or just use any die you have.</p>
<div class="grid" style="grid-template-columns:repeat({2 if len(teams) <= 4 else 3},1fr);margin-top:6mm;row-gap:6mm">{caps}</div>
{extra}
<div style="display:flex;gap:10mm;margin-top:6mm;align-items:flex-start">{die_net()}{die_net()}</div>""")


# ---------------------------------------------------------------- Brew Ludo
LUDO_TEAMS = [("Malt", AMBER, "M"), ("Hops", GREEN, "H"), ("Yeast", GOLD, "Y"), ("Water", BLUE, "W")]
LUDO_ICON = {"Malt": "barley", "Hops": "hop", "Yeast": "yeast", "Water": "drop"}


def ludo_path():
    p = [(6, c) for c in range(1, 6)] + [(r, 6) for r in range(5, -1, -1)] + [(0, 7), (0, 8)]
    p += [(r, 8) for r in range(1, 6)] + [(6, c) for c in range(9, 15)] + [(7, 14), (8, 14)]
    p += [(8, c) for c in range(13, 8, -1)] + [(r, 8) for r in range(9, 15)] + [(14, 7), (14, 6)]
    p += [(r, 6) for r in range(13, 8, -1)] + [(8, c) for c in range(5, -1, -1)] + [(7, 0), (6, 0)]
    assert len(p) == 52 and len(set(p)) == 52
    return p


def ludo_board():
    path = ludo_path()
    starts = {0: AMBER, 13: GREEN, 26: GOLD, 39: BLUE}
    safe = {8, 21, 34, 47}
    lanes = {AMBER: [(7, c) for c in range(1, 6)], GREEN: [(r, 7) for r in range(1, 6)],
             GOLD: [(7, c) for c in range(9, 14)], BLUE: [(r, 7) for r in range(9, 14)]}
    out = []
    for i, (r, c) in enumerate(path):
        fill = starts.get(i, "#fffaf0")
        out.append(f'<rect x="{c}" y="{r}" width="1" height="1" fill="{fill}" stroke="#333" stroke-width=".03"/>')
        if i in safe:
            out.append(f'<text x="{c + .5}" y="{r + .62}" text-anchor="middle" font-size=".5" fill="{AMBER}">&#9733;</text>'
                       f'<text x="{c + .5}" y="{r + .9}" text-anchor="middle" font-size=".17" font-family="Hanken Grotesk" font-weight="700" fill="#555">TAP</text>')
        if i in starts:
            out.append(f'<text x="{c + .5}" y="{r + .68}" text-anchor="middle" font-size=".42" fill="#fff" font-weight="700">GO</text>')
    for colour, cells in lanes.items():
        out += [f'<rect x="{c}" y="{r}" width="1" height="1" fill="{colour}" stroke="#333" stroke-width=".03"/>' for r, c in cells]
    bases = [(0, 0, LUDO_TEAMS[0]), (9, 0, LUDO_TEAMS[1]), (9, 9, LUDO_TEAMS[2]), (0, 9, LUDO_TEAMS[3])]
    for x, y, (name, colour, _) in bases:
        out.append(f'<rect x="{x}" y="{y}" width="6" height="6" fill="{colour}" stroke="#333" stroke-width=".04"/>'
                   f'<rect x="{x + 1}" y="{y + 1}" width="4" height="4" rx=".3" fill="#fff"/>')
        for dx, dy in [(1.75, 1.75), (4.25, 1.75), (1.75, 4.25), (4.25, 4.25)]:
            out.append(f'<circle cx="{x + dx}" cy="{y + dy}" r=".5" fill="{colour}" fill-opacity=".18" stroke="{colour}" stroke-width=".09"/>')
        out.append(svg_icon(LUDO_ICON[name], x + 2.1, y + 2.1, 1.8, colour, 3.2))
        out.append(f'<text x="{x + 3}" y="{y + .72}" text-anchor="middle" font-size=".52" font-family="Alfa Slab One" fill="#fff">{name}</text>')
    tri = {AMBER: "6,6 6,9 7.5,7.5", GREEN: "6,6 9,6 7.5,7.5", GOLD: "9,6 9,9 7.5,7.5", BLUE: "6,9 9,9 7.5,7.5"}
    out += [f'<polygon points="{p}" fill="{c}" stroke="#333" stroke-width=".03"/>' for c, p in tri.items()]
    out.append(f'<circle cx="7.5" cy="7.5" r=".72" fill="#fff" stroke="{COPPER}" stroke-width=".08"/>' + svg_icon("glass", 6.98, 6.95, 1.04, COPPER, 3.4))
    return f'<svg width="174mm" height="174mm" viewBox="0 0 15 15" style="background:#fff">{"".join(out)}</svg>'


def make_ludo():
    g = "Brew Ludo"
    board = felt_board(g, "2 to 4 players", f"{ludo_board()}",
                       "Four ingredients race to the glass. Malt, Hops, Yeast and Water each need to get home before the beer is brewed.")
    rules = rules_sheet(g, f"""<div class="eyebrow">How to play</div><h1>Rules</h1>
<h2>Set up</h2><ol><li>Each player picks an ingredient and puts its four caps in their store, the big coloured corner.</li>
<li>Everyone rolls. The highest roll goes first, then play passes clockwise.</li></ol>
<h2>On your turn</h2><ol>
<li>Roll a 6 to move a cap out of your store onto your GO square.</li>
<li>Move one cap clockwise by the number you roll. If no cap can move, your turn ends.</li>
<li>A 6 gives you another roll. Three 6s in a row and the batch boils over: your turn ends at once.</li>
<li>Land exactly on another player's cap and it is a spoiled batch: that cap goes back to its store.</li>
<li>Star squares are taprooms. Caps on a taproom are safe and cannot be sent home.</li>
<li>Two of your own caps on one square form a blend. Nobody can land on or pass a blend.</li></ol>
<h2>Getting home</h2><ol>
<li>After one full lap, turn into your own coloured lane towards the glass.</li>
<li>You need the exact number to reach the glass. Too high and the cap stays put.</li>
<li>The first player with all four caps in the glass wins the round of beers.</li></ol>
<div class="note"><b>Know your ingredients.</b> Malt gives the sugar, body and colour. Hops give bitterness and aroma. Yeast turns sugar into alcohol and carbon dioxide. Water is more than 90 per cent of every beer, so its minerals matter.</div>
<div class="note"><b>Brewer's rule (optional).</b> Roll a 1 while on a taproom and you may tell a beer fact. If the table agrees it is true, roll again.</div>""")
    write_pdf("brew-ludo", [board, rules, pieces_sheet(g, LUDO_TEAMS, 4)])


# ---------------------------------------------------------------- Snakes and ladders
LADDERS = [(4, 25, "Sanitised", "Sanitised everything", "Clean, then sanitise every surface that touches cold wort."),
           (9, 31, "Calibrated", "Calibrated the thermometer", "A thermometer two degrees out changes your whole mash."),
           (21, 42, "Healthy yeast", "Pitched healthy yeast", "Enough fresh yeast gives a fast and clean start."),
           (28, 56, "Temp control", "Controlled fermentation temperature", "Steady temperature keeps esters and fusel alcohols in check."),
           (36, 57, "Gravity check", "Took gravity readings", "The hydrometer, not the calendar, tells you fermentation is done."),
           (51, 72, "Brew log", "Kept a brew log", "Write it down so you can repeat a good batch or fix a bad one."),
           (62, 83, "CO2 purge", "Purged kegs with CO2", "Oxygen is the enemy of finished beer."),
           (71, 92, "Sensory panel", "Ran a sensory panel", "Trained tasters catch faults before customers do.")]
SNAKES = [(17, 7, "No sanitising", "Skipped sanitising", "Bacteria and wild yeast love a lazy brewer."),
          (32, 10, "Stuck mash", "Stuck mash", "Too fine a crush or too much wheat stops the run-off."),
          (48, 26, "Mash too hot", "Mashed too hot", "Beta-amylase dies early, leaving a sweet and heavy beer."),
          (54, 34, "Rushed rest", "Rushed the diacetyl rest", "Packaging too early leaves a buttery off-flavour."),
          (87, 24, "Infection", "Infected batch", "One dirty valve can sour a whole tank."),
          (93, 73, "Oxidised", "Oxidised in packaging", "Oxygen pickup turns fresh hops to cardboard within weeks."),
          (95, 75, "Clear glass", "Clear glass bottles", "Sunlight plus hops makes skunky beer in minutes."),
          (98, 79, "Over-primed", "Over-primed bottles", "Too much priming sugar means gushers or even bottle bombs.")]


SL_ICON = {1: "barley", 100: "glass", 4: "drop", 9: "thermo", 21: "yeast", 28: "snow", 36: "magnifier", 51: "pencil",
           62: "keg", 71: "glass", 17: "bug", 32: "kettle", 48: "flame", 54: "clock", 87: "bug", 93: "box", 95: "sun", 98: "bottle"}


def sl_centre(n):
    r, k = divmod(n - 1, 10)
    c = k if r % 2 == 0 else 9 - k
    return c + .5, 9 - r + .5


def sl_board():
    out, text, labels = [], [], {a: s for a, _, s, *_ in LADDERS} | {a: s for a, _, s, *_ in SNAKES}
    halo = 'stroke="#fffaf0" stroke-width=".045" paint-order="stroke" stroke-linejoin="round"'
    labels |= {1: "Grain", 100: "Glass!"}
    shades = ["#fbf3df", "#f6e3b4"]
    for n in range(1, 101):
        x, y = sl_centre(n)
        out.append(f'<rect x="{x - .5}" y="{y - .5}" width="1" height="1" fill="{shades[n % 2]}" stroke="#c9b48a" stroke-width=".015"/>')
        text.append(f'<text x="{x - .42}" y="{y - .28}" font-size=".2" font-weight="700" fill="{TEAL}" {halo}>{n}</text>')
        if n in SL_ICON:
            out.append(svg_icon(SL_ICON[n], x - .19, y - .2, .38, "#8a6a3a", 3))
        if n in labels:
            text.append(f'<text x="{x}" y="{y + .4}" text-anchor="middle" font-size=".12" font-weight="700" fill="#5a4a2a" {halo}>{labels[n]}</text>')
    for a, b, *_ in LADDERS:
        (x1, y1), (x2, y2) = sl_centre(a), sl_centre(b)
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        nx, ny = -dy / L * .13, dx / L * .13
        for s in (1, -1):
            out.append(f'<line x1="{x1 + s * nx}" y1="{y1 + s * ny}" x2="{x2 + s * nx}" y2="{y2 + s * ny}" stroke="#8b5a2b" stroke-width=".07" stroke-linecap="round"/>')
        steps = max(2, int(L / .3))
        for i in range(1, steps):
            t = i / steps
            px, py = x1 + dx * t, y1 + dy * t
            out.append(f'<line x1="{px + nx}" y1="{py + ny}" x2="{px - nx}" y2="{py - ny}" stroke="#c08a4a" stroke-width=".05"/>')
    for k, (a, b, *_) in enumerate(SNAKES):
        dark, light = [("#7a2418", "#c0503a"), ("#3f5a1e", "#7fa046"), ("#4b2a5a", "#8d5aa6")][k % 3]
        (x1, y1), (x2, y2) = sl_centre(a), sl_centre(b)
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        waves = max(1.5, L / 1.6)
        pts = []
        for i in range(61):
            t = i / 60
            w = math.sin(t * math.pi * 2 * waves) * .28 * (1 - t * .5)
            pts.append(f"{x1 + dx * t + nx * w:.3f},{y1 + dy * t + ny * w:.3f}")
        pl = " ".join(pts)
        out.append(f'<polyline points="{pl}" fill="none" stroke="{dark}" stroke-width=".2" stroke-linecap="round" stroke-linejoin="round"/>'
                   f'<polyline points="{pl}" fill="none" stroke="{light}" stroke-width=".13" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray=".12 .08"/>'
                   f'<circle cx="{x1}" cy="{y1}" r=".17" fill="{dark}"/>'
                   f'<circle cx="{x1 - .06}" cy="{y1 - .04}" r=".035" fill="#fff"/><circle cx="{x1 + .06}" cy="{y1 - .04}" r=".035" fill="#fff"/>')
    return f'<svg width="174mm" height="174mm" viewBox="0 0 10 10">{"".join(out + text)}</svg>'


def make_snakes():
    g = "Grain to Glass Snakes and Ladders"
    board = felt_board(g, "2 to 6 players", f"{sl_board()}",
                       "Good brewing habits are ladders. Brewing faults are snakes. Start at the grain and race to the glass.")
    lad = "".join(f"<li><b>{a} to {b}: {t}.</b> {why}</li>" for a, b, _, t, why in LADDERS)
    sna = "".join(f"<li><b>{a} to {b}: {t}.</b> {why}</li>" for a, b, _, t, why in SNAKES)
    rules = rules_sheet(g, f"""<div class="eyebrow">How to play</div><h1>Rules and lessons</h1>
<ol style="margin-top:3mm"><li>Everyone starts off the board, before square 1. Youngest player goes first.</li>
<li>Roll the die and move your cap that many squares, following the numbers.</li>
<li>Land at the foot of a ladder and climb to its top. Land on a snake's head and slide down to its tail.</li>
<li>Read the lesson out loud each time you climb or slide. That is the brewing class.</li>
<li>You need the exact roll to land on 100. The first player into the glass wins.</li></ol>
<h2>Ladders: good habits</h2><ul>{lad}</ul>
<h2>Snakes: brewing faults</h2><ul>{sna}</ul>""")
    teams = [("Pale", GOLD, "P"), ("Amber", AMBER, "A"), ("Hop", GREEN, "H"), ("Stout", "#3b2a20", "S"), ("Blue", BLUE, "B"), ("Teal", TEAL, "T")]
    write_pdf("grain-to-glass-snakes-ladders", [board, rules, pieces_sheet(g, teams, 1)])


# ---------------------------------------------------------------- Brewery Tycoon
GROUPS = {"brown": "#8b5a3c", "sky": "#7fc4d8", "pink": "#d16a9a", "orange": AMBER,
          "red": "#c0392b", "yellow": GOLD, "green": GREEN, "navy": "#1f3a7a"}
BUILD = {"brown": 50, "sky": 50, "pink": 100, "orange": 100, "red": 150, "yellow": 150, "green": 200, "navy": 200}
# (kind, name, price, group)  kind: go, prop, dist, util, luck, market, tax, audit, rest, lapse
SQUARES = [
    ("go", "Brew Day", 0, ""), ("prop", "Kitchen Brewery", 60, "brown"), ("market", "Market Day", 0, ""),
    ("prop", "Garage Brewery", 60, "brown"), ("tax", "Excise Duty", 200, ""), ("dist", "North Distributor", 200, ""),
    ("prop", "Chandigarh Taproom", 100, "sky"), ("luck", "Brewer's Luck", 0, ""), ("prop", "Jaipur Taproom", 100, "sky"),
    ("prop", "Kolkata Taproom", 120, "sky"), ("audit", "Excise Audit", 0, ""),
    ("prop", "Goa Taproom", 140, "pink"), ("util", "Glycol Chiller", 150, ""), ("prop", "Hyderabad Taproom", 140, "pink"),
    ("prop", "Chennai Taproom", 160, "pink"), ("dist", "South Distributor", 200, ""), ("prop", "Lucknow Taproom", 180, "orange"),
    ("market", "Market Day", 0, ""), ("prop", "Indore Taproom", 180, "orange"), ("prop", "Nagpur Taproom", 200, "orange"),
    ("rest", "Free Tasting", 0, ""),
    ("prop", "Noida Taproom", 220, "red"), ("luck", "Brewer's Luck", 0, ""), ("prop", "Gurugram Taproom", 220, "red"),
    ("prop", "Delhi Taproom", 240, "red"), ("dist", "East Distributor", 200, ""), ("prop", "Navi Mumbai Taproom", 260, "yellow"),
    ("prop", "Pune Taproom", 260, "yellow"), ("util", "Water Treatment", 150, ""), ("prop", "Mumbai Taproom", 280, "yellow"),
    ("lapse", "Licence Lapsed", 0, ""),
    ("prop", "Whitefield Taproom", 300, "green"), ("prop", "Koramangala Taproom", 300, "green"), ("market", "Market Day", 0, ""),
    ("prop", "Indiranagar Taproom", 320, "green"), ("dist", "West Distributor", 200, ""), ("luck", "Brewer's Luck", 0, ""),
    ("prop", "Export to Singapore", 350, "navy"), ("tax", "Licence Renewal", 100, ""), ("prop", "Export to Munich", 400, "navy"),
]
assert len(SQUARES) == 40

LUCK = ["Your IPA wins gold at a beer festival. Collect ₹150.", "A batch gets infected. Pay ₹100 to dump it and deep clean.",
        "Advance to Brew Day. Collect ₹200.", "The glycol chiller breaks down in May. Pay ₹120 for repairs.",
        "Go to Excise Audit. Do not pass Brew Day.", "Advance to the nearest Distributor. If it is owned, pay double rent.",
        "Hop prices spike after a poor harvest. Pay ₹50.", "A food writer loves your taproom. Collect ₹100.",
        "A pump fails mid-transfer. Move back 3 squares.", "Your licence paperwork is perfect. Keep this card to leave Excise Audit free.",
        "Advance to Koramangala Taproom. Collect ₹200 if you pass Brew Day.", "Power cut during the boil. Pay ₹40 for diesel.",
        "You sign a contract brewing deal. Collect ₹120.", "Maintenance is due. Pay ₹25 per taproom and ₹100 per brewpub you own.",
        "A dairy farm buys your spent grain. Collect ₹30.", "Bottles gush from over-priming. Pay ₹60 in refunds."]
MARKET = ["A company books a corporate tasting. Collect ₹100.", "Bank loan interest is due. Pay ₹50.",
          "It is your taproom's birthday. Collect ₹10 from every player.", "Your sensory panel catches a fault before release. Collect ₹50.",
          "The excise department rejects your label. Pay ₹80 to reprint.", "The monsoon slows sales. Pay ₹40.",
          "IPL final night and the taps run dry. Collect ₹150.", "A dry day is announced. Pay ₹30.",
          "Advance to Brew Day. Collect ₹200.", "Go to Excise Audit. Do not pass Brew Day.",
          "Keep this card to leave Excise Audit free.", "Brewing course graduates join your team. Collect ₹60.",
          "A malt delivery arrives damp. Pay ₹50.", "New Year's Eve rush. Collect ₹200.",
          "Your water test fails, so you add RO treatment. Pay ₹70.", "Readers vote you best new brewery. Collect ₹80."]
assert len(LUCK) == len(MARKET) == 16


def rents(price):
    base = max(2, round(price / 10))
    return base, base * 5, base * 15, base * 40, base * 60


def board_pos(i):
    """(row, col) on an 11 by 11 grid, Brew Day at bottom right, moving clockwise."""
    if i <= 10:
        return 11, 11 - i
    if i <= 20:
        return 11 - (i - 10), 1
    if i <= 30:
        return 1, 1 + (i - 20)
    return 1 + (i - 30), 11


ICON = {"go": "arrow", "luck": "question", "market": "star", "tax": "coin", "dist": "truck", "util": "snow",
        "audit": "magnifier", "rest": "glass", "lapse": "bolt"}


def tycoon_cell(i, sq):
    kind, name, price, group = sq
    row, col = board_pos(i)
    side = "bottom" if row == 11 else "top" if row == 1 else "left" if col == 1 else "right"
    corner = (row in (1, 11)) and (col in (1, 11))
    band = ""
    if kind == "prop":
        edge = {"bottom": "top", "top": "bottom", "left": "right", "right": "left"}[side]
        band = f"border-{edge}:3.2mm solid {GROUPS[group]};"
    label = {"go": "Collect ₹200 as you pass", "audit": "Just visiting", "rest": "Take a break",
             "lapse": "Go to Excise Audit", "tax": f"Pay ₹{price}"}.get(kind, f"₹{price}" if price else "")
    name_icon = "drop" if name == "Water Treatment" else ICON.get(kind)
    ic = icon(name_icon, "9mm" if corner else "5mm", COPPER) if name_icon else ""
    size = "8pt" if corner else "5.6pt"
    return (f'<div style="grid-row:{row};grid-column:{col};border:.25mm solid #333;{band}background:{CREAM if corner else "#fff"};'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:.8mm;gap:.6mm">'
            f'{ic}<div style="font-size:{size};font-weight:700;line-height:1.15">{name}</div>'
            f'<div style="font-size:5pt;color:#555">{label}</div></div>')


def tycoon_board():
    cells = "".join(tycoon_cell(i, sq) for i, sq in enumerate(SQUARES))
    centre = f"""<div style="grid-row:2/11;grid-column:2/11;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5mm;background:radial-gradient(circle at 50% 45%,#fffdf6,#f3ead6)">
<div style="width:34mm;height:34mm;border-radius:50%;background:{COPPER};display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 1.2mm {GOLD},0 0 0 2.4mm {COPPER}">{icon("kettle", "22mm", FOAM)}</div>
<div style="font-family:'Alfa Slab One',serif;font-size:28pt;color:{TEAL};text-shadow:.5mm .5mm 0 {GOLD}">Brewery Tycoon</div>
<div style="font-size:9pt;color:{COPPER};font-weight:700">Build a beer business across India</div>
<div style="display:flex;gap:8mm;margin-top:4mm">
<div class="cut" style="width:38mm;height:26mm;display:flex;align-items:center;justify-content:center;font-weight:700;color:{BLUE};transform:rotate(-8deg)">Brewer's Luck</div>
<div class="cut" style="width:38mm;height:26mm;display:flex;align-items:center;justify-content:center;font-weight:700;color:{GREEN};transform:rotate(8deg)">Market Day</div></div></div>"""
    return (f'<div style="display:grid;width:172mm;height:172mm;background:#fff;grid-template-columns:22mm repeat(9,1fr) 22mm;'
            f'grid-template-rows:22mm repeat(9,1fr) 22mm">{cells}{centre}</div>')


def deed(sq):
    kind, name, price, group = sq
    head = GROUPS.get(group, TEAL if kind == "dist" else BLUE)
    if kind == "prop":
        r = rents(price)
        rows = [("Rent", r[0]), ("Rent with full colour set", r[0] * 2), ("With 1 taproom", r[1]), ("With 2 taprooms", r[2]),
                ("With 3 taprooms", r[3]), ("With a brewpub", r[4])]
        body = "".join(f'<div style="display:flex;justify-content:space-between"><span>{k}</span><b>₹{v}</b></div>' for k, v in rows)
        body += f'<div style="margin-top:1.5mm;border-top:.2mm solid #ccc;padding-top:1.5mm">Taproom ₹{BUILD[group]} each. Brewpub ₹{BUILD[group]} plus 3 taprooms.</div>'
    elif kind == "dist":
        body = "".join(f'<div style="display:flex;justify-content:space-between"><span>If you own {n}</span><b>₹{v}</b></div>'
                       for n, v in [("1", 25), ("2", 50), ("3", 100), ("all 4", 200)])
    else:
        body = "<p style='font-size:7.5pt'>Own one: rent is 4 times the dice roll.<br>Own both: rent is 10 times the dice roll.</p>"
    return (f'<div class="cut" style="height:58mm;padding:2.5mm;font-size:7.5pt;display:flex;flex-direction:column;gap:1mm">'
            f'<div style="background:{head};color:#fff;text-align:center;padding:2mm;border-radius:1mm">'
            f'<div style="font-size:5.5pt;letter-spacing:.15em">TITLE DEED</div><div style="font-weight:700;font-size:9pt">{name}</div></div>'
            f'{body}<div style="margin-top:auto;display:flex;justify-content:space-between;color:#555"><span>Price ₹{price}</span><span>Mortgage ₹{price // 2}</span></div></div>')


def card(deck, colour, text):
    return gcard(colour, "question" if deck.startswith("Brewer") else "star", deck, deck, text, h=40, win=12)


def note(value, colour):
    return (f'<div class="cut" style="height:28mm;background:{colour};padding:2mm;display:flex;align-items:center;justify-content:space-between;color:{TEAL}">'
            f'<b style="font-size:13pt">₹{value}</b><div style="text-align:center;font-family:Alfa Slab One,serif;font-size:8pt">Brewery Tycoon<br>'
            f'<span style="font-size:22pt;font-weight:600">{value}</span></div><b style="font-size:13pt">₹{value}</b></div>')


def make_tycoon():
    g = "Brewery Tycoon"
    board = felt_board(g, "2 to 6 players", f"{tycoon_board()}",
                       "Start in a kitchen, end up exporting to Munich. Buy taprooms, build brewpubs and survive the excise audit.")
    owned = [sq for sq in SQUARES if sq[0] in ("prop", "dist", "util")]
    deeds = [sheet(g, f'<div class="eyebrow">Cut out · title deeds {n + 1} of 3</div>'
                      f'<div class="grid" style="grid-template-columns:repeat(3,1fr);margin-top:3mm">{"".join(deed(s) for s in owned[n * 12:(n + 1) * 12])}</div>')
             for n in range(3)]
    luck = sheet(g, f'<div class="eyebrow">Cut out · Brewer\'s Luck cards</div><div class="grid" style="grid-template-columns:repeat(3,1fr);margin-top:3mm">'
                    f'{"".join(card("Brewer&#39;s Luck", BLUE, t) for t in LUCK)}</div>')
    market = sheet(g, f'<div class="eyebrow">Cut out · Market Day cards</div><div class="grid" style="grid-template-columns:repeat(3,1fr);margin-top:3mm">'
                      f'{"".join(card("Market Day", GREEN, t) for t in MARKET)}</div>')
    tints = {1: "#ffffff", 5: "#fde8d0", 10: "#fdf2c2", 20: "#d9f0e0", 50: "#d6ecf3", 100: "#f3d9e4", 500: "#e6dcf5"}
    mix = [500, 500, 100, 100, 100, 100, 50, 50, 20, 20, 10, 10, 10, 5, 5, 1, 1, 1, 1, 1, 50, 20, 100, 500]
    money = sheet(g, f'<div class="eyebrow">Cut out · money, print this page 4 times, or 6 for a big game</div>'
                     f'<div class="grid" style="grid-template-columns:repeat(3,1fr);margin-top:3mm">{"".join(note(v, tints[v]) for v in mix)}</div>')
    builds = "".join(f'<div class="cut" style="height:13mm;background:{GREEN};color:#fff;display:flex;align-items:center;justify-content:center;font-size:6.5pt;font-weight:700">TAPROOM</div>' for _ in range(32))
    builds += "".join(f'<div class="cut" style="height:13mm;background:{AMBER};color:#fff;display:flex;align-items:center;justify-content:center;font-size:6.5pt;font-weight:700">BREWPUB</div>' for _ in range(12))
    extra = f'<h2>Taprooms and brewpubs</h2><div class="grid" style="grid-template-columns:repeat(11,1fr);gap:1.5mm">{builds}</div>'
    teams = [("Bottle", GOLD, "B"), ("Can", AMBER, "C"), ("Keg", GREEN, "K"), ("Growler", "#3b2a20", "G"), ("Pint", BLUE, "P"), ("Hop", TEAL, "H")]
    rules = rules_sheet(g, f"""<div class="eyebrow">How to play</div><h1>Rules</h1>
<h2>Set up</h2><ol><li>One player is the Bank. Each player gets ₹1,500: two ₹500, four ₹100, one ₹50, one ₹20, two ₹10, one ₹5 and five ₹1.</li>
<li>Shuffle both card decks face down in the middle. Everyone starts on Brew Day.</li></ol>
<h2>On your turn</h2><ol>
<li>Roll two dice and move clockwise. Roll doubles and you go again. Three doubles in a row sends you straight to Excise Audit.</li>
<li>Each time you pass Brew Day, collect ₹200 from the Bank.</li>
<li>Land on an unowned taproom, distributor or utility and you may buy it at the printed price. If you pass, the Bank auctions it to the highest bidder.</li>
<li>Land on a square someone owns and pay them the rent on its title deed.</li>
<li>Land on Brewer's Luck or Market Day, take the top card, do what it says and put it at the bottom.</li>
<li>Excise Duty and Licence Renewal are paid to the Bank.</li></ol>
<h2>Growing your brewery</h2><ol>
<li>Own every taproom in a colour set and rent doubles. Then you can build taprooms, one per square at a time, keeping the set even.</li>
<li>With 3 taprooms on a square you can upgrade to a brewpub: pay the price and return the 3 taprooms to the Bank.</li>
<li>Short of cash? Mortgage a square for half its price. No rent is due on it until you pay back the mortgage plus 10 per cent.</li></ol>
<h2>Excise Audit</h2><ol>
<li>Licence Lapsed, three doubles or a card can send you to Excise Audit. Do not collect ₹200 on the way.</li>
<li>To leave, pay ₹50, use a keep card or roll doubles. After three failed turns you must pay ₹50 and move.</li>
<li>Landing on Excise Audit by a normal roll means you are just visiting.</li></ol>
<h2>Winning</h2><p>If you cannot pay what you owe, you are out and everything you own goes to whoever you owe. The last brewery standing wins.
For a shorter game, stop after an agreed time: the richest player, counting cash, square prices and buildings, wins.</p>""")
    back = lambda title, ic: sheet(g, '<div class="eyebrow">Card backs. Print on the reverse of the sheet before.</div>' + backs(16, title, ic, 40))
    write_pdf("brewery-tycoon", [board, rules, *deeds, luck, back("Brewer's Luck", "question"), market, back("Market Day", "star"),
                                 money, pieces_sheet(g, teams, 1, extra)])


if __name__ == "__main__":
    make_ludo()
    make_snakes()
    make_tycoon()
    import games_party
    import games_strategy
    games_party.main()
    games_strategy.main()
