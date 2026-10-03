# -*- coding: utf-8 -*-
"""Party and quiz games: Beer Style Bingo, Hop and Style Trumps, Pairing Dominoes,
Brewery Quiz Trail. Shared page helpers live in make_games.py.

Style facts come from content/styles_plan.json and content/styles/*.json (our own
text). Hop alpha acid figures are typical supplier ranges; crop years vary.
"""
import json
import math
import random
import re

from game_art import COPPER, FOAM, backs, gcard, icon
from make_games import (AMBER, BLUE, CREAM, GOLD, GREEN, HERE, TEAL, cap, die_net,
                        felt_board, pieces_sheet, rules_sheet, sheet, write_pdf)

PLAN = json.loads((HERE / "content/styles_plan.json").read_text())
COPY = {p["slug"]: json.loads((HERE / f"content/styles/{p['slug']}.json").read_text()) for p in PLAN}


def top(rng):
    """Upper bound of a range like '4.8-5.4%' or '18-30'; None if unparseable."""
    nums = re.findall(r"\d+(?:\.\d+)?", rng or "")
    return float(nums[-1]) if nums else None


def masked_tagline(style):
    line = COPY[style["slug"]].get("tagline", "")
    for word in re.findall(r"[A-Za-zÀ-ÿ]{4,}", style["name"]):
        if word.lower() not in {"style", "american", "english", "german", "belgian"}:
            line = re.sub(word, "____", line, flags=re.I)
    return line


POOL = [s for s in PLAN if all(top(s[k]) for k in ("abv", "ibu", "srm"))][::2][:40]


# ---------------------------------------------------------------- Beer Style Bingo
def bingo_card(n):
    picks = random.Random(n).sample(POOL, 24)
    picks.insert(12, None)
    cells = "".join(
        f'<div style="border:.3mm solid {TEAL};display:flex;align-items:center;justify-content:center;text-align:center;'
        f'padding:1mm;font-size:{7 if s else 9}pt;font-weight:700;background:{GOLD if not s else "#fff"};line-height:1.15">'
        f'{s["name"] if s else "FREE<br>PINT"}</div>' for s in picks)
    return (f'<div class="cut" style="padding:3mm"><div style="display:flex;justify-content:space-between;align-items:baseline">'
            f'<b style="font-family:Alfa Slab One,serif;font-size:16pt;color:{TEAL}">Beer Style Bingo</b><span style="font-size:8pt;color:#777">Card {n}</span></div>'
            f'<div style="display:grid;grid-template-columns:repeat(5,1fr);grid-auto-rows:20mm;margin-top:2mm">{cells}</div></div>')


def bingo_clue(s):
    body = (f'{masked_tagline(s)}<br><span style="color:#666">ABV {s["abv"]}, IBU {s["ibu"]}, colour {s["srm"]} SRM</span>'
            f'<br><span style="color:{COPPER}">Answer: <b>{s["name"]}</b></span>')
    return gcard(AMBER, "glass", s["family"], "Which style am I?", body, h=48, win=11)


def make_bingo():
    g = "Beer Style Bingo"
    rules = rules_sheet(g, f"""<h1>Beer Style Bingo</h1>
<p style="margin-top:2mm">A caller reads out style clues. Players work out the style and mark it on their card.</p>
<h2>You need</h2><ul><li>One bingo card per player (12 different cards are included).</li>
<li>The caller's clue cards, cut out and shuffled.</li><li>A pencil, or bottle caps as markers.</li></ul>
<h2>How to play</h2><ol>
<li>The caller draws a clue card and reads the family, the description and the numbers. Not the answer.</li>
<li>Players who think they have that style on their card mark it. The caller keeps drawn cards in a pile.</li>
<li>First to complete a row, a column or a diagonal shouts "Cheers!" The caller checks each marked style against the pile.</li>
<li>A wrong mark means that player sits out the next clue. Keep playing for a full card if you like.</li></ol>
<h2>Make it harder</h2><ul><li>Read only the numbers: ABV, IBU and colour.</li><li>Pour small samples and let the beer be the clue.</li></ul>
<div class="note"><b>Reading the numbers.</b> ABV is alcohol by volume. IBU is bitterness: under 20 is gentle, over 60 is bold.
SRM is colour: 2 to 4 is straw, 10 to 17 is amber to copper, 30 and up is black.</div>""")
    cards = [sheet(g, f'<div class="eyebrow">Player cards {p * 2 + 1} and {p * 2 + 2}</div>'
                      f'<div class="grid" style="gap:8mm;margin-top:3mm">{bingo_card(p * 2 + 1)}{bingo_card(p * 2 + 2)}</div>')
             for p in range(6)]
    clues = [sheet(g, f'<div class="eyebrow">Caller clue cards · cut out</div><div class="grid" style="grid-template-columns:repeat(3,1fr);margin-top:3mm">'
                      f'{"".join(bingo_clue(s) for s in POOL[i:i + 15])}</div>') for i in range(0, len(POOL), 15)]
    clues = [page for c in clues for page in (c, sheet(g, '<div class="eyebrow">Card backs. Print on the reverse of the sheet before.</div>' + backs(15, g, "star", 48)))]
    write_pdf("beer-style-bingo", [rules, *clues, *cards])


# ---------------------------------------------------------------- Hop and Style Trumps
HOPS = [  # name, origin, alpha low, alpha high, year (0 = heritage), aroma
    ("Saaz", "Czech Republic", 3, 4.5, 0, "Earthy, herbal, spicy"), ("Hallertauer Mittelfrüh", "Germany", 3, 5.5, 0, "Floral, gentle spice"),
    ("Tettnanger", "Germany", 3.5, 5.5, 0, "Floral, herbal"), ("Spalter", "Germany", 2.5, 5.5, 0, "Spicy, woody"),
    ("East Kent Goldings", "England", 4, 6.5, 0, "Honey, earthy, smooth"), ("Fuggle", "England", 3, 5.6, 1875, "Woody, minty, grassy"),
    ("Northern Brewer", "England", 7, 10, 1934, "Woody, mint"), ("Challenger", "England", 6.5, 9, 1972, "Cedar, green tea"),
    ("Target", "England", 9.5, 12.5, 1972, "Sage, spice"), ("Perle", "Germany", 6, 9, 1978, "Mint, light spice"),
    ("Magnum", "Germany", 12, 14, 1980, "Clean bittering"), ("Herkules", "Germany", 12, 17, 2005, "Pepper, pine"),
    ("Hallertau Blanc", "Germany", 9, 12, 2012, "White wine, gooseberry"), ("Mandarina Bavaria", "Germany", 7, 10, 2012, "Tangerine"),
    ("Huell Melon", "Germany", 5, 8, 2012, "Honeydew, strawberry"), ("Cascade", "USA", 4.5, 7, 1972, "Grapefruit, flowers"),
    ("Willamette", "USA", 4, 6, 1976, "Herbal, floral"), ("Chinook", "USA", 12, 14, 1985, "Pine, spice, grapefruit"),
    ("Centennial", "USA", 9.5, 11.5, 1990, "Lemon, flowers"), ("Amarillo", "USA", 8, 11, 2000, "Orange, apricot"),
    ("Simcoe", "USA", 12, 14, 2000, "Pine, passion fruit"), ("Citra", "USA", 11, 13, 2008, "Lime, mango, passion fruit"),
    ("El Dorado", "USA", 14, 16, 2010, "Pear, watermelon, sweets"), ("Mosaic", "USA", 11.5, 13.5, 2012, "Blueberry, tropical, pine"),
    ("Sabro", "USA", 12, 16, 2018, "Coconut, tangerine"), ("Nelson Sauvin", "New Zealand", 12, 13, 2000, "White wine, gooseberry"),
    ("Motueka", "New Zealand", 6.5, 7.5, 1998, "Lime, tropical"), ("Galaxy", "Australia", 13, 15, 2009, "Passion fruit, peach"),
    ("Vic Secret", "Australia", 14, 17, 2013, "Pineapple, pine"), ("Sorachi Ace", "Japan", 11, 16, 1984, "Lemon, dill"),
]


def trump_card(colour, kicker, name, sub, stats, note):
    rows = "".join(f'<div style="display:flex;justify-content:space-between;border-bottom:.2mm solid #e5e5e5;padding:1.1mm 0;font-size:8pt">'
                   f'<span>{k}</span><b style="color:{colour}">{v}</b></div>' for k, v in stats)
    body = f'<div style="color:#666;margin-bottom:1mm">{sub}</div>{rows}<div style="margin-top:2mm;color:#555">{note}</div>'
    return gcard(colour, "hop" if kicker == "HOP" else "glass", "Hop" if kicker == "HOP" else "Style", name, body, h=84, win=24)


def make_trumps():
    g = "Hop and Style Trumps"
    hop_cards = [trump_card(GREEN, "HOP", n, o, [("Alpha acid, top %", f"{hi:g}"), ("Alpha range", f"{lo:g} to {hi:g}%"),
                                                  ("Released", str(y) if y else "Heritage")], f"Aroma: {a}")
                 for n, o, lo, hi, y, a in HOPS]
    families = {}
    for s in PLAN:
        if all(top(s[k]) for k in ("abv", "ibu", "srm")) and len(families.get(s["family"], [])) < 3:
            families.setdefault(s["family"], []).append(s)
    styles = [s for group in families.values() for s in group][:30]
    style_cards = [trump_card(AMBER, "STYLE", s["name"], s["family"],
                              [("ABV, top %", f"{top(s['abv']):g}"), ("IBU, top", f"{top(s['ibu']):g}"), ("Colour SRM, top", f"{top(s['srm']):g}")],
                              COPY[s["slug"]].get("tagline", "")) for s in styles]
    def pages(cards, label, ic):
        out = []
        for i in range(0, len(cards), 9):
            chunk = cards[i:i + 9]
            out.append(sheet(g, f'<div class="eyebrow">{label}. Cut along the edges.</div><div class="grid" style="grid-template-columns:repeat(3,1fr);margin-top:3mm">{"".join(chunk)}</div>'))
            out.append(sheet(g, '<div class="eyebrow">Card backs. Print on the reverse of the sheet before.</div>' + backs(len(chunk), label, ic, 84)))
        return out
    rules = rules_sheet(g, f"""<h1>Hop and Style Trumps</h1>
<p style="margin-top:2mm">Two decks in one pack: {len(HOPS)} hop varieties and {len(styles)} beer styles. Play them apart or shuffle them for a chaos round.</p>
<h2>How to play</h2><ol>
<li>Shuffle one deck and deal it all out face down. Players hold their pile and look only at the top card.</li>
<li>The player left of the dealer reads one stat from their top card, for example "Alpha acid, top: 16".</li>
<li>Everyone reads the same stat from their own top card. The highest number wins all the top cards and goes next.</li>
<li>On the Released stat the newest hop wins. Heritage hops are the oldest of all.</li>
<li>A tie puts the cards in the middle. The winner of the next round takes them too.</li>
<li>Win every card, or hold the most when time is up.</li></ol>
<div class="note"><b>What the numbers mean.</b> Alpha acid is the share of a hop that turns bitter in the boil: high alpha hops bitter efficiently,
low alpha hops are usually kept for aroma. Hop figures are typical supplier ranges and change from crop to crop, so check your own spec sheet.
Style figures are the top of each style's range in our Style Library.</div>""")
    write_pdf("hop-and-style-trumps", [rules, *pages(hop_cards, "Hop deck", "hop"), *pages(style_cards, "Style deck", "glass")])


# ---------------------------------------------------------------- Pairing Dominoes
FAMILIES = [  # family, colour, beers, dishes
    ("Crisp", "#7fb3c8", ["Pilsner", "Helles"], ["Vegetable pakora", "Samosa"]),
    ("Citrus", GOLD, ["Witbier", "Gose"], ["Fish Amritsari", "Lemon rice"]),
    ("Smoky", "#8b5a3c", ["Rauchbier", "Smoked porter"], ["Tandoori chicken", "Baingan bharta"]),
    ("Caramel", AMBER, ["Amber ale", "Brown ale"], ["Gulab jamun", "Onion uttapam"]),
    ("Roast", "#3b2a20", ["Dry stout", "Imperial stout"], ["Chocolate brownie", "Mutton seekh kebab"]),
    ("Spice", "#c0392b", ["Saison", "Belgian tripel"], ["Hyderabadi biryani", "Chole bhature"]),
    ("Tropical", GREEN, ["Hazy IPA", "Mango sour"], ["Kerala prawn curry", "Mango kulfi"]),
]


FAM_ICON = {"Crisp": "snow", "Citrus": "sun", "Smoky": "flame", "Caramel": "drop", "Roast": "kettle", "Spice": "star", "Tropical": "hop"}


def domino_half(fi, slot):
    fam, colour, beers, dishes = FAMILIES[fi]
    item = (beers + dishes)[slot % 4]
    kind = "BEER" if slot % 4 < 2 else "DISH"
    return (f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:1mm">'
            f'<div style="width:9mm;height:9mm;border-radius:50%;background:{colour};display:flex;align-items:center;justify-content:center">{icon(FAM_ICON[fam], "6mm", FOAM)}</div>'
            f'<div style="font-size:6.5pt;color:#777;margin-top:.8mm">{fam} {kind.lower()}</div>'
            f'<div style="font-size:8.5pt;font-weight:700;line-height:1.15">{item}</div></div>')


def make_dominoes():
    g = "Pairing Dominoes"
    tiles, used = [], [0] * 7
    for a in range(7):
        for b in range(a, 7):
            if a == b:  # a double shows the perfect pairing: a beer and a dish from one family
                left, right = domino_half(a, used[a] % 2), domino_half(a, 2 + used[a] % 2)
            else:
                left, right = domino_half(a, used[a]), domino_half(b, used[b])
                used[a] += 1
                used[b] += 1
            tiles.append(f'<div style="height:34mm;display:flex;border-radius:3mm;background:#fffdf7;border:.5mm solid #2b1d16;box-shadow:inset 0 0 0 1.2mm #fff,inset 0 0 0 1.6mm #d8cfbd">{left}'
                         f'<div style="width:.4mm;background:#999;margin:2mm 0"></div>{right}</div>')
    grid = lambda ts: f'<div class="grid" style="grid-template-columns:repeat(2,1fr);margin-top:3mm">{"".join(ts)}</div>'
    fam_rows = "".join(f'<li><b style="color:{c}">{f}:</b> {", ".join(be)} with {", ".join(d)}.</li>' for f, c, be, d in FAMILIES)
    rules = rules_sheet(g, f"""<h1>Pairing Dominoes</h1>
<p style="margin-top:2mm">A 28-tile set where the pips are flavour families. Join halves that share a family and you build a chain of beer and food pairings.</p>
<h2>How to play</h2><ol>
<li>Shuffle the tiles face down. Each player takes 7 (with 2 players) or 5 (with 3 or 4 players). The rest are the boneyard.</li>
<li>The player holding the Roast double starts. Otherwise the highest double starts.</li>
<li>On your turn, place a tile so one half touches an open end of the same colour family. Say the pairing out loud.</li>
<li>Cannot play? Draw from the boneyard until you can, or pass when it is empty.</li>
<li>First to play all their tiles wins. If everyone is stuck, the fewest tiles wins.</li></ol>
<h2>The families</h2><ul>{fam_rows}</ul>
<div class="note"><b>Why it works.</b> Shared flavours amplify each other: roast meets chocolate, smoke meets the tandoor.
Doubles show a beer and a dish from the same family, the strongest match in the set. Real pairing also uses contrast,
like a crisp lager cutting through fried pakora, so argue about the edges.</div>""")
    write_pdf("pairing-dominoes", [rules, sheet(g, f'<div class="eyebrow">Tiles 1 to 14 · cut out</div>{grid(tiles[:14])}'),
                                   sheet(g, f'<div class="eyebrow">Tiles 15 to 28 · cut out</div>{grid(tiles[14:])}')])


# ---------------------------------------------------------------- Brewery Quiz Trail
CAT_ICON = {"Ingredients": "barley", "Process": "kettle", "Styles": "glass", "Sensory": "magnifier", "Business": "coin", "India": "star"}
CATS = [("Ingredients", BLUE), ("Process", GREEN), ("Styles", GOLD), ("Sensory", AMBER), ("Business", TEAL), ("India", "#c0392b")]
QUESTIONS = {
    "Ingredients": [("Which grain is most often malted for beer?", "Barley"),
                    ("Besides bitterness, what do hops give beer?", "Aroma and flavour; they also help keep it fresh"),
                    ("What does yeast make from sugar?", "Alcohol and carbon dioxide"),
                    ("Roughly how much of a beer is water?", "More than 90 per cent"),
                    ("Which part of the hop plant goes into beer?", "The flower, called the cone"),
                    ("Which hop compounds turn bitter in the boil?", "Alpha acids"),
                    ("What is the species name of lager yeast?", "Saccharomyces pastorianus"),
                    ("What is the species name of ale yeast?", "Saccharomyces cerevisiae"),
                    ("Which water ion gives a drier, firmer hop bite?", "Sulphate"),
                    ("Which water ion gives a rounder, fuller malt feel?", "Chloride"),
                    ("Saaz hops come from which country?", "Czech Republic"),
                    ("Grain that is steeped, sprouted and dried is called what?", "Malt")],
    "Process": [("What is the step where crushed malt soaks in hot water?", "Mashing"),
                ("What do brewers call beer before it ferments?", "Wort"),
                ("How long is a typical boil?", "60 to 90 minutes"),
                ("Name one reason to chill wort fast after the boil.", "Less DMS, less infection risk, ready to pitch yeast"),
                ("What does pitching mean?", "Adding yeast to the wort"),
                ("Which instrument measures gravity?", "A hydrometer or a refractometer"),
                ("What is lagering?", "Cold conditioning for weeks"),
                ("What is dry hopping?", "Adding hops after the boil, usually in the fermenter"),
                ("What does CIP stand for?", "Cleaning in place"),
                ("What is sparging?", "Rinsing the grain bed with hot water to collect more sugar"),
                ("What is the hot break?", "Proteins clumping together in the boil"),
                ("Why do brewers hold a diacetyl rest?", "So yeast can clean up buttery diacetyl"),
                ],
    "Styles": [("Which city gave the Pilsner its name?", "Plzeň (Pilsen), Czech Republic"),
               ("Which German wheat beer tastes of banana and clove?", "Hefeweizen"),
               ("Which Belgian wheat beer uses coriander and orange peel?", "Witbier"),
               ("What does IPA stand for?", "India Pale Ale"),
               ("Which black Irish style is known for roast and a creamy head?", "Dry stout"),
               ("Which German style is linked with Oktoberfest?", "Märzen, or Festbier today"),
               ("Which pale ale style comes from Cologne?", "Kölsch"),
               ("Which Belgian farmhouse ale was brewed for seasonal workers?", "Saison"),
               ("Which tart wheat beer from Leipzig uses salt and coriander?", "Gose"),
               ("Which strong German lager has a goat as its symbol?", "Bock"),
               ("What does NEIPA stand for?", "New England India Pale Ale"),
               ("Which smoked lager is famous in Bamberg?", "Rauchbier")],
    "Sensory": [("Which off-flavour smells of butter or butterscotch?", "Diacetyl"),
                ("Which off-flavour smells of cooked sweetcorn?", "DMS (dimethyl sulphide)"),
                ("A green apple aroma usually points to what?", "Acetaldehyde"),
                ("Wet cardboard tells you a beer is what?", "Oxidised"),
                ("What makes a beer smell skunky?", "Light striking hop compounds"),
                ("Where does clove in a wheat beer come from?", "Yeast phenols"),
                ("What is a triangle test?", "Three samples, two the same: find the odd one"),
                ("Which glass shape holds aroma best?", "One that curves inwards, like a tulip"),
                ("Why serve a stout warmer than a lager?", "Cold hides aroma; fuller beers open up a little warmer"),
                ("Banana in a Hefeweizen comes from which ester?", "Isoamyl acetate"),
                ("What does mouthfeel describe?", "Body, carbonation and texture"),
                ("What order should a tasting flight follow?", "Light and low alcohol first, dark and strong last")],
    "Business": [("What is a brewpub?", "A pub that brews its own beer on site"),
                 ("What is contract brewing?", "Paying another brewery to brew your recipe"),
                 ("What is gypsy brewing?", "Brewing in other people's breweries without owning one"),
                 ("Kegs or bottles: which is cheaper per litre to package?", "Kegs"),
                 ("What does COGS stand for?", "Cost of goods sold"),
                 ("What does on-trade mean?", "Bars, pubs and restaurants"),
                 ("What does off-trade mean?", "Shops and retailers"),
                 ("What is a taproom?", "A brewery's own bar, selling straight to drinkers"),
                 ("What is a seasonal release?", "A beer sold for a limited time of year"),
                 ("Why clean draught lines often?", "Dirty lines cause off-flavours and lost sales"),
                 ("What is spent grain often used for?", "Animal feed"),
                 ("What does brewhouse efficiency measure?", "How much of the malt's sugar ends up in the wort")],
    "India": [("Which city is often called India's craft beer capital?", "Bengaluru"),
              ("Who issues liquor licences in an Indian state?", "The state excise department"),
              ("Which national body sets food safety rules for beer?", "FSSAI"),
              ("Name one Indian state where alcohol is prohibited.", "Gujarat, Bihar, Nagaland or Mizoram"),
              ("Which grains are common adjuncts in Indian mass-market lager?", "Rice and maize"),
              ("Why does fermentation temperature control matter so much in India?", "Heat makes yeast throw off-flavours"),
              ("Why does kveik yeast suit Indian heat?", "It ferments cleanly at high temperatures"),
              ("Pune's craft beer scene is in which state?", "Maharashtra"),
              ("What is a dry day?", "A day when alcohol sales are banned"),
              ("Which Indian spice is classic in a witbier?", "Coriander"),
              ("Which Indian fruit is a favourite in craft sours and wheat beers?", "Mango"),
              ("Can beer brands advertise directly in India?", "No; brands use surrogate advertising instead")],
}


def quiz_board():
    n, cx, cy, R = 36, 93, 93, 78
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n - math.pi / 2
        hq = i % 6 == 0
        name, colour = CATS[(i - i // 6 - 1) % 6]  # the 30 plain squares cycle through all six colours
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        r = 9 if hq else 6.5
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{CATS[(i // 6) % 6][1] if hq else colour}" stroke="#333" stroke-width=".4"/>')
        if hq:
            out.append(f'<text x="{x:.1f}" y="{y + 1.5:.1f}" text-anchor="middle" font-size="4" font-weight="700" fill="#fff">HQ</text>')
    for k, (name, colour) in enumerate(CATS):
        a = 2 * math.pi * (k * 6) / n - math.pi / 2
        x1, y1 = cx + (R - 10) * math.cos(a), cy + (R - 10) * math.sin(a)
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{colour}" stroke-width="5" stroke-linecap="round" opacity=".35"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="{CREAM}" stroke="{TEAL}" stroke-width=".8"/>'
               f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" font-family="Alfa Slab One" font-size="7" font-weight="600" fill="{TEAL}">The Glass</text>'
               f'<text x="{cx}" y="{cy + 6}" text-anchor="middle" font-size="3.4" fill="#555">Final question here</text>')
    legend = "".join(f'<span style="display:inline-flex;align-items:center;gap:1.5mm;margin-right:5mm;font-size:9pt">'
                     f'<span style="width:4mm;height:4mm;border-radius:50%;background:{c}"></span>{n}</span>' for n, c in CATS)
    return f'<svg width="170mm" height="170mm" viewBox="0 0 186 186" style="background:#fff;border-radius:2mm">{"".join(out)}</svg><div style="background:#fff;padding:2mm 3mm">{legend}</div>'


def quiz_card(k):
    rows = "".join(f'<div style="display:flex;gap:2mm;margin-bottom:1.2mm"><span style="flex:none;width:5mm;height:5mm;border-radius:50%;background:{c};display:flex;align-items:center;justify-content:center">{icon(CAT_ICON[n], "3.6mm", FOAM, 3.4)}</span>'
                   f'<div><div style="font-size:7.5pt;line-height:1.25">{QUESTIONS[n][k][0]}</div>'
                   f'<div style="font-size:6.5pt;color:#666">Answer: {QUESTIONS[n][k][1]}</div></div></div>' for n, c in CATS)
    return f'<div class="gcard" style="height:62mm;padding:3mm;box-shadow:inset 0 0 0 1.2mm {TEAL}"><div class="title" style="color:{COPPER};font-size:10pt;margin-bottom:1.5mm">Quiz card {k + 1}</div>{rows}</div>'


def make_quiz():
    g = "Brewery Quiz Trail"
    board = felt_board(g, "2 to 6 players or teams", f"{quiz_board()}",
                       "Answer your way round the trail, win a badge at each HQ, then finish in the glass.")
    rules = rules_sheet(g, """<div class="eyebrow">How to play</div><h1>Rules</h1>
<ol style="margin-top:3mm"><li>Everyone starts on any HQ space. Roll the die and move either way round the trail.</li>
<li>The player to your left draws a quiz card and reads the question in the colour you landed on. Answers are in small print below.</li>
<li>Right answer: roll again. Wrong answer: your turn ends.</li>
<li>Land on an HQ and answer its colour correctly to win that category's badge. Tick it on a scrap of paper or take a cap of that colour.</li>
<li>With all six badges, head into the glass along any spoke. Your opponents choose the category for the final question.</li>
<li>Get the final question right and you win.</li></ol>
<h2>Quick version</h2><p>No board needed. Deal the cards to a quizmaster who asks round the table. First to six correct, one per colour, wins.</p>
<div class="note">72 questions across six categories: ingredients, process, styles, sensory, business and India. They match what Craft Beer School teaches,
so the quiz works well as an end-of-course test.</div>""")
    cards = [sheet(g, f'<div class="eyebrow">Quiz cards · cut out</div><div class="grid" style="grid-template-columns:repeat(2,1fr);margin-top:3mm">'
                      f'{"".join(quiz_card(k) for k in range(i, i + 8) if k < 12)}</div>') for i in (0, 8)]
    cards = [cards[0], sheet(g, '<div class="eyebrow">Card backs. Print on the reverse of the sheet before.</div>' + backs(8, g, "question", 62, 2)),
             cards[1], sheet(g, '<div class="eyebrow">Card backs. Print on the reverse of the sheet before.</div>' + backs(4, g, "question", 62, 2))]
    teams = [(n, c, n[0]) for n, c in CATS]
    write_pdf("brewery-quiz-trail", [board, rules, *cards, pieces_sheet(g, teams, 1)])


def main():
    make_bingo()
    make_trumps()
    make_dominoes()
    make_quiz()


if __name__ == "__main__":
    main()
