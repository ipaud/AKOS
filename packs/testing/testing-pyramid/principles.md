# Principles — Testing Pyramid Pack

- **TP1** — Unit tests form the bulk of the suite: pure functions, business logic, utilities, isolated component behavior — fast (milliseconds), run on every save.
- **TP2** — Integration tests cover component boundaries (API endpoint + database, service + external client) at a moderate volume — verify the seams unit tests can't.
- **TP3** — E2E tests cover only critical user journeys (signup, checkout, core task completion) — few in number, each expensive to write and maintain.
- **TP4** — Flaky tests are fixed or removed immediately, never left "usually passing" — a flaky test is worse than no test.
- **TP5** — Test layer choice matches what's being verified: business logic → unit; "do these two systems talk correctly" → integration; "can a real user complete this flow" → E2E.
- **TP6** — CI suite runtime is a budget; slow layers (E2E) run less frequently or in parallel/sharded, fast layers (unit) run on every commit.
