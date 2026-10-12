# Translator brief: Craft Beer School in Hindi, Marathi, Telugu and Kannada

You translate packs of website text for craftbeerschool.in, an Indian beer school.

## Files

- Input pack: `content/i18n/todo/<lang>-NNN.json`, an object of `"key": "English text or HTML"`.
- Output: `content/i18n/done/<lang>-NNN.json`, the same keys, every value translated.
- Languages: `hi` Hindi, `mr` Marathi, `te` Telugu, `kn` Kannada, each in its own script.

## Markup must survive exactly

- Many values contain HTML: `<a href="...">`, `<strong>`, `<em>`, `<span class="...">`, `<br>`. Keep every tag, every attribute and every `href` exactly as it is, in the same order where the grammar allows. Translate only the visible text between tags.
- Never add, drop or change a tag, class, id, URL, `data-` attribute or entity.
- A merge script rejects any value whose tags or links differ from the English.

## What to keep in English (Latin script)

- Brewing and drinks terms brewers in India use in English: IPA, lager, ale, stout, porter, hefeweizen, saison, mash, wort, boil, hops, malt, yeast, ABV, IBU, EBC, SRM, OG, FG, pH, CIP, kveik, dry hop, brewhouse, fermenter, unitank, keg, can, sensory, off-flavour names. You may add a short native word before or after the English term when it helps, for example `मैश (mash)`.
- Product, brand and company names: Fermentis, SafAle US-05, Weyermann, CARAMUNICH, Citra, Craft Beer School, WSET, BJCP, Cicerone, FSSAI.
- Brewery, venue and beer names: Toit, Doolally, Effingut, Tint-In-Wit, and so on.
- People's names may be written in the target script (Ankur Napa as अंकुर नापा) except inside links and bylines, where you keep them as they appear.
- Course names: translate the description, keep the course name in English followed by a translation in brackets the first time it appears in a value only when it reads naturally. A value that is only a course name (a button, a menu item) stays in English.
- Numbers, °C and °F, units (litres, hl, kg, %), prices (₹5,000, Rs 1,999), dates and times stay as written.
- City and state names go in the target script (Pune as पुणे, Bengaluru as बेंगलुरु / ಬೆಂಗಳೂರು / బెంగళూరు).

## Voice

- Plain, warm, conversational, as a working brewer who teaches would speak to someone in that language. Avoid stiff, Sanskritised officialese in Hindi and Marathi; everyday words that people actually use are better. Mixed usage with English drinks terms is fine and expected.
- Keep it short where the English is short: buttons, menu items, labels and chips stay brief.
- Do not add or drop meaning. Do not add marketing claims. Keep responsible-drinking lines exactly as strong as the English.
- Punctuation: no em dashes, no en dashes, no curly quotes. Use the target language's normal full stop (। in Hindi and Marathi is fine) and straight quotes.

## Values that are only a proper noun

If a value is only a brewery name, a beer name, a person's name or a product code, return it unchanged.

## Check before you finish

Write a short python3 check that, for each pack you did: the output has exactly the input's keys; every value is non-empty; the list of HTML tags and the list of href values match the input; no em dash, en dash or curly quote appears. Fix and re-run until clean.
