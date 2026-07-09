# Reasoning Profiles

A profile tells agents what this piece of software is *for*, so process scales to context. The profile changes agent weights, scoring weights, and which pipeline steps are mandatory — it never changes the safety floor.

Declare the profile in the project's `.akos/config.md`, or state it in the request. If unknown, agents ask once, then default to **Startup MVP**.

## Profile definitions

### Prototype

**Goal:** learn something fast, then probably throw it away.
**Prioritize:** speed, learning, minimal viable implementation, low ceremony.
**Still enforce:** basic accessibility (labels, keyboard, contrast), obvious UX, no security leaks (no real secrets in code, no exposed endpoints with real data), honest states on the happy path.
**Skip freely:** test coverage targets, architecture layering, exhaustive error handling, performance budgets, documentation.
**Agent posture:** bias to "ship it, note the debt". BLOCKED verdicts only for floor violations.

### Startup MVP

**Goal:** real users, fast iteration, product still searching for fit.
**Prioritize:** speed, usability, iteration, maintainable-enough architecture.
**Enforce additionally:** empty/loading/error/success states everywhere, mobile/responsive review, auth done properly, Supabase RLS on any real user data, smoke tests on critical flows.
**Skip:** enterprise ceremony, exhaustive docs, >80% coverage targets, premature scalability.

### Production

**Goal:** paying users depend on it.
**Prioritize:** maintainability, security, accessibility, performance, testing, clean architecture.
**Enforce:** full [review pipeline](review-pipeline.md); WCAG AA; OWASP review; performance budgets (Core Web Vitals); test coverage on core logic; migration/rollback thinking; observability basics.
**Agent posture:** CRITICAL and HIGH findings block. Tradeoffs need written justification.

### Enterprise

**Goal:** many teams, compliance exposure, long life.
**Prioritize:** compliance, observability, documentation, reliability, governance.
**Enforce (beyond Production):** audit logging, access-control review, documented decision records, dependency and license review, SLO thinking, upgrade/deprecation paths.

### Game Dev

**Goal:** fun. Feel is the product.
**Prioritize:** feel, responsiveness, immersion, performance (frame time), iteration speed.
**Adjust:** UX heuristics apply to menus/UI, not to core mechanics (deliberate challenge ≠ friction defect). Performance agent weights frame budget over page-load metrics. Accessibility still applies: remappable inputs, readable text, colorblind-safe signaling where feasible.

### Internal Tool

**Goal:** make a workflow faster for a known, small audience.
**Prioritize:** productivity, clarity, speed of workflows; low visual polish acceptable.
**Enforce:** data safety (internal tools touch real data), obvious destructive-action guards, keyboard-friendly flows.
**Skip:** visual identity work, marketing-grade polish, broad browser matrix.

## Weight tables

Agent emphasis per profile (0 = skip unless asked, 1 = light pass, 2 = standard, 3 = strict):

| Agent | Prototype | MVP | Production | Enterprise | Game Dev | Internal |
|---|---|---|---|---|---|---|
| ux-reviewer | 2 | 3 | 3 | 2 | 2 | 2 |
| accessibility-reviewer | 1 | 2 | 3 | 3 | 2 | 2 |
| architecture-reviewer | 0 | 1 | 3 | 3 | 1 | 1 |
| security-reviewer | 1 | 2 | 3 | 3 | 1 | 2 |
| performance-reviewer | 0 | 1 | 3 | 2 | 3 | 1 |
| product-reviewer | 1 | 3 | 2 | 2 | 2 | 1 |
| frontend-reviewer | 1 | 2 | 3 | 2 | 2 | 1 |
| backend-reviewer | 1 | 2 | 3 | 3 | 1 | 2 |
| database-reviewer | 0 | 2 | 3 | 3 | 1 | 2 |
| testing-reviewer | 0 | 1 | 3 | 3 | 1 | 1 |
| copy-reviewer | 1 | 2 | 2 | 2 | 1 | 1 |
| mobile-reviewer | 1 | 2 | 3 | 2 | 1 | 1 |
| release-reviewer | 0 | 1 | 3 | 3 | 2 | 1 |

Score weighting for the overall score lives in [scoring-model.md](scoring-model.md) and `scoring/overall-score.md`.

## Choosing a profile

- Real users' money or data → at least Production.
- Anyone outside your machine can reach it → at least MVP rules for auth/RLS.
- "Just for me, local" → Prototype is honest.
- Profile drift is normal: prototypes get promoted. Promotion means re-review under the new profile, not a rename.
