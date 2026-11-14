"""Advanced Brewing Science poster band on the home page, in the slot the Diwali poster used.

It hides the Beer for Starters band below it until UNTIL. After that a date check removes
this band and the Starters band comes back by itself.
"""
UNTIL = "2026-11-22T00:00:00+05:30"  # the online batch starts on 21 November 2026
SLUG = "advanced-brewing-science-course.html"

HOME_BAND = f"""
<section class="abs-band" aria-label="Advanced Brewing Science" style="padding-block:0;background:#f7f3ea;border-bottom:1px solid #e3dccb">
  <style>.abs-band:not(.abs-over)+.okt-band{{display:none}}.abs-band.abs-over{{display:none}}</style>
  <script>if(new Date()>=new Date('{UNTIL}'))document.currentScript.parentNode.classList.add('abs-over')</script>
  <div class="wrap" style="display:flex;align-items:center;gap:clamp(1rem,3vw,2.5rem);flex-wrap:wrap;padding-block:clamp(1.4rem,3vw,2.2rem)">
    <a href="{SLUG}" data-cta="home-abs-poster" style="flex:0 1 280px;max-width:100%;display:block">
      <img src="assets/advanced-brewing-science-poster-560.jpg" srcset="assets/advanced-brewing-science-poster-560.jpg 1x, assets/advanced-brewing-science-poster.jpg 2x" width="560" height="996" loading="eager" style="width:100%;height:auto;border-radius:12px;box-shadow:0 14px 30px -14px rgba(17,32,64,.45)"
           alt="Advanced Brewing Science poster: a new live online batch starts 21 November 2026, six weeks for working brewers, Brewing Fundamentals graduates and serious homebrewers"></a>
    <div style="flex:1 1 320px">
      <span class="eyebrow">New online batch · starts 21 November 2026</span>
      <h2 style="margin:.3rem 0">Advanced Brewing Science, 6 weeks live online.</h2>
      <p style="margin:0">Take your brewing knowledge further with chemistry, microbiology and fermentation. Built for working brewers, Brewing Fundamentals graduates and serious homebrewers.</p>
    </div>
    <a href="{SLUG}" class="btn btn-amber" data-cta="home-abs">Enrol now [[arrow-right]]</a>
  </div>
</section>
"""

# First line of the top strip; build.py removes it after UNTIL and shows the next offer.
ANNOUNCE = (f'<span class="ann abs-ann">New online batch: Advanced Brewing Science starts 21 November 2026. '
            f'<a href="{SLUG}" data-cta="announce-abs">Enrol now [[arrow-right]]</a></span>')
