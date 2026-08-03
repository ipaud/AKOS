---
schema_version: 1
id: new-feature
description: Adding a feature to an existing project.
agents: [product-reviewer, architecture-reviewer]
packs: [testing/tdd, devops/git]
profiles: [Prototype, Production]
status: stable
maintainer: core
---

# Workflow: New Feature

Adding a feature to an existing project.

## Steps

1. **Confirm the profile** (from `.akos/config.md`) — sets how much process applies.
2. **Product framing** ([product-reviewer](../agents/product-reviewer.md), weight per profile): what outcome does this feature serve? For MVP+, name the metric it should move.
3. **Reuse check:** existing component/pattern/pack covering most of it?
4. **Challenge complexity** ([architecture-reviewer](../agents/architecture-reviewer.md) posture): does this need the abstraction being proposed? Push back before building ([pau-avila principle 2](../packs/personal/pau-avila/principles.md)).
5. **TDD on the logic** ([tdd pack](../packs/testing/tdd/README.md)) where it applies — failing test first for business logic and bug-adjacent behavior.
6. **Build** applying the relevant packs as constraints (frontend, backend, database as touched).
7. **Design the four states** for any new async surface.
8. **Run the review pipeline** at feature completion — at minimum UX, accessibility, mobile, copy for user-facing; add security/database if it touches auth/data; architecture if it adds structure.
9. **Commit** with atomic, well-messaged commits ([git pack](../packs/devops/git/README.md)).

## Profile adjustments

- **Prototype:** steps 2, 5, and full pipeline relaxed; UX obviousness, a11y basics, four states, and (if deployed) RLS still enforced.
- **Production:** full pipeline; security + database review mandatory if data/auth touched.

## Exit criteria

Feature works, all four states present, relevant reviews PASS or PASS WITH FIXES with the fixes enumerated. INCOMPLETE doesn't satisfy this — re-run the lens that didn't report rather than treating its silence as done.
