# Engineering Rules — Twelve-Factor App Pack

- TF1. No secrets, URLs, or environment-varying config values are committed to source control; all such values are read from environment variables at runtime.
- TF2. A dependency manifest with a lockfile pins exact versions; the build fails if dependencies aren't fully declared (no reliance on globally pre-installed packages).
- TF3. Application processes hold no state required for correctness beyond the current request/job; session/cache/queue state lives in a backing service.
- TF4. The app binds its own port and serves requests directly (or via a declared, versioned web server dependency) rather than requiring injection of a runtime-provided server.
- TF5. Horizontal scaling is achieved by running more process instances, not by increasing single-process resource limits as the primary scaling lever.
- TF6. Processes start within a bounded, short time window and handle SIGTERM by finishing in-flight work and shutting down cleanly (graceful shutdown implemented, not assumed).
- TF7. Development environment uses the same type of backing services as production (same database engine, same cache technology) — not a lightweight stand-in with different behavior.
- TF8. Application logs are written to stdout/stderr as a stream; the app does not manage its own log file rotation, compression, or storage location.
- TF9. One-off admin/management commands (migrations, data backfills, consoles) run using the identical codebase, dependency versions, and config as the live app — never a divergent script/environment.
- TF10. Builds are immutable once created; a config change produces a new release, never an in-place mutation of a running release's artifact.
