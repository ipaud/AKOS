# Principles — Apple HIG Pack

- **AH1 — Clarity first:** legibility at every Dynamic Type size; icons precise and labeled where meaning isn't universal; functionality visually signaled.
- **AH2 — Content leads, chrome defers:** interface elements recede (translucency, minimal bars, edge-to-edge content within safe areas); the user's content is the hero.
- **AH3 — Depth communicates:** transitions show origin and destination (push slides, sheets rise, popovers point); layers encode hierarchy; motion is informational, not decorative — and respects Reduce Motion.
- **AH4 — Use the platform grammar:** tab bar for parallel top-level sections (2–5), navigation stack for hierarchy, sheet for scoped temporary tasks, alert only for critical decisions, action sheet/menu for contextual choices. Match relationship → element.
- **AH5 — System gestures are sacred:** edge-swipe back, home indicator, control/notification centers. Never hijack; custom gestures only as accelerators with visible equivalents ([Norman NR1](../don-norman/engineering-rules.md)).
- **AH6 — Touch ergonomics:** ≥44pt targets; primary actions thumb-reachable; destructive away from habitual zones; spacing prevents fat-finger slips.
- **AH7 — Adopt Dynamic Type end-to-end:** semantic text styles everywhere; layouts tested at accessibility sizes; truncation designed, not accidental.
- **AH8 — Adaptivity is mandatory:** size classes, safe areas, both orientations where sensible, dark and light appearance both intentional.
- **AH9 — Feedback through system channels:** immediate visual response; semantic haptics for meaningful moments; progress for anything slow ([NR9–NR13](../don-norman/engineering-rules.md)).
- **AH10 — Integrate, don't reinvent:** system share sheet, context menus, standard controls, SF Symbols, system colors (which auto-adapt to appearance modes and accessibility settings) before custom equivalents.
- **AH11 — Accessibility is platform-native:** VoiceOver labels/traits, Dynamic Type, sufficient contrast in both appearances, Reduce Motion/Transparency honored. WCAG substance + Apple API idiom ([wcag pack](../wcag/README.md) governs substance).
- **AH12 — Ask permission in context, once, with a reason:** trigger permission prompts at the moment of need with a pre-prompt explanation; degrade gracefully on denial.
- **AH13 — Launch fast into the last context:** restore state; never splash-screen marketing; first frame resembles the app (launch screen = skeleton of UI).
- **AH14 — macOS is not big iOS:** menus bar with full command set, keyboard shortcuts, resizable windows, pointer precision, density expectations differ. Mac apps earn Mac-ness.
