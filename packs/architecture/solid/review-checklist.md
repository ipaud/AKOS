# Review Checklist — SOLID Pack

## High

- [ ] No class edited by unrelated stakeholders for unrelated reasons without cause to split. (SD1)
- [ ] Adding a variant to existing multi-case behavior doesn't require editing tested existing cases. (SD2)
- [ ] No subclass overrides throw/no-op to narrow a contract. (SD3)
- [ ] Business logic depends on interfaces, not concrete infra classes, wherever a second implementation exists or tests need isolation. (SD5)

## Medium

- [ ] Interfaces sized to actual client usage — no stub implementations. (SD4)
- [ ] No interface/strategy pattern introduced for a single stable case. (SD6)

## Low

- [ ] Class responsibilities describable in one sentence without "and".
- [ ] SOLID findings are proportionate — not blocking trivial utilities for lack of abstraction.
