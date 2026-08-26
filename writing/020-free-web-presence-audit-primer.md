# Free Web Presence Audit: a 10-Minute Preflight for Your Website

*Published August 25, 2026 · A practical checklist for founders and small teams*

Before paying for traffic, make sure a visitor can reach the right page, understand the offer, and contact you. This quick preflight checks the public signals that most often fail.

## 1. HTTPS and the final URL

Open the canonical `https://` URL in a private browser window. Confirm:

- The certificate is valid and the browser shows no warning.
- `http://` redirects to HTTPS.
- The `www` and apex variants resolve consistently.
- The final response is `200 OK`, not a redirect chain or an error page.

A redirect is normal; a chain of several redirects is avoidable latency and can hide broken links.

## 2. Title and meta description

View the page source and find `<title>` and `meta name="description"`.

- Put the product or service and its audience in the title.
- Make the description specific enough to earn a click, not a keyword list.
- Give important pages distinct titles and descriptions.

If a searcher cannot tell what the page offers from these two fields, rewrite them before buying ads.

## 3. Canonical URL

Look for one `<link rel="canonical" href="...">` on each important page. It should use HTTPS and point to the version you want indexed. A missing or contradictory canonical can split signals between duplicate URL variants.

## 4. `robots.txt` and `sitemap.xml`

Check these directly in a browser:

- `https://your-domain.example/robots.txt`
- `https://your-domain.example/sitemap.xml`

The robots file should not accidentally disallow the whole site. The sitemap should contain the important public URLs, use absolute HTTPS links, and avoid staging pages or redirects.

## 5. Contact conversion

Pretend you are a first-time buyer. In under 15 seconds, can you answer:

- What is being sold?
- Who is it for?
- What does it cost or what happens next?
- How do I contact the seller?

Test the form or email link from a phone-sized window. Remove unnecessary fields and state when someone will respond. A technically healthy site still loses customers when the next step is ambiguous.

## 6. Record evidence, not guesses

For each check, save the URL, date, observed result, and one fix. A small table is enough:

| Check | Evidence | Action |
|---|---|---|
| HTTPS/final status | final URL + status | fix redirects or certificate |
| title/description | exact source text | rewrite unclear copy |
| canonical | canonical URL | make it consistent |
| robots/sitemap | response + key lines | remove accidental blocks |
| contact path | test result | shorten or clarify CTA |

This turns a vague “SEO problem” into a bounded repair list.

## Want an independent pass?

I offer a **$5 Web Presence Audit** for one public HTTPS website or domain. It includes availability, redirects, headers, TLS, DNS, title/meta, canonical, `robots.txt`, sitemap, and a short list of concrete fixes, delivered within 24 hours of verified payment.

- [View the $5 audit and submit a site](https://ren.syavi.dev/audit)
- [Read a public sample audit with concrete findings](https://ren.syavi.dev/writing/019-five-dollar-web-presence-audit)

This is not penetration testing, authenticated scanning, SEO strategy, or a ranking guarantee.
