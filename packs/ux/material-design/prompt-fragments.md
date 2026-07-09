# Prompt Fragments — Material Design Pack

## Fragment: build-mode constraint block (Material targets)

```text
Apply Material Design 3 constraints (AKOS L1 on Android/Material surfaces):
- Stock components themed via tokens; customs only with full anatomy
  sheets (states, semantics, motion).
- Token pyramid: components consume system/component tokens; zero raw
  hex/dp; color via role pairs (X/on-X) with contrast holding in light,
  dark, and dynamic-color schemes.
- Emphasis ladder: one filled button per surface; ≤1 FAB (signature
  action); tonal/outlined/text for the rest.
- Full state set via state layers (hover/focus/pressed/selected/disabled)
  on everything interactive — surviving all theming.
- Type roles (display/headline/title/body/label); elevation ladder with
  tonal surfaces in dark; motion semantics (container transform /
  shared axis / fade-through) with reduced-motion fallbacks.
- 48dp targets; navigation morphs bar→rail→drawer by width; canonical
  layouts (list-detail/feed/supporting pane) on large canvases.
- Feedback: snackbar = transient+optional-action; dialog = decisions;
  banner = persistent conditions; actionable errors never snackbar-only.
- Theme is mandatory: seed color scheme + type ramp + shape family;
  baseline Material theme never ships.
```

## Fragment: Material review lens

```text
Review this Material UI:
1. Token audit — raw hex/dp in components; role-pair contrast both schemes.
2. Emphasis audit — filled-button count per surface; FAB legitimacy.
3. State audit — state layers present and surviving theme overrides.
4. Adaptive audit — width-class navigation morph; canonical layout vs
   stretched phone.
5. Feedback audit — snackbar/dialog/banner used per their contracts.
6. Template audit — is the theme distinguishable from Material baseline?
7. Chimera audit — M2/M3 idiom mixing.
Findings cite MT-rules; accessibility substance routes to the wcag pack.
```

## One-liner

```text
Material: themed stock components; token pyramid with role pairs; one
filled button + ≤1 FAB; state layers everywhere; type roles; elevation
ladder; motion with jobs; 48dp; nav morphs by width; snackbar/dialog/
banner contracts; never ship baseline theme; never Material-on-iOS.
```
