# Prompt Fragments — Refactoring Pack

## Fragment: build-mode constraint block

```text
Apply disciplined refactoring practice (AKOS L2):
- Never mix behavior changes and structural refactoring in the same step
  or commit — separate them (refactor hat vs. feature hat).
- Before refactoring code with no test coverage, add characterization
  tests capturing current behavior.
- Take small steps; run tests after each; commit at each green checkpoint.
- Extract duplication on the third occurrence, not the first or second
  (rule of three) — resist speculative abstraction.
- Name refactorings using the standard catalog (Extract Function, Move
  Function, Inline, Introduce Parameter Object, Rename) for reviewability.
- Prefer incremental refactoring over rewrites; if a rewrite is truly
  necessary, use a strangler-fig incremental replacement, not a big-bang
  cutover.
```

## Fragment: review lens

```text
Review this diff for refactoring discipline:
1. Behavior/structure mixing — does this PR change both behavior and
   structure in the same commit? Flag for splitting if so.
2. Test safety net — is refactored code covered by tests that ran green
   before and after?
3. Smell scan — identify code smells present (long method, large class,
   duplicated code, feature envy, primitive obsession, shotgun surgery)
   and name the standard refactoring that addresses each.
4. Premature abstraction check — was anything extracted/generalized after
   only one or two occurrences?
5. Scope check — are unrelated smells noted as follow-ups rather than
   folded into this change?
```

## One-liner

```text
Refactoring: one hat at a time (structure XOR behavior per step); tests
green before and after every step; extract on the third duplicate, not
the first; name smells, apply the standard refactoring; incremental
strangler-fig over big-bang rewrites.
```
