# Prompt Fragments — CI/CD Pack

```text
Apply CI/CD discipline (AKOS L2): order pipeline stages fast-first (lint/
typecheck/unit before build/E2E/deploy); branch protection requires a
green pipeline before merge; secrets in the CI platform's secret
manager, never committed config; production deploy automated from a
passing pipeline, no manual drift-prone steps; rollback is a single
tested automated action; keep pipeline runtime budgeted via caching/
parallelization.
```
