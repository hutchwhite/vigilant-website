#!/usr/bin/env python3
"""Generates the Vigilant static site pages with a shared header, footer and head."""
import json, os, re

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://vigilantcybersecurity.net"
BOOK = "https://outlook.office.com/book/VigilantCybersecurity1@vigilantcybersecurity.net/"
FONTS = "https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,500..800&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@500&display=swap"
UPDATED = "2026-09-27"

BUSINESS = {
    "@type": "ProfessionalService",
    "@id": f"{SITE}/#business",
    "name": "Vigilant Cybersecurity",
    "url": f"{SITE}/",
    "telephone": "+1-907-229-5222",
    "email": "consultations@vigilantcybersecurity.net",
    "address": {"@type": "PostalAddress", "addressLocality": "Anchorage", "addressRegion": "AK", "addressCountry": "US"},
    "areaServed": [{"@type": "State", "name": "Alaska"}, {"@type": "Country", "name": "United States"}],
    "founder": {"@type": "Person", "@id": f"{SITE}/about#hutch", "name": "Hutch White"},
    "description": "Practitioner-led CMMC Level 1 and Level 2 readiness for small and mid-sized defense contractors.",
    "logo": f"{SITE}/assets/logo-512.png",
    "image": f"{SITE}/assets/og-image.png",
}

NAV = [("/", "Home"), ("/cmmc", "CMMC"), ("/services", "Services"), ("/blog", "Briefings"), ("/about", "About"), ("/contact", "Contact")]


def page(path, title, desc, og_title, body, extra_graph=None, noindex=False, og_type="website", extra_head="", nav_path=None):
    url = SITE + path
    graph = [BUSINESS, {"@type": "WebPage", "@id": url + "#page", "url": url, "name": og_title,
                        "dateModified": UPDATED, "publisher": {"@id": f"{SITE}/#business"}}]
    if extra_graph:
        graph += extra_graph
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    cur = ' aria-current="page"'
    nav = "\n".join(
        f'        <li><a href="{h}"{cur if h == (nav_path or path) else ""}>{t}</a></li>' for h, t in NAV)
    robots = '\n<meta name="robots" content="noindex">' if noindex else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">{robots}
<meta name="theme-color" content="#191970">
<meta name="google-site-verification" content="ilmt1BuGJWr-0vZWOinix2JCIPiZpV2shWxJ1QzHnnA">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Vigilant Cybersecurity">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<script type="application/ld+json">
{ld}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/site.css">
<link rel="alternate" type="application/rss+xml" title="CMMC Weekly Briefing" href="{SITE}/feed.xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">{extra_head}
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<meta property="og:image" content="{SITE}/assets/og-image.png">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="/"><img src="/assets/logo-reverse.svg" alt="Vigilant Cybersecurity" width="253" height="64"></a>
    <nav aria-label="Main">
      <ul class="nav">
{nav}
        <li class="cta"><a class="btn btn-primary" href="{BOOK}">Book a call</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="main">
{body.strip()}
</main>

<footer class="site-foot">
  <div class="wrap">
    <a class="brand" href="/"><img src="/assets/logo-reverse.svg" alt="Vigilant Cybersecurity" width="253" height="64"></a>
    <ul class="foot-links">
      <li><a href="/cmmc">CMMC Status</a></li>
      <li><a href="/services">Services</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/contact">Contact</a></li>
      <li><a href="/privacy">Privacy</a></li>
      <li><a href="https://cyberab.org/Member/LCCA-66640-White-Carl" rel="noopener">Cyber AB Marketplace</a></li>
      <li><a href="https://www.linkedin.com/in/hutch-white" rel="noopener">LinkedIn</a></li>
    </ul>
    <div class="foot-meta">
      <span>© 2026 Vigilant Cybersecurity · Anchorage, Alaska</span>
      <span>Banner photos are public domain from DVIDS. The appearance of U.S. Department of Defense visual information does not imply or constitute DoD endorsement.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def cta_band(heading, text, quote=None):
    q = f'\n      <p class="quote">{quote}</p>' if quote else ""
    return f"""
  <section class="band" aria-labelledby="cta-h">
    <div class="wrap">
      <h2 id="cta-h">{heading}</h2>
      <p>{text}</p>{q}
      <div><a class="btn btn-primary" href="{BOOK}">Schedule a Complimentary Scoping Call</a></div>
      <p class="contact">Or reach a practitioner directly: <a href="tel:+19072295222">(907) 229-5222</a> · consultations@vigilantcybersecurity.net</p>
    </div>
  </section>"""


STARTER = """
  <section class="section" aria-labelledby="kit-h">
    <div class="wrap">
      <div class="teaser">
        <p class="label">Not ready for a call?</p>
        <h2 id="kit-h">Start with the free CMMC Resource Starter Kit</h2>
        <p>Level 1 readiness resources, funding options, and where Alaska contractors can get free help, including APEX Accelerators and Project Spectrum.</p>
        <p><a class="btn btn-ghost" href="/contact?topic=starter-kit">Send me the Starter Kit</a></p>
      </div>
    </div>
  </section>"""

# ---------------------------------------------------------------- HOME
home = f"""
  <section class="hero">
    <div class="wrap">
      <p class="eyebrow">Anchorage, Alaska · CMMC Level 1 and Level 2</p>
      <h1>CMMC Readiness for Alaska's Defense Contractors</h1>
      <p class="sub">Built for small and mid-sized defense contractors. Led personally, not delegated.</p>
      <p class="lede">Vigilant Cybersecurity guides Level 1 and Level 2 defense contractors from gap assessment through assessment-ready.</p>
      <div class="actions">
        <a class="btn btn-primary" href="{BOOK}">Schedule a Complimentary Scoping Call</a>
        <a class="btn btn-ghost" href="/cmmc">Learn About CMMC</a>
      </div>
    </div>
  </section>

  <section class="status" aria-labelledby="now-h">
    <div class="wrap">
      <div class="teaser">
        <p class="label">CMMC status · Updated September 27, 2026</p>
        <h2 id="now-h">Phase 2 is on hold. Your safeguarding obligations are not.</h2>
        <p>The Department of War suspended the November 2026 Phase 2 transition, and contracting officers are to "remove or revise the CMMC requirements" in solicitations and contracts. Contracts may still require Level 1 (Self) or Level 2 (Self). NIST SP 800-171 Rev. 2 under DFARS 252.204-7012 and the FAR basic safeguarding requirements still apply.</p>
        <p><a class="more" href="/cmmc">Read what this means for your contracts</a></p>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="how-h">
    <div class="wrap">
      <h2 id="how-h">How We Work</h2>
      <div class="grid grid-3">
        <article class="card">
          <h3>Practitioner Led</h3>
          <p>Every engagement is led personally by a CISSP and Lead CMMC Certified Assessor. No bench staff billing for "discovery" calls, no handoffs to a team you've never met, no junior consultants learning on your dime.</p>
        </article>
        <article class="card">
          <h3>Right-Sized</h3>
          <p>We don't sell managed services, software licenses or security tools, so our advice isn't shaped by what we resell. You get the controls and documentation your CMMC level requires to close your real gaps — no more, no less.</p>
        </article>
        <article class="card">
          <h3>Sustainable</h3>
          <p>The controls and documentation we help you implement are ones your team can keep up after we're gone. Compliance shouldn't depend on a consultant on permanent retainer.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="meet-h">
    <div class="wrap">
      <div class="meet">
        <img class="portrait" src="/assets/img/hutch-white-400.webp" srcset="/assets/img/hutch-white-400.webp 400w, /assets/img/hutch-white-800.webp 800w" sizes="220px" width="400" height="400" alt="Hutch White, founder and principal consultant of Vigilant Cybersecurity" loading="lazy">
        <div class="prose">
          <p class="label">Your practitioner</p>
          <h2 id="meet-h">Hutch White, LCCA, CISSP</h2>
          <p>Every Vigilant engagement is led by Hutch personally, from the first scoping call to the final evidence review. He is a Lead CMMC Certified Assessor with over 15 years in information security, based in Anchorage.</p>
          <p><a href="/about">More about Hutch and his credentials</a></p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="svc-h">
    <div class="wrap">
      <h2 id="svc-h">What We Focus On</h2>
      <div class="grid grid-2">
        <article class="card"><p class="label">2–4 weeks</p><h3>Gap Assessment</h3><p>A focused engagement that tells you exactly where you stand and what it will take to close the distance.</p><a class="more" href="/services#gap-assessment">Gap Assessment details</a></article>
        <article class="card"><p class="label">3–6 months</p><h3>CMMC Readiness</h3><p>Full-engagement Level 1 and Level 2 readiness for defense contractors and subcontractors moving from current state to assessment-ready.</p><a class="more" href="/services#cmmc-readiness">CMMC Readiness details</a></article>
        <article class="card"><p class="label">Monthly retainer</p><h3>vCISO Services</h3><p>Fractional security leadership for organizations that need a CISO's judgment but not a CISO's salary.</p><a class="more" href="/services#vciso">vCISO details</a></article>
        <article class="card"><p class="label">Annual or quarterly</p><h3>Compliance Sustainment</h3><p>Ongoing support for organizations that have already achieved readiness and need to maintain it year-over-year.</p><a class="more" href="/services#sustainment">Sustainment details</a></article>
      </div>
    </div>
  </section>
{STARTER}
{cta_band("Secure the Mission. Protect the Supply Chain.", "A free scoping call is the fastest way to find out which CMMC level applies to you and what it will take to get there. Bring your contract requirements, your timeline, or just your questions.")}
"""

# ---------------------------------------------------------------- SERVICES
def pkg(id_, title, for_, intro, items, term):
    lis = "\n".join(f"          <li>{i}</li>" for i in items)
    return f"""
      <article class="pkg" id="{id_}">
        <div class="pkg-intro">
          <h3>{title}</h3>
          <p class="for">{for_}</p>
          <p>{intro}</p>
          <p class="term">{term}</p>
        </div>
        <div class="inc">
          <p class="label">What's included</p>
          <ul class="checks">
{lis}
          </ul>
        </div>
      </article>"""

services = f"""
  <section class="hero">
    <div class="wrap">
      <p class="eyebrow">Services</p>
      <h1>Service Packages for Defense Contractors</h1>
      <p class="lede">Vigilant Cybersecurity offers four core engagement types for small and mid-sized defense contractors.</p>
      <p class="prose">Each offering is scoped to a different point in your compliance journey. Start with a Gap Assessment if you're not sure where you stand, commit to a CMMC Readiness engagement when you're ready to close the gaps, bring in vCISO Services for ongoing leadership, or stay assessment-ready year-over-year with Compliance Sustainment.</p>
      <p class="prose"><strong>We don't sell managed services, software licenses or security tools, so our advice isn't shaped by what we resell.</strong></p>
    </div>
  </section>

  <section class="section" aria-label="Service packages">
    <div class="wrap">
{pkg("cmmc-readiness", "CMMC Readiness", "For defense contractors and subcontractors that need to meet CMMC Level 1 or Level 2 requirements.",
     "A full engagement that takes your organization from current state through assessment-ready, built on NIST SP 800-171 and the CMMC program (32 CFR Part 170).",
     ["Right-sized scope and system boundary definition",
      "Comprehensive NIST SP 800-171 / CMMC gap analysis with prioritized remediation roadmap",
      "All required compliance artifacts — SSP, POA&amp;M, policies, and evidence packages",
      "Assessment-ready posture at engagement close"],
     "Typical engagement: 3–6 months, depending on starting posture and target level.")}
{pkg("gap-assessment", "Gap Assessment", "For organizations that need to understand where they stand before committing to a full readiness program.",
     "A focused engagement that gives you an honest, prioritized picture of your compliance posture and the cost and timeline to close the distance.",
     ["Current-state assessment against CMMC, NIST SP 800-171, or your applicable framework",
      "Prioritized findings report",
      "Draft Plan of Action &amp; Milestones (POA&amp;M)",
      "Remediation cost and timeline estimates"],
     "Typical engagement: 2–4 weeks.")}
{pkg("vciso", "vCISO Services", "For organizations that need senior security leadership without a full-time CISO's salary.",
     "We embed as your fractional security executive — owning your program roadmap, advising leadership and the board, and managing your compliance posture on a sustainable cadence.",
     ["Strategic security roadmap ownership",
      "Compliance program oversight (CMMC, HIPAA, NIST)",
      "Executive and board reporting",
      "Incident response coordination",
      "Vendor and third-party risk oversight"],
     "Typical engagement: Monthly retainer, ongoing.")}
{pkg("sustainment", "Compliance Sustainment", "For organizations that have already achieved CMMC, HIPAA, or NIST SP 800-171 readiness and need to maintain it year-over-year.",
     "Compliance isn't a one-time project — it's an annual cycle of self-assessments, affirmations, evidence collection, control reviews, and POA&amp;M closure. Sustainment engagements keep your program assessment-ready between assessments without putting a full vCISO on retainer.",
     ["Annual self-assessment execution and documentation",
      "Annual affirmation preparation",
      "Evidence collection and artifact management",
      "Control drift detection and remediation guidance",
      "POA&amp;M tracking and closure support",
      "Reassessment preparation",
      "Ad-hoc compliance advisory as questions arise"],
     "Typical engagement: Annual or quarterly cadence, scoped to your framework and assessment cycle.")}
    </div>
  </section>

  <section class="section" aria-labelledby="method-h">
    <div class="wrap">
      <h2 id="method-h">Inside a CMMC Readiness engagement</h2>
      <p class="prose">Every CMMC Readiness engagement follows the same six-phase methodology, scaled to your organization's size and level requirement. Gap Assessment engagements cover phases 1 and 2; vCISO Services span the full lifecycle as part of ongoing security leadership.</p>
      <div class="cover-wrap">
        <table class="cover">
          <caption>Which phases each engagement covers</caption>
          <thead><tr><th scope="col">Engagement</th><th scope="col">01 Scope</th><th scope="col">02 Gaps</th><th scope="col">03 Plan</th><th scope="col">04 Implement</th><th scope="col">05 Document</th><th scope="col">06 Validate</th></tr></thead>
          <tbody>
            <tr><th scope="row">Gap Assessment</th><td class="on" colspan="2">Phases 1–2</td><td colspan="4"></td></tr>
            <tr><th scope="row">CMMC Readiness</th><td class="on" colspan="6">All six phases</td></tr>
            <tr><th scope="row">vCISO Services</th><td class="on alt" colspan="6">Full lifecycle, as ongoing leadership</td></tr>
          </tbody>
        </table>
      </div>
      <ol class="phases">
        <li><div><h3>Discovery &amp; Scoping</h3><p>We begin by understanding your business structure, regulatory exposure (FCI or CUI), IT environment, and organizational goals. This phase defines your system boundary and establishes the scope for your compliance engagement — so nothing is over-built and nothing is missed.</p></div></li>
        <li><div><h3>Gap Analysis</h3><p>Your current practices are assessed against CMMC Level 1 or Level 2 requirements. We identify which requirements are met, which are missing, and the realistic level of effort to close each gap — producing a clear, prioritized findings report your team can act on.</p></div></li>
        <li><div><h3>Remediation Planning</h3><p>Based on your gap assessment, we build a risk-based remediation roadmap covering technical fixes, policy development, training requirements, and timelines. For Level 2 engagements, a draft Plan of Action and Milestones (POA&amp;M) is produced to guide implementation.</p></div></li>
        <li><div><h3>Implementation &amp; Hardening</h3><p>We apply and verify technical controls — access management, endpoint protection, secure configurations, backup and recovery — alongside administrative safeguards including policies, procedures, and security awareness training aligned to CMMC requirements.</p></div></li>
        <li><div><h3>Documentation &amp; Evidence</h3><p>We prepare or update the compliance artifacts required for a self-assessment or third-party assessment: System Security Plan (SSP), security policies, POA&amp;M, training records, access control documentation, and supporting evidence packages.</p></div></li>
        <li><div><h3>Validation &amp; Readiness Confirmation</h3><p>A final structured review confirms all requirements are addressed and evidence is complete. You leave this phase with a documented, defensible compliance posture — and a clear picture of what ongoing maintenance requires.</p></div></li>
      </ol>
    </div>
  </section>

  <section class="section" aria-labelledby="led-h">
    <div class="wrap">
      <h2 id="led-h">Led personally. Built to last.</h2>
      <p class="prose">Vigilant Cybersecurity was founded to give Alaska's small and mid-sized defense contractors a path to real, sustainable compliance — without the cost, complexity, or disconnect of a national firm. Whichever engagement type fits your situation, you'll work directly with the practitioner doing the work, and you'll come away with a security posture your team can maintain after the engagement ends.</p>
      <p class="prose">Hutch will not serve on a CMMC assessment of any organization Vigilant Cybersecurity has advised. Advisory and assessment work are kept separate, consistent with CMMC's conflict-of-interest rules.</p>
    </div>
  </section>
{STARTER}
{cta_band("Not sure where to start?", "A free consultation is the fastest way to figure out which engagement fits your situation. Bring your contract requirements, your timeline, or just your questions — we'll talk through it together.")}
"""

# ---------------------------------------------------------------- ABOUT
CREDS = [("LCCA", "Lead CMMC Certified Assessor"),
         ("CISSP", "Certified Information Systems Security Professional"),
         ("ISSMP", "Information Systems Security Management Professional"),
         ("CGRC", "Certified in Governance, Risk and Compliance"),
         ("GSTRT", "GIAC Strategic Planning, Policy, and Leadership"),
         ("RP", "CMMC Registered Practitioner")]
cred_li = "\n".join(f'            <li><abbr title="{n}">{a}</abbr><span>{n}</span></li>' for a, n in CREDS)

about = f"""
  <section class="hero">
    <div class="wrap">
      <p class="eyebrow">About</p>
      <h1>A Focused Practice for Alaska's Defense Industrial Base</h1>
      <p class="sub">Cybersecurity compliance, led personally — not delegated.</p>
    </div>
  </section>

  <section class="section" aria-label="Our approach">
    <div class="wrap">
      <div class="prose">
        <p>Vigilant Cybersecurity is a specialized consultancy serving small and mid-sized defense contractors in Alaska's defense industrial base. We exist for organizations that need to meet CMMC and federal cybersecurity requirements without the cost, overhead, and disconnect of a national firm — and that means doing the work differently.</p>
        <p>Every engagement is led personally by the principal consultant, supported by a vetted network of independent specialists when implementation requires it. Strategy, scoping, assessment, remediation guidance, and documentation all come from the same hands. When something needs to change mid-engagement, the conversation is with the person who can change it — not the partner-in-charge, not the engagement manager, not the bench staff.</p>
        <p>The result is compliance work that fits your operation rather than fighting it: scoped honestly, documented defensibly, and built so your team can sustain it after the engagement closes.</p>
      </div>
    </div>
  </section>

  <section class="section" id="hutch" aria-labelledby="hutch-h">
    <div class="wrap">
      <div class="bio">
        <div class="prose">
          <p class="label">Principal Consultant</p>
          <h2 id="hutch-h">About Hutch White</h2>
          <p>Hutch White is the founder and principal consultant of Vigilant Cybersecurity. He is a Lead CMMC Certified Assessor and brings over 15 years of security experience across multiple industries, including hands-on information system security officer work inside a regulated organization and support for compliance audits at organizations with thousands of users.</p>
          <p>Hutch founded Vigilant Cybersecurity to bring real-world, operationally grounded compliance expertise to organizations that have historically had to choose between under-qualified local generalists and unaffordable national firms.</p>
          <p>He is based in Anchorage and serves clients across Alaska and nationwide.</p>
          <p class="label">Independence</p>
          <p>Hutch will not serve on a CMMC assessment of any organization Vigilant Cybersecurity has advised. Advisory and assessment work are kept separate, consistent with CMMC's conflict-of-interest rules.</p>
        </div>
        <div class="bio-side">
          <img class="portrait" src="/assets/img/hutch-white-800.webp" srcset="/assets/img/hutch-white-400.webp 400w, /assets/img/hutch-white-800.webp 800w" sizes="(max-width: 820px) 90vw, 360px" width="800" height="800" alt="Hutch White, founder and principal consultant of Vigilant Cybersecurity">
        </div>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="creds-h">
    <div class="wrap">
      <h2 id="creds-h">Credentials</h2>
      <div class="cred-groups">
      <div class="cred-group cmmc">
        <p class="label">CMMC</p>
        <ul class="cred-list">
          <li class="cred lead"><span class="badge"><img src="/assets/img/badge-lcca-240.webp" width="120" height="120" alt="" loading="lazy"></span><div><p class="abbr">LCCA</p><p class="name">Lead CMMC Certified Assessor</p></div></li>
          <li class="cred"><span class="badge"><img src="/assets/img/badge-rp-240.webp" width="120" height="120" alt="" loading="lazy"></span><div><p class="abbr">RP</p><p class="name">Registered Practitioner</p><p class="issuer">The Cyber AB</p></div></li>
        </ul>
      </div>
      <div class="cred-group sec">
        <p class="label">Security leadership and governance</p>
        <ul class="cred-list">
          <li class="cred"><span class="badge"><img src="/assets/img/badge-cissp-240.webp" width="120" height="120" alt="" loading="lazy"></span><div><p class="abbr">CISSP</p><p class="name">Certified Information Systems Security Professional</p><p class="issuer">ISC2</p></div></li>
          <li class="cred"><span class="badge"><img src="/assets/img/badge-issmp-240.webp" width="120" height="120" alt="" loading="lazy"></span><div><p class="abbr">ISSMP</p><p class="name">Information Systems Security Management Professional</p><p class="issuer">ISC2</p></div></li>
          <li class="cred"><span class="badge"><img src="/assets/img/badge-cgrc-240.webp" width="120" height="120" alt="" loading="lazy"></span><div><p class="abbr">CGRC</p><p class="name">Certified in Governance, Risk and Compliance</p><p class="issuer">ISC2</p></div></li>
          <li class="cred"><span class="badge"><img src="/assets/img/badge-gstrt-240.webp" width="120" height="120" alt="" loading="lazy"></span><div><p class="abbr">GSTRT</p><p class="name">Strategic Planning, Policy, and Leadership</p><p class="issuer">GIAC</p></div></li>
        </ul>
      </div>
      </div>
      <p class="cred-verify"><a href="https://cyberab.org/Member/LCCA-66640-White-Carl" rel="noopener">Verify Hutch's LCCA listing on the Cyber AB Marketplace</a></p>
      <p class="cred-verify"><a href="https://www.linkedin.com/in/hutch-white" rel="noopener">Connect with Hutch on LinkedIn</a></p>
    </div>
  </section>

  <section class="section" aria-labelledby="focus-h">
    <div class="wrap">
      <h2 id="focus-h">What We Focus On</h2>
      <div class="grid grid-2">
        <article class="card"><h3>vCISO Services</h3><p>Fractional security leadership for organizations that need a CISO's judgment but not a CISO's salary.</p></article>
        <article class="card"><h3>Gap Assessment</h3><p>A focused 2–4 week engagement that tells you exactly where you stand and what it will take to close the distance.</p></article>
        <article class="card"><h3>CMMC Readiness</h3><p>Full-engagement Level 1 and Level 2 readiness for defense contractors and subcontractors moving from current state to assessment-ready.</p></article>
        <article class="card"><h3>Compliance Sustainment</h3><p>Annual and quarterly support for organizations that have already achieved readiness and need to maintain it year-over-year.</p></article>
      </div>
      <p><a href="/services">See service packages and timelines</a></p>
    </div>
  </section>
{cta_band("Get a Free Consultation", "Whether you're scoping a CMMC engagement, preparing for an upcoming defense contract, or just want a candid second opinion on your current security posture — we'd be glad to connect.")}
"""
about_person = [{"@type": "Person", "@id": f"{SITE}/about#hutch", "name": "Hutch White",
                 "jobTitle": "Founder and Principal Consultant", "image": f"{SITE}/assets/img/hutch-white-800.webp", "worksFor": {"@id": f"{SITE}/#business"}, "sameAs": ["https://cyberab.org/Member/LCCA-66640-White-Carl", "https://www.linkedin.com/in/hutch-white"],
                 "hasCredential": [{"@type": "EducationalOccupationalCredential", "name": n} for _, n in CREDS]}]

# ---------------------------------------------------------------- CONTACT
contact = f"""
  <section class="hero">
    <div class="wrap">
      <p class="eyebrow">Contact</p>
      <h1>Secure Your Business Today</h1>
      <p class="lede">Talk directly with the practitioner who will do the work. We typically respond within one business day.</p>
    </div>
  </section>

  <section class="section" aria-label="Ways to reach us">
    <div class="wrap">
      <div class="contact-grid">
        <div class="ways">
          <div class="way">
            <p class="label">Schedule a consultation</p>
            <p>The fastest way to get on the calendar. Pick a time that works for you.</p>
            <p><a class="btn btn-primary" href="{BOOK}">Book a Time</a></p>
          </div>
          <div class="way">
            <p class="label">Email</p>
            <p>For project inquiries, questions, or document exchange.</p>
            <p class="val">consultations@vigilantcybersecurity.net</p>
          </div>
          <div class="way">
            <p class="label">Phone</p>
            <p>Speak directly with a practitioner.</p>
            <p class="val"><a href="tel:+19072295222">(907) 229-5222</a></p>
          </div>
        </div>

        <form class="msg" id="contact-form" action="https://formspree.io/f/xwlpwapo" method="POST" aria-labelledby="form-h">
          <h2 id="form-h">Send Us a Message</h2>
          <div class="row2">
            <div class="field"><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name"></div>
            <div class="field"><label for="email">Email (required)</label><input id="email" name="email" type="email" autocomplete="email" required></div>
          </div>
          <div class="row2">
            <div class="field"><label for="company">Company</label><input id="company" name="company" type="text" autocomplete="organization"></div>
            <div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
          </div>
          <div class="field">
            <label for="topic">What can we help with?</label>
            <select id="topic" name="topic">
              <option value="general">General question</option>
              <option value="starter-kit">Send me the CMMC Resource Starter Kit</option>
              <option value="updates">Email me CMMC status updates</option>
              <option value="level-1">CMMC Level 1</option>
              <option value="level-2">CMMC Level 2</option>
              <option value="gap-assessment">Gap Assessment</option>
              <option value="vciso">vCISO Services</option>
              <option value="sustainment">Compliance Sustainment</option>
            </select>
          </div>
          <div class="field">
            <label for="message">Message (required)</label>
            <textarea id="message" name="message" required></textarea>
            <p class="hint">Describe your business and what you're working on. Please don't send CUI or other sensitive contract information through this form.</p>
          </div>
          <input type="hidden" name="_subject" value="New inquiry from vigilantcybersecurity.net">
          <div class="hp" aria-hidden="true"><label for="_gotcha">Leave this field empty</label><input id="_gotcha" name="_gotcha" type="text" tabindex="-1" autocomplete="off"></div>
          <p id="form-status" class="form-status" role="status" aria-live="polite" hidden></p>
          <button class="btn btn-primary" type="submit">Send</button>
          <p class="fine">By sending this form you agree to our <a href="/privacy">privacy policy</a>.</p>
        </form>
      </div>
    </div>
  </section>

  <section class="section" aria-label="Service area">
    <div class="wrap">
      <p class="prose">Vigilant Cybersecurity is based in <strong>Alaska</strong> and serves defense contractors and regulated organizations <strong>nationwide</strong>. Most engagements are conducted remotely, with on-site work available across Alaska and by arrangement in the lower 48.</p>
    </div>
  </section>
"""

# ---------------------------------------------------------------- PRIVACY
privacy = """
  <section class="hero has-art">
    <div class="wrap">
      <div class="hero-text">
        <p class="eyebrow">Privacy</p>
        <h1>Privacy Policy</h1>
        <p class="lede">What we collect through this site, why, and how it's protected.</p>
        <p class="stamp">Last updated September 27, 2026</p>
      </div>
      <img class="hero-art" src="/assets/img/art-privacy.svg" width="400" height="330" alt="">
    </div>
  </section>

  <section class="section" aria-label="Policy">
    <div class="wrap">
      <div class="doc">
        <p>Vigilant Cybersecurity ("we," "our," or "us") respects your privacy and is committed to protecting the personal information you share with us. This Privacy Policy describes how we collect, use, and protect your information when you use our website.</p>

        <h2>Information We Collect</h2>
        <p>When you use our contact form, we collect the following personal information:</p>
        <ul>
          <li>Name</li>
          <li>Email address</li>
          <li>Company name and phone number, if you provide them</li>
          <li>Any other information you voluntarily submit</li>
        </ul>

        <h2>How We Use Your Information</h2>
        <p>We use your information to:</p>
        <ul>
          <li>Respond to your inquiries or requests</li>
          <li>Provide you with information about our services</li>
          <li>Improve our website and user experience</li>
          <li>Comply with legal or regulatory requirements</li>
        </ul>

        <h2>Information Sharing</h2>
        <p>We do <strong>not</strong> sell, rent, or share your personal information with third parties, except:</p>
        <ul>
          <li>With your explicit consent</li>
          <li>As required by law or regulatory authority</li>
          <li>With third-party service providers that help us operate our website, such as our website host, form processor, and email provider, under confidentiality obligations</li>
        </ul>

        <h2>Data Security</h2>
        <p>We implement appropriate technical and organizational measures to protect your data, consistent with industry best practices and aligned with NIST SP 800-171 guidelines for safeguarding Controlled Unclassified Information (CUI), though this website does not handle CUI. Please do not submit CUI through this website.</p>

        <h2>Cookies and Analytics</h2>
        <p>This site uses privacy-focused, cookie-free analytics to understand how pages are used. No advertising or tracking cookies are set, and no sensitive personal data is collected.</p>

        <h2>Your Rights</h2>
        <p>You may request access to, correction of, or deletion of your personal information by contacting us at the email below. We will respond in accordance with applicable privacy laws.</p>

        <h2>Third-Party Links</h2>
        <p>Our website may include links to third-party websites, including our scheduling page. We are not responsible for their privacy practices or content.</p>

        <h2>Children's Privacy</h2>
        <p>Our website is not intended for use by children under the age of 13. We do not knowingly collect personal information from children.</p>

        <h2>Changes to This Policy</h2>
        <p>We may update this Privacy Policy at any time. Changes will be posted on this page with an updated date.</p>

        <h2>Contact Us</h2>
        <p>Questions about this policy: <span class="cite">consultations@vigilantcybersecurity.net</span></p>
      </div>
    </div>
  </section>
"""

# ---------------------------------------------------------------- 404
notfound = f"""
  <section class="hero has-art">
    <div class="wrap">
      <div class="hero-text">
      <p class="eyebrow">Error 404</p>
      <h1>That page isn't here</h1>
      <p class="lede">The link may be old or mistyped. These pages will get you back on track:</p>
      <div class="actions">
        <a class="btn btn-primary" href="/">Home</a>
        <a class="btn btn-ghost" href="/cmmc">CMMC status</a>
        <a class="btn btn-ghost" href="/contact">Contact</a>
      </div>
      </div>
      <img class="hero-art" src="/assets/img/art-404.svg" width="440" height="330" alt="">
    </div>
  </section>
"""

# ---------------------------------------------------------------- CMMC (reuse existing body)
cmmc_src = open(os.path.join(OUT, "cmmc.html")).read()
cmmc_body = re.search(r"<main[^>]*>(.*?)</main>", cmmc_src, re.S).group(1)
# strip generated additions so rebuilding from the published file stays idempotent
cmmc_body = re.sub(r'<section class="hero photo-[a-z0-9-]+">', '<section class="hero">', cmmc_body)
cmmc_body = re.sub(r'\n\s*<p class="credit">.*?</p>', '', cmmc_body)
cmmc_body = re.sub(r'<span class="ico" aria-hidden="true">.*?</span>', '', cmmc_body)
cmmc_body = re.sub(r'  <section class="section" id="faq".*?</section>\n\n', '', cmmc_body, flags=re.S)
cmmc_body = re.sub(r'  <section class="section" id="latest".*?</section>\n\n', '', cmmc_body, flags=re.S)
FAQ = [
    ("Is CMMC Phase 2 still starting November 10, 2026?",
     "No. On July 13, 2026, the Department of War CIO suspended the Phase 2 transition and later rollout milestones while a Reform Task Force reviews the program. No new date has been set."),
    ("Can a new contract still require CMMC?",
     "Yes. DFARS Class Deviation 2026-O0025, Revision 3 directs contracting officers to remove or revise the CMMC requirements in new and existing solicitations and contracts, and it permits requiring CMMC Level 1 (Self) or Level 2 (Self)."),
    ("If I handle CUI, do I still have to meet NIST SP 800-171?",
     "Yes. DFARS 252.204-7012 still requires NIST SP 800-171 Rev. 2 for covered contractor systems, and DoD can still conduct Medium or High assessments whose scores are posted in SPRS."),
    ("What does a small, FCI-only contractor need?",
     "Level 1 covers Federal Contract Information: the 15 basic safeguarding requirements in FAR 52.240-93 (formerly 52.204-21). When a contract requires Level 1 (Self), you post an annual self-assessment in SPRS and an affirming official signs an annual affirmation."),
    ("How long does it take to get ready?",
     "A Gap Assessment takes 2 to 4 weeks. A full CMMC Readiness engagement typically runs 3 to 6 months, depending on your starting point and target level."),
    ("Can the consultant who prepares us also assess us?",
     "No. CMMC's conflict-of-interest rules separate advisory work from assessment. Hutch will not serve on a CMMC assessment of any organization Vigilant Cybersecurity has advised."),
]


def faq_section():
    items = "\n".join(f'        <details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    return f"""  <section class="section" id="faq" aria-labelledby="faq-h">
    <div class="wrap">
      <h2 id="faq-h">CMMC Questions We Hear Most</h2>
      <div class="faq">
{items}
      </div>
    </div>
  </section>

"""


FAQ_SCHEMA = [{"@type": "FAQPage", "@id": f"{SITE}/cmmc#faq",
               "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]

cmmc_body = cmmc_body.replace('  <section class="band"', faq_section() + '  <section class="band"', 1)
cmmc_body = cmmc_body.replace("<h3>Level 3", "<h3>Level 3")  # no-op, body reused as is


ICONS = {
    "Gap Assessment": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.3 15.3 21 21"/><path d="M7.8 10.6l1.9 1.9 3.5-3.6"/>',
    "CMMC Readiness": '<path d="M12 2.8 19.5 6v5.4c0 4.6-3.1 8.2-7.5 9.8-4.4-1.6-7.5-5.2-7.5-9.8V6z"/><path d="M8.6 12.1l2.4 2.4 4.5-4.6"/>',
    "vCISO Services": '<circle cx="12" cy="12" r="9.2"/><path d="M12 5.2l1.5 5.3 5.3 1.5-5.3 1.5L12 18.8l-1.5-5.3L5.2 12l5.3-1.5z"/>',
    "Compliance Sustainment": '<path d="M19.6 9.2A8 8 0 0 0 5.3 7.4"/><path d="M4.4 14.8a8 8 0 0 0 14.3 1.8"/><path d="M5 3.6v4.1h4.1"/><path d="M19 20.4v-4.1h-4.1"/>',
}


def add_icons(html):
    for name, paths in ICONS.items():
        svg = ('<span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" '
               'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + paths + '</svg></span>')
        html = html.replace(f"<h3>{name}</h3>", svg + f"<h3>{name}</h3>")
    return html


HERO_PHOTOS = {
    "index.html": ("photo-cook-inlet", None),  # Adobe Stock, licensed; no credit required
    "cmmc.html": ("photo-sm1a", "Photo: Thomas Deaton, SM-1A site at Fort Greely, Alaska (DVIDS)"),
    "services.html": ("photo-cordova", "Photo: Alejandro Pena, Shepard Point near Cordova, Alaska (DVIDS)"),
    "about.html": ("photo-seward", "Photo: Airman 1st Class Miranda Parnell, 169th Civil Engineer Squadron at Seward, Alaska (DVIDS)"),
    "contact.html": ("photo-runway", "Photo: Senior Airman Tala Hunt, runway expansion at Joint Base Elmendorf-Richardson (DVIDS)"),
}


def add_hero_photo(fname, html):
    if fname not in HERO_PHOTOS:
        return html
    cls, credit = HERO_PHOTOS[fname]
    start = html.index('<section class="hero">')
    html = html[:start] + f'<section class="hero {cls}">' + html[start + len('<section class="hero">'):]
    if not credit:
        return html
    close = html.index('\n    </div>\n  </section>', start)
    return html[:close] + f'\n      <p class="credit">{credit}</p>' + html[close:]

PAGES = {
    "index.html": ("/", "CMMC Consultant in Alaska | Vigilant Cybersecurity",
                   "Practitioner-led CMMC Level 1 and Level 2 readiness for Alaska defense contractors. Gap assessments, SSPs and POA&amp;Ms, led by a Lead CMMC Certified Assessor.",
                   "CMMC Readiness for Alaska's Defense Contractors", home, None),
    "cmmc.html": ("/cmmc", "CMMC Status Update 2026: What Contractors Must Do Now | Vigilant Cybersecurity",
                  "Phase 2 is suspended, but NIST SP 800-171 and basic safeguarding rules still apply. A plain-English update for Alaska defense contractors, revised as guidance changes.",
                  "CMMC Status Update 2026: What Contractors Must Do Now", cmmc_body, FAQ_SCHEMA),
    "services.html": ("/services", "CMMC Gap Assessment, Readiness &amp; vCISO | Vigilant",
                      "Fixed-scope CMMC gap assessments in 2 to 4 weeks, full Level 1 and Level 2 readiness, vCISO and compliance sustainment for small defense contractors.",
                      "Service Packages for Defense Contractors", services, None),
    "about.html": ("/about", "About Hutch White, LCCA, CISSP | Vigilant Cybersecurity",
                   "Anchorage-based Lead CMMC Certified Assessor with 15+ years in security. Every engagement is led personally, never handed off to junior staff.",
                   "About Vigilant Cybersecurity", about, about_person),
    "contact.html": ("/contact", "Book a Free CMMC Scoping Call | Vigilant Cybersecurity",
                     "Talk directly with a practitioner about your CMMC scope, contracts and timeline. Anchorage-based, serving contractors on-site and remotely.",
                     "Contact Vigilant Cybersecurity", contact, None),
    "privacy.html": ("/privacy", "Privacy Policy | Vigilant Cybersecurity",
                     "How Vigilant Cybersecurity collects and protects information submitted through this site.",
                     "Privacy Policy", privacy, None),
}

for fname, (path, title, desc, og, body, extra) in PAGES.items():
    html = add_hero_photo(fname, add_icons(page(path, title, desc, og, body, extra)))
    if fname == "contact.html":
        html = html.replace("</body>", '<script src="/assets/contact.js" defer></script>\n</body>')
    open(os.path.join(OUT, fname), "w").write(html)
open(os.path.join(OUT, "404.html"), "w").write(
    page("/404", "Page Not Found | Vigilant Cybersecurity", "This page could not be found.", "Page Not Found", notfound, None, noindex=True))
import blog
posts = blog.build(page, cta_band, SITE, OUT)
print("built", list(PAGES) + ["404.html"], "posts:", len(posts))
