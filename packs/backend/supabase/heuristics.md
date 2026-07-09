# Heuristics — Supabase Pack

- New table created → check RLS status immediately, before writing any query against it — `ALTER TABLE x ENABLE ROW LEVEL SECURITY;` is step one, not a later step.
- Grep client-side code (frontend bundle, mobile app) for `service_role` or the service key pattern — it should never appear there.
- Test every policy as an actual "attacker": log in as user A, attempt to read/write user B's row via the client SDK directly — RLS violations are invisible in code review but obvious in this test.
- A feature needing "just this one query to bypass RLS for convenience" → that's an edge function candidate, not a client-side service_role leak.
- Storage bucket created → is it public or private, and does that match what should actually be publicly fetchable?
