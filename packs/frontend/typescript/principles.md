# Principles — TypeScript Pack

- **TS1** — `strict: true` in tsconfig from project start; retrofitted incrementally if inherited loose.
- **TS2** — `any` is never used without an explicit, reviewed justification comment; prefer `unknown` + narrowing.
- **TS3** — State with mutually exclusive variants is modeled as a discriminated union, not multiple optional fields.
- **TS4** — External data (API responses, form input, env vars) is validated against a schema at the boundary (Zod/io-ts/similar), not cast.
- **TS5** — Function signatures express real constraints (non-empty arrays, branded IDs) rather than the loosest type that compiles.
- **TS6** — Type assertions (`as`) are rare and justified; prefer type guards/narrowing.
