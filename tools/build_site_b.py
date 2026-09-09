# -*- coding: utf-8 -*-
"""Generate Prototype B at /prototype-b/.

Same content model and same page set as the live site, wrapped in a different
shell (tools/layout_b.py) and styled by assets/css/site-b.css. Running this after
build_site.py keeps both directions in step, so the two can be compared on
identical copy rather than on different words.

    python tools/build_site.py && python tools/build_site_b.py
"""
import os, re, sys, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build_site as B
import layout_b as LB
from layout import ROOT

PREFIX = "prototype-b"

# ---------------------------------------------------------------------------
# Swap the shell. build_site.py bound these names at import time, so they are
# rebound on its module globals rather than on the layout module.
# ---------------------------------------------------------------------------
B.head = LB.head
B.header = LB.sidebar
B.drawer = LB.drawer
B.footer = LB.footer
B.tail = LB.tail
B.btn = LB.btn
B.link_arrow = LB.link_arrow

# Section helpers live in layout.py and build their own markup from these names.
import layout as L
L.btn = LB.btn
L.link_arrow = LB.link_arrow

_ASSET_OR_PROTO = re.compile(r'href="/(?!assets/|favicon|apple-touch|site\.webmanifest|robots|sitemap|llms|' + PREFIX + r'/)')


def _rewrite(html_str):
    """Point every internal link at the prototype, leaving shared assets alone."""
    return _ASSET_OR_PROTO.sub(f'href="/{PREFIX}/', html_str)


_written = []


def write(path, html_str, url=None, prio="0.6", freq="monthly"):
    full = os.path.join(ROOT, PREFIX, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(_rewrite(html_str))
    _written.append("/" + PREFIX + (url or "/" + path))
    # keep build_site's own URL list intact so its sitemap logic still works
    if url is not None:
        B.URLS.append((url, prio, freq))


B.write = write


def main():
    out = os.path.join(ROOT, PREFIX)
    if os.path.isdir(out):
        shutil.rmtree(out)

    B.build_home()
    B.build_services_index()
    for s in B.SERVICES:
        B.build_service(s)
    B.build_projects_index()
    for i, p in enumerate(B.PROJECTS):
        B.build_project(p,
                        B.PROJECTS[i - 1] if i else None,
                        B.PROJECTS[i + 1] if i + 1 < len(B.PROJECTS) else None)
    B.build_about()
    B.build_contact()

    print(f"Prototype B: {len(_written)} pages under /{PREFIX}/")
    for u in _written:
        print("  ", u)


if __name__ == "__main__":
    main()
