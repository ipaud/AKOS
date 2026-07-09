# Engineering Rules — React Pack

- RE1. State updates use setter functions with immutable patterns (spread/map/filter), never direct mutation.
- RE2. Hooks are never called conditionally or inside loops.
- RE3. Lists use stable unique keys; index keys are used only for static, non-reorderable lists.
- RE4. No `useEffect` exists solely to sync one piece of state into another derivable state.
- RE5. `"use client"` is added only to components/files that need interactivity, state, or browser-only APIs.
- RE6. `useMemo`/`useCallback`/`memo` usage is justified by a profiled cost, documented if non-obvious.
- RE7. Props interfaces avoid more than ~4 boolean flags; compound components or discriminated variant props used instead.
