---
name: akos
description: Load AKOS knowledge (constitution, authority model, reasoning profile, and 2-5 task-relevant packs) before non-trivial work on user-facing features, UI, architecture, security, data, or performance. Use when the user mentions AKOS, asks for opinionated guidance or a style direction, or starts a feature in a project containing .akos/config.md.
---

# AKOS — build mode

AKOS root is `~/DEV/AKOS`. If that path does not exist, AKOS root is the
directory two levels above this file. Every path below is relative to it.

Read files with your file-reading tool. Do not load the whole repo — it is 45
packs. Load the constitution, the profile, the Level-0 layer, and 2-5 packs.

## 1. Bootstrap

Read in order:

1. `core/constitution.md` — 11 articles. Top of the stack; overrides every pack.
2. `core/authority-model.md` — L0 personal → L1 standards → L2 industry → L3 books → L4 community.
3. `core/reasoning-profiles.md` — the six profiles and the agent weight table.

## 2. Set the reasoning profile

Read `.akos/config.md` in the current project. If absent or unset, default to
**Startup MVP**. Profiles: Prototype · Startup MVP · Production · Enterprise ·
Game Dev · Internal Tool.

State the active profile in your first response. Choosing the wrong profile is
itself a review finding (Article 6).

## 3. Load the Level-0 layer

Read `packs/personal/pau-avila/`. This is authority Level 0 — it outranks every
external source and always applies. Start with `principles.md` and
`ai-agent-rules.md`; add `coding-preferences.md`, `ux-preferences.md`,
`design-language.md`, `project-patterns.md`, or `supabase-rules.md` when the
task touches them.

## 4. Route to packs

Pick **2-5** packs closest to the task from `packs/<domain>/<pack>/`:

| Domain | Packs |
|---|---|
| `architecture` | clean-architecture · design-patterns · domain-driven-design · martin-fowler-refactoring · solid · twelve-factor-app |
| `backend` | graphql · postgres · rest · supabase |
| `devops` | ci-cd · deployment · git · sre |
| `frontend` | css · design-systems · html · react · typescript |
| `performance` | browser-rendering · core-web-vitals · network-performance · web-dev |
| `product` | continuous-discovery-habits · escaping-the-build-trap · inspired · lean-startup |
| `security` | nist-ssdf · owasp-api-top-10 · owasp-asvs · owasp-top-10 |
| `testing` | playwright · qa-checklists · tdd · testing-pyramid |
| `ux` | apple-hig · don-norman · laws-of-ux · material-design · nielsen-norman-group · refactoring-ui · steve-krug · universal-principles-of-design · wcag |
| `personal` | pau-avila — Level 0, always loaded (step 3) |

For each pack selected:

- Read `prompt-fragments.md` **first**. It ships a pre-written build-mode
  constraint block — the pack's designed injection surface, and usually all you
  need.
- Read `principles.md` (always true) and `engineering-rules.md` (checkable in an
  artifact) only when the task needs depth beyond the fragment.
- Reach for `heuristics.md`, `anti-patterns.md`, `decision-framework.md`, or
  `examples.md` only on a specific question.

`graphs/` cross-links one concept across packs — use it when a single idea
(e.g. recognition over recall) needs multiple angles.

## 5. Apply

- Pack principles and engineering rules are **constraints and defaults**, not
  suggestions. Surface only conflicts, tradeoffs, and deliberate profile-based
  skips.
- Cite the authority level (L0–L4) on load-bearing guidance.
- On conflict between sources, follow `core/conflict-resolution.md` and state
  the tradeoff. Never silently pick a winner (Article 3).
- Give a recommendation with its confidence, not a survey (Article 5).
  "It depends" without a follow-up decision rule is a violation.
- Challenge unnecessary complexity, including when the user proposed it
  (Article 7).

## 6. The floor — never waived

Security · accessibility basics · data integrity. Not traded for speed in any
profile, at any authority level. "It's just a prototype" relaxes ceremony, never
the floor (Article 2).

Also non-negotiable per the constitution: four async states — empty, loading,
error, success — on every user-facing surface (Article 8), and responsive /
touch behavior reviewed by default for web (Article 9).

## Reviewing rather than building?

Use the `akos-review` skill — it runs the twelve-lens pipeline and emits the
unified Review Summary.
