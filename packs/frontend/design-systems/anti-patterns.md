# Anti-Patterns — Design Systems Pack

- **Token pyramid bypass** — feature code with raw hex/px values because "the token didn't exist yet," instead of adding it properly.
- **Undocumented components** — a component exists in the codebase but no docs, so every consumer reads the source or asks in chat.
- **Prop accretion** — a Button component with 20 props added reactively over two years, each solving one feature's need, none designed together.
- **Instant breaking changes** — a shared component's API changed in one PR with no deprecation window, breaking every consumer simultaneously.
- **Unowned system** — no one reviews additions; the "design system" package becomes a junk drawer of inconsistent one-offs.
