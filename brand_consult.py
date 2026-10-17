"""Brand consultancy with Chatty Girija: the page every branding guide's CTA lands on.

The form posts to an Apps Script web app (backend/brand-enquiries) that emails
Chatty directly, with Reply-To set to the enquirer. "WhatsApp instead" opens a
chat with her, carrying whatever the person already typed.
"""
from urllib.parse import quote

import mentors

SLUG = "brand-consultancy.html"
HREF = f"{SLUG}#enquire"
# ponytail: empty until the owner authorises the script; the form then falls back to mailto Chatty.
LIVE = False
ENDPOINT = ("https://script.google.com/macros/s/"
            "AKfycbweTRmWW0c5ANWl9Hi41fGG21ek4LtG9oERVB1mLh1xwD3EBPBF5B-n6AbR3cu3zGw3/exec")
TITLE = "Brand Consultancy for Breweries | Craft Beer School"
DESC = ("Talk to Chatty Girija, 30 years in advertising, about your brewery's brand: "
        "positioning, naming, labels, rebrands and launches.")
NEEDS = ["A new brewery brand", "A rebrand or refresh", "Positioning and brand strategy",
         "Naming a brewery or beer", "Labels and packaging", "A launch plan", "Brand voice and social media",
         "Not sure yet"]
WA = (f"https://wa.me/{mentors.WHATSAPP_NUMBER}?text="
      + quote("Hi Chatty, I would like to talk about my brewery's brand."))


def page(banner):
    options = "".join(f"<option>{n}</option>" for n in NEEDS)
    body = banner("Brand consultancy", "Brand consultancy", "Talk to Chatty about your brand.",
                  "Positioning, naming, labels, rebrands and launches for breweries, brewpubs and drinks brands.") + f"""
<section>
  <div class="wrap split">
    <div class="prose-block reveal">
      <span class="eyebrow">Who you work with</span>
      <h2>Thirty years of advertising, now poured into beer.</h2>
      <p><a href="mentor-chatty-girija.html">Chatty Girija</a> spent more than 30 years in advertising before turning that craft to beer. She hosts the <a href="podcast.html">Cheers Chatty Beer Podcast</a> and teaches branding at Craft Beer School.</p>
      <p>She works with owners and their teams on site or remotely. The work stays with you: your team leaves able to run it.</p>
      <ul class="checklist" style="margin-top:1.2rem"><li>Brand audits and rebrand plans</li><li>Positioning workshops and brand strategy</li><li>Naming shortlists for a brewery or a beer</li><li>Label systems and packaging direction</li><li>Brand voice for menus, Instagram and WhatsApp</li><li>Launch plans that respect India's alcohol advertising rules</li></ul>
      <p style="margin-top:1.2rem">Not ready to talk? Start with the free guides: <a href="brewery-branding-guide.html">branding a new brewery</a> and <a href="brewery-rebrand-guide.html">rebranding a brewery</a>.</p>
    </div>
    <form class="form-card reveal" id="enquire" data-formspree{f' data-endpoint="{ENDPOINT}"' if LIVE else ""} data-thanks="Thank you. Your note has gone straight to Chatty. She will reply within 24 hours.">
      <h3 style="margin-bottom:1.1rem">Send Chatty a note</h3>
      <div class="row2">
        <div class="field"><label>Name</label><input name="name" required autocomplete="name" placeholder="Your name" /></div>
        <div class="field"><label>Brewery or brand</label><input name="company" autocomplete="organization" placeholder="Optional" /></div>
      </div>
      <div class="row2">
        <div class="field"><label>Phone or WhatsApp</label><input name="phone" type="tel" inputmode="tel" required autocomplete="tel" placeholder="+91" /></div>
        <div class="field"><label>Email</label><input type="email" name="email" required autocomplete="email" placeholder="you@email.com" /></div>
      </div>
      <div class="row2">
        <div class="field"><label>Looking for</label><select name="course" required><option value="">Select…</option>{options}</select></div>
        <div class="field"><label>City</label><input name="city" autocomplete="address-level2" placeholder="Optional" /></div>
      </div>
      <div class="field"><label>Message</label><textarea name="message" placeholder="Where is your brand today and what would you like to change?"></textarea></div>
      <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" />
      <button class="btn btn-amber" type="submit" data-cta="brand-email">Send to Chatty</button><a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener" data-cta="brand-whatsapp">[[whatsapp]] WhatsApp Chatty instead</a>
      <p class="form-msg" role="status" aria-live="polite" style="display:none;margin-top:.9rem;font-size:.85rem;font-weight:600"></p>
    </form>
  </div>
</section>
"""
    return TITLE, DESC, "", body
