# Principles — Refactoring Pack

- **RF1 — Refactor continuously, not as a separate phase.** Interleaved with feature work, driven by the rule of three and by "make the change easy."
- **RF2 — Never mix refactoring and behavior change in one step.** One hat at a time; ideally one commit per hat.
- **RF3 — Every step is small and independently verifiable.** If a step can't be verified by running tests in under a minute, it's too big — split it.
- **RF4 — Tests must exist and pass before refactoring starts**, and pass again after each step. No test coverage on the code being touched → write characterization tests first, or accept elevated risk explicitly.
- **RF5 — Name the smell before choosing the refactoring.** Diagnosis before treatment avoids applying a familiar refactoring to the wrong problem.
- **RF6 — Prefer the standard, named refactoring** (Extract Function, Rename, Move Function, Inline, etc.) over an improvised restructuring — named refactorings are well-understood, tool-supportable, and reviewable.
- **RF7 — Refactor toward removing duplication on the third occurrence**, not the first or second.
- **RF8 — Rewrite is a last resort**, chosen only when incremental refactoring has been tried and structurally can't reach the target (e.g., a foundational technology change) — and even then, prefer the strangler-fig pattern (incremental replacement behind a facade) over a big-bang cutover.
- **RF9 — Refactoring has a cost budget too.** Not every smell needs fixing today; prioritize refactorings that unblock the current or next feature, and leave the rest noted.
