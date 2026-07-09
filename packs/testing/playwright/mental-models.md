# Mental Models — Playwright Pack

- **Auto-waiting over sleep:** Playwright's locators wait for actionability (visible, enabled, stable) automatically — a fixed `sleep(ms)` is almost always a sign of fighting the framework instead of using it.
- **Role/text-based selectors as the resilient layer:** `getByRole('button', {name: 'Submit'})` survives markup refactors that would break a CSS-class selector; it also doubles as an accessibility check (elements need real roles/names to be selectable this way).
- **Test isolation via fresh context:** each test gets its own browser context (cookies, storage) by default — tests should not depend on execution order or shared mutable state.
- **Trace/video-on-failure as the debugging safety net:** capturing traces only on retry/failure keeps CI fast while still providing full debugging context when something breaks.
