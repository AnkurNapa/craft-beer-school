"""House-style batch: 20 guides written in the brewing house style (built from the
New Brewer archive), published together on 7 October 2026.
Rerun is safe: it replaces its own rows (batch "house-style-1") and leaves every other row alone."""
import json, pathlib

here = pathlib.Path(__file__).parent
BATCH, DATE = "house-style-1", "2026-10-07"
STAGE = {"a": "awareness", "c": "consideration", "d": "decision"}
COURSE = {
    "Professional brewers": "advanced-brewing-science-course.html",
    "Founders": "brewery-business-management-course.html",
    "Brand builders": "beer-branding-packaging-course.html",
    "Beer lovers": "sensory-evaluation-course.html",
}

# segment|cat|slug|h1|stage, optionally |course override
ROWS = """Professional brewers|Brewing science|root-cause-analysis-for-brewers|Root cause analysis: stop solving the same brewery problem twice|c
Professional brewers|Brewing science|forced-ageing-tests|Forced ageing tests: tasting month three in week one|c
Professional brewers|Brewing science|spunding-explained|Spunding: carbonating with your own fermentation CO2|c
Professional brewers|Brewing science|monotanking-in-a-unitank|Monotanking: fermenting, conditioning and serving from one tank|c
Professional brewers|Brewing science|yeast-nutrition-zinc-and-fan|Yeast nutrition: zinc and FAN do most of the work|c
Professional brewers|Brewing science|thiolized-yeast-explained|Thiolized yeast and biotransformation, explained|a
Professional brewers|Brewing science|trialling-a-new-hop-variety|Trialling a new hop without risking your flagship|c
Professional brewers|Brewing science|control-charts-for-brewers|Control charts for brewers: noise or a real problem|c
Professional brewers|Brewing science|cip-water-and-chemical-savings|Cutting CIP water and chemicals without cutting corners|c
Professional brewers|Brewing science|standard-work-on-brew-day|Standard work: taking an hour out of brew day|c
Professional brewers|Ingredients|regenerative-barley-and-sustainable-malt|Regenerative barley and sustainable malt: what a brewer can ask for|a
Founders|Business|flagship-beer-strategy|Why a brewery needs a flagship, and when to retire one|c
Founders|Business|preventive-maintenance-plan-brewery|A preventive maintenance plan for a small brewery|c
Founders|Business|keg-tracking-and-losses|Keg tracking: stop losing kegs and the money inside them|c
Founders|Business|beer-recall-plan|Planning a beer recall before you need one|c
Founders|Business|brewery-safety-culture|Building a safety culture in a small brewery|c|safety-in-brewing-course.html
Founders|Business|brewer-burnout|Burnout in brewing: spotting it before you lose a good brewer|a
Brand builders|Branding|bringing-back-a-retired-beer|Bringing back a retired beer: nostalgia as a sales tool|a
Brand builders|Branding|younger-drinkers-and-craft-beer|What younger drinkers want from craft beer|a
Beer lovers|Styles|cold-ipa-explained|Cold IPA: the lager-brewed IPA, explained|a"""


def main():
    plan = [p for p in json.loads((here / "plan.json").read_text()) if p.get("batch") != BATCH]
    rows = [line.split("|") for line in ROWS.splitlines()]
    slugs = [r[2] for r in rows]
    for i, (seg, cat, slug, h1, st, *course) in enumerate(rows):
        peers = [r[2] for r in rows if r[1] == cat and r[2] != slug]
        peers += [p["slug"] for p in plan if p["cat"] == cat and p["date"] < DATE][:3 - len(peers)] if len(peers) < 3 else []
        start = peers.index(slugs[(i + 1) % len(slugs)]) if slugs[(i + 1) % len(slugs)] in peers else 0
        plan.append({"slug": slug, "h1": h1, "cat": cat, "course": course[0] if course else COURSE[seg],
                     "related": [peers[(start + j) % len(peers)] for j in range(min(3, len(peers)))],
                     "segment": seg, "stage": STAGE[st], "batch": BATCH, "date": DATE})
    assert len({p["slug"] for p in plan}) == len(plan), "duplicate slug"
    (here / "plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))
    print(len(rows), "rows,", len(plan), "total")


if __name__ == "__main__":
    main()
