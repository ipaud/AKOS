# Engineering Rules — Testing Pyramid Pack

- TY1. Business logic and utility functions have unit test coverage as a default expectation for new code.
- TY2. API endpoints/service boundaries have integration tests verifying the actual contract (not mocked at the boundary being tested).
- TY3. E2E tests are limited to critical user journeys; new E2E tests require justification for why unit/integration coverage isn't sufficient.
- TY4. Flaky tests are tracked and fixed within a bounded time (e.g. one sprint) or removed/quarantined, not left indefinitely intermittent.
- TY5. CI reports test counts/runtime by layer, making pyramid-shape drift visible over time.
