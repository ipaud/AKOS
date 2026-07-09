# Engineering Rules — Refactoring Pack

- MF1. A commit/PR that changes behavior and restructures code in the same diff is split into separate commits (or separate PRs) — one for the refactor, one for the behavior change.
- MF2. Refactoring commits pass the full relevant test suite before and after; no refactoring commit lands with a broken or skipped test.
- MF3. Code with no test coverage gets characterization tests before structural refactoring begins, unless the change is trivial (rename, single-file extract with obvious equivalence).
- MF4. Duplicated logic is not extracted into an abstraction until it appears a third time; the first two occurrences are left duplicated intentionally.
- MF5. Refactoring steps are named after standard catalog refactorings (Extract Function, Rename, Move Function, Inline, Introduce Parameter Object, etc.) in commit messages/PR descriptions where feasible — aids review and tooling.
- MF6. A rewrite (as opposed to incremental refactoring) requires an explicit decision record naming why incremental refactoring was judged insufficient.
