# Supabase Rules — Pau Avila

Supabase/RLS conventions for this owner's projects. Composes with the [supabase pack](../../backend/supabase/README.md) — this file is the personal-layer emphasis on top of it. **These carry safety-floor weight** ([constitution](../../../core/constitution.md)) once a project is deployed anywhere reachable.

## Non-negotiables (any deployed project)

1. **RLS enabled on every table with real user data, at table creation time** — never deferred to "before launch." A new table without RLS is treated as a bug the moment it's created.
2. **`service_role` key never in client-shipped code** — browser bundles, mobile binaries, committed config. Server-side only (edge functions / API routes), with the caller's identity validated first.
3. **Policies scoped with `auth.uid()`**, never always-true (`USING (true)`) placeholders written to silence an RLS error.
4. **Policies tested as multiple real users** — log in as user A, attempt user B's data via the client SDK; RLS gaps are invisible in code review, obvious in this test.

## Standing review rule

Every production (or any deployed) Supabase project gets an RLS/security review before it's considered done — this is a mandatory step in this owner's workflow, matching [principle 6](principles.md).

## Storage

- Buckets explicitly public or private with a stated reason; private content uses signed URLs or storage policies, never a public bucket "to make it work."

## Prototype exception

A genuinely local, never-deployed prototype may defer RLS — but the moment it's deployed anywhere reachable, RLS becomes mandatory (Prototype profile's floor still forbids security leaks, [reasoning-profiles](../../../core/reasoning-profiles.md)).
