# Principles — QA Checklists Pack

- **QA1** — Every async/data-driven surface is checked in all four states: empty, loading, error, success.
- **QA2** — Boundary values are tested explicitly: zero items, one item, maximum items, minimum/maximum input length, special characters (unicode, emoji, SQL-special chars for injection-adjacent robustness).
- **QA3** — Network conditions are tested: offline, slow 3G, request timeout, mid-request disconnect.
- **QA4** — Cross-browser/device coverage is weighted by real usage data (analytics), not exhaustive theoretical combinations.
- **QA5** — Destructive actions are tested for their guard behavior (confirmation, undo) and for the actual data-loss risk if bypassed.
- **QA6** — Exploratory sessions are time-boxed with a stated charter/focus area, and findings are logged reproducibly (steps, expected vs actual).
- **QA7** — Regression checks cover previously-fixed bugs before each release, not just new functionality.
