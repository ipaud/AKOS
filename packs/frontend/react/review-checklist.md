# Review Checklist — React Pack

## High
- [ ] No direct state mutation. (RE1)
- [ ] Hooks called unconditionally at top level. (RE2)
- [ ] Stable keys on reorderable lists. (RE3)

## Medium
- [ ] No redundant state-sync effects. (RE4)
- [ ] "use client" scoped to components that need it. (RE5)
- [ ] Memoization justified by profiling. (RE6)

## Low
- [ ] Boolean-prop proliferation avoided via composition. (RE7)
