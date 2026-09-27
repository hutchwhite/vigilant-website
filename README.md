# vigilantcybersecurity.net

Static site for Vigilant Cybersecurity. Plain HTML and CSS, no build step, no server code.

## Files

| File | What it is |
| --- | --- |
| `index.html`, `cmmc.html`, `services.html`, `about.html`, `contact.html`, `privacy.html` | The six pages. Cloudflare Pages serves `cmmc.html` at `/cmmc`, so existing URLs stay the same. |
| `404.html` | Shown for any missing page |
| `assets/site.css` | All styling, shared by every page |
| `assets/logo.svg`, `assets/logo-reverse.svg` | Full logo for light and dark backgrounds (text is outlined, no font needed) |
| `assets/logo-mark.svg`, `assets/favicon.svg` | The V-and-star mark alone, and the browser-tab icon |
| `assets/topo.svg` | Contour-line texture used behind dark sections |
| `assets/og-image.png` | Preview image shown when the site is shared on LinkedIn and elsewhere |
| `assets/contact.js` | Preselects the contact form topic from links like `/contact?topic=starter-kit` |
| `_headers` | Security headers (CSP, HSTS and others), applied by Cloudflare Pages |
| `robots.txt`, `sitemap.xml` | For search engines. Update `lastmod` in the sitemap when a page changes. |

## Before going live

1. **Contact form:** connected to Formspree form `xwlpwapo`. Submissions arrive at the email set in your Formspree dashboard.
2. **Analytics:** in Cloudflare Pages, turn on Web Analytics for the project. It is cookie-free, and `_headers` already allows it.
3. **Search Console:** after cutover, add the site as a Domain property and submit `https://vigilantcybersecurity.net/sitemap.xml`.

## Moving DNS off GoDaddy's website builder

Keep every existing MX, TXT (SPF, DMARC, domain verification), CNAME (`autodiscover`, `selector1._domainkey`, `selector2._domainkey`, `enterpriseregistration`, `enterpriseenrollment`) and SRV record exactly as it is. Only the records for the website itself (`@` and `www`) change. Export or screenshot the current GoDaddy DNS zone before touching anything.
