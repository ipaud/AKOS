# Scoring Rubric — SRE Pack

| Finding | Deduction |
|---------|-----------|
| No SLO/monitoring on a critical production service | −15 (HIGH) |
| Cause-based-only alerting with no symptom-based alerts | −10 (HIGH) |
| No runbooks for known failure modes | −6 (MEDIUM) |
| Blame-oriented postmortems / no postmortem practice | −6 (MEDIUM) |
| High alert-noise ratio (many ignored pages) | −6 (MEDIUM) |
| Toil untracked, no automation investment | −2 (LOW) |

Anchors: 90 full SLO discipline, low-noise alerting, blameless culture · 75 solid with a gap · 60 reactive-only operations · <50 no monitoring/alerting discipline at all.
