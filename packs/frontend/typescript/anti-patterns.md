# Anti-Patterns — TypeScript Pack

- **`as MyType` casting API responses** — no runtime validation, type is a lie at the boundary.
- **`any` escape hatches accumulating** — each one disables checking for everything downstream.
- **Boolean flag soup for state** — `{isLoading, isError, hasData}` allowing impossible combinations (`isLoading && isError`).
- **`// @ts-ignore` instead of fixing the type** — silences the error without addressing the underlying issue.
- **Non-null assertion (`!`) as a habit** — bypassing null checks the type system correctly flagged.
