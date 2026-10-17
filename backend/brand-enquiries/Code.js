// Brand consultancy enquiries from craftbeerschool.in/brand-consultancy.html.
// Each enquiry is emailed straight to Chatty, with Reply-To set to the enquirer.
const TO = 'chatty@cheerschattyventures.com';
const FIELDS = [['name', 'Name'], ['company', 'Brewery or brand'], ['city', 'City'], ['phone', 'Phone'],
  ['email', 'Email'], ['course', 'Looking for'], ['message', 'Message'], ['came_from', 'Came from']];
const MAX_PER_HOUR = 40; // ponytail: one script-wide cap stops a flood, per-IP limits need a real backend

function clean_(v, max) {
  return String(v || '').replace(/[\u0000-\u0008\u000b-\u001f]/g, '').trim().slice(0, max || 300);
}

function reply_(ok, error) {
  return ContentService.createTextOutput(JSON.stringify({ ok: ok, error: error || null }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p._gotcha) return reply_(true); // honeypot: bots fill hidden fields
  const f = {};
  FIELDS.forEach(([k]) => { f[k] = clean_(p[k], k === 'message' ? 3000 : 300); });
  if (!f.name || (!f.email && !f.phone)) return reply_(false, 'name and a phone or email are required');
  if (f.email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.email)) return reply_(false, 'email looks wrong');

  const cache = CacheService.getScriptCache();
  const sent = Number(cache.get('sent') || 0);
  if (sent >= MAX_PER_HOUR) return reply_(false, 'busy, please use WhatsApp');
  cache.put('sent', String(sent + 1), 3600);

  const body = FIELDS.filter(([k]) => f[k]).map(([k, label]) => label + ': ' + f[k]).join('\n');
  const mail = {
    to: TO,
    subject: 'Brand consultancy enquiry: ' + f.name + (f.company ? ', ' + f.company : ''),
    body: 'A new brand consultancy enquiry from Craft Beer School.\n\n' + body +
      '\n\nReply to this email to answer ' + f.name + ' directly.',
    name: 'Craft Beer School',
  };
  if (f.email) mail.replyTo = f.email;
  MailApp.sendEmail(mail);
  return reply_(true);
}

function doGet() {
  return reply_(true);
}
