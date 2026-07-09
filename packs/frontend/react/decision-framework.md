# Decision Framework — React Pack

Server vs client component: needs interactivity/state/browser APIs/event handlers → client. Otherwise → server (default). State management tier: local UI state → `useState`; server-derived data → a data-fetching library (React Query/SWR/framework loader), not manually synced state; cross-cutting client state → a lightweight store (Zustand/Jotai) only once prop drilling genuinely hurts. Memoization: profile first (React DevTools Profiler); memoize only the specific expensive computation/component identified, not preemptively everywhere.
