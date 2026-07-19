# Prompt Fragments — React Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply React practice (AKOS L2):
- Render is a pure function of props and state. No side effects, no
  mutation, no subscriptions in the render body.
- State updates are immutable — spread/map/filter into a new value.
  Never `state.items.push(x)` or field assignment on state or props.
- Hooks are called unconditionally at the top level, same order every
  render — never in a conditional, loop, or after an early return.
- List keys are stable unique IDs. Index keys only for static lists that
  never reorder, filter, or delete.
- Derive, don't synchronize: compute values from existing state during
  render (or `useMemo` when measurably expensive). No `useEffect` whose
  only job is copying one piece of state into another.
- Effects synchronize with systems outside React — DOM APIs,
  subscriptions, timers, widgets — with complete deps and cleanup.
- In RSC-capable frameworks, server components are the default. Add
  `"use client"` only where interactivity, state, refs, or browser-only
  APIs are actually used, and push it to the leaf, not the tree root.
- Memoize only after profiling shows a real cost; `useMemo`/
  `useCallback`/`memo` applied reflexively is overhead without benefit.
- Prefer composition — children, slots, compound components — over prop
  drilling or boolean flags; >4 booleans is a refactor signal.
```

## Fragment: review lens

```text
Review this React code as a React reviewer:
1. Mutation scan — any direct write to a state or props object/array?
2. Hook rules — any hook after an early return, or inside a condition,
   loop, or nested callback?
3. Keys — every `.map()` producing elements: stable ID or index? If the
   list can reorder, filter, or delete, an index key is a bug.
4. Effects — for each `useEffect`, name the external system it
   synchronizes. If the answer is "another piece of React state", it
   should be derived instead. Check dependency completeness and cleanup.
5. Client boundary — for each `"use client"`, name the interactivity
   requiring it, and whether it can move down to a leaf.
6. Memoization — for each `useMemo`/`useCallback`/`memo`, is there a
   profiled cost behind it, or is it defensive?
7. Component API — prop count, boolean flags, prop-drilling depth.
8. Render cost — object, array, or function literals passed as props to
   memoized children, silently defeating the memo.
Report by severity per review-checklist.md with the concrete edit.
```

## Fragment: effect elimination pass

```text
Audit every `useEffect` in this file. For each, answer: what system
outside React is being synchronized?
- "A value derived from props/state" → delete the effect and its
  companion state; compute during render.
- "An event happened" → move the logic into the handler that caused it.
- "Fetch data" → move to the framework data layer or a query library;
  effect-based fetching leaks race conditions and waterfalls.
- A real external system (DOM API, subscription, timer, third-party
  widget) → keep it; verify dependencies and cleanup.
Output: effects removed, effects kept with the system each one owns.
```

## Fragment: server/client boundary pass

```text
Draw the server/client boundary for this component tree:
- Start from the assumption that every component is a server component.
- Mark a component client only if it uses state, effects, event
  handlers, refs, or browser-only APIs.
- Push `"use client"` to the smallest leaves — a client parent pulls
  every imported child into the client bundle.
- Pass server-fetched data down as props, and server-rendered subtrees
  through `children`, so an interactive shell can wrap static content
  without forcing it client-side.
Report each boundary drawn and what it costs in shipped JS.
```

## One-liner (for tight token budgets)

```text
React rules: render pure, state updated immutably; hooks unconditional
at top level; stable ID keys on any list that reorders; derive values
instead of state-sync effects; effects only for external systems, with
deps and cleanup; server components by default, `"use client"` at the
leaves; memoize only after profiling; composition over boolean props.
```
