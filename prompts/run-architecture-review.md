# Prompt: Run Architecture Review

---

Load AKOS (`~/DEV/AKOS/prompts/load-akos.md`) and run the architecture review workflow (`~/DEV/AKOS/workflows/architecture-review.md`) on [describe the codebase/module].

Act as `agents/architecture-reviewer.md`, loading the six architecture packs.

Sweep:
1. Import-direction check — business logic importing frameworks/ORM directly?
2. Unplug test — core logic testable without DB/framework?
3. Composition-root check — wiring separated from business decisions?
4. Boundary-cost check — interfaces/rings present with no real second implementation (over-engineering), or missing at genuine seams (under-engineering)?
5. SOLID scan + overuse boundary.
6. DDD/pattern proportionality.

**Challenge complexity actively** (per pau-avila principle 2): push back on any abstraction/dependency/layer that hasn't earned its place *now*. Flag BOTH under- and over-engineering — each is a finding with a minimal fix (extract an interface, or inline an unnecessary one).

Produce a Review Summary with Architecture + Maintainability scores. Scale to profile: don't impose four-ring Clean Architecture on a small prototype (that itself is an over-engineering finding).
