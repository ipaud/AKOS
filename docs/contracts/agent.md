# Contract: reviewer agent frontmatter

Machine schema: [`schemas/v1/agent.schema.json`](../../schemas/v1/agent.schema.json) (resolved via [`schemas/registry.json`](../../schemas/registry.json)). Run `akos validate agents` to check. This validates the YAML frontmatter block of `agents/*.md` only — the prose body is meant for an LLM to read and reason over, not data to be schema-validated. See "Why not the prose body" below.

## Field reference

| Field | Type | Required? | Meaning |
|---|---|---|---|
| `schema_version` | integer, `enum: [1]` | **Yes** | Which version of this contract the file was authored against. An unknown value fails explicitly rather than falling back to the current schema |
| `name` | string, pattern `^akos-[a-z-]+$` | **Yes** | e.g. `akos-ux-reviewer` |
| `description` | string, min 20 chars | **Yes** | When Claude Code should delegate to this subagent |
| `tools` | string (comma-joined, e.g. `Read, Grep, Glob`) | **Yes** | **Not** a YAML list — confirmed the real format across all 13 agents |
| `id` | string | optional | Default: the pipeline-lens number this agent owns, e.g. `lens-2` |
| `status` | `draft` \| `stable` \| `deprecated` | optional, default `stable` | |
| `maintainer` | string | optional, default `core` | |

`additionalProperties` is `false` — an unknown top-level key (a typo) is a validation error, not a silently-ignored extra field. All 13 real agents carry `schema_version: 1`.

## Minimal valid example (today's real shape)

```yaml
---
schema_version: 1
name: akos-ux-reviewer
description: AKOS lens 2 — UX clarity. Can a first-time user accomplish the task without thinking? Catches cognitive friction, unclear navigation, weak hierarchy, missing async states. Use for the AKOS UX review of a screen or flow.
tools: Read, Grep, Glob
---
```

## Why not the prose body

`agents/*.md`'s body sections (Purpose, When to use, Packs to load, Review checklist, Severity levels, Scoring rubric, Refusal/limits, Output format) are hand-written, human-reviewed documents meant to be read and reasoned over by an LLM — the same nature as the knowledge packs themselves. JSON Schema validates the *shape* of structured data; forcing structure onto prose either validates nothing meaningful or fights the authoring workflow.

The one thing worth checking mechanically — *are the 9 canonical section headings present* (Purpose, When to use, Packs to load, Review checklist, Severity levels, Scoring rubric, Pre-report gate, Refusal / limits, Output format) — is a presence check, not a schema concern. `akos validate agents` does this separately via a heading-count grep (the same technique `doctor.sh` already uses for `SKILL.md` frontmatter), reported alongside the frontmatter schema result but implemented independently.

**Pre-report gate** (added alongside the other 8, positioned right before Output format): the discipline a lens applies to its own findings before writing them into Critical/High/Medium/Low — cited location, concrete failure mode, context actually read, severity defensible against the agent's own Severity levels. Canonical rationale: [`core/review-pipeline.md`](../../core/review-pipeline.md). It operationalizes `core/confidence-model.md`'s "verify before asserting" rule as a mechanical step at report time rather than a standing principle alone.

## Validate

```bash
akos validate agents
akos validate agents --format json
```
