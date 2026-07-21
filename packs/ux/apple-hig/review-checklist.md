# Review Checklist — Apple HIG Pack

Applies on Apple platforms; runs with [wcag](../wcag/review-checklist.md) (substance) beside it.

## Critical

- [ ] System gestures unblocked: edge-swipe back everywhere, safe areas respected, nothing interactive under the home indicator. (AHE3, AHE4)
- [ ] Largest accessibility text size: no lost content/controls. (AHE2)
- [ ] VoiceOver completes the primary task; all elements labeled with traits. (AHE13)
- [ ] Sheets/modals can't silently destroy unsaved work. (AHE6)

## High

- [ ] Correct container grammar (tabs/push/sheet/alert per relationship). (AH4)
- [ ] Touch targets ≥44pt, primaries thumb-reachable, destructive displaced. (AHE1, AH6)
- [ ] Dark + light both intentional; contrast verified in both. (AHE8)
- [ ] iPad: orientations + split view survive; size-class layout. (AHE9)
- [ ] Permissions in context with pre-prompt rationale; denial degrades gracefully. (AHE15)
- [ ] Alerts only for critical decisions. (AHE7)

## Medium

- [ ] System share sheet/context menus/pickers used. (AHE11)
- [ ] SF Symbols (or optically matched) icons aligned to text. (AHE10)
- [ ] Semantic haptics, sparing. (AHE12)
- [ ] Reduce Motion degrades animations. (AHE14)
- [ ] Launch = UI skeleton; state restored. (AHE16)
- [ ] Web-on-iOS: safe-area CSS, no zoom-jump inputs. (AHE18)

## Low (macOS)

- [ ] Menu bar complete with standard shortcuts; windows resizable. (AHE17)
