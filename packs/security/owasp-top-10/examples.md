# Examples — OWASP Top 10 Pack

## A01 — server-side ownership check

Bad:

```js
app.get('/invoices/:id', (req, res) => {
  const invoice = db.getInvoice(req.params.id); // no ownership check
  res.json(invoice);
});
```

Good:

```js
app.get('/invoices/:id', requireAuth, (req, res) => {
  const invoice = db.getInvoice(req.params.id);
  if (!invoice || invoice.userId !== req.user.id) return res.status(404).end();
  res.json(invoice);
});
```

## A03 — parameterized query

Bad: `db.query("SELECT * FROM users WHERE email = '" + email + "'")`
Good: `db.query("SELECT * FROM users WHERE email = $1", [email])`

## A02 — password hashing

Bad: `db.save({ password: sha256(password) })`
Good: `db.save({ passwordHash: await bcrypt.hash(password, 12) })`

## A10 — SSRF allowlist

Bad: `const preview = await fetch(req.body.url)` (any URL, including internal metadata endpoints).
Good:

```js
const url = new URL(req.body.url);
if (!ALLOWED_HOSTS.includes(url.hostname) || isPrivateIp(url.hostname)) {
  return res.status(400).json({ error: 'URL not allowed' });
}
const preview = await fetch(url);
```

## A08 — safe deserialization

Bad: `pickle.loads(request.body)` on an untrusted upload (Python) — arbitrary code execution risk.
Good: `json.loads(request.body)` validated against a strict schema (e.g. Pydantic/Zod), rejecting unknown fields.

## A05 — generic client error, detailed server log

```js
app.use((err, req, res, next) => {
  logger.error({ err, path: req.path, userId: req.user?.id }); // detailed, server-side
  res.status(500).json({ error: 'Something went wrong. Please try again.' }); // generic, client-facing
});
```
