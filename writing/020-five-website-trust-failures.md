# Five Website Trust Failures a $5 Audit Can Catch

*2026-08-25*

A website can be online and still lose a visitor in seconds. The most expensive failures are often small, visible signals: a broken HTTPS path, a redirect that never settles, a blank search result, or no clear way to contact the person behind the site.

This guide is a fast self-check for founders and small businesses. It is not penetration testing or an SEO ranking promise. It focuses on public, observable trust and availability signals.

## 1. HTTPS is missing or inconsistent

Open the exact URL in a private browser window. Confirm that it loads over `https://`, that the certificate is valid, and that the HTTP version redirects to HTTPS. Also test the hostname with and without `www`; an abandoned alternate hostname is a common source of warnings and lost visitors.

Useful check: `curl -IL http://example.com` and `curl -IL https://example.com`. Look for a final `200` page and a deliberate redirect chain.

## 2. Redirects loop or point at the wrong place

A redirect should take a visitor to one canonical destination. Several hops are slower; a loop is fatal. Check the apex domain, `www`, trailing slash variants, and the most important page linked from ads or profiles.

Useful check: `curl -IL --max-redirs 10 https://example.com`. Record every `Location` header and the final status.

## 3. The page has no useful title or description

Search engines and shared links need a clear description. View the HTML source and confirm that `<title>` says what the business does—not just “Home”—and that the meta description explains the audience and next action. One useful title is better than keyword stuffing.

Useful check: inspect `<title>`, `<meta name="description">`, and the first heading. They should agree about the page’s purpose.

## 4. Crawlers cannot find the right pages

A missing or contradictory `robots.txt`, sitemap, or canonical tag can hide a site from discovery. Fetch `/robots.txt` and `/sitemap.xml`; then check whether the canonical URL matches the URL visitors actually use. These files should help crawlers, not point them to an old domain or staging host.

Useful check: `curl -i https://example.com/robots.txt` and `curl -i https://example.com/sitemap.xml`.

## 5. The visitor cannot tell what to do next

Technical correctness does not create a customer by itself. Within a few seconds, a visitor should see who the site serves, what is offered, and one obvious next step: contact, book, buy, or request a quote. Test the page on a phone and follow the primary link. A form that silently fails is worse than no form because it creates false confidence.

Useful check: ask someone unfamiliar with the business to name the next action after ten seconds. If they cannot, rewrite the hero section and primary call to action.

## A cheap way to prioritize fixes

Fix failures in this order:

1. Broken or insecure access.
2. Redirect and canonical confusion.
3. Missing discovery metadata.
4. Unclear conversion path.
5. Cosmetic improvements.

If you want an evidence-backed second pair of eyes, the [$5 Web Presence Audit](/audit) reviews one public HTTPS site and returns cited observations plus bounded fixes within 24 hours of verified payment. Read the [public sample audit](/writing/019-five-dollar-web-presence-audit) first to see the format.

The audit is intentionally narrow: it does not access private areas, perform penetration testing, promise rankings, or provide ongoing support.
