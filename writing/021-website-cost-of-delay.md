# The Cost of Sending Visitors to a Broken Website

*2026-08-25*

A website can be technically online and still lose the next customer. A redirect may land on the wrong URL, a missing title can make a shared link unclear, a stale canonical can point search engines elsewhere, or a contact path can fail on the final page. These are cheap problems to check and expensive problems to discover after a launch, referral, or campaign.

## A ten-minute preflight

Before sending traffic to a site, check:

1. **Availability and final URL.** Request the HTTPS URL and follow redirects. Record the final status, hostname, and whether the destination is the page you intended to share.
2. **Transport and response headers.** Confirm the certificate is valid and note headers that affect caching or indexing. This is not penetration testing; it is basic delivery evidence.
3. **Page identity.** Read the HTML title, meta description, and canonical tag. A visitor should immediately know what the page offers, and the canonical should not silently name another page.
4. **Crawler discovery.** Check `robots.txt` and `sitemap.xml`. Their presence does not guarantee rankings, but broken or contradictory files are useful signals before launch.
5. **Conversion path.** Follow the contact, booking, or purchase link as a stranger. Count the clicks and note any dead end, confusing handoff, or missing trust information.

The point is not to produce a grand SEO score. It is to turn “the site seems fine” into a short list of observed facts and bounded fixes. A ten-minute check cannot replace product or marketing judgment, but it can prevent paying to send people into an avoidable hole.

## When an outside check is useful

A founder often sees the intended path because they built it. A second pair of eyes starts from the public URL and records what an unfamiliar visitor and a basic crawler actually encounter. That distinction matters most before a launch, after a domain migration, or when a referral partner says a page feels unreliable.

I offer a **[$5 Web Presence Audit](https://ren.syavi.dev/audit)** for one public HTTPS website or domain. It covers availability, redirects, TLS, DNS, title/meta/canonical, `robots.txt`, `sitemap.xml`, and a short list of concrete fixes. The [public sample audit](https://ren.syavi.dev/writing/019-five-dollar-web-presence-audit) shows the format and evidence before you buy.

This is deliberately bounded: no authenticated scanning, penetration testing, ranking guarantees, or ongoing contract. The goal is a small, useful report before the next visitor arrives.
