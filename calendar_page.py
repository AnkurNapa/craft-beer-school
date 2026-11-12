# -*- coding: utf-8 -*-
"""2027 course calendar: every batch of every course, with a WhatsApp booking button per batch.

Dates come from content/calendar-2027.json, written by the 2027 calendar script
(~/Documents/Craft Beer School 2027 Calendar/build_calendar.py). Classes run on
weekends only and skip Indian holidays. English only: the slug is not in i18n PHASE1.
"""
import json
import pathlib
from datetime import date
from html import escape
from urllib.parse import quote

import mentors
import pages_a
from pages_a import banner, course_href

SLUG = "course-calendar-2027.html"
DATA = pathlib.Path(__file__).parent / "content" / "calendar-2027.json"
COURSES = {c["name"].replace("&amp;", "&"): c for c in pages_a.COURSE_DATA}
DAY = {"Sat": "Saturday", "Sun": "Sunday"}


def _runs():
    runs = json.loads(DATA.read_text())
    for r in runs:
        r["days"] = [date.fromisoformat(d) for d in r["classes"]]
    return runs


def _when(slots):
    """['Sat morning', 'Sun morning'] -> 'Saturday and Sunday mornings'."""
    days = [DAY[s.split()[0]] for s in slots]
    parts = sorted({s.split()[1] for s in slots})
    return f'{" and ".join(days)} {" and ".join(parts)}{"s" if len(days) > 1 else ""}'


def _book_href(course, r):
    dates = "; ".join(d.strftime("%a %d %b") for d in r["days"])
    text = (f"Hi Craft Beer School, I want to book {course} starting {r['days'][0]:%A %d %B %Y}. "
            f"Classes: {dates} ({_when(r['slots'])}). Please confirm my seat.")
    return f"https://wa.me/{mentors.WHATSAPP_NUMBER}?text={quote(text)}"


def _row(r):
    name = r["course"]
    c = COURSES[name]
    first, last = r["days"][0], r["days"][-1]
    span = f"{first:%a %d %b}" if first == last else f"{first:%a %d %b} to {last:%a %d %b}"
    return f"""<li class="cal-run" data-course="{escape(name)}">
  <div class="cal-date"><b>{first:%d}</b><span>{first:%b}</span></div>
  <div class="cal-body">
    <a class="cal-name" href="{course_href(c['name'])}">{escape(name)}</a>
    <p>{span} · {_when(r['slots'])} · {len(r['days'])} classes · {c['price']}</p>
  </div>
  <a class="btn btn-amber cal-book" href="{_book_href(name, r)}" target="_blank" rel="noopener" data-cta="calendar-book" aria-label="Book {escape(name)} starting {first:%d %B} on WhatsApp">Book on WhatsApp</a>
</li>"""


STYLE = """<style>
.cal-tools{display:flex;gap:1rem;align-items:center;flex-wrap:wrap;margin-bottom:2rem}
.cal-tools select{font:inherit;padding:.6rem .9rem;border:1px solid #e3d3b2;border-radius:10px;background:#fff;min-width:min(100%,320px)}
.cal-month{margin-bottom:2.6rem}
.cal-month h2{font-size:1.5rem;border-bottom:2px solid #e19e13;padding-bottom:.4rem;margin-bottom:1rem}
.cal-list{list-style:none;margin:0;padding:0;display:grid;gap:.75rem}
.cal-run{display:grid;grid-template-columns:auto 1fr auto;gap:1rem;align-items:center;padding:.9rem 1rem;border:1px solid #eee2c8;border-radius:14px;background:#fff}
.cal-run:hover{border-color:#e19e13;box-shadow:0 8px 20px -14px rgba(59,36,20,.45)}
.cal-date{width:3.4rem;text-align:center;line-height:1.1;color:#9a5f08}
.cal-date b{display:block;font-size:1.5rem}
.cal-date span{font-size:.8rem;text-transform:uppercase;letter-spacing:.06em}
.cal-name{font-weight:600;color:#2b1a0c;text-decoration:none}
.cal-name:hover{text-decoration:underline}
.cal-body p{margin:.2rem 0 0;color:var(--ink-soft);font-size:.92rem}
@media (max-width:640px){.cal-run{grid-template-columns:auto 1fr}.cal-book{grid-column:1/-1;text-align:center}}
</style>"""

SCRIPT = """<script>
(function(){
  var sel=document.getElementById('cal-course');
  function apply(){
    var v=sel.value;
    document.querySelectorAll('.cal-run').forEach(function(li){li.hidden=!!v&&li.dataset.course!==v;});
    document.querySelectorAll('.cal-month').forEach(function(m){m.hidden=!m.querySelector('.cal-run:not([hidden])');});
  }
  var q=new URLSearchParams(location.search).get('course');
  if(q&&[].some.call(sel.options,function(o){return o.value===q;})){sel.value=q;}
  sel.addEventListener('change',function(){
    var u=new URL(location.href);
    if(sel.value){u.searchParams.set('course',sel.value);}else{u.searchParams.delete('course');}
    history.replaceState(null,'',u);apply();
  });
  apply();
})();
</script>"""


def render():
    runs = _runs()
    names = sorted({r["course"] for r in runs})
    options = "".join(f'<option value="{escape(n)}">{escape(n)}</option>' for n in names)
    months = {}
    for r in runs:
        months.setdefault(r["days"][0].strftime("%B %Y"), []).append(r)
    body = "".join(
        f'<section class="cal-month" aria-label="{m}"><h2>{m}</h2><ul class="cal-list">{"".join(_row(r) for r in rs)}</ul></section>'
        for m, rs in months.items())
    intro = ("Every batch we run in 2027, month by month. All classes are live on Saturdays and Sundays, "
             "never on a national holiday or a big festival. Pick a date and book it on WhatsApp.")
    return banner("2027 course calendar", "Plan your year", "2027 course calendar.", intro) + STYLE + f"""
<section>
  <div class="wrap">
    <div class="cal-tools">
      <label for="cal-course"><b>Show</b></label>
      <select id="cal-course"><option value="">All courses</option>{options}</select>
    </div>
    {body}
    <p style="color:var(--ink-soft);font-size:.9rem">Class times are confirmed when you book. Dates can move if a batch fills early or for a festival. We will tell you first. Looking for something else? See <a href="courses.html" style="color:var(--blue);text-decoration:underline">all courses</a>.</p>
  </div>
</section>""" + SCRIPT


def course_block(name):
    """A course page's own 2027 batches, or "" when the course has no fixed dates.
    Rows are translate="no" so the language pages need only the heading."""
    runs = [r for r in _runs() if r["course"] == name]
    if not runs:
        return ""
    rows = "".join(_row(r) for r in runs)
    return STYLE + f"""
<section id="dates">
  <div class="wrap">
    <h2>2027 dates.</h2>
    <ul class="cal-list" translate="no">{rows}</ul>
    <p style="margin-top:1rem"><a class="link-arrow" href="{SLUG}" data-cta="course-calendar">2027 course calendar</a></p>
  </div>
</section>"""


def pages():
    """slug -> (title, desc, active, body) for build.PAGES."""
    desc = ("Craft Beer School 2027 course calendar: every weekend batch of every course, month by month, "
            "with dates, fees and a WhatsApp button to book your seat.")
    return {SLUG: ("2027 Course Calendar | Craft Beer School", desc, "courses", render())}
