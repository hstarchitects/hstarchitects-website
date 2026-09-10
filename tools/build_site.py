# -*- coding: utf-8 -*-
"""Generate every page of hstarchitects.com from tools/content.py."""
import os, sys, json, shutil, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import (SITE, NAV, SERVICES, PROJECTS, PROCESS, SECTORS,
                     VISUALS, WHY_US, HOME_FAQS, PAGES_SEO)
import layout as L
from layout import (esc, img, img_url, og_url, icon, plan_deco, btn, link_arrow, arrow_badge, head, header,
                    drawer, footer, tail, breadcrumbs, breadcrumb_ld, faq_block, faq_ld,
                    cta_band, related_block, org_ld, website_ld, ROOT)

TODAY = datetime.date.today().isoformat()
URLS = []   # (loc, priority, changefreq)


def write(path, html_str, url=None, prio="0.6", freq="monthly"):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html_str)
    if url is not None:
        URLS.append((url, prio, freq))


def svc(key):
    return next(s for s in SERVICES if s["key"] == key)


# ===========================================================================
# HOME
# ===========================================================================
def build_home():
    seo = PAGES_SEO["home"]

    # every figure below is counted from the portfolio itself, never asserted
    facts = [
        (str(len(PROJECTS)), "Projects in this portfolio"),
        ("3", "Disciplines in-house"),
        (str(len({p["cat"] for p in PROJECTS})), "Sectors delivered"),
        ("2", "Emirates covered"),
    ]
    stats = "".join(
        f'<div class="hero-stats__item"><div class="hero-stats__v">{esc(v)}</div>'
        f'<div class="hero-stats__l">{esc(l)}</div></div>' for v, l in facts)

    svc_cards = ""
    for s in SERVICES:
        caps = "".join(f'<li>{esc(c["t"])}</li>' for c in s["capabilities"][:4])
        svc_cards += f'''<article class="svc reveal" data-d="{s["num"][-1]}">
  <div class="svc__media">{img(s["card_img"], s["card_alt"], sizes="(max-width:620px) 92vw, (max-width:900px) 46vw, 30vw")}
    <span class="svc__num">{esc(s["num"])}</span></div>
  <div class="svc__body">
    <h3 class="h3"><a href="{s["url"]}">{esc(s["title"])}</a></h3>
    <p class="small muted">{esc(s["short"])}</p>
    <ul class="svc__list">{caps}</ul>
    {link_arrow("Explore " + s["title"].split(" &")[0].lower(), s["url"])}
  </div>
</article>'''

    feat = [p for p in PROJECTS if p["slug"] in
            ("springfield-properties-office", "emirates-hills-villa", "damac-hills-landscape",
             "mehr-o-mah-art-cafe", "district-one-roof-garden", "al-wasl-gym")]
    rail = "".join(f'''<a class="tile" href="/projects/{p["slug"]}/">
  {img(p["img"], p["alt"], sizes="(max-width:620px) 82vw, 32vw")}
  <div class="tile__label"><div><h3>{esc(p["title"])}</h3><p>{esc(p["cat"])} &middot; {esc(p["loc"])}</p></div>
  {arrow_badge()}</div></a>''' for p in feat)

    steps = "".join(f'''<div class="step reveal"><div class="step__n">{esc(s["n"])}</div>
  <h3 class="step__t">{esc(s["t"])}</h3><p class="step__d">{esc(s["d"])}</p></div>''' for s in PROCESS)

    why = "".join(f'''<div class="glass reveal" data-d="{i+1}" style="padding:1.6rem">
  <span class="arrow-badge" style="background:var(--accent-soft);color:var(--accent);width:38px;height:38px">{icon("check")}</span>
  <h3 class="h4" style="margin:1.05rem 0 .5rem">{esc(w["t"])}</h3>
  <p class="small muted">{esc(w["d"])}</p></div>''' for i, w in enumerate(WHY_US))

    sectors = "".join(f'''<a class="tile tile--wide reveal" data-d="{(i%4)+1}" href="/projects/">
  {img(x["img"], x["t"] + " project by HST Architects in the UAE", sizes="(max-width:620px) 92vw, (max-width:900px) 46vw, 31vw")}
  <div class="tile__label"><div><h3>{esc(x["t"])}</h3><p>{esc(x["d"])}</p></div>{arrow_badge()}</div></a>'''
  for i, x in enumerate(SECTORS))

    disciplines = ["Interior Design", "Fit-Out", "Landscaping", "Joinery", "MEP Services",
                   "3D Visualisation", "Space Planning", "Pools & Water Features",
                   "Lighting Design", "Maintenance"]
    marquee = "".join(f'<span class="marquee__item">{icon("compass")}{esc(d)}</span>' for d in disciplines * 2)

    ld = [org_ld(), website_ld(), faq_ld(HOME_FAQS),
          {"@context": "https://schema.org", "@type": "WebPage",
           "@id": SITE["domain"] + "/#webpage", "url": SITE["domain"] + "/",
           "name": seo["title"], "description": seo["meta"],
           "isPartOf": {"@id": SITE["domain"] + "/#website"},
           "about": {"@id": SITE["domain"] + "/#organization"},
           "primaryImageOfPage": {"@type": "ImageObject", "url": og_url("hero/hero-pool-dusk")},
           "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".hero h1", ".hero__sub"]}}]

    html_out = head(title=seo["title"], meta=seo["meta"], url="/", jsonld=ld,
                    image=og_url("hero/hero-pool-dusk")) + header("home") + drawer("home") + f'''
<main id="main">

<section class="hero">
  <div class="wrap wrap-wide">
    <div class="hero__frame">
      <div class="hero__media">{img("hero/hero-pool-dusk",
        "HST Architects landscaped villa terrace in Dubai at dusk, with built-in seating, uplit palms and warm concealed lighting",
        sizes="100vw", priority=True)}</div>
      <div class="hero__wordmark" aria-hidden="true">HST</div>

      <div class="trust-chip">
        <div class="trust-chip__avatars">
          <span style="background:#B66B55">HS</span><span style="background:#182331">DB</span><span style="background:#7C8A99">AE</span>
        </div>
        <div class="trust-chip__txt"><b>Design and build under one roof</b><small>Part of {esc(SITE["legal"])}, Downtown Dubai</small></div>
      </div>

      <div class="hero__body">
        <div class="hero__grid">
          <div>
            <span class="eyebrow on-dark">Interior &middot; Renovation &middot; Landscape</span>
            <h1 class="display">{esc(seo["h1"].split(" to ")[0])} <span class="lite">to outlast the trend</span></h1>
          </div>
          <div>
            <p class="hero__sub">We design and build <strong>villas, offices, showrooms and gardens</strong> across Dubai. One team
              from the first sketch to the final snag, so nothing is lost in translation between designer and site.</p>
            <div class="hero__cta">
              {btn("Book a site visit", "/contact/", "light")}
              {btn("View our projects", "/projects/", "outline")}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="hero-stats reveal">{stats}</div>
  </div>
</section>

<section class="strip section-sm">
  <p class="strip__label">Delivering <b>interiors, fit-out and landscape</b> across the Emirates</p>
  <div class="marquee">{marquee}</div>
</section>

<section class="section" aria-labelledby="svc-h">
  {plan_deco("courtyard", "head")}
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__text">
        <span class="eyebrow">Our expertise</span>
        <h2 class="h2 split-head" id="svc-h">Crafted for <span class="lite">exceptional</span> Dubai <span class="lite">spaces</span></h2>
        <p class="lede">Three disciplines that most clients need together, delivered by one studio under one contract.</p>
      </div>
      {btn("All services", "/services/", "ghost")}
    </div>
    <div class="grid g-3">{svc_cards}</div>
  </div>
</section>

<section class="section" aria-labelledby="about-h">
  <div class="wrap">
    <div class="split reveal">
      <div class="split__media">{img("hero/hero-office-skyline",
        "HST Architects designed office interior in Dubai with a chandelier and floor-to-ceiling city views",
        sizes="(max-width:900px) 92vw, 46vw")}</div>
      <div class="split__body">
        <span class="eyebrow">About us</span>
        <h2 class="h2 split-head" id="about-h">Luxury interiors<span class="inline-pill">{img("services/interior-curved-living", "", sizes="124px")}</span>
          <span class="lite">and outdoor spaces</span><span class="inline-pill">{img("services/landscape-villa-pool", "", sizes="124px")}</span>
          engineered <span class="lite">to last.</span></h2>
        <p class="lede" style="margin-top:1.4rem">HST Architects is the design arm of {esc(SITE["legal"])}, a licensed UAE building
          maintenance and technical services company. That licence is the reason we can draw a project and then actually build it,
          with joinery, finishes and technical works included.</p>
        <div class="grid g-2" style="margin-top:2rem;gap:1rem">{why}</div>
        <div style="margin-top:2rem">{btn("More about the studio", "/about/", "ghost")}</div>
      </div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="proj-h">
  <div class="wrap wrap-wide">
    <div class="sec-head reveal">
      <div class="sec-head__text">
        <span class="eyebrow">Selected work</span>
        <h2 class="h2 split-head" id="proj-h">Explore our newest <span class="lite">project gallery</span></h2>
      </div>
      <div style="display:flex;gap:.6rem;align-items:center">
        <div class="rail-nav" data-rail="home-rail">
          <button class="icon-btn" type="button" data-dir="prev" aria-label="Previous projects">{icon("arrow-l")}</button>
          <button class="icon-btn" type="button" data-dir="next" aria-label="Next projects">{icon("arrow-r")}</button>
        </div>
        {btn("View all projects", "/projects/", "ghost")}
      </div>
    </div>
    <div class="rail reveal" id="home-rail">{rail}</div>
  </div>
</section>

<section class="section" aria-labelledby="proc-h">
  {plan_deco("dual", "right", size="min(38%, 500px)")}
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__text">
        <span class="eyebrow">How we work</span>
        <h2 class="h2 split-head" id="proc-h">From first visit <span class="lite">to final snag</span></h2>
        <p class="lede">Five stages, each with a deliverable you sign off before the next one starts.</p>
      </div>
    </div>
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="section" aria-labelledby="sect-h">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__text">
        <span class="eyebrow">Sectors</span>
        <h2 class="h2 split-head" id="sect-h">The kinds of space <span class="lite">we work on</span></h2>
        <p class="lede">Residential, workplace, retail, hospitality, fitness and landscape, every one of these is represented in the portfolio.</p>
      </div>
      {btn("See the portfolio", "/projects/", "ghost")}
    </div>
    <div class="grid g-3">{sectors}</div>
  </div>
</section>

{faq_block(HOME_FAQS, "Straight answers before you call",
           "The questions we are asked most often about working with a Dubai design-and-build studio.")}

{cta_band("Tell us about the space.", "We will tell you what it needs.",
          "Send the property details and what you want to change. We arrange a site visit and follow it with a written scope and a fixed fee.")}

{related_block([
  ("Interior design in Dubai", "Concept, 3D visuals and full FF&E", "/services/interior-design/"),
  ("Renovation & fit-out", "Turnkey refurbishment with approvals handled", "/services/renovation/"),
  ("Landscaping", "Gardens, pools and pergolas for the Gulf climate", "/services/landscaping/"),
  ("The full portfolio", "12 selected projects across the UAE", "/projects/"),
], "Where to go next")}

</main>''' + footer() + tail()

    write("index.html", html_out, "/", "1.0", "weekly")


# ===========================================================================
# SERVICES INDEX
# ===========================================================================
def build_services_index():
    seo = PAGES_SEO["services"]
    trail = [("Home", "/"), ("Services", "/services/")]

    blocks = ""
    for i, s in enumerate(SERVICES):
        caps = "".join(f'''<div><h4 class="h4" style="margin-bottom:.35rem">{esc(c["t"])}</h4>
          <p class="small muted">{esc(c["d"])}</p></div>''' for c in s["capabilities"])
        rev = " split--reverse" if i % 2 else ""
        blocks += f'''<section class="section" aria-labelledby="s-{s["key"]}">
  <div class="wrap">
    <div class="split{rev} reveal">
      <div class="split__media">{img(s["hero_img"], s["hero_alt"], sizes="(max-width:900px) 92vw, 46vw")}</div>
      <div class="split__body">
        <span class="eyebrow">{esc(s["num"])} &middot; {esc(s["title"])}</span>
        <h2 class="h2 split-head" id="s-{s["key"]}">{esc(s["lede"])}</h2>
        <p class="lede" style="margin-top:1.2rem">{esc(s["intro"])}</p>
        <div class="grid g-2" style="margin-top:2rem;gap:1.3rem 1.6rem">{caps}</div>
        <div style="margin-top:2.1rem">{btn(f'{s["title"]} in detail', s["url"], "accent")}</div>
      </div>
    </div>
  </div>
</section>'''

    all_faqs = [f for s in SERVICES for f in s["faqs"][:2]]
    ld = [org_ld(), breadcrumb_ld(trail), faq_ld(all_faqs),
          {"@context": "https://schema.org", "@type": "CollectionPage",
           "url": SITE["domain"] + "/services/", "name": seo["title"], "description": seo["meta"],
           "hasPart": [{"@type": "Service", "name": s["title"], "description": s["short"],
                        "url": SITE["domain"] + s["url"],
                        "provider": {"@id": SITE["domain"] + "/#organization"},
                        "areaServed": {"@type": "City", "name": "Dubai"}} for s in SERVICES]}]

    html_out = head(title=seo["title"], meta=seo["meta"], url="/services/", jsonld=ld,
                    image=og_url("services/renovation-boardroom")) + header("services") + drawer("services") + f'''
<main id="main">
<section class="page-head">
  <div class="wrap">
    {breadcrumbs(trail)}
    <div class="page-head__grid">
      <div>
        <span class="eyebrow">What we do</span>
        <h1 class="h1 split-head">Three disciplines, <span class="lite">one accountable team</span></h1>
      </div>
      <p class="lede">Most projects need more than one of these. Because interiors, construction and landscape sit under a
        single contract at HST, nobody spends the project pointing at someone else.</p>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="wrap"><div class="grid g-3 reveal">
    {"".join(f"""<a class="tile tile--wide" href="{s["url"]}">{img(s["card_img"], s["card_alt"], sizes="(max-width:620px) 92vw, 31vw")}
      <div class="tile__label"><div><h3>{esc(s["title"])}</h3><p>{esc(s["short"])}</p></div>{arrow_badge()}</div></a>""" for s in SERVICES)}
  </div></div>
</section>

{blocks}

{faq_block(all_faqs, "Service questions, answered")}

{cta_band("One studio.", "Every trade under one contract.",
          "Whether you need a single room reworked or a villa taken back to shell and rebuilt with a new garden, the same team runs it.")}

{related_block([
  ("Selected projects", "See these services applied in the UAE", "/projects/"),
  ("About the studio", "Who signs the drawings and runs the site", "/about/"),
  ("Start a project", "Book a site visit in Dubai", "/contact/"),
], "Next steps")}
</main>''' + footer() + tail()

    write("services/index.html", html_out, "/services/", "0.9", "monthly")


# ===========================================================================
# SERVICE DETAIL
# ===========================================================================
def build_service(s):
    trail = [("Home", "/"), ("Services", "/services/"), (s["title"], s["url"])]
    others = [o for o in SERVICES if o["key"] != s["key"]]
    rel_projects = [p for p in PROJECTS if p["service"] == s["key"]][:3]

    caps = "".join(f'''<article class="glass reveal" data-d="{(i%4)+1}" style="padding:1.55rem">
  <h3 class="h4" style="margin-bottom:.5rem">{esc(c["t"])}</h3>
  <p class="small muted">{esc(c["d"])}</p></article>''' for i, c in enumerate(s["capabilities"]))

    gal = "".join(f'<figure>{img(k, a, sizes="(max-width:620px) 92vw, (max-width:900px) 46vw, 31vw")}</figure>'
                  for k, a in s["gallery"])

    outcomes = "".join(f'<li>{esc(o)}</li>' for o in s["outcomes"])

    proj_cards = "".join(f'''<a class="tile" href="/projects/{p["slug"]}/">
  {img(p["img"], p["alt"], sizes="(max-width:620px) 92vw, 31vw")}
  <div class="tile__label"><div><h3>{esc(p["title"])}</h3><p>{esc(p["loc"])}</p></div>{arrow_badge()}</div></a>'''
  for p in rel_projects)

    ld = [org_ld(), breadcrumb_ld(trail), faq_ld(s["faqs"]),
          {"@context": "https://schema.org", "@type": "Service",
           "@id": SITE["domain"] + s["url"] + "#service",
           "serviceType": s["title"], "name": s["seo_title"], "description": s["meta"],
           "url": SITE["domain"] + s["url"],
           "provider": {"@id": SITE["domain"] + "/#organization"},
           "areaServed": [{"@type": "City", "name": a} for a in SITE["areas"][:8]],
           "audience": {"@type": "Audience", "audienceType": "Homeowners, developers and commercial tenants in the UAE"},
           "hasOfferCatalog": {"@type": "OfferCatalog", "name": s["title"] + " capabilities",
             "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": c["t"], "description": c["d"]}}
                                 for c in s["capabilities"]]},
           "image": og_url(s["hero_img"])},
          {"@context": "https://schema.org", "@type": "WebPage",
           "url": SITE["domain"] + s["url"], "name": s["seo_title"], "description": s["meta"],
           "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".lede"]}}]

    html_out = head(title=s["seo_title"], meta=s["meta"], url=s["url"], jsonld=ld,
                    image=og_url(s["hero_img"])) + header("services") + drawer("services") + f'''
<main id="main">
<section class="page-head">
  <div class="wrap">
    {breadcrumbs(trail)}
    <div class="page-head__grid">
      <div>
        <span class="eyebrow">Service {esc(s["num"])}</span>
        <h1 class="h1 split-head">{esc(s["title"])} <span class="lite">in Dubai</span></h1>
      </div>
      <p class="lede">{esc(s["intro"])}</p>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="wrap wrap-wide">
    <div class="split__media reveal" style="border-radius:var(--r-xl);overflow:hidden">
      {img(s["hero_img"], s["hero_alt"], sizes="100vw", priority=True, style="aspect-ratio:16/8;object-fit:cover;width:100%")}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="cap-h">
  {plan_deco("corner", "left", size="min(48%, 640px)")}
  <div class="wrap">
    <div class="sec-head sec-head--split reveal">
      <div class="sec-head__text">
        <span class="eyebrow">What is included</span>
        <h2 class="h2 split-head" id="cap-h">{esc(s["lede"])}</h2>
      </div>
      <div class="sec-head__aside">
        <ul class="tick-list">{outcomes}</ul>
        <p class="small muted" style="margin-top:1.2rem">{esc(s["process_note"])}</p>
      </div>
    </div>
    <div class="grid g-3">{caps}</div>
  </div>
</section>

<section class="section" aria-labelledby="gal-h">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__text">
        <span class="eyebrow">Delivered work</span>
        <h2 class="h2 split-head" id="gal-h">{esc(s["title"])} <span class="lite">we have built</span></h2>
      </div>
    </div>
    <div class="gallery-grid reveal">{gal}</div>
  </div>
</section>

{"" if not proj_cards else f'''<section class="section" aria-labelledby="rp-h">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__text">
        <span class="eyebrow">Case studies</span>
        <h2 class="h2 split-head" id="rp-h">{esc(s["title"])} <span class="lite">projects</span></h2>
      </div>
      {btn("All projects", "/projects/", "ghost")}
    </div>
    <div class="grid g-3 reveal">{proj_cards}</div>
  </div>
</section>'''}

{faq_block(s["faqs"], f'{s["title"]} in Dubai, common questions')}

{cta_band("Ready to start?", "Book the site visit.",
          "Tell us the property, the timeline and roughly what you want to spend. We will come and look, then send a written scope and a fixed fee.")}

{related_block(
  [(o["title"], o["short"], o["url"]) for o in others] +
  [("Selected projects", "See the work across all three disciplines", "/projects/")],
  "Related services")}
</main>''' + footer() + tail()

    write(s["url"].strip("/") + "/index.html", html_out, s["url"], "0.9", "monthly")


# ===========================================================================
# PROJECTS INDEX
# ===========================================================================
def build_projects_index():
    seo = PAGES_SEO["projects"]
    trail = [("Home", "/"), ("Projects", "/projects/")]
    cats = sorted({p["cat"] for p in PROJECTS})

    filters = '<span class="filters__thumb" aria-hidden="true"></span>'
    filters += '<button class="filter is-active" data-filter="all" aria-pressed="true" type="button">All work</button>'
    filters += "".join(f'<button class="filter" data-filter="{esc(c)}" aria-pressed="false" type="button">{esc(c)}</button>' for c in cats)

    cards = "".join(f'''<article class="card reveal" data-cat="{esc(p["cat"])}">
  <div class="card__inner">
    <div class="card__media">{img(p["img"], p["alt"], sizes="(max-width:620px) 92vw, (max-width:900px) 46vw, 31vw")}</div>
    <div class="card__body">
      <div class="card__meta"><span>{esc(p["cat"])}</span></div>
      <h2 class="h3"><a class="card__link" href="/projects/{p["slug"]}/">{esc(p["title"])}</a></h2>
      <p class="small muted card__blurb">{esc(p["blurb"])}</p>
      <div class="card__foot"><span class="small muted">{esc(p["loc"])}</span></div>
    </div>
  </div>
  {arrow_badge("card__go")}
</article>''' for p in PROJECTS)

    ld = [org_ld(), breadcrumb_ld(trail),
          {"@context": "https://schema.org", "@type": "CollectionPage",
           "url": SITE["domain"] + "/projects/", "name": seo["title"], "description": seo["meta"],
           "mainEntity": {"@type": "ItemList", "numberOfItems": len(PROJECTS),
             "itemListElement": [
               {"@type": "ListItem", "position": i + 1,
                "url": SITE["domain"] + "/projects/" + p["slug"] + "/", "name": p["title"]}
               for i, p in enumerate(PROJECTS)]}}]

    html_out = head(title=seo["title"], meta=seo["meta"], url="/projects/", jsonld=ld,
                    image=og_url("projects/proj-cafe-greenery")) + header("projects") + drawer("projects") + f'''
<main id="main">
<section class="page-head">
  <div class="wrap">
    {breadcrumbs(trail)}
    <div class="page-head__grid">
      <div>
        <span class="eyebrow">Portfolio</span>
        <h1 class="h1 split-head">Selected work <span class="lite">across the UAE</span></h1>
      </div>
      <p class="lede">Villas, offices, showrooms, hospitality and gardens delivered by HST Architects across Dubai and Abu Dhabi.
        Each entry lists the scope and location so you can see the kind of work we take on.</p>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="wrap">
    <div class="filters-bar"><div class="filters" data-filters role="group" aria-label="Filter projects by type">{filters}</div></div>
    <div class="grid g-3">{cards}</div>
  </div>
</section>

{cta_band("Yours could be next.", "Let us see the space.",
          "Most of these started with a single site visit and an honest conversation about budget. Book one and we will tell you what is realistic.")}

{related_block([
  (s["title"], s["short"], s["url"]) for s in SERVICES
], "Browse by service")}
</main>''' + footer() + tail()

    write("projects/index.html", html_out, "/projects/", "0.9", "weekly")


# ===========================================================================
# PROJECT DETAIL
# ===========================================================================
def build_project(p, prev_p, next_p):
    url = f'/projects/{p["slug"]}/'
    trail = [("Home", "/"), ("Projects", "/projects/"), (p["title"], url)]
    s = svc(p["service"])
    # keep titles under ~60 chars and descriptions under ~155 so neither is truncated in the SERP
    title = f'{p["title"]} | HST Architects'
    if len(title) > 60:
        title = f'{p["title"]} | HST'
    meta = p["blurb"]
    if len(meta) < 120:
        meta += f' {p["cat"]} project in {p["loc"]}.'
    meta = meta[:155].rsplit(" ", 1)[0].rstrip(" ,.") + "." if len(meta) > 155 else meta

    year_row = (f'<div class="spec__i"><b>Completed</b><span>{esc(p["year"])}</span></div>'
                if p.get("year") else "")
    year_pill = f'<span class="pill">{esc(p["year"])}</span>' if p.get("year") else ""
    eyebrow = f'{esc(p["cat"])} &middot; {esc(p["year"])}' if p.get("year") else esc(p["cat"])

    gal = "".join(f'<figure>{img(k, a, sizes="(max-width:620px) 92vw, (max-width:900px) 46vw, 31vw")}</figure>'
                  for k, a in p["gallery"])

    idx = PROJECTS.index(p)
    others = [o for o in PROJECTS if o["slug"] != p["slug"] and o["cat"] == p["cat"]][:3]
    if len(others) < 3:
        # walk forward from this project so every case study gets linked from somewhere
        rotated = PROJECTS[idx + 1:] + PROJECTS[:idx]
        others += [o for o in rotated if o["slug"] != p["slug"] and o not in others][:3 - len(others)]
    more = "".join(f'''<a class="tile tile--fade" href="/projects/{o["slug"]}/">
  {img(o["img"], o["alt"], sizes="(max-width:620px) 92vw, 31vw")}
  <div class="tile__label"><div><h3>{esc(o["title"])}</h3><p>{esc(o["cat"])} &middot; {esc(o["loc"])}</p></div>{arrow_badge()}</div></a>'''
  for o in others)

    ld = [org_ld(), breadcrumb_ld(trail),
          {"@context": "https://schema.org", "@type": "CreativeWork",
           "@id": SITE["domain"] + url + "#project",
           "name": p["title"], "description": p["blurb"],
           "url": SITE["domain"] + url,
           **({"dateCreated": p["year"]} if p.get("year") else {}),
           "creator": {"@id": SITE["domain"] + "/#organization"},
           "locationCreated": {"@type": "Place", "name": p["loc"],
             "address": {"@type": "PostalAddress", "addressLocality": p["loc"].split(",")[0],
                         "addressRegion": "Dubai", "addressCountry": "AE"}},
           "genre": p["cat"], "keywords": f'{p["cat"]}, {s["title"]}, {p["loc"]}, Dubai',
           "image": [og_url(p["img"])] + [og_url(k) for k, _ in p["gallery"]],
           "about": {"@type": "Service", "name": s["title"], "url": SITE["domain"] + s["url"]}}]

    nav_links = ""
    if prev_p: nav_links += f'<a class="link-arrow" href="/projects/{prev_p["slug"]}/">{icon("arrow-l")}<span>{esc(prev_p["title"])}</span></a>'
    if next_p: nav_links += f'<a class="link-arrow" href="/projects/{next_p["slug"]}/"><span>{esc(next_p["title"])}</span>{icon("arrow-r")}</a>'

    html_out = head(title=title, meta=meta, url=url, jsonld=ld,
                    image=og_url(p["img"])) + header("projects") + drawer("projects") + f'''
<main id="main">
<section class="page-head">
  <div class="wrap">
    {breadcrumbs(trail)}
    <div class="page-head__grid">
      <div>
        <span class="eyebrow">{eyebrow}</span>
        <h1 class="h1 split-head">{esc(p["title"])}</h1>
      </div>
      <p class="lede">{esc(p["blurb"])}</p>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="wrap wrap-wide">
    <div class="hero-figure reveal">
      <div class="hero-figure__media">
        {img(p["img"], p["alt"], sizes="100vw", priority=True, style="aspect-ratio:16/8;object-fit:cover;width:100%")}
      </div>
      <div class="spec spec--float glass">
      <div class="spec__i"><b>Location</b><span>{esc(p["loc"])}</span></div>
      {year_row}
      <div class="spec__i"><b>Sector</b><span>{esc(p["cat"])}</span></div>
      <div class="spec__i"><b>Discipline</b><span><a href="{s["url"]}" style="color:inherit;border-bottom:1px solid var(--line-strong)">{esc(s["title"])}</a></span></div>
      </div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="scope-h">
  {plan_deco("atrium", "right", size="min(40%, 540px)")}
  <div class="wrap">
    <div class="split reveal">
      <div class="split__body prose">
        <span class="eyebrow">The brief</span>
        <h2 class="h2 split-head" id="scope-h">Scope <span class="lite">of works</span></h2>
        <p style="margin-top:1.2rem">{esc(p["scope"])}.</p>
        <p>Delivered as a single package by HST Architects: design, technical drawings, authority coordination where
           required, site execution and handover. The discipline lead for this project was
           <a href="{s["url"]}">{esc(s["title"].lower())}</a>, supported by our in-house technical services team.</p>
        <div class="pill-list" style="margin-top:1.6rem">
          <span class="pill">{esc(p["cat"])}</span><span class="pill">{esc(p["loc"])}</span>{year_pill}
        </div>
        <div style="margin-top:2rem">{btn("Start a similar project", "/contact/", "accent")}</div>
      </div>
      <div class="split__media">{img(p["gallery"][0][0] if p["gallery"] else p["img"],
        p["gallery"][0][1] if p["gallery"] else p["alt"], sizes="(max-width:900px) 92vw, 46vw")}</div>
    </div>
  </div>
</section>

{"" if not gal else f'''<section class="section" aria-labelledby="pg-h">
  <div class="wrap">
    <div class="sec-head reveal"><div class="sec-head__text">
      <span class="eyebrow">Gallery</span>
      <h2 class="h2 split-head" id="pg-h">Inside <span class="lite">{esc(p["title"])}</span></h2>
    </div></div>
    <div class="gallery-grid reveal">{gal}</div>
  </div>
</section>'''}

<section class="section-sm">
  <div class="wrap"><div style="display:flex;justify-content:space-between;gap:1.5rem;flex-wrap:wrap;
    padding-block:1.6rem;border-block:1px solid var(--line)">{nav_links}</div></div>
</section>

<section class="section" aria-labelledby="more-h">
  <div class="wrap">
    <div class="sec-head reveal"><div class="sec-head__text">
      <span class="eyebrow">More work</span>
      <h2 class="h2 split-head" id="more-h">Related <span class="lite">projects</span></h2>
    </div>{btn("All projects", "/projects/", "ghost")}</div>
    <div class="grid g-3 reveal">{more}</div>
  </div>
</section>

{cta_band("Like what you see?", "Let us do it for your space.",
          "Send the property details and a note about what you want to change. We will arrange a site visit from there.")}

{related_block([
  (s["title"], s["short"], s["url"]),
  ("All projects", "The full HST portfolio", "/projects/"),
  ("Contact the studio", "Downtown Dubai, Sat to Thu", "/contact/"),
], "Continue")}
</main>''' + footer() + tail()

    write(f'projects/{p["slug"]}/index.html', html_out, url, "0.7", "yearly")


# ===========================================================================
# ABOUT
# ===========================================================================
def build_about():
    seo = PAGES_SEO["about"]
    trail = [("Home", "/"), ("About", "/about/")]

    steps = "".join(f'''<div class="step reveal"><div class="step__n">{esc(s["n"])}</div>
  <h3 class="step__t">{esc(s["t"])}</h3><p class="step__d">{esc(s["d"])}</p></div>''' for s in PROCESS)
    why = "".join(f'''<article class="glass reveal" data-d="{i+1}" style="padding:1.7rem">
  <span class="arrow-badge" style="background:var(--accent-soft);color:var(--accent);width:40px;height:40px">{icon("check")}</span>
  <h3 class="h4" style="margin:1.05rem 0 .5rem">{esc(w["t"])}</h3>
  <p class="small muted">{esc(w["d"])}</p></article>''' for i, w in enumerate(WHY_US))
    facts = [(str(len(PROJECTS)), "Projects in this portfolio"),
             ("3", "Disciplines in-house"),
             (str(len({p["cat"] for p in PROJECTS})), "Sectors delivered"),
             ("2", "Emirates covered")]
    stats = "".join(f'<div class="hero-stats__item"><div class="hero-stats__v">{esc(v)}</div>'
                    f'<div class="hero-stats__l">{esc(l)}</div></div>' for v, l in facts)

    about_faqs = [
        {"q": "Is HST Architects a design studio or a contractor?",
         "a": "Both. HST Architects is the design arm of HST Group, a licensed UAE building maintenance and technical services "
              "company. We produce the design and then execute it with our own technicians and vetted trades under one contract."},
        {"q": "How long has the studio been operating in the UAE?",
         "a": "Since 2015. The practice grew out of building maintenance and technical services work, which is why our drawings "
              "tend to be more buildable than most: the practice grew out of fixing what other people specified."},
        {"q": "Do you take on projects outside Dubai?",
         "a": "Yes. Most of our work is in Dubai, but we deliver selected projects in Abu Dhabi and Sharjah, including the "
              "GAMA Fashion showroom in Abu Dhabi, which is in the portfolio."},
        {"q": "Who will I actually be dealing with?",
         "a": "One project lead from the first site visit to handover. They attend the design meetings and they walk the site, "
              "so you are never re-explaining the project to a new face."},
    ]

    ld = [org_ld(), breadcrumb_ld(trail), faq_ld(about_faqs),
          {"@context": "https://schema.org", "@type": "AboutPage",
           "url": SITE["domain"] + "/about/", "name": seo["title"], "description": seo["meta"],
           "mainEntity": {"@id": SITE["domain"] + "/#organization"}}]

    html_out = head(title=seo["title"], meta=seo["meta"], url="/about/", jsonld=ld,
                    image=og_url("hero/hero-architecture-dark")) + header("about") + drawer("about") + f'''
<main id="main">
<section class="page-head">
  <div class="wrap">
    {breadcrumbs(trail)}
    <div class="page-head__grid">
      <div>
        <span class="eyebrow">About HST</span>
        <h1 class="h1 split-head">A studio that signs <span class="lite">its own site drawings</span></h1>
      </div>
      <p class="lede">HST Architects is the design practice inside {esc(SITE["legal"])}, a licensed Dubai building maintenance
        and technical services company. We draw projects, then we build them.</p>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="wrap wrap-wide">
    <div class="reveal" style="border-radius:var(--r-xl);overflow:hidden">
      {img("hero/hero-office-skyline", "HST Architects designed office in Downtown Dubai with sweeping city views",
           sizes="100vw", priority=True, style="aspect-ratio:16/7.5;object-fit:cover;width:100%")}
    </div>
    <div class="hero-stats reveal">{stats}</div>
  </div>
</section>

<section class="section" aria-labelledby="story-h">
  <div class="wrap">
    <div class="split reveal">
      <div class="split__body prose">
        <span class="eyebrow">Who we are</span>
        <h2 class="h2 split-head" id="story-h">We started on the maintenance side. <span class="lite">It shows in the drawings.</span></h2>
        <p style="margin-top:1.3rem">Most design studios hand a set of drawings to a contractor and hope. HST came at it from the
          other direction: years of building maintenance and technical services work across residential and commercial
          buildings in Dubai, watching which details fail in year two and which ones hold.</p>
        <p>That is the practice's advantage. When we specify a stone, a joinery detail or an irrigation run, it is chosen
          against what we have already had to repair somewhere else in this city. Our head office is in Boulevard Plaza,
          Downtown Dubai, and our teams work across the Emirates on
          <a href="/services/interior-design/">interior design</a>,
          <a href="/services/renovation/">renovation and fit-out</a>, and
          <a href="/services/landscaping/">landscaping</a>.</p>
        <p>We work for private villa owners, property developers, retail brands and commercial tenants. The common thread is
          that they wanted one company answerable for the result rather than three pointing at each other.</p>
        <div style="margin-top:2rem">{btn("See the portfolio", "/projects/", "accent")}</div>
      </div>
      <div class="split__media">{img("hero/hero-architecture-dark",
        "Contemporary angular architecture with dark glazing, representing the HST design language",
        sizes="(max-width:900px) 92vw, 46vw")}</div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="why-h">
  <div class="wrap">
    <div class="sec-head reveal"><div class="sec-head__text">
      <span class="eyebrow">Why clients stay</span>
      <h2 class="h2 split-head" id="why-h">Four things <span class="lite">we will not compromise on</span></h2>
    </div></div>
    <div class="grid g-4">{why}</div>
  </div>
</section>

<section class="section" aria-labelledby="proc-h">
  {plan_deco("dual", "right", size="min(38%, 500px)")}
  <div class="wrap">
    <div class="sec-head reveal"><div class="sec-head__text">
      <span class="eyebrow">Our process</span>
      <h2 class="h2 split-head" id="proc-h">Five stages, <span class="lite">each one signed off</span></h2>
      <p class="lede">No stage begins until you have approved the one before it, in writing.</p>
    </div></div>
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="section">
  {plan_deco("curved", "center", size="min(46%, 560px)")}
  <div class="wrap wrap-narrow" style="text-align:center">
    <span class="eyebrow" style="justify-content:center">Our standard</span>
    <blockquote class="quote reveal" style="margin:0">&ldquo;Architecture is the thoughtful making of space, light, and form.&rdquo;</blockquote>
    <p class="small muted" style="margin-top:1.2rem;letter-spacing:.14em;text-transform:uppercase">HST Architects</p>
  </div>
</section>

{faq_block(about_faqs, "About the studio")}

{cta_band("Come and see us.", "Boulevard Plaza, Downtown Dubai.",
          "Or send the property details and we will come to you. Either way the first conversation costs nothing.")}

{related_block([
  ("Our services", "Interior, renovation and landscape", "/services/"),
  ("Selected projects", "Twelve case studies across the UAE", "/projects/"),
  ("Contact the studio", "Call, email or book a visit", "/contact/"),
])}
</main>''' + footer() + tail()

    write("about/index.html", html_out, "/about/", "0.8", "monthly")


# ===========================================================================
# CONTACT
# ===========================================================================
def build_contact():
    seo = PAGES_SEO["contact"]
    trail = [("Home", "/"), ("Contact", "/contact/")]

    opts = "".join(f'<option value="{esc(s["title"])}">{esc(s["title"])}</option>' for s in SERVICES)

    ld = [org_ld(), breadcrumb_ld(trail),
          {"@context": "https://schema.org", "@type": "ContactPage",
           "url": SITE["domain"] + "/contact/", "name": seo["title"], "description": seo["meta"],
           "mainEntity": {"@id": SITE["domain"] + "/#organization"}}]

    html_out = head(title=seo["title"], meta=seo["meta"], url="/contact/", jsonld=ld,
                    image=og_url("hero/hero-pergola-lounge")) + header("contact") + drawer("contact") + f'''
<main id="main">
<section class="page-head">
  <div class="wrap">
    {breadcrumbs(trail)}
    <div class="page-head__grid">
      <div>
        <span class="eyebrow">Get in touch</span>
        <h1 class="h1 split-head">Tell us about <span class="lite">the space</span></h1>
      </div>
      <p class="lede">Tell us the property type, size, timeline and rough budget up front. The more we know, the
        more useful our first reply will be.</p>
    </div>
  </div>
</section>

<section class="section-sm">
  {plan_deco("orthogonal", "left", size="min(40%, 500px)")}
  <div class="wrap">
    <div class="split" style="align-items:start;gap:clamp(1.6rem,4vw,3.5rem)">

      <div class="contact-panel glass reveal">
        <h2 class="h3" style="margin-bottom:.6rem">Send an enquiry</h2>
        <p class="small muted" style="margin-bottom:1.6rem">Fields marked with an asterisk are required.</p>

        <form class="form" id="contact-form" novalidate>
          <div class="form__row">
            <div class="field">
              <label for="f-name">Your name <span class="req" aria-hidden="true">*</span></label>
              <input id="f-name" name="name" type="text" autocomplete="name" required placeholder="Ali Hassan">
              <span class="field__err"></span>
            </div>
            <div class="field">
              <label for="f-email">Email <span class="req" aria-hidden="true">*</span></label>
              <input id="f-email" name="email" type="email" autocomplete="email" required placeholder="you@company.ae">
              <span class="field__err"></span>
            </div>
          </div>
          <div class="form__row">
            <div class="field">
              <label for="f-phone">Phone or WhatsApp</label>
              <input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="+971 50 000 0000">
              <span class="field__err"></span>
            </div>
            <div class="field">
              <label for="f-service">What do you need?</label>
              <select id="f-service" name="service">
                <option value="">Select a service</option>
                {opts}
                <option value="Multiple / not sure">Multiple, or not sure yet</option>
              </select>
            </div>
          </div>
          <div class="field">
            <label for="f-budget">Indicative budget</label>
            <select id="f-budget" name="budget">
              <option value="">Prefer not to say</option>
              <option value="Under AED 250k">Under AED 250,000</option>
              <option value="AED 250k to 750k">AED 250,000 to 750,000</option>
              <option value="AED 750k to 2m">AED 750,000 to 2 million</option>
              <option value="Over AED 2m">Over AED 2 million</option>
            </select>
          </div>
          <div class="field">
            <label for="f-message">About the project <span class="req" aria-hidden="true">*</span></label>
            <textarea id="f-message" name="message" required
              placeholder="A 4-bedroom villa in Dubai Hills. We want the ground floor reworked and the garden landscaped, ideally starting after Ramadan."></textarea>
            <span class="field__err"></span>
          </div>
          <div class="hp" aria-hidden="true">
            <label for="f-company">Company (leave blank)</label>
            <input id="f-company" name="company" type="text" tabindex="-1" autocomplete="off">
          </div>
          <div class="form__status" id="form-status" role="status" aria-live="polite"></div>
          <button class="btn btn--accent btn--lg" type="submit" style="justify-self:start">
            <span>Send enquiry</span><span class="arrow">{icon("arrow")}</span>
          </button>
          <p class="form__note">By sending this you agree that we may contact you about your project. We do not share your
            details with anyone else.</p>
        </form>
      </div>

      <div class="reveal">
        <div class="contact-panel glass">
          <h2 class="h3" style="margin-bottom:1rem">Studio details</h2>
          <div class="contact-item">
            <span class="contact-item__ic">{icon("phone")}</span>
            <div><b>Call the studio</b>
              <a href="tel:{SITE["phone_link"]}">{SITE["phone_display"]}</a><br>
              <a href="tel:{SITE["landline_link"]}">{SITE["landline_display"]}</a></div>
          </div>
          <div class="contact-item">
            <span class="contact-item__ic">{icon("mail")}</span>
            <div><b>Email</b><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></div>
          </div>
          <div class="contact-item">
            <span class="contact-item__ic">{icon("pin")}</span>
            <div><b>Visit</b><span>{esc(SITE["address_line"])}<br>{esc(SITE["address_locality"])}, UAE</span></div>
          </div>
          <div class="contact-item">
            <span class="contact-item__ic">{icon("clock")}</span>
            <div><b>Opening hours</b><span>Saturday to Thursday, 9:00 to 18:00</span></div>
          </div>
          <div style="margin-top:1.4rem;display:flex;gap:.6rem;flex-wrap:wrap">
            {btn("WhatsApp us", "https://wa.me/" + SITE["phone_link"].lstrip("+"), "accent",
                 attrs='rel="noopener noreferrer nofollow" target="_blank"')}
          </div>
        </div>

        <div style="margin-top:1.2rem;border-radius:var(--r-lg);overflow:hidden;border:1px solid var(--line)">
          <iframe title="Map showing HST Architects at Boulevard Plaza Tower 1, Downtown Dubai"
            src="https://www.google.com/maps?q=Boulevard%20Plaza%20Tower%201%20Downtown%20Dubai&output=embed"
            width="100%" height="300" style="border:0;display:block" loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>

        <div style="margin-top:1.2rem" class="pill-list">
          {"".join(f'<span class="pill">{esc(a)}</span>' for a in SITE["areas"][:9])}
        </div>
      </div>

    </div>
  </div>
</section>

{related_block([
  ("Interior design", "Concept, 3D and FF&E for Dubai properties", "/services/interior-design/"),
  ("Renovation & fit-out", "Turnkey delivery with approvals included", "/services/renovation/"),
  ("Landscaping", "Gardens, pools and pergolas", "/services/landscaping/"),
  ("Selected projects", "See what we have delivered", "/projects/"),
], "Before you write, have a look at")}
</main>''' + footer() + tail()

    write("contact/index.html", html_out, "/contact/", "0.9", "monthly")


# ===========================================================================
# 404
# ===========================================================================
def build_404():
    html_out = head(title="Page not found | HST Architects",
                    meta="That page is not here. Browse our Dubai interior design, renovation and landscaping work instead.",
                    url="/404.html", robots="noindex, follow") + header("") + drawer("") + f'''
<main id="main">
<section class="page-head" style="padding-bottom:clamp(4rem,10vw,8rem)">
  <div class="wrap wrap-narrow" style="text-align:center">
    <span class="eyebrow" style="justify-content:center">Error 404</span>
    <h1 class="display" style="margin-bottom:1.2rem">Not<span style="color:var(--ink-faint)"> here</span></h1>
    <p class="lede" style="margin-inline:auto;max-width:48ch">The page you were after has moved or never existed.
      Everything we build is one of these three things, so start there.</p>
    <div style="display:flex;gap:.7rem;justify-content:center;flex-wrap:wrap;margin-top:2rem">
      {btn("Back to home", "/", "accent")}{btn("View projects", "/projects/", "ghost")}
    </div>
  </div>
</section>
{related_block([(s["title"], s["short"], s["url"]) for s in SERVICES] +
               [("Contact the studio", "Downtown Dubai", "/contact/")], "Try one of these")}
</main>''' + footer() + tail()
    write("404.html", html_out)


# ===========================================================================
# Static assets
# ===========================================================================
def build_static():
    # favicon, a compact HST monogram that stays legible at 16px
    favicon = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="13" fill="#182331"/>
<path d="M13 19h6.4v10.1h9.2V19H35v26h-6.4V34.6h-9.2V45H13V19Z" fill="#F7F3EA"/>
<path d="M38.5 45c-1 0-1.6-.7-1.6-1.6s.6-1.6 1.6-1.6h12.4c1 0 1.6.7 1.6 1.6s-.6 1.6-1.6 1.6H38.5Z" fill="#B66B55"/>
<path d="M39 41.6c3-8 7.4-13.6 12.2-16.6" stroke="#B66B55" stroke-width="2.6" fill="none" stroke-linecap="round"/>
</svg>'''
    write("favicon.svg", favicon)

    # iOS composites apple-touch-icons on black and applies its own corner mask,
    # so this is drawn opaque and square at 4x, then downsampled for clean edges.
    from PIL import Image, ImageDraw
    S = 720
    icon_img = Image.new("RGB", (S, S), "#182331")
    d = ImageDraw.Draw(icon_img)
    bar, h_l, h_r, h_top, h_bot = S * 0.072, S * 0.20, S * 0.545, S * 0.28, S * 0.70
    d.rectangle([h_l, h_top, h_l + bar, h_bot], fill="#F7F3EA")            # H left stem
    d.rectangle([h_r, h_top, h_r + bar, h_bot], fill="#F7F3EA")            # H right stem
    d.rectangle([h_l, S * 0.455, h_r + bar, S * 0.455 + bar], fill="#F7F3EA")  # H crossbar
    d.rectangle([S * 0.20, S * 0.745, S * 0.80, S * 0.745 + bar * 0.62], fill="#B66B55")
    icon_img.resize((180, 180), Image.LANCZOS).save(
        os.path.join(ROOT, "apple-touch-icon.png"), "PNG", optimize=True)

    manifest = {
        "name": SITE["name"], "short_name": "HST",
        "description": SITE["short_desc"],
        "start_url": "/", "scope": "/", "display": "standalone",
        "background_color": "#F1EDE4", "theme_color": "#182331",
        "lang": "en-AE", "dir": "ltr",
        "icons": [
            {"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
            {"src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
        ],
    }
    write("site.webmanifest", json.dumps(manifest, indent=2, ensure_ascii=False))

    robots = f"""# robots.txt, {SITE['domain']}
User-agent: *
Allow: /
Disallow: /_
Disallow: /*?filter=

# Generative / answer engines are welcome to read and cite this site.
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-Web
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: CCBot
Allow: /

Sitemap: {SITE['domain']}/sitemap.xml
Host: {SITE['domain'].replace('https://', '')}
"""
    write("robots.txt", robots)

    # llms.txt, a plain-text map for answer engines
    svc_lines = "\n".join(f'- [{s["title"]}]({SITE["domain"]}{s["url"]}): {s["short"]}' for s in SERVICES)
    proj_lines = "\n".join(
        f'- [{p["title"]}]({SITE["domain"]}/projects/{p["slug"]}/): {p["cat"]}, {p["loc"]}, {p["year"]}.'
        for p in PROJECTS)
    llms = f"""# {SITE['name']}

> {SITE['short_desc']}

{SITE['name']} is the design practice of {SITE['legal']}, a licensed UAE building maintenance and technical
services company operating from {SITE['address_line']}, {SITE['address_locality']}. The studio delivers design
and build under one contract: interior design, renovation and fit-out, and landscaping.

- Location: {SITE['address_line']}, {SITE['address_locality']}, United Arab Emirates
- Phone: {SITE['phone_display']} / {SITE['landline_display']}
- Email: {SITE['email']}
- Hours: {SITE['hours_display']} (Gulf Standard Time)
- Areas served: {", ".join(SITE['areas'])}

## Services
{svc_lines}

## Projects
{proj_lines}

## Key pages
- [Home]({SITE['domain']}/): overview of the studio and its three disciplines.
- [Services]({SITE['domain']}/services/): full capability list across interiors, construction and landscape.
- [Projects]({SITE['domain']}/projects/): {len(PROJECTS)} case studies with scope, area, location and year.
- [About]({SITE['domain']}/about/): studio history, process and standards.
- [Contact]({SITE['domain']}/contact/): enquiry form, phone, email and studio address.
"""
    write("llms.txt", llms)

    # Vercel config: clean URLs, security headers, long-lived asset caching
    vercel = {
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "cleanUrls": True,
        "trailingSlash": True,
        "headers": [
            # Images are content-stable: a new photograph gets a new slug.
            {"source": "/assets/img/(.*)",
             "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            # CSS and JS change on every content edit and carry no content hash in
            # the filename, so they are revalidated rather than pinned for a year.
            {"source": "/assets/(css|js)/(.*)",
             "headers": [{"key": "Cache-Control",
                          "value": "public, max-age=600, stale-while-revalidate=86400"}]},
            {"source": "/(.*)",
             "headers": [
                 {"key": "X-Content-Type-Options", "value": "nosniff"},
                 {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
                 {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                 {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), interest-cohort=()"},
                 {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
             ]},
        ],
        # NOTE: trailingSlash normalises "/x" to "/x/" BEFORE redirects are matched,
        # so every source below must carry the trailing slash or it will never fire.
        "redirects": [
            {"source": "/index.html", "destination": "/", "permanent": True},
        ] + [
            {"source": src, "destination": dest, "permanent": True}
            for src, dest in [
                ("/home/", "/"),
                ("/services/interior/", "/services/interior-design/"),
                ("/services/interiors/", "/services/interior-design/"),
                ("/services/fit-out/", "/services/renovation/"),
                ("/services/fitout/", "/services/renovation/"),
                ("/services/landscape/", "/services/landscaping/"),
                ("/services/landscaping-dubai/", "/services/landscaping/"),
                ("/portfolio/", "/projects/"),
                ("/work/", "/projects/"),
                ("/our-work/", "/projects/"),
                ("/gallery/", "/projects/"),
                ("/about-us/", "/about/"),
                ("/contact-us/", "/contact/"),
                ("/get-a-quote/", "/contact/"),
            ]
        ],
    }
    write("vercel.json", json.dumps(vercel, indent=2))


def prune_orphans():
    """Delete generated pages that the current content model no longer produces."""
    keep = {u for u, _, _ in URLS} | {"/404.html"}
    removed = []
    for base in ("projects", "services"):
        root = os.path.join(ROOT, base)
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            d = os.path.join(root, name)
            if not os.path.isdir(d):
                continue
            if f"/{base}/{name}/" not in keep:
                shutil.rmtree(d)
                removed.append(f"/{base}/{name}/")
    if removed:
        print(f"Pruned {len(removed)} orphaned page(s):")
        for r in removed:
            print("  -", r)


def build_sitemap():
    entries = ""
    for loc, prio, freq in URLS:
        entries += (f'\n  <url>\n    <loc>{SITE["domain"]}{loc}</loc>'
                    f'\n    <lastmod>{TODAY}</lastmod>'
                    f'\n    <changefreq>{freq}</changefreq>'
                    f'\n    <priority>{prio}</priority>\n  </url>')
    xml = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}\n</urlset>\n')
    write("sitemap.xml", xml)


# ===========================================================================
def main():
    build_home()
    build_services_index()
    for s in SERVICES:
        build_service(s)
    build_projects_index()
    for i, p in enumerate(PROJECTS):
        build_project(p, PROJECTS[i - 1] if i else None, PROJECTS[i + 1] if i + 1 < len(PROJECTS) else None)
    build_about()
    build_contact()
    build_404()
    build_static()
    prune_orphans()
    build_sitemap()
    print(f"Built {len(URLS)} indexable pages + static files")
    for u, p, f in URLS:
        print(f"  {p}  {u}")


if __name__ == "__main__":
    main()
