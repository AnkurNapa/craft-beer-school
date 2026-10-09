"""Weyermann malt series: one guide per Weyermann malt plus a hub, published 9 October 2026.
Each row carries `malt` and `wheel` so the page shows Weyermann's Malt Aroma Wheel for that malt.
Rerun is safe: it replaces its own rows (batch "weyermann-1") and leaves every other row alone."""
import json, pathlib

here = pathlib.Path(__file__).parent
BATCH, DATE, HUB = "weyermann-1", "2026-10-09", "weyermann-malts-guide"
COURSE = "advanced-brewing-science-course.html"

# group|slug|malt name as printed|h1|wheel (assets/weyermann/<file>.webp, "-" for none)
ROWS = """Base|weyermann-pilsner-malt|Pilsner Malt|Weyermann Pilsner malt: the base for clean, pale lagers|pilsner-malt
Base|weyermann-extra-pale-premium-pilsner-malt|Extra Pale Premium Pilsner Malt|Weyermann Extra Pale Premium Pilsner malt: for the palest beers|extra-pale-premium-pilsner-malt
Base|weyermann-bohemian-pilsner-malt|Bohemian Pilsner Malt|Weyermann Bohemian Pilsner malt: Czech character in the grist|bohemian-pilsner-malt
Base|weyermann-floor-malted-bohemian-pilsner-malt|Floor-Malted Bohemian Pilsner Malt|Weyermann Floor-Malted Bohemian Pilsner malt: the old way of malting|floor-malted-bohemian-pilsner-malt
Base|weyermann-floor-malted-bohemian-dark-malt|Floor-Malted Bohemian Dark Malt|Weyermann Floor-Malted Bohemian Dark malt: for Czech dark lagers|floor-malted-bohemian-dark-malt
Base|weyermann-barke-pilsner-malt|Barke Pilsner Malt|Weyermann Barke Pilsner malt: a heritage barley in a modern lager|barke-pilsner-malt
Base|weyermann-eraclea-pilsner-malt|Eraclea Pilsner Malt|Weyermann Eraclea Pilsner malt: an Italian barley for pale beers|eraclea-pilsner-malt
Base|weyermann-isaria-1924-malt|Isaria 1924|Weyermann Isaria 1924 malt: brewing with a 100-year-old barley|isaria-1924
Base|weyermann-pale-ale-malt|Pale Ale Malt|Weyermann Pale Ale malt: a fuller base for ales|pale-ale-malt
Base|weyermann-diastatic-barley-malt|Diastatic Barley Malt|Weyermann Diastatic Barley malt: extra enzymes for adjunct-heavy mashes|diastatic-barley-malt
Kilned|weyermann-vienna-malt|Vienna Malt|Weyermann Vienna malt: golden colour and a toasty backbone|vienna-malt
Kilned|weyermann-barke-vienna-malt|Barke Vienna Malt|Weyermann Barke Vienna malt: heritage barley, kilned for Vienna lager|barke-vienna-malt
Kilned|weyermann-munich-malt|Munich Malt Type 1 and Type 2|Weyermann Munich malt Type 1 and Type 2: choosing the right one|munich-malt
Kilned|weyermann-barke-munich-malt|Barke Munich Malt|Weyermann Barke Munich malt: deep malt flavour from a heritage barley|barke-munich-malt
Kilned|weyermann-brewing-malt-type-cologne|Brewing Malt Type Cologne|Weyermann Brewing Malt Type Cologne: a base malt built for Kolsch|brewing-malt-type-cologne
Caramel|weyermann-carapils-malt|CARAPILS|Weyermann CARAPILS: body and foam without colour|carapils
Caramel|weyermann-carahell-malt|CARAHELL|Weyermann CARAHELL: light caramel for pale beers|carahell
Caramel|weyermann-carafoam-malt|CARAFOAM|Weyermann CARAFOAM: a foam and body malt for pale beers|carafoam
Caramel|weyermann-carabohemian-malt|CARABOHEMIAN|Weyermann CARABOHEMIAN: the caramel malt behind Czech amber lagers|carabohemian
Caramel|weyermann-caramunich-malt|CARAMUNICH Type 1, 2 and 3|Weyermann CARAMUNICH Type 1, 2 and 3: amber caramel, three depths|caramunich
Caramel|weyermann-caraamber-malt|CARAAMBER|Weyermann CARAAMBER: amber colour with a bready finish|caraamber
Caramel|weyermann-carared-malt|CARARED|Weyermann CARARED: red colour without roast|carared
Caramel|weyermann-caraaroma-malt|CARAAROMA|Weyermann CARAAROMA: the darkest caramel for big malt aroma|caraaroma
Caramel|weyermann-carabelge-malt|CARABELGE|Weyermann CARABELGE: caramel for Belgian ales|carabelge
Caramel|weyermann-carawheat-malt|CARAWHEAT|Weyermann CARAWHEAT: caramel malt from wheat|carawheat
Caramel|weyermann-cararye-malt|CARARYE|Weyermann CARARYE: caramel malt from rye|cararye
Caramel|weyermann-abbey-malt|Abbey Malt|Weyermann Abbey malt: biscuit and honey for Belgian ales|abbey-malt
Caramel|weyermann-melanoidin-malt|Melanoidin Malt|Weyermann Melanoidin malt: decoction-style depth without the decoction|melanoidin-malt
Caramel|weyermann-special-w-malt|Special W|Weyermann Special W: dark caramel with a dried-fruit edge|special-w
Roasted|weyermann-carafa-malt|CARAFA Type 1, 2 and 3|Weyermann CARAFA Type 1, 2 and 3: roasted malt for dark beers|carafa
Roasted|weyermann-carafa-special-malt|CARAFA SPECIAL Type 1, 2 and 3|Weyermann CARAFA SPECIAL: dark colour with less roast bite|carafa-special
Roasted|weyermann-roasted-barley|Roasted Barley|Weyermann Roasted Barley: the dry roast of a stout|roasted-barley
Roasted|weyermann-chocolate-wheat-malt|Chocolate Wheat Malt|Weyermann Chocolate Wheat malt: dark wheat for dunkels and porters|chocolate-wheat-malt
Roasted|weyermann-chocolate-rye-malt|Chocolate Rye Malt|Weyermann Chocolate Rye malt: roast with a spicy edge|chocolate-rye-malt
Grains|weyermann-pale-wheat-malt|Wheat Malt Pale|Weyermann Pale Wheat malt: the heart of a Hefeweizen|pale-wheat-malt
Grains|weyermann-dark-wheat-malt|Wheat Malt Dark|Weyermann Dark Wheat malt: for Dunkelweizen and Weizenbock|dark-wheat-malt
Grains|weyermann-pale-rye-malt|Rye Malt Pale|Weyermann Pale Rye malt: spice, body and a lautering challenge|pale-rye-malt
Grains|weyermann-spelt-malt|Spelt Malt|Weyermann Spelt malt: brewing with an ancient wheat|spelt-malt
Smoked|weyermann-beech-smoked-barley-malt|Beech Smoked Barley Malt|Weyermann Beech Smoked Barley malt: the Bamberg Rauchbier malt|beech-smoked-barley-malt
Smoked|weyermann-oak-smoked-wheat-malt|Oak Smoked Wheat Malt|Weyermann Oak Smoked Wheat malt: a gentler smoke for Grodziskie and more|oak-smoked-wheat-malt
Acid|weyermann-acidulated-malt|Acidulated Malt|Weyermann Acidulated malt: lowering mash pH the natural way|acidulated-malt
Acid|weyermann-sour-wort|Sour Wort|Weyermann Sour Wort: biological acidification in a can|-
Extract|weyermann-sinamar-and-malt-extracts|SINAMAR and malt extracts|Weyermann SINAMAR and malt extracts: colour and wort from a can|-"""

HUB_ROW = f"Hub|{HUB}|Weyermann malts|Weyermann malts: a brewer's guide to every malt in the range|-"


def main():
    plan = [p for p in json.loads((here / "plan.json").read_text()) if p.get("batch") != BATCH]
    rows = [line.split("|") for line in [HUB_ROW] + ROWS.splitlines()]
    for grp, slug, malt, h1, wheel in rows:
        peers = [r[1] for r in rows if r[0] == grp and r[1] != slug]
        if slug == HUB:
            related = ["weyermann-pilsner-malt", "weyermann-caramunich-malt", "weyermann-carafa-special-malt"]
        else:
            # Hub first, then two from the same group; a small group borrows from the whole series.
            others = peers + [r[1] for r in rows[1:] if r[1] != slug and r[1] not in peers]
            related = [HUB] + others[:2]
        row = {"slug": slug, "h1": h1, "cat": "Ingredients", "course": COURSE, "related": related,
               "segment": "Professional brewers", "stage": "awareness" if slug == HUB else "consideration",
               "batch": BATCH, "date": DATE, "malt": malt}
        if wheel != "-":
            row["wheel"] = f"assets/weyermann/{wheel}.webp"
        plan.append(row)
    assert len({p["slug"] for p in plan}) == len(plan), "duplicate slug"
    (here / "plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))
    print(len(rows), "rows,", len(plan), "total")


if __name__ == "__main__":
    main()
