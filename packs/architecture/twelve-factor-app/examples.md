# Examples — Twelve-Factor App Pack

## Config from environment (TF1)

Bad:

```js
const dbUrl = "postgres://prod-user:hunter2@db.internal:5432/app";
```

Good:

```js
const dbUrl = process.env.DATABASE_URL;
if (!dbUrl) throw new Error("DATABASE_URL not set");
```

`.env.example` documents required vars with placeholder values; real values never committed.

## Stateless session handling (TF3)

Bad: `req.session.cart = items` stored in process memory (`express-session` with the default `MemoryStore`).
Good: session store backed by Redis (`connect-redis`) — any process instance can serve any request.

## Graceful shutdown (TF6)

```js
process.on('SIGTERM', async () => {
  server.close(() => process.exit(0)); // stop accepting new requests, finish in-flight, then exit
});
```

## Logs as a stream (TF8)

Bad: custom `fs.appendFile('/var/log/app.log', ...)` with manual rotation.
Good: `console.log(JSON.stringify({ level: 'info', msg: 'order placed', orderId }))` — platform (Docker/k8s/PaaS) captures stdout and routes it.

## Build/release/run separation (TF10)

- Build: `docker build -t app:abc123 .` (code → artifact, no config baked in).
- Release: `app:abc123` + `DATABASE_URL=prod-url` + `LOG_LEVEL=info` → release `v42`.
- Run: platform starts N instances of release `v42`.
- Rollback: run release `v41` again — no rebuild needed.

## Admin process parity (TF9)

```bash
# Migration run with the exact same image and env as the live app:
docker run --env-file .env.production app:abc123 npm run migrate
```

Not a developer's laptop with manually copied env vars.
