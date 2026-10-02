# Writer brief: Craft Beer School seeded articles

You are writing guides for craftbeerschool.in, an Indian online beer school. Each
guide is one JSON file at `content/articles/<slug>.json`. Your batch of slugs is in
your task prompt. Every guide's plan (h1, category, segment, funnel stage, course,
related slugs, date) is in `content/plan.json`. Use those values exactly.

## Read these first

1. `~/.claude/skills/humanizer/SKILL.md` and `~/.claude/skills/humanizer/references/patterns.md`. Apply them silently to everything you write.
2. The reference guide, to match voice and depth:
   `python3 -c "import articles_a,json;print(json.dumps(articles_a.ARTICLES_A[3],indent=1,ensure_ascii=False))"`
   Run it from `/Users/ankurnapa/Documents/craft-beer-school`.

## Voice

- The school speaks as "we": working brewers who teach. Plain, direct, practical. A little dry wit is fine. No hype.
- Write for the plan's `segment`. A beer lover needs no jargon. A professional brewer wants numbers and mechanisms.
- Ground it in India where it is natural: heat, the cold chain, borewell and municipal water, rice and maize adjuncts, rupees, state-by-state excise, Indian food. Do not force it into every paragraph.
- One concrete brewhouse-floor detail per guide, used precisely. For example, a real temperature, a real piece of kit or a real failure. Not five.
- British English throughout: colour, flavour, litre, optimise, sanitise, pasteurise, analyse, fibre, grey, mould, programme, centre.

## Hard rules (the validator enforces these)

- No em dash, en dash, curly quotes or double spaces anywhere. Use commas, colons, full stops or parentheses. Straight quotes only.
- None of these words: delve, tapestry, landscape, seamless, unlock, empower, leverage, pivotal, crucial, embark, elevate, game changer, testament, realm, "in conclusion", "it's important to note".
- Avoid the other tells too: "not just X but Y", rule-of-three padding, "serves as", closing summaries, rhetorical-question openers.
- Accuracy first. Use standard, well-established brewing values (for example ABV = (OG - FG) x 131.25, lager fermentation around 8 to 13 °C, mash pH 5.2 to 5.6). Never invent statistics, studies, surveys, named experts, quotes, prices, licence fees or legal section numbers. For Indian regulation, describe the process and say that rules and fees vary by state and change, so readers should check the current notification or ask a licensing consultant.
- No medical or health claims about beer. Nothing that encourages heavy or underage drinking.

## JSON shape (exactly these keys)

```json
{
 "slug": "<slug>",
 "cat": "<plan cat>",
 "h1": "<plan h1, you may polish wording but keep the meaning>",
 "title": "<under 60 chars total, ending exactly ' | Craft Beer School'>",
 "desc": "<meta description, 50 to 160 chars, says what the reader gets>",
 "teaser": "<one or two short sentences for the card, makes someone click>",
 "standfirst": "<two or three sentences under the headline, the promise of the piece>",
 "read": "<N min, where N = round(body words / 200), minimum 3>",
 "updated": "<plan date, YYYY-MM-DD>",
 "updated_label": "<Month YYYY of that date, e.g. October 2021>",
 "sections": [["<sentence-case heading>", "<p>HTML body</p>"], "... 5 to 8 sections"],
 "faqs": [["<question?>", "<plain-text answer, 1 to 3 sentences>"], "... 3 or 4"],
 "cta": {"title": "...", "body": "...", "href": "<plan course>", "label": "..."},
 "related": ["<exactly the plan's related list>"]
}
```

- Body total 650 to 1200 words across sections. Aim for about 800.
- Section HTML may use only `<p> <strong> <em> <ul> <ol> <li> <a> <br>`. Headings are sentence case.
- Include one to three internal links inside the body, `<a href="<slug>.html">`, to other slugs in `content/plan.json` or to these existing guides: what-is-craft-beer, beer-styles-guide, how-to-taste-beer, beer-off-flavours, craft-beer-in-india, start-a-microbrewery-india, become-a-brewer-india, brewing-for-india. Link where a reader would genuinely want to go next.
- Date-appropriate: the guide is dated at its plan date. Do not mention events after that date or call anything "new in 2026" in a 2022 piece.

## The funnel (the CTA is the point of the piece)

The CTA sells the course at the plan's `course` page. Its copy depends on the plan's `stage`:

- `awareness`: the reader is curious, not shopping. Soft. Title names the next thing they would enjoy learning. Body says what the course covers in one or two sentences. Label: "See what the course covers".
- `consideration`: the reader is trying to do the thing. Title names the problem the course solves. Body names the course, its length and what it teaches that this guide could not. Label: "See the full syllabus".
- `decision`: the reader is planning a move (a brewery, a career, going pro). Direct. Title is an invitation. Body: live weekend classes, max 20 per batch, certificate. Label: "Save your seat".

The CTA is shown twice (mid-article and at the end), so it must read well in both places. Also let the body earn it: at least one moment in the guide should make the reader feel the gap that the course fills, without turning into an advert.

Course facts you may use: all courses are live online on Saturdays and Sundays, 12:00 PM to 2:00 PM IST, max 20 students, with recordings, weekly assignments and a certificate. Durations and fees: Brewing Fundamentals 4 weeks, Rs 5,999; Advanced Brewing Science 6 weeks, Rs 12,999; Brewery Business Management 3 weeks, Rs 8,999; Style Specialization 8 weeks, Rs 18,999; Beer Branding & Packaging 3 weeks, Rs 4,999; Sensory Evaluation 2 weeks, Rs 5,999; AI for Craft Breweries 2 weeks, Rs 5,000; Digital Transformation Basics for Brewing 2 weeks, Rs 5,000; ESG in Craft Brewing 2 weeks, Rs 5,000; Safety in Brewing 1 week, free; Craft Distilling 4 weeks, Rs 9,999; Craft Gin Making 4 weeks, Rs 9,999; RTD Drinks 2 weeks, Rs 5,000; Hop Water 2 weeks, Rs 5,000; Hard Seltzer 2 weeks, Rs 5,000; Kombucha 2 weeks, Rs 5,000; Non-Alcoholic Beer 2 weeks, Rs 5,000. In person in Bengaluru: Professional Beer Tasting Day, 1 day, Rs 4,999 with beers; Brewery Business Tour, half day, on enquiry. Write the rupee sign as ₹. Do not mention fees in pieces dated before 2026 (prices change), and never promise refunds or discounts.

## Workflow

1. Write each file (use the Write tool, or a short Python script with `json.dump(..., ensure_ascii=False, indent=1)`).
2. Run `python3 validate_articles.py <your slugs...>` from the repo folder. Fix every failure and rerun until your whole batch passes.
3. Reread two of your guides as a sceptical brewer would. Fix anything vague, wrong or AI-sounding.
4. Only touch your own slugs' files. Do not edit any other file in the repo.
5. Report back in five lines or fewer: how many passed, and anything you were unsure was factually right.

## Corporate teams segment (plan segment "Corporate teams")

These 44 guides are for people who work inside beer, wine and spirits companies but have never made the product: GCC analysts, planners, buyers, finance, marketing, technology and new joiners in Bengaluru, Pune and Hyderabad. They cover beer, whisky and wine, not only beer.

- Write for a smart professional with no production background. Explain each term once, then use it. Connect the product to their desk: what the number in their dashboard means on the floor, why a forecast or a stock plan behaves the way it does.
- Whisky and wine facts must be as accurate as the brewing ones. Standard, well-established values only (for example: whisky in Scotland must age at least three years in oak; Indian heat raises evaporation loss well above Scotland's commonly quoted ~2% a year; wine yeast converts grape sugar to alcohol; red wine gets its colour from skins). No invented market sizes, shares, rankings or company figures. Name real regions and grape varieties; do not name a specific company's plant, numbers or calibration.
- Indian regulation: process level only, rules vary by state and change, check the current notification. Never legal advice.
- Tastings: always responsible, opt-in, within company policy, with non-drinkers welcome and spit cups. No encouragement to drink more.
- No serial comma and no ", and" joins: write "malt, hops and water", and split a sentence rather than join two clauses with ", and".
- CTA (href is `contact.html?course=Corporate%20training#enroll`, the enquiry form with Corporate training pre-selected). It sells a programme to a team, not a seat to an individual:
  - `awareness`: title names what the reader's team would gain from knowing this. Body: we run beverage training for drinks companies and GCC teams, modules like Beverage 101 and guided sensory sessions. Label: "Ask about team training" (the button opens the enquiry form).
  - `consideration`: title names the work problem (bad forecasts, KPIs nobody can explain). Body names the relevant module (Beverage 101; Brewing and distilling operations; Raw materials and supply chain; Route to market and regulation in India; Guided sensory sessions; Data and AI in beverages) and says it is built around the team's own portfolio. Label: "Plan a programme".
  - `decision`: direct invitation to a team lead or L&D manager. Body: programmes run on-site in Bengaluru, Pune and Hyderabad or live online, sized to the team. Label: "Plan a programme".
- Never quote corporate fees. Internal links may also point at `for-companies.html` and the other corporate slugs in the plan.

## Drinks producers segment (plan segment "Drinks producers", cat "Consultancy")

26 guides for owners, founders, head brewers and product teams of breweries, brewpubs, cideries, distilleries, wineries and drinks brands in India that are open, opening or struggling. Each plan row has a `by` field: the guide is bylined to Rahul Baliyan (mentor-rahul-baliyan.html: Weihenstephan-trained German-style Brewmaster, M.Tech. Food Biotechnology, a decade as Consultant Brew Master in North India, on 10 hl brewhouses; start-ups, excise compliance, team supervision, yield and raw material sourcing) or Ankur Napa (mentor-ankur-napa.html: Master Brewer who also works in data and AI; quality systems, costing, data, AI). Write in the school's "we" voice in the author's area of expertise.

- Never invent case studies, client names, before-and-after numbers or personal anecdotes presented as real. "In consulting work we often see..." followed by a general, well-known pattern is fine. Do not name any venue, client or brand.
- Practical and specific: checklists, the order to do things in, the numbers to measure and typical healthy ranges from standard brewing practice. A brewer should finish the guide knowing what to check tomorrow.
- Excise and licensing: process level only, state rules vary and change, work with a licensing adviser. No section numbers, rates or fees.
- No serial comma and no ", and" joins.
- CTA href is `contact.html?course=Brewery%20consultancy#enroll` (the enquiry form with Brewery consultancy pre-selected). It sells a consultation, not a course:
  - `awareness`: title names what the owner would gain. Body: our consultant brewers work with breweries and brewpubs on site or remotely. Label: "Talk to a consultant brewer".
  - `consideration`: title names the problem. Body names the work (for example a yield and loss review, commissioning support, a quality system set-up), who leads it (Rahul on brewing, Ankur on quality, cost and data) and that it leaves the team able to run it. Label: "Book a consultation".
  - `decision`: direct invitation to the owner. Body: we start with a brewery health check and a written action plan. Label: "Book a consultation".
- Never quote consultancy fees or promise outcomes (no "raise yield by X%").
- Internal links may also point at `for-companies.html` and other plan slugs, including existing guides such as brewhouse-efficiency, brewery-qc-lab-on-a-budget, brewery-failure-reasons, cost-per-litre-beer, taproom-economics.
