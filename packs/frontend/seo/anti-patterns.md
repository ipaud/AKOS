# Anti-Patterns — SEO Pack

Named failure modes, how to spot them, and what to do instead. The last two are failures
of *applying* this domain, and in SEO specifically they are the likelier problem.

## Disallow plus noindex

**Detect:** a path blocked in `robots.txt` that the team also expects to be out of search
results; pages still appearing months after "we blocked them".
**Why it fails:** blocking fetching means the `noindex` directive can never be read. The
URL stays known, stays listed, and now cannot even be described.
**Fix:** pick one. To de-index, allow fetching and serve `noindex`. To hide from crawling
entirely, accept that already-known URLs may persist and use authentication instead. (SEO1,
SEO2)

## The empty shell

**Detect:** fetching the page without executing JavaScript returns a `<div id="root">` and
nothing else; navigation is click handlers on non-anchors.
**Why it fails:** content that arrives only after client-side fetching may never be
indexed, and links that are not anchors are not followable, so the pages behind them are
never discovered either.
**Fix:** static or server rendering for anything a stranger should land on, and real
anchors with `href` everywhere. Verify by fetching as a crawler, not by viewing source
after hydration. (SEO9, SEO11, SEO13, SEO45)

## Four URLs, one page

**Detect:** `http` and `https`, `www` and bare, trailing slash and not, mixed case, and
`?utm_source=` variants all serving the same content with a 200.
**Why it fails:** every signal about that page is split across identities, and the site
contradicts itself about which one is real.
**Fix:** choose one canonical form, redirect the rest permanently, self-reference the
canonical, and keep tracking parameters out of the indexable set. Cheap on day one, a
migration later. (SEO14, SEO15, SEO16)

## The canonical that contradicts the site

**Detect:** a canonical pointing at a URL that redirects, 404s, is `noindex`, or that no
internal link ever references.
**Why it fails:** a canonical is a hint weighed against internal links, sitemaps, and
redirects. When they disagree, the resolution is not yours to make.
**Fix:** make canonical, links, sitemap, and redirects state the same thing. (SEO17,
SEO18)

## Structured data that lies

**Detect:** review markup on a page with no visible reviews; price or availability markup
that does not match what is shown; author markup on an unattributed page. Usually because
the markup is maintained separately from the content.
**Why it fails:** it misrepresents the page — the one part of this domain that is actively
enforced rather than advisory, with penalties attached.
**Fix:** generate structured data from the same data the page renders, so it cannot drift.
If the page does not show it, do not claim it. (SEO27, SEO30)

## The staging site in the index

**Detect:** preview, staging, or branch deployment URLs appearing in search results;
exclusion attempted with `robots.txt` alone.
**Why it fails:** every preview is a full duplicate of production competing with it, and
`robots.txt` does not remove what is already known.
**Fix:** authentication, or `noindex` applied by environment configuration so a new
deployment cannot forget it. (SEO4, SEO48)

## Migration by homepage redirect

**Detect:** a restructure where every old URL 301s to `/`; or old URLs simply 404 with no
map; or a chain of three redirects to reach the destination.
**Why it fails:** a bulk homepage redirect is treated as a soft 404, so the page's identity
is lost rather than transferred — this is where organic traffic actually disappears, not in
markup.
**Fix:** a redirect map to specific destinations, derived from analytics and logs before
the change, permanent and direct, with a pre-migration baseline to check against
afterwards. (SEO36, SEO37, SEO38, SEO40)

## The soft 404

**Detect:** removed content returning 200 with a "sorry, not found" message; a category
page that renders an empty list with a success status.
**Why it fails:** a 200 says "this is a real page", so it stays indexed as a real page with
no content.
**Fix:** return 404 or 410 deliberately. (SEO39)

## Keywords in the alt attribute

**Detect:** alt text listing terms rather than describing the image; hidden text; content
served differently to crawlers than to people.
**Why it fails:** it fails the safety floor before it fails any search policy — a screen
reader user gets a keyword list instead of a description — and every technique of this
shape has since been penalized anyway.
**Fix:** describe the image. The accessible answer and the discoverable answer are the same
answer. (SEO24, SEO44)

## Optimizing for a ranking theory

**Detect:** work justified by keyword density, an "optimal" title length, or a claim about
what "the algorithm rewards"; a review comment saying a page "would rank better if".
**Why it fails:** these are Level 4 claims about an unpublished system. They cannot be
verified, cannot be refuted, and displace work on mechanisms that are documented.
**Fix:** restrict decisions to what is documented and checkable — access, rendering,
identity, markup validity. Stop at "are we indexable"; ranking is not something this pack,
or anyone outside the search engine, can tell you. (P1, P2)

## Auditing a site with no public surface

**Detect:** an SEO review of an application entirely behind a login, producing
recommendations about titles and structured data for pages no crawler will ever fetch.
**Why it fails:** it manufactures work, and it buries the one finding that actually
mattered — whether anything is leaking into the index that shouldn't.
**Fix:** confirm exclusion, say there is nothing else to audit, and stop.
([decision-framework](decision-framework.md), "does discoverability matter for this
surface")
