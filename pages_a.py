# -*- coding: utf-8 -*-
"""Page bodies: Home, About, Courses, Resources, Blog."""

# ---- shared course card snippets -------------------------------------------
def course(no, tag, dur, name, blurb, items, price, ph):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f"""<article class="card course-card reveal">
  <div class="top"><span class="course-no">{no} / {tag}</span><span class="course-dur">{dur}</span></div>
  <div class="card-body">
    <h3>{name}</h3>
    <p>{blurb}</p>
    <ul>{lis}</ul>
    <div class="foot"><span class="price">{price}</span><a href="contact.html" class="btn btn-ghost" style="padding:.55rem 1.1rem">Enroll</a></div>
  </div>
</article>"""

C1 = course("01","Foundations","4 Weeks","Brewing Fundamentals",
    "The science of brewing — ingredients, equipment, technique. Online sessions plus your first real recipe.",
    ["Brewing science &amp; theory","Raw materials &amp; quality","Equipment &amp; sanitation","Recipe formulation basics"],"₹5,999","")
C2 = course("02","Deep Craft","6 Weeks","Advanced Brewing Science",
    "Go deeper into chemistry, microbiology and advanced fermentation for serious brewers and pros.",
    ["Microbiology &amp; fermentation","Water chemistry optimization","Advanced mashing techniques","Quality assurance &amp; control"],"₹12,999","")
C3 = course("03","Business","3 Weeks","Brewery Business Management",
    "The business behind the brew — plan, launch and grow a brewery, from finance to distribution.",
    ["Business planning &amp; finance","Licensing &amp; regulations","Marketing &amp; branding","Distribution strategies"],"₹8,999","")
C4 = course("04","Mastery","8 Weeks","Style Specialization",
    "Master IPAs, stouts, lagers, sours and Belgian ales — history, technique and award-winning versions.",
    ["Style guidelines &amp; origins","Specialized techniques","Ingredient selection &amp; pairing","Competition brewing skills"],"₹18,999","")
C5 = course("05","Brand","3 Weeks","Beer Branding &amp; Packaging",
    "Build a beer brand that stands out and packaging that sells — for aspiring brewers and founders.",
    ["Build your brand identity","Design packaging that pops","Launch planning &amp; promotion","Certificate &amp; community access"],"₹4,999","")
C6 = course("06","Palate","2 Weeks","Sensory Evaluation",
    "Train your palate like a pro — taste, identify off-flavours and score beer with real sensory methods.",
    ["Flavour chemistry","Tasting techniques","Off-flavour identification","Quality scoring systems"],"₹5,999","")

# ============================================================================
HOME = f"""
<section class="hero">
  <div class="wrap hero-offset">
    <div class="hero-copy reveal">
      <span class="eyebrow">India · Online &amp; In-Person</span>
      <h1 class="display">Brew like<br>you <span class="script">mean it.</span></h1>
      <p class="lead">India's trusted beer school. We teach everything inside and outside the bottle — ingredients, brewing, tasting, branding and the business of beer. Live sessions, guided tastings and hands-on brewery workshops.</p>
      <div class="hero-cta">
        <a href="courses.html" class="btn btn-amber">Explore courses →</a>
        <div class="sticker"><b>₹999</b><small>Intro session · all in</small></div>
      </div>
    </div>
    <div class="hero-media reveal">
      <div class="offset-img"><img src="assets/hero.jpg" alt="A craft beer tasting flight — grain to glass at Craft Beer School" width="1200" height="900" loading="eager" fetchpriority="high" /></div>
    </div>
  </div>
</section>

<section style="padding-block:0">
  <div class="wrap">
    <div class="stats reveal">
      <div class="stat"><b>6</b><span>Career-grade courses</span></div>
      <div class="stat"><b>1:1</b><span>Expert mentorship</span></div>
      <div class="stat"><b>WSET</b><span>+ Cicerone prep</span></div>
      <div class="stat"><b>∞</b><span>Grain to glass</span></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Basics to Business</span>
      <h2>Six pours, one path from grain to glass.</h2>
      <p class="lead">Each course blends theory with real practice — small groups, one-on-one mentorship, industry experts.</p>
    </div>
    <div class="grid-3">{C1}{C2}{C3}</div>
    <div style="margin-top:2rem"><a href="courses.html" class="link-arrow">See all six courses &amp; in-person workshops</a></div>
  </div>
</section>

<section class="navy-sec">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Why Craft Beer School</span><h2>Better beer education brews better beer.</h2></div>
    <div class="features">
      <div class="feature reveal" style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)"><div class="ic">[[flask]]</div><h3 style="color:#fff">Small batches, big learning</h3><p style="color:rgba(255,255,255,.7)">Tiny cohorts so every question gets answered and every batch gets tasted.</p></div>
      <div class="feature reveal" style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)"><div class="ic">[[cap]]</div><h3 style="color:#fff">One-on-one mentorship</h3><p style="color:rgba(255,255,255,.7)">Learn directly from working brewers, sensory pros and founders.</p></div>
      <div class="feature reveal" style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)"><div class="ic">[[globe]]</div><h3 style="color:#fff">Learn anywhere</h3><p style="color:rgba(255,255,255,.7)">Flexible live online sessions you can join from any city, plus in-person workshops.</p></div>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap split">
    <div class="split-media reveal"><div class="offset-img"><img src="assets/team1.jpg" alt="The Craft Beer School team" loading="lazy" /></div></div>
    <div class="prose-block reveal">
      <span class="eyebrow">Free Resources</span>
      <h2>Start learning before you enrol.</h2>
      <p>Beer 101, a styles primer, a working brewing glossary and calculators — everything you need to sharpen your palate and your process, on the house.</p>
      <ul class="checklist"><li>Beer 101 crash course</li><li>Beer styles &amp; off-flavour guides</li><li>Brewing calculators &amp; tasting tools</li></ul>
      <a href="resources.html" class="link-arrow">Browse the resource library</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">The Journal · Blog &amp; Podcasts</span><h2>Insights from the brewing world.</h2></div>
    <div class="grid-3">
      <article class="card reveal"><img class="thumb" src="assets/blog-03.png" alt="The Rise of Craft Beer in India" loading="lazy" /><div class="card-body"><span class="cat">India</span><h3>The Rise of Craft Beer in India</h3><p>How a young, thirsty market is turning into one of the world's most exciting beer scenes.</p><div class="foot"><a href="blog.html" class="link-arrow">Read</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/blog-04.png" alt="How to Start a Microbrewery in India" loading="lazy" /><div class="card-body"><span class="cat">Business</span><h3>How to Start a Microbrewery in India</h3><p>Licensing, capital and the role of real brewing education in getting it right.</p><div class="foot"><a href="blog.html" class="link-arrow">Read</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/blog-06.png" alt="How to Taste Craft Beer Like a Pro" loading="lazy" /><div class="card-body"><span class="cat">Tasting</span><h3>How to Taste Craft Beer Like a Pro</h3><p>Aroma, flavour and mouthfeel — a simple framework to read any beer in the glass.</p><div class="foot"><a href="blog.html" class="link-arrow">Read</a></div></div></article>
    </div>
  </div>
</section>

<section class="sand">
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow">Beer Stories</span><h2>Spreading the cheer.</h2></div>
    <div class="grid-2">
      <blockquote class="quote reveal"><p>"I recently completed the Brewing Fundamentals course, hosted by Ankur and Chatty, and it was an outstanding experience."</p><div class="who"><span class="av">S</span><div><b>Sunil Prakash Rao</b><span>Singapore</span></div></div></blockquote>
      <blockquote class="quote reveal"><p>"I'm from Ratnagiri, with an M.Sc. in Nutrition and Food Processing. Despite no prior brewing background, this online class made it click."</p><div class="who"><span class="av">P</span><div><b>Poorva Shinde</b><span>Ratnagiri</span></div></div></blockquote>
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <h2>Join the Craft Beer School &amp; brew your future.</h2>
    <p>Open to beer lovers, professionals and future brewery founders — in India and across the world.</p>
    <a href="contact.html" class="btn btn-amber">Enroll now</a>
  </div>
</section>
"""

# ============================================================================
def banner(crumb, eyebrow, title, sub):
    return f"""<section class="banner"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a> / {crumb}</div>
  <span class="eyebrow">{eyebrow}</span>
  <h1 class="display">{title}</h1>
  <p>{sub}</p>
</div></section>"""

ABOUT = banner("About","About Craft Beer School","We teach the whole bottle.",
    "India's trusted online and in-person beer school — grain to glass and everything around it.") + """
<section>
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Our story</span>
      <h2>Better beer education brews better beer.</h2>
      <p>We are Craft Beer School — India's trusted beer school, online and in person. We teach everything inside and outside the bottle: from ingredients and brewing to tasting, branding and the business of beer.</p>
      <p>Our learning goes grain to glass and beyond through live sessions, guided tastings and hands-on brewery workshops. We also support WSET and Cicerone certification exam preparation, helping you build global beer knowledge and real industry confidence.</p>
      <p>Our courses are open to beer lovers, professionals and future brewery founders in India and across the world. Learn from industry experts through flexible online sessions and practical insights you can use anywhere.</p>
    </div>
    <div class="split-media reveal"><div class="offset-img"><img src="assets/team2.jpg" alt="Craft Beer School recognised at an industry awards ceremony" loading="lazy" /></div></div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow">What makes us different</span><h2>From passion to profession.</h2></div>
    <div class="features">
      <div class="feature reveal"><div class="ic">[[flask]]</div><h3>Small batches, big learning</h3><p>Tiny cohorts so every question gets answered and every batch gets tasted.</p></div>
      <div class="feature reveal"><div class="ic">[[cap]]</div><h3>One-on-one mentorship</h3><p>Learn directly from working brewers, sensory pros and founders who've built brands in India.</p></div>
      <div class="feature reveal"><div class="ic">[[globe]]</div><h3>Learn anywhere</h3><p>Flexible live online sessions you can join from any city — plus in-person brewery days.</p></div>
      <div class="feature reveal"><div class="ic">[[award]]</div><h3>Certification ready</h3><p>Structured WSET and Cicerone exam prep so your knowledge travels beyond the classroom.</p></div>
      <div class="feature reveal"><div class="ic">[[briefcase]]</div><h3>Passion to profession</h3><p>Curricula built to turn a hobby into a career or a business.</p></div>
      <div class="feature reveal"><div class="ic">[[beer]]</div><h3>Hands-on workshops</h3><p>Guided tastings and real brewery days — grain to glass, in person.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow">Your mentors</span><h2>Taught by people who brew.</h2></div>
    <div class="grid-3">
      <article class="card reveal"><img class="mentor-img" src="assets/team3.jpg" alt="Ankur Napa, Master Brewer and course instructor" loading="lazy" /><div class="card-body"><span class="cat">Course Instructor · Master Brewer</span><h3>Ankur Napa</h3><p>A Master Brewer with hands-on experience at global brewing giants. Bridges the science of the mash tun with the reality of the brewery floor.</p></div></article>
      <article class="card reveal"><img class="mentor-img" src="assets/team5.jpg" alt="Chatty Girija, beer podcaster and creative strategist" loading="lazy" /><div class="card-body"><span class="cat">Beer Podcaster · Creative Strategist</span><h3>Chatty Girija</h3><p>30+ years in advertising and a deep passion for craft beer. Brings the stories, the branding and the business of beer to every session.</p></div></article>
      <article class="card reveal"><img class="mentor-img" src="assets/team4.jpg" alt="Anu Rao, Head of Strategy and Operations" loading="lazy" /><div class="card-body"><span class="cat">Head of Strategy &amp; Operations</span><h3>Anu Rao</h3><p>15+ years across social responsibility, education and operations — keeping every cohort running smoothly, grain to glass.</p></div></article>
    </div>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Ready to go grain to glass?</h2><p>Pick a course, book a tasting, or ask us anything.</p><a href="contact.html" class="btn btn-amber">Talk to us</a></div></section>
"""

# ============================================================================
COURSES = banner("Courses","Basics to Business","Learn the art, science &amp; business of brewing.",
    "From your first pint to your professional journey. Simple, clear and full of real-world learning — online and in person.") + f"""
<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Online courses</span><h2>Six pours from grain to glass.</h2></div>
    <div class="grid-3">{C1}{C2}{C3}{C4}{C5}{C6}</div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">In person</span><h2>Hands-on workshops &amp; tastings.</h2><p class="lead">Prefer to learn at the bench? Join us in the room.</p></div>
    <div class="grid-2">
      <article class="card reveal"><div class="card-body"><span class="cat">1 Day · Intensive</span><h3>1-Day Super Intensive Craft Beer Course</h3><p>Step into a real microbrewery for a full day — from raw materials to a finished pour, condensed into one focused classroom-plus-brewery session.</p><div class="foot"><a href="contact.html" class="btn btn-ghost" style="padding:.55rem 1.1rem">Enquire</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="cat">1 Month · Advanced</span><h3>1-Month Advanced Craft Beer Brewing Course</h3><p>Bragger to a beer founder — an advanced, hands-on programme with focused mentorship over four weeks.</p><div class="foot"><a href="contact.html" class="btn btn-ghost" style="padding:.55rem 1.1rem">Enquire</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="cat">1 Day · At Home</span><h3>1-Day Home Visit Brewing Course</h3><p>Our brew master comes to your home with all the equipment and ingredients needed to brew your first batch, start to finish.</p><div class="foot"><a href="contact.html" class="btn btn-ghost" style="padding:.55rem 1.1rem">Enquire</a></div></div></article>
      <article class="card reveal"><div class="card-body"><span class="cat">2 Hours · Tasting</span><h3>2-Hour Craft Beer Tasting Course</h3><p>A guided tasting flight in Bengaluru — learn to read aroma, flavour and style in two focused hours.</p><div class="foot"><a href="contact.html" class="btn btn-ghost" style="padding:.55rem 1.1rem">Enquire</a></div></div></article>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow">How enrolment works</span><h2>From enquiry to first pour.</h2></div>
    <div class="steps">
      <div class="step reveal"><h3>Pick a course</h3><p>Choose a single pour or the full flight — online or in person.</p></div>
      <div class="step reveal"><h3>Reach out</h3><p>Submit the form or WhatsApp us. We confirm dates and answer questions.</p></div>
      <div class="step reveal"><h3>Confirm &amp; pay</h3><p>Secure your seat. Small cohorts fill quickly.</p></div>
      <div class="step reveal"><h3>Start brewing</h3><p>Join live sessions, get 1:1 mentorship and build your first recipe.</p></div>
    </div>
    <p style="text-align:center;margin-top:2rem;color:var(--ink-soft);font-size:.9rem">Enrolment is subject to our <a href="refund.html" style="color:var(--blue);text-decoration:underline">terms &amp; refund policy</a>.</p>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Not sure which course fits?</h2><p>Tell us where you are and where you want to go — we'll point you to the right pour.</p><a href="contact.html" class="btn btn-amber">Get a recommendation</a></div></section>
"""

# ============================================================================
RESOURCES = banner("Resources","Free beer education","Start learning today — on the house.",
    "Beer 101, a styles primer, a working glossary, calculators and tasting tools. No enrolment required.") + """
<section>
  <div class="wrap">
    <div class="grid-3">
      <article class="card reveal"><div class="ph amber">[[book-open]]</div><div class="card-body"><span class="cat">Start here</span><h3>Beer 101</h3><p>What is craft beer? Ingredients, the four pillars, and how a beer is actually made — grain to glass in plain English.</p><div class="foot"><a href="contact.html" class="link-arrow">Get the crash course</a></div></div></article>
      <article class="card reveal"><div class="ph mint">[[beer]]</div><div class="card-body"><span class="cat">Reference</span><h3>Beer Styles Primer</h3><p>IPAs, stouts, lagers, sours and Belgian ales — origins, flavour signatures and what to expect in the glass.</p><div class="foot"><a href="courses.html" class="link-arrow">Explore styles</a></div></div></article>
      <article class="card reveal"><div class="ph">[[book]]</div><div class="card-body"><span class="cat">Reference</span><h3>Brewing Glossary</h3><p>ABV, IBU, OG/FG, attenuation, lauter, dry hop — the words brewers use, defined clearly.</p><div class="foot"><a href="#glossary" class="link-arrow">Jump to glossary</a></div></div></article>
      <article class="card reveal"><div class="ph mint">[[calculator]]</div><div class="card-body"><span class="cat">Tool · App</span><h3>Indian Brewing Calculator</h3><p>ABV, attenuation and recipe math built for Indian brewing — check your numbers before you brew.</p><div class="foot"><a href="https://ankurnapa.github.io/indian-brewing-calculator/" class="link-arrow" target="_blank" rel="noopener">Open the calculator</a></div></div></article>
      <article class="card reveal"><div class="ph amber">[[wind]]</div><div class="card-body"><span class="cat">Tool · App</span><h3>Aroma Forge</h3><p>Predict a beer's aroma by superimposing digitised Weyermann malt aroma wheels — see how your grain bill smells before you brew.</p><div class="foot"><a href="https://ankurnapa.github.io/aroma-forge/" class="link-arrow" target="_blank" rel="noopener">Open Aroma Forge</a></div></div></article>
      <article class="card reveal"><div class="ph mint">[[sliders]]</div><div class="card-body"><span class="cat">Tool · App</span><h3>Advanced Brewing Calculator</h3><p>Pro-tier formulation, spec sheets and recipe comparison — for serious brewers who want the full picture.</p><div class="foot"><a href="https://ankurnapa.github.io/advanced-brewing-calc/" class="link-arrow" target="_blank" rel="noopener">Open the pro suite</a></div></div></article>
    </div>
  </div>
</section>

<section class="tint" id="glossary">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Quick reference</span><h2>Brewing glossary.</h2></div>
    <div class="grid-2">
      <div class="prose-block reveal">
        <p><b>ABV</b> — Alcohol by volume, the percentage of alcohol in the finished beer.</p>
        <p><b>OG / FG</b> — Original and final gravity, measured before and after fermentation to track sugar converted to alcohol.</p>
        <p><b>IBU</b> — International Bitterness Units, a measure of hop bitterness.</p>
        <p><b>Attenuation</b> — How much of the sugar the yeast fermented; higher means a drier beer.</p>
      </div>
      <div class="prose-block reveal">
        <p><b>Mash</b> — Steeping crushed malt in hot water to convert starch to fermentable sugar.</p>
        <p><b>Lauter / Sparge</b> — Separating and rinsing the sweet wort from the grain.</p>
        <p><b>Dry hop</b> — Adding hops after the boil for aroma without added bitterness.</p>
        <p><b>Lagering</b> — Cold conditioning that gives lagers their clean, crisp finish.</p>
      </div>
    </div>
    <p style="margin-top:1.5rem"><a href="courses.html" class="link-arrow">Go deeper in Brewing Fundamentals</a></p>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Ready to move from reading to brewing?</h2><p>Turn these fundamentals into a finished pour with a mentor beside you.</p><a href="courses.html" class="btn btn-amber">See the courses</a></div></section>
"""

# ============================================================================
BLOG = banner("Blog","The Journal · Blog &amp; Podcasts","Insights from the brewing world.",
    "Quality, marketing, tasting and the business of beer — plus podcast conversations with the people making it.") + """
<section>
  <div class="wrap">
    <div class="grid-3">
      <article class="card reveal"><img class="thumb" src="assets/blog-01.png" alt="What is Craft Beer? A Beginner's Guide" loading="lazy" /><div class="card-body"><span class="cat">Start here</span><h3>What is Craft Beer? A Beginner's Guide</h3><p>The ingredients, the four pillars and what actually makes a beer "craft" — in plain English.</p><div class="foot"><a href="#" class="link-arrow">Read</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/blog-02.png" alt="Types of Craft Beer: A Complete Style Guide" loading="lazy" /><div class="card-body"><span class="cat">Styles</span><h3>Types of Craft Beer: A Complete Style Guide</h3><p>IPAs, stouts, lagers, sours and Belgian ales — how to tell them apart in the glass.</p><div class="foot"><a href="#" class="link-arrow">Read</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/blog-03.png" alt="The Rise of Craft Beer in India" loading="lazy" /><div class="card-body"><span class="cat">India</span><h3>The Rise of Craft Beer in India</h3><p>How a young, thirsty market is turning into one of the world's most exciting beer scenes.</p><div class="foot"><a href="#" class="link-arrow">Read</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/blog-04.png" alt="How to Start a Microbrewery in India" loading="lazy" /><div class="card-body"><span class="cat">Business</span><h3>How to Start a Microbrewery in India</h3><p>Licensing, capital and the role of real brewing education in getting it right.</p><div class="foot"><a href="#" class="link-arrow">Read</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/blog-05.png" alt="Top Indian Craft Beer Brands You Must Try" loading="lazy" /><div class="card-body"><span class="cat">Culture</span><h3>Top Indian Craft Beer Brands You Must Try</h3><p>A tour of the breweries putting Indian craft beer on the map.</p><div class="foot"><a href="#" class="link-arrow">Read</a></div></div></article>
      <article class="card reveal"><img class="thumb" src="assets/blog-06.png" alt="How to Taste Craft Beer Like a Pro" loading="lazy" /><div class="card-body"><span class="cat">Tasting</span><h3>How to Taste Craft Beer Like a Pro</h3><p>Aroma, flavour and mouthfeel — a simple framework to read any beer.</p><div class="foot"><a href="#" class="link-arrow">Read</a></div></div></article>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Cheers Chatty Ventures</span>
      <h2>The podcast.</h2>
      <p>Every episode we sit down with brewers, founders and sensory pros to talk about what really happens between grain and glass — the wins, the off-flavours and the business of building a beer brand in India.</p>
      <a href="contact.html" class="link-arrow">Suggest a guest or topic</a>
    </div>
    <div class="split-media reveal"><div class="offset-img"><img src="assets/team5.jpg" alt="Chatty Girija, host of the Cheers Chatty Ventures beer podcast" loading="lazy" /></div></div>
  </div>
</section>

<section class="cta"><div class="wrap"><h2>Never miss a pour.</h2><p>Get new articles, podcast episodes and course dates in your inbox.</p><a href="contact.html" class="btn btn-amber">Join the list</a></div></section>
"""
