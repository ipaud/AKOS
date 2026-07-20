# Decision Framework — Material Design Pack

## Adopt Material at all?

- Android native → yes (it's the platform grammar).
- Flutter → Material widgets are the default rail; adopt + theme.
- Web app → a choice: Material-derived library (fast, coherent, template-risk) vs custom system ([Refactoring UI](../refactoring-ui/decision-framework.md) rails). Deciding factor: team design capacity. Low → Material themed hard (MD12); high → custom system may express identity better.
- iOS → no. Share tokens/brand, use HIG grammar ([R3](../../../core/conflict-resolution.md)).

## Which feedback surface?

| Situation | Surface |
|-----------|---------|
| Transient FYI, optional single action | Snackbar |
| Must-decide-now | Dialog |
| Persistent condition until resolved | Banner |
| Field-level problem | Text-field error slot |
| Actionable error | Persistent inline/banner + live region — never snackbar |

## Which navigation container?

Compact width → bottom navigation bar (3–5 destinations). Medium → rail. Expanded → drawer or rail+drawer. >5 destinations → the IA needs consolidation first ([More-tab landfill](../apple-hig/anti-patterns.md) applies equally).

## Custom component admission test

1. No Material component covers the need after honest search?
2. Anatomy sheet written (container/label/states/motion/semantics)?
3. State layers + role pairs + type roles consumed from the token system?
4. TalkBack/keyboard behavior specified and implemented?
All four or it doesn't ship. Cost estimate: 3–5× the visual build ([same rule](../wcag/decision-framework.md) as ARIA widgets).

## Theming depth

Minimum viable brand: seed color scheme + type ramp + shape family (MD12). Add: custom motion durations, component token overrides, illustration/iconography language. Stop before: breaking state layers, breaking role-pair contrast, per-component one-off overrides ([system-breaking](../refactoring-ui/decision-framework.md)).
