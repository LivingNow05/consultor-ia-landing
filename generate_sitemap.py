#!/usr/bin/env python3
"""
generate_sitemap.py
Genera sitemap.xml a partir de todos los archivos HTML en dist/
"""

import os
import re
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, ElementTree, indent

BASE_URL = "https://consultor-ia.com.co"
DIST_DIR = "dist"
OUTPUT_SITEMAP = os.path.join(DIST_DIR, "sitemap.xml")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Priority & changefreq by path depth
def get_priority_and_freq(path):
    """Assign SEO priority based on URL depth."""
    depth = path.strip("/").count("/")
    if depth == 0:          # Homepage
        return "1.0", "daily"
    elif depth == 1:        # Hub de industria / hub de pais
        return "0.9", "weekly"
    elif depth == 2:        # Sub-hub de pais / pillar
        return "0.8", "weekly"
    else:                   # Landing programática
        return "0.7", "monthly"

urls = []

for root, dirs, files in os.walk(DIST_DIR):
    for file in files:
        if file != "index.html":
            continue
        full_path = os.path.join(root, file)
        # Convert dist/foo/bar/index.html -> /foo/bar/
        rel_path = os.path.relpath(full_path, DIST_DIR)
        # Remove index.html suffix
        url_path = rel_path.replace("index.html", "").replace("\\", "/")
        if not url_path.startswith("/"):
            url_path = "/" + url_path

        full_url = BASE_URL + url_path
        priority, freq = get_priority_and_freq(url_path)
        urls.append((full_url, TODAY, freq, priority))

# Sort: homepage first, then by priority desc, then alpha
urls.sort(key=lambda x: (float(x[3]) * -1, x[0]))

print(f"✅ Total URLs encontradas: {len(urls)}")

# Build XML
urlset = Element("urlset")
urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
urlset.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
urlset.set("xsi:schemaLocation",
           "http://www.sitemaps.org/schemas/sitemap/0.9 "
           "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")

for full_url, lastmod, changefreq, priority in urls:
    url_el = SubElement(urlset, "url")
    SubElement(url_el, "loc").text = full_url
    SubElement(url_el, "lastmod").text = lastmod
    SubElement(url_el, "changefreq").text = changefreq
    SubElement(url_el, "priority").text = priority

indent(urlset, space="  ")
tree = ElementTree(urlset)

with open(OUTPUT_SITEMAP, "wb") as f:
    f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
    tree.write(f, encoding="utf-8", xml_declaration=False)

print(f"✅ Sitemap generado en: {OUTPUT_SITEMAP}")

# Also dump URLs to a text file for the indexing script
url_list_path = "all_urls.txt"
with open(url_list_path, "w", encoding="utf-8") as f:
    for full_url, *_ in urls:
        f.write(full_url + "\n")
print(f"✅ Lista de URLs exportada a: {url_list_path} ({len(urls)} líneas)")
