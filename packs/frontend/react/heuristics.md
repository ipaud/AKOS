# Heuristics — React Pack

- Array `.map()` using `index` as `key` on a reorderable/filterable list → switch to a stable ID.
- A `useEffect` syncing one state to another (`useEffect(() => setB(a), [a])`) → usually should be computed inline or via `useMemo`, not a second state + effect.
- New component defaulting to `"use client"` without checking if it needs interactivity/browser APIs → try server component first.
- `useMemo`/`useCallback` added everywhere reflexively → profile first; premature memoization adds complexity without proven benefit.
- A component with 5+ boolean props → candidate for compound-component or variant-prop refactor.
