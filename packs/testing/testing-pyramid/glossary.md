# Glossary — Testing Pyramid Pack

- **Unit test** — tests a single function/component in isolation, no real I/O.
- **Integration test** — tests real cooperation between two or more components/systems.
- **E2E (end-to-end) test** — tests a complete user journey through the real (or near-real) system.
- **Ice cream cone (anti-pattern)** — an inverted pyramid: mostly E2E, few unit tests.
- **Flaky test** — a test that passes/fails inconsistently without code changes.
- **Test quarantine** — temporarily excluding a known-flaky test from blocking CI while it's fixed.
