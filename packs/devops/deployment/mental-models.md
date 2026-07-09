# Mental Models — Deployment Pack

- **Blast radius as the deployment risk unit:** how much of production/how many users are affected if this release is bad, before detection and rollback.
- **Canary releases:** deploy to a small percentage of traffic first, monitor, then progressively increase — bugs are caught while affecting few users.
- **Blue-green deployment:** two full production environments, traffic switches atomically between them — enables instant rollback (switch back) at the cost of running double infrastructure briefly.
- **Expand-contract migrations:** schema/data changes happen in safe stages (add new, dual-write, migrate reads, remove old) so the deployed application and the database schema are never in an incompatible state during rollout.
- **Rollback as a first-class deployment feature**, not an emergency improvisation — designed and tested before it's needed.
