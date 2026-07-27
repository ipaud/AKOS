# Pack: SEO — Discoverability as a Pipeline, Not a Ranking Theory

**Domain:** Frontend · **Authority:** Level 1 (Google Search Central, IETF, schema.org) · **Version:** 1.0.0

Makes a site findable using only what is **documented and enforceable**: crawl and index
control, URL identity, canonicalization, structured data, metadata, internationalization,
and migration safety.

Independent distillation for personal engineering use. Not affiliated with or endorsed by
Google, the IETF, or Schema.org. See [references.md](references.md) for the originals.

## What this pack refuses to contain

**Ranking.** Not demoted to a lower authority level — excluded. How results are ordered is
unpublished, so every claim about it is a Level 4 assertion about a system nobody outside
the search engine can inspect, and
[source-policy](../../../core/source-policy.md) bars a Level 4 source from being a pack's
basis.

This is the domain with the widest gap in the corpus between how much advice exists and how
much of it is verifiable. The pack's usefulness depends on keeping that line visible, so it
appears in the principles, the checklist, the rubric, and the anti-patterns.

**You control access and comprehension. You do not control ranking.** Everything here is
about the first.

## When to load this pack

- A public marketing site, landing page, docs, or blog.
- A URL structure is being designed or **changed** — migrations are the only high-stakes
  moment in this domain.
- Deciding rendering strategy for public routes.
- Adding structured data.
- Confirming an app or preview environment stays *out* of the index.

**When not to:** an application entirely behind a login. That is a five-minute exclusion
check, not an audit — and this pack says so rather than producing a report about pages no
crawler will fetch.

## What's inside

| File | Highlights |
|------|-----------|
| [principles.md](principles.md) | P1–P17. What the pack refuses to claim, the pipeline, URL identity, what markup can and cannot do. |
| [engineering-rules.md](engineering-rules.md) | SEO1–SEO50, including a React/Next-class framework mapping. Only two rules are starred. |
| [decision-framework.md](decision-framework.md) | Does discoverability matter here, **which stage is broken**, rendering strategy per route, how much structured data, the migration procedure, apparent conflicts. |
| [review-checklist.md](review-checklist.md) | By severity, plus two reviewer-discipline rules: name the pipeline stage, never report ranking. |
| [anti-patterns.md](anti-patterns.md) | Disallow-plus-noindex, the empty shell, four URLs one page, structured data that lies, migration by homepage redirect, optimizing for a ranking theory. |
| [scoring-rubric.md](scoring-rubric.md) | `n/a` for login-only surfaces; no deduction may rest on a ranking claim. |
| [heuristics.md](heuristics.md) | Defaults while deciding. |
| [prompt-fragments.md](prompt-fragments.md) | Build-mode block, review lens, migration checklist. |
| [glossary.md](glossary.md) | Terms used precisely, including collisions with other packs. |
| [references.md](references.md) | Sources, and exactly what Level 1 covers here. |

## Core claim, one line

Indexing is a pipeline — discover, crawl, render, index, serve — and naming the failing
stage *is* the diagnosis; a finding that cannot name one is folklore.

## The two starred rules

Both are floor business rather than discoverability: **structured data must describe only
what the page shows** (SEO27 — the one actively enforced rule in the domain), and **nothing
here is applied at the cost of accessibility, honesty, or performance** (SEO44). Hidden
text and keyword-stuffed alt attributes fail the safety floor before they fail any search
policy.

## Related packs

[frontend/html](../html/README.md) · [frontend/react](../react/README.md) ·
[performance/core-web-vitals](../../performance/core-web-vitals/README.md) ·
[mobile/responsive-web](../../mobile/responsive-web/README.md) ·
[content/gov-uk-content-design](../../content/gov-uk-content-design/README.md)
