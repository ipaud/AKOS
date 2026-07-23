# Contract: knowledge pack `metadata.yaml`

Machine schema: [`schemas/v1/knowledge-pack.schema.json`](../../schemas/v1/knowledge-pack.schema.json) (resolved via [`schemas/registry.json`](../../schemas/registry.json)). Run `akos validate packs` to check a pack against it. The *why* of the pack file contract lives in [`core/knowledge-schema.md`](../../core/knowledge-schema.md) — this document is the exact field-by-field *what* of `metadata.yaml` specifically.

## Field reference

| Field | Type | Required? | Default | Meaning |
|---|---|---|---|---|
| `schema_version` | integer, `enum: [1]` | **Yes** | — | Which version of this contract the file was authored against. An unknown value fails explicitly rather than falling back to the current schema |
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

## Strict since schema_version 1

`schema_version: 1` is a versioned, strict contract: `additionalProperties` is `false` at the root and in every nested object (`sources[]` items, `conflicts[]` items, `profiles`), so an unknown top-level or nested key (a typo like `maintaner`) is a validation **error**, not a silently-ignored extra field. The pre-v1 schema was non-breaking by construction (`additionalProperties: true`, no `schema_version`); this version trades that looseness for catching typos and contract drift, backfilled atomically across the whole corpus (see Migration note below) so nothing broke mid-flight.

Two cross-field checks run alongside the schema (`schemas/validate.py`'s `_check_pack_semantics`, not expressible in JSON Schema since they need the file's own path): `domain`/`name`/`id` must actually match the directory the pack lives in, and `deprecated: true` requires a non-empty `replacement`.

## Required fields

The 8 required fields (`schema_version` plus the 7 already universal across the corpus before this version) are exactly what's already present in all 54 non-personal packs post-migration — `akos validate packs` reports zero errors against the real corpus.

## Minimal valid example (today's real shape)

```yaml
schema_version: 1
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
schema_version: 1
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

All 48 pre-existing packs were migrated on 2026-07-20 by [`bin/migrate-pack-metadata.py`](../../bin/migrate-pack-metadata.py) to carry the 7 recommended fields (`id`, `status`, `last_reviewed`, `review_after`, `maintainer`, `license`, `deprecated`). The same idempotent, append-only script backfilled `schema_version: 1` onto all 54 non-personal packs (the original 48 plus the 6 `ai-engineering/*` packs added since) when the strict schema landed — it never rewrites an existing line, only appends missing top-level keys at end-of-file; re-running it is a no-op. `akos create-pack` scaffolds `schema_version: 1` directly for new packs (`status: draft`, dates from creation time).

## Validate

```bash
akos validate packs
akos validate packs --format json
```
