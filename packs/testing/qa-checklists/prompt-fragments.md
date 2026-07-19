# Prompt Fragments — QA Checklists Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply QA verification discipline (AKOS L3):
- Every async or data-driven surface implements and is checked in all
  four states: empty, loading, error, success. The empty state is
  designed and seen against real empty data, never assumed.
- Collections are exercised at zero items, one item, and a large set.
  Each surfaces its own bug class: missing guidance, pluralization and
  layout, pagination and performance.
- Every text input is probed with maximum-length content, emoji and
  non-Latin characters, leading/trailing whitespace, and markup-like
  strings — handled or rejected clearly, never silently mangled.
- Degraded network is exercised on the primary flow: offline,
  throttled connection, request timeout, disconnect mid-submit. The
  app fails visibly and leaves no half-written state.
- Destructive actions are tested for their guard — confirmation or
  undo — and for what is actually lost when the guard is bypassed.
- Submit controls disable on first activation; double-submit produces
  one effect, not two.
- The browser and device matrix comes from real analytics share, not
  from a guessed list of theoretical combinations.
- Previously fixed critical and high bugs carry a regression check
  that runs before each release.
```

## Fragment: review lens

```text
Review this feature as a pre-release QA reviewer:
1. For each async surface, demand evidence of all four states — empty,
   loading, error, success. Flag any that exists only in theory.
2. Walk the boundaries: zero items, one item, many. Then max-length,
   emoji, and markup-like input in every field.
3. Interrupt the primary flow — go offline mid-submit, kill the
   request, double-click the submit control. Note hangs, silent
   failures, and state left half-written.
4. Read the error messages: do they say what happened and what to do
   next, or surface a raw status code?
5. Compare the tested browser/device set against analytics share.
6. Confirm previously fixed critical and high bugs are re-verified.
7. Confirm findings carry steps, expected, and actual — an
   unreproducible report is not a finding.
Report by severity with reproduction steps for each.
```

## Fragment: exploratory session charter

```text
Run a time-boxed exploratory session:
- State one charter before starting: the area and the risk being
  hunted ("explore checkout for data loss under interruption").
- Time-box it (45-90 minutes). Do not drift; log unrelated areas for a
  later charter instead of chasing them now.
- Vary deliberately along one axis at a time: input extremes, timing
  and interruption, action ordering, permission and role, device and
  viewport.
- Log every finding with exact steps, expected, actual, environment.
  Anything not reproducible is recorded as unconfirmed — neither
  dropped nor filed as a bug.
- Close with the top three risks found and what remains unexplored.
```

## Fragment: release regression sweep

```text
Build the pre-release regression pass:
- List critical and high bugs fixed since the last release; each needs
  a check that fails if the bug returns.
- Automate every check that is deterministic and repeatable; keep only
  judgment-based checks manual.
- Include primary flows this release did not touch — regressions
  surface most often where nobody looked.
- Run it on the analytics-derived browser/device set, not the
  developer machine alone.
Output: pass/fail per item, blocking failures named first.
```

## One-liner (for tight token budgets)

```text
QA sweep: four states (empty/loading/error/success) on every async
surface; boundaries at zero/one/many; max-length, emoji, and
markup-like strings in every input; offline and mid-submit
interruption on the primary flow; guarded destructive actions and
disabled double-submit; browser matrix from analytics not guesses;
regression check on past critical bugs; findings logged reproducibly.
```
