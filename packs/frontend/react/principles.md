# Principles — React Pack

- **RC1** — State updates are immutable; never mutate state/props objects directly.
- **RC2** — Hooks are called unconditionally, at the top level, every render — never inside conditionals/loops.
- **RC3** — List items use stable, unique `key`s (an ID), never array index for lists that reorder/filter.
- **RC4** — Derived values are computed during render (or memoized), not duplicated into separate state that can drift.
- **RC5** — Side effects live in `useEffect`/event handlers, never inline in the render body.
- **RC6** — Server components are the default in RSC-capable frameworks; `"use client"` is added only where interactivity/browser APIs are actually needed.
- **RC7** — Expensive computation/re-renders are memoized (`useMemo`/`memo`) only after profiling shows a real cost — not reflexively on every component.
- **RC8** — Composition (children props, compound components) is preferred over deep prop drilling or boolean-prop proliferation for flexible components.
