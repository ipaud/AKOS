# Contract: workflow frontmatter (optional)

Machine schema: [`schemas/workflow.schema.json`](../../schemas/workflow.schema.json). Run `akos validate workflows` to check.

## None of the 9 `workflows/*.md` files have frontmatter today — and that's valid

Every field in this schema is optional and the schema has no `required` list at all, so a workflow file with no leading `---` block is valid — it never claimed to have frontmatter, so there's nothing to fail. `akos validate workflows` reports this as an informational note, not a warning or error.

**No automated migration backfills this.** Unlike the pack metadata migration (see [`docs/contracts/knowledge-pack.md`](knowledge-pack.md)), adding frontmatter to a workflow is lower value — these are 9 prose files read mostly by humans and LLMs, not consumed by the rules/benchmark machinery — and is done by hand, one workflow at a time, only if/when that workflow needs machine routing.

## Field reference (when present)

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Workflow identifier |
| `agents` | string[] | Which `agents/*.md` this workflow chains |
| `packs` | string[] | Packs this workflow always loads |
| `profiles` | enum[] | Which reasoning profiles this workflow applies to |
| `status` | `draft` \| `stable` \| `deprecated` | Lifecycle state |

## Example, if a workflow adopts frontmatter

```yaml
---
id: ui-screen-review
agents: [ux-reviewer, accessibility-reviewer, mobile-reviewer, copy-reviewer, frontend-reviewer]
profiles: [Startup MVP, Production, Enterprise]
status: stable
---
```

## Validate

```bash
akos validate workflows
akos validate workflows --format json
```
