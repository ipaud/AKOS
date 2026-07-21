# Contract: knowledge pack `metadata.yaml`

Machine schema: [`schemas/knowledge-pack.schema.json`](../../schemas/knowledge-pack.schema.json). Run `akos validate packs` to check a pack against it. The *why* of the pack file contract lives in [`core/knowledge-schema.md`](../../core/knowledge-schema.md) — this document is the exact field-by-field *what* of `metadata.yaml` specifically.

## Field reference

| Field | Type | Required? | Default | Meaning |
|---|---|---|---|---|
| `name` | string | **Yes** | — | Pack's directory name, e.g. `steve-krug` |
| `domain` | string | **Yes** | — | Domain directory, e.g. `ux` |
| `authority-level` | integer 0–4 | **Yes** | — | See [`core/authority-model.md`](../../core/authority-model.md) |
| `version` | string (semver) | **Yes** | — | This pack's content version |
| `tags` | string[] | **Yes** | — | Free-text search tags |
| `sources` | object[] `{title, author?, org?, url}` | **Yes** | — | Attribution only, per [`core/source-policy.md`](../../core/source-policy.md) — either `author` or `org` is typically present, neither is schema-required (real content uses both patterns) |
| `related` | string[] (`packs/domain/name`) | **Yes** | — | Cross-links, informational |
| `id` | string (`domain/name`) | recommended | `<domain>/<name>` | Canonical identifier |
| `status` | `draft` \| `stable` \| `deprecated` | recommended | `stable` | Lifecycle state |
| `last_reviewed` | date | recommended | — | When someone last verified this pack against its sources |
| `review_after` | date | recommended | — | When it's next due for a look — see [`docs/maintenance/freshness.md`](../maintenance/freshness.md) |
| `maintainer` | string | recommended | `core` | Who owns this pack |
| `license` | string | optional | `MIT` | Usually inherited from the repo license |
| `deprecated` | boolean | optional | `false` | |
| `replacement` | string \| null | optional | — | Pack id replacing this one, when deprecated |
| `platform-scope` | string[] | optional | — | Narrows to a specific platform (present on 2 packs today) |
| `profiles.relevant` | enum[] | optional | *(all six)* | Advisory routing narrowing only — does not replace [`core/reasoning-profiles.md`](../../core/reasoning-profiles.md)'s per-agent weight table |
| `dependencies` | string[] | optional | *(none)* | Packs this one's guidance is genuinely incomplete without. Expected empty for nearly all packs |
| `conflicts` | object[] `{pack, ruling}` | optional | *(none)* | Pre-registered tensions, feeding [`core/conflict-resolution.md`](../../core/conflict-resolution.md) |

## Required fields are exactly what's already universal

The 7 required fields are the 7 fields already present in all 48 pre-existing packs, confirmed by direct inspection before this schema was written. This is deliberate: the schema is non-breaking *by construction* — `akos validate packs` reports zero errors against the existing corpus from the moment it ships, with no migration gate in front of it.

## Minimal valid example (today's real shape)

```yaml
name: wcag
domain: ux
authority-level: 1
version: 1.0.0
tags: [accessibility, a11y, wcag, contrast, keyboard, aria, focus, forms, semantics]
sources:
  - title: "Web Content Accessibility Guidelines (WCAG) 2.2"
    author: W3C Web Accessibility Initiative
    url: https://www.w3.org/TR/WCAG22/
related:
  - packs/ux/steve-krug
```

## Fully-populated example

```yaml
name: wcag
domain: ux
authority-level: 1
version: 1.0.0
tags: [accessibility, a11y, wcag, contrast, keyboard, aria, focus, forms, semantics]
sources:
  - title: "Web Content Accessibility Guidelines (WCAG) 2.2"
    author: W3C Web Accessibility Initiative
    url: https://www.w3.org/TR/WCAG22/
related:
  - packs/ux/steve-krug
id: ux/wcag
status: stable
last_reviewed: 2026-07-09
review_after: 2028-01-05
maintainer: core
license: MIT
deprecated: false
profiles:
  relevant: [Production, Enterprise]
dependencies: []
conflicts: []
```

## Migration note

All 48 pre-existing packs were migrated on 2026-07-20 by [`bin/migrate-pack-metadata.py`](../../bin/migrate-pack-metadata.py) — a one-time, idempotent, append-only script (re-running it is a no-op). It never rewrites an existing line; it only appends the 7 recommended fields at end-of-file, computing `last_reviewed` from each pack's `CHANGELOG.md` and `review_after` from an authority-level-dependent cadence (18 months for L0–1, 12 for L2, 9 for L3–4). `akos create-pack` now scaffolds all of this directly for new packs (`status: draft`, dates from creation time).

## Validate

```bash
akos validate packs
akos validate packs --format json
```
