# Writer brief: Style Library cards

The Style Library is a set of 80 short, structured style cards on craftbeerschool.in,
one page per style. Each card is one JSON file at `content/styles/<slug>.json`. Your
batch of slugs is in your task prompt. The facts for every style (name, family,
colour/bitterness/ABV ranges, linked long guide, similar styles) are in
`content/styles_plan.json`. The page renders those numbers itself, so you do not
repeat them as a list, but you may mention one in the prose where it helps.

## Why this exists, and the one rule that matters most

We researched these styles from CraftBeer.com (the Brewers Association's consumer
site). Our version must be our own. Do **not** open, quote or paraphrase their text
sentence by sentence. Write each card from brewing knowledge, as a working Indian
brewer would describe the beer to a curious drinker. The validator rejects any run
of 7 or more words that matches their text, but the spirit goes further: different
angle, different examples, different pairings, our own voice.

## Read these first

1. `~/.claude/skills/humanizer/SKILL.md` and `~/.claude/skills/humanizer/references/patterns.md`. Apply them silently.
2. `content/WRITER_BRIEF.md` for the school's voice and hard rules. All of its Voice and Hard rules sections apply here too (we, plain, practical, British English, no em/en dashes, no curly quotes, no banned words, no invented facts, no health claims).
3. One existing long guide, to match voice: `python3 -c "import json;print(json.load(open('content/articles/west-coast-ipa.json'))['sections'][0])"`

## JSON shape (exactly these keys)

```json
{
 "slug": "<plan slug>",
 "name": "<display name; you may tidy it, e.g. 'German Pilsner', 'Kolsch', 'Irish Red Ale'>",
 "family": "<plan family, exactly>",
 "title": "<under 60 chars, ending exactly ' | Craft Beer School', e.g. 'Kolsch: Style Guide | Craft Beer School'>",
 "desc": "<meta description, 50 to 160 chars>",
 "tagline": "<one line under the name, max 120 chars, our take on the beer>",
 "tastes": "<p>...</p><p>...</p> 120 to 220 words: what it tastes like, where it comes from, what makes it itself>",
 "profile": {
   "look": "<colour, clarity, head, in our words, max 40 words>",
   "aroma_flavour": "<malt, hops, yeast character, max 40 words>",
   "mouthfeel": "<body, carbonation, finish, max 40 words>",
   "ingredients": "<typical malts, hops, yeast, water or adjuncts, max 40 words>"
 },
 "glass": "<one of: Pint, Nonic pint, Tulip, Snifter, Pilsner glass, Stange, Weizen glass, Goblet, Teku, Willi becher, Thistle, Stemmed glass>",
 "serve_c": "<serving range in whole degrees C, e.g. '4-7'; your own call as a brewer>",
 "in_india": "<p>50 to 120 words: drinking or brewing this style in India. Heat and the cold chain, how it travels, whether you will find it on tap, what it suits (monsoon, summer afternoon, a wedding), rice or local ingredients if natural.</p>",
 "pairings": [
   {"food": "<an Indian dish>", "why": "<one sentence on why it works: contrast, cut, echo, cool the chilli>"},
   "... 3 or 4 total. At least one vegetarian main, one dessert or mithai. Cover more than one region of India across your batch. A cheese is fine if it is easy to buy in India."
 ],
 "examples": [
   {"beer": "<beer name>", "brewery": "<Indian brewery>", "source": "<URL that shows this brewery makes or made this beer>"},
   "... 0 to 3"
 ],
 "examples_note": "<required if examples is empty, e.g. 'Rare in India so far. Ask your local brewpub, several brew one as a seasonal.' Otherwise an empty string.>"
}
```

## Indian examples: verified or nothing

Use WebSearch (and WebFetch if needed) to find Indian craft beers of this style:
packaged brands (Bira 91, Simba, White Owl, Kati Patang, Bombay Duck, Witlinger, Great
State Ale Works, Geist, Medusa, Independence Brewing, Brewhouse by Bombay Duck and so
on) and well-known brewpubs (Toit, Arbor, Windmills, Byg Brewski, Doolally, Gateway,
Brewbot, Effingut, Prost, 1 Ki Tchn and others). Only list a beer if a page you
actually opened (brewery site, menu, Untappd, a news article) shows that brewery makes
or made it, and put that URL in `source`. Brewpub rotating beers are fine if a source
shows them. If you cannot verify one, leave `examples` empty and write an honest
`examples_note`. A wrong brand name on our site is worse than none.

## Numbers

Read the plan's srm/ibu/abv for your style. If one disagrees clearly with current
BJCP or BA guidelines as you know them, do not change the plan; mention it in your
final report.

## Workflow

1. Write each file with `json.dump(..., ensure_ascii=False, indent=1)` or the Write tool.
2. Run `python3 validate_styles.py <your slugs...>` from `/Users/ankurnapa/Documents/craft-beer-school`. Fix every failure and rerun until your whole batch passes.
3. Reread two cards as a sceptical Indian brewer would. Fix anything vague, wrong, generic or AI-sounding. Pairings must be specific dishes (Chettinad chicken, dal makhani, Goan prawn balchao), not "spicy food".
4. Only touch your own slugs' files. Do not edit any other file.
5. Report in five lines or fewer: how many pass, how many have verified Indian examples, and any number or fact you doubted.
