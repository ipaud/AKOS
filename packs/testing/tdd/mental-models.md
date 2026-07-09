# Mental Models — TDD Pack

- **Red-Green-Refactor:** write a failing test (Red) → write the minimum code to pass it (Green) → improve the structure with tests as a safety net (Refactor) → repeat.
- **The minimum-code discipline:** Green means the *smallest* change that passes, not the most complete/elegant implementation — elegance is the Refactor step's job, done with tests already protecting behavior.
- **Tests as executable specification:** a TDD suite documents intended behavior more reliably than prose docs, because it's continuously verified against real code.
- **Triangulation:** when the minimal implementation for one test looks like cheating (hardcoding the expected value), a second test with a different input forces genuine generalization.
