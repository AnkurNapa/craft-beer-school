# Course applications backend

Free forever on Supabase's free tier. Postgres, auth and an admin page, no card.

What you get: every course application lands in a real database, and
`https://craftbeerschool.in/admin.html` lets you sign in, read them, triage
them and export CSV.

## Why this is safe to run from a public static site

The site is static, so the Supabase **anon key ships inside the page**. That is
by design: it is a publishable key, not a secret. What keeps applicant details
private is Row Level Security in `schema.sql`:

| Who | Can insert | Can read | Can update |
|-----|-----------|----------|-----------|
| Public visitor (`anon`) | yes | **no** | no |
| You, signed in (`authenticated`) | yes | yes | yes |

With RLS enabled, no policy means denial. Anyone can lift the anon key out of
the page and submit an application; nobody can use it to read one.

**Never put the `service_role` key anywhere near this repo.** It bypasses RLS
entirely. `test_backend.py` fails the build if it ever appears in a page.

## Setup, about ten minutes

### 1. Create the project

1. Sign up at [supabase.com](https://supabase.com) and create a project.
2. Pick the region closest to your learners (Mumbai, `ap-south-1`).
3. Save the database password somewhere safe. You will rarely need it.

### 2. Create the table

Dashboard, **SQL Editor**, **New query**. Paste all of `schema.sql`, then Run.
It is safe to re-run; it uses `if not exists` and re-creates policies cleanly.

### 3. Create your admin login

Dashboard, **Authentication**, **Users**, **Add user**, **Create new user**.
Use your email and a strong password, and tick **Auto Confirm User**. This is
the login for `admin.html`.

Then under **Authentication**, **Providers**, turn **Email** signups **off**
(`Allow new users to sign up`). Otherwise anyone could register themselves an
account and, being `authenticated`, read your applications. This step matters.

### 4. Get the keys

Dashboard, **Project Settings**, **API**:

- **Project URL**, e.g. `https://abcdefgh.supabase.co`
- **anon / public** key, the long `eyJ...` string. Not `service_role`.

### 5. Build the site with them

```bash
export SUPABASE_URL="https://abcdefgh.supabase.co"
export SUPABASE_ANON_KEY="eyJhbGciOi..."
python3 build.py
python3 test_backend.py     # runs live checks too when these are set
git add -A && git commit -m "chore: wire applications backend" && git push
```

Anyone rebuilding without those variables gets a site that falls back to
Formspree, then to a prefilled email, so a rebuild never silently drops
applications on the floor.

### 6. Stop the project going to sleep

Supabase pauses free projects after about a week with no API traffic. A paused
project would make the form fall back to email without you noticing.
`.github/workflows/keep-supabase-awake.yml` pings it once a day and costs
nothing on a public repo. Add two repository secrets so it can run:

GitHub repo, **Settings**, **Secrets and variables**, **Actions**, **New
repository secret**:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`

Then **Actions**, **Keep Supabase awake**, **Run workflow** once to confirm it
returns a 2xx or 4xx.

## Using it

Go to `https://craftbeerschool.in/admin.html` and sign in.

- **Search** across name, email, phone and city.
- **Filter** by status or course.
- **Status** and **Notes** save the moment you change them, no save button.
- **Export CSV** exports whatever is currently filtered, and quotes any value
  starting with `=`, `+`, `-` or `@` so Excel treats it as text rather than a
  formula.
- The phone number links straight to WhatsApp.

## Reporting later

It is plain Postgres, so Power BI, Tableau and `psql` all connect directly with
the connection string under Project Settings, Database. Use a read-only role
for BI rather than the owner credentials.

## If something looks wrong

| Symptom | Cause |
|---|---|
| Form says "Opening your email app" | `SUPABASE_URL`/`SUPABASE_ANON_KEY` were not set at build time, or the project is paused |
| Admin page says "Not configured yet" | Same, rebuild with the variables set |
| Sign in fails | User does not exist, or was created without Auto Confirm |
| Admin loads but shows nothing | Signed in, but `schema.sql` was never run |
| `test_backend.py` fails on anon read | An RLS policy is granting `anon` too much. Fix before deploying |
