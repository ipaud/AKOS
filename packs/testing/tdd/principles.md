# Principles — TDD Pack

- **TD1** — Write the test before the implementation; run it and confirm it fails for the expected reason (Red).
- **TD2** — Write the minimum code to make the test pass (Green) — no extra generality, no unrelated improvements.
- **TD3** — Refactor only with passing tests as a safety net (Refactor); never refactor and add behavior in the same step ([two hats](../../architecture/martin-fowler-refactoring/mental-models.md)).
- **TD4** — Each cycle is small — minutes, not hours; a test that requires an hour of implementation to pass is too large, split it.
- **TD5** — Tests describe behavior (inputs → outputs/effects), not implementation details, so refactoring doesn't require rewriting tests.
- **TD6** — When the obvious implementation would be "cheating" (hardcoding), triangulate with a second test before generalizing.
- **TD7** — TDD is a design tool, not just a verification tool — a hard-to-test unit is signaling a design problem (tight coupling, hidden dependencies) worth addressing.
