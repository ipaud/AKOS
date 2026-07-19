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

## 2. Read the project config

Read `.akos/config.md` in the current project. Every section in it is binding —
do not stop at the profile:

| Section | What it does |
|---|---|
| **Reasoning profile** | Sets strictness. If absent or unset, default to **Startup MVP**. Profiles: Prototype · Startup MVP · Production · Enterprise · Game Dev · Internal Tool. |
| **Project context** | `Stack:` narrows pack routing in step 4. `Deployed: yes` makes security and Supabase/RLS packs **mandatory**, not optional (personal principle 6). `Primary surface:` decides whether mobile and responsive apply. |
| **Profile overrides** | Per-lens weight changes with a stated reason. These beat the profile's defaults — and only these; an override never lowers the safety floor. |
| **Packs to always load** | Load every pack listed here **in addition to** the 2-5 you route to in step 4. The project owner has already decided these are load-bearing. |
| **Style direction** | The committed visual direction. Every UI surface you build must follow it, so screens stay consistent across the project. Absent? Ask for one before building UI rather than defaulting to generic styling (personal principle 4). |
| **Notes** | Project-specific facts. Read them; they override your assumptions about the project. |

State the active profile in your first response. Choosing the wrong profile is
itself a review finding (Article 6).

No `.akos/config.md`? Default to Startup MVP, say so, and treat the project as
undeployed until told otherwise. Suggest `akos install-project` once — don't
nag.

## 3. Load the Level-0 layer

Read `packs/personal/pau-avila/`. This is authority Level 0 — it outranks every
external source and always applies. Start with `principles.md` and
`ai-agent-rules.md`; add `coding-preferences.md`, `ux-preferences.md`,
`design-language.md`, `project-patterns.md`, or `supabase-rules.md` when the
task touches them.

## 4. Route to packs

Load, in this order:

1. Everything under **Packs to always load** in `.akos/config.md` — already decided, not negotiable.
2. If `Deployed: yes`, the security and Supabase/RLS packs, whether or not the task looks security-shaped (personal principle 6).
3. **2-5** more packs closest to the task, from the table below. Let `Stack:` narrow the choice — a React + Supabase project routes to `frontend/react` and `backend/supabase`, not to `graphql` or `css` in the abstract.

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

Open with one line naming the active profile and the packs you loaded, so the
caller can tell AKOS actually ran and correct the routing if it's wrong:

```
AKOS · Production · packs: backend/supabase, security/owasp-top-10,
frontend/react, ux/wcag
```

Then:

- Pack principles and engineering rules are **constraints and defaults**, not
  suggestions. Surface only conflicts, tradeoffs, and deliberate profile-based
  skips.
- Follow the **Style direction** from `.akos/config.md` on every UI surface. It
  is the project's committed look — consistency across screens beats a locally
  prettier one-off, and it is what keeps output from drifting to generic
  template UI (personal principle 4).
- Apply any **Profile overrides** from the config over the profile's default
  weights. An override can raise strictness or lower ceremony; it can never
  lower the safety floor.
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
