# -*- coding: utf-8 -*-
"""Strategy games: Off-Flavour Detective, Brew Day Dash, Tank Planner.
Shared page helpers live in make_games.py.
"""
from game_art import COPPER, backs, gcard, icon
from make_games import AMBER, BLUE, CREAM, GOLD, GREEN, TEAL, felt_board, pieces_sheet, rules_sheet, sheet, write_pdf

RED = "#c0392b"


def small_card(colour, kicker, title, text, h=40, ic="star"):
    return gcard(colour, ic, kicker, title, text, h=h, win=min(14, h * .3))


def card_pages(game, label, cards, per_page=18, cols=3, h=40, back_icon="star"):
    """Front sheets plus one backs sheet per front sheet, for double-sided printing."""
    out = []
    for i in range(0, len(cards), per_page):
        chunk = cards[i:i + per_page]
        out.append(sheet(game, f'<div class="eyebrow">{label}. Cut along the edges.</div><div class="grid" style="grid-template-columns:repeat({cols},1fr);margin-top:3mm">'
                               f'{"".join(chunk)}</div>'))
        out.append(sheet(game, f'<div class="eyebrow">Card backs. Print on the reverse of the sheet before.</div>{backs(len(chunk), game, back_icon, h, cols)}'))
    return out


# ---------------------------------------------------------------- Off-Flavour Detective
FAULTS = [("Diacetyl", "Butter, butterscotch", "Beer packaged before the yeast reabsorbed it, or a bacterial infection.",
           "Hold a warm diacetyl rest and check by forcing a sample before crashing."),
          ("DMS", "Cooked sweetcorn, tinned vegetables", "A weak or covered boil, or wort left hot too long before chilling.",
           "Boil hard with the lid off and chill quickly."),
          ("Acetaldehyde", "Green apple, fresh-cut pumpkin", "Beer taken off the yeast too early, or unhealthy yeast.",
           "Pitch enough healthy yeast and give fermentation time to finish."),
          ("Oxidation", "Wet cardboard, sherry, stale bread", "Oxygen picked up after fermentation, usually in transfer or packaging.",
           "Purge tanks and kegs with CO2 and measure dissolved oxygen."),
          ("Lightstruck", "Skunk, burnt rubber", "Light hitting hop compounds, worst in clear or green glass.",
           "Use brown glass or cans and keep beer out of the sun."),
          ("Sour infection", "Vinegar, sour milk", "Bacteria from poor cleaning or a dirty draught line.",
           "Clean, then sanitise, everything that touches the beer.")]
FAULT_ICON = {"Diacetyl": "drop", "DMS": "flame", "Acetaldehyde": "clock", "Oxidation": "box", "Lightstruck": "sun", "Sour infection": "bug"}
BEERS = ["Pilsner", "Helles", "Hefeweizen", "American IPA", "Dry Stout", "Saison"]
ROOM_ICON = {"Malt Store": "barley", "Mill Room": "mill", "Brewhouse": "kettle", "QC Lab": "magnifier", "Fermentation Hall": "tank",
             "Cold Room": "snow", "Taproom": "glass", "Keg Store": "keg", "Packaging Line": "can"}
ROOMS = [["Malt Store", "Mill Room", "Brewhouse"], ["QC Lab", "Fermentation Hall", "Cold Room"], ["Taproom", "Keg Store", "Packaging Line"]]


def detective_board():
    cells = []
    for r, row in enumerate(ROOMS):
        for c, room in enumerate(row):
            pipe = {(0, 0): "Pipe to Packaging Line", (2, 2): "Pipe to Malt Store", (0, 2): "Pipe to Taproom", (2, 0): "Pipe to Brewhouse"}.get((r, c), "")
            start = "Everyone starts here" if room == "Taproom" else ""
            cells.append(f'<div style="position:relative;background:{CREAM if (r + c) % 2 == 0 else "#fff"};border:.8mm solid {TEAL};'
                         f'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2mm;text-align:center">'
                         f'{icon(ROOM_ICON[room], "13mm", COPPER)}<div style="font-family:Alfa Slab One,serif;font-size:12pt;color:{TEAL}">{room}</div>'
                         f'<div style="font-size:7.5pt;color:{AMBER};font-weight:700">{pipe}</div><div style="font-size:7.5pt;color:#777">{start}</div></div>')
    doors = []
    for r in range(3):
        for c in range(2):  # doors between horizontal neighbours
            doors.append(f'<div style="position:absolute;left:{(c + 1) * 56 - 3}mm;top:{r * 56 + 22}mm;width:6mm;height:12mm;background:{GOLD};border:.4mm solid {TEAL}"></div>')
    for r in range(2):
        for c in range(3):  # doors between vertical neighbours
            doors.append(f'<div style="position:absolute;left:{c * 56 + 22}mm;top:{(r + 1) * 56 - 3}mm;width:12mm;height:6mm;background:{GOLD};border:.4mm solid {TEAL}"></div>')
    return (f'<div style="position:relative;width:168mm;height:168mm;background:#fff"><div style="display:grid;grid-template-columns:repeat(3,56mm);'
            f'grid-template-rows:repeat(3,56mm)">{"".join(cells)}</div>{"".join(doors)}</div>')


def notebook():
    def block(title, items):
        rows = "".join(f'<tr><td style="padding:1.6mm 2mm;font-size:9pt">{i}</td>{"".join("<td></td>" for _ in range(5))}</tr>' for i in items)
        return f'<tr><th colspan="6" style="text-align:left;background:{TEAL};color:#fff;font-size:7.5pt;padding:.8mm 2mm">{title}</th></tr>{rows}'
    rooms = [x for row in ROOMS for x in row]
    return (f'<div class="cut" style="padding:3mm"><b style="font-family:Alfa Slab One,serif;color:{TEAL}">Detective notebook</b>'
            f'<span style="font-size:7pt;color:#777;margin-left:3mm">Player columns: tick what you have seen, cross what you rule out</span>'
            f'<table style="width:100%;border-collapse:collapse;margin-top:2mm" border="1" cellspacing="0">'
            f'<tr><td></td>{"".join(f"<td style=font-size:6.5pt;text-align:center;width:11mm>P{n}</td>" for n in range(1, 6))}</tr>'
            f'{block("Fault", [f[0] for f in FAULTS])}{block("Beer", BEERS)}{block("Room", rooms)}</table></div>')


def make_detective():
    g = "Off-Flavour Detective"
    board = felt_board(g, "3 to 6 players", f"{detective_board()}",
                       "A batch has gone wrong. Which fault, in which beer, found in which room? Question the team and crack the case.")
    rules = rules_sheet(g, f"""<div class="eyebrow">How to play</div><h1>Rules</h1>
<h2>Set up</h2><ol><li>Sort the cards into faults, beers and rooms. Without looking, put one of each in the case file envelope.</li>
<li>Shuffle the rest together and deal them all out. Some players may get one more card than others.</li>
<li>Everyone takes a notebook and ticks the cards in their own hand. All caps start in the Taproom.</li></ol>
<h2>On your turn</h2><ol>
<li>Move your cap through a gold door into the next room, or take a pipe from a corner room to the opposite corner.</li>
<li>In your new room you may make a suggestion: "I think it was <b>oxidation</b> in the <b>Pilsner</b>, found in the <b>Cold Room</b>." The room must be the one you are in.</li>
<li>The player to your left shows you one matching card in secret if they hold any. If not, the next player tries, then the next.</li>
<li>Once a card has been shown to you, or nobody can show one, your turn ends. Note what you learned.</li></ol>
<h2>Solving the case</h2><ol>
<li>Once per game, on your turn, you may accuse: name a fault, a beer and a room, then check the case file in secret.</li>
<li>All three right and you win. Read the fault card out loud so everyone learns how to prevent it.</li>
<li>Wrong and you are out of the running, but you still show cards when asked.</li></ol>
<div class="note"><b>Learn the faults.</b> Every fault card lists its aroma, its usual cause and how brewers prevent it. Pair the game with an off-flavour
spiking kit and let players smell the real thing before they accuse.</div>""")
    fault_cards = [small_card(RED, "Fault", n, f"<b>Smells like:</b> {a}.<br><b>Cause:</b> {c}<br><b>Prevent:</b> {p}", h=58, ic=FAULT_ICON[n])
                   for n, a, c, p in FAULTS]
    beer_cards = [small_card(GOLD, "Beer", b, "One of the six beers in the brewery this week.", h=58, ic="glass") for b in BEERS]
    room_cards = [small_card(TEAL, "Room", r, "Where the fault was found.", h=58, ic=ROOM_ICON[r]) for row in ROOMS for r in row]
    case = small_card(AMBER, "Case file", "Top secret", ic="magnifier", text=
                      "Fold an envelope or a sheet of paper around this card. Place one fault, one beer and one room inside, unseen.", h=58)
    cards = card_pages(g, "Clue cards", fault_cards + beer_cards + room_cards + [case], per_page=12, h=58, back_icon="magnifier")
    notes = sheet(g, f'<div class="eyebrow">Notebook · print one per player</div><div style="margin-top:3mm">{notebook()}</div>')
    teams = [("Inspector Malt", AMBER, "M"), ("Inspector Hop", GREEN, "H"), ("Inspector Yeast", GOLD, "Y"),
             ("Inspector Water", BLUE, "W"), ("Inspector Stout", "#3b2a20", "S"), ("Inspector Teal", TEAL, "T")]
    write_pdf("off-flavour-detective", [board, rules, *cards, notes, pieces_sheet(g, teams, 1)])


# ---------------------------------------------------------------- Brew Day Dash
STAGES = [("Mill", "Crack the malt so water can reach the starch."), ("Mash", "Hot water turns starch into sugar."),
          ("Lauter", "Run off the sweet wort and rinse the grain."), ("Boil", "Add hops, sterilise and drive off DMS."),
          ("Whirlpool", "Spin out hop debris and proteins."), ("Chill", "Cool the wort fast before the yeast goes in."),
          ("Ferment", "Yeast turns sugar into alcohol and CO2."), ("Condition", "Cold time to clear and smooth the beer."),
          ("Package", "Keg, can or bottle it. Play this and you win!")]
STAGE_ICON = {"Mill": "mill", "Mash": "kettle", "Lauter": "drop", "Boil": "flame", "Whirlpool": "kettle", "Chill": "snow",
              "Ferment": "tank", "Condition": "clock", "Package": "can"}
TROUBLE_ICON = {"Stuck Mash": "kettle", "Boil-over": "flame", "Power Cut": "bolt", "Infection": "bug",
                "Stuck Fermentation": "yeast", "Oxygen Pickup": "box"}
TROUBLE = [("Stuck Mash", "The run-off stops dead.", "Rice Hulls", "Loosen the grain bed so wort flows again."),
           ("Boil-over", "Hot wort all over the floor.", "Burner Control", "Turn the heat down through the hot break."),
           ("Power Cut", "The brewhouse goes dark.", "Generator", "Diesel backup gets you running again."),
           ("Infection", "Something wild got into the tank.", "Sanitiser", "Clean, sanitise and start the stage again."),
           ("Stuck Fermentation", "The yeast gives up too early.", "Fresh Yeast", "Pitch a healthy starter to finish the job."),
           ("Oxygen Pickup", "Air sneaks in during transfer.", "CO2 Purge", "Push the air out before the beer goes in.")]


def make_dash():
    g = "Brew Day Dash"
    stage_cards = [small_card(GREEN, f"Stage {i} of 9", n, t, ic=STAGE_ICON[n]) for i, (n, t) in enumerate(STAGES, 1) for _ in range(4)]
    fault_cards = [small_card(RED, "Trouble: play on a rival", f, ic=TROUBLE_ICON[f], text= f"{t} They cannot add a stage until they play <b>{fix}</b>.")
                   for f, t, fix, _ in TROUBLE for _ in range(2)]
    fix_cards = [small_card(BLUE, "Fix: play on yourself", fix, f"{t} Cancels <b>{f}</b>.", ic="check") for f, _, fix, t in TROUBLE for _ in range(3)]
    order = "".join(f"<li><b>{n}.</b> {t}</li>" for n, t in STAGES)
    rules = rules_sheet(g, f"""<h1>Brew Day Dash</h1>
<p style="margin-top:2mm">Race to brew a batch from mill to package while your rivals throw trouble at your brewhouse.</p>
<h2>Set up</h2><ol><li>Shuffle all {len(stage_cards) + len(fault_cards) + len(fix_cards)} cards. Deal 5 to each player and put the rest face down as the draw pile.</li></ol>
<h2>On your turn</h2><ol><li>Draw one card.</li><li>Then do one of these:
<ul><li>Play your <b>next stage</b> face up in your own row. Stages must go in order, starting with Mill.</li>
<li>Play a <b>trouble</b> card on a rival who has no trouble showing. They are stuck until they fix it.</li>
<li>Play the matching <b>fix</b> on your own trouble. Both cards go to the discard pile.</li>
<li>Discard one card if you cannot or do not want to play.</li></ul></li>
<li>End your turn with 5 cards in hand.</li></ol>
<h2>Winning</h2><p>The first player to lay Package on a complete row of nine stages wins the brew day. If the draw pile runs out, shuffle the discards.</p>
<h2>The nine stages</h2><ol>{order}</ol>""")
    write_pdf("brew-day-dash", [rules, *card_pages(g, "Cards", stage_cards + fault_cards + fix_cards, back_icon="flame")])


# ---------------------------------------------------------------- Tank Planner
BEER_WEEKS = [("L", "Lager", 4), ("S", "Stout", 3), ("I", "IPA", 2), ("W", "Wheat", 2)]
ORDERS = [("Taproom", "IPA", 1, 4, 50), ("Taproom", "Wheat", 1, 4, 45), ("Hotel chain", "Lager", 1, 6, 70),
          ("Beer festival", "Stout", 2, 7, 110), ("Corporate party", "IPA", 2, 6, 100), ("Hotel chain", "Lager", 2, 8, 140),
          ("Wedding", "Wheat", 2, 7, 90), ("Beer festival", "IPA", 3, 9, 150), ("Taproom", "Stout", 1, 8, 55),
          ("Retail chain", "Lager", 3, 11, 210), ("Taproom", "Wheat", 1, 9, 45), ("Taproom", "IPA", 1, 10, 50),
          ("Restaurant group", "Stout", 2, 11, 110), ("Taproom", "Lager", 1, 12, 70), ("New Year's Eve", "IPA", 2, 12, 100),
          ("Summer launch", "Wheat", 3, 12, 135), ("Export trial", "Lager", 2, 10, 140), ("Taproom", "Stout", 1, 12, 55)]
EVENTS = [("Glycol failure", "Nobody may start a new brew this week."),
          ("Power cut", "Every brew already running takes one extra week. Add a box to each."),
          ("Monsoon slump", "The next order revealed is worth ₹20 less."),
          ("Festival boom", "Orders delivered this week pay ₹20 more each."),
          ("Yeast shortage", "Each player may start at most one brew this week."),
          ("CIP day", "Each player blocks one empty tank this week for cleaning.")]


def planner_sheet():
    head = "".join(f'<th style="width:11mm;font-size:7pt">W{w}</th>' for w in range(1, 13))
    rows = "".join(f'<tr><th style="font-size:7.5pt;padding:2mm">Tank {t}</th>{"".join("<td style=height:11mm></td>" for _ in range(12))}</tr>' for t in range(1, 7))
    ledger = "".join('<tr><td style="height:7mm"></td><td></td><td></td><td></td></tr>' for _ in range(8))
    key = " · ".join(f"<b>{k}</b> {n} ({w} weeks)" for k, n, w in BEER_WEEKS)
    return (f'<div class="cut" style="padding:4mm"><b style="font-family:Alfa Slab One,serif;font-size:14pt;color:{TEAL}">Tank planner</b>'
            f'<span style="font-size:8pt;margin-left:3mm">Brewery name: ______________________</span>'
            f'<table border="1" cellspacing="0" style="width:100%;border-collapse:collapse;margin-top:3mm"><tr><th></th>{head}</tr>{rows}</table>'
            f'<p style="font-size:8pt;margin-top:2mm">Write the beer letter in one box per week it sits in a tank. Circle the last box when it is ready. {key}</p>'
            f'<table border="1" cellspacing="0" style="width:100%;border-collapse:collapse;margin-top:3mm;font-size:8pt">'
            f'<tr><th>Week</th><th>Order delivered</th><th>Income ₹</th><th>Brews started × ₹20</th></tr>{ledger}'
            f'<tr><th colspan="2" style="text-align:right;padding:1.5mm">Totals</th><td></td><td></td></tr></table>'
            f'<p style="font-size:9pt;margin-top:2mm"><b>Profit = income minus brew costs: ₹ ____________</b></p></div>')


def make_planner():
    g = "Tank Planner"
    order_cards = [small_card(GREEN, f"Order: {who}", f"{n} × {beer}", ic="truck", text=
                              f"Due by the end of week <b>{due}</b>.<br>Pays <b>₹{pay}</b>.") for who, beer, n, due, pay in ORDERS]
    event_cards = [small_card(RED, "Event", t, x, ic="bolt") for t, x in EVENTS]
    key = "".join(f"<li><b>{n}</b> takes {w} weeks in a tank.</li>" for _, n, w in BEER_WEEKS)
    rules = rules_sheet(g, f"""<h1>Tank Planner</h1>
<p style="margin-top:2mm">Six fermenters, twelve weeks and a stream of orders. Plan your tanks to deliver the right beer on time.</p>
<h2>You need</h2><ul><li>One planner sheet and a pencil per player.</li><li>The order and event cards, shuffled into one deck.</li></ul>
<h2>The beers</h2><ul>{key}</ul>
<h2>Each week</h2><ol>
<li><b>Reveal.</b> Turn over the top card. An order stays face up until it is delivered or its due week passes. An event applies this week only.</li>
<li><b>Brew.</b> Start beers in any empty tanks. Write the letter in a box for each week it needs, starting this week. Each brew costs ₹20.</li>
<li><b>Deliver.</b> A beer is ready at the end of its last week. Use ready tanks of the right beer to fill a face-up order and take the card.
Players claim orders in turn. The first player moves left each week.</li>
<li><b>Stale beer.</b> Ready beer not delivered within 2 weeks is dumped. Cross it out.</li></ol>
<h2>Winning</h2><p>After week 12, add up income from delivered orders and take away ₹20 for every brew you started. The biggest profit wins.
Solo players: beat ₹600, then try for ₹800.</p>
<div class="note"><b>The real lesson.</b> Lagers tie up a tank for twice as long as ales, so they need higher prices or longer notice.
Planning tank time against demand is one of the first places breweries use data and forecasting.</div>""")
    sheets = [sheet(g, f'<div class="eyebrow">Planner sheet · print one per player</div>{planner_sheet()}')]
    write_pdf("tank-planner", [rules, *card_pages(g, "Order and event cards", order_cards + event_cards, back_icon="tank"), *sheets])


def main():
    make_detective()
    make_dash()
    make_planner()


if __name__ == "__main__":
    main()
