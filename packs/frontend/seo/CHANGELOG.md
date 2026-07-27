# Changelog — seo

## [1.0.0] — 2026-07-27

### Added

- First complete version. Authority level 1 (Google Search Central, IETF RFC 9309,
  schema.org, sitemaps.org), review cadence 545 days (`review_after: 2028-01-23`). Cleared
  the source intake gate on a verified gap: `schema.org`, `sitemap`, `robots.txt`,
  `structured data`, `rich result`, `hreflang`, `noindex`, `open graph`, `title tag`, and
  `page experience` all returned zero across the 58-pack corpus. `canonical` returned 41
  hits, every one in the "canonical ruling" sense rather than `rel=canonical`.
- Principles P1–P17 and engineering rules SEO1–SEO50 across crawl and index control,
  rendering and indexability, URL identity, metadata, structured data, internationalization,
  migrations, monitoring, and a React/Next-class framework mapping.

### The pack's organising decision: what it refuses to contain

**Ranking is excluded entirely — not demoted, excluded.** How results are ordered is
unpublished, so every claim about it is a Level 4 assertion about a system nobody outside
the search engine can inspect, and `core/source-policy.md` bars a Level 4 source from being
a pack's basis. There is no honest version of this pack that includes that material.

This is the domain with the widest gap in the corpus between how much advice exists and how
much is verifiable, so the line is enforced in five places rather than stated once:

- P1 and P2 in the principles.
- A reviewer-discipline rule requiring every finding to **name the pipeline stage** it
  breaks — discover, crawl, render, index, serve. A finding that cannot name one is
  folklore and is dropped.
- A second reviewer rule forbidding ranking claims outright in the review lens.
- A scoring rule that no deduction may rest on a ranking claim.
- An anti-pattern, *optimizing for a ranking theory*, naming the review comment that
  triggers it ("this would rank better if…").

`references.md` states exactly what Level 1 covers here — documented, enforceable
mechanisms: crawl directives, indexing controls, canonicalization, structured-data
eligibility requirements, spam policies with real penalties. Google is the platform owner
for appearing in Google Search, the same basis on which `performance/web-dev`,
`ux/material-design` and `ux/apple-hig` are Level 1, and RFC 9309 is a genuine IETF RFC.

### Other notable choices

- **Only two rules are starred, and neither is discoverability.** SEO27 (structured data
  describes only what the page shows — the one actively enforced rule in the domain) and
  SEO44 (nothing applied at the cost of accessibility, honesty, or performance). Hidden
  text and keyword-stuffed alt attributes fail the safety floor before they fail any search
  policy.
- **The pipeline is the diagnostic method, not a description.** The decision framework's
  central artifact is a five-stage ladder — discover, crawl, render, index, serve — worked
  top-down until the first failure. Naming the failing stage *is* the diagnosis; skipping
  it is how teams end up adding tags to a page a crawler never fetched.
- **`n/a` for surfaces with no public pages.** An application entirely behind a login
  scores `n/a` rather than a low number, and the decision framework says explicitly that
  this is a five-minute exclusion check rather than an audit. The matching anti-pattern —
  auditing a site with no public surface — names the failure of producing a report about
  pages no crawler will fetch.
- **Migrations are treated as the only high-stakes moment.** Everything else in the domain
  is incremental; a URL change is not, and it is where organic traffic is actually lost.
  Given a dedicated procedure in the decision framework, a prompt fragment, and four rules
  (SEO36–SEO40) built around capturing a baseline *before* the change.
- Anti-patterns: disallow-plus-noindex, the empty shell, four URLs one page, the canonical
  that contradicts the site, structured data that lies, the staging site in the index,
  migration by homepage redirect, the soft 404, keywords in the alt attribute, plus the two
  failures of applying the domain.

### Scope boundary

Recorded against `packs/frontend/html` (semantics and forms in depth),
`packs/performance/core-web-vitals` (page experience, scored there and never twice),
`packs/mobile/responsive-web` (responsive layout, and the mobile-first *CSS* sense of a
colliding term), `packs/content/gov-uk-content-design` (whether the content is any good),
and `packs/ux/wcag` (the accessibility rules SEO11, SEO23 and SEO24 arrive at from the
other direction).
