"""The WhatsApp message a student sends when they ask about a course.

It carries the course facts students otherwise ring to ask about (fee, length,
timings, batch size, what is included, topics, links), then the details Chatty
needs to reply. The site's enquiry form fills those details in before WhatsApp
opens (Chatty's request, 21 Nov 2026: fewer long calls).

No dates go in the text: a date would change by itself when a batch starts and
take the translated pages offline, so the message links to the 2027 calendar.
"""
import html

SITE = "https://craftbeerschool.in"
FIELDS = ("Name", "Mobile No.", "Email Id", "Location", "Course preference/s",
          "Background (educational or professional)")
ALL_FEES = f"{SITE}/courses.html"
CALENDAR = f"{SITE}/course-calendar-2027.html"
GREETING = "Hi Craft Beer School, I'd like to enquire about a course."


def plain(name):
    return html.unescape(name).strip()


def _online():
    """Course name -> list of (label, value) for every online course."""
    import calendar_page
    import course_pages
    import pages_a
    dated = {r["course"] for r in calendar_page._runs()}
    out = {}
    for c in pages_a.COURSE_DATA:
        name, f = plain(c["name"]), course_pages.fmt(c)
        facts = dict(f["logistics"])
        rows = [("Fee", "Free" if c["amount"] == "0" else f"{c['price']}, paid in full at sign-up"),
                ("Duration", c["dur"].lower()),
                ("Sessions", f["sessions"]),
                ("Format", pages_a.MODE_LABEL[pages_a.MODE.get(c["name"], "Online")]),
                ("Schedule", ", ".join(f["when"])),
                ("Batch", f["batch"]),
                ("Included", facts["Included"]),
                ("Certificate", facts["Certificate"]),
                ("Topics", "; ".join(plain(i) for i in c["items"])),
                ("Syllabus", f"{SITE}/{pages_a.course_href(c['name'])}")]
        if name in dated:
            rows.append(("2027 dates", CALENDAR))
        rows.append(("Enrol online", f"{SITE}/{pages_a.enroll_href(name)}"))
        out[name] = rows
    return out


def _in_person():
    import inperson_pages
    import pages_a
    out = {}
    for c in inperson_pages.COURSES:
        facts = dict(c["facts"])
        rows = [("Fee", facts.get("Fee", "On enquiry"))]
        rows += [(k, v) for k, v in c["facts"] if k != "Fee"]
        if c.get("included"):
            rows.append(("Included", c["included"]))
        rows += [("Details", f"{SITE}/{c['slug']}"), ("Enrol online", f"{SITE}/{pages_a.enroll_href(plain(c['name']))}")]
        out[plain(c["name"])] = rows
    return out


_CACHE = {}


def details(course):
    """(label, value) rows for a course, or None when the site does not know it."""
    if not _CACHE:
        _CACHE.update(_online())
        _CACHE.update(_in_person())
    return _CACHE.get(plain(course))


def fees():
    """Course name -> fee line, for the enrol form's live fee display."""
    details("")
    return {name: rows[0][1] for name, rows in _CACHE.items()}


def text(course=None, url=None, intro=None):
    """Prefilled WhatsApp text: greeting, course details, then the details form."""
    course = plain(course) if course else ""
    rows = details(course) if course else None
    lines = [intro or (f"Hi Craft Beer School, I'd like to enquire about the {course} course." if course else GREETING), ""]
    if rows:
        lines += ["*Course details*"] + [f"{k}: {v}" for k, v in rows]
    else:
        lines += [f"Courses and fees: {ALL_FEES}", f"2027 dates: {CALENDAR}"]
    lines += ["", "*My details*"]
    lines += [f"{f}: {course}" if f == "Course preference/s" else f"{f}:" for f in FIELDS]
    if url:
        lines += ["", f"Page: {url}"]
    return "\n".join(lines)


if __name__ == "__main__":
    t = text("Brewing Fundamentals", f"{SITE}/x.html")
    assert "Fee: ₹5,999, paid in full at sign-up" in t, t
    assert "Course preference/s: Brewing Fundamentals" in t and "Mobile No.:" in t
    assert "Syllabus: https://craftbeerschool.in/brewing-fundamentals-course.html" in t
    assert "Fee: Free" in text("Safety in Brewing")
    assert "Fee: ₹25,000" in text("1-Day Super Intensive Craft Beer Course")
    assert ALL_FEES in text() and fees()["Brewing Fundamentals"].startswith("₹5,999")
    print(t)
