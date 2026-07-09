# Mental Models — Git Pack

- **Commits as atomic, reviewable units:** each commit should be a complete, logical, ideally-revertable-independently change — not a save-point snapshot of wherever you happened to stop.
- **History as documentation:** commit messages answer "why," since the diff already answers "what."
- **Branches as short-lived integration units:** long-lived divergent branches accumulate merge conflict risk; trunk-based or short-lived feature branches minimize it.
- **Force-push as a scoped, communicated operation:** rewriting shared history without warning breaks collaborators' local state — force-push is safe only on branches nobody else has pulled, or with explicit coordination.
