"""Machina Logic static site builder.

Edit content in src/pages/*.html, styles in src/site.css, behaviour in src/site.js and
vector artwork in art.py, then run:  python3 build.py
Pages are written to dist/ and are self-contained (CSS, JS, logo and artwork inlined),
so they open by double-clicking and can be uploaded to any static host as-is.
Copy the contents of dist/ to the repository root to publish.

Placeholders available inside pages:
  {{EMAIL}} {{PHONE_DISPLAY}} {{PHONE_TEL}} {{ADDRESS}}
  {{ART:hero}} {{ART:gap}} {{ART:map}} {{ART:purdue}}
  {{SVC:<name>|<aria label>}}   service drawing (visibility, detection, response, risk, compliance, workforce)
  {{SEC:<name>|<aria label>}}   sector drawing (energy, mining, manufacturing, water, ports, government)
"""
import base64, json, pathlib, re
import art

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
SITE = "https://machina-logic.com"

EMAIL = "info@machina-logic.com"
PHONE_DISPLAY = "+234 802 394 8090"
PHONE_TEL = "+2348023948090"
ADDRESS = "Lekki, Lagos State, Nigeria"

LOGO = "data:image/png;base64," + base64.b64encode((SRC / "logo.png").read_bytes()).decode()
FAVICON_SVG = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
               "<rect width='32' height='32' rx='5' fill='#11233F'/>"
               "<path d='M6 16h20M11 16V8M21 16v8' fill='none' stroke='#FFC21A' stroke-width='3'/>"
               "<rect x='8' y='5' width='6' height='6' fill='#FFC21A'/><rect x='18' y='21' width='6' height='6' fill='#FFC21A'/></svg>")
FAVICON = "data:image/svg+xml;base64," + base64.b64encode(FAVICON_SVG.encode()).decode()
CSS = (SRC / "site.css").read_text()
JS = (SRC / "site.js").read_text()
FONTS = ("https://fonts.googleapis.com/css2?family=Big+Shoulders:opsz,wght@10..72,600..900"
         "&family=Atkinson+Hyperlegible+Next:ital,wght@0,400..800;1,400&display=swap")

SPRITE = """<svg class="sprite" aria-hidden="true" focusable="false"><defs>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M3 6h18M3 12h12M3 18h18"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path d="M5 5l14 14M19 5 5 19"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24"><path d="M3 5h18v14H3z"/><path d="M3 6l9 7 9-7"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21.5s-7-6.2-7-11.5a7 7 0 0 1 14 0c0 5.3-7 11.5-7 11.5z"/><circle cx="12" cy="10" r="2.5"/></symbol>
<symbol id="i-globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z"/></symbol>
<symbol id="i-warn" viewBox="0 0 24 24"><path d="M12 3 22 20H2z"/><path d="M12 10v4.5M12 17v.5"/></symbol>
</defs></svg>"""

NAV = [("services.html", "Services"), ("industries.html", "Industries"),
       ("resources.html", "Resources"), ("about.html", "About")]

SERVICES = [("asset-visibility", "Asset visibility"), ("threat-detection", "Threat detection & monitoring"),
            ("incident-response", "Incident response"), ("risk-assessment", "Risk & vulnerability assessment"),
            ("compliance", "Compliance & regulatory advisory"), ("workforce", "Workforce readiness")]


def ico(name, cls="ico"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def logo(cls="logo"):
    return f'<span class="{cls}" role="img" aria-label="Machina Logic"></span>'


def header(active):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>' for href, label in NAV)
    mlinks = "".join(f'<a class="m-link" href="{h}" style="--i:{i}">{l}</a>'
                     for i, (h, l) in enumerate([("index.html", "Home")] + NAV + [("contact.html", "Contact")]))
    return f"""<header class="site-header">
  <div class="bar">
    <a href="index.html" class="brand" aria-label="Machina Logic home">{logo()}</a>
    <nav class="navlinks" aria-label="Primary">{links}</nav>
    <a href="contact.html" class="btn btn-go nav-cta">Request a briefing</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu">
      {ico("menu", "ico ico-open")}{ico("close", "ico ico-close")}
    </button>
  </div>
</header>
<nav id="mobile-nav" class="mobile-nav" aria-label="Mobile" hidden>
  <div class="m-links">{mlinks}</div>
  <a href="contact.html" class="btn btn-go">Request a briefing</a>
  <div class="m-contact"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div>
</nav>"""


CTA = f"""<section class="cta-band">
  <div class="hazard-edge" aria-hidden="true"></div>
  <div class="wrap cta-grid">
    <span class="node" data-kind="earth" aria-hidden="true"></span>
    <h2>Know what's really connected to your plant.</h2>
    <div class="cta-side">
      <p>Book a confidential briefing. We'll talk through your environment, your concerns and where an independent OT security view would help most.</p>
      <div class="ctas">
        <a href="contact.html" class="btn btn-ink">Request a briefing</a>
        <a href="mailto:{EMAIL}" class="btn btn-line">Email {EMAIL}</a>
      </div>
    </div>
  </div>
</section>"""


def footer():
    svc = "".join(f'<li><a href="services.html#{i}">{n.replace("&", "&amp;")}</a></li>' for i, n in SERVICES)
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a href="index.html" aria-label="Machina Logic home">{logo("logo logo-light")}</a>
      <p>Operational technology security for the plants, grids, mines, ports and water works that keep African economies running.</p>
      <p class="plate plate-hz">Lagos HQ, working across Africa</p>
    </div>
    <div>
      <h3>Company</h3>
      <ul><li><a href="about.html">About</a></li><li><a href="industries.html">Industries</a></li><li><a href="resources.html">Resources</a></li><li><a href="contact.html">Contact</a></li><li><a href="privacy.html">Privacy notice</a></li></ul>
    </div>
    <div>
      <h3>Services</h3>
      <ul>{svc}</ul>
    </div>
    <div>
      <h3>Talk to us</h3>
      <ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li><li>{ADDRESS}</li></ul>
    </div>
  </div>
  <div class="wrap footer-bottom"><div>
    <span>&copy; <span data-year>2026</span> Machina Logic. All rights reserved.</span>
    <span>Secure. Operate. Endure.</span>
  </div></div>
</footer>"""


ORG_LD = json.dumps({
    "@context": "https://schema.org", "@type": "Organization", "name": "Machina Logic",
    "url": SITE, "email": EMAIL, "telephone": PHONE_TEL,
    "description": "Operational technology (OT) and industrial control system (ICS) cybersecurity for critical infrastructure across Africa.",
    "address": {"@type": "PostalAddress", "addressLocality": "Lekki", "addressRegion": "Lagos State", "addressCountry": "NG"},
    "areaServed": "Africa"
})

PAGES = [
    # file, source, title, description, nav-active, include CTA band, in sitemap
    ("index.html", "home.html", "Machina Logic | OT & ICS Cybersecurity for African Critical Infrastructure",
     "Machina Logic secures the operational technology behind Africa's power, water, mining, manufacturing, ports and public infrastructure.", "", True, True),
    ("services.html", "services.html", "OT Security Services | Machina Logic",
     "Asset visibility, OT threat monitoring, incident response, risk assessment, compliance advisory and workforce readiness for industrial operators across Africa.", "services.html", True, True),
    ("industries.html", "industries.html", "Industries We Protect | Machina Logic",
     "OT security for energy and utilities, oil, gas and mining, manufacturing, water, ports and logistics, and the public sector across Africa.", "industries.html", True, True),
    ("about.html", "about.html", "About Machina Logic | OT Security Built for Africa",
     "Machina Logic is a specialist operational technology security practice built for the infrastructure operators that keep African economies running.", "about.html", True, True),
    ("resources.html", "resources.html", "OT Security Primer, Frameworks & Glossary | Machina Logic",
     "A practical introduction to operational technology security: the Purdue model, IT vs OT, key frameworks, African regulation and an OT glossary.", "resources.html", True, True),
    ("contact.html", "contact.html", "Contact Machina Logic | Request an OT Security Briefing",
     "Talk to Machina Logic about securing your industrial environment. Request a confidential briefing.", "", False, True),
    ("privacy.html", "privacy.html", "Privacy Notice | Machina Logic",
     "How Machina Logic handles personal information submitted through this website.", "", False, True),
    ("thank-you.html", "thank-you.html", "Request received | Machina Logic",
     "Thank you for contacting Machina Logic.", "", False, False),
    ("404.html", "404.html", "Page not found | Machina Logic", "The page you were looking for could not be found.", "", False, False),
]


def fill(body):
    body = (body.replace("{{EMAIL}}", EMAIL).replace("{{PHONE_DISPLAY}}", PHONE_DISPLAY)
                .replace("{{PHONE_TEL}}", PHONE_TEL).replace("{{ADDRESS}}", ADDRESS))
    body = re.sub(r"\{\{ART:(\w+)\}\}", lambda m: art.art(m.group(1)), body)
    body = re.sub(r"\{\{SVC:(\w+)\|([^}]*)\}\}", lambda m: art.service_art(m.group(1), m.group(2)), body)
    body = re.sub(r"\{\{SEC:(\w+)\|([^}]*)\}\}", lambda m: art.sector_art(m.group(1), m.group(2)), body)
    assert "{{" not in body, re.findall(r"\{\{[^}]*\}\}", body)
    return body


def render(file, src, title, desc, active, cta, _sitemap):
    body = fill((SRC / "pages" / src).read_text())
    path = "" if file == "index.html" else file
    ld = f'<script type="application/ld+json">{ORG_LD}</script>' if file == "index.html" else ""
    robots = '<meta name="robots" content="noindex">' if file in ("404.html", "thank-you.html") else ""
    page = file.replace(".html", "")
    return f"""<!doctype html>
<html lang="en" data-page="{page}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{path}">
{robots}
<meta name="theme-color" content="#D4D7CF">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Machina Logic">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{path}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<script>document.documentElement.classList.add('js');</script>
<style>
:root{{--logo:url("{LOGO}")}}
{CSS}
</style>
{ld}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{SPRITE}
{header(active)}
<main id="main">
{body}
{CTA if cta else ""}
</main>
{footer()}
<script>
{JS}
</script>
</body>
</html>
"""


def main():
    DIST.mkdir(exist_ok=True)
    for p in PAGES:
        (DIST / p[0]).write_text(render(*p))
        print("built", p[0])
    urls = "".join(f"  <url><loc>{SITE}/{'' if p[0] == 'index.html' else p[0]}</loc></url>\n"
                   for p in PAGES if p[6])
    (DIST / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print("built sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
