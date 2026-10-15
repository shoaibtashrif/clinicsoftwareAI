"""Apply ClinicSoftware content to the downloaded Webflow mirror.

The script keeps the downloaded DOM, classes, layout and media structure. It only
changes copy/branding, disables third-party lead forms and adds the existing Ava
embed. Run once against a fresh HTTrack mirror.
"""

from pathlib import Path
from urllib.parse import urlparse
import os
import re

from bs4 import BeautifulSoup, NavigableString


ROOT = Path(__file__).resolve().parent
SITE = ROOT / "www.lassomd.com"


REPLACEMENTS = [
    ("Lasso MD", "ClinicSoftware.ai"),
    ("LassoMD", "ClinicSoftware.ai"),
    ("ClinicSoftware MD", "ClinicSoftware.ai"),
    ("Lasso’s", "ClinicSoftware.ai’s"),
    ("Lasso's", "ClinicSoftware.ai's"),
    ("Lasso", "ClinicSoftware"),
    ("dental marketing agencies", "clinic website providers"),
    ("Dental Marketing Agencies", "Clinic Website Providers"),
    ("dental marketing agency", "clinic website partner"),
    ("Dental Marketing Agency", "Clinic Website Partner"),
    ("dental marketing", "clinic growth"),
    ("Dental Marketing", "Clinic Growth"),
    ("dental websites", "clinic websites"),
    ("Dental Websites", "Clinic Websites"),
    ("dental website", "clinic website"),
    ("Dental Website", "Clinic Website"),
    ("dental practices", "independent clinics"),
    ("Dental Practices", "Independent Clinics"),
    ("dental practice", "independent clinic"),
    ("Dental Practice", "Independent Clinic"),
    ("dental patients", "patients"),
    ("Dental Patients", "Patients"),
    ("dentists", "clinic teams"),
    ("Dentists", "Clinic Teams"),
    ("dentist", "clinician"),
    ("Dentist", "Clinician"),
    ("dentistry", "healthcare"),
    ("Dentistry", "Healthcare"),
    ("dental", "clinic"),
    ("Dental", "Clinic"),
    ("patients/month", "patient opportunities"),
    ("Pricing", "Specialties"),
    ("Blog", "Resources"),
    ("Book a Demo", "Request a Mock-up"),
    ("Schedule Demo", "Request a Mock-up"),
    ("Schedule a Discovery Call", "Request a Clinic Mock-up"),
    ("Contact Sales", "Request a Mock-up"),
    ("Contact Support", "Project Support"),
    ("Marketing Software", "AI Reception & Scheduling"),
    ("Lead Tracking", "AI Receptionist"),
    ("Lead Generation", "AI Reception"),
    ("Lead Management", "Managed Updates"),
    ("Calls Management", "Patient Conversations"),
    ("ROI Tracking", "Journey Insights"),
    ("Transparent Specialties", "Clinic Solutions"),
    ("3X ROI Guarantee", "Managed Growth Approach"),
    ("3x ROI Guarantee", "Managed Growth Approach"),
    ("888-448-8149", "AI Reception"),
    ("8884488149", ""),
    ("sales@lassomd.com", "hello@clinicsoftware.ai"),
    ("billing@lassomd.com", "support@clinicsoftware.ai"),
    ("partner@lassomd.com", "partners@clinicsoftware.ai"),
    ("cs@lassomd.com", "support@clinicsoftware.ai"),
    ("help@lassomd.com", "support@clinicsoftware.ai"),
    ("www.lassomd.com", "clinicsoftware.ai"),
    ("Schedule a Discovery\u00a0Call", "Request a Clinic Mock-up"),
    ("See More ClinicSoftware.ai Reviews", "Explore ClinicSoftware features"),
]


HEADINGS = {
    "index.html": ("Modern clinic websites and AI reception", "Turn website visits into", "clear patient action."),
    "company.html": ("About ClinicSoftware.ai", "A modern digital front door for", "independent healthcare."),
    "company/customer-reviews.html": ("Website directions", "Modern clinic experiences built to", "earn patient trust."),
    "company/lasso-md-process.html": ("Our process", "From practice information to a", "launch-ready clinic website."),
    "company/our-philosophy.html": ("Our philosophy", "Useful technology should make care", "easier to access."),
    "dental-marketing.html": ("Clinic website platform", "Websites, AI reception and scheduling", "working as one."),
    "dental-marketing/website-design.html": ("Clinic website design", "Clinic websites that establish your", "digital foundation."),
    "dental-marketing/website-design/website-design-portfolio.html": ("Website preview library", "Explore modern website directions for", "independent clinics."),
    "dental-marketing/website-design/rapidlaunch-showcase.html": ("RapidLaunch previews", "Strong clinic website directions", "ready to personalize."),
    "dental-marketing/creative-branding.html": ("Clinic branding", "A visual identity patients can", "recognize and trust."),
    "dental-marketing/creative-branding/logo-showcase.html": ("Identity preview library", "Distinct clinic brands built for", "real-world use."),
    "dental-marketing/video-photo.html": ("Video and photography", "Make the practice feel familiar", "before the first visit."),
    "dental-marketing/video-photo/the-creator-network.html": ("Clinic creator network", "Simple visual production for", "modern medical websites."),
    "dental-marketing/dental-seo.html": ("Local clinic search", "Help nearby patients find and", "understand your practice."),
    "dental-marketing/social-media-marketing.html": ("Clinic social content", "Keep the practice visible with", "clear, useful content."),
    "dental-marketing/dental-google-ads.html": ("Campaign landing pages", "Turn paid attention into", "qualified patient action."),
    "dental-marketing-software/lead-tracking.html": ("AI virtual reception", "A helpful front desk inside", "every clinic website."),
    "dental-marketing-software/calls-management.html": ("Patient conversations", "Give every question a clear", "next step."),
    "dental-marketing-software/roi-tracking.html": ("Journey insights", "Understand how visitors become", "scheduled patients."),
    "dental-marketing-software/online-scheduling.html": ("Scheduling connections", "Make booking easy from", "every patient pathway."),
    "pricing.html": ("Medical specialties", "One flexible platform for", "many kinds of care."),
    "case-studies.html": ("Clinic website previews", "See how the platform adapts to", "different practices."),
    "help-center.html": ("ClinicSoftware resources", "Practical guidance for a better", "digital patient experience."),
    "blog.html": ("ClinicSoftware insights", "Ideas for modern clinic websites and", "patient access."),
    "contact-sales.html": ("Request a clinic mock-up", "See what your clinic’s next website", "could look like."),
    "contact-support.html": ("Project support", "Help with your ClinicSoftware", "website and assistant."),
    "contact.html": ("Contact ClinicSoftware.ai", "Let’s talk about your clinic’s", "digital front door."),
    "work-with-us.html": ("Work with ClinicSoftware", "Build better digital experiences for", "independent healthcare."),
    "work-with-us/partners.html": ("Partner network", "Bring modern clinic websites and AI reception", "to your network."),
    "work-with-us/referral-program.html": ("Referral network", "Help clinics move toward a better", "patient experience."),
}


PAGE_DESCRIPTIONS = {
    "index.html": "Modern managed clinic websites with AI reception, scheduling connections and ongoing content support.",
    "pricing.html": "Website and AI reception solutions for dental, optometry, chiropractic and independent medical practices.",
    "contact-sales.html": "Request a focused ClinicSoftware website mock-up for your practice.",
}


def replace_terms(value: str) -> str:
    for old, new in REPLACEMENTS:
        value = value.replace(old, new)
    value = re.sub(r"over\s+700\s+(?:independent clinics|practices)", "independent healthcare practices", value, flags=re.I)
    value = re.sub(r"700\+?\s+(?:independent clinics|practices)", "independent healthcare practices", value, flags=re.I)
    value = value.replace("predictable, repeatable, & measurable new patient revenue streams", "a clear journey from discovery to scheduling")
    value = value.replace("predictable, repeatable, &amp; measurable new patient revenue streams", "a clear journey from discovery to scheduling")
    return value


def set_heading(soup: BeautifulSoup, eyebrow: str, lead: str, accent: str) -> None:
    h1 = soup.find("h1")
    if not h1:
        return
    h1.clear()
    h1.append(NavigableString(lead + " "))
    span = soup.new_tag("span")
    span["class"] = ["text-color-purple"]
    span.string = accent
    h1.append(span)
    crumb = soup.select_one(".bcrumb-current")
    if crumb:
        crumb.string = eyebrow


def local_href(page: Path, target: str) -> str:
    return os.path.relpath(SITE / target, page.parent).replace(os.sep, "/")


def customize_page(page: Path) -> None:
    relative = page.relative_to(SITE).as_posix()
    soup = BeautifulSoup(page.read_text(errors="ignore"), "html.parser")
    html = soup.find("html")
    for node in list(soup.find_all(string=True)):
        if "Mirrored from" in str(node) and "HTTrack Website Copier" in str(node):
            node.extract()
            continue
        if node.parent and node.parent.name in {"script", "style", "svg"}:
            continue
        changed = replace_terms(str(node))
        if changed != str(node):
            node.replace_with(NavigableString(changed))

    for tag in soup.find_all(True):
        for attr in ("title", "alt", "aria-label", "content"):
            if isinstance(tag.get(attr), str):
                tag[attr] = replace_terms(tag[attr])
        for attr in ("href", "src"):
            value = tag.get(attr)
            if isinstance(value, str) and "lassomd.com" in value:
                tag[attr] = value.replace("www.lassomd.com", "clinicsoftware.ai").replace("lassomd.com", "clinicsoftware.ai")

    heading = HEADINGS.get(relative)
    if heading:
        set_heading(soup, *heading)

    title = soup.find("title")
    page_name = heading[0] if heading else replace_terms(title.get_text(" ", strip=True) if title else "ClinicSoftware.ai")
    if title:
        title.string = f"{page_name} | ClinicSoftware.ai"
    description = soup.find("meta", attrs={"name": "description"})
    if description:
        description["content"] = PAGE_DESCRIPTIONS.get(relative, "Modern clinic websites, AI reception and scheduling connections for independent healthcare practices.")

    for anchor in soup.find_all("a"):
        href = anchor.get("href", "")
        if href.startswith("tel:"):
            anchor["href"] = local_href(page, "dental-marketing-software/calls-management.html")
        if "patientloop.com" in href:
            anchor["href"] = local_href(page, "dental-marketing-software/lead-tracking.html")
            anchor.attrs.pop("target", None)
        if href.endswith("blog.html"):
            for text_node in anchor.select(".nav-link-text"):
                text_node.string = "Insights"
            if anchor.get_text(" ", strip=True) == "Resources":
                anchor.string = "Insights"
        if href.endswith("contact-sales.html") and "nav-link" in anchor.get("class", []) and "button" not in anchor.get("class", []):
            for text_node in anchor.select(".nav-link-text"):
                text_node.string = "Start"

    if relative == "index.html":
        h1 = soup.find("h1")
        if h1:
            h1.clear()
            h1.append(NavigableString("Modern clinic websites that turn visits into "))
            accent = soup.new_tag("span")
            accent["class"] = ["text-color-purple"]
            accent.string = "patient action."
            h1.append(accent)
            h1.append(soup.new_tag("br"))
            sub = soup.new_tag("span")
            sub["class"] = ["homepage-h3-copy"]
            sub.string = "Managed websites, AI reception and scheduling connections for independent healthcare practices."
            h1.append(sub)
        trust_heading = soup.select_one(".homepage-h2")
        if trust_heading:
            trust_heading.clear()
            trust_heading.append(NavigableString("A complete digital front door for "))
            strong = soup.new_tag("span")
            strong["class"] = ["text-color-violet"]
            strong.string = "independent healthcare"
            trust_heading.append(strong)
            trust_heading.append(soup.new_tag("br"))
            small = soup.new_tag("span")
            small["class"] = ["homepage-h3"]
            small.string = "website, patient guidance and scheduling working together"
            trust_heading.append(small)
        for section_heading in soup.find_all("h2"):
            if section_heading.get_text(" ", strip=True).startswith("The Future of Clinic Growth"):
                section_heading.clear()
                section_heading.append(NavigableString("A connected platform for the "))
                highlight = soup.new_tag("span")
                highlight["class"] = ["text-color-violet"]
                highlight.string = "complete patient journey"
                section_heading.append(highlight)
        home_copy = {
            "Start your journey with a website": "Start with a clinic website patients can understand and trust.",
            "We handle the nitty-gritty": "We build a modern, responsive website around the practice’s services, people, locations and patient journey.",
            "Website Collections & Recent Work": "Explore Website Previews",
            "Establish your brand identity": "Give the practice a clear and memorable visual identity.",
            "Success with online marketing": "Typography, color, imagery and voice work together to make the practice recognizable across every patient touchpoint.",
            "Upgrade your online marketing": "Show the people and place behind the practice with photos and video.",
            "Elevate your practice's image": "Use polished clinic photography, provider portraits and short video moments to make the first visit feel more familiar.",
            "Achieve new patient revenue goals": "Help nearby patients discover and understand the care you provide.",
            "Our game plan is simple": "Service and location pages, useful content and a sound technical foundation make the clinic easier to find and evaluate.",
            "Schedule more leads and track ROI": "Keep the website and virtual receptionist current as the practice changes.",
            "Skip the hassle of old-school analytics": "Staff updates, new services, campaign pages and approved assistant knowledge can be managed through one ongoing workflow.",
            "Give modern patients what they want": "Connect every patient pathway to simple online scheduling.",
            "You call the shots on available slots": "Use the scheduling platform the clinic already trusts, with distinct routes for new patients, existing patients and general questions.",
            "Schedule a 15 minute discovery call": "Request a focused clinic website mock-up.",
            "During this 15-minute call": "Share the current site, specialty and location. We’ll prepare a concrete visual direction for the conversation.",
            "Integrate Your Patient Database": "Connect the scheduling tools you already use",
            "ClinicSoftware.ai Clinic Growth FAQ": "ClinicSoftware.ai website and AI reception questions",
            "Why is ClinicSoftware.ai the best": "What does ClinicSoftware.ai manage?",
            "What sets ClinicSoftware.ai apart": "ClinicSoftware.ai manages the patient-facing website, approved virtual receptionist knowledge and scheduling connections as one service.",
            "How much should a independent clinic spend": "Can the website connect to our current scheduler?",
            "Investing in your practice's growth": "Yes. The preferred approach is to connect the scheduling experience the clinic already uses rather than replace it.",
            "What are the best ways to get new patients": "How does the AI receptionist answer questions?",
            "Visibility is just the start": "It uses clinic-approved information such as hours, services, first-visit expectations, policies and scheduling instructions to produce natural answers.",
            "Do I need to use custom photos": "Can we launch before filming clinic-specific video?",
            "Yes, and here's why": "Yes. A preview can use appropriate stock media and later replace it with simple clinic photography or short, professionally edited phone footage.",
            "How can I check if my marketing company": "Does ClinicSoftware store clinical records?",
            "With ClinicSoftware.ai, you'll never be in the dark": "No. The platform is a public marketing, information and scheduling layer. Clinical records remain in the clinic’s established systems.",
            "What is clinic growth and why": "Which types of clinics can use the platform?",
            "Clinic marketing is the strategic use": "The core system supports dental, optometry, chiropractic, physical therapy and a broad range of independent specialty practices.",
            "How do I choose the right clinic growth company": "Can each clinic have a different visual direction?",
            "Look for a clinic-specific agency": "Yes. Shared production components make delivery efficient while typography, color, imagery, video, copy and page composition adapt to the practice.",
            "What results should I expect": "How quickly can a practice see a mock-up?",
            "Within the first 30": "The system is designed to produce a focused prospect direction within days after receiving the current website and basic practice information.",
            "Does ClinicSoftware.ai integrate with my Practice Management Software": "What happens after the website launches?",
            "Yes. PatientLoop": "ClinicSoftware can manage routine content changes, new landing pages and virtual receptionist knowledge updates as the practice evolves.",
        }
        for node in list(soup.find_all(string=True)):
            current = " ".join(str(node).split())
            for prefix, replacement in home_copy.items():
                if current.startswith(prefix):
                    node.replace_with(NavigableString(replacement))
                    break
        clean_home_headings = {
            "Start with a clinic website": "Start with a clinic website patients can understand and trust.",
            "Give the practice a clear and memorable": "Give the practice a clear and memorable visual identity.",
            "Show the people and place": "Show the people and place behind the practice with photos and video.",
            "Help nearby patients": "Help nearby patients discover and understand the care you provide.",
            "Keep the website and virtual receptionist": "Keep the website and virtual receptionist current as the practice changes.",
            "Connect every patient pathway": "Connect every patient pathway to simple online scheduling.",
            "Request a focused clinic website mock-up": "Request a focused clinic website mock-up.",
            "Schedule a 15 minute discovery call": "Request a focused clinic website mock-up.",
            "Connect the scheduling tools": "Connect the scheduling tools you already use.",
            "Integrate Your Patient Database": "Connect the scheduling tools you already use.",
            "ClinicSoftware.ai Clinic Growth FAQ": "ClinicSoftware.ai website and AI reception questions",
        }
        for node in soup.find_all(["h2", "h3"]):
            current = " ".join(node.get_text(" ", strip=True).split())
            for prefix, replacement in clean_home_headings.items():
                if current.startswith(prefix):
                    node.clear()
                    node.append(NavigableString(replacement))
                    break

    review_copy = [
        ("Modern clinic website", "Clear service information, strong presentation and a simple route toward scheduling.", "Website design system"),
        ("AI virtual reception", "Natural answers drawn from approved clinic information, with an appropriate handoff when staff should help.", "Patient experience system"),
        ("Scheduling connections", "New and existing patients can reach the right scheduling path without searching through the site.", "Conversion pathway"),
        ("Managed over time", "Staff, service, policy and assistant knowledge updates can stay aligned after launch.", "Ongoing website service"),
    ]
    for index, card in enumerate(soup.select(".review-card")):
        values = review_copy[index % len(review_copy)]
        paragraphs = card.find_all("p")
        for item, value in zip(paragraphs, values):
            item.clear()
            item.append(NavigableString(value))

    if relative == "pricing.html":
        plans = ["Dental", "Chiropractic", "Optometry", "Specialty Care"]
        for node, value in zip(soup.select(".is-pricing-plan-name"), plans):
            node.string = value
        for node in soup.select(".is-pricing-mo"):
            node.string = "Website + AI"
        for node in soup.find_all(string=re.compile(r"\$[\d,]+")):
            node.replace_with(NavigableString("Tailored to the practice"))
        hero_copy = soup.select_one(".referral-hero-body")
        if hero_copy:
            hero_copy.string = "Choose a proven website direction, then tailor the content, visual identity, clinic knowledge and scheduling path to the practice."
        specialty_names = [
            "General and pediatric dentistry", "Orthodontics and oral surgery", "Optometry and optical",
            "Chiropractic", "Physical therapy and rehabilitation", "Podiatry", "Dermatology",
            "Ophthalmology", "Orthopedics", "ENT", "Urgent care", "Pain management",
            "Sports medicine", "Mental health", "OB-GYN", "Independent primary care",
            "Audiology", "Allergy and asthma", "Gastroenterology", "Plastic surgery and med spa",
            "Veterinary clinics", "Fertility clinics", "Sleep clinics",
        ]
        for node, value in zip(soup.select(".addon-desc-text.hyphenate"), specialty_names):
            node.string = value
        section_names = ["Core specialties", "Additional specialties", "Creative and managed support"]
        for node, value in zip(soup.select(".addon-name"), section_names):
            node.string = value

    if relative == "dental-marketing-software/lead-tracking.html":
        ai_headings = [
            "A virtual front desk designed around real clinic questions",
            "Answer general questions in a natural voice",
            "Guide each patient toward the right scheduling path",
            "Keep clinical decisions with qualified people",
            "Improve the experience from real conversations",
            "Available from every page on desktop and mobile",
            "Connect conversations to useful patient actions",
            "AI receptionist questions, answered",
        ]
        for node, value in zip(soup.find_all(["h2", "h3"]), ai_headings):
            node.clear()
            node.append(NavigableString(value))
        ai_paragraphs = [
            "Ava uses approved practice information such as hours, services, first-visit expectations, insurance policies and scheduling instructions to create a natural response.",
            "The assistant can understand an informal question, preserve conversational context and answer without forcing the visitor through a rigid menu.",
            "New patients, existing patients and general enquiries can be directed to the booking route or clinic contact method that applies to them.",
            "Questions about symptoms, treatment or medication are handed back to a clinician. Emergency language directs the visitor to emergency services.",
            "Clinic knowledge and conversation patterns can be reviewed and updated as hours, services, policies or scheduling systems change.",
        ]
        long_paragraphs = [node for node in soup.find_all("p") if len(node.get_text(" ", strip=True)) > 90]
        for index, node in enumerate(long_paragraphs):
            node.clear()
            node.append(NavigableString(ai_paragraphs[index % len(ai_paragraphs)]))
        label_changes = {
            "Clinic SEO": "Approved clinic knowledge",
            "Google Ads": "Scheduling connection",
            "Browse Our SEO FAQ's": "Explore common questions",
            "Get Your Google ads Analysis": "Request an AI receptionist preview",
            "Get Your Free Google ads Analysis": "Request an AI receptionist preview",
        }
        for node in soup.find_all(string=True):
            value = node.strip()
            if value in label_changes:
                node.replace_with(NavigableString(label_changes[value]))

    # Disable the original company's analytics, lead capture and tracking scripts.
    blocked_hosts = ("googletagmanager.com", "hs-scripts.com", "linkedin.com", "licdn.com", "patientloop.com", "customerioforms.com", "termly.io")
    for script in list(soup.find_all("script", src=True)):
        if any(host in script.get("src", "") for host in blocked_hosts):
            script.decompose()

    css_href = local_href(page, "clinicsoftware-overrides.css")
    if soup.head and not soup.find("link", href=css_href):
        css = soup.new_tag("link", rel="stylesheet", href=css_href)
        soup.head.append(css)
    js_src = local_href(page, "clinicsoftware.js")
    if soup.body and not soup.find("script", src=js_src):
        script = soup.new_tag("script", src=js_src, defer=True)
        soup.body.append(script)

    if html:
        html["data-clinicsoftware"] = "1"
        html["data-chat-host"] = "http://127.0.0.1:8000"
        html["data-wf-domain"] = "clinicsoftware.ai"
    page.write_text(str(soup))


for html_page in sorted(SITE.rglob("*.html")):
    customize_page(html_page)

print(f"Customized {len(list(SITE.rglob('*.html')))} HTML pages for ClinicSoftware.ai")
