# Scoring Rubric — Apple HIG Pack (Platform Fidelity)

Feeds UX and mobile scores when the target is an Apple platform.

| Finding | Deduction |
|---------|-----------|
| System gesture blocked / safe-area violation on primary flow | −25 (CRITICAL) |
| VoiceOver cannot complete primary task | −25 (CRITICAL — also WCAG) |
| Accessibility text sizes break primary screens | −10 (HIGH) |
| Wrong container grammar on a main flow (modal-as-push etc.) | −10 (HIGH) |
| Foreign platform idiom (hamburger/FAB/toast-primary) | −10 (HIGH) |
| Permission battery at launch / context-free prompts | −10 (HIGH) |
| Unintentional dark mode, alert spam, sub-44pt targets | −4 each (MEDIUM) |
| Custom where system exists, non-semantic haptics, missing state restore | −4 each (MEDIUM) |
| Icon family mismatch, missing Reduce Motion niceties | −1 each, cap −5 (LOW) |

Modifiers: full system-integration set adopted (share sheet, context menus, Dynamic Type, both appearances, haptics): +5.

Anchors: **93** feels native, integrates deeply · **80** native grammar with integration gaps · **70** functional but visibly cross-platform generic · **<60** fights the platform (gestures blocked, grammar wrong) — BLOCKED for App Store-quality bars.
