# -*- coding: utf-8 -*-
"""Article art shared by the share images (make_og.py) and the banner at the top
of every guide (article_render.py): the colour says the category, the icon the topic."""
import hashlib

import game_art

# Article art: the tile colour says the category, the icon says the topic.
CAT_COLOUR = {"Wine": "#8e2c48", "Whisky": "#b8662f", "Drinks business": "#2e7f9a", "Beer for teams": "#d9862a",
              "Business": "#2e7f9a", "Branding": "#b3302c", "Careers": "#6b4fa0", "Tasting": "#c98a1b",
              "Ingredients": "#4f7f2f", "Brewing science": "#0a6d84", "Brewing basics": "#d9862a", "Styles": "#b8662f"}
CAT_ICON = {"Wine": "wineglass", "Whisky": "cask", "Drinks business": "chart", "Beer for teams": "chart",
            "Business": "coin", "Branding": "pencil", "Careers": "people", "Tasting": "glass", "Ingredients": "barley",
            "Brewing science": "tank", "Brewing basics": "kettle", "Styles": "glass"}
# First matching word in the slug wins, so order runs specific to general.
TOPIC_ICON = [("grape", "grapes"), ("wine", "wineglass"), ("whisky", "cask"), ("cask", "cask"), ("distill", "cask"),
              ("spirit", "cask"), ("hop", "hop"), ("yeast", "yeast"), ("kveik", "yeast"), ("brett", "yeast"),
              ("ferment", "tank"), ("lager", "snow"), ("cold", "snow"), ("chill", "snow"), ("glycol", "snow"),
              ("ph", "drop"), ("water", "drop"), ("temperature", "thermo"), ("mash", "thermo"), ("boil", "flame"),
              ("malt", "barley"), ("barley", "barley"), ("wheat", "barley"), ("oat", "barley"), ("rice", "barley"),
              ("can", "can"), ("keg", "keg"), ("bottl", "bottle"), ("packag", "box"), ("label", "pencil"),
              ("design", "pencil"), ("brand", "pencil"), ("nam", "pencil"), ("pair", "plate"), ("food", "plate"),
              ("cheese", "plate"), ("dessert", "plate"), ("off-flavour", "magnifier"), ("infection", "bug"),
              ("sour", "bug"), ("quality", "magnifier"), ("kpi", "chart"), ("data", "chart"), ("forecast", "chart"),
              ("sales", "chart"), ("depletion", "chart"), ("price", "coin"), ("pricing", "coin"), ("cost", "coin"),
              ("excise", "coin"), ("funding", "coin"), ("economics", "coin"), ("regulation", "check"), ("rules", "check"), ("licence", "check"), ("compliance", "check"),
              ("fssai", "check"), ("supply", "truck"),
              ("distribution", "truck"), ("trade", "truck"), ("energy", "bolt"), ("job", "people"),
              ("career", "people"), ("team", "people"), ("joiner", "people"), ("staff", "people"), ("shelf", "clock"),
              ("long", "clock"), ("stale", "clock"), ("judge", "star"), ("bjcp", "star"), ("score", "star")]


def topic_icon(slug, cat):
    words = slug.split("-")
    for key, name in TOPIC_ICON:
        if key in words or (len(key) >= 3 and any(w.startswith(key) for w in words)) or (
                "-" in key and key in slug):
            return name
    return CAT_ICON.get(cat, "glass")


# Supporting icons per category, for the banner pattern and accents.
CAT_SET = {"Wine": ["grapes", "wineglass", "bottle", "sun", "plate"], "Whisky": ["cask", "barley", "flame", "glass", "clock"],
           "Beer for teams": ["chart", "truck", "keg", "can", "barley"], "Drinks business": ["chart", "check", "coin", "truck", "people"],
           "Business": ["coin", "chart", "truck", "keg"], "Branding": ["pencil", "can", "bottle", "star"],
           "Careers": ["people", "star", "kettle", "check"], "Tasting": ["glass", "plate", "magnifier", "star"],
           "Ingredients": ["barley", "hop", "yeast", "drop"], "Brewing science": ["tank", "thermo", "yeast", "flame"],
           "Brewing basics": ["kettle", "thermo", "glass", "barley"], "Styles": ["glass", "hop", "barley", "keg"]}
NAVY, GOLD, CREAM = "#0f3340", "#f3c34d", "#fff8ec"


def _mix(hex_a, hex_b, t):
    a, b = (tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) for h in (hex_a, hex_b))
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def _use(name, x, y, size, colour, width, rot=0, op=1):
    """Place a 48-unit icon symbol centred on (x, y). Stroke width is in screen pixels."""
    k = size / 48
    return (f'<use href="#i-{name}" width="48" height="48" transform="translate({x - size / 2:.0f} {y - size / 2:.0f}) rotate({rot} {size / 2:.0f} {size / 2:.0f}) scale({k:.3f})" '
            f'stroke="{colour}" stroke-width="{width / k:.2f}" opacity="{op}"/>')


def banner_svg(slug, cat):
    """1200x500 banner, no text: category ground, icon pattern, topic icon in a gold-ringed disc."""
    colour = CAT_COLOUR.get(cat, "#d9862a")
    main = topic_icon(slug, cat)
    pool = [i for i in CAT_SET.get(cat, ["glass", "hop", "barley", "keg"]) if i != main] or ["glass"]
    seed = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    acc = [pool[seed % len(pool)], pool[(seed + 1) % len(pool)]]
    names = sorted({main, *pool, *acc})
    defs = "".join(f'<symbol id="i-{n}" viewBox="0 0 48 48" overflow="visible"><g fill="none" stroke-linecap="round" '
                   f'stroke-linejoin="round">{game_art._P[n]}</g></symbol>' for n in names)
    pattern = "".join(_use(pool[(r + c + seed) % len(pool)], c * 120 + (60 if r % 2 else 0) - 20, r * 110 + 30, 54,
                           CREAM, 2, (seed + r * 31 + c * 17) % 40 - 20, ".09")
                      for r in range(5) for c in range(11))
    cx, cy = 810, 250
    dark = _mix(colour, NAVY, .55)
    return f"""<svg viewBox="0 0 1200 500" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true" focusable="false">
<defs>{defs}<linearGradient id="g-{slug}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{colour}"/><stop offset="1" stop-color="{dark}"/></linearGradient></defs>
<rect width="1200" height="500" fill="url(#g-{slug})"/>{pattern}
<circle cx="{cx + 18}" cy="{cy + 18}" r="200" fill="none" stroke="{GOLD}" stroke-width="4" opacity=".7"/>
<circle cx="{cx}" cy="{cy}" r="190" fill="{NAVY}" opacity=".55"/>
{_use(main, cx, cy, 250, CREAM, 11)}
<circle cx="{cx - 230}" cy="{cy - 130}" r="58" fill="{dark}" stroke="{GOLD}" stroke-width="4"/>{_use(acc[0], cx - 230, cy - 130, 62, GOLD, 4.5)}
<circle cx="{cx + 215}" cy="{cy + 150}" r="48" fill="{dark}" stroke="{GOLD}" stroke-width="4"/>{_use(acc[1], cx + 215, cy + 150, 52, GOLD, 4.5)}
<rect y="490" width="1200" height="10" fill="{GOLD}" opacity=".85"/>
</svg>"""
