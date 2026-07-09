# Scoring Rubric — Twelve-Factor App Pack

Feeds [scoring/architecture-score.md](../../../scoring/architecture-score.md) and release-readiness scoring.

| Finding | Deduction |
|---------|-----------|
| Secrets/credentials committed to source control | −25 (CRITICAL — also security) |
| Correctness-critical state held only in process memory | −15 (HIGH) |
| No graceful shutdown handling | −10 (HIGH) |
| Admin tasks run in a divergent environment from the live app | −10 (HIGH) |
| Self-managed log files instead of stdout streaming | −4 (MEDIUM) |
| Dev/prod backing-service type mismatch | −4 (MEDIUM) |
| Scaling achieved by growing a single process instead of the process model | −4 (MEDIUM) |
| Mutable in-place release "hotfixes" | −6 (MEDIUM) |

Anchors: **90** fully twelve-factor compliant, safely scalable and disposable · **75** solid with minor parity gaps · **60** stateful processes or self-managed logging causing operational pain · **<50** committed secrets or unsafe deploy practices, BLOCKED for Production.
