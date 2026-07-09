# Heuristics — TDD Pack

- Wrote code before a test exists for it? Stop, revert conceptually, write the test first — retrofitted tests tend to just confirm what the code already does, not what it should do.
- A test that passes on the first run without ever seeing it fail → suspicious; verify it can actually fail (mutate the code briefly to confirm).
- Struggling to write a test for a unit → often means the unit has too many responsibilities or hidden dependencies; that's a design signal, not just a testing inconvenience.
- Implementation feels like "cheating" the test (hardcoded return value) → add a second test with different input to force generalization.
- A refactor step introduces new failing tests → stop, that's a behavior change smuggled into refactoring; separate it out.
