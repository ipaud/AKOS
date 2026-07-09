# Examples — OWASP API Security Pack

## API1 — object-level authorization

Bad: `GET /api/orders/:id → db.orders.findById(id)` — any authenticated user can view any order by guessing IDs.
Good: `db.orders.findOne({ id, userId: req.user.id })` — scoped to the requester.

## API3 — field-level allowlisting (DTO)

Bad: `db.users.update(userId, req.body)` — accepts any field including `isAdmin`.
Good:

```ts
const { displayName, avatarUrl } = req.body; // explicit allowlist
db.users.update(userId, { displayName, avatarUrl });
```

## API4 — bounded pagination

Bad: `GET /api/items?limit=999999` returns all rows.
Good:

```ts
const limit = Math.min(parseInt(req.query.limit) || 20, 100); // hard cap
```

## API5 — independent function-level check

```ts
app.delete('/api/admin/users/:id', requireAuth, requireRole('admin'), (req, res) => {
  // role check is separate from any object-ownership logic
});
```

## API6 — anti-automation on checkout

```ts
const attempts = await rateLimiter.check(`checkout:${req.user.id}`, { max: 5, window: '1m' });
if (!attempts.allowed) return res.status(429).json({ error: 'Too many attempts' });
```

## API8 — CORS scoped correctly

Bad: `cors({ origin: '*', credentials: true })`
Good: `cors({ origin: ['https://app.example.com'], credentials: true })`

## API10 — validating third-party responses

```ts
const rawData = await weatherApi.get('/forecast');
const parsed = WeatherResponseSchema.safeParse(rawData);
if (!parsed.success) {
  logger.warn('Unexpected weather API response shape', parsed.error);
  return fallbackForecast();
}
useForecast(parsed.data);
```
