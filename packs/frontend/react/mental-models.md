# Mental Models — React Pack

- **UI as a pure function of state:** given the same props/state, render output is deterministic — side effects belong in `useEffect`/event handlers, never inline in render.
- **Reconciliation via keys:** React matches list items across renders by `key`; unstable/index keys cause incorrect diffing and lost component state.
- **The rules of hooks as a dependency graph contract:** calling hooks unconditionally, in the same order, every render, is what lets React associate state correctly across renders.
- **Server vs. client components:** server components render once on the server (zero client JS cost, direct backend access); client components hydrate and run interactively — the boundary is a deliberate architectural line, not a default.
- **Derived state over synchronized state:** compute values from existing state/props during render rather than mirroring them into a second `useState`, which invites drift.
