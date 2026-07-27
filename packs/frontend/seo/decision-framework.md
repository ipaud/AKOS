# Decision Framework — SEO Pack

The choices this domain presents, and how to settle each one.

## Does discoverability matter for this surface?

| Surface | Answer |
|---|---|
| Marketing site, landing page, docs, blog | **Yes.** Organic discovery is the point. |
| Public product pages behind no auth | **Yes**, for the pages a stranger could land on. |
| App behind a login | **No.** Nothing indexable exists. Ensure it stays out (SEO4) and stop. |
| Internal tool | **No**, and it should be actively excluded. |
| Prototype | **No** — but choose a rendering strategy anyway (SEO12), because retrofitting it later is the expensive version. |

If a surface has no public pages, this pack is a five-minute exclusion check, not a
project.

## Which stage is broken?

The whole diagnostic method. Work down; stop at the first failure.

```
1. DISCOVER — does anything link to it? Is it in the sitemap?
      not found at all → internal linking or sitemap
2. CRAWL — can the crawler fetch it? robots.txt, auth, status code, server errors
      fetch blocked → SEO1-SEO4
3. RENDER — does the fetched HTML contain the content and the links?
      empty shell → SEO9, SEO12, SEO45
4. INDEX — is it allowed in, and is it the version chosen among duplicates?
      excluded → noindex present? canonical pointing elsewhere? (SEO16-SEO18)
5. SERVE — is it shown, and how?
      shown but plain → structured data eligibility (SEO27-SEO31), not a bug
      not shown → this pack stops here (P1)
```

A finding that cannot be placed on this ladder is not a finding from this pack.

## Rendering strategy per route

| Route content | Strategy | Why |
|---|---|---|
| Marketing, docs, blog — same for everyone | Static | Fastest, most reliably indexed, cheapest. |
| Public but personalized or frequently changing | Server-rendered | Content present in the response; freshness preserved. |
| Public, huge, long tail | Static with incremental regeneration | Build time stays bounded. |
| Behind auth, or genuinely interactive | Client | Indexing is irrelevant; don't pay for SSR. |

Rule of thumb: **if a stranger should be able to land on it from a search result, the
content is in the response.** Everything else is a performance decision, not this pack's.

## How much structured data?

1. **Is there a documented enhanced result for this page type?** No → skip. Generic markup
   with no consuming feature is effort with no mechanism behind it.
2. **Does the page visibly show everything the markup would claim?** No → stop. SEO27 is
   the one enforced rule in the domain (P12).
3. **Can it be generated from the same data the page renders?** No → fix that first;
   hand-maintained parallel markup drifts into SEO27 territory.
4. Then add it, validate it, and treat absence of an enhancement as normal (SEO31).

## Migration: the only high-stakes moment

Everything else in this pack is incremental. A URL change is not.

**Before:** capture indexed URLs, top organic landing pages, and current crawl errors.
That baseline is the only way to tell afterwards whether something broke (SEO40).
**Map:** every previously indexable URL to its specific new destination, derived from
analytics and logs rather than memory (SEO36). Bulk-redirecting to the homepage is a soft
404 (SEO38).
**Ship:** permanent redirects, direct, no chains, no loops (SEO37).
**After:** re-check the baseline. Expect a temporary dip; a sustained one means the map
missed something.

If a migration cannot get this treatment, the honest options are to delay it or to accept
a stated traffic loss — not to ship and hope.

## Where SEO appears to conflict with something else

| Apparent conflict | Resolution |
|---|---|
| "More keywords in alt text" vs accessibility | Accessibility wins, and the SEO advice was folklore. Alt text describes the image (SEO24, R1). |
| Hidden text or cloaked content "for crawlers" | Never. Fails the floor before it fails a search policy (SEO44). |
| SSR "for SEO" on a route behind auth | No indexing benefit exists. Decide it on performance grounds instead. |
| Interstitials, popups, consent walls | Consent obligations are real ([privacy](../../security/privacy/README.md)); intrusive interstitials are a page-experience problem. Design one that satisfies both. |
| Infinite scroll vs crawlable pagination | Provide real paginated URLs underneath the scroll. Both audiences win. |

The pattern: genuine conflicts are rare, and an apparent one usually means the SEO side of
it was never documented in the first place (P3).

## Profile modulation

- **Prototype** — exclusion check only (SEO4), plus a recorded rendering choice.
- **Startup MVP** — the High items: canonical form enforced, titles unique, content in the
  response, previews not indexable, and a redirect map the day URLs change.
- **Production** — full checklist, CI assertions on indexability (SEO42), search console
  monitored.
- **Enterprise** — plus international correctness (SEO32–SEO34) and a migration baseline
  procedure that exists before it is needed.

## When NOT to use this pack

- **No public surface.** Check exclusion, leave.
- **The question is "why aren't we ranking".** Outside what this pack claims (P1). It can
  tell you whether you are *indexable*; it cannot tell you where you place.
- **The question is whether the content is any good.** That is
  [gov-uk-content-design](../../content/gov-uk-content-design/README.md) and, further
  back, a product question (P17).
- **The question is page speed.** [core-web-vitals](../../performance/core-web-vitals/README.md).
- **Someone wants a "quick SEO audit" of an app behind a login.** There is nothing to
  audit; say so rather than producing a report.
