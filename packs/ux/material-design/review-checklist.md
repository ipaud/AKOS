# Review Checklist — Material Design Pack

Runs with [wcag](../wcag/review-checklist.md) (substance authority) on Material surfaces.

## Critical

- [ ] TalkBack/keyboard semantics intact after theming; custom components carry full semantics. (MT15)
- [ ] Actionable errors never snackbar-only. (MT10)
- [ ] Touch targets ≥48dp. (MT1)

## High

- [ ] Tokens only — no raw hex/dp in components; dark scheme via tokens. (MT2)
- [ ] Role pairs everywhere; `on-X` contrast passes in both schemes. (MT3)
- [ ] Full state set via state layers on every interactive component. (MT4)
- [ ] One filled button per surface; ≤1 FAB, signature action only. (MT6)
- [ ] Navigation morphs by width class; large canvases use canonical layouts. (MT9)
- [ ] Production theme ≠ Material baseline (seed scheme + type ramp + shape family defined). (MT14)

## Medium

- [ ] Type roles, not ad-hoc sizes. (MT5)
- [ ] Elevation ladder consistent; dark theme uses tonal surfaces. (MT7)
- [ ] Motion semantics match transitions; reduced-motion degrades. (MT8)
- [ ] Dialogs: decision-titled, verb actions, destructive styled. (MT11)
- [ ] Text fields: persistent labels, reserved helper/error slot, non-color-only errors. (MT12)
- [ ] No M2/M3 idiom mixing.

## Low

- [ ] Density via tokens only, MT1 preserved. (MT13)
- [ ] Dynamic-color hue-rotation survivability where adopted. (MT16)
