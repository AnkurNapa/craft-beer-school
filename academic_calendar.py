"""Academic Calendar 2027 page. Dates come from content/academic-calendar-2027.md,
so a change to the planning file is the only edit needed."""
import calendar
import datetime as dt
import html
import pathlib
import re

SLUG = "academic-calendar.html"
SRC = pathlib.Path("content/academic-calendar-2027.md")
YEAR = 2027
TRACKS = {"A": "Brewing", "B": "Spirits, wine and drinks", "C": "Business and brand"}


def _d(s):
    return dt.datetime.strptime(f"{s.strip()} {YEAR}", "%d %b %Y").date()


def load():
    md = SRC.read_text(encoding="utf-8")
    courses, closures = [], {}
    for line in md.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if re.match(r"\| [ABC] \|", line):
            sats = [_d(x) for x in cells[5].split(",")]
            courses.append(dict(track=cells[0], name=cells[1], weeks=int(cells[2]), sats=sats))
        m = re.match(r"\| (\d\d \w+)\S(\d\d \w+) \|", line)
        if m:
            closures[_d(m.group(1))] = cells[1]
    return courses, closures


def _fmt(d):
    return f"{d.day} {d:%b}"


def _month(m, by_sat, closures):
    esc = html.escape
    rows = []
    for d in (dt.date(YEAR, m, 1) + dt.timedelta(i) for i in range(calendar.monthrange(YEAR, m)[1])):
        if d.weekday() != 5:
            continue
        if d in closures:
            rows.append(f'<li class="ac-row ac-closed"><b>{d.day}</b><span>School closed: {esc(closures[d])}</span></li>')
        elif d in by_sat:
            chips = "".join(f'<span class="ac-chip ac-{c["track"].lower()}" title="{esc(TRACKS[c["track"]])}">{esc(c["name"])}</span>' for c in by_sat[d])
            rows.append(f'<li class="ac-row"><b>{d.day}</b><span>{chips}</span></li>')
        else:
            rows.append(f'<li class="ac-row ac-free"><b>{d.day}</b><span>Open for tutorials and replacement classes</span></li>')
    return f'<article class="card ac-month reveal"><h3>{calendar.month_name[m]}</h3><ol>{"".join(rows)}</ol></article>'


def page(banner):
    esc = html.escape
    courses, closures = load()
    by_sat = {}
    for c in courses:
        for s in c["sats"]:
            by_sat.setdefault(s, []).append(c)
    weeks = sum(c["weeks"] for c in courses)
    legend = "".join(f'<span class="ac-chip ac-{k.lower()}">Track {k}: {v}</span>' for k, v in TRACKS.items())
    table = "".join(
        f'<tr data-q="{esc((c["name"] + " " + TRACKS[c["track"]]).lower())}"><td><span class="ac-chip ac-{c["track"].lower()}">{c["track"]}</span></td>'
        f'<td>{esc(c["name"])}</td><td>{c["weeks"]}</td><td>{_fmt(c["sats"][0])}</td>'
        f'<td>{_fmt(c["sats"][-1] + dt.timedelta(1))}</td></tr>' for c in courses)
    months = "".join(_month(m, by_sat, closures) for m in range(1, 13))
    body = banner("Academic calendar", "Academic Calendar 2027", "Every weekend of 2027, planned.",
                  f"All {len(courses)} online courses in one year, taught on Saturdays and Sundays from 12 to 2 pm IST. "
                  "This is a proposed schedule, not an announced intake.") + f"""
<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">How it works</span><h2>Three tracks, one weekend slot.</h2></div>
    <p class="lead">Each class weekend is two days of two hours, so four contact hours. {len(courses)} courses add up to {weeks} teaching weeks. Batches take up to 20 students. Recordings help you catch up. To complete a course, submit every assignment and attend at least 80% of live classes.</p>
    <p class="ac-legend">{legend}<span class="ac-chip ac-closed-chip">School closed</span></p>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Month by month</span><h2>Pick your weekend.</h2></div>
    <div class="grid-3 ac-grid">{months}</div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">All courses</span><h2>First class and last class.</h2></div>
    <div class="ac-scroll"><table class="bd-table ac-table"><thead><tr><th>Track</th><th>Course</th><th>Weeks</th><th>First class</th><th>Last class</th></tr></thead><tbody>{table}</tbody></table></div>
    <p class="ac-note">Duration counts teaching weeks. Festival closures stretch the calendar, so some courses finish a few weeks after they start. Weekday festivals such as Republic Day, Holi and Janmashtami carry no deadlines. Check your state calendar before you enrol, as regional holidays can add a replacement weekend.</p>
  </div>
</section>
<section class="cta"><div class="wrap"><h2>Ready to pick a weekend?</h2><p>Tell us the course and the month. We will confirm the batch and the seats.</p><a href="contact.html#enroll" class="btn btn-amber" data-cta="academic-calendar-enrol">Enrol</a> <a href="courses.html" class="btn btn-ghost" data-cta="academic-calendar-courses">See all courses</a></div></section>
"""
    return ("Academic Calendar 2027 | Craft Beer School",
            f"The 2027 Craft Beer School calendar: all {len(courses)} online courses by weekend, with start dates, end dates and school closures.",
            "courses", body)
