# Anti-Patterns — Testing Pyramid Pack

- **Ice cream cone** — mostly E2E tests, few unit tests; slow, flaky CI, hard to pinpoint failures.
- **Ignored flaky tests** — a test that fails ~10% of the time, re-run until green, normalized as "just flaky" instead of fixed.
- **Testing implementation, not behavior** — unit tests asserting internal implementation details that break on every refactor even when behavior is unchanged.
- **E2E-only bug regression tests** — every production bug gets one slow E2E test instead of a fast unit test at the actual fault layer.
- **No integration layer** — only unit tests (mocking everything) and E2E tests (testing everything), missing the "do these two real components actually cooperate" layer where many real bugs live.
