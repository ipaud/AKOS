# Prompt Fragments — Playwright Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply Playwright E2E practice (AKOS L2):
- Every wait is on application state — element visible/enabled/stable,
  a named network response, or specific text present. No
  waitForTimeout, no fixed sleep. A sleep ships only with a comment
  naming the exact condition that could not be waited on.
- Locators resolve by role, label, or text: getByRole('button',
  {name: 'Submit'}) first, then getByLabel/getByText. getByTestId is
  the escape hatch for elements with no semantic anchor. CSS class and
  XPath chains require written justification.
- Every locator action is actually awaited; a missing await is the
  most common source of CI-only failures.
- Tests are order-independent: fresh browser context per test, no
  shared mutable fixture, no test reading another test's leftovers.
- Test data is created per test via API or fixture, never assumed to
  pre-exist in a shared environment.
- Trace and video capture on failure and retry in CI; off on the green
  path so the suite stays fast.
- E2E covers critical journeys only. Anything expressible as a unit or
  integration test belongs at that layer instead.
- Retry counts are never raised to hide flakiness; a flaky test is
  root-caused or quarantined.
```

## Fragment: review lens

```text
Review this Playwright suite as an E2E reliability reviewer:
1. Grep for waitForTimeout, sleep, and bare setTimeout — each is a
   finding unless commented with the condition it substitutes for.
2. Scan locators; flag auto-generated CSS classes, deep descendant
   chains, and nth-child indexing. Name the role/label replacement.
3. Check every locator action for a missing await.
4. Look for cross-test dependencies: module-level mutable state,
   shared seeded rows, tests that assume execution order.
5. Check data setup — API/fixture-seeded per test, or assumed
   environment state?
6. Check CI config for trace/video on failure, and for retry counts
   inflated to mask flakiness.
7. Count E2E tests; name any covering UI permutations that belong at
   the unit or integration layer.
Report by severity with the specific replacement locator or wait.
```

## Fragment: flake triage protocol

```text
Triage a flaky Playwright test:
- Reproduce with repeated runs at full parallelism, not one local run
  — flakiness usually needs contention to surface.
- Read the trace from the failing run first; identify the exact step
  and what the DOM held at that moment.
- Classify the cause: (a) timing — an implicit assumption the app had
  settled; (b) isolation — state leaked from another test; (c) locator
  — matched a different or transient element; (d) a real product race.
- Fails only in CI → resource contention plus a bypassed auto-wait.
  Fails only when run alongside others → isolation.
- Fix at the cause: state-based wait, per-test data and fresh context,
  role-based locator, or a product bug report.
- Raising retries does not close the ticket.
```

## Fragment: locator hardening pass

```text
Harden the locators in these tests:
- Replace each CSS-class, XPath, or structural selector with the
  highest rung of the ladder that resolves it: getByRole → getByLabel
  / getByText → getByTestId → CSS as last resort.
- If no role or accessible name exists to select by, that is an
  accessibility defect — fix the component, do not reach for a test id
  to route around it.
- Scope ambiguous matches with a container locator, not with nth().
- Output: table of old selector → new locator → component change.
```

## One-liner (for tight token budgets)

```text
Playwright: wait on state never on time (no waitForTimeout); locators
by role/label/text, testid as escape hatch, never CSS class chains;
fresh context and API-seeded data per test, zero shared state;
trace/video on failure; E2E for critical journeys only; root-cause
flakes instead of raising retries.
```
