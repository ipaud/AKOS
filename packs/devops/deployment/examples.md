# Examples — Deployment Pack

## Expand-contract migration

```
Deploy 1 (expand): add nullable `email_verified` column; app writes to
  both old and new logic paths; backfill existing rows.
Deploy 2 (contract, days later, after confirming no issues): make
  column NOT NULL; remove old verification-tracking logic.
```

## Canary rollout config

```yaml
rollout:
  strategy: canary
  steps:
    - setWeight: 10   # 10% of traffic for 10 min
    - pause: 10m
    - setWeight: 50
    - pause: 10m
    - setWeight: 100
```

## Post-deploy smoke test

```bash
#!/bin/bash
curl -f https://app.example.com/api/health || exit 1
curl -f https://app.example.com/api/orders/ping || exit 1
echo "Smoke tests passed"
```

## Blue-green cutover

Two full production environments (blue = current, green = new release); traffic switches at the load balancer once green passes health checks; blue stays warm for instant rollback if issues appear post-cutover.
