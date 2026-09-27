"""Machina Logic static site builder.

Edit content in src/pages/*.html and shared styles/scripts in src/site.css and src/site.js,
then run:  python3 build.py
Every page in dist/ is fully self-contained (CSS, JS and logo inlined), so it opens
correctly by double-clicking and can be uploaded to any static host as-is.
"""
import base64, json, pathlib

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
SITE = "https://machina-logic.com"

EMAIL = "info@machina-logic.com"
PHONE_DISPLAY = "+234 112 3456 347"
PHONE_TEL = "+2341123456347"
ADDRESS = "Lekki, Lagos State, Nigeria"

LOGO = "data:image/png;base64," + base64.b64encode((SRC / "logo.png").read_bytes()).decode()
FAVICON_SVG = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
               "<rect width='32' height='32' fill='#17181a'/>"
               "<path d='M5 13v14h11M27 19V5H16' fill='none' stroke='#3fd8be' stroke-width='3'/></svg>")
FAVICON = "data:image/svg+xml;base64," + base64.b64encode(FAVICON_SVG.encode()).decode()
CSS = (SRC / "site.css").read_text()
JS = (SRC / "site.js").read_text()

SPRITE = """<svg class="sprite" aria-hidden="true" focusable="false"><defs>
<symbol id="i-visibility" viewBox="0 0 24 24"><path d="M4 8V4h4M16 4h4v4M20 16v4h-4M8 20H4v-4"/><circle cx="12" cy="12" r="2.2"/></symbol>
<symbol id="i-pulse" viewBox="0 0 24 24"><path d="M2 13h4l2-7 3 14 3-11 2 4h6"/></symbol>
<symbol id="i-response" viewBox="0 0 24 24"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></symbol>
<symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 3 19 6v6c0 5-3.3 7.6-7 9-3.7-1.4-7-4-7-9V6z"/><path d="M9 12.2 11 14.2 15.2 10"/></symbol>
<symbol id="i-doc" viewBox="0 0 24 24"><path d="M6 2h9l3 3v17H6z"/><path d="M15 2v3h3"/><path d="M9 9h3M9 12.5h6M9 16h6"/></symbol>
<symbol id="i-people" viewBox="0 0 24 24"><circle cx="8.2" cy="7.2" r="2.7"/><path d="M2.3 20.5v-1.8a4 4 0 0 1 4-4h3.8a4 4 0 0 1 4 4v1.8"/><circle cx="17" cy="7.7" r="2.1"/><path d="M15.6 11.3h1.6a3.6 3.6 0 0 1 3.6 3.6v1.4"/></symbol>
<symbol id="i-energy" viewBox="0 0 24 24"><path d="M12 2 6.5 22M12 2l5.5 20"/><path d="M9.3 8h5.4M7.6 14h8.8M5.8 20h12.4"/></symbol>
<symbol id="i-mining" viewBox="0 0 24 24"><path d="M13.2 2.8 21 10.6l-3 3-7.8-7.8z"/><path d="M10.9 8.5 13.5 11.1"/><path d="M3 21l7.9-7.9"/></symbol>
<symbol id="i-factory" viewBox="0 0 24 24"><path d="M3 21V10l5 3V10l5 3V10l5 3V4h3v17z"/><path d="M7 17h2M12 17h2M17 17h1"/></symbol>
<symbol id="i-water" viewBox="0 0 24 24"><path d="M12 2.5 17.5 11a6 6 0 1 1-11 0z"/><path d="M9.5 15.5a2.6 2.6 0 0 0 2.5 2"/></symbol>
<symbol id="i-ports" viewBox="0 0 24 24"><path d="M3 10.5h18v8H3z"/><path d="M3 14.5h18M7.5 10.5v8M12 10.5v8M16.5 10.5v8"/><path d="M12 10.5V3.5l7 4"/></symbol>
<symbol id="i-gov" viewBox="0 0 24 24"><path d="M3.5 9 12 3.5 20.5 9"/><path d="M5.5 9v10.5M18.5 9v10.5M9.7 9v10.5M14.3 9v10.5"/><path d="M3 20.5h18"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="M4.5 12.5 9.5 17.5 19.5 6.5"/></symbol>
<symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 4v16M4 12h16"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M3 7h18M3 12h18M9 17h12"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path d="M5 5l14 14M19 5 5 19"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24"><path d="M3 5h18v14H3z"/><path d="M3 6l9 7 9-7"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21.5s-7-6.2-7-11.5a7 7 0 0 1 14 0c0 5.3-7 11.5-7 11.5z"/><circle cx="12" cy="10" r="2.5"/></symbol>
<symbol id="i-layers" viewBox="0 0 24 24"><path d="M12 2.5 2.5 7.5 12 12.5l9.5-5z"/><path d="M2.5 12 12 17l9.5-5M2.5 16.5 12 21.5l9.5-5"/></symbol>
<symbol id="i-target" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/></symbol>
<symbol id="i-balance" viewBox="0 0 24 24"><path d="M12 3v18M6 21h12M4 7h16"/><path d="M7 7l-3 7h6zM17 7l-3 7h6z"/></symbol>
<symbol id="i-radar" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><path d="M12 12l6.4-6.4"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></symbol>
<symbol id="i-siren" viewBox="0 0 24 24"><path d="M6 18v-6a6 6 0 0 1 12 0v6"/><path d="M4 18h16v3H4z"/><path d="M12 2v2M4.2 5.2l1.4 1.4M19.8 5.2l-1.4 1.4"/></symbol>
<symbol id="i-book" viewBox="0 0 24 24"><path d="M3 4h6.5A2.5 2.5 0 0 1 12 6.5V20a2 2 0 0 0-2-2H3z"/><path d="M21 4h-6.5A2.5 2.5 0 0 0 12 6.5V20a2 2 0 0 1 2-2h7z"/></symbol>
<symbol id="i-alert" viewBox="0 0 24 24"><path d="M12 3 22 20H2z"/><path d="M12 10v4.5M12 17v.5"/></symbol>
<symbol id="i-globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z"/></symbol>
</defs></svg>"""

NAV = [("services.html", "Services"), ("industries.html", "Industries"),
       ("resources.html", "Resources"), ("about.html", "About")]

SERVICES = [("asset-visibility", "Asset visibility"), ("threat-detection", "Threat detection & monitoring"),
            ("incident-response", "Incident response"), ("risk-assessment", "Risk & vulnerability assessment"),
            ("compliance", "Compliance & regulatory advisory"), ("workforce", "Workforce readiness")]


def ico(name, cls="ico"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def header(active):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>' for href, label in NAV)
    mlinks = "".join(f'<a class="m-link" href="{h}">{l}{ico("arrow")}</a>'
                     for h, l in [("index.html", "Home")] + NAV + [("contact.html", "Contact")])
    return f"""<header class="site-header">
  <div class="wrap nav">
    <a href="index.html" class="brand" aria-label="Machina Logic home"><img src="{LOGO}" alt="Machina Logic" width="75" height="32"></a>
    <nav class="navlinks" aria-label="Primary">{links}</nav>
    <div class="nav-actions">
      <a href="contact.html" class="btn btn-primary">Request a briefing {ico("arrow")}</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu">
        {ico("menu", "ico ico-open")}{ico("close", "ico ico-close")}
      </button>
    </div>
  </div>
</header>
<nav id="mobile-nav" class="mobile-nav" aria-label="Mobile" hidden>
  {mlinks}
  <a href="contact.html" class="btn btn-primary">Request a briefing {ico("arrow")}</a>
  <div class="m-contact"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div>
</nav>"""


CTA = f"""<section class="cta-band">
  <div class="wrap">
    <div class="cta-box bracket reveal">
      <div class="bg-lines"></div>
      <div>
        <p class="eyebrow">Start the conversation</p>
        <h2>Know what's really connected to your plant.</h2>
        <p>Book a confidential briefing with our team. We'll discuss your environment, your concerns and where an independent OT security view would help most.</p>
      </div>
      <div class="ctas">
        <a href="contact.html" class="btn btn-primary">Request a briefing {ico("arrow")}</a>
        <a href="mailto:{EMAIL}" class="btn btn-ghost">Email us</a>
      </div>
    </div>
  </div>
</section>"""


def footer():
    svc = "".join(f'<li><a href="services.html#{i}">{n.replace("&", "&amp;")}</a></li>' for i, n in SERVICES)
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a href="index.html" aria-label="Machina Logic home"><img src="{LOGO}" alt="Machina Logic" width="85" height="36"></a>
      <p>Operational technology security for the infrastructure that keeps African economies running.</p>
      <p class="loc"><span class="status-dot"></span> Lagos · Africa-wide</p>
    </div>
    <div>
      <h4>Company</h4>
      <ul><li><a href="about.html">About</a></li><li><a href="industries.html">Industries</a></li><li><a href="resources.html">Resources</a></li><li><a href="contact.html">Contact</a></li><li><a href="privacy.html">Privacy notice</a></li></ul>
    </div>
    <div>
      <h4>Services</h4>
      <ul>{svc}</ul>
    </div>
    <div>
      <h4>Contact</h4>
      <ul class="fc"><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li><li>{ADDRESS}</li></ul>
    </div>
  </div>
  <div class="footer-bottom"><div class="wrap">
    <span>&copy; <span data-year>2026</span> Machina Logic. All rights reserved.</span>
    <span class="mono">SECURE · OPERATE · ENDURE</span>
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
    # file, source, title, description, nav-active, include CTA band
    ("index.html", "home.html", "Machina Logic | OT & ICS Cybersecurity for African Critical Infrastructure",
     "Machina Logic secures the operational technology behind Africa's power, water, mining, manufacturing, ports and public infrastructure.", "", True),
    ("services.html", "services.html", "OT Security Services | Machina Logic",
     "Asset visibility, OT threat monitoring, incident response, risk assessment, compliance advisory and workforce readiness for industrial operators across Africa.", "services.html", True),
    ("industries.html", "industries.html", "Industries We Protect | Machina Logic",
     "OT security for energy and utilities, oil, gas and mining, manufacturing, water, ports and logistics, and the public sector across Africa.", "industries.html", True),
    ("about.html", "about.html", "About Machina Logic | OT Security Built for Africa",
     "Machina Logic is a specialist operational technology security practice built for the infrastructure operators that keep African economies running.", "about.html", True),
    ("resources.html", "resources.html", "OT Security Primer, Frameworks & Glossary | Machina Logic",
     "A practical introduction to operational technology security: the Purdue model, IT vs OT, key frameworks, African regulation and an OT glossary.", "resources.html", True),
    ("contact.html", "contact.html", "Contact Machina Logic | Request an OT Security Briefing",
     "Talk to Machina Logic about securing your industrial environment. Request a confidential briefing.", "", False),
    ("privacy.html", "privacy.html", "Privacy Notice | Machina Logic",
     "How Machina Logic handles personal information submitted through this website.", "", False),
    ("404.html", "404.html", "Page not found | Machina Logic", "The page you were looking for could not be found.", "", False),
]


def render(file, src, title, desc, active, cta):
    body = (SRC / "pages" / src).read_text()
    body = (body.replace("{{EMAIL}}", EMAIL).replace("{{PHONE_DISPLAY}}", PHONE_DISPLAY)
                .replace("{{PHONE_TEL}}", PHONE_TEL).replace("{{ADDRESS}}", ADDRESS))
    path = "" if file == "index.html" else file
    ld = f'<script type="application/ld+json">{ORG_LD}</script>' if file == "index.html" else ""
    robots = '<meta name="robots" content="noindex">' if file == "404.html" else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{path}">
{robots}
<meta name="theme-color" content="#17181a">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Machina Logic">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{path}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
<script>document.documentElement.classList.add('js');</script>
<style>
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
                   for p in PAGES if p[0] != "404.html")
    (DIST / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print("built sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
