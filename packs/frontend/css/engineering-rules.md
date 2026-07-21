# Engineering Rules — CSS Pack

- CSE1. Spacing, color, type, radius, and shadow values reference custom-property tokens, not hardcoded literals.
- CSE2. Base styles target mobile viewport; `min-width` media queries layer up progressively.
- CSE3. Animations/transitions apply only to `transform`/`opacity`.
- CSE4. No `!important` outside of a documented, rare escape-hatch case (e.g. utility override layer).
- CSE5. Selector nesting depth ≤3; specificity kept flat and predictable.
- CSE6. Reusable components needing size-aware layout use container queries, not viewport media queries.
- CSE7. Logical properties used where writing-mode/RTL support is a requirement.
