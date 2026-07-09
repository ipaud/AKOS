# Engineering Rules — NN/g Pack

Checkable rules grouped by heuristic. Cross-references: [Krug ER](../steve-krug/engineering-rules.md), [Norman NR](../don-norman/engineering-rules.md) — shared ground is cited, not duplicated.

## H1 — Status

- NG1. Async mutations show optimistic state or in-flight indicator; completion confirms with result (= NR9–NR12).
- NG2. List/table views show position context: count, filter state, page/scroll position indicator.
- NG3. Long-lived background work (imports, exports, builds) has a persistent, revisitable status surface — not only a transient toast.
- NG4. Auto-save surfaces its state ("Saving… / Saved · 2m ago"); manual-save surfaces dirty state.

## H2 — Real-world match

- NG5. All user-facing nouns/verbs come from the product glossary of user vocabulary; schema names never leak (= NR23, NR24).
- NG6. Dates, numbers, currency respect locale; relative times ("2h ago") carry absolute tooltips.
- NG7. Options are ordered by user logic (frequency, workflow, magnitude) — alphabetical only when users know the name they seek.

## H3 — Control & freedom

- NG8. Every modal closes via X, Escape, and backdrop (destructive-confirm modals may drop backdrop-close).
- NG9. Every multi-step flow has Back (state-preserving) and an explicit exit; exits warn iff unsaved work exists (= NR17).
- NG10. Undo for content mutations (= NR18); cancel for any operation >10s (= NR10).
- NG11. Anything subscribable/enablable is unsubscribable/disablable in ≤ the same number of steps.

## H4 — Consistency

- NG12. One component per pattern: a single Button/Select/Modal set used everywhere (no per-page variants).
- NG13. Identical actions carry identical labels, icons, and placements app-wide.
- NG14. Platform-standard controls and shortcuts are used unless a measured reason exists (⌘C is never something else).
- NG15. Visual style tokens (spacing, radius, color roles) come from one source of truth.

## H5 — Prevention

- NG16. Structured input uses constrained controls (pickers, steppers, selects, masked inputs) over free text wherever the value space is known (= NR14).
- NG17. Defaults are safe and most-likely; destructive is never default; Enter never triggers destruction.
- NG18. Double-submit prevented mechanically (disable-on-submit + idempotent server).
- NG19. High-cost commitments show a review step restating consequences (= NR16 proportionality).

## H6 — Recognition

- NG20. Confirmation/commit screens restate the object of the action (name, count, scope) — never "Are you sure?" alone.
- NG21. Multi-step flows keep prior choices visible or one tap away.
- NG22. Icon-only buttons only for universally learned icons; all others icon+label (= NR1, Krug mystery-meat).
- NG23. Search offers suggestions/recents; empty search states teach queryable dimensions.

## H7 — Efficiency

- NG24. Full keyboard path through all forms and primary flows (also WCAG — see [wcag pack](../wcag/engineering-rules.md)).
- NG25. Repeatable operations offer bulk selection and bulk action.
- NG26. Frequent-input surfaces offer recents/favorites/templates.
- NG27. Every distinct app state is deep-linkable (URL reflects filters, tabs, selection where sensible).

## H8 — Minimalism

- NG28. Every element on a task screen traces to a user need; org-serving content (promos, upsells) is banned inside task flows.
- NG29. Rare/advanced options sit behind progressive disclosure with a discoverable control.
- NG30. Data displays default to the decision-relevant subset; "show more" reveals the long tail.

## H9 — Error recovery

- NG31. Errors persist until acknowledged or resolved (no vanishing toasts for actionable errors).
- NG32. Field errors render adjacent to fields, with focus moved to the first error (also WCAG).
- NG33. Error copy = what + why + next step, user language (= NR20, Krug ER17); error codes, if needed for support, appear as secondary fine print.
- NG34. Full-page errors (404/500) offer: home, back, search, and support path.

## H10 — Help

- NG35. Empty states teach: what this is + first action (= Krug ER25).
- NG36. Contextual help (hint, popover, link) is available at the point of known confusion — measured by support-ticket mapping.
- NG37. Docs are task-titled ("Invite your team") not feature-titled ("The Members panel"), searchable, and linked from the relevant UI.
