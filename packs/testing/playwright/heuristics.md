# Heuristics — Playwright Pack

- Grep for `waitForTimeout`/`sleep` in test files — each is a candidate for a proper state-based wait.
- A selector like `.css-x7f3a` or a deep `div > div > span` chain → switch to `getByRole`/`getByText`/`getByLabel`.
- A test failing only in CI, not locally → suspect timing/resource contention; check for auto-waiting bypass or missing `await`.
- Two tests failing together but passing individually → shared state leak; check for missing isolation/cleanup.
- A retry count set high to "make CI green" → the tests are flaky and need root-causing, not more retries.
