# Examples — OWASP ASVS Pack

## Stated target level (AV1)

```markdown
## Security
Target: OWASP ASVS Level 2 (handles payment data via Stripe, PII for
~50k users). Reviewed quarterly against the L2 checklist in
~/DEV/AKOS/packs/security/owasp-asvs/review-checklist.md.
```

## Centralized authorization (AV2)

Bad: each route handler writes its own `if (req.user.id === resource.ownerId || req.user.role === 'admin')`.
Good: `router.get('/orders/:id', authorize('orders', 'read'), handler)` — one `authorize()` policy engine, endpoints declare intent.

## Multi-layer authorization (AV5)

API layer checks `req.user.id === order.userId`. Additionally, Postgres Row-Level Security policy: `CREATE POLICY orders_owner ON orders USING (user_id = current_user_id());` — even a direct DB query (from a BI tool or a bug) can't leak other users' orders.

## Allowlist validation (AV6)

Bad: reject input containing `<script>`, `DROP TABLE`, etc. (denylist, easily bypassed).
Good: `z.string().email()` / `z.enum(['draft','published','archived'])` — define the valid shape, reject everything else.

## Business-logic state machine (AV9)

```
Order states: cart → payment_pending → paid → fulfilled
Transition rules enforced server-side:
- payment_pending → paid requires a verified payment webhook, not a client call
- paid → fulfilled cannot be called twice (idempotency key checked)
- no transition skips a state
```

## Configuration diff on release (AV10)

CI step comparing `staging.env.example` vs `production.env.example` keys, flagging any production-only debug flag or wildcard CORS origin before deploy is approved.
