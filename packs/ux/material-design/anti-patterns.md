# Anti-Patterns — Material Design Pack

## Default-theme shipping ("the template look")

Baseline purple, Roboto, stock shapes — straight to production. Reads as unfinished to users and as no-decision to reviewers. Fix: MD12/MT14 — theming is not optional.

## Pyramid bypass

Hex codes and dp values inline in components; dark theme then implemented as a second pile of hex. Fix: MT2 — tokens or it doesn't merge.

## FAB abuse

FAB as navigation, FAB opening menus, three FABs, FAB on every screen including settings. The FAB is Von Restorff spent at maximum — one signature action or none. Fix: MT6.

## Snackbar as error console

Errors that require action auto-dismissing after 4s; snackbar queues stacking. Fix: MT10 + [NG31](../nielsen-norman-group/engineering-rules.md).

## Elevation soup

Cards at random elevations, shadows tweaked per-screen, dark mode with pure shadows (invisible). Depth channel becomes noise. Fix: MT7 ladder.

## State-layer amputation

Custom-themed components losing hover/focus/pressed feedback because the override painted over the state layer. Kills both usability and a11y focus visibility. Fix: MT4/MT15 — state layers survive theming.

## Stretched-phone tablet UI

Phone layout at 1200dp: bottom bar spanning a desktop, cards at 1100dp wide, list without detail pane. Fix: MT9 canonical layouts.

## M2/M3 chimera

Half the app on old idioms (M2 top app bar, sharp FAB) and half on M3 (tonal surfaces, pill FAB) after a partial migration. Fix: version-pin and migrate wholesale per surface.

## Material-on-iOS

Ripples, FABs, Material page transitions in the iOS build "for consistency". Consistency with yourself is not consistency for the user ([Jakob's](../laws-of-ux/principles.md) is per-platform). Fix: shared brand tokens, per-platform grammar.
