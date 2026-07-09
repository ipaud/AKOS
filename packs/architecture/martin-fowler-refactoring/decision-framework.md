# Decision Framework — Refactoring Pack

## Refactor now vs. defer

| Signal | Action |
|--------|--------|
| Smell is directly in the way of the current feature/fix | Refactor now, as the first step |
| Smell is real but unrelated to current work | Note it (ticket/TODO with the smell name); don't scope-creep |
| Smell appears on the third occurrence of duplication | Refactor now (RF7) |
| Smell is cosmetic, no test-coverage risk, no change velocity impact | Leave it |

## Refactor vs. rewrite

1. Can the target structure be reached via a sequence of named, small, behavior-preserving refactorings? → Refactor incrementally.
2. Is the blocker a foundational technology choice (language, framework, data model) that no refactoring sequence reaches? → Consider rewrite, but prefer the **strangler fig** pattern: build the new system alongside the old, route traffic incrementally, retire the old piece by piece — never a hard cutover with a multi-month freeze.
3. Is test coverage on the legacy system near zero? → That's an argument for *more* incremental refactoring (each step is independently verifiable) not less — a rewrite compounds the same risk at a much larger scale.

## Prioritizing which smell to fix first

Fix smells that: (a) block the current task, (b) are hit repeatedly (shotgun surgery, duplicated code touched often), (c) are cheap relative to their unblock value. Defer smells that are isolated, rarely touched, or purely aesthetic.

## Refactoring during code review

If a reviewer spots a smell unrelated to the PR's purpose, it becomes a follow-up note, not a blocking request on this PR — mixing concerns in review has the same "two hats" problem as mixing them in commits.
