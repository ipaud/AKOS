# Philosophy — Material Design Pack

## A physics, not a style

Material's founding idea: give digital surfaces a consistent physics — surfaces at elevations, casting shadows, responding to touch with ripples, moving with weight and easing. Users get a spatial model for free: what's above what, what moved where, what's touchable. The aesthetics evolved (flat → M3's tonal surfaces); the physics-as-comprehension idea is the durable core ([Norman's conceptual model](../don-norman/mental-models.md), systematized).

## Components as the contract

Material ships a complete component vocabulary — buttons (5 emphasis levels), FAB, chips, cards, sheets, dialogs, navigation bar/rail/drawer, text fields, menus — each with prescribed anatomy, states, motion, and accessibility. Adopting the vocabulary buys coherence and a11y; the design work moves up a level: *which* component, *what* content, *how* themed. Fighting the vocabulary (custom one-offs beside stock components) buys inconsistency at premium prices.

## Tokens all the way down

M3 formalizes design decisions as a token pyramid: reference tokens (raw palette) → system tokens (semantic roles: `primary`, `on-primary`, `surface-container`) → component tokens (this button's fill). Theming = swapping token values; dark mode, dynamic color (user-wallpaper-derived palettes), and brand theming all ride the same rails. This is the industry's reference implementation of [Refactoring UI's systems-first doctrine](../refactoring-ui/philosophy.md).

## Motion is meaning

Material motion has jobs: continuity (shared-element transitions show identity), hierarchy (containers transform, contents follow), feedback (ripples locate touch). Duration/easing tokens keep it physical. Motion without a job is decoration — and must bow to Reduce Motion ([WCAG WC22](../wcag/engineering-rules.md)).

## Adaptive by canvas

Material targets phones, tablets, foldables, desktops from one system: navigation morphs (bar → rail → drawer), layouts use canonical patterns (list-detail, feed, supporting pane), density adapts to pointer precision. Like [HIG's size classes](../apple-hig/mental-models.md): rules, not pictures.

## Where Material stops

Material is a complete *system*, which tempts teams into unmodified default-theme shipping — the "template look" ([design-quality anti-pattern](../../personal/pau-avila/design-language.md)). The system expects theming: color, type, shape are explicitly yours. And off-Android, Material is one choice among many — never impose Material grammar on iOS ([R3](../../../core/conflict-resolution.md), both directions).
