# -*- coding: utf-8 -*-
"""Shared art for the printable games: palette, line icons, felt texture,
label-style title badge, framed cards and card backs.

Look: a beer label laid on a teal games-table felt. Copper frames, malt-gold
accents, slab titles. Boldness lives on the board pages; cards and rules stay quiet.
"""
import base64

FELT, FELT_DARK, COPPER, GOLD, FOAM = "#123c4a", "#0b2a34", "#b8662f", "#e9b949", "#fff8ec"
HOP, STOUT, CHERRY, SKY = "#4f7f2f", "#2b1d16", "#b3302c", "#2e7f9a"

# 48x48 line icons, drawn with currentColor strokes
_P = {
    "hop": '<path d="M24 3c1 3 3 5 6 6"/><path d="M24 11c-6 0-10 4-10 9 4 0 7-2 10-5 3 3 6 5 10 5 0-5-4-9-10-9z"/>'
           '<path d="M14 20c0 5 4 9 10 9s10-4 10-9"/><path d="M15.5 28c1 6 4 10 8.5 13 4.5-3 7.5-7 8.5-13"/><path d="M24 15v26"/>',
    "barley": '<path d="M24 45V8"/>' + "".join(
        f'<path d="M24 {y + 7}c-5 0-8-3-8-8 5 0 8 3 8 8z"/><path d="M24 {y + 7}c5 0 8-3 8-8-5 0-8 3-8 8z"/>' for y in (8, 16, 24))
        + '<path d="M24 8l-3-5M24 8l3-5"/>',
    "yeast": '<circle cx="20" cy="23" r="10"/><circle cx="32.5" cy="33" r="6"/><circle cx="34" cy="13" r="3.5"/><circle cx="17" cy="20" r="2"/>',
    "drop": '<path d="M24 5C18 15 12 22 12 30a12 12 0 0024 0c0-8-6-15-12-25z"/><path d="M18 31a6 6 0 006 6"/>',
    "glass": '<path d="M14 12h20l-3 31H17z"/><path d="M14.6 19h18.8"/>'
             '<path d="M13 12c-1-4 3-6 6-4 1-3 7-3 8 0 3-2 7 0 6 4"/>',
    "bottle": '<path d="M20 3h8v9l4 6v24a2 2 0 01-2 2H18a2 2 0 01-2-2V18l4-6z"/><path d="M16 25h16v10H16"/>',
    "can": '<rect x="14" y="7" width="20" height="35" rx="3"/><path d="M14 13h20M14 36h20M20 22h8"/>',
    "keg": '<rect x="12" y="8" width="24" height="33" rx="4"/><path d="M12 16h24M12 33h24M21 8V4h6v4"/>',
    "tank": '<path d="M14 5h20v24l-10 11-10-11z"/><path d="M14 13h20M24 40v5M17 33l-4 12M31 33l4 12"/>',
    "kettle": '<path d="M10 19c0-7 6-11 14-11s14 4 14 11v15a4 4 0 01-4 4H14a4 4 0 01-4-4z"/><path d="M24 8V3M10 25h28M17 38v6M31 38v6"/>',
    "mill": '<path d="M11 6h26l-7 12H18z"/><circle cx="18" cy="27" r="5"/><circle cx="30" cy="27" r="5"/><path d="M16 42l4-6h8l4 6"/>',
    "thermo": '<path d="M21 30V8a3 3 0 016 0v22"/><circle cx="24" cy="35" r="6"/><path d="M24 30V16"/>',
    "flame": '<path d="M24 4c2 8 11 12 11 23a11 11 0 01-22 0c0-7 4-9 5-15 3 2 4 5 4 7 2-4 2-10 2-15z"/>',
    "snow": '<path d="M24 5v38M8 14.5l32 19M8 33.5l32-19"/><path d="M19 8l5 4 5-4M19 40l5-4 5 4"/>',
    "bolt": '<path d="M28 3L11 28h13l-4 17 17-25H24z"/>',
    "bug": '<ellipse cx="24" cy="27" rx="9" ry="12"/><path d="M24 15v24M15 22H8M15 30H8M15 36l-6 4M33 22h7M33 30h7M33 36l6 4M20 15l-3-6M28 15l3-6"/>',
    "sun": '<circle cx="24" cy="24" r="8"/>' + "".join(
        f'<path d="M24 24" transform="rotate({a} 24 24)"/><line x1="24" y1="5" x2="24" y2="11" transform="rotate({a} 24 24)"/>' for a in range(0, 360, 45)),
    "box": '<path d="M7 16l17-8 17 8v18l-17 8-17-8z"/><path d="M7 16l17 8 17-8M24 24v18"/>',
    "star": '<path d="M24 5l5.6 12 13 1.5-9.6 8.8 2.6 12.9L24 33.8 12.4 40.2 15 27.3 5.4 18.5l13-1.5z"/>',
    "coin": '<circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="12"/><path d="M19 18h10M19 22h10M22 18c5 0 5 8 0 8h-3l8 8"/>',
    "magnifier": '<circle cx="20" cy="20" r="12"/><path d="M29 29l13 13"/>',
    "clock": '<circle cx="24" cy="24" r="17"/><path d="M24 13v11l8 5"/>',
    "truck": '<path d="M3 13h25v19H3zM28 20h9l7 8v4H28"/><circle cx="12" cy="35" r="4"/><circle cx="35" cy="35" r="4"/>',
    "plate": '<circle cx="24" cy="28" r="15"/><circle cx="24" cy="28" r="9"/><path d="M18 9c-2 2 2 4 0 6M24 7c-2 2 2 4 0 6M30 9c-2 2 2 4 0 6"/>',
    "pencil": '<path d="M8 40l3-11L32 8l8 8-21 21z"/><path d="M28 12l8 8M8 40l11-3"/>',
    "question": '<circle cx="24" cy="24" r="17"/><path d="M18 19a6 6 0 1110 4c-3 2-4 3-4 6"/><circle cx="24" cy="35" r="1.2"/>',
    "arrow": '<path d="M6 24h32M28 13l11 11-11 11"/>',
    "check": '<circle cx="24" cy="24" r="17"/><path d="M15 24l6 6 12-13"/>',
    "wineglass": '<path d="M15 5h18c0 10-3 17-9 17s-9-7-9-17z"/><path d="M16 12h16M24 22v18M16 43h16"/>',
    "cask": '<path d="M13 6h22c3 6 3 30 0 36H13c-3-6-3-30 0-36z"/><path d="M11 15h26M11 33h26M10.5 24h27"/>',
    "grapes": '<path d="M24 3v6M24 9c3-4 8-4 10-2"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="4.5"/>' for x, y in
        ((15.5, 15), (24, 15), (32.5, 15), (19.8, 23), (28.2, 23), (24, 31), (24, 39))),
    "chart": '<path d="M6 42h36M6 42V6"/><path d="M12 34l9-10 7 6 12-15"/><path d="M34 15h6v6"/>',
    "people": '<circle cx="17" cy="16" r="6"/><circle cx="32" cy="18" r="5"/><path d="M5 40c0-8 5-13 12-13s12 5 12 13M28 29c6 0 11 4 11 11"/>',
}


def icon(name, size="10mm", colour="currentColor", width=2.6):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none" stroke="{colour}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round" style="display:block">{_P[name]}</svg>')


def _felt_tile():
    motifs = "".join(f'<g transform="translate({x} {y}) rotate({r} 24 24) scale(.55)" fill="none" stroke="#fff" stroke-width="2.6" '
                     f'stroke-linecap="round" stroke-linejoin="round" opacity=".07">{_P[n]}</g>'
                     for n, x, y, r in (("hop", 4, 4, -15), ("barley", 52, 40, 20), ("drop", 10, 64, 0), ("yeast", 62, 2, 10)))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96">{motifs}</svg>'
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


FELT_BG = (f"background-color:{FELT};background-image:url('{_felt_tile()}'),"
           f"radial-gradient(ellipse at 50% 40%,rgba(255,255,255,.08),rgba(0,0,0,.25));")

ART_CSS = f"""
.felt{{{FELT_BG}color:{FOAM}}}
.felt .foot{{color:rgba(255,248,236,.7)}}
.badge{{display:inline-flex;flex-direction:column;align-items:center;padding:3mm 9mm 2.5mm;background:{COPPER};
  border:1mm solid {GOLD};outline:.5mm solid {COPPER};outline-offset:.8mm;border-radius:7mm 7mm 3mm 3mm;
  box-shadow:0 1.5mm 0 {FELT_DARK}}}
.badge b{{font-family:"Alfa Slab One",serif;font-weight:400;font-size:26pt;line-height:1;color:{FOAM};
  text-shadow:.6mm .6mm 0 {STOUT};letter-spacing:.02em}}
.badge span{{font-size:9pt;color:{FOAM};margin-top:1mm;opacity:.95}}
.frame{{padding:3mm;background:{COPPER};border-radius:3mm;box-shadow:0 0 0 .8mm {GOLD},0 2.5mm 0 .8mm {FELT_DARK};display:inline-block}}
.frame>*{{display:block}}
.frame{{color:#1d2b30}}
.ruled~.foot{{left:52mm}}
.chips{{display:flex;justify-content:center;gap:5mm;margin-top:5mm}}
.chips div{{display:flex;align-items:center;gap:2mm;background:rgba(255,255,255,.08);border:.4mm solid rgba(233,185,73,.6);border-radius:20mm;padding:2mm 4mm;font-size:9pt;color:{FOAM}}}
.side{{position:absolute;left:0;top:0;bottom:0;width:46mm;{FELT_BG}color:{FOAM};padding:12mm 6mm 22mm;display:flex;flex-direction:column;align-items:center;gap:6mm;text-align:center}}
.side .stat{{display:flex;flex-direction:column;align-items:center;gap:1mm;font-size:9pt}}
.side .name{{font-family:"Alfa Slab One",serif;font-size:15pt;line-height:1.1;color:{GOLD}}}
.ruled{{margin-left:40mm}}
.ruled h1{{font-family:"Alfa Slab One",serif;font-weight:400;color:{FELT};font-size:24pt}}
.ruled h2{{font-family:"Alfa Slab One",serif;font-weight:400;color:{COPPER};font-size:13pt;margin:5mm 0 2mm}}
.gcard{{position:relative;border-radius:2.5mm;overflow:hidden;background:#fff;border:.35mm solid #c9c2b3;display:flex;flex-direction:column}}
.gcard .win{{display:flex;align-items:center;justify-content:center;position:relative}}
.gcard .title{{font-family:"Alfa Slab One",serif;font-weight:400;line-height:1.05}}
.back{{border-radius:2.5mm;{FELT_BG}display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2mm;color:{GOLD};
  box-shadow:inset 0 0 0 2mm {FELT},inset 0 0 0 2.6mm {GOLD}}}
.back b{{font-family:"Alfa Slab One",serif;font-weight:400;font-size:11pt;color:{FOAM};text-align:center;line-height:1.1;padding:0 3mm}}
"""


def badge(title, sub=""):
    return f'<div style="text-align:center"><div class="badge"><b>{title}</b>{f"<span>{sub}</span>" if sub else ""}</div></div>'


def board_page(title, sub, board, intro="", chips=()):
    """Body for a felt board page: badge, framed board, intro, game-box chips."""
    row = "".join(f'<div>{icon(i, "6mm", GOLD)}{t}</div>' for i, t in chips)
    return (f'{badge(title, sub)}<div style="text-align:center;margin-top:5mm"><div class="frame">{board}</div></div>'
            f'<p style="text-align:center;margin:5mm auto 0;max-width:150mm;color:{FOAM};font-size:10.5pt">{intro}</p>'
            f'<div class="chips">{row}</div>')


def side_strip(title, emblem, players, minutes, ages="12+"):
    stats = "".join(f'<div class="stat">{icon(i, "8mm", GOLD)}<span>{t}</span></div>'
                    for i, t in (("check", players), ("clock", minutes), ("star", f"Ages {ages}")))
    return (f'<div class="side"><div style="width:26mm;height:26mm;border-radius:50%;background:{COPPER};display:flex;align-items:center;'
            f'justify-content:center;box-shadow:0 0 0 1mm {GOLD}">{icon(emblem, "16mm", FOAM)}</div>'
            f'<div class="name">{title}</div>{stats}<div style="margin-top:auto;font-size:8pt;opacity:.8">Print, cut, play.<br>craftbeerschool.in</div></div>')


def gcard(colour, ic, kicker, title, text, h=40, win=14, tint=None):
    """Framed game card: coloured header window with an icon, slab title, body text."""
    tint = tint or colour
    return (f'<div class="gcard" style="height:{h}mm;box-shadow:inset 0 0 0 1.2mm {colour}">'
            f'<div class="win" style="height:{win}mm;background:radial-gradient(circle at 50% 60%,rgba(255,255,255,.28),rgba(0,0,0,.12)),{tint}">'
            f'{icon(ic, f"{win * .62:.1f}mm", FOAM)}'
            f'<span style="position:absolute;left:2.5mm;top:1.8mm;font-size:5.8pt;color:{FOAM};opacity:.9">{kicker}</span></div>'
            f'<div style="padding:1.8mm 3mm 2.5mm;display:flex;flex-direction:column;gap:.8mm;flex:1">'
            f'<div class="title" style="font-size:10pt;color:{FELT}">{title}</div>'
            f'<div style="font-size:7.2pt;line-height:1.3;color:#33403f">{text}</div></div></div>')


def backs(n, title, ic, h, cols=3):
    one = f'<div class="back" style="height:{h}mm">{icon(ic, "13mm", GOLD)}<b>{title}</b></div>'
    return f'<div class="grid" style="grid-template-columns:repeat({cols},1fr);margin-top:3mm">{one * n}</div>'


def svg_icon(name, x, y, size, colour, width=2.6):
    """The same icon as a <g> for drawing inside another SVG (x, y = top left)."""
    k = size / 48
    return (f'<g transform="translate({x} {y}) scale({k})" fill="none" stroke="{colour}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round">{_P[name]}</g>')
