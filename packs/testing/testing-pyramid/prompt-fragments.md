# Prompt Fragments — Testing Pyramid Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply testing-pyramid balance (AKOS L2):
- Default new coverage to the fast layer: pure logic, branching rules,
  parsing, calculation, and utilities get unit tests that run in
  milliseconds with no I/O.
- Integration tests cover real seams — endpoint against a real
  database, service against its actual client — with the boundary
  under test left unmocked. Mocking the seam being verified makes the
  test assert your assumptions instead of the contract.
- Keep the integration layer. Unit-plus-E2E only leaves the component
  boundaries where most cross-system bugs live unverified.
- E2E is reserved for critical user journeys — signup, checkout, the
  core task the product exists for. Adding one requires stating why
  unit and integration coverage cannot reach it.
- Choose the layer by what is being verified: is this function correct
  → unit; do these two real components cooperate → integration; can a
  user complete the task → E2E.
- For a production bug, add coverage at the cheapest layer that would
  have caught it. A logic bug gets a unit test, not an E2E test.
- A flaky test is fixed or quarantined within the sprint. Never leave
  one intermittently green — it erodes trust in every other result.
- Suite runtime is a budget: the unit layer runs on every commit; slow
  layers run sharded, parallelized, or on a reduced trigger.
```

## Fragment: review lens

```text
Review this suite's shape as a test-strategy reviewer:
1. Count tests and runtime by layer. Pyramid, ice cream cone (mostly
   E2E), or hourglass (no integration layer)?
2. For each E2E test, ask what it verifies that unit or integration
   coverage could not. Name the ones that should move down.
3. Check integration tests for a mocked boundary — if the seam under
   test is stubbed, the test proves nothing about the contract.
4. Check unit tests for implementation coupling: assertions that would
   break under a behavior-preserving refactor.
5. Identify tests retried, skipped, or annotated as flaky. Each needs
   a fix owner and date, or a quarantine decision.
6. Find the slowest tests and weigh their runtime against the unique
   confidence they buy.
7. For recent production bugs, check whether coverage landed at the
   fault layer or reflexively at E2E.
Report by severity, naming specific layer moves and tests.
```

## Fragment: layer routing decision

```text
Route this test to a layer:
- Deterministic input to output, no I/O → unit. Default here.
- Crosses a real boundary (handler + database, service + queue, client
  + contract) → integration, with that boundary real.
- Depends on browser rendering, real navigation, or a multi-step user
  path that must hold together → E2E, only if the journey is critical.
- Guarding a bug's return → the lowest layer that reproduces it.
- If two layers would both catch it, take the lower one and stop.
  Duplicating at a higher layer buys runtime cost, not confidence.
```

## Fragment: suite reshaping plan

```text
Rebalance an inverted suite:
- Inventory current tests by layer with counts and runtime; state the
  actual shape before proposing any change.
- For the slowest E2E tests, identify the specific assertion each one
  exists for, and the unit or integration test that would cover it.
- Migrate downward in small batches; an E2E test is deleted only once
  its replacement is green, never before.
- Keep one E2E test per critical journey as the smoke check; delete
  the permutation variants around it.
- Report layer counts and runtime in CI so shape drift stays visible.
```

## One-liner (for tight token budgets)

```text
Pyramid: most coverage in fast unit tests on logic; a real integration
layer at component seams with the seam unmocked; E2E only for critical
journeys and only where lower layers cannot reach; route each
regression test to the cheapest layer that catches the bug; fix or
quarantine flaky tests within the sprint; treat suite runtime as a
budget.
```
