# Coding Preferences — Pau Avila

Code-style and tooling defaults. Compose with the language packs ([typescript](../../frontend/typescript/README.md), [react](../../frontend/react/README.md), [css](../../frontend/css/README.md)).

## Style

- **Immutability by default** — new objects, never in-place mutation.
- **Many small files over few large ones** — 200–400 lines typical, 800 hard max; organize by feature/domain, not by file type.
- **KISS / DRY / YAGNI** — simplest thing that works; extract on the real second/third repetition, not speculatively.
- **Early returns over deep nesting** (>4 levels is a smell).
- **Named constants over magic numbers.**
- **Comprehensive error handling** — never silently swallow; user-friendly messages in UI, detailed context in server logs.
- **Validate at system boundaries** — schema validation (Zod-class) on all external/untrusted input.

## Naming

- `camelCase` variables/functions, `PascalCase` types/components/interfaces, `UPPER_SNAKE_CASE` constants, `use`-prefixed hooks.
- Boolean names prefixed `is`/`has`/`should`/`can`.

## Tooling defaults

- TypeScript strict mode on from project start.
- Prettier + ESLint (+ Stylelint for CSS) wired as format/lint on save where the project supports it.
- Prefer project-local tooling over remote one-off package execution in hooks.
- Incremental typecheck in hooks (`tsc --incremental` + `timeout`) to avoid process pile-up.

## Testing posture

- TDD encouraged on business logic and bug fixes; relaxed for pure UI/layout and throwaway prototypes ([tdd decision framework](../../testing/tdd/decision-framework.md)).
- Test balance follows the [pyramid](../../testing/testing-pyramid/README.md); E2E reserved for critical journeys.
