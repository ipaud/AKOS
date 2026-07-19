# Prompt Fragments — GraphQL Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply GraphQL practice (AKOS L2):
- Batch every relation-fetching resolver through DataLoader or an
  equivalent. No per-item database call inside a resolver that runs once
  per parent row — that is an N+1 and it scales with the client's query,
  not with your test fixture.
- Bound query cost at the server before production traffic: a maximum
  depth limit at minimum, cost/complexity weighting when depth alone
  proves insufficient. Unbounded nesting is a denial-of-service surface
  any client can reach.
- Authorize per field and per object inside the resolver that returns
  the data. A top-level authentication gate proves who is asking, never
  what they may see. Sensitive scalars (email, phone, internal ids)
  resolve to null for unauthorized viewers rather than throwing away the
  whole response.
- Model the schema on domain and client needs. Do not generate types as
  a 1:1 mirror of database tables — that leaks internal columns and welds
  the public contract to storage layout.
- Keep internal-only fields out of the public schema unless a consumer
  explicitly needs them.
- Mutations return the created, updated, or deleted object (its id at
  minimum) so clients update caches without a follow-up round trip.
  {success: true} is not a mutation payload.
- Removing a field is a two-step: mark @deprecated(reason: "...") with
  the migration path and a removal date, then remove.
- In production, use persisted queries or an operation allowlist; where
  that is not feasible, disable introspection and keep cost limiting on.
```

## Fragment: review lens

```text
Review this GraphQL API as a schema-and-resolver reviewer:
1. Resolver performance — trace each list query's resolver chain. Any
   database call per parent item? Name the field and the loader that
   should batch it.
2. Cost bounds — is a depth limit configured? A complexity limit? Compute
   the worst-case query a client could send through recursive or
   self-referential types.
3. Authorization — for every field carrying user-scoped or role-scoped
   data, is the check in the resolver returning it, or inherited from a
   top-level gate?
4. Schema shape — do types mirror database tables? Are internal-only
   columns exposed? Does the shape serve the clients that exist?
5. Mutations — does each return the affected object's data?
6. Evolution — are removed or renamed fields @deprecated with a reason
   and timeline first, or silently dropped?
7. Production posture — introspection state, persisted queries or
   allowlist, cost limiting active?
Report by severity per review-checklist.md, naming the exact resolver,
type, or field and the concrete fix.
```

## Fragment: N+1 resolver audit

```text
Audit resolvers for N+1, using evidence rather than reading:
- For each type, list the fields whose resolver performs I/O.
- Execute a representative list query and count the database queries it
  issues. Query count scaling with returned row count is the signature.
- For each hit, specify the batching key and the loader that collapses
  it (DataLoader keyed on the foreign key, batched into one IN query).
- Confirm loaders are created per request, never shared across requests
   — a process-lifetime loader caches one user's data into another's.
- Re-run and report query count before and after.
```

## Fragment: production hardening pass

```text
Before this GraphQL endpoint takes untrusted traffic, verify:
- Depth limit set, with the chosen value justified against the schema's
  deepest legitimate query.
- Complexity/cost limiting configured for list and connection fields, or
  a stated reason depth alone suffices.
- Persisted queries or an operation allowlist enabled; if not,
  introspection disabled and the tradeoff recorded.
- Field-level authorization present on every sensitive field, verified by
  a test querying as an unauthorized identity.
- Resolver errors return a safe client message; internals and stack
  traces stay in server logs.
- Batched or aliased-field request abuse bounded (limit operations per
  request and aliases per query).
```

## One-liner (for tight token budgets)

```text
GraphQL rules: batch every relation resolver with a per-request
DataLoader — no query-per-row; bound cost with depth and complexity
limits before production; authorize per field in the resolver, not at a
single top-level gate; schema models the domain, not the tables, and
hides internal fields; mutations return the affected object; deprecate
with reason before removing; persisted queries or no introspection live.
```
