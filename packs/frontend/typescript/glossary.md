# Glossary — TypeScript Pack

- **Strict mode** — the tsconfig flag bundle enabling full type-safety checks (null checks, implicit any bans, etc.).
- **Discriminated union** — a union type distinguished by a common literal "tag" field, enabling exhaustive narrowing.
- **Type guard** — a function narrowing a type via a runtime check (`x is Foo`).
- **Branded type** — a primitive type tagged with a phantom property to prevent accidental misuse.
- **Structural typing** — type compatibility determined by shape, not declared inheritance.
- **Parse, don't validate** — transforming untrusted input into a trusted typed value once, at the boundary.
