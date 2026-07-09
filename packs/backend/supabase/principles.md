# Principles — Supabase Pack

- **SB1 — RLS is enabled on every table containing real user data**, from the moment the table is created — never deferred to "before launch."
- **SB2 — A policy exists for every operation a table's rows can undergo** (SELECT/INSERT/UPDATE/DELETE); a missing policy means that operation is denied by default (safe), but should be an explicit decision, not an oversight discovered later.
- **SB3 — `service_role` key never reaches client-side code** — browser bundles, mobile app binaries, or any client-inspectable surface.
- **SB4 — Policies are tested with multiple user identities**, not just verified to "look right" by reading the SQL — an actual query as user A attempting user B's data.
- **SB5 — Storage buckets have policies matching their sensitivity** (public buckets are a deliberate choice, not a default; private buckets have RLS-equivalent storage policies).
- **SB6 — Edge functions handle logic that RLS can't express** (cross-table business rules, third-party integrations, service_role-requiring operations) rather than routing around RLS with elevated client keys.
- **SB7 — Auth state changes (sign-out, password change) invalidate sessions server-side**, matching [OWASP OW12](../../security/owasp-top-10/engineering-rules.md).
