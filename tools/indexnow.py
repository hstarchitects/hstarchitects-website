# -*- coding: utf-8 -*-
"""Tell the IndexNow search engines that pages here have changed.

IndexNow is a push notification instead of a wait. One POST reaches Bing, Yandex,
Seznam and Naver at once, so a new project page can be crawled in hours rather
than whenever the crawler next comes round. Google does not participate, and
neither does Brave; those still rely on the sitemap.

Ownership is proved by the key file the build writes to the site root, so this
only works once that file is deployed.

    python tools/indexnow.py                 # every URL in sitemap.xml
    python tools/indexnow.py /projects/x/    # just these paths
    python tools/indexnow.py --dry-run
"""
import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import SITE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://api.indexnow.org/IndexNow"
HOST = SITE["domain"].replace("https://", "")


def sitemap_urls():
    tree = ET.parse(os.path.join(ROOT, "sitemap.xml"))
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [e.text.strip() for e in tree.getroot().findall(".//s:loc", ns) if e.text]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv

    if args:
        urls = [a if a.startswith("http") else SITE["domain"] + a for a in args]
    else:
        urls = sitemap_urls()

    if not urls:
        sys.exit("nothing to submit")
    # The endpoint accepts 10,000 per request; this site is nowhere near that.
    payload = {
        "host": HOST,
        "key": SITE["indexnow_key"],
        "keyLocation": f"{SITE['domain']}/{SITE['indexnow_key']}.txt",
        "urlList": urls,
    }

    print(f"{len(urls)} URL(s) -> {ENDPOINT}")
    for u in urls:
        print("  " + u)
    if dry:
        print("dry run, nothing sent")
        return

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            # 200 accepted, 202 accepted but the key is still being verified.
            print(f"OK  HTTP {r.status}")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        sys.exit(f"HTTP {e.code}: {detail}")


if __name__ == "__main__":
    main()
