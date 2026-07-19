# Prompt Fragments — Supabase Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply Supabase practice (AKOS L2 — RLS and key handling are safety-floor
items, never waived by profile once the project is deployed anywhere
reachable):
- ENABLE ROW LEVEL SECURITY in the same migration that creates any table
  holding user-scoped or sensitive data. Not a pre-launch task, not a
  follow-up ticket. With direct client-to-database access, RLS is the
  authorization layer, not a backup to one.
- Write an explicit policy per operation the table actually needs:
  SELECT / INSERT / UPDATE / DELETE. Read access never implies write
  access. No policy means denied — make that denial a decision.
- Scope every policy to the requester: USING (auth.uid() = user_id) on
  reads and deletes, WITH CHECK (auth.uid() = user_id) on INSERT and
  UPDATE. USING (true) is never a shippable policy.
- service_role key lives only in server-side environment variables (edge
  functions, server route handlers). Never in a browser bundle, mobile
  binary, client-exposed env var, or committed config. anon and
  authenticated keys are client-safe only because RLS constrains them.
- Every service_role code path validates the caller's identity and
  permission before the privileged call — service_role bypasses RLS, so
  that check is the only remaining gate.
- Storage buckets are declared public or private deliberately, with the
  reason stated. Private buckets get storage policies at table-RLS
  discipline and are served via short-expiry signed URLs.
- Rules RLS cannot express (cross-table business logic, third-party
  calls) go into an edge function, never into client code holding an
  elevated key.
- Sign-out and password change revoke the session server-side, not only
  clear client state.
```

## Fragment: review lens

```text
Review this Supabase project as an RLS auditor, in this order:
1. Enumerate every table. RLS off on any table holding user data is
   CRITICAL — report it before continuing.
2. For each table, list policies by operation. Flag missing policies for
   operations the app performs, and any USING/WITH CHECK that is true,
   constant, or has no auth.uid() tie.
3. Confirm INSERT/UPDATE policies carry WITH CHECK — a USING-only policy
   lets a user write rows they cannot read back.
4. Grep every client-shipped surface for the service_role key and for
   service-key-shaped values in client-exposed env. Any hit is CRITICAL.
5. For each server-side service_role usage, confirm caller identity and
   authorization are verified first.
6. List storage buckets with their public/private setting; flag any
   mismatch against the sensitivity of what they hold.
7. Confirm policies were tested by real queries as two distinct
   authenticated users. Inspected-only means unverified.
8. Confirm logout and password change revoke access server-side.
Report against review-checklist.md severities; ★ items block anything
past a local, never-deployed prototype.
```

## Fragment: new-table RLS authoring pass

```text
For each new or modified table, emit in one migration:
- CREATE TABLE, then ALTER TABLE <t> ENABLE ROW LEVEL SECURITY.
- The owning column the policy scopes on (typically user_id referencing
  auth.users), declared NOT NULL with a foreign key.
- One CREATE POLICY per operation the application performs, named for
  what it permits, each predicate written against auth.uid().
- For rows scoped through a parent table, express the predicate as an
  EXISTS against the parent rather than duplicating the owner column —
  unless the join makes the policy unreadable, in which case move the
  rule into an edge function.
State explicitly which operations are intentionally denied by having no
policy. Never emit a permissive placeholder policy to clear an error.
```

## Fragment: adversarial policy test

```text
Prove the policies, do not read them. Generate a test that:
- Creates two distinct authenticated users, A and B, each owning rows.
- As A: asserts a select returns only A's rows and never B's.
- As A: asserts update and delete against B's row ids affect 0 rows.
- As A: asserts an insert forging B's owner column is rejected by
  WITH CHECK.
- As an anonymous client: asserts every operation is denied.
- For private buckets: asserts an unsigned object URL fails and that a
  signed URL stops working after its expiry.
Run it through the client SDK against the real database — the same path
a user has. A policy with no failing-case assertion is untested.
```

## One-liner (for tight token budgets)

```text
Supabase floor: RLS enabled in the table's creation migration; explicit
per-operation policies scoped to auth.uid() with WITH CHECK on writes,
never USING (true); service_role server-side only and gated by a caller
authorization check; buckets deliberately public or private with signed
URLs for private; RLS-inexpressible logic in edge functions; policies
proven by cross-user tests; sessions revoked server-side on logout.
```
