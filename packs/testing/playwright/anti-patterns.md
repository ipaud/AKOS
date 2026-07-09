# Anti-Patterns — Playwright Pack

- **Sleep-driven waits** — `await page.waitForTimeout(2000)` scattered through tests, slow and still occasionally too short.
- **Brittle CSS selectors** — `.MuiButton-root-482` style auto-generated class selectors breaking on every library upgrade.
- **Shared mutable test fixtures** — tests that pass individually but fail when run together due to shared database rows/state.
- **Retry-until-green** — raising retry counts to mask flakiness instead of fixing the root cause.
- **E2E test explosion** — hundreds of E2E tests covering every UI permutation, making CI take an hour and every test a maintenance burden.
