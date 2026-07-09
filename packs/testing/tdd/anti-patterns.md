# Anti-Patterns — TDD Pack

- **Test-after theater** — writing implementation first, then tests that just confirm what the code happens to do, providing no real design pressure or regression safety for actual intended behavior.
- **Never-red tests** — a test that's never been watched to fail, quietly not actually testing anything (bad assertion, wrong setup).
- **Implementation-detail assertions** — tests checking private internals/call counts instead of observable behavior, breaking on every harmless refactor.
- **Giant cycles** — a single Red-Green step spanning hours of implementation, defeating the tight-feedback-loop purpose of TDD.
- **Refactor-with-new-behavior** — sneaking in a feature change during what's supposed to be a pure refactor step, with no test coverage for the new behavior.
