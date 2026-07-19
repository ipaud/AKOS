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

Several packs cover the same domain from different angles. Route on the **reach
for it when** column, not on the name — picking `laws-of-ux` when the question
is really about visual craft wastes a slot.

| Pack | Reach for it when |
|---|---|
| `ux/steve-krug` | Web usability: is the screen self-evident? Forms, navigation, button copy. |
| `ux/don-norman` | The user's mental model is wrong. Affordances, feedback, error-proofing. |
| `ux/laws-of-ux` | Too many choices, too much to remember, targets too small. Cognitive load. |
| `ux/nielsen-norman-group` | You need a systematic heuristic sweep with severity ratings. |
| `ux/universal-principles-of-design` | Grouping, progressive disclosure, chunking — design theory behind a layout. |
| `ux/refactoring-ui` | It works but looks amateur. Hierarchy, spacing, type, color, depth. |
| `ux/wcag` | Conformance is the question. Contrast, keyboard, ARIA, focus order, AA criteria. |
| `ux/apple-hig` | Building for iOS or macOS specifically. |
| `ux/material-design` | Building for Android, or adopting Material as the system. |
| `content/ux-writing` | Words inside the UI: button labels, error messages, empty states, voice and tone. Any screen whose copy you are writing or changing. |
| `content/gov-uk-content-design` | Prose the user has to read: guidance, help, onboarding, docs. Not for control-dense screens — those are `ux-writing`. |
| `mobile/responsive-web` | Layout across sizes: breakpoints, fluid type, container queries, 320px reflow, when to restructure instead of scroll. |
| `mobile/touch-ergonomics` | The hand and the device: target sizes and spacing, thumb zones, no-hover, virtual keyboard, locale input parsing, gestures. |
| `frontend/react` | React or Next.js: hooks, rendering, server components, composition. |
| `frontend/typescript` | Types are loose or wrong. Strict mode, unions, schema validation at boundaries. |
| `frontend/css` | Layout and motion: grid, flexbox, custom properties, container queries. |
| `frontend/html` | Semantics and forms before styling. Landmarks, native elements. |
| `frontend/design-systems` | Tokens, shared component library, theming, versioned component APIs. |
| `backend/supabase` | Supabase in the stack. **Mandatory when deployed** — RLS, auth, storage. |
| `backend/postgres` | Schema, indexing, migrations, slow queries. |
| `backend/rest` | Designing or changing an HTTP API: resources, status codes, pagination, versioning. |
| `backend/graphql` | GraphQL specifically: schema, resolvers, N+1, query cost. |
| `security/owasp-top-10` | Any deployed web surface. Injection, access control, auth, secrets, SSRF. |
| `security/owasp-api-top-10` | The surface is an API. Object-level authz, mass assignment, rate limits. |
| `security/owasp-asvs` | You need verifiable security requirements at a stated level. |
| `security/nist-ssdf` | Securing the pipeline itself: supply chain, SBOM, vulnerability response. |
| `performance/core-web-vitals` | Page feels slow to load or shifts. LCP, INP, CLS budgets. |
| `performance/web-dev` | Bundle too big, images and fonts unoptimized, caching absent. |
| `performance/browser-rendering` | Animation janks or scrolling stutters. Frame budget, reflow, compositing. |
| `performance/network-performance` | Transport is the bottleneck: CDN, compression, HTTP/2-3, offline. |
| `architecture/clean-architecture` | Business logic is tangled with framework or database code. |
| `architecture/solid` | Class and module design: coupling, cohesion, dependency direction. |
| `architecture/domain-driven-design` | The domain is genuinely complex and the language is inconsistent. |
| `architecture/design-patterns` | A recurring structural problem has a known named solution. |
| `architecture/martin-fowler-refactoring` | Code works but resists change. Smells, incremental restructuring. |
| `architecture/twelve-factor-app` | Config, statelessness, and portability for a deployed service. |
| `testing/tdd` | Writing new logic — tests lead the implementation. |
| `testing/testing-pyramid` | Deciding *what level* to test at; the suite is slow or top-heavy. |
| `testing/playwright` | Writing or stabilizing E2E browser tests. |
| `testing/qa-checklists` | Pre-release exploratory sweep: edge cases, states, cross-browser. |
| `product/inspired` | Is this the right thing to build? Discovery, risk, empowered-team practice. |
| `product/lean-startup` | The assumption is unvalidated. MVP scope, hypothesis, measure-learn. |
| `product/continuous-discovery-habits` | Setting up a real customer-contact cadence and opportunity mapping. |
| `product/escaping-the-build-trap` | Shipping features but not outcomes. Strategy and org shape. |
| `devops/deployment` | Rollout and rollback: canary, blue-green, migration safety. |
| `devops/ci-cd` | Pipeline design and what gates a merge. |
| `devops/sre` | Reliability as a target: SLOs, error budgets, alerting, incidents. |
| `devops/git` | Branching model, commit hygiene, history strategy. |
| `personal/pau-avila` | Level 0 — always loaded in step 3, never a routing choice. |

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
