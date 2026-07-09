# Review Checklist — CI/CD Pack

## High
- [ ] Pipeline stages ordered fast-first (lint/typecheck/unit before build/E2E). (CI-E1)
- [ ] Branch protection requires pipeline pass before merge. (CI-E2)
- [ ] Secrets in CI platform's secret manager, not committed config. (CI-E3)

## Medium
- [ ] Production deploy automated from a passing pipeline. (CI-E4)
- [ ] Rollback is a single tested automated action. (CI-E5)

## Low
- [ ] Pipeline caching keeps runtime reasonable. (CI-E6)
