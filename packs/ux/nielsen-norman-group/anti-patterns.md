# Anti-Patterns — NN/g Pack

Organized by the heuristic they violate.

## Silent machine (H1)

No feedback on save, background jobs invisible, sync state unknowable. Users develop superstitions (double-saving, refreshing). Fix: NG1–NG4.

## Org-chart vocabulary (H2)

UI speaks internal language: "SKU entities", "provisioning", team-name features ("Falcon dashboard"). Fix: product glossary of user words, enforced in review.

## Roach motel (H3)

Easy to enter, hard to leave: subscriptions without cancel paths, wizards without exits, imports that can't be aborted, accounts that can't be deleted. Severity floor: HIGH; legal exposure in many jurisdictions.

## Pattern zoo (H4)

Four button styles, three modal behaviors, two date formats. Each inconsistency is small; the aggregate makes every screen a re-learning event. Fix: NG12–NG15, design tokens.

## Error-message-driven design (H5)

The interface permits everything, then scolds. Every validation message is a design decision deferred to runtime. Fix: NG16–NG19; count error messages as design debt.

## Memory quiz (H6)

"Enter the workspace ID", confirmations without objects, comparisons requiring back-and-forth navigation. Fix: NG20–NG23; show, don't quiz.

## Novice ceiling (H7)

Everything is guided, nothing is fast: no shortcuts, no bulk, no templates; the 500th use is as slow as the 1st. Fix: NG24–NG27. Twin: **expert cliff** — accelerators replace the visible path instead of layering over it.

## Kitchen-sink screen (H8)

Everything the org wants a user to see, on one screen, forever (cf. [Krug kitchen-sink homepage](../steve-krug/anti-patterns.md)). Fix: NG28–NG30; each element justified by user value or removed.

## Toast-and-gone errors (H9)

Actionable errors in 3-second toasts; failures users discover minutes later with no trail. Fix: NG31; errors persist until handled.

## "Something went wrong" (H9)

The null error message: no what, no why, no next step. One grade below it: raw exception text. Fix: NG33.

## Help as landfill (H10)

Docs organized by feature, unreachable from the point of confusion, teaching what the UI should signify. FAQ entries = UI bug reports ([Krug](../steve-krug/anti-patterns.md)). Fix: NG35–NG37.

## Process anti-patterns

- **Heuristics as decoration** — running the checklist after decisions are frozen, findings filed unread. Evaluation must precede commitment.
- **Severity inflation** — everything HIGH; prioritization dies. Rate honestly, use the persistence multiplier.
- **One-pass exhaustiveness claim** — "we heuristic-evaluated it, it's done." Inspection samples; iterate (evaluator effect).
- **Testing to confirm** — recruiting friendly users, leading tasks, helping mid-test. Tests exist to surprise you.
