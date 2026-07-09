# Heuristics — SOLID Pack

- **The "and" test (SRP):** describe the class in one sentence; if it needs "and" ("handles order validation *and* sends emails"), split it.
- **The edit-existing test (OCP):** adding a new case requires editing an existing tested `switch`/`if` chain → candidate for polymorphism, but only after the second or third case appears, not preemptively for the first.
- **The "throws NotSupported" smell (LSP):** a subclass overriding a method to throw or no-op signals the hierarchy models the wrong relationship.
- **The unused-methods test (ISP):** if a class implementing an interface stubs out half its methods, the interface is fat — split by actual client need.
- **The "new" grep (DIP):** business logic instantiating concrete infra classes directly (`new SqlClient()` inside a use case) is an inversion violation; check whether an interface already exists nearby before adding one.
- **Apply on the second occurrence, not the first.** One case doesn't need an abstraction; two similar cases are a pattern worth naming; three confirm it.
- **When principles conflict with simplicity, simplicity wins until pain is real** — this is YAGNI intersecting SOLID; both are true, sequence matters.
