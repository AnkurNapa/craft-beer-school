"""The WhatsApp message a student sends when they ask about a course.

It names the course with its fee and duration, so nobody has to ask the price in
the chat, then lists the details Chatty needs to reply (Chatty's request, 21 Nov 2026).
"""
import html

FIELDS = ("Name", "Mobile No.", "Email Id", "Location", "Course preference/s",
          "Background (educational or professional)")
ALL_FEES = "https://craftbeerschool.in/courses.html"
GREETING = "Hi Craft Beer School, I'd like to enquire about a course."


def plain(name):
    return html.unescape(name).strip()


def fees():
    """Course name -> 'fee, duration, format' for every online and in-person course."""
    import inperson_pages
    import pages_a
    mode = lambda n: pages_a.MODE_LABEL[pages_a.MODE.get(n, "Online")].lower()
    online = {plain(c["name"]): f'{"Free" if c["amount"] == "0" else c["price"]}, {c["dur"].lower()}, {mode(c["name"])}'
              for c in pages_a.COURSE_DATA}
    in_person = {}
    for c in inperson_pages.COURSES:
        facts = dict(c["facts"])
        in_person[plain(c["name"])] = f'{facts.get("Fee", "On enquiry")}, {facts.get("Duration", "").lower()}, in person'
    return {**online, **in_person}


def text(course=None, url=None, intro=None):
    """Prefilled WhatsApp text: greeting, course and fee, then the blank details form."""
    course = plain(course) if course else ""
    fee = fees().get(course) if course else None
    lines = [intro or (f"Hi Craft Beer School, I'd like to enquire about the {course} course." if course else GREETING)]
    lines.append(f"Fee: {fee}" if fee else f"Course fees: {ALL_FEES}")
    lines.append("")
    lines += [f"{f}: {course}" if f == "Course preference/s" else f"{f}:" for f in FIELDS]
    if url:
        lines += ["", f"Page: {url}"]
    return "\n".join(lines)


if __name__ == "__main__":
    t = text("Brewing Fundamentals", "https://craftbeerschool.in/x.html")
    assert "Fee: ₹5,999, 2 weeks, online" in t, t
    assert "Course preference/s: Brewing Fundamentals" in t and "Mobile No.:" in t
    assert "Fee: Free" in text("Safety in Brewing")
    assert "Fee: ₹25,000, 1 day, in person" in text("1-Day Super Intensive Craft Beer Course")
    assert ALL_FEES in text() and "Course preference/s: \n" in text() + "\n"
    print(t)
