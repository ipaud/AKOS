# Heuristics — Git Pack

- A commit touching unrelated files/concerns → split into separate commits before pushing.
- A commit message that's just "fix" or "wip" → rewrite to state what and why before it becomes permanent history.
- A feature branch alive for weeks with major drift from main → rebase/merge from main now, don't wait for a painful conflict later.
- About to force-push → check if anyone else has pulled this branch first.
- Accidentally committed a secret → rotate the secret immediately; history rewrite alone isn't sufficient if it was ever pushed.
