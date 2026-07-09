# Prompt Fragments — Testing Pyramid Pack

```text
Apply testing-pyramid balance (AKOS L2): bulk of coverage in fast unit
tests on business logic; integration tests at real component boundaries
(API+DB, service+client); E2E tests limited to critical user journeys
only; fix or quarantine flaky tests immediately, never leave them
intermittent; choose test layer by the cheapest layer that would have
caught a given bug, not reflexively at E2E.
```
