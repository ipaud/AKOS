# Review Checklist — Refactoring Pack

## High

- [ ] Behavior changes and structural refactoring are separated (commits/PRs). (MF1)
- [ ] Refactored code has test coverage; characterization tests added where missing. (MF3)
- [ ] Full test suite passes at each meaningful checkpoint, not just at the end. (MF2)

## Medium

- [ ] Duplication extracted only at the third occurrence, not preemptively. (MF4, RF7)
- [ ] Refactoring steps map to named catalog refactorings, reviewable individually. (MF5)
- [ ] Unrelated smells spotted in review are filed as follow-ups, not scope-crept into this PR.

## Low

- [ ] Rewrite decisions (if any) have a recorded justification for why incremental refactoring was insufficient. (MF6)
- [ ] Comments explaining "what" are replaced by clearer extracted names where feasible.
