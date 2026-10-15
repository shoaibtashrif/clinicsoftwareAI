"""Create ClinicSoftware-branded local routes for the external template selector."""
from pathlib import Path
from urllib.parse import urlparse
import re

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "www.lassomd.com"
PORTFOLIO = SITE / "dental-marketing/website-design/website-design-portfolio.html"
SOURCE_HOST = "template-theme-selector.webflow.io"

soup = BeautifulSoup(PORTFOLIO.read_text(errors="ignore"), "html.parser")
cards = []
for anchor in soup.select(f'a[href*="{SOURCE_HOST}/versions/"],a[href*="template-previews/"]'):
    current = anchor.get("href", "")
    slug = urlparse(current).path.rstrip("/").split("/")[-1]
    if not slug:
        continue
    source = f"https://{SOURCE_HOST}/versions/{slug}"
    name = " ".join(anchor.get_text(" ", strip=True).split())
    words = name.split()
    if len(words) % 2 == 0 and words[:len(words)//2] == words[len(words)//2:]:
        name = " ".join(words[:len(words)//2])
    anchor["href"] = f"../../../template-previews/{slug}/"
    anchor["target"] = "_blank"
    cards.append((slug, source, name or slug.replace("-", " ").title()))

PORTFOLIO.write_text(str(soup), encoding="utf-8")

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 ClinicSoftware preview builder"
for slug, (source, name) in dict((slug, (source, name)) for slug, source, name in cards).items():
    response = session.get(source, timeout=25)
    response.raise_for_status()
    page = BeautifulSoup(response.text, "html.parser")
    if page.title:
        page.title.string = f"{name} | ClinicSoftware.ai Website Preview"
    for icon in page.select('link[rel="shortcut icon"],link[rel="icon"],link[rel="apple-touch-icon"]'):
        icon.decompose()
    favicon = page.new_tag("link", rel="icon", href="/clinicsoftware-favicon.svg", type="image/svg+xml")
    page.head.append(favicon)
    color = page.new_tag("meta", attrs={"name": "theme-color", "content": "#0b0b0d"})
    page.head.append(color)
    for anchor in page.select('a[href*="lassomd.com"],a[href*="LassoMD"]'):
        anchor["href"] = "/dental-marketing/website-design/website-design-portfolio.html"
        anchor.attrs.pop("target", None)
    brand = page.select_one(".lasso-logo-wrapper")
    if brand:
        brand.clear()
        brand["href"] = "/"
        brand.attrs.pop("target", None)
        logo = page.new_tag("img", src="/clinicsoftware-logo.svg", alt="ClinicSoftware.ai")
        logo["style"] = "display:block;width:150px;height:auto"
        brand.append(logo)
    brand_style = page.new_tag("style")
    brand_style.string = """
      .lasso-logo-wrapper{display:flex!important;align-items:center!important;background:#0b0b0d!important;border-radius:9px!important;padding:7px 12px!important;width:auto!important;height:auto!important}
      .w-webflow-badge{display:none!important}
    """
    page.head.append(brand_style)
    destination = SITE / "template-previews" / slug / "index.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(str(page), encoding="utf-8")

print(f"Built {len(set(slug for slug, _, _ in cards))} branded template previews")
