# -*- coding: utf-8 -*-
"""Prototype B — "Atelier" shell.

Same content and page structure as prototype A, a deliberately different visual
system: a fixed vertical nav rail, serif display type, hairline rules instead of
filled cards, and a dark-first palette.
"""
import json
from content import SITE, NAV, SERVICES
from layout import (esc, img, img_url, icon, ICONS, arrow_badge, breadcrumbs,   # noqa: F401
                    breadcrumb_ld, faq_ld, org_ld, website_ld, ROOT, MANIFEST)  # noqa: F401

PREFIX = "/prototype-b"

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Montserrat:wght@400;500;600;700&"
         "family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap")


def btn(label, href, variant="", arrow=True, big=False, attrs=""):
    cls = "btn" + (f" btn--{variant}" if variant else "") + (" btn--lg" if big else "")
    inner = f'<span>{esc(label)}</span>' + (f'<i class="btn__ic" aria-hidden="true">{icon("arrow")}</i>' if arrow else "")
    return f'<a class="{cls}" href="{href}" {attrs}>{inner}</a>'


def link_arrow(label, href, attrs=""):
    return f'<a class="link-arrow" href="{href}" {attrs}><span>{esc(label)}</span>{icon("arrow")}</a>'


def head(*, title, meta, url, image=None, jsonld=None, robots=None, prototype=True):
    """Prototype B is a design preview: always noindex so it cannot compete with the live site."""
    og_img = image or img_url("hero/hero-architecture-dark", 800)
    return f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)} — Prototype B</title>
<meta name="description" content="{esc(meta)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0B0F14">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(meta)}">
<meta property="og:image" content="{og_img}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/css/site-b.css">
<script>(function(){{try{{var t=localStorage.getItem("hst-theme-b")||"dark";document.documentElement.setAttribute("data-theme",t);}}catch(e){{}}}})();</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="proto-flag">Prototype&nbsp;B &mdash; Atelier &middot; <a href="/">see Prototype&nbsp;A</a></div>'''


def rail(active):
    items = []
    for i, n in enumerate(NAV):
        cur = ' aria-current="page"' if n["key"] == active else ""
        items.append(
            f'<li><a href="{PREFIX}{n["url"]}"{cur}>'
            f'<span class="rail__n">{i+1:02d}</span><span class="rail__t">{esc(n["label"])}</span></a></li>')
    return f'''
<aside class="rail" aria-label="Primary">
  <a class="rail__brand" href="{PREFIX}/" aria-label="{esc(SITE['name'])} — home">
    <img src="/assets/img/brand/logo-light.svg" alt="{esc(SITE['name'])}" width="236" height="134">
  </a>
  <nav class="rail__nav"><ul>{"".join(items)}</ul></nav>
  <div class="rail__foot">
    <button class="rail__toggle" data-theme-toggle type="button" aria-label="Switch theme" aria-pressed="true">{icon("sun")}{icon("moon")}</button>
    <a class="rail__tel" href="tel:{SITE['phone_link']}">{esc(SITE['phone_display'])}</a>
  </div>
</aside>

<header class="topbar">
  <a class="topbar__brand" href="{PREFIX}/" aria-label="{esc(SITE['name'])} — home">
    <img src="/assets/img/brand/logo-light.svg" alt="{esc(SITE['name'])}" width="236" height="134">
  </a>
  <div style="display:flex;gap:.5rem">
    <button class="icon-btn" data-theme-toggle type="button" aria-label="Switch theme">{icon("sun")}{icon("moon")}</button>
    <button class="icon-btn" data-drawer-open type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">{icon("menu")}</button>
  </div>
</header>'''


def drawer(active):
    items = []
    for n in NAV:
        items.append(f'<a href="{PREFIX}{n["url"]}">{esc(n["label"])}</a>')
        if n.get("children"):
            sub = "".join(f'<a href="{PREFIX}{c["url"]}">{esc(c["label"])}</a>' for c in n["children"])
            items.append(f'<div class="sub">{sub}</div>')
    return f'''
<div class="drawer" id="drawer" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="drawer__top">
    <img src="/assets/img/brand/logo-light.svg" alt="{esc(SITE['name'])}" width="236" height="134" style="height:44px;width:auto">
    <button class="icon-btn" data-drawer-close type="button" aria-label="Close menu">{icon("close")}</button>
  </div>
  <nav class="drawer__nav" aria-label="Mobile">{"".join(items)}</nav>
  <div class="drawer__foot">
    {btn("Start a project", PREFIX + "/contact/", "accent", big=True)}
    <a class="link-arrow" href="tel:{SITE['phone_link']}">{esc(SITE['phone_display'])}{icon("arrow")}</a>
  </div>
</div>'''


def footer():
    svc_links = "".join(f'<a href="{PREFIX}{s["url"]}">{esc(s["title"])}</a>' for s in SERVICES)
    return f'''
<footer class="footer">
  <div class="shell">
    <div class="footer__lead">
      <span class="eyebrow">Say hello</span>
      <p class="footer__big">Let us look at<br>the space.</p>
      <a class="footer__mail" href="mailto:{SITE['email']}">{SITE['email']}</a>
    </div>
    <div class="footer__cols">
      <div><h4>Services</h4><nav class="footer__links">{svc_links}</nav></div>
      <div><h4>Studio</h4><nav class="footer__links">
        <a href="{PREFIX}/projects/">Projects</a><a href="{PREFIX}/about/">About</a><a href="{PREFIX}/contact/">Contact</a>
      </nav></div>
      <div><h4>Visit</h4><div class="footer__links">
        <span>{esc(SITE['address_line'])}<br>{esc(SITE['address_locality'])}, UAE</span>
        <a href="tel:{SITE['phone_link']}">{esc(SITE['phone_display'])}</a>
        <a href="tel:{SITE['landline_link']}">{esc(SITE['landline_display'])}</a>
      </div></div>
      <div><h4>Follow</h4><div class="footer__links">
        <a href="{SITE['socials']['instagram']}" rel="noopener nofollow" target="_blank">Instagram</a>
        <a href="{SITE['socials']['linkedin']}" rel="noopener nofollow" target="_blank">LinkedIn</a>
        <a href="https://wa.me/{SITE['phone_link'].lstrip('+')}" rel="noopener nofollow" target="_blank">WhatsApp</a>
      </div></div>
    </div>
    <div class="footer__bottom">
      <span>&copy; <span data-year>2026</span> {esc(SITE['name'])}, part of {esc(SITE['legal'])}</span>
      <span>Interior design &middot; Renovation &amp; fit-out &middot; Landscaping &middot; Dubai</span>
    </div>
  </div>
</footer>'''


def tail(config_js=True):
    cfg = '<script src="/assets/js/config.js"></script>' if config_js else ""
    return f'''{cfg}<script src="/assets/js/site.js" defer></script>
<script>
/* prototype B keeps its own theme preference so it can be compared side by side */
(function(){{
 var r=document.documentElement;
 function set(t){{r.setAttribute("data-theme",t);try{{localStorage.setItem("hst-theme-b",t);}}catch(e){{}}}}
 document.addEventListener("click",function(e){{
   if(!e.target.closest("[data-theme-toggle]"))return;
   e.stopImmediatePropagation();
   set(r.getAttribute("data-theme")==="dark"?"light":"dark");
 }},true);
}})();
</script>
</body>
</html>'''
