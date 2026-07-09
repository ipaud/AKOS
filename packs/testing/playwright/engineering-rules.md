# Engineering Rules — Playwright Pack

- PL1. No `waitForTimeout`/fixed sleep in test code except as a rare, commented last resort.
- PL2. Selectors use `getByRole`/`getByLabel`/`getByText` by default; CSS/XPath selectors require justification.
- PL3. Tests run independently in isolation (fresh browser context, no shared mutable fixtures across tests).
- PL4. Trace/video capture enabled on retry/failure in CI for debugging.
- PL5. E2E test count is bounded to critical journeys; broad UI permutation testing happens at a lower pyramid layer.
- PL6. Test data setup uses API calls/fixtures per test, not manual pre-existing database state.
