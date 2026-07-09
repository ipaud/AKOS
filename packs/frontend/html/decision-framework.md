# Decision Framework — HTML Pack

Native element exists for the interaction → use it. Native element exists but needs custom visuals → use it, restyle within CSS's reach. No native element covers the pattern (rich combobox, custom slider) → adopt a maintained accessible component library implementing the full [ARIA APG pattern](../../ux/wcag/decision-framework.md) rather than hand-rolling. Hand-roll only as a last resort, budgeting the full semantics/keyboard/states cost.
