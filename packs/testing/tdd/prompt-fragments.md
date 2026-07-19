# Prompt Fragments — TDD Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply TDD discipline (AKOS L2):
- For logic-bearing code the failing test exists first. Run it and
  read the failure message — confirm it fails for the intended reason,
  not from a typo, wrong import, or broken setup.
- A test that passes the first time it runs has not been verified.
  Break the implementation briefly to prove the test can fail.
- Green means the smallest change that satisfies the current test. No
  extra branches, no parameters no test demands, no error handling
  nothing asserts. Generality is earned by the next test.
- When the smallest passing change is a hardcoded return, that is a
  legitimate step — add a second test with different input to force
  the generalization rather than guessing at it.
- Refactor only from green, and only structure: no new behavior, no
  new assertions, no observable signature change. Suite green before
  and after, with the same set of tests passing.
- Assertions target observable behavior — return values, emitted
  events, persisted state, thrown errors. Never private methods, call
  counts, or internal field shape.
- Keep cycles at minutes. A test needing an hour of implementation is
  too coarse; split it into a smaller behavior.
- A unit that is hard to test is reporting a design problem — hidden
  dependency, too many responsibilities. Fix the design; do not add
  mocks to route around it.
- Bug fixes start with a test that reproduces the bug.
```

## Fragment: review lens

```text
Review this change as a TDD reviewer:
1. Does every piece of new logic-bearing code have a test that would
   fail without it? Mentally delete the implementation — which tests
   go red? Untouched tests mean untested code.
2. Is the implementation minimal to its tests, or does it carry
   branches, options, and generality nothing asserts?
3. Do assertions describe behavior, or pin internals — spies on
   private calls, internal-state snapshots, call-count checks that
   break under any harmless restructure?
4. Does any commit labelled "refactor" change behavior? A new or
   changed assertion inside one is a behavior change in disguise.
5. Can any test pass regardless of the implementation — tautological
   assertion, missing await, assertion after an early return?
6. For a bug fix: is there a test that fails against the pre-fix code?
Report by severity, naming the specific missing or misplaced test.
```

## Fragment: regression-first bug fix

```text
Fix this bug test-first:
- Reproduce the defect as a failing test at the cheapest layer that
  exhibits it — usually unit, rarely E2E.
- Assert on the wrong observable behavior becoming correct, not on the
  internal mechanism you expect to change.
- Run it against the current, unmodified code and confirm it fails. A
  regression test that passes before the fix proves nothing.
- Fix minimally to green, then refactor the surrounding code if needed
  with the suite as the safety net.
- Keep the test permanently; it is the guard against the bug's return.
```

## Fragment: testability design probe

```text
This unit is hard to test. Diagnose before mocking:
- What must be constructed or stubbed to exercise it? Each item is a
  dependency the unit reaches for instead of receiving.
- Does it do more than one thing? Split at the seam where the test
  setup starts getting complicated.
- Is state hidden in module scope, clocks, randomness, or I/O? Inject
  those so behavior becomes deterministic input to output.
Propose the design change first; scaffolding only if it cannot move.
```

## One-liner (for tight token budgets)

```text
TDD: failing test first, verified failing for the right reason; the
minimum code to pass, generality earned by the next test; triangulate
before generalizing; refactor only from green and never with new
behavior; assert observable behavior not internals; minute-scale
cycles; hard-to-test means bad design; bug fixes start with a failing
regression test.
```
