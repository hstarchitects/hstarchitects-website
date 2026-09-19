-- Campaign attribution for website enquiries.
--
-- The site keeps the first-touch campaign parameters of a browser session
-- (utm_source, utm_medium, utm_campaign, utm_content, utm_term, utm_id, fbclid,
-- gclid, plus the landing path and referring host) and sends them with the
-- enquiry, so the studio can see which advert produced it.
--
-- api/enquiry.js already sends this field. Until this migration runs it notices
-- PostgREST rejecting the unknown column and stores the enquiry without it, so
-- no enquiry is ever lost to a missing column. The campaign also appears in the
-- notification email either way.

alter table public.enquiries
  add column if not exists attribution jsonb
    check (attribution is null or pg_column_size(attribution) <= 4096);

comment on column public.enquiries.attribution is
  'First-touch campaign parameters for the session: utm_*, fbclid, gclid, landing path, referrer host';

-- Querying by campaign is the point of the column.
create index if not exists enquiries_attr_source_idx
  on public.enquiries ((attribution ->> 'utm_source'));
create index if not exists enquiries_attr_campaign_idx
  on public.enquiries ((attribution ->> 'utm_campaign'));

-- The existing anon INSERT policy (0001) covers the new column; anon still
-- cannot read any row.
