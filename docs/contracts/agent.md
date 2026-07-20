# Contract: reviewer agent frontmatter

Machine schema: [`schemas/agent.schema.json`](../../schemas/agent.schema.json). Run `akos validate agents` to check. This validates the YAML frontmatter block of `agents/*.md` only — the prose body is meant for an LLM to read and reason over, not data to be schema-validated. See "Why not the prose body" below.

## Field reference

| Field | Type | Required? | Meaning |
|---|---|---|---|
| `name` | string, pattern `^akos-[a-z-]+$` | **Yes** | e.g. `akos-ux-reviewer` |
| `description` | string, min 20 chars | **Yes** | When Claude Code should delegate to this subagent |
| `tools` | string (comma-joined, e.g. `Read, Grep, Glob`) | **Yes** | **Not** a YAML list — confirmed the real format across all 13 agents |
| `id` | string | optional | Default: the pipeline-lens number this agent owns, e.g. `lens-2` |
| `status` | `draft` \| `stable` \| `deprecated` | optional, default `stable` | |
| `maintainer` | string | optional, default `core` | |

## Minimal valid example (today's real shape)

```yaml
---
name: akos-ux-reviewer
description: AKOS lens 2 — UX clarity. Can a first-time user accomplish the task without thinking? Catches cognitive friction, unclear navigation, weak hierarchy, missing async states. Use for the AKOS UX review of a screen or flow.
tools: Read, Grep, Glob
---
```

## Why not the prose body

`agents/*.md`'s body sections (Purpose, When to use, Packs to load, Review checklist, Severity levels, Scoring rubric, Refusal/limits, Output format) are hand-written, human-reviewed documents meant to be read and reasoned over by an LLM — the same nature as the knowledge packs themselves. JSON Schema validates the *shape* of structured data; forcing structure onto prose either validates nothing meaningful or fights the authoring workflow.

The one thing worth checking mechanically — *are the 8 canonical section headings present* — is a presence check, not a schema concern. `akos validate agents` does this separately via a heading-count grep (the same technique `doctor.sh` already uses for `SKILL.md` frontmatter), reported alongside the frontmatter schema result but implemented independently.

## Validate

```bash
akos validate agents
akos validate agents --format json
```
