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

# Workflow: UI Screen Review

Reviewing a single user-facing screen or flow.

## Agents (in order)

1. [ux-reviewer](../agents/ux-reviewer.md) — no-think walk, five-second test, trunk test, four states.
2. [accessibility-reviewer](../agents/accessibility-reviewer.md) — the three walks (keyboard, tree, stress). Floor-level.
3. [mobile-reviewer](../agents/mobile-reviewer.md) — 320px, thumb zones, touch targets, poor-network. Default-on.
4. [copy-reviewer](../agents/copy-reviewer.md) — labels, errors, empty-state copy, no happy talk.
5. [frontend-reviewer](../agents/frontend-reviewer.md) — visual craft, hierarchy, designed states, anti-template.

## Merge

Combine per-agent findings into one [unified Review Summary](../core/review-pipeline.md). Final decision = worst individual decision.

## Profile adjustments

- **Prototype:** run 1-4 at reduced depth; a11y floor and four states still enforced; frontend visual-craft optional.
- **Production:** all five at full depth.

## Exit criteria

Unified summary with severity-ranked findings, scores (UX, Accessibility), and a PASS / PASS WITH FIXES / BLOCKED decision. No screen passes without its empty/loading/error states.
