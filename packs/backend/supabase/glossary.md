# Glossary — Supabase Pack

- **RLS (Row-Level Security)** — Postgres's per-row access control mechanism, Supabase's primary authorization layer.
- **Policy** — a rule defining which rows a given operation (SELECT/INSERT/UPDATE/DELETE) can affect for a given role.
- **`anon` key** — the public, RLS-constrained API key safe for client-side use.
- **`service_role` key** — the privileged key bypassing RLS entirely; server-side only, never client-exposed.
- **`auth.uid()`** — the Postgres function returning the currently authenticated user's ID within a policy.
- **Edge function** — a server-side Deno function for logic RLS can't express or that requires service_role.
- **Storage policy** — RLS-equivalent access control for Supabase Storage buckets/objects.
