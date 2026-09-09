-- Website enquiry capture for hstarchitects.com
-- The public site may INSERT only. Reading is restricted to the dashboard /
-- service-role clients, so no visitor can enumerate other people's enquiries.

create extension if not exists "pgcrypto";

create table if not exists public.enquiries (
  id           uuid primary key default gen_random_uuid(),
  created_at   timestamptz not null default now(),
  name         text not null check (char_length(name) between 1 and 120),
  email        text not null check (char_length(email) between 3 and 160),
  phone        text        check (phone is null or char_length(phone) <= 40),
  service      text        check (service is null or char_length(service) <= 80),
  budget       text        check (budget is null or char_length(budget) <= 60),
  message      text not null check (char_length(message) between 10 and 4000),
  source_page  text        check (source_page is null or char_length(source_page) <= 200),
  status       text not null default 'new'
               check (status in ('new','contacted','qualified','won','lost','spam')),
  notes        text
);

comment on table public.enquiries is 'Contact-form submissions from hstarchitects.com';

alter table public.enquiries enable row level security;

drop policy if exists "public site may submit enquiries" on public.enquiries;
create policy "public site may submit enquiries"
  on public.enquiries
  for insert
  to anon
  with check (true);

create index if not exists enquiries_created_at_idx on public.enquiries (created_at desc);
create index if not exists enquiries_status_idx     on public.enquiries (status);
