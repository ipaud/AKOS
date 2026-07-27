# Prompt Fragments — SEO Pack

Copy-paste blocks for injecting this pack into an agent prompt. Read this file first — in
most tasks the build-mode block is all that needs loading.

## Fragment: build-mode constraint block

```text
SEO CONSTRAINTS (Level 1 on documented mechanisms only — this pack says NOTHING about
ranking, and neither should you):

Scope check first
- No public pages? Confirm the app is excluded from indexing, then stop. Don't audit
  pages no crawler will fetch.

Crawl and index
- robots.txt controls FETCHING. noindex controls INCLUSION. Never combine disallow with
  an expectation of de-indexing — a blocked page can't be read to discover it asked to be
  excluded.
- Render-critical CSS/JS/images must be fetchable.
- Preview/staging excluded by auth or environment config, never by robots.txt alone.
- Sitemap: generated from routes, canonical indexable URLs only, referenced from
  robots.txt.

Rendering
- If a stranger should land on it from a search result, the content is in the served HTML.
- Real anchors with href for navigation. A click handler is not a link, and pages behind
  one are never discovered.
- Rendering strategy per route is a recorded decision, not a framework default.
- Verify by fetching as a crawler would — not view-source after hydration.

URL identity
- ONE canonical form enforced by redirect: protocol, host, trailing slash, case.
- Self-referencing canonical on every indexable page, pointing at a 200 indexable page.
- Canonical, internal links, sitemap and redirects must all agree.
- Tracking parameters never create a separate indexable URL.

Metadata
- Unique specific <title> per page. One <h1>. Headings nest without skipping.
- Descriptions written for a person scanning results, or absent — never filler.
- Link text survives being read out of context. Alt text describes the image.

Structured data
- Only where a documented enhancement consumes it.
- MUST describe only what the page visibly shows — this is the one enforced rule here.
- Generated from the same data the page renders from, never a hand-maintained parallel copy.

Migrations (the only high-stakes moment)
- Capture a baseline BEFORE: indexed URLs, top organic landing pages, crawl errors.
- Redirect map covering every previously indexable URL, to its SPECIFIC replacement.
- Permanent, direct, no chains, no loops. Bulk-redirecting to the homepage is a soft 404.
- Removed content returns 404/410, never 200 with a "not found" message.

FLOOR: nothing here at the cost of accessibility, honesty, or performance. Hidden text,
cloaking, and keyword-stuffed alt attributes fail the safety floor before they fail any
search policy.
```

## Fragment: review lens

```text
Review this surface against the AKOS SEO pack (frontend/seo).

Two rules bind the review itself:

1. NAME THE PIPELINE STAGE. Every finding states which of discover / crawl / render /
   index / serve it breaks. If none applies, it is not a finding — drop it.
2. NEVER REPORT RANKING. "This would rank better if…" is outside what the pack claims and
   outside what anyone can verify. Report the mechanism, not the outcome.

Only two findings are CRITICAL, and both are floor rather than discoverability: structured
data describing content the page doesn't show (SEO27), and any technique costing
accessibility, honesty, or performance (SEO44).

Then in order: migration without a redirect map, content absent from served HTML on public
routes, navigation that isn't real anchors, disallow-plus-noindex, indexable previews, no
enforced canonical form, soft 404s.

If the surface has no public pages, report only whether anything leaks into the index and
say there is nothing else to audit.

For each finding: rule code, file/line, the pipeline stage broken, and the smallest fix.
```

## Fragment: migration checklist

```text
This change alters URLs. Before it ships:

1. Baseline captured? Indexed URLs, top organic landing pages, current crawl errors.
   Without it you cannot tell afterwards what broke.
2. Redirect map covers every previously indexable URL — derived from analytics and logs,
   not from memory.
3. Each redirect goes to the SPECIFIC replacement. Anything pointing at the homepage is a
   soft 404 in disguise.
4. Permanent status codes, direct, no chains, no loops.
5. Genuinely removed content returns 404 or 410, not 200.
6. Sitemap regenerated; canonicals updated; internal links updated to the new URLs so the
   site doesn't contradict its own redirects.
7. After: re-check the baseline. A temporary dip is expected; a sustained one means the
   map missed something.

If this treatment isn't possible, the honest options are to delay or to accept a stated
traffic loss — not to ship and hope.
```

## One-liner (for tight token budgets)

```text
SEO floor: no public pages → confirm exclusion and stop. Otherwise: name the failing
pipeline stage (discover/crawl/render/index/serve) or it isn't a finding, and never claim
anything about ranking. robots.txt = fetching, noindex = inclusion, never both on one URL.
Content and real anchors in the served HTML for anything a stranger should land on. One
canonical URL form enforced by redirect, self-referencing canonical, canonical + links +
sitemap + redirects all agreeing. Unique specific titles, one h1. Structured data only
where an enhancement consumes it, only describing what's visible, generated from rendered
data. URL changes need a redirect map to specific targets built from a pre-change baseline.
Never at the cost of accessibility or honesty.
```
