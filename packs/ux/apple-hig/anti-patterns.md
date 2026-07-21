# Anti-Patterns — Apple HIG Pack

## Android-on-iOS (and web-on-iOS)

Hamburger drawers, FABs, toasts as primary feedback, system-back assumptions, Material ripples. Each imports a foreign grammar users must translate. Fix: platform grammar per AH4/AH5.

## Gesture hijacking

Custom carousels swallowing edge-swipe back; bottom elements fighting the home indicator; long-press repurposed where context menus are expected. Fix: AHE3, AHE4 — system gestures are sacred.

## The mandatory tour

Five-screen onboarding carousel before any value; permissions battery (notifications+location+tracking) on first launch. Fix: AH12/AH13 — value first, permissions in context ([Krug sign-up wall](../steve-krug/anti-patterns.md) cousin).

## Dynamic Type denial

Fixed 14px labels everywhere; accessibility sizes shatter the layout or, worse, are locked out. Fix: AHE2 — semantic styles, tested at extremes.

## Fake dark mode

Dark appearance as an unmaintained afterthought: hardcoded whites flashing, illegible grays, images unadapted. Fix: AHE8 — both appearances designed or the toggle unsupported honestly.

## Alert spam

Alerts for routine confirmations, marketing, ratings begging on launch. Trains reflex-dismissal, spending the channel needed for real emergencies ([confirmation wallpaper](../don-norman/anti-patterns.md)). Fix: AHE7.

## Sheet limbo

Sheets without Done/Cancel, dismissible only by mystery swipe, losing work on dismissal. Fix: AHE6.

## More-tab landfill

A 5th "More" tab hiding half the app. The IA needs consolidation, not a junk drawer. Fix: AH4 — collapse concepts.

## Splash-screen marketing

3-second logo animation before an app that then loads for 2 more. Fix: AHE16 — launch screen = UI skeleton; restore state.

## iOS app in a Mac window

Catalyst/RN app shipped to macOS with no menu bar items, no shortcuts, giant touch paddings, single fixed window. Fix: AHE17 — Mac apps earn Mac-ness or don't ship on Mac.
