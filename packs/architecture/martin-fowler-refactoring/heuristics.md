# Heuristics — Refactoring Pack

## Smell catalog (fast recognition)

- **Long method** — if you have to scroll to see the whole thing, or hesitate before naming it, it's probably too long. → Extract Function.
- **Large class** — a class doing many unrelated things (see [SRP](../solid/heuristics.md)). → Extract Class.
- **Duplicated code** — same logic in ≥2 places (the third occurrence triggers action). → Extract Function, call from both.
- **Feature envy** — a method more interested in another class's data than its own. → Move Function to where the data lives.
- **Long parameter list** — >3-4 params, especially several of the same type. → Introduce Parameter Object.
- **Shotgun surgery** — one conceptual change requires edits across many files. → often the inverse of Extract Class done wrong; consolidate.
- **Divergent change** — one class changes for many different unrelated reasons. → the SRP violation; split.
- **Primitive obsession** — raw strings/numbers standing in for a real concept. → Introduce value object ([DDD DD4](../domain-driven-design/principles.md)).
- **Comments explaining what, not why** — often masking code that should just be clearer. → Extract Function with a good name; delete the comment.

## Practice heuristics

- Refactor *before* adding a feature to code that's hard to extend — not after, and not instead of.
- If tests don't exist for code you're about to refactor, write characterization tests (tests capturing current behavior, even if "wrong") before touching structure.
- Commit after every green step during a refactoring session — cheap rollback beats careful debugging mid-refactor.
- If a refactoring session reveals a design that should be fundamentally different, stop, note it, and finish the current small step first — don't scope-creep mid-refactor.
- Rewrite temptation check: can 80% of the value be reached via 5-10 targeted refactorings instead? Usually yes.
