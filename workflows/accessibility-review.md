---
schema_version: 1
id: accessibility-review
description: "Focused WCAG 2.2 AA pass — the safety-floor accessibility check."
agents: [accessibility-reviewer]
packs: [ux/wcag]
profiles: [Prototype, Production, Enterprise]
status: stable
maintainer: core
---

# Workflow: Accessibility Review

Focused WCAG 2.2 AA pass — the safety-floor accessibility check.

## Agent

[accessibility-reviewer](../agents/accessibility-reviewer.md), loading the [WCAG pack](../packs/ux/wcag/README.md).

## The three walks

1. **Keyboard walk** — unplug the mouse, complete the primary task. Log unreachable controls, invisible focus, traps, illogical order.
2. **Tree walk** — read the accessibility tree. Log nameless/roleless interactives, placeholder-only labels, stale ARIA states, missing landmarks.
3. **Stress walk** — 200% zoom, 320px reflow, text-spacing overrides, grayscale (color-independence), reduced motion.

Automated scan (axe/Lighthouse) is the entry ticket, not the audit.

## Profile adjustments

- **Prototype:** floor rules only (keyboard reachability, names, labels, contrast, no traps) — but these are never waived.
- **Production:** full WCAG 2.2 AA via all three walks.
- **Enterprise:** AA + documented conformance (VPAT-style).

## Exit criteria

No open floor-level CRITICAL (caps score at 59 otherwise). Scanner-clean is necessary but not sufficient — the three walks must be performed (else score caps at 79). Findings cite SC numbers.
