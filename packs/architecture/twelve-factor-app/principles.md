# Principles — Twelve-Factor App Pack

1. **Codebase** — one codebase tracked in version control, many deploys (dev/staging/prod all deploy from the same codebase at different versions/config).
2. **Dependencies** — explicitly declare and isolate all dependencies (lockfiles, no reliance on system-wide packages assumed to "just be there").
3. **Config** — store config that varies between deploys in the environment (env vars), never in code, never committed.
4. **Backing services** — treat backing services (DB, cache, queue, third-party APIs) as attached resources, accessed via config-supplied URLs, swappable without code change.
5. **Build, release, run** — strictly separate the build, release, and run stages; releases are immutable and versioned.
6. **Processes** — execute the app as one or more stateless, share-nothing processes; persistent state lives in a backing service.
7. **Port binding** — the app is self-contained and exports services via port binding, not relying on runtime injection of a web server.
8. **Concurrency** — scale out via the process model (more processes/workers), not by making individual processes heavier.
9. **Disposability** — maximize robustness with fast startup and graceful shutdown; processes can be started/stopped at a moment's notice.
10. **Dev/prod parity** — keep development, staging, and production as similar as possible (same backing services, small time gap between deploy and dev, same people involved).
11. **Logs** — treat logs as event streams written to stdout; let the execution environment handle routing/storage/rotation.
12. **Admin processes** — run one-off admin/management tasks (migrations, consoles) as one-off processes in an identical environment, using the same codebase and config as the app.
