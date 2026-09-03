# -*- coding: utf-8 -*-
"""Page bodies: Careers, Contact, FAQ, Privacy, Refund."""
from pages_a import banner

# ============================================================================
CAREERS = banner("Careers","Careers &amp; Mentors","Help India learn beer.",
    "Become a CBS mentor or join the team. If you love brewing and love teaching it, there's a seat for you.") + """
<section>
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Become a CBS Mentor</span>
      <h2>Teach what you know. Grow the craft.</h2>
      <p>Are you a working brewer, a sensory pro, a packaging designer or a brewery founder? Join Craft Beer School as a guest mentor and help the next generation of Indian brewers go from passion to profession.</p>
      <ul class="checklist">
        <li>Lead a session in your area of expertise</li>
        <li>Flexible, remote-friendly, paid engagements</li>
        <li>Small cohorts, real impact, real conversations</li>
        <li>Free CBS membership and community access</li>
      </ul>
      <a href="#apply" class="btn btn-amber">Apply to mentor</a>
    </div>
    <div class="split-media reveal"><div class="offset-img"><img src="assets/team1.jpg" alt="Join the Craft Beer School mentor team" loading="lazy" /></div></div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow">Open roles</span><h2>Ways to join.</h2></div>
    <div class="grid-3">
      <article class="card reveal"><div class="card-body"><span class="cat">Guest Faculty</span><h3>Course Mentor</h3><p>Own a module in brewing science, business, branding or sensory. Remote, per-cohort.</p></div></article>
      <article class="card reveal"><div class="card-body"><span class="cat">In person</span><h3>Workshop Host</h3><p>Run hands-on brewery days and tastings in Bengaluru and beyond.</p></div></article>
      <article class="card reveal"><div class="card-body"><span class="cat">Media</span><h3>Podcast Collaborator</h3><p>Co-host or guest on Cheers Chatty Ventures. Bring a story worth pouring.</p></div></article>
    </div>
  </div>
</section>

<section id="apply">
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Application</span>
      <h2>Tell us about you.</h2>
      <p>Send a short note about your background and how you'd like to contribute. We read every one and reply within a few days.</p>
      <p style="color:var(--ink-soft);font-size:.9rem">Prefer email? Write to <a href="mailto:chatty@cheerschattyventures.com" style="color:var(--blue);text-decoration:underline">chatty@cheerschattyventures.com</a>.</p>
    </div>
    <form class="form-card reveal" data-formspree>
      <input type="hidden" name="_subject" value="Mentor / careers application, Craft Beer School" />
      <div class="row2">
        <div class="field"><label>Name</label><input name="name" required placeholder="Your name" /></div>
        <div class="field"><label>Phone</label><input name="phone" placeholder="+91" /></div>
      </div>
      <div class="field"><label>Email</label><input type="email" name="email" required placeholder="you@email.com" /></div>
      <div class="field"><label>Area of expertise</label>
        <select name="expertise" required><option value="">Select…</option><option>Brewing science</option><option>Sensory / tasting</option><option>Business / operations</option><option>Branding / packaging</option><option>Podcast / media</option><option>Other</option></select>
      </div>
      <div class="field"><label>About you</label><textarea name="about" required placeholder="A few lines on your background and how you'd like to contribute…"></textarea></div>
      <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" />
      <button class="btn btn-amber" type="submit">Send application</button><a class="btn btn-wa" href="__WA__" target="_blank" rel="noopener" data-cta="form-whatsapp">[[whatsapp]] WhatsApp instead</a>
      <p class="form-msg" role="status" aria-live="polite" style="display:none;margin-top:.9rem;font-size:.85rem;font-weight:600"></p>
    </form>
  </div>
</section>
"""

# ============================================================================
CONTACT = banner("Contact","Contact &amp; Enroll","Let's get you pouring.",
    "Enrol, ask a question or book a tasting. We reply within 24 hours.") + """
<section>
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Reach us</span>
      <h2>Talk to Craft Beer School.</h2>
      <p>Whether you're a beer lover chasing your first batch or a professional levelling up, we'd love to hear from you.</p>
      <ul class="checklist" style="margin-top:1.5rem">
        <li><b>Phone / WhatsApp:</b> <a href="tel:+919820925347" style="color:var(--blue)">+91 98209 25347</a> · <a href="tel:+919082256507" style="color:var(--blue)">+91 90822 56507</a></li>
        <li><b>Email:</b> <a href="mailto:chatty@cheerschattyventures.com" style="color:var(--blue)">chatty@cheerschattyventures.com</a></li>
        <li><b>Based in:</b> Bengaluru, India, serving learners across the world</li>
        <li><b>Hours:</b> Mon, Sat, 10:00-19:00 IST</li>
      </ul>
      <p style="margin-top:1.2rem"><a href="faq.html" class="link-arrow">Read the FAQ first</a></p>
    </div>
    <form class="form-card reveal" id="enroll" data-formspree>
      <h3 style="margin-bottom:1.1rem">Enrol or enquire</h3>
      <input type="hidden" name="_subject" value="New enquiry, Craft Beer School" />
      <div class="row2">
        <div class="field"><label>Name</label><input name="name" required placeholder="Your name" /></div>
        <div class="field"><label>Phone</label><input name="phone" required placeholder="+91" /></div>
      </div>
      <div class="field"><label>Email</label><input type="email" name="email" required placeholder="you@email.com" /></div>
      <div class="field"><label>Interested in</label>
        <select name="course" required><option value="">Select…</option><option>Brewing Fundamentals</option><option>Advanced Brewing Science</option><option>Brewery Business Management</option><option>Style Specialization</option><option>Beer Branding &amp; Packaging</option><option>Sensory Evaluation</option><option>In-person workshop / tasting</option><option>Not sure yet</option></select>
      </div>
      <div class="row2">
        <div class="field"><label>City</label><input name="city" placeholder="Optional" /></div>
        <div class="field"><label>Promo code</label><input name="promo" placeholder="Optional" /></div>
      </div>
      <div class="field"><label>Message</label><textarea name="message" placeholder="Anything you'd like us to know…"></textarea></div>
      <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" />
      <button class="btn btn-amber" type="submit">Apply now</button><a class="btn btn-wa" href="__WA__" target="_blank" rel="noopener" data-cta="form-whatsapp">[[whatsapp]] WhatsApp instead</a>
      <p class="form-msg" role="status" aria-live="polite" style="display:none;margin-top:.9rem;font-size:.85rem;font-weight:600"></p>
    </form>
  </div>
</section>
"""

# ============================================================================
# Every rendered FAQ is recorded so seo.py can emit FAQPage structured data
# from the same source. Answer engines quote these directly.
FAQ_ITEMS = []


def faq_item(q, a):
    FAQ_ITEMS.append((q, a))
    return f"<details class=\"reveal\"><summary>{q}</summary><p>{a}</p></details>"

FAQ = banner("FAQ","Questions","Everything you wanted to ask.",
    "Courses, format, certification, payment and refunds, answered.") + f"""
<section>
  <div class="wrap">
    <div class="faq">
      {faq_item("Do I need any brewing experience to start?","Not at all. Brewing Fundamentals is built for complete beginners, we start with the science and ingredients and build up from there. Many of our students had no prior brewing background.")}
      {faq_item("Are the courses online or in person?","Both. Our six core courses run as flexible live online sessions you can join from any city. We also offer in-person workshops, home-visit brewing and guided tastings, mainly around Bengaluru.")}
      {faq_item("What are the class sizes?","Small by design. Tiny cohorts mean every question gets answered and every batch gets tasted, with one-on-one mentorship from industry experts.")}
      {faq_item("Do you help with WSET or Cicerone certification?","Yes. We provide structured exam preparation for WSET and Cicerone so you can build globally recognised beer knowledge and sit the exams with confidence.")}
      {faq_item("How do I enrol and pay?","Pick a course and submit the enquiry form or WhatsApp us. We confirm dates and share payment details. Seats are confirmed once payment is received, cohorts fill quickly.")}
      {faq_item("What is your refund policy?","See our full <a href='refund.html' style='color:var(--blue);text-decoration:underline'>Refund &amp; Cancellation policy</a>. In short, cancellations before a cohort starts are eligible for a refund within the stated window.")}
      {faq_item("Do I get a certificate?","Yes, courses include a digital certificate and access to the Craft Beer School community.")}
      {faq_item("Can you teach a group or corporate session?","Absolutely. We run private workshops and tastings for teams and events. Reach out via the <a href='contact.html' style='color:var(--blue);text-decoration:underline'>contact page</a> with your group size and dates.")}
    </div>
    <p style="text-align:center;margin-top:2.5rem;color:var(--ink-soft)">Still curious? <a href="contact.html#enroll" class="link-arrow" style="display:inline-flex" data-cta="ask-us-directly">Ask us directly</a></p>
  </div>
</section>
"""

# ============================================================================
PRIVACY = banner("Privacy","Legal","Privacy Policy","How we collect, use and protect your information.") + """
<section>
  <div class="wrap prose">
    <p class="updated">Last updated: July 2026</p>
    <p>Craft Beer School ("we", "us") respects your privacy. This policy explains what we collect when you use our website or enrol in a course, and how we use it.</p>
    <h2>Information we collect</h2>
    <ul>
      <li>Contact details you submit through our forms, name, email, phone, city.</li>
      <li>Course preferences and messages you send us.</li>
      <li>Basic, non-identifying usage data (such as pages visited) to improve the site.</li>
    </ul>
    <h2>How we use it</h2>
    <ul>
      <li>To respond to enquiries and process enrolments.</li>
      <li>To send course information, dates and updates you've asked for.</li>
      <li>To improve our courses, content and website.</li>
    </ul>
    <h2>Sharing</h2>
    <p>We do not sell your personal information. We share it only with trusted services that help us operate, for example, form delivery and email, and only as needed to provide our services.</p>
    <h2>Your choices</h2>
    <p>You can ask us to access, correct or delete your information at any time by emailing <a href="mailto:chatty@cheerschattyventures.com">chatty@cheerschattyventures.com</a>. You can unsubscribe from updates at any time.</p>
    <h2>Cookies</h2>
    <p>We use minimal cookies for basic functionality and analytics. You can control cookies through your browser settings.</p>
    <h2>Contact</h2>
    <p>Questions about this policy? Email <a href="mailto:chatty@cheerschattyventures.com">chatty@cheerschattyventures.com</a> or call +91 98209 25347.</p>
  </div>
</section>
"""

# ============================================================================
REFUND = banner("Refunds","Legal","Refund &amp; Cancellation","Clear terms for online and in-person courses.") + """
<section>
  <div class="wrap prose">
    <p class="updated">Last updated: July 2026</p>
    <p>We want you to enrol with confidence. This policy explains cancellations and refunds for Craft Beer School courses and workshops.</p>
    <h2>Cancellations by you</h2>
    <ul>
      <li><b>Before a cohort starts:</b> Cancel at least 7 days before the start date for a full refund, less any payment-processing fees.</li>
      <li><b>Within 7 days of the start date:</b> We can offer a credit toward a future cohort, subject to availability.</li>
      <li><b>After a course has started:</b> Fees are non-refundable, as seats are limited and materials are prepared per student.</li>
    </ul>
    <h2>In-person workshops &amp; tastings</h2>
    <p>Because in-person sessions involve booked venues, ingredients and equipment, cancellations within 72 hours of the session are non-refundable but may be rescheduled once, subject to availability.</p>
    <h2>Cancellations by us</h2>
    <p>If we cancel or reschedule a cohort, you may choose a full refund or a transfer to the next available cohort at no extra cost.</p>
    <h2>How to request</h2>
    <p>Email <a href="mailto:chatty@cheerschattyventures.com">chatty@cheerschattyventures.com</a> with your name and course details. Approved refunds are processed to the original payment method within 7-10 business days.</p>
    <p style="margin-top:1.5rem"><a href="contact.html#enroll" class="link-arrow" data-cta="questions-contact-us">Questions? Contact us</a></p>
  </div>
</section>
"""
