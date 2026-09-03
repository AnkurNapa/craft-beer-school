# -*- coding: utf-8 -*-
"""Article records, part one: the awareness and craft cluster.

All prose here is original. Reference material in the vault (vendor datasheets,
third party fault guides, licensed formulation tables, scraped recipe sets) was
used only as background reading. No dataset, spec table or recipe from any of
it is reproduced, and no source is named, because this is a commercial site.
"""

ENROL = "contact.html#enroll"
COURSES = "courses.html"

WHAT_IS_CRAFT_BEER = dict(
    slug="what-is-craft-beer",
    cat="Start here",
    h1="What is craft beer, really?",
    title="What Is Craft Beer? A Beginner's Guide | Craft Beer School",
    desc="What craft beer actually means, how it differs from mass market lager, "
         "and what to drink first. A plain English guide for Indian beer drinkers.",
    teaser="Four ingredients, one process, and a lot of marketing noise. Here is "
           "what the word actually means.",
    standfirst="The word gets used to sell everything from a genuine small batch "
               "saison to a mass produced lager in a fancier can. The difference is "
               "not the label. It is what happens in the brewhouse.",
    read="7 min", updated="2026-09-03", updated_label="September 2026",
    sections=[
        ("Beer is four ingredients", """
<p>Every beer you have ever drunk is built from water, malted grain, hops and
yeast. That is the whole list. Everything else, every aroma, every colour, every
bit of bitterness, comes from how a brewer handles those four things.</p>
<p>Water is the bulk of it, around 90 per cent of what is in the glass, and its
mineral content quietly decides whether a beer tastes crisp or soft. Malted
barley provides the sugar the yeast will eat, plus the colour and most of the
body. Hops add bitterness to balance that sugar, along with aroma that can run
from pine to mango depending on the variety. Yeast does the actual work, turning
sugar into alcohol and carbon dioxide, and throwing off flavour compounds while
it does.</p>
<p>Change the ratio of those four and you change the beer completely. That is
why a stout and a pilsner can share an ingredient list and taste nothing
alike.</p>"""),
        ("So what makes a beer craft?", """
<p>There is no single legal definition, and in India there is no official one at
all. In practice, three things separate craft from commodity brewing.</p>
<p><strong>Scale.</strong> Craft brewers work in batches small enough that a
single decision, a mash temperature, a hop addition, changes the beer noticeably.
At industrial volume the priority is that every batch tastes identical to the
last one.</p>
<p><strong>Intent.</strong> A craft brewery is usually trying to make a specific
beer, sometimes an awkward one that will only appeal to some people. A commodity
brewery is trying to make a beer that offends nobody.</p>
<p><strong>Ingredient choice.</strong> Mass lager often uses rice or maize
alongside barley, partly for a lighter body and partly because it is cheaper.
Craft brewing tends to use more malt, more hops, and pays for both.</p>
<p>None of that makes craft automatically better. It makes it different, and
usually more expensive to produce.</p>"""),
        ("Craft versus the lager you grew up with", """
<p>Most Indian drinkers arrive at craft beer from strong lager. The jump can be
jarring, so it helps to know what is actually changing.</p>
<table class="tbl">
<thead><tr><th>What you notice</th><th>Mass lager</th><th>Craft beer</th></tr></thead>
<tbody>
<tr><td>Aroma</td><td>Faint, mostly grain</td><td>Deliberate, often the point</td></tr>
<tr><td>Bitterness</td><td>Low and quick</td><td>Ranges from none to bracing</td></tr>
<tr><td>Body</td><td>Light, thin by design</td><td>Thin to full, chosen per style</td></tr>
<tr><td>Serving temperature</td><td>Very cold, near freezing</td><td>Cool, so flavour survives</td></tr>
<tr><td>Freshness</td><td>Months on shelf</td><td>Often best within weeks</td></tr>
</tbody></table>
<p>That last row explains a lot of bad first experiences. A hoppy beer that has
sat warm for three months has lost the aroma it was built around. It is not that
you dislike the style. You met it late.</p>"""),
        ("How the beer is actually made", """
<p>The process is the same in a two hundred litre pilot kit and a two hundred
hectolitre plant. Only the scale changes.</p>
<p><strong>Milling.</strong> The malt is cracked open, not ground to flour. You
want the starch accessible and the husk intact, because the husk acts as a filter
bed later.</p>
<p><strong>Mashing.</strong> Crushed malt is mixed with hot water and held, often
somewhere in the mid sixties Celsius, while enzymes convert starch into
fermentable sugar. Hold it cooler and you get a drier, more alcoholic beer. Hold
it warmer and you get more body and a sweeter finish. This single decision is one
of the most powerful levers a brewer has.</p>
<p><strong>Lautering.</strong> The sweet liquid, now called wort, is separated
from the spent grain.</p>
<p><strong>Boiling.</strong> The wort boils for around an hour. Hops added early
give bitterness because the heat converts their acids. Hops added late or after
the boil give aroma, because those oils are volatile and would otherwise
evaporate.</p>
<p><strong>Fermentation.</strong> The wort is cooled, yeast is added, and over
days or weeks the sugar becomes alcohol. Temperature control here decides whether
you get clean beer or a fruit bomb.</p>
<p><strong>Conditioning and packaging.</strong> The beer matures, clears, and is
carbonated before it goes into keg, can or bottle.</p>"""),
        ("What to drink first", """
<p>If you are starting out, do not begin with the most extreme thing on the
menu. A heavily bitter double IPA is a poor introduction in the same way that a
peated cask strength whisky is.</p>
<p>Start with a wheat beer or a pale ale. Both are approachable, both have enough
character that you can actually taste what the brewer intended, and neither will
strip your palate. From there, move towards whatever you found interesting, more
aroma, more bitterness, more roast.</p>
<p>Order a tasting flight where you can. Four small pours teach you more in one
sitting than four separate pints across four weeks, because comparison is what
builds a palate.</p>"""),
    ],
    faqs=[
        ("Is craft beer stronger than normal beer?",
         "Not necessarily. Plenty of craft beers sit between 4 and 5 per cent, which "
         "is lower than many Indian strong lagers. Strength is a choice per style, "
         "not a property of craft brewing."),
        ("Why does craft beer cost more?",
         "More malt and hops per litre, smaller batches, imported ingredients in most "
         "of India, and far shorter shelf life. The excise structure in several states "
         "also taxes on strength or on volume in ways that penalise small producers."),
        ("Is craft beer healthier?",
         "It is unfiltered more often, so it may retain more yeast derived B vitamins, "
         "but the difference is not meaningful. It is still alcohol, and often at a "
         "higher strength. Drink it for the flavour, not for your health."),
    ],
    cta=dict(title="Taste the difference properly",
             body="Our two hour guided tasting takes you through a structured flight, "
                  "so you learn what you are actually drinking.",
             href=ENROL, label="Book a tasting"),
    related=["beer-styles-guide", "how-to-taste-beer", "craft-beer-in-india"],
)

BEER_STYLES = dict(
    slug="beer-styles-guide",
    cat="Styles",
    h1="Beer styles, explained without the jargon",
    title="Beer Styles Explained | Craft Beer School",
    desc="Ales, lagers, IPAs, stouts, wheat beers and sours explained simply, "
         "with what to expect in the glass and which to try first.",
    teaser="Ale or lager is only the first fork in the road. Here is the map "
           "of everything after it.",
    standfirst="Style names sound like a members only vocabulary. They are really "
               "just shorthand for a set of decisions a brewer made, and once you can "
               "read them you can order confidently anywhere.",
    read="9 min", updated="2026-09-03", updated_label="September 2026",
    sections=[
        ("The one distinction that matters first", """
<p>Almost every beer is either an ale or a lager, and the difference is the
yeast.</p>
<p>Ale yeast works warm, often between 18 and 22 degrees Celsius, and works fast.
While it does, it produces esters, compounds that read as fruit. That is why ales
often carry banana, pear or citrus notes that nobody added.</p>
<p>Lager yeast works cold, often between 8 and 12 degrees, and slowly. Cold and
slow suppresses those fruity compounds, which leaves a cleaner beer where the
malt and hops have nowhere to hide. A lager is harder to brew well for exactly
that reason. There is no fruitiness to cover a mistake.</p>
<p>Everything below is a variation on one of those two.</p>"""),
        ("Lagers", """
<p><strong>Pilsner.</strong> Pale, crisp, genuinely bitter. A well made pilsner
is one of the hardest beers to hide behind and a good test of a brewery.</p>
<p><strong>Helles.</strong> Softer and maltier than a pilsner, less bitter, built
for drinking rather than analysing.</p>
<p><strong>Dunkel and Bock.</strong> Darker lagers, bread crust and light caramel
rather than roast. Bock is the stronger of the two.</p>
<p>Lagers suit the Indian climate well. They are refreshing, they are familiar
enough that a table will share one, and they reward a brewery with good
temperature control.</p>"""),
        ("Pale ales and IPAs", """
<p><strong>Pale ale.</strong> Balanced, hop forward but not aggressive. The
sensible default on most taplists.</p>
<p><strong>India Pale Ale.</strong> More hops, more bitterness, more aroma. The
modern American version leans tropical and citrus. The English version is
earthier and more restrained.</p>
<p><strong>Hazy or New England IPA.</strong> Deliberately cloudy, low perceived
bitterness, heavy fruit aroma, soft mouthfeel. It is the most popular craft style
in India right now and also the most perishable. Drink it fresh or do not
bother.</p>
<p>The historical story that IPA was invented strong and hoppy to survive the
voyage to India is mostly a tidy myth. Beer of many strengths made the journey
fine. The style did become associated with the export trade, but the neat
origin story is later marketing.</p>"""),
        ("Wheat beers", """
<p><strong>Hefeweizen.</strong> German, unfiltered, brewed with a large
proportion of wheat. The yeast throws banana and clove. Nothing is added, that is
purely fermentation character.</p>
<p><strong>Witbier.</strong> Belgian, usually spiced with coriander and orange
peel, lighter and tarter than a hefeweizen.</p>
<p>Wheat beers convert Indian drinkers more reliably than anything else on a
taplist. They are refreshing in heat, they are low in bitterness, and the aroma
is immediately obvious even to someone tasting attentively for the first
time.</p>"""),
        ("Stouts and porters", """
<p>Dark beers are dark because some of the malt was roasted, in the same way
coffee beans are. That roast brings chocolate, coffee and sometimes a dry, ashy
bitterness quite separate from hop bitterness.</p>
<p><strong>Porter.</strong> Chocolate and light roast, medium body.</p>
<p><strong>Dry stout.</strong> Sharper roast, dry finish, often served on nitrogen
for that thick creamy head.</p>
<p><strong>Imperial stout.</strong> Much stronger, thick, often aged. A sipping
beer.</p>
<p>Colour tells you very little about strength. A dry stout is frequently weaker
than a pale IPA sitting next to it.</p>"""),
        ("Sours and Belgian styles", """
<p><strong>Belgian ales.</strong> Driven by expressive yeast, giving pepper,
clove and stone fruit. Often deceptively strong, because the alcohol is well
hidden.</p>
<p><strong>Kettle sour, gose, Berliner weisse.</strong> Deliberately acidic,
soured with lactic bacteria before or during fermentation. Refreshing rather than
challenging once you expect the tartness.</p>
<p><strong>Barrel aged and wild.</strong> Long maturation, mixed cultures,
complex and expensive. A specialist corner of the market.</p>"""),
        ("Reading a style spec", """
<p>Taplists usually print three numbers. They are worth understanding.</p>
<p><strong>ABV</strong> is alcohol by volume, straightforwardly how strong the
beer is.</p>
<p><strong>IBU</strong> estimates bitterness. It is useful but not absolute,
because perceived bitterness depends on how sweet the beer is underneath. A
sweet beer at 60 IBU can taste gentler than a dry beer at 35.</p>
<p><strong>SRM or EBC</strong> describes colour, from pale straw to opaque black.
It says nothing about flavour intensity or strength.</p>
<p>Treat all three as a rough map rather than a promise. The only reliable test
is the glass in front of you.</p>"""),
    ],
    faqs=[
        ("What is the difference between ale and lager?",
         "The yeast and the temperature. Ale yeast ferments warm and fast and produces "
         "fruity compounds. Lager yeast ferments cold and slow, giving a cleaner beer "
         "with less fruit character."),
        ("What does IBU actually mean?",
         "International Bitterness Units, an estimate of bitter compounds from hops. It "
         "is a guide, not a guarantee, because malt sweetness masks bitterness. Always "
         "read IBU alongside the strength and the style."),
        ("Which style should a beginner order?",
         "A wheat beer or a pale ale. Both are aromatic enough to be interesting and "
         "gentle enough not to overwhelm a palate that is still calibrating."),
        ("Are dark beers stronger than pale beers?",
         "No. Colour comes from roasted malt and is independent of alcohol. Plenty of "
         "dry stouts are weaker than the pale IPA beside them."),
    ],
    cta=dict(title="Learn the styles properly",
             body="Style Specialization covers origins, technique and how to brew "
                  "award standard versions across eight weeks.",
             href=COURSES, label="See the course"),
    related=["what-is-craft-beer", "how-to-taste-beer", "brewing-for-india"],
)

HOW_TO_TASTE = dict(
    slug="how-to-taste-beer",
    cat="Tasting",
    h1="How to taste beer like a professional",
    title="How to Taste Craft Beer Like a Pro | Craft Beer School",
    desc="A repeatable framework for tasting beer: appearance, aroma, flavour, "
         "mouthfeel and finish, plus how to train your palate faster.",
    teaser="Drinking is not tasting. A method turns a vague impression into "
           "something you can name and repeat.",
    standfirst="Professional tasters are not born with better tongues. They have a "
               "system, they use it every time, and they have practised naming what "
               "they find. All three are learnable.",
    read="8 min", updated="2026-09-03", updated_label="September 2026",
    sections=[
        ("Set the conditions before you taste", """
<p>Most tasting mistakes happen before the beer reaches your mouth.</p>
<p><strong>Temperature.</strong> Ice cold suppresses aroma and mutes flavour. If
you want to assess a beer, let it come up to roughly 8 to 12 degrees Celsius.
Lagers at the lower end, stronger dark beers at the higher end. In an Indian
taproom this often means simply waiting five minutes.</p>
<p><strong>Glass.</strong> Use something that narrows towards the top, so aroma
collects. A wine glass beats a straight pint glass for assessment. The glass must
be free of detergent residue, which kills head retention instantly.</p>
<p><strong>Your own state.</strong> No coffee, mint or strong food immediately
before. Taste early in a session rather than late.</p>"""),
        ("Appearance", """
<p>Hold the glass against something neutral and white.</p>
<p>Note the colour honestly, straw, gold, amber, ruby, brown, black. Note whether
it is clear or hazy, and whether that haze looks deliberate, as in a New England
IPA, or like a fault.</p>
<p>Then watch the head. Good head retention suggests healthy proteins and clean
glassware. A head that collapses in seconds can indicate a problem, often fat,
detergent residue, or a beer that has been mishandled.</p>"""),
        ("Aroma", """
<p>This is where most of what you call taste actually happens.</p>
<p>Swirl gently and take short sharp sniffs rather than one long inhale. Your
nose fatigues fast, so sniff, pause, sniff again.</p>
<p>Work through categories deliberately rather than hunting for a single word.
Is there malt character, bread, biscuit, caramel, chocolate, roast? Is there hop
character, citrus, pine, tropical fruit, grass, herbs? Is there yeast character,
banana, clove, pepper, stone fruit? Is there anything that does not belong,
butter, cooked sweetcorn, wet cardboard, solvent?</p>
<p>Name what you find out loud or write it down. Naming is what fixes a smell in
memory, and it is the single fastest way to improve.</p>"""),
        ("Flavour, mouthfeel and finish", """
<p>Take a decent mouthful, not a sip, and let it cover your whole tongue.</p>
<p><strong>Flavour</strong> should largely confirm the aroma, with sweetness and
bitterness added. Notice the order in which things arrive. Many beers lead malty
and finish bitter.</p>
<p><strong>Mouthfeel</strong> is texture, not taste. Is it thin and watery, or
full and coating? Is the carbonation soft and fine, or sharp and prickly? Is
there any astringency, that drying, tea like grip at the sides of the tongue,
which usually signals a process problem.</p>
<p><strong>Finish</strong> is what remains after swallowing, and for how long. A
crisp lager should finish clean and short. An imperial stout should linger.
Whether the finish suits the style matters more than whether it is long.</p>"""),
        ("Judge it against the style, not your preference", """
<p>The discipline that separates a taster from a drinker is this: assess whether
the beer does what it set out to do.</p>
<p>You may dislike smoked beer. That is irrelevant when judging a smoked beer.
The question is whether the smoke is clean, whether it is balanced, whether the
beer is free of faults, and whether it matches its declared style.</p>
<p>Formal scoring systems split marks across aroma, appearance, flavour,
mouthfeel and overall impression, weighting aroma and flavour most heavily.
Even scoring informally in those five buckets will sharpen your thinking, because
it forces you to separate a beer being unpleasant from a beer being wrong.</p>"""),
        ("Train faster with deliberate practice", """
<p>Three habits move people quickest.</p>
<p><strong>Taste side by side.</strong> Two beers of the same style next to each
other teach more than ten tasted alone across a month. Difference is easier to
perceive than absolutes.</p>
<p><strong>Taste faults deliberately.</strong> Once you have knowingly tasted
diacetyl or acetaldehyde in a spiked sample, you will recognise it forever. Until
then you will keep sensing that something is off without being able to say what.
This is the single highest return exercise in sensory training.</p>
<p><strong>Keep notes.</strong> Same format every time. Your notes from six
months ago are the clearest evidence of whether you are improving.</p>"""),
    ],
    faqs=[
        ("What temperature should beer be tasted at?",
         "Around 8 to 12 degrees Celsius. Colder suppresses aroma and hides both the "
         "good and the faulty. Lighter lagers sit at the cooler end, strong dark beers "
         "at the warmer end."),
        ("Does the glass really matter?",
         "Yes, more than most people expect. A glass that narrows at the top concentrates "
         "aroma, and aroma carries most of flavour. Detergent residue destroys head "
         "retention, so rinse well."),
        ("How long does it take to build a decent palate?",
         "Structured tasting a few times a week produces a noticeable difference within "
         "two or three months. Tasting faults deliberately accelerates it more than any "
         "other single exercise."),
    ],
    cta=dict(title="Train your palate with a sensory panel",
             body="Sensory Evaluation teaches flavour chemistry, off flavour "
                  "identification and real scoring methods in two weeks.",
             href=COURSES, label="See the course"),
    related=["beer-off-flavours", "beer-styles-guide", "what-is-craft-beer"],
)

OFF_FLAVOURS = dict(
    slug="beer-off-flavours",
    cat="Quality",
    h1="Beer off flavours, and what causes them",
    title="Beer Off-Flavours: Causes and Fixes | Craft Beer School",
    desc="The common beer faults, what each one tastes like, the process failure "
         "behind it and how brewers prevent it. A practical quality guide.",
    teaser="Butterscotch, cooked sweetcorn, wet cardboard. Each one is a message "
           "about something that went wrong upstream.",
    standfirst="An off flavour is not bad luck. It is a process telling you where it "
               "broke. Learn to read them and you can fix the cause rather than "
               "guessing at the symptom.",
    read="10 min", updated="2026-09-03", updated_label="September 2026",
    sections=[
        ("Why this is the most valuable skill in a brewery", """
<p>Recipe design gets the attention. Quality control keeps the business alive.</p>
<p>A brewery that cannot reliably detect its own faults will ship inconsistent
beer, and inconsistency loses customers faster than a beer being merely
uninteresting. The brewers who become indispensable are the ones who can taste a
tank, name the problem and point at the step that caused it.</p>
<p>Almost every fault below is preventable with process control rather than
better ingredients.</p>"""),
        ("Diacetyl: butter, butterscotch, slick", """
<p><strong>What you notice.</strong> Butter or butterscotch on the nose, and a
slick, almost oily film across the tongue. At low levels it reads as a rounded
sweetness rather than anything obviously wrong.</p>
<p><strong>Where it comes from.</strong> Yeast produces a precursor during
fermentation and then normally reabsorbs and reduces it. Diacetyl in finished
beer usually means the yeast was not given the chance to finish that job, because
fermentation was cooled too early, the yeast was unhealthy, or the beer was pulled
off the yeast too soon. It can also come from a bacterial infection, which is the
worse diagnosis.</p>
<p><strong>The fix.</strong> A diacetyl rest, holding the beer a few degrees
warmer near the end of fermentation, lets the yeast clean up. Do not crash cool
until the beer tests clean. If it recurs across batches with good practice,
investigate infection.</p>
<p>A small amount is acceptable, even traditional, in some English ales and
Czech lagers. In a crisp modern lager it is a fault.</p>"""),
        ("DMS: cooked sweetcorn, cabbage", """
<p><strong>What you notice.</strong> Cooked or tinned sweetcorn, sometimes
cabbage or tomato.</p>
<p><strong>Where it comes from.</strong> A malt derived precursor converts to
dimethyl sulphide with heat, and DMS is volatile, so a vigorous open boil drives
it off. It survives when the boil is too gentle, too short, or lidded, and it
re-forms if hot wort sits around slowly cooling after the boil.</p>
<p><strong>The fix.</strong> A strong rolling boil with the lid off, and rapid
cooling afterwards. The gap between the end of the boil and pitching temperature
is where a lot of DMS is created. Pale lagers show it most, because there is
nothing to hide behind.</p>"""),
        ("Acetaldehyde: green apple, emulsion paint", """
<p><strong>What you notice.</strong> Fresh green apple, sometimes a solvent edge
like emulsion paint.</p>
<p><strong>Where it comes from.</strong> It is an intermediate on the way to
ethanol. Its presence generally means the beer is simply not finished, or the
yeast was stressed and gave up early.</p>
<p><strong>The fix.</strong> Patience, adequate yeast pitching rates, proper
aeration of the wort before pitching, and stable fermentation temperature. Most
acetaldehyde complaints are really a packaging schedule that ran ahead of the
biology.</p>"""),
        ("Oxidation: wet cardboard, sherry, stale", """
<p><strong>What you notice.</strong> Wet cardboard or paper in pale beers, a
sherry or dried fruit note in stronger dark ones, and a general flattening of hop
aroma.</p>
<p><strong>Where it comes from.</strong> Oxygen picked up after fermentation, at
transfer, filtration or packaging. Warm storage accelerates it dramatically.</p>
<p><strong>The fix.</strong> This one cannot be corrected once it has happened, so
it must be prevented. Purge tanks, kegs and cans, minimise splashing on transfer,
fill without foaming, and control the cold chain from brewery to glass. In Indian
conditions the cold chain is usually the weakest link, and a hoppy beer that sat
warm in transit will arrive stale no matter how well it was brewed.</p>"""),
        ("Phenolic, lightstruck and astringent", """
<p><strong>Phenolic.</strong> Clove, smoke, plastic or medicinal notes. Clove is
correct and desirable in a hefeweizen, where it comes from the yeast strain.
Plastic or medicinal character elsewhere usually points at chlorine in the brewing
water reacting with phenols, or at wild yeast. Filter or treat your water and the
problem generally disappears.</p>
<p><strong>Lightstruck.</strong> A distinct skunky aroma, caused by light striking
hop compounds. It develops in minutes in clear or green glass. Cans and brown
bottles prevent it entirely, which is why so many careful brewers have moved to
cans.</p>
<p><strong>Astringency.</strong> A drying, puckering grip rather than a flavour.
Caused by over milling the grain, sparging too hot or for too long, or pushing
the mash pH too high, all of which extract tannin from the husk. Watch your
sparge temperature and stop collecting wort earlier than you think.</p>"""),
        ("Building a sensory programme that actually works", """
<p>You do not need a laboratory. You need consistency.</p>
<p>Taste every batch at the same points in the process, with the same small panel
of people, using the same vocabulary. Train that panel on spiked samples so
everyone means the same thing by the same word. Record results, because the value
appears in the trend rather than in any single tasting.</p>
<p>Then close the loop. A panel that identifies diacetyl but never changes the
fermentation schedule is an expensive ritual. The point of tasting is to change
what you do next.</p>"""),
    ],
    faqs=[
        ("Is diacetyl always a fault?",
         "No. A low level is traditional in some English ales and Czech lagers. In a "
         "clean modern lager or a hop forward beer it is a defect and usually indicates "
         "fermentation was cut short."),
        ("Why does my beer taste like wet cardboard?",
         "Oxidation. Oxygen was picked up after fermentation, most often at transfer or "
         "packaging, and warm storage sped it up. It cannot be reversed, so the answer "
         "is prevention and a tighter cold chain."),
        ("Can off flavours be fixed after packaging?",
         "Almost never. Diacetyl and acetaldehyde can sometimes be reduced before "
         "packaging if the yeast is still present and active. Oxidation, lightstruck "
         "character and infection cannot be undone."),
        ("What causes the skunky smell in some imported beers?",
         "Light. Hop compounds react within minutes of exposure through clear or green "
         "glass. Brown glass helps and cans prevent it completely."),
    ],
    cta=dict(title="Learn to find faults before your customers do",
             body="Sensory Evaluation trains you on real off flavour standards, "
                  "scoring systems and how to run a panel.",
             href=COURSES, label="See the course"),
    related=["how-to-taste-beer", "brewing-for-india", "become-a-brewer-india"],
)

ARTICLES_A = [WHAT_IS_CRAFT_BEER, BEER_STYLES, HOW_TO_TASTE, OFF_FLAVOURS]
