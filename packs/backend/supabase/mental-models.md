# Mental Models — Supabase Pack

- **RLS as the API layer:** with the client hitting Postgres via PostgREST directly, RLS policies are the *only* authorization boundary for that access path — there's no implicit "the server checked it first."
- **`anon` vs `authenticated` vs `service_role` keys:** `anon`/`authenticated` keys are safe to ship client-side *because* RLS constrains what they can do; `service_role` bypasses RLS entirely and must never reach the client.
- **Policies as per-operation, per-table rules:** SELECT/INSERT/UPDATE/DELETE each get their own policy — a table readable by its owner isn't automatically writable by them unless a matching policy exists.
- **Edge functions as the escape hatch for what RLS can't express:** complex cross-table business logic, third-party API calls, or service_role-requiring operations belong in an edge function (server-side, controlled), not client code with elevated keys.
