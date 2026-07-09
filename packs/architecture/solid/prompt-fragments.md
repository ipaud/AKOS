# Prompt Fragments — SOLID Pack

## Fragment: build-mode constraint block

```text
Apply SOLID proportionally to real pain (AKOS L3):
- SRP: one describable responsibility per class/module; split when two
  unrelated stakeholders drive unrelated changes to the same file.
- OCP: once ≥2 variants of a behavior exist, new variants are added
  without editing existing tested cases; don't pre-build for a first case.
- LSP: subclasses never override to throw/no-op/narrow a contract; if
  they would, use composition or a narrower interface instead.
- ISP: interfaces sized to actual client needs; no stub implementations.
- DIP: business logic depends on interfaces it owns, not concrete infra
  classes, once a second implementation exists or tests need isolation.
- Do not add interfaces/strategies for single, stable cases with no
  near-term second variant — that's over-engineering, not SOLID.
```

## Fragment: review lens

```text
Review this code against SOLID, principle by principle:
SRP: does each class have one axis of change? "And" in its description?
OCP: does adding a variant require editing existing tested cases?
LSP: any override that throws/no-ops/narrows the base contract?
ISP: any interface with stub/no-op implementers?
DIP: any business logic instantiating concrete infra directly?
For each finding, also check the overuse boundary — flag ceremony
(interface-per-class, speculative strategies) as its own finding
category, not virtue.
```

## One-liner

```text
SOLID: one axis of change per class; extend without editing existing
cases (once ≥2 variants exist); subclasses never break base contracts;
interfaces sized to client need; core depends on owned abstractions, not
concrete infra. Apply to real pain, not speculatively.
```
