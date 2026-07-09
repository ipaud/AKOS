# Review Checklist — Apple HIG Pack

Applies on Apple platforms; runs with [wcag](../wcag/review-checklist.md) (substance) beside it.

## Critical

- [ ] System gestures unblocked: edge-swipe back everywhere, safe areas respected, nothing interactive under the home indicator. (AP3, AP4)
- [ ] Largest accessibility text size: no lost content/controls. (AP2)
- [ ] VoiceOver completes the primary task; all elements labeled with traits. (AP13)
- [ ] Sheets/modals can't silently destroy unsaved work. (AP6)

## High

- [ ] Correct container grammar (tabs/push/sheet/alert per relationship). (AH4)
- [ ] Touch targets ≥44pt, primaries thumb-reachable, destructive displaced. (AP1, AH6)
- [ ] Dark + light both intentional; contrast verified in both. (AP8)
- [ ] iPad: orientations + split view survive; size-class layout. (AP9)
- [ ] Permissions in context with pre-prompt rationale; denial degrades gracefully. (AP15)
- [ ] Alerts only for critical decisions. (AP7)

## Medium

- [ ] System share sheet/context menus/pickers used. (AP11)
- [ ] SF Symbols (or optically matched) icons aligned to text. (AP10)
- [ ] Semantic haptics, sparing. (AP12)
- [ ] Reduce Motion degrades animations. (AP14)
- [ ] Launch = UI skeleton; state restored. (AP16)
- [ ] Web-on-iOS: safe-area CSS, no zoom-jump inputs. (AP18)

## Low (macOS)

- [ ] Menu bar complete with standard shortcuts; windows resizable. (AP17)
