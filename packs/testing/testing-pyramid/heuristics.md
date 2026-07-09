# Heuristics — Testing Pyramid Pack

- Count the suite's tests by layer — if E2E outnumbers unit tests, that's an inverted pyramid worth addressing.
- A bug found in production → ask "which layer should have caught this?" and add a test at the *cheapest* layer that would have caught it, not reflexively at E2E.
- A flaky test → fix its root cause (timing, test isolation, shared state) within the sprint, or quarantine/remove it — don't let it linger "usually green."
- CI taking many minutes → check the layer distribution; often a few slow E2E tests dominate runtime disproportionately to their coverage value.
