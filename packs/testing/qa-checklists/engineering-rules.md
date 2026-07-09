# Engineering Rules — QA Checklists Pack

- QA-E1. Pre-release checklist includes explicit verification of empty/loading/error/success states for all new/changed async surfaces.
- QA-E2. Boundary-value testing (zero/one/max items, long/special-character input) is performed on new form/list features before release.
- QA-E3. At least one test pass simulates degraded network conditions (offline or slow) on the primary flow being shipped.
- QA-E4. Browser/device test matrix is derived from real analytics data, reviewed periodically as usage shifts.
- QA-E5. Exploratory testing sessions have a written charter and log findings with reproduction steps.
- QA-E6. Previously-fixed critical/high bugs have a regression check before each release (automated where possible, manual checklist otherwise).
