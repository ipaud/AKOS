# Glossary — React Pack

- **Reconciliation** — React's process of diffing render output to determine minimal DOM updates.
- **Key** — the identity hint React uses to match list items across renders.
- **Rules of Hooks** — the constraint that hooks are called unconditionally, in the same order, every render.
- **Server component (RSC)** — a component rendered server-side with zero client JS shipped, no interactivity.
- **Client component** — a component hydrated and interactive in the browser (`"use client"`).
- **Derived state** — a value computed from existing state/props rather than stored redundantly.
- **Compound component** — a pattern where a parent owns state and children consume it via context (e.g. `Tabs`/`Tabs.List`/`Tabs.Panel`).
