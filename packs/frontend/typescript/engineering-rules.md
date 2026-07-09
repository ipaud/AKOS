# Engineering Rules — TypeScript Pack

- TE1. `tsconfig.json` has `strict: true` (or the individual strict flags it bundles).
- TE2. No `any` in new code without an inline comment justifying it; CI lint flags bare `any`.
- TE3. External/untrusted data is parsed through a schema validator before being typed and used.
- TE4. Discriminated unions used for state with mutually exclusive shapes (loading/error/success patterns).
- TE5. `as` type assertions are grep-auditable and each has a clear reason (rare, e.g. after a runtime check TypeScript can't narrow).
- TE6. Public function/API signatures avoid `any`/`unknown` in their exported surface; internal narrowing happens before the boundary.
