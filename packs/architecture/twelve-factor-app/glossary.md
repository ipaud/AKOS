# Glossary — Twelve-Factor App Pack

- **Build, release, run** — the three strictly-separated deployment stages.
- **Release** — an immutable, versioned combination of a build and its config.
- **Backing service** — any external resource (DB, cache, queue, API) the app consumes over a network, treated as attached and swappable via config.
- **Stateless process** — a process holding no correctness-critical state beyond the current request/job.
- **Disposability** — the property of being safely startable/killable at any moment with fast startup and graceful shutdown.
- **Dev/prod parity** — minimizing divergence between development and production environments.
- **Port binding** — the app self-serving via a bound port rather than depending on runtime web-server injection.
- **Admin process** — a one-off management task (migration, console, backfill) run in the same environment as the live app.
- **Config** — anything that varies between deploys (credentials, URLs, flags); externalized to the environment.
