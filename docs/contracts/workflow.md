# Contract: workflow frontmatter

Machine schema: [`schemas/v1/workflow.schema.json`](../../schemas/v1/workflow.schema.json) (resolved via [`schemas/registry.json`](../../schemas/registry.json)). Run `akos validate workflows` to check.

## All 9 `workflows/*.md` files now carry frontmatter

`schema_version: 1` requires frontmatter to be present (the file must open with a `---` block) and requires `schema_version` itself — every other field stays optional so a future minimal workflow still validates. A file with no leading `---` block is now a validation **error**, not the informational skip it was pre-v1.

All 9 real workflows were migrated by hand (there is no automated migrator for this — each workflow's `agents`/`packs` were derived by actually reading that file's body, not invented) to carry `id`, `description`, `agents`, `packs`, `profiles`, `status`, and `maintainer`. `additionalProperties` is `false`, so an unknown top-level key is also an error.

## Field reference

| Field | Type | Required? | Meaning |
|---|---|---|---|
| `schema_version` | integer, `enum: [1]` | **Yes** | Which version of this contract the file was authored against. An unknown value fails explicitly rather than falling back to the current schema |
| `id` | string | optional | Workflow identifier |
| `description` | string | optional | One-line summary of what the workflow is for |
| `agents` | string[] | optional | Which `agents/*.md` this workflow chains |
| `packs` | string[] | optional | Packs this workflow always loads (can be empty — many workflows load packs transitively through their chained agents instead of flattening them here) |
| `profiles` | enum[] | optional | Which reasoning profiles this workflow applies to |
| `status` | `draft` \| `stable` \| `deprecated` | optional | Lifecycle state |
| `maintainer` | string | optional, default `core` | |

## Real example (`workflows/ui-screen-review.md`)

```yaml
---
schema_version: 1
id: ui-screen-review
description: Reviewing a single user-facing screen or flow.
agents: [ux-reviewer, accessibility-reviewer, mobile-reviewer, copy-reviewer, frontend-reviewer]
packs: []
profiles: [Prototype, Production]
status: stable
maintainer: core
---
```

## Validate

```bash
akos validate workflows
akos validate workflows --format json
```
