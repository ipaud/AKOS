# Engineering Rules — Design Systems Pack

- DG1. Design tokens defined in a three-layer structure (reference/system/component); feature code references system/component tokens only.
- DG2. Every published component has usage documentation, a prop reference, and documented accessibility behavior (keyboard, focus, screen-reader).
- DG3. Base interactive components (button, input, select) implement full state sets (hover/focus/active/disabled) and accessibility semantics once, centrally.
- DG4. Breaking API changes ship with a deprecation period (old prop/behavior supported alongside new) before removal.
- DG5. Changes to shared tokens/components go through review by a named owner/team, not merged unreviewed.
