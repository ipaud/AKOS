# Principles — Playwright Pack

- **PW1** — Use Playwright's auto-waiting locators (`getByRole`, `getByText`, `getByLabel`) instead of fixed `sleep`/`waitForTimeout`.
- **PW2** — Prefer role/label/text-based selectors over CSS class or XPath selectors — resilient to markup changes and doubles as an accessibility check.
- **PW3** — Each test is independent: no test depends on another test's execution or leftover state; use fixtures/`beforeEach` for setup.
- **PW4** — Tests wait on application state (element visible, network response, specific text), never on arbitrary durations.
- **PW5** — Flaky tests are debugged via trace/video capture, root-caused, and fixed — not retried into passing.
- **PW6** — E2E tests cover critical user journeys only (per [testing-pyramid TP3](../testing-pyramid/principles.md)), not exhaustive UI permutations.
- **PW7** — Test data is seeded/created per-test (via API/fixtures), not dependent on pre-existing shared environment state.
