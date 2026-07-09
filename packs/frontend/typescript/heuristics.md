# Heuristics — TypeScript Pack

- Grep for `any` and `as` — each is a candidate for narrowing to a real type.
- Multiple optional booleans on one type (`isLoading?`, `isError?`, `data?`) → likely should be a discriminated union (`{status:'loading'} | {status:'error',error} | {status:'success',data}`).
- Data crossing a network/file/env boundary without a schema validator → add one; don't trust `JSON.parse(...) as MyType`.
- A function accepting `string` when it really means "a UUID" or "an email" → consider a branded type if misuse is a real risk.
