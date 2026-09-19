-- Phone-first enquiries from the ads landing page (/consultation/).
--
-- The landing form asks for a name and a mobile or WhatsApp number, and makes
-- email optional, because a phone number is how the studio actually follows up
-- to arrange the site visit. The table required an email, so a phone-only lead
-- could be emailed to the studio but not stored.
--
-- Until this runs, api/enquiry.js still delivers a phone-only lead by email and
-- answers the visitor with success; it just cannot store it. After it runs, the
-- lead is stored as well.

alter table public.enquiries alter column email drop not null;

-- There must still be one way back to the person.
alter table public.enquiries drop constraint if exists enquiries_email_or_phone;
alter table public.enquiries
  add constraint enquiries_email_or_phone check (email is not null or phone is not null);

-- Tell PostgREST the table changed, so the API accepts the new shape at once.
notify pgrst, 'reload schema';
