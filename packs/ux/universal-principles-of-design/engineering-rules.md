# Engineering Rules — Universal Principles Pack

Rules here fill gaps between other packs' rules; overlaps are cited to their owners.

- UD1. Spacing ratios encode grouping app-wide: unrelated ≥ 1.5× related spacing (owner: [RU10](../refactoring-ui/engineering-rules.md), [ER13](../steve-krug/engineering-rules.md)).
- UD2. One visual style per semantic kind: identical functions look identical; different functions look different (similarity both ways).
- UD3. Enclosure (cards/boxes) only where proximity + background shift are insufficient.
- UD4. Layouts align to a grid; primary alignment edges per screen ≤3.
- UD5. Modal/layer stacking always disambiguated (scrim, elevation) — figure-ground never ambiguous.
- UD6. Top-5 user actions (by analytics or design intent) reachable within 2 interactions from their natural context.
- UD7. Rare/advanced capability behind progressive disclosure, with a discoverable control (owner: [NG29](../nielsen-norman-group/engineering-rules.md)).
- UD8. Sequences >5 items chunked into named groups (steps, sections, phases).
- UD9. Every destructive action has a forgiveness mechanism beyond confirmation where technically feasible: undo, trash retention, drafts, versioning (owner: [NR18](../don-norman/engineering-rules.md); this rule extends it to *storage design* — soft-delete columns, history tables).
- UD10. New options/settings ship with a recorded flexibility price (who needs it, % served, cost to the rest); settings pages audited yearly for <2%-usage toggles.
- UD11. Decorative elements carrying no signal are absent from task surfaces (owner: [NG28](../nielsen-norman-group/engineering-rules.md)).
- UD12. Feedback loops close: any user action with delayed consequences surfaces those consequences where the user will see them (job status, quota impact, billing effect).
