# Review Checklist — SEO Pack

Binary checks, each citing its rule. Only two items are CRITICAL, and both are floor
business rather than discoverability. **A finding must name the pipeline stage it breaks**
— discover, crawl, render, index, or serve. A finding that cannot name one is folklore
(P2, P4).

## Critical (blocks in every profile)

- [ ] Structured data describes only what the page visibly shows. (SEO27)
- [ ] No technique here costs accessibility, honesty to the user, or performance — no
      hidden text, cloaking, doorway pages, or keyword-stuffed alt attributes. (SEO44)

## High

- [ ] No URL is both disallowed in `robots.txt` and expected to be de-indexed. (SEO2)
- [ ] Render-critical CSS, JS, and images are fetchable. (SEO3)
- [ ] Non-production environments are kept out of search by auth or `noindex`, not by
      `robots.txt` alone. (SEO4)
- [ ] Primary content and links exist in the initially served HTML. (SEO9)
- [ ] Navigation uses real anchors with `href`. (SEO11)
- [ ] One canonical URL form is enforced by redirect — protocol, host, trailing slash,
      case. (SEO14)
- [ ] Every indexable page declares a self-referencing canonical. (SEO16)
- [ ] Canonicals point at a 200, indexable page — never a redirect, 404, or `noindex`
      page. (SEO18)
- [ ] Every indexable page has a unique, specific `<title>`. (SEO20)
- [ ] A URL change ships with a redirect map covering every previously indexable
      URL. (SEO36)
- [ ] Redirects are permanent where the move is, go direct, and contain no loops. (SEO37)
- [ ] Removed content returns 404/410, not a 200 saying "not found". (SEO39)
- [ ] Structured data is generated from the same source the page renders from. (SEO30)

## Medium

- [ ] `robots.txt` controls fetching only; exclusion from results uses `noindex`. (SEO1)
- [ ] The sitemap lists canonical, indexable URLs only. (SEO5)
- [ ] The sitemap is generated, not hand-maintained, and referenced from
      `robots.txt`. (SEO6)
- [ ] Faceted, filtered, and paginated URL spaces have a stated indexability
      policy. (SEO7)
- [ ] Search-result pages and unbounded parameter combinations are not indexable. (SEO8)
- [ ] Interaction-hidden content is in the markup, or its non-indexing is accepted in
      writing. (SEO10)
- [ ] Rendering strategy per route is a recorded decision. (SEO12)
- [ ] Indexability was verified by fetching as a crawler, not by viewing source after
      hydration. (SEO13)
- [ ] Tracking parameters do not create separate indexable URLs. (SEO15)
- [ ] Canonicals, internal links, sitemap, and redirects agree with each other. (SEO17)
- [ ] One `<h1>` per page; headings nest without skipping. (SEO22)
- [ ] Link text describes the destination out of context. (SEO23)
- [ ] Images have real alternative text; decorative images have empty alt. (SEO24)
- [ ] Structured data validates and uses types matching what the page is. (SEO28, SEO29)
- [ ] Redirects preserve the specific target rather than dumping to the homepage. (SEO38)
- [ ] Post-migration, indexed counts and crawl errors were checked against a baseline
      captured beforehand. (SEO40)
- [ ] Indexability is asserted by a CI test on the routes that matter. (SEO42)

## Low

- [ ] URLs are stable, readable, and free of session or ordering state. (SEO19)
- [ ] Meta descriptions are unique and written for a person, or absent. (SEO21)
- [ ] Social preview metadata is set and verified by a real preview. (SEO25)
- [ ] `<html lang>` is set and correct. (SEO26)
- [ ] `hreflang` annotations are reciprocal, self-referencing, and use valid
      codes. (SEO32, SEO33)
- [ ] Localized pages canonicalize to themselves. (SEO34)
- [ ] Duplicate content is consolidated by canonical or redirect. (SEO35)
- [ ] A search console property is verified and someone reads it. (SEO41)

## Framework (React / Next-class)

- [ ] Discovery-relevant routes are static or server-rendered. (SEO45)
- [ ] Metadata comes from the framework's per-route API, not injected after
      hydration. (SEO46)
- [ ] Sitemap and `robots.txt` are generated from the route manifest. (SEO47)
- [ ] Preview and branch deployments are excluded from indexing by configuration. (SEO48)
- [ ] Client-side navigation updates title, description, and canonical. (SEO49)
- [ ] Structured data is emitted server-side. (SEO50)

## Reviewer discipline

Two rules, both aimed at this domain's specific failure mode:

1. **Name the pipeline stage.** Every finding says which of discover / crawl / render /
   index / serve it breaks. If none applies, it is not a finding from this pack.
2. **Do not report ranking.** "This would rank better if…" is outside what the pack
   claims and outside what anyone can verify (P1, P2). Report the mechanism, not the
   outcome.

## Deferred, not checked here

- Page experience and Core Web Vitals →
  [performance/core-web-vitals](../../performance/core-web-vitals/README.md) (SEO43)
- Content quality and reading level →
  [content/gov-uk-content-design](../../content/gov-uk-content-design/README.md)
- Semantics and forms in depth → [frontend/html](../html/README.md)
