# Mental Models — Material Design Pack

## The token pyramid

Reference tokens (`palette.blue40`) → system tokens (`color.primary`, `color.surface-container-high`) → component tokens (`button.filled.container-color`). Decisions flow down; themes swap the middle layer; components never reach past their layer. Dark mode, dynamic color, and brand theming are all middle-layer swaps. Any hardcoded hex in a component is a hole in the pyramid.

## State layers

Interaction states are *overlays* at standard opacities (hover 8%, focus 10%, pressed 10-12%) tinted with the content color — one mechanism generating consistent states for every component on every surface color. Beats per-component hover-color decisions by construction.

## Surface + elevation as information

Surfaces sit at levels; level = importance/recency of the layer (dialogs above sheets above content). M3 expresses level via tonal color shift (+ shadow where needed). Reading a Material screen = reading a depth map. Random elevations = noise in the depth channel.

## Canonical layouts

Larger canvases don't get "stretched phone UI"; they get canonical patterns: **list-detail** (master list + selected item), **feed** (responsive card grid), **supporting pane** (primary + contextual side surface). Navigation morphs bar→rail→drawer alongside. Same model as [HIG adaptivity](../apple-hig/mental-models.md): rules, not screenshots.

## Component anatomy sheets

Every Material component is specified as anatomy (container, label, icon, state layer), measurements, states, and motion. Custom components earn citizenship by writing the same sheet — if you can't specify its anatomy and states, it isn't designed yet.

## Dynamic color

Android derives user palettes from wallpaper; apps opting in re-key their system tokens to it. Consequence: never assume your primary is *the* blue — designs must survive hue swaps, which token discipline (MD5/MD6) guarantees and hardcoding breaks.
