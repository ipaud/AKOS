---
schema_version: 1
id: architecture-review
description: "Focused structural pass — including the complexity challenge the owner wants enforced."
agents: [architecture-reviewer]
packs: [architecture/clean-architecture, architecture/design-patterns, architecture/domain-driven-design, architecture/martin-fowler-refactoring, architecture/solid, architecture/twelve-factor-app]
profiles: [Prototype, Production, Enterprise]
status: stable
maintainer: core
---

# Workflow: Architecture Review

Focused structural pass — including the complexity challenge the owner wants enforced.

## Agent

[architecture-reviewer](../agents/architecture-reviewer.md), loading the six [architecture packs](../packs/architecture/clean-architecture/README.md).

## Sweep

1. **Import-direction check** — does business logic import frameworks/ORM directly?
2. **Unplug test** — can core logic be tested without DB/framework?
3. **Composition-root check** — is wiring separated from business decisions?
4. **Boundary-cost check** — interfaces/rings present without a real second implementation (over-engineering), or missing where genuine volatility exists (under-engineering)?
5. **SOLID scan** — god classes, LSP violations, fat interfaces; and the overuse boundary (interface-per-class ceremony, speculative strategies).
6. **DDD/pattern proportionality** — tactical ceremony on trivial CRUD? Pattern applied with no real trigger?

## The complexity challenge

Per [pau-avila principle 2](../packs/personal/pau-avila/principles.md), actively push back on any abstraction/dependency/layer that hasn't earned its place *now* — flag both under- and over-engineering.

## Profile adjustments

- **Prototype:** weight 0 (skip) — simplicity is the default; flag only egregious future-pain traps.
- **Production/Enterprise:** weight 3, full sweep.

## Exit criteria

Findings tagged under- vs over-engineering, each with the minimal fix (extract an interface, or inline an unnecessary one). Architecture + Maintainability scores.
