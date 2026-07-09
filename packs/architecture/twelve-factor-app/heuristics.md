# Heuristics — Twelve-Factor App Pack

- **Grep for hardcoded config.** URLs, credentials, feature flags in source (even in a "config file" committed to git) — should be env vars supplied at runtime.
- **The "kill -9 test":** can the process be killed at any random moment with no data loss and a clean restart? If not, state has leaked into the process.
- **The "clone and run" test:** can a new team member clone the repo, set env vars, and run the app with zero manual steps beyond documented setup? Friction here signals dependency/config problems.
- **The "scale by cloning" test:** can load be handled by running more identical processes rather than making one process bigger/more complex? If not, statelessness may be violated.
- **Backing-service swap test:** could the local dev database be swapped for a different provider by changing one config value, with zero code changes? If not, the backing service isn't properly abstracted.
- **Logs check:** does the app write to stdout, or does it manage its own log files/rotation? The latter fights the platform.
- **Admin task check:** are migrations/console tasks run via the same deploy artifact and config as the running app, or via a separate ad-hoc script with its own environment assumptions?
