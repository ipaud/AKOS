# Decision Framework — Apple HIG Pack

## Container choice (the core HIG decision)

Ask about the content relationship:
- Peers users switch among daily → **tab bar**.
- Parent→detail → **push** on the stack.
- Interrupting scoped task → **sheet** (default) / **full-screen cover** (immersive only).
- Momentary options on a thing → **context menu / action sheet**.
- Critical either/or with consequences → **alert**.
Never choose by visual preference; the container prescribes gestures, dismissal, and user expectations.

## Custom control vs system control

1. System control exists → use it (free: accessibility, Dynamic Type, appearance modes, future OS updates).
2. Need brand styling → style the system control within its API.
3. Interaction genuinely absent from the platform → custom, budgeting: VoiceOver actions, Dynamic Type, both appearances, Reduce Motion, haptic semantics. Same 3–5× rule as [WCAG custom widgets](../wcag/decision-framework.md).

## Following HIG vs product identity (L0)

Identity lives in: color, type personality (within Dynamic Type), illustration, copy tone, micro-animation flavor, app icon.
Grammar stays platform: navigation containers, gestures, control behaviors, permission flows.
Conflict → grammar wins ([R3](../../../core/conflict-resolution.md)); identity re-expresses itself inside it.

## iOS-first web app: how native to feel?

- Traffic mostly iOS Safari + installable → adopt AP18 fully, bottom-oriented primary actions, sheet-style modals, iOS-calibrated tap targets.
- Mixed traffic → platform-neutral web idioms ([Krug](../steve-krug/README.md) + [Material](../material-design/README.md)/HIG blend), but never fake one platform's chrome on another's device.

## When HIG and WCAG diverge

Substance (contrast, target minimums where stricter, focus behavior) → WCAG. Idiom (which control, which gesture, which transition) → HIG. Design satisfying both exists nearly always ([R12](../../../core/conflict-resolution.md)).
