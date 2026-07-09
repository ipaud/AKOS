# Examples — SRE Pack

## SLI/SLO definition

```
SLI: % of checkout requests completing successfully within 2s
SLO: 99.5% over a rolling 28-day window
Error budget: 0.5% of checkout requests (~3.6 hours of full downtime
  equivalent per month)
```

## Symptom-based alert

Bad: `alert: cpu_usage > 80% for 5m`
Good: `alert: checkout_error_rate > 1% for 5m` (directly reflects user impact; CPU may or may not matter)

## Blameless postmortem excerpt

```
What happened: Deploy at 14:02 introduced a null-pointer bug in the
  pricing service, causing 12% of checkout requests to fail for 23 min.
Why it wasn't caught: no integration test covered the null-discount
  edge case; canary deployment wasn't configured for this service.
Follow-ups:
  - Add integration test for null-discount case (owner: @dana, due Fri)
  - Configure canary deploy for pricing service (owner: @sam, due next sprint)
No individual named as "the cause" — the gap was a missing test and
  missing canary config, both now tracked.
```

## Runbook entry

```
Alert: checkout_error_rate high
1. Check pricing-service logs for the last 15 min: `kubectl logs -l app=pricing --tail=200`
2. If NullPointerException present, roll back to previous release: `akos-deploy rollback --to-previous`
3. Page @pricing-team if rollback doesn't resolve within 5 min
```
