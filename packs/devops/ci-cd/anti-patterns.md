# Anti-Patterns — CI/CD Pack

- **Slow-pipeline bypass** — a 45-minute pipeline routinely skipped or merged around under deadline pressure, defeating its entire purpose.
- **Snowflake manual deploys** — production deployment involving a person SSHing in and running commands from memory/a wiki page, different every time.
- **Secrets in pipeline YAML** — API keys/deploy credentials committed directly in CI config files.
- **Untested rollback** — a documented rollback procedure nobody has actually run since it was written, discovered broken during a real incident.
- **Red main tolerated** — the main branch pipeline failing for days while work continues to pile on top, normalizing a broken build state.
