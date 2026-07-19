# Prompt Fragments — Design Systems Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply design-system practice (AKOS L2):
- Tokens are three-layered: reference (raw palette and scale values) →
  system (semantic roles, `color.text.primary`) → component
  (`button.primary.background`). Feature code consumes system or
  component tokens only — never the reference layer, never a literal.
- A missing token gets added to the system properly, never bypassed
  with a raw value "just this once".
- Name tokens by role, not appearance: `color-action-primary`, not
  `color-blue-600`.
- Base interactive components implement the full state set once —
  default, hover, focus-visible, active, disabled, loading, error —
  plus role, accessible name, and keyboard behavior, so consumers
  inherit correctness for free.
- Every published component ships usage docs, a prop reference, and
  documented accessibility behavior. Undocumented means unpublished.
- Design the API for the anticipated range of cases up front. High
  visual or structural variance → composition (children, slots,
  compound components). Small closed variant set → props.
- A prop list past ~8-10 is an API smell: restructure toward
  composition rather than appending another flag.
- Breaking changes ship with a deprecation window — old and new coexist,
  the old path warns, removal is a later announced release.
- Shared token and component changes are reviewed by the named owner.
```

## Fragment: review lens

```text
Review this component or system contribution:
1. Token compliance — grep the feature code for raw hex, rgb, px, and
   font stacks. Per hit: which token should it be, or which is missing?
2. Layer discipline — does anything reference the reference layer
   directly, or hardcode what a component token should resolve?
3. State coverage — does the base component handle default, hover,
   focus-visible, active, disabled, loading, and error?
4. Accessibility inheritance — are role, accessible name, keyboard
   interaction, and focus management central, or left to each consumer?
5. API shape — prop count, boolean flags, and whether the variance this
   component absorbs is better expressed by composition.
6. Duplication — does this restate an existing system component? Should
   it be a variant of that component rather than a new one?
7. Docs — usage, props, and a11y notes present at publish time?
8. Change safety — breaking API change, and is there a deprecation path?
Report by severity per review-checklist.md, naming the token, prop, or
component and the specific change required.
```

## Fragment: promotion decision

```text
Decide whether this component belongs in the shared system:
- Used in ≥2 places, or reusable by clear design intent → promote, with
  tokens, the full state set, accessibility, and docs before it ships.
- Used once, reusability uncertain → keep local, revisit on the second.
- Resembles an existing system component → extend that component with a
  deliberate variant instead of adding a near-duplicate.
- Consumers already copy-and-modify an existing component → the API
  does not cover their case. Fix the API; do not accept the fork.
Output: promote / keep local / extend existing, plus the work required.
```

## Fragment: deprecation plan

```text
Plan the deprecation for this breaking change:
- Ship the new API alongside the old in the same release.
- Keep the old path working, emitting a one-time dev-mode warning that
  names its replacement.
- Publish a migration note: old → new mapping, plus a codemod or
  find/replace pattern wherever the change is mechanical.
- Set and announce the removal release; remove only after migration.
Never change a shared component's API and all its consumers in one PR.
```

## One-liner (for tight token budgets)

```text
Design-system rules: three token layers (reference → system →
component), feature code uses system/component tokens only, never
literals; tokens named by role; base components own the full state set
and accessibility centrally; docs (usage, props, a11y) required before a
component counts as published; composition over prop accretion;
deprecation window on breaking changes; a named owner reviews changes.
```
