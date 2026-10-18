"""Current in-person offers: one list feeds the top banner, the blog finder's
recommendation box and the end-of-guide CTA on the guides closest to each offer.
Change an offer here and rebuild; nothing else needs touching."""

CITIES = "Pune, Delhi, Gurugram and Bengaluru"

OFFERS = [
    dict(key="wset",
         banner="Exam soon? Last-minute WSET Level 1 Beer prep, in person.",
         link="Enrol now",
         article="wset-level-1-beer-last-minute-training.html",
         title="Exam coming up? Get ready in a room with a tutor",
         body=f"In-person WSET Level 1 Beer prep in {CITIES}, in a group or one to one. Syllabus, guided tastings and a timed mock paper.",
         href="contact.html?course=WSET%20Beer%20exam%20prep#enroll",
         label="Save your seat",
         # Finder words that should surface this offer.
         words=["wset", "exam", "certification", "cicerone", "bjcp", "judge", "sommelier"],
         # Guides whose CTA now sells this offer.
         guides=["wset-beer-course", "brewing-certifications-guide", "cicerone-certification-guide",
                 "beer-judge-bjcp-exam", "beer-sommelier-career", "how-beer-judges-score"]),
    dict(key="bundle",
         banner="The Brewing Fundamentals Study Book with crosswords, for ₹1,999.",
         link="See the book",
         article="brewing-fundamentals-and-beer-crosswords-bundle.html",
         title="Study the full syllabus at your own pace",
         body="Study material, not a course: 17 chapters of notes with a crossword for each and every answer at the back. Pay ₹1,999 and we email it to you.",
         href="contact.html?course=Brewing%20Fundamentals%20Study%20Book#enroll",
         label="Order the book",
         words=["crossword", "book", "study", "notes", "bundle", "beginner", "fundamentals", "first brew", "homebrew"],
         guides=["how-beer-is-made-step-by-step", "homebrewing-starter-kit-india", "first-homebrew-mistakes",
                 "extract-vs-all-grain-brewing", "brew-in-a-bag-method", "brewing-in-a-small-indian-apartment"]),
    dict(key="in-person",
         banner=f"Hands-on brewing courses in {CITIES}.",
         link="1-day and 1-month courses",
         article="in-person-brewing-courses-pune-delhi-gurugram-bengaluru.html",
         title=f"Brew with us in {CITIES.replace(' and ', ' or ')}",
         body="Choose the 1-day course (₹25,000) or the 1-Month Intensive Brewing Excellence Course (₹1,25,000). Hands-on, with a brewer beside you.",
         href="contact.html?course=In-person+workshop+%2F+tasting#enroll",
         label="Save your seat",
         words=["pune", "delhi", "gurugram", "gurgaon", "bengaluru", "bangalore", "in person", "in-person",
                "workshop", "hands-on", "offline", "classroom"],
         guides=["become-a-brewer-india", "homebrewer-to-pro-brewer", "brewing-degree-vs-short-course",
                 "brewery-internship-india", "assistant-brewer-job", "jobs-in-a-brewery"]),
]

BY_GUIDE = {slug: o for o in OFFERS for slug in o["guides"]}
