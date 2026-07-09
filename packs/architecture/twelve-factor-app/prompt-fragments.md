# Prompt Fragments — Twelve-Factor App Pack

## Fragment: build-mode constraint block

```text
Apply twelve-factor discipline (AKOS L2) to any deployable service:
- All environment-varying config (URLs, credentials, flags) read from
  environment variables at runtime; nothing committed to source control.
- Dependencies fully declared with a lockfile.
- Processes are stateless; anything that must persist lives in a backing
  service (DB, cache, queue), not process memory or local disk.
- Graceful shutdown on SIGTERM; fast, bounded startup time.
- Logs written to stdout/stderr as a stream, not self-managed files.
- Admin/one-off tasks (migrations, backfills) run with the identical
  codebase and config as the live app.
- Scale by running more processes, not by growing a single process.
- Builds are immutable; a config change produces a new release, never an
  in-place edit of a running one.
```

## Fragment: review lens

```text
Review this service's deployment readiness against the twelve factors:
1. Config scan — any hardcoded URLs/credentials/flags in source?
2. Statelessness check — any correctness-critical state in process
   memory or local disk that should be in a backing service?
3. Shutdown check — is SIGTERM handled gracefully?
4. Logging check — stdout streaming, or self-managed log files?
5. Admin-task check — same environment as the live app, or a divergent
   ad-hoc script?
6. Parity check — does dev use the same backing-service type as prod?
Report gaps with the specific factor violated and the concrete fix.
```

## One-liner

```text
Twelve-factor: config from environment, never in code; stateless
processes with state in backing services; graceful shutdown; logs to
stdout; admin tasks run identically to the live app; scale via more
processes; immutable releases.
```
