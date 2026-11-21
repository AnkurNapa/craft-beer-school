// Course helper: a chat bubble that answers course facts (fee, dates, timings,
// length, certificate, what is included, topics, format) from assets/helper.json,
// which build.py writes from the same course data as the pages. Anything it cannot
// answer goes to Chatty through the WhatsApp details form. No AI, no third party.
(() => {
  const TOPICS = [
    ['batch', /batch size|students|seats|how many (people|students)|class size/, ['Batch']],
    ['fee', /\b(fees?|price|cost|how much|charges?|pay|rupees?|rs|discounts?|emi)\b|₹/, ['Fee']],
    ['dates', /date|when|start|next batch|batch|month|january|february|march|calendar|2027/, 'DATES'],
    ['time', /\b(time|timings?|hours?|weekends?|saturdays?|sundays?|mornings?|evenings?|ist)\b/, ['Schedule', 'Sessions']],
    ['length', /\b(long|duration|weeks?|days?|sessions?|classes)\b/, ['Duration', 'Sessions']],
    ['cert', /certif/, ['Certificate']],
    ['incl', /includ|record|kit|deck|material|notes|what do i get/, ['Included']],
    ['topics', /learn|topic|syllabus|cover|module|content|teach|curriculum/, ['Topics', 'Syllabus', 'Details']],
    ['format', /\b(online|in person|offline|where|city|cities|location|venue|format|mode)\b/, ['Format', 'Cities', 'City', 'Where']],
    ['enrol', /enrol|enroll|join|register|sign ?up|book|admission|apply/, ['Enrol online']],
  ];
  const CHIPS = [['fee', 'Fee'], ['dates', 'Next batch'], ['time', 'Timings'], ['incl', "What's included"], ['cert', 'Certificate'], ['topics', 'Topics']];
  const STOP = new Set(['the', 'and', 'for', 'course', 'courses', 'what', 'is', 'are', 'how', 'much', 'does', 'about', 'with', 'your', 'can', 'you', 'tell']);
  let data, cur = null, pending = null, root, log, input;

  const el = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  const track = (topic, course) => { if (window.gtag) gtag('event', 'helper_question', { topic, course: course || '' }); };
  const load = async () => {
    if (!data) { try { data = await (await fetch('/assets/helper.json')).json(); } catch (e) { data = { courses: [] }; } }
    return data;
  };

  function css() {
    const s = el('style');
    s.textContent = '.ch-btn{position:fixed;right:1rem;bottom:1rem;z-index:1000;display:flex;align-items:center;gap:.45rem;border:0;border-radius:999px;padding:.75rem 1.05rem;background:var(--ink,#1d1d1f);color:#fff;font:600 .92rem var(--sans,sans-serif);box-shadow:0 8px 24px rgba(0,0,0,.22);cursor:pointer}' +
      '.ch-btn svg{width:18px;height:18px}.ch-panel{position:fixed;right:1rem;bottom:4.6rem;z-index:1001;width:min(22rem,calc(100vw - 2rem));max-height:min(34rem,calc(100vh - 7rem));display:flex;flex-direction:column;background:#fff;border-radius:18px;box-shadow:0 18px 50px rgba(0,0,0,.25);overflow:hidden;font:.92rem/1.45 var(--sans,sans-serif);color:var(--ink,#1d1d1f)}' +
      '.ch-head{display:flex;justify-content:space-between;align-items:center;padding:.8rem 1rem;background:var(--sand,#fbf6ec);border-bottom:1px solid var(--line,#e8e8ed)}.ch-head strong{font-size:.98rem}.ch-head button{border:0;background:none;font-size:1.3rem;line-height:1;cursor:pointer;color:inherit}' +
      '.ch-log{flex:1;overflow-y:auto;padding:.9rem 1rem;display:flex;flex-direction:column;gap:.55rem}.ch-msg{max-width:88%;padding:.55rem .75rem;border-radius:14px;background:var(--cloud,#f5f5f7);white-space:pre-line}.ch-me{align-self:flex-end;background:var(--amber,#e19e13);color:#1d1d1f}' +
      '.ch-msg a{color:var(--amber-deep,#9a5f08);font-weight:600;word-break:break-word}.ch-chips{display:flex;flex-wrap:wrap;gap:.4rem}.ch-chips button{border:1px solid var(--line,#e8e8ed);background:#fff;border-radius:999px;padding:.35rem .7rem;font:inherit;font-size:.82rem;cursor:pointer}' +
      '.ch-chips button.ch-wa{background:#1f7a4d;color:#fff;border-color:#1f7a4d}.ch-msg select{margin-top:.4rem;width:100%;padding:.45rem;border-radius:10px;border:1px solid var(--line,#e8e8ed);font:inherit}' +
      '.ch-form{display:flex;gap:.4rem;padding:.6rem;border-top:1px solid var(--line,#e8e8ed)}.ch-form input{flex:1;min-width:0;padding:.55rem .7rem;border:1px solid var(--line,#e8e8ed);border-radius:999px;font:inherit}.ch-form button{border:0;border-radius:999px;padding:0 .9rem;background:var(--ink,#1d1d1f);color:#fff;font:inherit;font-weight:600;cursor:pointer}' +
      '@media(max-width:680px){.ch-btn{bottom:5.2rem}.ch-panel{bottom:8.8rem;max-height:calc(100vh - 10rem)}body:has(#enroll) .ch-btn{bottom:1rem}body:has(#enroll) .ch-panel{bottom:4.6rem}.ch-btn span{display:none}}@media print{.ch-btn,.ch-panel{display:none}}';
    document.head.appendChild(s);
  }

  function say(text, who) {
    const m = el('div', 'ch-msg' + (who === 'me' ? ' ch-me' : ''));
    if (typeof text === 'string') m.textContent = text; else m.append(...text);
    log.appendChild(m); log.scrollTop = log.scrollHeight; return m;
  }
  function link(href, label) { const a = el('a', null, label || href); a.href = href; if (/^https?:/.test(href) && !href.includes(location.host)) { a.target = '_blank'; a.rel = 'noopener'; } return a; }
  function chips(list) {
    const box = el('div', 'ch-chips');
    list.forEach(([label, fn, cls]) => { const b = el('button', cls || null, label); b.type = 'button'; b.onclick = fn; box.appendChild(b); });
    log.appendChild(box); log.scrollTop = log.scrollHeight;
  }
  function chatty(course) {
    // Clicking a WhatsApp enquiry link opens the site's details form first.
    const a = el('a'); a.href = course ? course.wa : data.wa; a.target = '_blank'; a.rel = 'noopener'; a.hidden = true;
    document.body.appendChild(a); a.click(); a.remove(); track('whatsapp', course && course.n);
  }
  function rowsFor(course, keys) {
    return course.rows.filter(([k]) => keys.includes(k));
  }
  function render(course, rows) {
    const parts = [el('strong', null, course.n)];
    rows.forEach(([k, v]) => { parts.push(document.createTextNode('\n' + k + ': ')); parts.push(/^https?:/.test(v) ? link(v) : document.createTextNode(v)); });
    return parts;
  }
  function dates(course) {
    const today = new Date().toISOString().slice(0, 10);
    const next = course.runs.filter(r => r.d[r.d.length - 1] >= today).slice(0, 3);
    if (!next.length) return [el('strong', null, course.n), document.createTextNode('\nNo fixed dates are listed yet. Chatty confirms the next batch on WhatsApp. '), link(data.calendar, 'See the 2027 calendar')];
    const fmt = d => new Date(d + 'T00:00:00').toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
    const parts = [el('strong', null, course.n + ': next batches')];
    next.forEach(r => parts.push(document.createTextNode('\n' + fmt(r.d[0]) + ' to ' + fmt(r.d[r.d.length - 1]) + ', ' + r.w + ' (' + r.d.length + ' classes)')));
    parts.push(document.createTextNode('\n'), link(data.calendar, 'Full 2027 calendar'));
    return parts;
  }
  function answer(course, topic) {
    cur = course; pending = null; track(topic ? topic[0] : 'summary', course.n);
    if (!topic) say(render(course, rowsFor(course, ['Fee', 'Duration', 'Sessions', 'Format', 'Schedule', 'Cities', 'City'])));
    else if (topic[2] === 'DATES') say(dates(course));
    else {
      const rows = rowsFor(course, topic[2]);
      say(rows.length ? render(course, rows) : [el('strong', null, course.n), document.createTextNode('\nI do not have that detail for this course. Chatty can tell you on WhatsApp.')]);
    }
    chips(CHIPS.filter(([k]) => !topic || k !== topic[0]).map(([k, label]) => [label, () => { say(label, 'me'); ask(label, k); }])
      .concat([['Ask Chatty on WhatsApp', () => chatty(course), 'ch-wa']]));
  }
  function findCourse(q) {
    const words = q.split(/[^a-z0-9]+/).filter(w => w.length > 2 && !STOP.has(w));
    let best = null, score = 0;
    data.courses.forEach(c => {
      const name = c.n.toLowerCase(); let s = q.includes(name) ? 10 : 0;
      words.forEach(w => { if (name.split(/[^a-z0-9]+/).includes(w)) s += 2; else if (name.includes(w)) s += 1; });
      if (s > score) { score = s; best = c; }
    });
    return score >= 2 ? best : null;
  }
  function picker(topic) {
    // Pick an area first (Brewing, Business and brand...), then a course in it, each shown with its fee.
    pending = topic;
    say('What are you interested in?');
    chips(data.groups.map(([g, label]) => [label, () => { say(label, 'me'); courses(g); }])
      .concat([['Not sure, show all', () => { say('Show all', 'me'); courses(null); }]]));
  }
  function courses(g) {
    const list = data.courses.filter(c => !g || c.g === g);
    say(g ? 'Here are the courses. Tap one for the fee, dates and details.' : 'All our courses. Tap one for the details.');
    chips(list.map(c => [c.n + ' · ' + c.rows[0][1].split(', paid')[0], () => { say(c.n, 'me'); answer(c, pending); }]));
  }
  function ask(q, key) {
    if (!key) say(q, 'me');
    const t = q.toLowerCase();
    const topic = key ? TOPICS.find(x => x[0] === key) : TOPICS.find(x => x[1].test(t));
    const course = key ? cur : findCourse(t);
    if (/free/.test(t) && !course) {
      const free = data.courses.filter(c => c.rows[0][1] === 'Free');
      say(free.length ? 'Free courses: ' + free.map(c => c.n).join(', ') + '.' : 'There are no free courses right now.');
      return;
    }
    if (/all courses|which courses|list|what courses/.test(t) && !course) {
      say([document.createTextNode('Every course with its fee is here: '), link(data.all, 'All courses and fees')]); picker(null); return;
    }
    if (course) return answer(course, topic);
    if (topic && cur) return answer(cur, topic);
    if (topic) return picker(topic);
    say('I answer course facts: fees, next batch dates, timings, length, what is included, the certificate and topics. Try "fee for Craft Distilling" or "when does Winemaking start". For anything else, Chatty replies on WhatsApp.');
    chips([['Ask Chatty on WhatsApp', () => chatty(cur), 'ch-wa']]);
  }

  async function open() {
    if (root) { root.hidden = !root.hidden; if (!root.hidden) input.focus(); return; }
    await load();
    root = el('div', 'ch-panel'); root.setAttribute('role', 'dialog'); root.setAttribute('aria-label', 'Course helper');
    const head = el('div', 'ch-head'); head.append(el('strong', null, 'Course helper'));
    const x = el('button', null, '×'); x.type = 'button'; x.setAttribute('aria-label', 'Close'); x.onclick = () => { root.hidden = true; };
    head.append(x);
    log = el('div', 'ch-log'); log.setAttribute('aria-live', 'polite');
    const form = el('form', 'ch-form'); input = el('input'); input.placeholder = 'Ask about fees, dates, timings…'; input.setAttribute('aria-label', 'Your question');
    const send = el('button', null, 'Ask'); send.type = 'submit'; form.append(input, send);
    form.onsubmit = e => { e.preventDefault(); const q = input.value.trim(); if (q) { input.value = ''; ask(q); } };
    root.append(head, log, form); document.body.appendChild(root);
    root.addEventListener('keydown', e => { if (e.key === 'Escape') root.hidden = true; });
    const here = data.courses.find(c => c.s && location.pathname.endsWith('/' + c.s));
    say('Hi, I can answer questions about our courses straight away: fees, next batch dates, timings, what is included and more.');
    if (here) { cur = here; chips(CHIPS.map(([k, label]) => [label, () => { say(label + ' for ' + here.n, 'me'); ask(label, k); }])); }
    else picker(null);
    input.focus();
  }

  css();
  const btn = el('button', 'ch-btn'); btn.type = 'button'; btn.setAttribute('aria-label', 'Ask about our courses');
  btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg><span>Ask about courses</span>';
  btn.onclick = open; document.body.appendChild(btn);
})();
