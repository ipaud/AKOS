# Examples — Testing Pyramid Pack

## Choosing the right layer for a bug fix

Bug: discount calculation wrong for a specific coupon type.
Wrong: add one slow E2E test clicking through checkout with that coupon.
Right: add a unit test for `calculateDiscount()` covering that coupon type — runs in milliseconds, pinpoints the exact function, catches regressions instantly.

## Pyramid-shaped suite (illustrative ratio)

```
Unit:        ~200 tests, ~15s total runtime
Integration:  ~40 tests, ~90s total runtime
E2E:           ~8 tests, ~6min total runtime (critical journeys only:
               signup, checkout, core CRUD flow)
```

## Flaky test triage

A `waitFor(500ms)` in an E2E test causing intermittent failures under CI load → replaced with a deterministic wait on an actual UI state change (`waitFor(() => screen.getByText('Loaded'))`), eliminating the flake at its root cause rather than increasing the timeout.
