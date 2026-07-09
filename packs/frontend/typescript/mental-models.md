# Mental Models — TypeScript Pack

- **Make illegal states unrepresentable:** model data so invalid combinations can't be constructed (discriminated unions over multiple optional booleans).
- **Parse, don't validate:** transform untrusted input (API responses, form data) into a typed, validated shape once at the boundary, then trust the type everywhere downstream.
- **The `any` blast radius:** one `any` in a call chain silently disables type checking for everything it touches.
- **Structural typing:** TypeScript types are compatible by shape, not declared inheritance — useful for flexible interfaces, occasionally surprising for accidental compatibility.
