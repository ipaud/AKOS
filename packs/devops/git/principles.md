# Principles — Git Pack

- **GT1** — Commits are atomic: one logical change per commit, each independently reviewable and (ideally) revertable.
- **GT2** — Commit messages state the why, not just the what; a conventional-commits-style prefix (`feat:`, `fix:`, `refactor:`) aids scanning history.
- **GT3** — Feature branches are short-lived (days, not weeks); long-running branches are rebased/merged from main frequently to minimize conflict risk.
- **GT4** — Force-push is used only on branches not shared with others, or with explicit team coordination.
- **GT5** — Sensitive data (secrets, credentials) never enters history — even a later "removal" commit leaves it in history forever without a rewrite.
- **GT6** — Merge strategy (merge commit vs. squash vs. rebase) is chosen deliberately and applied consistently across the repo.
