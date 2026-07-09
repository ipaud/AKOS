# Heuristics — Universal Principles Pack

## Gestalt debugging

- Users misgroup elements → check which cue fires falsely: equal spacing across unrelated items (proximity lie), same styling across different kinds (similarity lie), one box around two concepts (region lie).
- Related things feel scattered → add the *weakest sufficient* cue: nudge proximity before drawing boxes.
- Alignment audit: count vertical edges on the screen; more than ~3 primary edges = visual disorder regardless of spacing.

## 80/20 in practice

- Quarterly: pull usage analytics; list top-5 actions vs their click-depth and polish. Any top-5 action deeper than 2 interactions is a finding.
- Any surface where the rare crowds the frequent (advanced fields inline, edge-case buttons in toolbars) → disclose or demote.
- Docs/support: the top handful of questions deserve in-product fixes, not better articles ([FAQ-as-bug-list](../steve-krug/anti-patterns.md)).

## Forgiveness audit

- List every destructive/irreversible action; for each: undo? draft? retention window? If the answer is "confirmation dialog only", the design is punishing, not forgiving.
- Watch for fear signals: "are you sure?" tickets, users exporting backups, low adoption of powerful features.

## Load shaving

- For any flow, count decisions + inputs + recalls per step; each step should shave at least one via default, inference, or removal before shipping.
- Two designs tie on looks → pick the lower-load one; ties are always breakable by load.

## Flexibility pricing

- Every proposed option/setting/mode answers: who needs it, what % of users, what does it cost the rest? No answer → no option ([YAGNI's UX twin](../../architecture/clean-architecture/README.md)).
- Existing settings page audit: any toggle <2% of users touch is a candidate for a default + removal.

## Signal-to-noise pass

- For each element: what does the user learn or do because of it? Nothing → noise → cut ([H8](../nielsen-norman-group/principles.md), [copy halving](../steve-krug/heuristics.md), [border audit](../refactoring-ui/heuristics.md) — same knife, different handles).
