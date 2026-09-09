# hstarchitects.com

Static marketing site for **HST Architects** — a Dubai interior design, renovation and
landscaping studio, part of HST Group.

Zero build step to deploy: the repository root *is* the site. Vercel serves it as static
files. The Python scripts under `tools/` regenerate that HTML from a single content file
so copy changes stay consistent across all 20 pages.

## Layout

```
index.html            home
about/                about the studio
services/             overview + interior-design/ renovation/ landscaping/
projects/             portfolio index + 12 project case studies
contact/              enquiry form (Supabase-backed)
404.html
assets/css/site.css   design system: brand palette, light + dark themes, glass surfaces
assets/js/site.js     theme, nav, reveal, accordion, filters, form
assets/js/config.js   runtime config (Supabase URL + publishable key)
assets/img/           responsive WebP (480/800/1280/1920) + JPEG fallbacks
sitemap.xml robots.txt llms.txt site.webmanifest vercel.json
supabase/migrations/  database schema
tools/                site generator (see below)
```

## Editing content

All copy, project data, service descriptions and per-page SEO live in
[`tools/content.py`](tools/content.py). Edit there, then:

```bash
python tools/build_site.py
```

That rewrites every HTML page, `sitemap.xml`, `robots.txt` and `llms.txt`.
Do not hand-edit the generated HTML — the next build overwrites it.

To add or replace photography, add the slug to `CURATED` in
[`tools/build_images.py`](tools/build_images.py) and run:

```bash
python tools/build_images.py
```

That writes four WebP widths plus a JPEG fallback and refreshes
`assets/img/manifest.json`, which the generator reads to emit correct `srcset`s.

## Local preview

```bash
python -m http.server 4321
```

Then open <http://localhost:4321>.

## Backend

The contact form posts directly to Supabase PostgREST. The `enquiries` table has row-level
security enabled with a single policy: the anonymous role may `INSERT` and nothing else, so
the publishable key in `assets/js/config.js` cannot be used to read submissions. Schema lives
in [`supabase/migrations/0001_enquiries.sql`](supabase/migrations/0001_enquiries.sql).

Read enquiries from the Supabase dashboard, or with a service-role key from a server.

## SEO / GEO

- Unique title, meta description and canonical on every page
- JSON-LD: `HomeAndConstructionBusiness`, `WebSite`, `Service`, `CreativeWork`,
  `BreadcrumbList`, `FAQPage`, `ContactPage`, `AboutPage`, with `speakable` hints
- `sitemap.xml` generated from the page list, `robots.txt` explicitly allows answer-engine
  crawlers, and `llms.txt` gives them a plain-text map of the site
- Breadcrumbs, related-service blocks and contextual body links on every page
- Long-lived immutable caching for `/assets`, security headers, and legacy-path redirects
  configured in `vercel.json`
