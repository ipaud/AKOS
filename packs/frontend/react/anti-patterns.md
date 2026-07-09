# Anti-Patterns — React Pack

- **Index-as-key on reorderable lists** — causes wrong component state to stick to the wrong item after a reorder/filter/delete.
- **State-sync effects** — `useEffect` whose only job is copying one state into another, introducing a render-lag bug and unnecessary re-renders.
- **Everything is a client component** — `"use client"` slapped at the top of every file by default, forfeiting the zero-JS server-component benefit everywhere.
- **Reflexive memoization** — `useMemo`/`useCallback` wrapping every value "for performance," adding cognitive and runtime overhead with no measured benefit.
- **Prop drilling through 5+ layers** — passing the same prop down a long component chain instead of composition/context/compound components.
- **Direct state mutation** — `state.items.push(x)` instead of `setState([...state.items, x])`, silently breaking React's change detection.
