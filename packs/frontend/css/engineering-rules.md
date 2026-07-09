# Engineering Rules — CSS Pack

- CE1. Spacing, color, type, radius, and shadow values reference custom-property tokens, not hardcoded literals.
- CE2. Base styles target mobile viewport; `min-width` media queries layer up progressively.
- CE3. Animations/transitions apply only to `transform`/`opacity`.
- CE4. No `!important` outside of a documented, rare escape-hatch case (e.g. utility override layer).
- CE5. Selector nesting depth ≤3; specificity kept flat and predictable.
- CE6. Reusable components needing size-aware layout use container queries, not viewport media queries.
- CE7. Logical properties used where writing-mode/RTL support is a requirement.
