# -*- coding: utf-8 -*-
"""Shared HTML shell: head, header, drawer, footer, image + icon helpers."""
import json, os, html
from content import SITE, NAV, SERVICES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = json.load(open(os.path.join(ROOT, "assets", "img", "manifest.json"), encoding="utf-8"))

def esc(s):
    return html.escape(str(s), quote=True)

# ---------------------------------------------------------------- images
def img(key, alt, sizes="100vw", cls="", loading="lazy", priority=False, style=""):
    """Responsive <picture> from the generated manifest."""
    m = MANIFEST.get(key)
    if not m:
        raise KeyError(f"image '{key}' is not in the manifest — add it to tools/build_images.py")
    widths = m["widths"]
    webp = ", ".join(f"/assets/img/{key}-{w['label']}.webp {w['real']}w" for w in widths)
    attrs = [
        f'src="/assets/img/{key}.jpg"',
        f'alt="{esc(alt)}"',
        f'width="{m["w"]}"', f'height="{m["h"]}"',
    ]
    if cls:   attrs.append(f'class="{cls}"')
    if style: attrs.append(f'style="{style}"')
    if priority:
        attrs.append('loading="eager"'); attrs.append('fetchpriority="high"'); attrs.append('decoding="async"')
    else:
        attrs.append(f'loading="{loading}"'); attrs.append('decoding="async"')
    return (f'<picture><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img {" ".join(attrs)}></picture>')

def og_url(key):
    """Social-card image. Always JPEG — LinkedIn and WhatsApp do not decode WebP."""
    if key not in MANIFEST:
        raise KeyError(key)
    return f'{SITE["domain"]}/assets/img/{key}.jpg'

def img_url(key, w=1280):
    m = MANIFEST.get(key)
    if not m: raise KeyError(key)
    labels = [x["label"] for x in m["widths"]]
    pick = w if w in labels else max(labels)
    return f'{SITE["domain"]}/assets/img/{key}-{pick}.webp'

# ---------------------------------------------------------------- icons
ICONS = {
  "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>',
  "arrow-r": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
  "arrow-l": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>',
  "sun": '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.2M12 19.8V22M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6M2 12h2.2M19.8 12H22M4.9 19.1l1.6-1.6M17.5 6.5l1.6-1.6"/></svg>',
  "moon": '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 14.2A8.6 8.6 0 0 1 9.8 3.5a8.6 8.6 0 1 0 10.7 10.7Z"/></svg>',
  "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
  "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
  "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21.5 16.9v2.8a1.9 1.9 0 0 1-2.1 1.9 18.8 18.8 0 0 1-8.2-2.9 18.5 18.5 0 0 1-5.7-5.7A18.8 18.8 0 0 1 2.6 4.7 1.9 1.9 0 0 1 4.5 2.6h2.8a1.9 1.9 0 0 1 1.9 1.6c.1.9.35 1.8.7 2.6a1.9 1.9 0 0 1-.42 2l-1.2 1.2a15 15 0 0 0 5.7 5.7l1.2-1.2a1.9 1.9 0 0 1 2-.42c.83.35 1.7.6 2.6.7a1.9 1.9 0 0 1 1.6 1.95Z"/></svg>',
  "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="4.5" width="19" height="15" rx="2.2"/><path d="m3 6.5 9 6.2 9-6.2"/></svg>',
  "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10.5c0 5.6-8 12-8 12s-8-6.4-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10.4" r="2.9"/></svg>',
  "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.2"/><path d="M12 7v5.3l3.4 2"/></svg>',
  "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="3.8"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg>',
  "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5A2.5 2.5 0 1 0 5 8.5a2.5 2.5 0 0 0-.02-5ZM3 9.5h4v11H3v-11Zm6.5 0h3.8v1.5h.05a4.2 4.2 0 0 1 3.77-2.07c4.03 0 4.78 2.65 4.78 6.1v5.47h-4v-4.85c0-1.16-.02-2.65-1.62-2.65-1.62 0-1.87 1.26-1.87 2.57v4.93h-4v-11Z"/></svg>',
  "whatsapp": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.6 2 2.2 6.4 2.2 11.84c0 1.74.46 3.44 1.32 4.94L2.1 22l5.35-1.4a9.8 9.8 0 0 0 4.6 1.17h.01c5.43 0 9.84-4.4 9.84-9.84 0-2.63-1.02-5.1-2.88-6.96A9.78 9.78 0 0 0 12.04 2Zm0 1.8a8 8 0 0 1 8.04 8.04c0 4.44-3.6 8.04-8.04 8.04a8 8 0 0 1-4.1-1.12l-.3-.18-3.05.8.81-2.98-.19-.3a8 8 0 0 1 6.83-12.3Zm-2.2 3.9c-.17-.4-.35-.4-.51-.41h-.44c-.15 0-.4.06-.6.3-.21.24-.79.77-.79 1.88s.81 2.18.92 2.33c.11.15 1.57 2.5 3.9 3.4 1.94.75 2.33.6 2.75.56.42-.04 1.35-.55 1.54-1.09.19-.53.19-.99.13-1.08-.06-.1-.21-.15-.44-.27-.23-.11-1.35-.66-1.56-.74-.21-.08-.36-.11-.51.12-.15.23-.58.73-.71.88-.13.15-.26.17-.49.06-.23-.12-.97-.36-1.85-1.14-.68-.61-1.14-1.36-1.28-1.59-.13-.23-.01-.35.1-.47.1-.1.23-.27.34-.4.11-.14.15-.23.23-.38.08-.15.04-.29-.02-.4-.06-.12-.51-1.24-.7-1.7Z"/></svg>',
  "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>',
  "compass": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.3"/><path d="m15.6 8.4-2.1 5.1-5.1 2.1 2.1-5.1 5.1-2.1Z"/></svg>',
  "ruler": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.6" y="8.6" width="18.8" height="6.8" rx="1.6" transform="rotate(-45 12 12)"/><path d="M9 8.2 10.4 9.6M11.6 10.8 13 12.2M14.2 13.4l1.4 1.4"/></svg>',
  "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20c0-8 5.4-14 16-15 .5 7.6-4.2 15-12 15H4Z"/><path d="M4 20c3-4.5 6.6-7.4 11-9.4"/></svg>',
}
def icon(n): return ICONS[n]

def arrow_badge(cls="arrow-badge"):
    return f'<span class="{cls}" aria-hidden="true">{icon("arrow")}</span>'

def btn(label, href, variant="", arrow=True, big=False, attrs=""):
    cls = "btn" + (f" btn--{variant}" if variant else "") + (" btn--lg" if big else "")
    inner = f'<span>{esc(label)}</span>' + (f'<span class="arrow">{icon("arrow")}</span>' if arrow else "")
    return f'<a class="{cls}" href="{href}" {attrs}>{inner}</a>'

def link_arrow(label, href, attrs=""):
    return f'<a class="link-arrow" href="{href}" {attrs}><span>{esc(label)}</span>{icon("arrow")}</a>'

# ---------------------------------------------------------------- head
FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Montserrat:wght@400;500;600;700&"
         "family=Cormorant+Garamond:ital,wght@0,600;1,600&display=swap")

def head(*, title, meta, url, image=None, jsonld=None, robots=None, prototype=False):
    canonical = SITE["domain"] + url
    og_img = image or og_url("hero/hero-pool-dusk")
    robots_tag = robots or "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    blocks = "".join(
        f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False, separators=(",", ":"))}</script>'
        for b in (jsonld or [])
    )
    return f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(meta)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots_tag}">
<meta name="theme-color" content="#F1EDE4">
<meta name="author" content="{esc(SITE['name'])}">
<meta name="geo.region" content="AE-DU">
<meta name="geo.placename" content="Dubai">
<meta name="geo.position" content="{SITE['geo']['lat']};{SITE['geo']['lng']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE['name'])}">
<meta property="og:locale" content="en_AE">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(meta)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="{esc(SITE['name'])} — {esc(SITE['tagline'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(meta)}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/css/site.css">
<script>(function(){{var r=document.documentElement;r.className+=" js";try{{var t=localStorage.getItem("hst-theme")||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");r.setAttribute("data-theme",t);}}catch(e){{}}}})();</script>
{blocks}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>'''

# ---------------------------------------------------------------- header
def header(active):
    links = []
    for n in NAV:
        cur = ' aria-current="page"' if n["key"] == active else ""
        if n.get("children"):
            sub = "".join(
                f'<a href="{c["url"]}">{esc(c["label"])}'
                f'<small>{esc(next(s["short"] for s in SERVICES if s["key"] == c["key"]))}</small></a>'
                for c in n["children"])
            links.append(
                f'<li class="nav__item"><a class="nav__link" href="{n["url"]}"{cur}>{esc(n["label"])}</a>'
                f'<div class="nav__panel">{sub}</div></li>')
        else:
            links.append(f'<li class="nav__item"><a class="nav__link" href="{n["url"]}"{cur}>{esc(n["label"])}</a></li>')
    return f'''
<header class="header">
  <div class="wrap wrap-wide">
    <div class="header__bar">
      <a class="brand" href="/" aria-label="{esc(SITE['name'])} — home">
        <img src="/assets/img/brand/logo.svg" alt="{esc(SITE['name'])}" width="236" height="134" class="logo-light">
        <img src="/assets/img/brand/logo-light.svg" alt="" width="236" height="134" class="logo-dark" hidden>
      </a>
      <nav class="nav" aria-label="Primary"><ul style="display:flex;align-items:center;gap:.15rem">{"".join(links)}</ul></nav>
      <div class="header__actions">
        <button class="icon-btn theme-toggle" data-theme-toggle type="button" aria-label="Switch to dark theme" aria-pressed="false">{icon("sun")}{icon("moon")}</button>
        <button class="icon-btn burger" data-drawer-open type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">{icon("menu")}</button>
        {btn("Start a project", "/contact/", "accent")}
      </div>
    </div>
  </div>
</header>'''

def drawer(active):
    items = []
    for n in NAV:
        items.append(f'<a href="{n["url"]}">{esc(n["label"])}</a>')
        if n.get("children"):
            sub = "".join(f'<a href="{c["url"]}">{esc(c["label"])}</a>' for c in n["children"])
            items.append(f'<div class="sub">{sub}</div>')
    return f'''
<div class="drawer" id="drawer" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="drawer__top">
    <a class="brand" href="/" aria-label="{esc(SITE['name'])} — home">
      <img src="/assets/img/brand/logo.svg" alt="{esc(SITE['name'])}" width="236" height="134" class="logo-light">
      <img src="/assets/img/brand/logo-light.svg" alt="" width="236" height="134" class="logo-dark" hidden>
    </a>
    <div style="display:flex;gap:.45rem">
      <button class="icon-btn theme-toggle" data-theme-toggle type="button" aria-label="Switch theme">{icon("sun")}{icon("moon")}</button>
      <button class="icon-btn" data-drawer-close type="button" aria-label="Close menu">{icon("close")}</button>
    </div>
  </div>
  <nav class="drawer__nav" aria-label="Mobile">{"".join(items)}</nav>
  <div class="drawer__foot">
    {btn("Start a project", "/contact/", "accent", big=True)}
    <a class="link-arrow" href="tel:{SITE['phone_link']}">{SITE['phone_display']}{icon("arrow")}</a>
  </div>
</div>'''

# ---------------------------------------------------------------- footer
def footer():
    svc_links = "".join(f'<a href="{s["url"]}">{esc(s["title"])}</a>' for s in SERVICES)
    area_links = ", ".join(esc(a) for a in SITE["areas"][:10])
    return f'''
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <img src="/assets/img/brand/logo-light.svg" alt="{esc(SITE['name'])}" width="236" height="134">
        <p>{esc(SITE['short_desc'])}</p>
        <div class="footer__social" style="margin-top:1.5rem">
          <a href="{SITE['socials']['instagram']}" rel="noopener noreferrer nofollow" target="_blank" aria-label="HST Architects on Instagram">{icon("instagram")}</a>
          <a href="https://wa.me/{SITE['phone_link'].lstrip('+')}" rel="noopener noreferrer nofollow" target="_blank" aria-label="Message HST Architects on WhatsApp">{icon("whatsapp")}</a>
        </div>
      </div>
      <div>
        <h3 class="footer__h">Services</h3>
        <nav class="footer__links" aria-label="Services">{svc_links}<a href="/services/">All services</a></nav>
      </div>
      <div>
        <h3 class="footer__h">Studio</h3>
        <nav class="footer__links" aria-label="Studio">
          <a href="/projects/">Projects</a>
          <a href="/about/">About us</a>
          <a href="/contact/">Contact</a>
        </nav>
      </div>
      <div>
        <h3 class="footer__h">Visit the studio</h3>
        <div class="footer__links">
          <span>{esc(SITE['address_line'])}<br>{esc(SITE['address_locality'])}, United Arab Emirates</span>
          <a href="tel:{SITE['phone_link']}">{SITE['phone_display']}</a>
          <a href="tel:{SITE['landline_link']}">{SITE['landline_display']}</a>
          <a href="mailto:{SITE['email']}">{SITE['email']}</a>
          <span class="small" style="opacity:.7">{esc(SITE["hours_display"])}</span>
        </div>
      </div>
    </div>
    <p class="small" style="padding-bottom:1.4rem;opacity:.55;max-width:none">
      Serving {area_links} and the wider UAE.
    </p>
    <div class="footer__bottom">
      <span>&copy; <span data-year>2026</span> {esc(SITE['name'])}, part of {esc(SITE['legal'])}. All rights reserved.</span>
      <span>Interior design &middot; Renovation &amp; fit-out &middot; Landscaping &middot; Dubai, UAE</span>
    </div>
  </div>
</footer>'''

def tail(config_js=True):
    cfg = '<script src="/assets/js/config.js"></script>' if config_js else ""
    return f'''{cfg}<script src="/assets/js/site.js" defer></script>
<script>
(function(){{
 function sync(){{var d=document.documentElement.getAttribute("data-theme")==="dark";
 document.querySelectorAll(".logo-light").forEach(function(e){{e.hidden=d;}});
 document.querySelectorAll(".logo-dark").forEach(function(e){{e.hidden=!d;}});}}
 sync();new MutationObserver(sync).observe(document.documentElement,{{attributes:true,attributeFilter:["data-theme"]}});
}})();
</script>
</body>
</html>'''

# ---------------------------------------------------------------- shared partials
def breadcrumbs(trail):
    """trail = [(label, url|None)] — last item is the current page."""
    out = []
    for i, (label, url) in enumerate(trail):
        if url and i < len(trail) - 1:
            out.append(f'<li><a href="{url}">{esc(label)}</a></li>')
        else:
            out.append(f'<li><span aria-current="page">{esc(label)}</span></li>')
    return f'<nav aria-label="Breadcrumb"><ol class="crumbs">{"".join(out)}</ol></nav>'

def breadcrumb_ld(trail):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": label,
             "item": SITE["domain"] + (url or "")}
            for i, (label, url) in enumerate(trail)
        ],
    }

def faq_block(faqs, heading="Frequently asked questions", intro=None, level="h2"):
    items = []
    for i, f in enumerate(faqs):
        items.append(f'''<div class="faq__item">
  <h3 style="font-size:inherit;font-weight:inherit;letter-spacing:inherit;margin:0">
    <button class="faq__q" type="button" aria-expanded="false" aria-controls="faq-{i}-{abs(hash(f['q']))%9999}">
      <span>{esc(f["q"])}</span><span class="faq__icon" aria-hidden="true"></span>
    </button>
  </h3>
  <div class="faq__a" id="faq-{i}-{abs(hash(f['q']))%9999}"><div>{esc(f["a"])}</div></div>
</div>''')
    lede = f'<p class="lede" style="margin-top:1rem">{esc(intro)}</p>' if intro else ""
    return f'''<section class="section" aria-labelledby="faq-h">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__text">
        <span class="eyebrow">Questions</span>
        <{level} class="h2 split-head" id="faq-h">{esc(heading)}</{level}>
        {lede}
      </div>
    </div>
    <div class="faq reveal">{"".join(items)}</div>
  </div>
</section>'''

def faq_ld(faqs):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f["q"],
             "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in faqs
        ],
    }

def cta_band(title_a, title_b, body, image="services/landscape-roof-garden"):
    return f'''<section class="section">
  <div class="wrap">
    <div class="cta reveal">
      <div class="cta__media">{img(image, "A completed HST Architects roof garden in Dubai, lit at night", sizes="(max-width:900px) 100vw, 1560px")}</div>
      <span class="eyebrow on-dark">Start here</span>
      <h2 class="h1 split-head">{esc(title_a)} <span class="lite" style="color:rgba(255,255,255,.6)">{esc(title_b)}</span></h2>
      <p>{esc(body)}</p>
      <div class="cta__actions">
        {btn("Book a site visit", "/contact/", "light", big=True)}
        {btn("See our work", "/projects/", "outline", big=True)}
      </div>
    </div>
  </div>
</section>'''

def related_block(items, heading="Continue exploring"):
    """items = [(title, subtitle, url)]"""
    cards = "".join(
        f'<a href="{u}"><span><b>{esc(t)}</b><small>{esc(s)}</small></span>{icon("arrow")}</a>'
        for t, s, u in items)
    return f'''<section class="section-sm" aria-labelledby="rel-h">
  <div class="wrap">
    <h2 class="h4" id="rel-h" style="margin-bottom:1.2rem">{esc(heading)}</h2>
    <div class="related reveal">{cards}</div>
  </div>
</section>'''

def org_ld():
    return {
        "@context": "https://schema.org",
        "@type": ["HomeAndConstructionBusiness", "GeneralContractor"],
        "@id": SITE["domain"] + "/#organization",
        "name": SITE["name"],
        "alternateName": SITE["legal"],
        "url": SITE["domain"] + "/",
        "logo": {"@type": "ImageObject", "url": SITE["domain"] + "/assets/img/brand/logo.svg"},
        "image": og_url("hero/hero-pool-dusk"),
        "description": SITE["short_desc"],
        "telephone": SITE["phone_display"],
        "email": SITE["email"],
        "currenciesAccepted": "AED",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": SITE["address_line"],
            "addressLocality": SITE["address_locality"],
            "addressRegion": SITE["address_region"],
            "addressCountry": SITE["address_country"],
        },
        "geo": {"@type": "GeoCoordinates", "latitude": SITE["geo"]["lat"], "longitude": SITE["geo"]["lng"]},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": SITE["hours_days"],
            "opens": SITE["hours_open"],
            "closes": SITE["hours_close"],
        }],
        "areaServed": [{"@type": "City", "name": a} for a in SITE["areas"]],
        "sameAs": [SITE["socials"]["instagram"]],
        "knowsAbout": [
            "Interior design", "Interior fit-out", "Villa renovation", "Office fit-out",
            "Landscape design", "Swimming pool construction", "Joinery and millwork",
            "MEP services", "Annual maintenance contracts", "3D visualisation",
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Design and build services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {
                    "@type": "Service", "name": s["title"], "description": s["short"],
                    "url": SITE["domain"] + s["url"]}}
                for s in SERVICES
            ],
        },
    }

def website_ld():
    return {
        "@context": "https://schema.org", "@type": "WebSite",
        "@id": SITE["domain"] + "/#website",
        "url": SITE["domain"] + "/",
        "name": SITE["name"],
        "description": SITE["short_desc"],
        "inLanguage": "en-AE",
        "publisher": {"@id": SITE["domain"] + "/#organization"},
    }
