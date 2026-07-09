# Examples — Material Design Pack

Invented cases.

## Button emphasis ladder (MD2/MT6)

Checkout screen:
- `Pay €48.20` → filled (the one).
- `Apply coupon` → outlined.
- `Back to cart` → text.
Bad version: all three filled in brand color — emphasis flatlined.

## Token pyramid in practice (MT2/MT3)

Bad: `containerColor = Color(0xFF6750A4)`.
Good: `containerColor = MaterialTheme.colorScheme.primary` — dark theme and dynamic color now free; contrast of `onPrimary` guaranteed by the scheme.

## Feedback surface choice

- File deleted → snackbar "Note deleted" + Undo (transient, reversible).
- Sync failing since yesterday → banner "Couldn't sync — check connection" persisting until resolved.
- Payment failed → inline persistent error + live-region announcement; **not** a snackbar.

## Navigation morph (MT9)

Email app: phone = bottom bar (Inbox/Search/Compose-FAB) → tablet = rail + list-detail (message list left, thread right) → desktop = rail + list-detail + supporting pane (thread details). One IA, three canonical layouts.

## Theming to escape the template (MT14)

Seed `#0E7C66` (brand green) → generated tonal palettes; type ramp swaps display/headline to the brand serif, keeps body on a workhorse sans; shape family medium-rounded (12dp mid components). Result: unmistakably branded, still 100% stock components underneath.

## State layer survival (MT4)

Custom card override before: `background: brandGradient` painted over everything — hover/focus vanish.
After: gradient on the container layer, state layer preserved above it (`hover: onSurface @ 8%`), focus ring from the theme. Brand + states coexist.
