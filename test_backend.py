#!/usr/bin/env python3
"""Backend safety checks. Run: python3 test_backend.py

The failure this exists to prevent is leaking applicant contact details. The
anon key ships inside a public page, so the only thing standing between an
attacker and every applicant's phone number is the RLS policy set. These
assertions read the schema and the built pages and refuse the two mistakes
that actually cause a breach: granting anon a read, or shipping a service_role
key to the browser.

Live checks against a real project run only when SUPABASE_URL and
SUPABASE_ANON_KEY are set in the environment.
"""
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).parent
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


# --- schema ---------------------------------------------------------------
sql = (HERE / "supabase" / "schema.sql").read_text()
low = sql.lower()

check("enable row level security" in low, "schema: RLS is never enabled")

# Find every policy and the roles it is granted to.
policies = re.findall(
    r'create policy\s+"([^"]+)"\s*on\s+[\w.]+\s+for\s+(\w+)\s*to\s+([^\n]+)', low)
check(policies, "schema: no policies found")

for name, action, roles in policies:
    roles_l = [r.strip() for r in roles.replace("(", "").replace(")", "").split(",")]
    if "anon" in roles_l:
        check(action == "insert",
              f"schema: policy '{name}' grants anon '{action}'. "
              "anon must only ever be able to insert.")

reads = [p for p in policies if p[1] in ("select", "all")]
for name, action, roles in reads:
    check("anon" not in roles,
          f"schema: read policy '{name}' includes anon, applicant data would be public")

check("status = 'new'" in low,
      "schema: anon insert policy does not pin status to 'new', "
      "a crafted request could write triage state")

# --- built pages ----------------------------------------------------------
SERVICE_KEY_HINTS = ("service_role", "supabase_service", "SUPABASE_SERVICE")
for p in sorted(HERE.glob("*.html")):
    html = p.read_text()
    for hint in SERVICE_KEY_HINTS:
        check(hint not in html,
              f"{p.name}: looks like it contains a service_role key, which bypasses RLS")

admin = (HERE / "admin.html")
if admin.exists():
    a = admin.read_text()
    check("noindex" in a, "admin.html: missing noindex")
    check("integrity=" in a, "admin.html: CDN script has no subresource integrity")
    check("signInWithPassword" in a, "admin.html: no auth step, page would be open")

robots = (HERE / "robots.txt").read_text()
check("Disallow: /admin.html" in robots, "robots.txt: admin surface not disallowed")

sitemap = (HERE / "sitemap.xml").read_text()
check("admin" not in sitemap, "sitemap.xml: admin surface is listed")

# --- live project (optional) ----------------------------------------------
url, key = os.environ.get("SUPABASE_URL", ""), os.environ.get("SUPABASE_ANON_KEY", "")
if url and key:
    def call(method, path, body=None):
        req = urllib.request.Request(
            f"{url}/rest/v1/{path}", method=method,
            data=body.encode() if body else None,
            headers={"apikey": key, "Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, r.read().decode()[:300]
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode()[:300]

    status, body = call("GET", "applications?select=*&limit=1")
    check(status in (401, 403) or body.strip() in ("[]", ""),
          f"LIVE: anon could read applications (HTTP {status}): {body}")
    print(f"  live anon read -> HTTP {status} (want empty or denied)")

    status, _ = call("PATCH", "applications?id=eq.00000000-0000-0000-0000-000000000000",
                     '{"status":"enrolled"}')
    check(status in (401, 403, 404), f"LIVE: anon update was not denied (HTTP {status})")
    print(f"  live anon update -> HTTP {status} (want denied)")
else:
    print("  (live checks skipped, set SUPABASE_URL and SUPABASE_ANON_KEY to run them)")

if errors:
    for e in errors:
        print("FAIL:", e)
    print(f"\n{len(errors)} backend check(s) failed")
    sys.exit(1)
print("All backend safety checks passed.")
