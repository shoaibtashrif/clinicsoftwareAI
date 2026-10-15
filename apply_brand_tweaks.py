"""Apply ClinicSoftware-owned branding without rerunning the content conversion."""
from pathlib import Path
import os
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "www.lassomd.com"

for page in SITE.rglob("*.html"):
    soup = BeautifulSoup(page.read_text(errors="ignore"), "html.parser")
    for node in list(soup.find_all(string=True)):
        if node.parent and node.parent.name in {"script", "style", "svg"}:
            continue
        value = str(node).replace("PatientLoop™ Growth Software", "ClinicSoftware AI Platform")
        value = value.replace("PatientLoop Growth Software", "ClinicSoftware AI Platform")
        value = value.replace("PatientLoop™", "ClinicSoftware")
        value = value.replace("PatientLoop", "ClinicSoftware")
        value = value.replace("Lasso MD", "ClinicSoftware.ai")
        value = value.replace("LassoMD", "ClinicSoftware.ai")
        if value != str(node):
            node.replace_with(value)
    logo_path = os.path.relpath(SITE / "clinicsoftware-logo.svg", page.parent).replace(os.sep, "/")
    mark_path = os.path.relpath(SITE / "clinicsoftware-mark.svg", page.parent).replace(os.sep, "/")
    favicon_path = os.path.relpath(SITE / "clinicsoftware-favicon.svg", page.parent).replace(os.sep, "/")
    for brand in soup.select(".navbar_brand"):
        image = brand.select_one("img.navbar_logo")
        if image:
            image["src"] = logo_path
            image["alt"] = "ClinicSoftware.ai"
    for brand in soup.select(".footer_brand"):
        brand.clear()
        image = soup.new_tag("img", src=logo_path, alt="ClinicSoftware.ai")
        image["class"] = ["clinicsoftware-footer-logo"]
        brand.append(image)
    for image in soup.select(".lasso-abs-box img"):
        image["src"] = mark_path
        image["alt"] = "ClinicSoftware.ai"
        image.attrs.pop("srcset", None)
        image.attrs.pop("sizes", None)
    for anchor in soup.select('a[href*="lassomd"], a[href*="LassoMD"]'):
        anchor["href"] = os.path.relpath(SITE / "contact.html", page.parent).replace(os.sep, "/")
        anchor.attrs.pop("target", None)
    for icon in soup.select('link[rel="shortcut icon"], link[rel="apple-touch-icon"]'):
        icon["href"] = favicon_path
    page.write_text(str(soup), encoding="utf-8")

print(f"Applied ClinicSoftware branding to {len(list(SITE.rglob('*.html')))} pages")
