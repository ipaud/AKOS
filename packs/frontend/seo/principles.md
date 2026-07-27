# Principles — SEO Pack

Durable rules for making a site findable, restricted to what is **documented and
enforceable**. This domain is the most polluted by unverifiable folklore in the whole
corpus, so the pack's first commitment is about what it refuses to contain. The `SEO*`
codes in [engineering-rules.md](engineering-rules.md) derive from these.

## What this pack will and won't claim

- **P1 — You control access and comprehension. You do not control ranking.** Directives
  (`robots.txt`, `noindex`, canonical hints, sitemaps, structured data) are how a site
  states what it wants understood. Where it then appears is not yours to set. Every rule
  here is about the first thing; none is about the second.
- **P2 — Ranking-factor speculation is Level 4 and stays out of the pack entirely.**
  Not demoted, not caveated — excluded. "Keyword density", "optimal title length for
  ranking", "the algorithm rewards X" are blog claims about an unpublished system. Per
  [source-policy](../../../core/source-policy.md), a Level 4 idea may never be a pack's
  basis, and an engineering decision made on one is unfalsifiable by construction.
- **P3 — When SEO advice conflicts with accessibility, performance, or honesty toward the
  user, those win.** Every technique that once traded a real user's experience for a
  crawler's attention has since been penalized. The interests are aligned far more often
  than folklore suggests; where they appear to diverge, the divergence is usually a sign
  the advice was folklore.

## The pipeline

- **P4 — Indexing is a pipeline — discover, crawl, render, index, serve — and every
  problem is one stage failing.** Naming the failing stage *is* the diagnosis; skipping
  that step is how teams end up "doing SEO" by adding tags to a page a crawler never
  fetched.
- **P5 — If it is not in the HTML the crawler ends up with, it does not exist.** Content
  that requires interaction, arrives after an event, or depends on client-side data
  fetching may never be seen. Rendering strategy is an indexing decision before it is a
  performance one.
- **P6 — Crawling and indexing are separate controls, and confusing them is the classic
  self-inflicted wound.** `robots.txt` governs fetching. `noindex` governs inclusion. A
  page blocked from fetching can never be read to discover it asked not to be indexed —
  so the two directives combined achieve the opposite of the intent.
- **P7 — Crawl budget is spent on what you let it be spent on.** Infinite parameter
  combinations, faceted navigation, and session URLs consume attention that never reaches
  the pages that matter. The fix is at the URL design level, not in a directives file.

## URLs and identity

- **P8 — One piece of content, one URL.** Every avoidable variant — trailing slash,
  protocol, `www`, casing, tracking parameters, ordering parameters — splits the signals
  for one thing across several identities. This is the most common structural problem and
  the cheapest to prevent at design time.
- **P9 — A canonical declaration is a hint that must be corroborated by the rest of the
  site.** It competes with internal links, sitemaps, and redirects. A canonical pointing
  one way while every link points another is a contradiction, and the contradiction is
  resolved by whoever reads it, not by you.
- **P10 — A URL is a long-lived interface, and changing one is a migration.** Redirects
  are how identity survives a restructure. Migrations are where organic traffic is
  actually lost — not through markup, through a redirect map nobody wrote.

## What markup can and cannot do

- **P11 — Structured data buys eligibility, never placement.** Correct markup makes a page
  *able* to be shown as an enhanced result. It does not cause it, and no amount of it
  compensates for the underlying page.
- **P12 — Markup that describes something the page does not show is a lie with a
  penalty attached.** Structured data must match visible content. This is the one place in
  the domain where the rule is enforced rather than advisory.
- **P13 — Metadata is written for a person reading a result, not for a parser.** A title
  and description are a promise about what the page contains; treat them as interface copy
  — see [content/ux-writing](../../content/ux-writing/README.md) — not as keyword
  containers.
- **P14 — Semantic HTML does the structural work, and you should be writing it
  anyway.** One `h1` describing the page, headings that nest, links with text that
  survives being read out of context, images with real alternative text. There is no
  separate "SEO markup layer" — see [frontend/html](../html/README.md).

## Context

- **P15 — The mobile rendering is the one that counts.** Where a small-screen experience
  hides content the desktop shows, the hidden version is the version being assessed.
- **P16 — Page experience signals are work you already owe the user.** Loading, stability,
  interactivity, HTTPS, no intrusive interstitials — all of it belongs to
  [performance/core-web-vitals](../../performance/core-web-vitals/README.md) and
  [ux/wcag](../../ux/wcag/README.md). This pack points there rather than restating it, and
  a team doing that work has done the part of SEO that is measurable.
- **P17 — Nothing here substitutes for having something worth finding.** Discoverability
  is a distribution problem layered on a product problem. A site nobody wants, made
  perfectly crawlable, is a crawlable site nobody wants.

## Scope

This pack covers technical discoverability: crawl and index control, URL identity,
canonicalization, structured data, metadata, internationalization, and migration safety.
It does not cover content strategy or writing quality
([content/gov-uk-content-design](../../content/gov-uk-content-design/README.md)), the
performance metrics behind page experience
([performance/core-web-vitals](../../performance/core-web-vitals/README.md)), semantics
and forms ([frontend/html](../html/README.md)), responsive layout
([mobile/responsive-web](../../mobile/responsive-web/README.md)), paid acquisition, or
anything about ranking.
