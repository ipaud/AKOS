# Mental Models — CSS Pack

- **Flexbox = one axis, Grid = two axes.** Choosing the wrong one produces workarounds; choosing right produces near-zero-hack layouts.
- **Cascade and specificity as a hierarchy to respect, not fight.** Fighting specificity with `!important` is a design-token gap in disguise.
- **Container queries vs. media queries:** media queries respond to the viewport; container queries respond to the component's own available space — use container queries for reusable components, media queries for page-level layout shifts.
- **Custom properties as the token layer:** CSS variables are the mechanical implementation of the [design-token pyramid](../../ux/material-design/mental-models.md) — reference once, theme by redefining at a scope.
