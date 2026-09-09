# Deployment

## What is wired up

| Piece | Where | Account |
|---|---|---|
| Repository | [hstarchitects/hstarchitects-website](https://github.com/hstarchitects/hstarchitects-website) | `hstarchitects` |
| Hosting | Vercel project `hstarchitects-website` | `hstarchitects` (Hobby) |
| Live URL | https://hstarchitects-website.vercel.app | |
| Database | Supabase project `mhfempltoebztrvybidb` | org `hstarchitects` |
| Domain | hstarchitects.com | GoDaddy |

Every push to `main` triggers a Vercel deployment. There is no build step: the
repository root is the site.

This project is deliberately isolated. It shares no account, org or team with any
other project — its own GitHub user, its own Vercel team, its own Supabase org.

## Remaining step: point the domain at Vercel

`hstarchitects.com` is added to the Vercel project but still resolves to a
Shopify store that returns "Store unavailable". Two records in GoDaddy need to
change. **Leave every other record alone** — the domain carries live Zoho email.

In GoDaddy → Domain Portfolio → hstarchitects.com → DNS:

| Action | Type | Name | Current value | New value |
|---|---|---|---|---|
| Edit | `A` | `@` | `23.227.38.32` | `216.198.79.1` |
| Edit | `CNAME` | `www` | `shops.myshopify.com.` | `cname.vercel-dns.com.` |

Do **not** touch these — they are the mail configuration:

- `MX @ mx.zoho.com` (10), `mx2.zoho.com` (20), `mx3.zoho.com` (50)
- `TXT @ v=spf1 include:dc-8e814c8572._spfm.hstarchitects.com ~all`
- `TXT dc-8e814c8572._spfm …` and both `zoho-verification` TXT records
- `CNAME zb43369083 → zmverify.zoho.com.`
- the two `NS` records and `CNAME _domainconnect`

The Shopify verification CNAME (`6c19a6ca-… → dns-verification.shopify.com.`)
becomes redundant and can be deleted, but leaving it does no harm.

After saving, Vercel picks the change up within minutes to an hour and issues
the TLS certificate automatically. Check with:

```bash
nslookup hstarchitects.com 8.8.8.8
```

When it returns `216.198.79.1`, open https://hstarchitects.com.

### Then add www in Vercel

Vercel project → Settings → Domains → Add `www.hstarchitects.com`, and set it to
redirect to `hstarchitects.com` so the apex stays canonical. The canonical tags
and the sitemap already point at the apex.

## Verifying a deployment

```bash
B=https://hstarchitects-website.vercel.app
curl -s -o /dev/null -w '%{http_code}\n' $B/
curl -s $B/sitemap.xml | grep -c '<loc>'
curl -s -o /dev/null -w '%{http_code}\n' $B/tools/content.py    # must be 404
```

Build tooling, the Supabase migration and the client PDFs are excluded from the
deployment by `.vercelignore`, so none of them are reachable as public URLs.

## The contact form

`assets/js/config.js` holds the Supabase project URL and its publishable key.
That key is designed to be public: the `enquiries` table has row-level security
enabled and grants the anonymous role `INSERT` only, so it cannot be used to read
submissions. Verified:

```
INSERT as anon              201
SELECT as anon              []          (row-level security blocks it)
INSERT with a short message 400         (check constraint)
```

Read enquiries in the Supabase dashboard under Table Editor → `enquiries`, or
from a server using the secret key. One test row from setup is in the table and
can be deleted.

## Design direction

Two directions were prototyped. **Prototype A was chosen** and is what the site
now is: rounded cards, a floating pill nav, geometric sans display type and glass
surfaces, following the Dribbble reference.

Prototype B ("Atelier": dark-first, vertical nav rail, Cormorant Garamond display
type, hairline rules) has been removed. It is recoverable from git history at
commit `e72f021` if it is ever wanted again:

```bash
git checkout e72f021 -- prototype-b tools/build_site_b.py tools/layout_b.py assets/css/site-b.css
```
