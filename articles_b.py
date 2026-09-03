# -*- coding: utf-8 -*-
"""Article records, part two: the India and commercial intent cluster.

These target the queries that bring people who are ready to act, someone
planning a brewery or changing career. All prose is original; see articles_a.py
for the sourcing note.
"""

ENROL = "contact.html#enroll"
COURSES = "courses.html"

CRAFT_BEER_INDIA = dict(
    slug="craft-beer-in-india",
    cat="India",
    h1="How craft beer actually grew in India",
    title="The Rise of Craft Beer in India | Craft Beer School",
    desc="How India went from two national lagers to hundreds of microbreweries, "
         "why it happened city by city, and what the market looks like now.",
    teaser="A licence change in one state started it. Everything after that was "
           "taprooms, heat and a generation that wanted choice.",
    standfirst="India's craft scene did not grow evenly, because beer is a state "
               "subject. It grew wherever the rules allowed a brewery to sell its own "
               "beer on its own premises, and stalled everywhere they did not.",
    read="8 min", updated="2026-09-03", updated_label="September 2026",
    sections=[
        ("The rule that started it", """
<p>For most of modern Indian history, beer meant a handful of national lagers,
usually strong, usually served very cold, usually indistinguishable.</p>
<p>What changed was regulatory rather than cultural. When states began permitting
microbreweries to brew and sell on their own premises, the economics suddenly
worked. A brewpub could skip the distributor, skip the retail margin, and sell
fresh beer directly at a price that covered small batch production.</p>
<p>That is why the story starts in a few specific cities rather than nationally.
Beer is regulated at state level in India, so the scene grew at the pace each
state government allowed. Understanding this one fact explains almost every
oddity in the Indian market.</p>"""),
        ("Why the taproom model won", """
<p>In most mature beer markets, a small brewery packages its beer and sells it
through shops and bars. In India that route is hard. Distribution is tightly
controlled, retail shelf space is contested, and excise rules vary by state in
ways that make national distribution expensive.</p>
<p>The brewpub sidesteps all of it. You brew where you sell. The beer travels
metres instead of hundreds of kilometres, which solves the freshness problem that
kills hoppy styles. You capture the full margin. You control serving temperature
and glassware, so the customer meets the beer at its best.</p>
<p>The trade off is that you are running a restaurant as well as a brewery. Many
Indian brewpubs make more money from food than from beer, and the ones that
struggle usually underestimated how much of the business is hospitality.</p>"""),
        ("What Indian drinkers actually order", """
<p>The taplist that works here is not the taplist that works in Europe or the
United States.</p>
<p>Wheat beers convert first time drinkers more reliably than anything else. They
are refreshing in heat, low in bitterness, and immediately aromatic. Most
successful Indian brewpubs have one on permanently.</p>
<p>Lagers and pilsners are the volume drivers once a venue matures, because they
are what a table can agree on. They are also unforgiving to brew, which quietly
separates good breweries from average ones.</p>
<p>Hoppy styles have grown fast, particularly hazy IPAs, but they carry a
freshness cost that many venues have not solved.</p>
<p>Stouts and sours sell in smaller volumes but do disproportionate work for
reputation, because they signal that a brewery has range.</p>"""),
        ("The constraints nobody warns you about", """
<p><strong>Heat.</strong> Ambient temperatures make glycol and cooling capacity a
first order design decision rather than an afterthought. Fermentation control is
where Indian breweries most often fail.</p>
<p><strong>Ingredients.</strong> Most specialty malt and almost all aroma hops are
imported, priced in foreign currency and subject to shipping delays. That affects
both cost and recipe consistency, and it rewards brewers who can reformulate
around what is actually available.</p>
<p><strong>Water.</strong> Source water varies enormously across the country and
often needs treatment before it is suitable. Chlorine in municipal supply is a
common and entirely avoidable cause of medicinal off flavours.</p>
<p><strong>Excise.</strong> Duty structures, licence fees and permitted formats
differ by state and change with little notice. A business model that works in one
city may be illegal or uneconomic three hundred kilometres away.</p>"""),
        ("Where the market is heading", """
<p>Three shifts look durable.</p>
<p>Packaging is growing. As more states permit small breweries to can and
distribute, the ceiling on any single brewery lifts beyond the seats in its own
room. Cans, not bottles, because they protect against light entirely.</p>
<p>Quality is becoming the differentiator. When a city has five brewpubs, novelty
sells. When it has fifty, consistency sells. The breweries investing in sensory
panels and process control are the ones separating from the pack.</p>
<p>Trained staff are scarce. Demand for brewers, quality technicians and people
who can genuinely run a cellar has outstripped supply, which is precisely why
formal beer education has become worth paying for in India rather than something
you had to travel abroad to get.</p>"""),
    ],
    faqs=[
        ("Why is craft beer expensive in India?",
         "Imported malt and hops, small batch production, high and variable state excise "
         "duty, and the cost of cooling in a hot climate. Licence fees and compliance "
         "also fall on a much smaller volume than a national brewery enjoys."),
        ("Why are microbreweries concentrated in a few cities?",
         "Because alcohol is regulated by state, not nationally. The scene grew wherever "
         "state rules first permitted breweries to sell their own beer on their premises, "
         "and it remains uneven for the same reason."),
        ("Is Indian craft beer any good?",
         "The best of it competes internationally. The variance is wider than in mature "
         "markets, mostly because of fermentation control and cold chain rather than "
         "recipe design."),
    ],
    cta=dict(title="Understand the market before you invest in it",
             body="Brewery Business Management covers planning, licensing, finance "
                  "and distribution for the Indian market.",
             href=COURSES, label="See the course"),
    related=["start-a-microbrewery-india", "brewing-for-india", "become-a-brewer-india"],
)

START_MICROBREWERY = dict(
    slug="start-a-microbrewery-india",
    cat="Business",
    h1="How to start a microbrewery in India",
    title="How to Start a Microbrewery in India | Craft Beer School",
    desc="Licences, capital, equipment, running costs and realistic timelines for "
         "opening a microbrewery or brewpub in India, without the sales pitch.",
    teaser="The brewhouse is the easy part. Licensing, cooling and working capital "
           "are what decide whether you open.",
    standfirst="Most people planning a brewery budget carefully for equipment and "
               "barely at all for the eighteen months of licensing, fit out and working "
               "capital that surround it. That imbalance is why projects stall.",
    read="12 min", updated="2026-09-03", updated_label="September 2026",
    sections=[
        ("Decide which business you are actually starting", """
<p>Three models exist in India, and they are genuinely different businesses.</p>
<p><strong>The brewpub.</strong> You brew and sell on your own premises. Highest
margin per litre, direct customer relationship, complete control of freshness.
You are also running a full hospitality operation, with kitchen, service and
rent in a high footfall location.</p>
<p><strong>The packaging microbrewery.</strong> You brew and distribute into
retail and other venues. Larger addressable market, far harder route to market,
and you inherit the state distribution and excise system in full.</p>
<p><strong>Contract or gypsy brewing.</strong> You develop recipes and brand and
pay someone else's plant to produce them. Dramatically lower capital, much faster
to market, thinner margins and no control of the asset. As a way to test a brand
before committing capital, it is badly underrated.</p>
<p>Choose deliberately. Equipment specified for one model is often wrong for
another.</p>"""),
        ("Licensing, the part that sets your timeline", """
<p>Alcohol is a state subject, so there is no single national process. What
follows is the shape of it rather than any particular state's checklist, and you
must verify current requirements with your own state excise department and a
local consultant.</p>
<p>Expect to deal with several of the following: a state excise licence for
manufacture, a separate licence to serve or to sell, local municipal trade
licence and building approvals, fire safety clearance, pollution control board
consent to establish and later consent to operate, food safety registration, and
often a specific approval covering the brewery equipment and its location within
the premises.</p>
<p>Three practical warnings. Approvals are frequently sequential rather than
parallel, so one delay pushes everything. Several licences are annual and must be
renewed, which is a recurring cost, not a one off. And premises usually must be
secured before some applications can proceed, meaning you pay rent through the
approval period while earning nothing.</p>
<p>Budget twelve to eighteen months from decision to first pour, and treat
anything faster as a pleasant surprise.</p>"""),
        ("What the capital actually goes on", """
<p>Founders consistently overweight the brewhouse. A realistic split of project
cost looks closer to this.</p>
<table class="tbl">
<thead><tr><th>Item</th><th>Share of project cost</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>Brewhouse and cellar vessels</td><td>25 to 35 per cent</td><td>The bit everyone budgets for</td></tr>
<tr><td>Glycol, chilling and utilities</td><td>10 to 15 per cent</td><td>Routinely underestimated in India</td></tr>
<tr><td>Interiors, kitchen and fit out</td><td>25 to 35 per cent</td><td>For a brewpub this can exceed the brewery</td></tr>
<tr><td>Licences, deposits, professional fees</td><td>5 to 10 per cent</td><td>Recurring, not one off</td></tr>
<tr><td>Working capital</td><td>15 to 20 per cent</td><td>Wages, ingredients and rent before revenue</td></tr>
</tbody></table>
<p>The single most common failure is running out of working capital during the
licensing period. Model at least six months of full operating cost with zero
revenue and treat that as non negotiable.</p>"""),
        ("Specifying the brewhouse", """
<p>Size the plant to the room, not to the ambition.</p>
<p>Start from realistic weekly sales in litres, then work backwards to batch size
and the number of fermenters. Most first time operators buy too few fermenters
and too small a chiller, then discover that fermentation and conditioning, not
brewing, are the bottleneck. You can brew a batch in a day. It may occupy a tank
for two to four weeks.</p>
<p>A workable rule is to plan for at least three to four fermentation vessels per
brewhouse, more if you intend to make lagers, which tie up tanks far longer than
ales.</p>
<p>Oversize the glycol system. In Indian ambient conditions this is the component
most often specified for a European climate and found wanting in May.</p>
<p>Insist on proper sampling valves, accessible cleaning points and accurate
temperature probes on every vessel. Cheap fittings are how quality problems
become permanent.</p>"""),
        ("Running costs and the honest economics", """
<p>Once open, the recurring costs that matter are ingredients, energy, labour,
excise and rent.</p>
<p>Ingredients are usually a smaller share of revenue than founders expect,
because the margin on beer sold on your own premises is high. Energy is larger
than expected, because cooling runs continuously. Excise varies enormously and can
be assessed on volume produced rather than sold, which punishes wastage.</p>
<p>Yield is where quiet money is lost. Beer left behind in tanks, dumped batches,
foamy dispense and over pouring all reduce sellable litres from wort you have
already paid duty and energy on. Measuring loss at each transfer and dispense point
is unglamorous and one of the highest return things a small brewery can do.</p>"""),
        ("A realistic timeline", """
<p><strong>Months 1 to 3.</strong> Model the business, choose the format, scout
premises, take advice on your state's specific excise position.</p>
<p><strong>Months 3 to 6.</strong> Secure premises, begin licence applications,
finalise equipment specification and place orders. Long lead items should be
ordered before fit out begins.</p>
<p><strong>Months 6 to 12.</strong> Fit out, installation, utilities, inspections.
Recruit and train your brewer now rather than later, because they should be
present during commissioning.</p>
<p><strong>Months 12 to 15.</strong> Commissioning, trial brews, staff training,
sensory baseline, soft launch. Your first three or four batches are for learning
the plant, not for reputation.</p>
<p><strong>Month 15 onward.</strong> Open, then spend a year tightening
consistency.</p>"""),
        ("The mistakes that recur", """
<p>Opening with too many beers. Four consistent taps beat ten inconsistent ones,
and every extra line ties up a tank.</p>
<p>Hiring a brewer late. They should influence equipment choice, not inherit it.</p>
<p>Ignoring water. Test and treat source water before you commission, not after
you have brewed three medicinal batches.</p>
<p>No sensory programme. Without one you will not know a batch has drifted until
customers stop returning.</p>
<p>Treating the kitchen as secondary. In most Indian brewpubs food carries the
revenue while beer carries the reputation. Underinvesting in either sinks the
venue.</p>"""),
    ],
    faqs=[
        ("How much does it cost to start a microbrewery in India?",
         "It varies widely by state, city, format and scale, so any single figure would "
         "mislead. Plan the split instead: brewhouse a quarter to a third, fit out a "
         "similar share, plus cooling, licences and at least six months of working "
         "capital. Get quotes for your own state and premises."),
        ("How long does licensing take?",
         "Commonly twelve to eighteen months from decision to first pour, because "
         "approvals are often sequential and premises must usually be secured first. "
         "Requirements differ by state and change, so verify locally."),
        ("Can I start without buying a brewery?",
         "Yes. Contract brewing lets you develop recipes and a brand on someone else's "
         "plant with far lower capital. It is a sensible way to test demand before "
         "committing to equipment."),
        ("Do I need to be a brewer to own a brewery?",
         "No, but somebody in the room must be. Owners who cannot assess their own beer "
         "are dependent on whoever they hire, and that is an expensive position when "
         "quality slips."),
    ],
    cta=dict(title="Plan it properly before you sign a lease",
             body="Brewery Business Management covers planning and finance, licensing "
                  "and regulations, branding and distribution across three weeks.",
             href=COURSES, label="See the course"),
    related=["become-a-brewer-india", "craft-beer-in-india", "brewing-for-india"],
)

BECOME_A_BREWER = dict(
    slug="become-a-brewer-india",
    cat="Careers",
    h1="How to become a brewer in India",
    title="How to Become a Brewer in India | Craft Beer School",
    desc="What brewers actually do, the routes into the job in India, which "
         "qualifications carry weight, and how to get hired without experience.",
    teaser="It is a production job with a science base and an early alarm. Here is "
           "the honest route in.",
    standfirst="Brewing looks like a creative job from the outside and is a process "
               "control job from the inside. The people who last are the ones who "
               "enjoyed the second description too.",
    read="9 min", updated="2026-09-03", updated_label="September 2026",
    sections=[
        ("What the job actually involves", """
<p>A working brewer spends far more time cleaning, measuring and recording than
designing recipes. On a normal day that means milling and mashing, monitoring
fermentation, taking gravity and pH readings, transferring beer, and cleaning
vessels and lines thoroughly enough that nothing contaminates the next batch.</p>
<p>It is physical. You will lift sacks, climb tanks, stand for long shifts and
start early. It is also unforgiving of carelessness, because a single missed
cleaning step can cost a tank of beer worth more than a month of your salary.</p>
<p>Recipe creation is real, but it is perhaps five per cent of the role and
usually earned rather than given. If that trade sounds fine to you, the career
suits you. If it does not, better to know now.</p>"""),
        ("The routes in", """
<p><strong>Start on the floor.</strong> Many Indian brewers began as cellar hands
or assistants and learned on the job. It is the most common route and the least
glamorous. You will clean for months before you touch a recipe.</p>
<p><strong>Come from food science or biotechnology.</strong> A relevant degree
gives you the microbiology and chemistry foundation quickly, and breweries value
it, but you will still learn the practical craft on site.</p>
<p><strong>Come from homebrewing.</strong> Homebrewing proves genuine interest and
teaches the process end to end. It does not teach scale, cleaning regimes or
consistency, so present it as evidence of commitment rather than as
experience.</p>
<p><strong>Formal training.</strong> Structured courses compress the theory that
would otherwise take years to absorb piecemeal, and matter most for people
switching careers who need credibility fast.</p>"""),
        ("Which qualifications carry weight", """
<p>Employers in India generally read credentials in three tiers.</p>
<p><strong>Brewing technical qualifications</strong> carry the most weight for
production roles, because they signal you understand process, microbiology and
quality rather than just enthusiasm.</p>
<p><strong>Beer knowledge and sensory certifications</strong> are strongest for
roles that face customers or manage quality perception, such as taproom
management, sales, training and brand work.</p>
<p><strong>Drinks industry qualifications more broadly</strong> help in
hospitality and beverage management, where beer sits alongside wine and
spirits.</p>
<p>No certificate substitutes for having actually run a fermentation. Combine
training with hands on time, ideally in the same period, so each reinforces the
other.</p>"""),
        ("Build evidence, not just interest", """
<p>Hiring managers are trying to answer one question: will this person cost me a
batch?</p>
<p>Reduce that risk visibly.</p>
<p>Keep a brew log. Every batch, with recipe, timings, temperatures, gravities and
what you would change. A disciplined log is more persuasive than any certificate,
because it demonstrates the exact habit the job requires.</p>
<p>Learn to taste and prove it. Being able to identify common off flavours
reliably is a genuine, testable skill and immediately useful to any brewery.</p>
<p>Get on a real plant. A few days shadowing a working brewery teaches things
homebrewing cannot, mainly around cleaning, scale and how much of the job is
logistics.</p>
<p>Learn basic data handling. Breweries collect far more numbers than they use.
A brewer who can turn fermentation logs into a trend that prevents a problem is
unusually valuable, and increasingly so.</p>"""),
        ("Pay, progression and where the jobs are", """
<p>Entry level brewing pay in India is modest and reflects that you are being
trained. It rises meaningfully with responsibility, particularly once you are
accountable for quality across multiple tanks or for a site.</p>
<p>A typical progression runs from assistant or cellar hand, to brewer, to head
brewer, and from there either to brewmaster across multiple sites, into quality
management, or into consulting and plant commissioning. Some move sideways into
technical sales, training or brand roles, where brewing knowledge is rarer and
often better paid.</p>
<p>Openings cluster where breweries cluster, which in India means a handful of
cities. Be realistic about relocating, at least at the start.</p>"""),
        ("Getting the first job", """
<p>Apply directly rather than through job boards. Most small breweries hire
through conversation, not process.</p>
<p>Visit in person during quiet hours, mid afternoon on a weekday rather than a
Friday night. Ask about their process, not about a job, on the first visit. Show
up again.</p>
<p>Offer to be useful in a way that costs them nothing, whether that is a shift
of cleaning or help at a festival. A remarkable number of brewing careers started
exactly there.</p>
<p>Be honest about what you do not know. Breweries can train an inexperienced
person who listens. They cannot fix someone who overstates their competence
around expensive tanks.</p>"""),
    ],
    faqs=[
        ("Do I need a science degree to become a brewer?",
         "No. A food science or biotechnology background helps and shortens the learning "
         "curve, but many working brewers came through cellar work or formal brewing "
         "training instead."),
        ("What does a brewer earn in India?",
         "Entry level pay is modest and reflects a training period. It rises "
         "substantially with responsibility for quality and for a site. Specialists in "
         "quality, commissioning and consulting typically earn most."),
        ("Is homebrewing enough experience to get hired?",
         "It proves interest and teaches the process, which matters. It does not teach "
         "scale, cleaning regimes or consistency, so pair it with formal training or "
         "time on a working plant."),
        ("What is the fastest way in if I am changing career?",
         "Structured training plus deliberate sensory practice plus visible time on a "
         "real plant. The combination answers the only question a brewery is really "
         "asking, which is whether you are a risk to their beer."),
    ],
    cta=dict(title="Start with the fundamentals",
             body="Brewing Fundamentals covers brewing science, raw materials, "
                  "equipment and recipe formulation over four weeks, with mentorship.",
             href=COURSES, label="See the course"),
    related=["beer-off-flavours", "start-a-microbrewery-india", "how-to-taste-beer"],
)

BREWING_FOR_INDIA = dict(
    slug="brewing-for-india",
    cat="Craft",
    h1="Brewing for Indian heat, water and palates",
    title="Brewing for Indian Heat and Water | Craft Beer School",
    desc="How heat, water chemistry, imported ingredients and the cold chain change "
         "brewing decisions in India, and which styles genuinely work here.",
    teaser="A recipe that works in Munich does not automatically work in May in "
           "India. The variables that change are worth knowing.",
    standfirst="Most brewing literature assumes a temperate climate, soft predictable "
               "water and short supply lines. India offers none of those, so the useful "
               "question is which decisions actually have to change.",
    read="9 min", updated="2026-09-03", updated_label="September 2026",
    sections=[
        ("Heat is a design constraint, not a detail", """
<p>Fermentation generates its own heat. In a cool climate that is a manageable
nuisance. In Indian ambient conditions it compounds with everything else, and
cooling capacity becomes the constraint the whole brewery is built around.</p>
<p>Under specified glycol shows up as fermentation running warmer than intended,
which pushes yeast to produce more esters and fusel alcohols. The result is beer
that tastes hot, solventy or oddly fruity for its style, and the cause is
mechanical rather than a recipe fault.</p>
<p>Two practical consequences. Specify chilling generously, for the worst month
rather than the average. And treat fermentation temperature as a controlled
variable you record every day, because it is the single largest driver of flavour
consistency.</p>"""),
        ("Water, and the chlorine problem", """
<p>Water is most of the beer and varies enormously across India, so brewing
without testing it is guessing.</p>
<p>The most common and most avoidable fault comes from chlorine or chloramine in
municipal supply. It reacts with compounds from the malt to produce chlorophenols,
which taste medicinal or plastic at vanishingly small concentrations. Carbon
filtration removes it, and doing so eliminates an entire category of complaint at
trivial cost.</p>
<p>Beyond that, mineral content shapes character. Sulphate accentuates hop
bitterness and dryness, which suits pale hoppy beers. Chloride accentuates
fullness and sweetness, which suits malty ones. Adjusting the balance between
those two is one of the cheapest ways to make a beer taste like the style
intends.</p>
<p>Very hard or alkaline source water raises mash pH, which causes poor
conversion and extracts harshness. Test first, then treat.</p>"""),
        ("Ingredients arrive late, warm and priced in dollars", """
<p>Most specialty malt and nearly all aroma hops are imported. That creates three
recurring problems.</p>
<p><strong>Cost and currency.</strong> Recipes that lean on large late hop
additions are considerably more expensive to run here than the same recipe
abroad.</p>
<p><strong>Consistency.</strong> A variety you built a flagship around may be
unavailable for a season. Brewers who understand hop character rather than hop
brand names can substitute intelligently. Those who only know names cannot.</p>
<p><strong>Storage.</strong> Hops lose aroma with heat and time, and malt is
vulnerable to humidity. Cold storage for hops is not optional, and grain needs to
be kept dry and used in rotation.</p>
<p>The good news is that base malt and adjuncts are increasingly available
regionally, and building recipes around what is reliably obtainable is a
discipline that improves consistency rather than compromising it.</p>"""),
        ("Which styles genuinely work here", """
<p>Climate and palate both push in the same direction.</p>
<p><strong>Wheat beers.</strong> Refreshing, aromatic, low bitterness. The most
reliable converter of new drinkers, and forgiving to brew.</p>
<p><strong>Lagers and pilsners.</strong> The volume driver in a mature venue.
Demanding, because there is nowhere to hide a flaw, and tank hungry because they
condition slowly. Worth doing well precisely because most do not.</p>
<p><strong>Pale ales.</strong> Hop character without the cost and perishability of
a heavily late hopped IPA. A sensible commercial middle.</p>
<p><strong>Hazy IPAs.</strong> Popular and profitable, but the most perishable
thing you can make. Only viable with genuine cold chain discipline and fast
turnover.</p>
<p><strong>Dark beers.</strong> Sell in smaller volume year round but build
reputation, and roast character survives warm serving better than delicate hop
aroma does.</p>"""),
        ("Serving is part of the recipe", """
<p>A well brewed beer is routinely ruined in the last three metres.</p>
<p>Serving too cold, which is the Indian default, mutes aroma and flavour. Let
lagers sit around 6 to 8 degrees and ales a little warmer, and the beer you
actually brewed becomes perceptible.</p>
<p>Dispense matters as much. Incorrect line pressure produces foaming, wasted
beer and inconsistent pours. Dirty lines produce sour and buttery flavours that
customers will attribute to your brewing, not to your cleaning schedule. Clean
lines on a fixed cycle and record it.</p>
<p>Glassware must be beer clean. Detergent film destroys head retention and
carries aroma from the previous drink.</p>"""),
        ("Shelf life deserves a number", """
<p>Fresh is not a marketing word, it is a measurable property, and different
styles decay at different rates.</p>
<p>Hop aroma fades fastest, so a hazy IPA is materially different after a few
weeks warm. Oxidation flattens everything over time and accelerates with
temperature. Dark and stronger beers hold up longest.</p>
<p>Decide a shelf life per style, based on your own tasting rather than a
default, and manage stock rotation to it. Then protect the cold chain from
brewery to glass, because in Indian conditions that chain is usually where the
quality you paid for is lost.</p>"""),
    ],
    faqs=[
        ("Does Indian brewing water need treatment?",
         "Almost always. At minimum remove chlorine or chloramine with carbon filtration, "
         "because it causes medicinal off flavours. Beyond that, test your source and "
         "adjust mineral balance to suit the styles you brew."),
        ("Why does my beer taste hot or solventy?",
         "Usually fermentation ran warmer than intended, producing fusel alcohols. In "
         "Indian conditions that generally points at cooling capacity rather than the "
         "recipe or the yeast."),
        ("Which beer styles sell best in India?",
         "Wheat beers convert new drinkers most reliably, and lagers drive volume in a "
         "mature venue. Hoppy styles are popular but demand real cold chain discipline "
         "because their aroma fades quickly."),
        ("How cold should beer be served?",
         "Cooler than most Indian venues pour it. Around 6 to 8 degrees Celsius for "
         "lagers and slightly warmer for ales lets the aroma and flavour actually "
         "reach the drinker."),
    ],
    cta=dict(title="Brew for the conditions you actually have",
             body="Advanced Brewing Science covers water chemistry, microbiology, "
                  "fermentation control and quality assurance over six weeks.",
             href=COURSES, label="See the course"),
    related=["beer-off-flavours", "craft-beer-in-india", "beer-styles-guide"],
)

ARTICLES_B = [CRAFT_BEER_INDIA, START_MICROBREWERY, BECOME_A_BREWER, BREWING_FOR_INDIA]
