"""Home page 'From the brew floor' strip: a daily brewer's tip beside the latest industry updates."""
import datetime
import html
import json
import pathlib

HERE = pathlib.Path(__file__).parent
CAT = "Industry update"


def _tips():
    return json.loads((HERE / "content/tips.json").read_text())


def _updates(limit=4):
    """Latest live Industry update guides, newest first."""
    today = datetime.date.today().isoformat()
    plan = {p["slug"]: p for p in json.loads((HERE / "content/plan.json").read_text())}
    live = [p for p in plan.values() if p["cat"] == CAT and p["date"] <= today
            and (HERE / f"content/articles/{p['slug']}.json").exists()]
    live.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return [json.loads((HERE / f"content/articles/{p['slug']}.json").read_text()) for p in live[:limit]]


def home_section():
    tips = _tips()
    if not tips:
        return ""
    first = tips[0]
    data = html.escape(json.dumps(tips, ensure_ascii=False), quote=True)
    rows = "".join(
        f'<li><a href="{a["slug"]}.html" data-cta="home-update"><b>{html.escape(a["h1"])}</b>'
        f'<span>{html.escape(a["teaser"])}</span></a></li>' for a in _updates())
    news = (f'<div class="bf-news reveal"><span class="eyebrow">What is new in brewing</span>'
            f'<ol class="bf-list">{rows}</ol>'
            f'<a href="blog.html" class="link-arrow" data-cta="home-updates-all">All guides on the blog</a></div>') if rows else ""
    return f"""
<section class="sand brew-floor">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">From the brew floor</span><h2>One tip a day, and what is new this month.</h2></div>
    <div class="bf-grid">
      <figure class="bf-tip reveal" data-tips="{data}">
        <span class="bf-label">Brewer's tip <span class="bf-no">No. 1</span></span>
        <blockquote class="bf-text">{html.escape(first["tip"])}</blockquote>
        <figcaption class="bf-foot">
          <a class="link-arrow on-dark bf-link" href="{first["slug"]}.html" data-cta="home-tip-guide">Read the guide</a>
          <button type="button" class="bf-next" data-cta="home-tip-next" aria-label="Show another tip">Another tip</button>
        </figcaption>
      </figure>
      {news}
    </div>
  </div>
</section>
<script>
(function(){{
  var box=document.querySelector('.bf-tip'); if(!box) return;
  var tips; try {{ tips=JSON.parse(box.dataset.tips); }} catch(e) {{ return; }}
  var i=Math.floor(Date.now()/864e5)%tips.length;
  var text=box.querySelector('.bf-text'), link=box.querySelector('.bf-link'), no=box.querySelector('.bf-no');
  function show(k){{ text.textContent=tips[k].tip; link.href=tips[k].slug+'.html'; no.textContent='No. '+(k+1); }}
  show(i);
  box.querySelector('.bf-next').addEventListener('click',function(){{ i=(i+1)%tips.length; show(i); }});
}})();
</script>
"""
