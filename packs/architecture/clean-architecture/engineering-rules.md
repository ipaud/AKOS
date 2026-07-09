# Engineering Rules — Clean Architecture Pack

- CR1. No file in the domain/use-case layer imports a framework, ORM, or HTTP library package.
- CR2. Every external dependency the core needs (persistence, notification, third-party API) is expressed as an interface defined in the core, implemented in an outer layer.
- CR3. Exactly one composition root per deployable process wires concrete implementations to interfaces.
- CR4. Business-rule tests run without a database connection, network call, or running framework.
- CR5. Data transfer objects crossing ring boundaries are plain structures, not ORM entities or framework request/response objects.
- CR6. Top-level module/folder names reflect business capabilities, not technical layers alone (may coexist: `orders/{domain,api,persistence}`).
- CR7. Controllers/handlers are humble: they parse input, call a use case, format output — no business rules inline.
- CR8. New architectural boundaries are added with a written reason (volatility, swappability, or testability need) — not by default template.
