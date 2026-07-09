# Heuristics — CSS Pack

- Reaching for `position: absolute` to center something? Try Flexbox/Grid centering first.
- Repeating a raw hex/px value a third time? Extract it to a custom property.
- Writing a media query inside a component file for that component's own internal layout? Consider a container query instead.
- About to add `!important`? First check if a token/specificity issue upstream is the real problem.
- Nesting selectors more than 2-3 levels? Flatten with a class-based approach (BEM-like or utility classes).
