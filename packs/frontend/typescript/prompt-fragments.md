# Prompt Fragments — TypeScript Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply TypeScript practice (AKOS L2):
- `strict: true` in tsconfig from project start. On an inherited loose
  codebase, migrate file-by-file — never attempt a big-bang flip.
- No `any`. Use `unknown` plus narrowing. Where `any` is genuinely
  unavoidable, it carries an inline comment stating why.
- External data — HTTP responses, request bodies, query params, form
  values, env vars, file contents, third-party SDK callbacks — is parsed
  through a schema validator at the boundary, with the type inferred
  from the schema. `JSON.parse(x) as T` is a lie, not a type.
- Parse once at the edge, then trust the type downstream; do not
  re-check the same shape at every call site.
- Mutually exclusive state is a discriminated union (`{status:'loading'}
  | {status:'error',error} | {status:'success',data}`), never optional
  booleans permitting impossible combinations.
- `as` assertions are rare and each carries a stated reason; prefer type
  guards and narrowing. Never `@ts-ignore`; use `@ts-expect-error` + why.
- No habitual non-null `!`; handle the null the type system flagged.
- Signatures express real constraints — branded IDs, literal unions,
  non-empty arrays — not the loosest type that compiles. Brand a
  primitive when misuse is a real risk (entity IDs, currency).
- Exported signatures leak no `any` or bare `unknown`.
```

## Fragment: review lens

```text
Review this TypeScript as a type-safety reviewer:
1. Config — is `strict` on? Which strict flags are individually off,
   and what checking does each one disable?
2. Grep `any` — each one justified inline? Trace its blast radius
   through the call chain it silently untypes.
3. Grep `as`, `!`, `@ts-ignore`, `@ts-expect-error` — each is a place
   the compiler was overruled. Is the override sound and still true?
4. Boundary audit — list every point untrusted data enters the program.
   Is each schema-parsed, or cast?
5. State shapes — find types whose optional fields or booleans are
   mutually exclusive in practice; propose the discriminated union.
6. Exhaustiveness — do switches over unions have a `never` default so a
   new variant becomes a compile error?
7. Public surface — do exported signatures leak `any`/`unknown`?
8. Primitive obsession — parameters typed `string`/`number` carrying a
   real invariant (IDs, emails, currency) with plausible misuse.
Report by severity per review-checklist.md, with the concrete
replacement type or schema, not a general recommendation.
```

## Fragment: boundary hardening pass

```text
Harden the untrusted boundaries in this module:
- Enumerate every entry point for external data: network responses,
  request bodies, query and route params, form values, `process.env`,
  localStorage, file reads, third-party SDK callbacks.
- Define a schema per entry point; infer the TypeScript type from it
  rather than declaring the shape separately.
- Parse at the edge and return a typed result. Handle parse failure
  explicitly — never swallow it, never fall back to a partial object.
- Delete the `as T` casts and defensive optional chaining the schema
  makes redundant.
```

## Fragment: state modeling pass

```text
Remodel this type so illegal states are unrepresentable:
- List the field combinations that cannot occur in practice
  (loading && error, success with no data, error with no message).
- Replace with a discriminated union keyed on a literal `status`/`kind`
  field; each variant carries only the fields valid in that state.
- Update consumers to switch on the discriminant, with a `never`
  exhaustiveness check in the default case, and delete the runtime
  guards the new shape makes dead.
```

## One-liner (for tight token budgets)

```text
TypeScript rules: strict mode on; no unjustified `any` — use `unknown`
plus narrowing; schema-parse all external data at the boundary and infer
the type from the schema, never cast; discriminated unions with
exhaustiveness checks instead of boolean flag soup; `as`, `!`, and
`@ts-ignore` rare and justified; brand high-risk primitives; no
`any`/`unknown` in exported signatures.
```
