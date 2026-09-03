-- Craft Beer School: course applications store.
-- Run once in the Supabase SQL editor (Dashboard > SQL Editor > New query).
--
-- Security model, and the reason this is safe to call from a public static site:
--   * anon may INSERT an application and nothing else.
--   * anon may NOT SELECT, UPDATE or DELETE, so the anon key shipped in the
--     page cannot be used to read anybody's contact details.
--   * only signed-in users (you) can read and triage.
-- The protection lives here in the database, not in the page.

create table if not exists public.applications (
  id          uuid primary key default gen_random_uuid(),
  created_at  timestamptz not null default now(),

  name        text not null check (char_length(name)  between 1 and 120),
  phone       text not null check (char_length(phone) between 4 and 32),
  email       text not null check (char_length(email) between 3 and 254
                                   and position('@' in email) > 1),
  course      text     check (char_length(course)  <= 120),
  city        text     check (char_length(city)    <= 120),
  promo       text     check (char_length(promo)   <= 60),
  message     text     check (char_length(message) <= 4000),

  -- where the application came from, for attribution
  source_page text     check (char_length(source_page) <= 200),

  -- triage fields, admin only
  status      text not null default 'new'
              check (status in ('new','contacted','enrolled','not_a_fit','spam')),
  notes       text     check (char_length(notes) <= 4000)
);

create index if not exists applications_created_at_idx on public.applications (created_at desc);
create index if not exists applications_status_idx     on public.applications (status);

alter table public.applications enable row level security;

-- Public may submit an application.
drop policy if exists "anon can submit an application" on public.applications;
create policy "anon can submit an application"
  on public.applications for insert
  to anon, authenticated
  with check (
    -- a submission always starts life as new and unannotated; this stops a
    -- crafted request from writing triage fields
    status = 'new' and notes is null
  );

-- Only signed-in users can read applications.
drop policy if exists "authenticated can read applications" on public.applications;
create policy "authenticated can read applications"
  on public.applications for select
  to authenticated
  using (true);

-- Only signed-in users can triage them.
drop policy if exists "authenticated can update applications" on public.applications;
create policy "authenticated can update applications"
  on public.applications for update
  to authenticated
  using (true) with check (true);

drop policy if exists "authenticated can delete applications" on public.applications;
create policy "authenticated can delete applications"
  on public.applications for delete
  to authenticated
  using (true);

-- Deliberately no policy grants anon SELECT/UPDATE/DELETE. With RLS on, the
-- absence of a policy is a denial.
