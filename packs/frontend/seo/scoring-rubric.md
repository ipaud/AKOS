# Scoring Rubric — SEO Pack

Feeds the product and maintainability dimensions
([scoring/product-score.md](../../../scoring/product-score.md),
[scoring/overall-score.md](../../../scoring/overall-score.md)). Page experience scores
under [performance/core-web-vitals](../../performance/core-web-vitals/README.md), never
twice.

Two things this rubric deliberately refuses to do: score ranking, and score a surface with
no public pages.

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| Structured data describing content the page does not show | −40 (CRITICAL) |
| Hidden text, cloaking, doorway pages, or keyword-stuffed alt attributes | −40 (CRITICAL) |
| Migration shipped with no redirect map, or old URLs bulk-redirected to the homepage | −25 (HIGH) |
| Primary content or navigation absent from the served HTML on a public route | −15 (HIGH) |
| Navigation that is not real anchors, so pages behind it are undiscoverable | −15 (HIGH) |
| `robots.txt` disallow combined with an expectation of de-indexing | −10 (HIGH) |
| Render-critical CSS/JS blocked from fetching | −10 (HIGH) |
| Preview or staging environment indexable | −10 (HIGH) |
| No single enforced canonical URL form (protocol, host, slash, case) | −10 (HIGH) |
| Canonical pointing at a redirect, 404, or `noindex` page | −10 (HIGH) |
| Removed content returning 200 instead of 404/410 | −10 (HIGH) |
| Redirect chains or loops | −6 (MEDIUM) |
| Missing or duplicated `<title>` across indexable pages | −6 (MEDIUM) |
| No self-referencing canonical on indexable pages | −6 (MEDIUM) |
| Sitemap containing redirects, `noindex` pages, or 404s; or hand-maintained | −6 (MEDIUM) |
| Unbounded crawl space — facets, parameters, search pages indexable with no policy | −6 (MEDIUM) |
| Structured data hand-maintained in parallel with the content it describes | −6 (MEDIUM) |
| Rendering strategy per route never decided, just inherited from a default | −4 (MEDIUM) |
| Indexability never verified by fetching as a crawler | −4 (MEDIUM) |
| Heading structure broken; no `h1`, or levels skipped | −4 (MEDIUM) |
| Non-reciprocal or invalid `hreflang`; localized pages canonicalizing to the original | −4 (MEDIUM) |
| No CI assertion on indexability for routes that matter | −4 (MEDIUM) |
| Link text that does not survive being read out of context | −2 (LOW) |
| Missing or auto-generated filler meta descriptions | −2 (LOW) |
| Missing `<html lang>`, missing social preview metadata | −2 (LOW) |
| No search console property, or nobody reads it | −2 (LOW) |

## Caps and floors

- Any CRITICAL: score ≤ 59 (Blocked band), per
  [core/scoring-model.md](../../../core/scoring-model.md). Both CRITICALs here are safety
  floor rather than discoverability — misrepresentation and user-hostile technique.
- **`n/a` when the surface has no public pages.** An application entirely behind a login
  scores `n/a`, not a low number. The only check that applies is whether anything is
  leaking into the index; that is pass/fail, not a score.
- **`n/a` under Prototype**, except the exclusion check.
- **No deduction may be justified by a ranking claim.** A finding that cannot name the
  pipeline stage it breaks — discover, crawl, render, index, serve — is not scored at all.
  This is the single most important line in the rubric for this domain.
- Page experience and Core Web Vitals are scored by their own pack. Restating them here
  would double-count the same work.

## Anchors

- **95** — one canonical URL form enforced, content in the response, sitemap generated and
  consistent, structured data derived from rendered data, previews excluded by config,
  indexability asserted in CI, and a migration procedure that exists before it is needed.
- **85** — sound; MEDIUM gaps (some duplicated titles, no CI assertion) scheduled.
- **72** — indexable and coherent, but fragile: no canonical form enforced, sitemap drifts,
  rendering strategy inherited rather than chosen.
- **60** — public content that a crawler cannot reliably read, or a URL space nobody
  controls.
- **≤ 40** — the site misrepresents itself, or a migration has already lost the identity of
  its pages.
