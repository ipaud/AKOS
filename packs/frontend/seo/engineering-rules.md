# Engineering Rules — SEO Pack

Checkable in the artifact. `★` marks the two rules that are floor business rather than
discoverability: markup must not misrepresent the page, and nothing here overrides
accessibility. Everything else is Level 1 guidance about documented, enforceable
mechanisms — not about ranking. Parenthetical codes cite the principle in
[principles.md](principles.md).

## Crawl and index control

- SEO1. `robots.txt` is used to control *fetching* only. Pages that must stay out of search
  results carry a `noindex` directive and remain fetchable so it can be read. (P6)
- SEO2. No URL is simultaneously disallowed in `robots.txt` and expected to be
  de-indexed — the combination is self-defeating and is a finding wherever it appears. (P6)
- SEO3. CSS, JavaScript, and image assets required to render a page are fetchable. Blocking
  them means the page is assessed in a form nobody ships. (P5, P6)
- SEO4. Staging, preview, and non-production environments are kept out of search by
  authentication or `noindex` — never by `robots.txt` alone, and never by hoping. (P6)
- SEO5. An XML sitemap lists canonical, indexable URLs only: no redirects, no `noindex`
  pages, no 404s, no non-canonical variants. A sitemap contradicting the rest of the site
  is a signal against it. (P9)
- SEO6. The sitemap is generated from the routing or content source, never maintained by
  hand, and is referenced from `robots.txt`. (P9)
- SEO7. Faceted, filtered, sorted, and paginated URL spaces have a stated policy: which
  combinations are indexable, which are canonicalized to a parent, which are not linked at
  all. Absent a policy, the default is an unbounded crawl space. (P7)
- SEO8. Search-result pages and infinite parameter combinations are not indexable. (P7)

## Rendering and indexability

- SEO9. Primary content and primary links exist in the initially served HTML. Content that
  appears only after client-side data fetching is treated as at risk of never being
  indexed. (P5)
- SEO10. Content behind an interaction — a tab, an accordion, a "load more" — is present in
  the markup even when visually collapsed, or it is accepted as unindexed and that
  acceptance is recorded. (P5)
- SEO11. Navigation uses real anchors with `href` attributes. A click handler on a
  non-anchor element is not a link, and is not followable — this is also the
  [wcag](../../ux/wcag/README.md) requirement, arriving from the other direction. (P14)
- SEO12. Rendering strategy per route is a deliberate choice recorded somewhere: static,
  server-rendered, or client-only. "Whatever the framework defaulted to" is not a
  choice. (P5)
- SEO13. Indexability is verified by fetching the page as a crawler would and reading the
  result, not by viewing source in a browser that already ran the JavaScript. (P4)

## URL identity

- SEO14. One canonical form is chosen and enforced by redirect: protocol, host (`www` or
  not), trailing slash, and letter case. Every other form 301s to it. (P8)
- SEO15. Tracking and campaign parameters never produce a separate indexable URL; the
  canonical points at the clean form. (P8)
- SEO16. Every indexable page declares a self-referencing canonical. (P9)
- SEO17. Canonical declarations, internal links, sitemap entries, and redirects all agree.
  A canonical pointing somewhere the site never links to is a contradiction. (P9)
- SEO18. Canonicals point at a page that returns 200 and is itself indexable — never at a
  redirect, a 404, or a `noindex` page. (P9)
- SEO19. URLs are stable, readable, and describe the content. Identifiers are acceptable;
  session state, ordering state, and implementation detail are not. (P8, P10)

## Metadata

- SEO20. Every indexable page has a unique, specific `<title>` describing that page
  rather than the site. Duplicated titles across a template are a finding. (P13)
- SEO21. Meta descriptions are written as a promise to a person scanning results, are
  unique per page, and are absent rather than auto-generated filler. (P13)
- SEO22. One `<h1>` per page, stating what the page is; heading levels nest without
  skipping. (P14)
- SEO23. Link text describes the destination and survives being read out of context. "Click
  here" and "read more" fail this and the accessibility rule simultaneously. (P14)
- SEO24. Images carry alternative text describing content and function; decorative images
  carry empty alt. Keyword-stuffed alt text is a defect against both this pack and
  [wcag](../../ux/wcag/README.md). (P14, P3)
- SEO25. Social preview metadata (`og:*` and equivalents) is set for pages likely to be
  shared, with an image of the declared dimensions, and is verified by rendering a real
  preview rather than assumed. (P13)
- SEO26. `<html lang>` is set and correct on every page. (P14)

## Structured data

- SEO27 ★. Structured data describes only what is visible on the page. Marking up reviews,
  prices, availability, or authorship the page does not show is misrepresentation, and it
  is the one part of this domain that is actively enforced. (P12)
- SEO28. Structured data validates against the vocabulary and against the consuming
  platform's requirements, checked with a testing tool before release rather than after a
  warning arrives. (P11)
- SEO29. Types used match what the page actually is. A generic type applied to everything
  communicates nothing. (P11)
- SEO30. Structured data is generated from the same data the page renders from, never
  hand-maintained in parallel — parallel copies drift, and the drift is SEO27. (P12)
- SEO31. Absence of an enhanced result is not treated as a markup bug. Eligibility is not
  entitlement, and adding more types does not increase it. (P11)

## International and duplicate content

- SEO32. Where multiple language or regional versions exist, each declares reciprocal
  `hreflang` annotations, including a self-reference. Non-reciprocal annotations are
  ignored. (P9)
- SEO33. `hreflang` values are valid language and region codes; a region alone is not a
  language. (P9)
- SEO34. Localized pages canonicalize to themselves, not to the original-language
  version. (P9)
- SEO35. Genuinely duplicated content across a site is consolidated by canonical or
  redirect rather than left to be resolved by someone else. (P8)

## Migrations

- SEO36. Any URL change ships with a redirect map covering every previously indexable URL,
  produced *before* the change and derived from real data — analytics, logs, sitemap — not
  from memory. (P10)
- SEO37. Redirects are permanent (301/308) where the move is permanent, and go directly to
  the final destination. Chains are collapsed; loops are a release blocker. (P10)
- SEO38. Redirects preserve the specific target. Bulk-redirecting a removed section to the
  homepage is treated as a soft 404 and loses the page's identity. (P10)
- SEO39. Removed content returns 404 or 410 deliberately, rather than a 200 with an
  "not found" message — a soft 404 keeps a dead page indexed. (P10)
- SEO40. After a migration, indexed-URL counts, crawl errors, and redirect behavior are
  checked against a pre-migration baseline captured for the purpose. (P10, P4)

## Monitoring

- SEO41. The property is verified in a search console and someone reads it — coverage
  errors, manual actions, and structured-data warnings are signals nobody else will
  forward to you. (P4)
- SEO42. Indexability is asserted by a test in CI for the routes that matter: canonical
  present and self-referencing, `noindex` absent from public routes and present on private
  ones, sitemap parses. A directive nobody checks eventually inverts. (P4)
- SEO43. Page experience is measured under
  [performance/core-web-vitals](../../performance/core-web-vitals/README.md), not
  re-derived here. (P16)

## Floor

- SEO44 ★. No technique in this pack is applied at the cost of accessibility, honesty to
  the user, or performance. Hidden text, cloaked content, doorway pages, and
  keyword-stuffed alt attributes all fail the safety floor before they fail a search
  policy. (P3)

## React and Next-class framework mapping

Rules for the default stack. They do not replace the ones above — they say where the
framework already handles one and where it quietly does not.

- SEO45. Routes whose content matters for discovery are statically generated or
  server-rendered. A client-only route is a deliberate decision with indexing accepted as
  a cost. (P5, SEO12)
- SEO46. Metadata is produced by the framework's metadata API per route rather than
  injected client-side after hydration. (P13, SEO20)
- SEO47. The sitemap and `robots.txt` are generated by the framework from the route
  manifest, so a new route cannot be missing from them. (P9, SEO6)
- SEO48. Preview and branch deployments are excluded from indexing by configuration, not
  by remembering — every preview URL is a duplicate of production otherwise. (SEO4)
- SEO49. Client-side navigation still updates title, description, and canonical; a
  single-page transition that leaves stale metadata is invisible in a browser and visible
  to a crawler. (P13)
- SEO50. Structured data is emitted server-side from the same source the page renders
  from. (SEO30)
