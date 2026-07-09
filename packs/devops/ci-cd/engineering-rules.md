# Engineering Rules — CI/CD Pack

- CI-E1. Pipeline runs lint/typecheck/unit tests before build/integration/E2E stages.
- CI-E2. Branch protection requires the pipeline to pass before merge to main.
- CI-E3. Pipeline secrets are stored in the CI platform's secret manager, never in repo-committed config.
- CI-E4. Deployment to production is triggered automatically from a passing pipeline on main (or an explicit, auditable manual trigger with the same verified artifact) — never a separately-built artifact.
- CI-E5. Rollback to the previous release is a single automated action (command/button), tested at least once outside a real incident.
- CI-E6. Pipeline caching (dependencies, build artifacts) is configured to keep runtime reasonable as the codebase grows.
