# Review Checklist — Design Patterns Pack

## High

- [ ] Every Strategy/Factory/Adapter pattern in the diff has ≥2 real implementations, not a hypothetical future one. (DP-E1)
- [ ] No new global-state Singleton introduced; shared instances are dependency-injected. (DP-E2)
- [ ] Pattern-named classes actually implement that pattern's structure. (DP-E5)

## Medium

- [ ] Language-native alternatives (closures, first-class functions) considered before a class-based pattern implementation. (DP-E3)
- [ ] Decorator/Composite used only where dynamic composition or tree-uniformity is a real requirement. (DP-E4)
- [ ] No layered creational-pattern stacking (Factory-of-Factories) without a matching real complexity.

## Low

- [ ] Pattern choices documented with the plain-language trigger they address, in comments or PR description.
