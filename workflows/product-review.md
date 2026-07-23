---
schema_version: 1
id: product-review
description: "Focused product-clarity pass — surfaces (doesn't block) product decisions."
agents: [product-reviewer]
packs: [product/continuous-discovery-habits, product/escaping-the-build-trap, product/inspired, product/lean-startup]
profiles: [Prototype, Startup MVP, Production]
status: stable
maintainer: core
---

# Workflow: Product Review

Focused product-clarity pass — surfaces (doesn't block) product decisions.

## Agent

[product-reviewer](../agents/product-reviewer.md), loading the four [product packs](../packs/product/inspired/README.md).

## Sweep

1. **Outcome check** — is there a stated metric + target, or just a feature description?
2. **Four-risk check** — value / usability / feasibility / viability each addressed?
3. **Validation check** — was value risk tested cheaply (prototype/interview/landing page) before committing to build?
4. **Feature-factory smell** — pre-decided output, no stated why, no discovery?
5. **Leap-of-faith assumption** — named and testable?

## Boundary

Per [Ruling R10](../core/conflict-resolution.md), the human owns product calls — this workflow **surfaces** the outcome/validation gap and recommends the cheapest next experiment; it doesn't veto features.

## Profile adjustments

- **Prototype:** light — a genuine idea-exploration isn't held to full discovery.
- **Startup MVP:** highest weight (product-market-fit search) — outcome + validation expected.
- **Production:** moderate — validate before large investments.

## Exit criteria

Product score; findings frame missing outcome/risk/validation with a concrete cheapest-next-experiment. Advisory decision (the human decides).
