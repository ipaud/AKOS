# Anti-Patterns — Git Pack

- **"wip" / "fix" commit messages** — permanent history with no useful information for future archaeology.
- **Mega-commits** — one commit touching 60 files across unrelated features, impossible to review or bisect meaningfully.
- **Committed secrets** — API keys/passwords committed then "removed" in a later commit, still fully present in history for anyone who clones.
- **Force-push to shared branches** — rewriting main/shared branch history, breaking every collaborator's local checkout silently.
- **Weeks-long feature branches** — massive drift from main producing a merge-conflict nightmare at integration time.
