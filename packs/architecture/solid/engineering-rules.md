# Engineering Rules — SOLID Pack

- SD1. A class/module's public methods serve one describable responsibility; if two unrelated stakeholders would request changes to it for unrelated reasons, split it.
- SD2. Adding a new variant of existing behavior (new payment method, new export format) does not require editing the tested logic for existing variants, once ≥2 variants exist.
- SD3. No subclass overrides a base method to throw, no-op, or silently narrow its contract; such cases are refactored to composition or a narrower interface.
- SD4. Interfaces are sized to actual client usage — no implementing class contains stub/no-op method bodies to satisfy an unused interface method.
- SD5. High-level modules depend on interfaces they or an adjacent core module define, not on concrete low-level classes, once a second implementation exists or a test needs isolation.
- SD6. No interface, strategy pattern, or abstraction is introduced for a single, stable case with no near-term second variant planned (over-engineering guard, paired with SD1–SD5's under-engineering guards).
