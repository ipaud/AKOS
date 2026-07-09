# Heuristics — GraphQL Pack

- A resolver calling `db.findOne()` inside a `.map()` over parent items → N+1 candidate, batch it.
- No query depth limit configured → any client can send an intentionally deeply nested query; add one before production traffic.
- A schema type mirroring a database table's exact columns including internal fields → check if it should be reshaped for client needs and internal-field-hidden.
- Mutation returning just `{success: true}` instead of the updated object → clients will need a follow-up query; return the object.
