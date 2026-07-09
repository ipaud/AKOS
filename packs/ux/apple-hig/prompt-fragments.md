# Prompt Fragments — Apple HIG Pack

## Fragment: build-mode constraint block (Apple targets)

```text
Apply Apple HIG constraints (AKOS L1 on Apple platforms):
- Grammar: tab bar (2-5, parallel worlds) / push (hierarchy, edge-swipe
  back sacred) / sheet (scoped task, explicit Done-Cancel) / alert
  (critical only). Match container to content relationship.
- Ergonomics: ≥44pt targets; primaries in thumb reach; destructive
  displaced; safe areas respected; nothing under system gesture zones.
- Type: semantic Dynamic Type styles; layouts survive largest
  accessibility size; truncation designed.
- Appearance: dark + light both intentional via semantic/system colors;
  contrast verified in both; Reduce Motion degrades animation to fades.
- Integration: SF Symbols, system share sheet, context menus, standard
  pickers, semantic haptics (sparingly). VoiceOver labels + traits on
  everything.
- Permissions: in context, once, pre-explained; denial paths work.
- Launch: UI-skeleton launch screen, state restoration, no splash marketing.
- Web-on-iOS: safe-area-inset CSS, 16px+ inputs (no zoom-jump), momentum
  scrolling.
```

## Fragment: platform-idiom review lens

```text
Review this Apple-platform UI for platform-grammar fidelity:
1. Container audit — is each screen's container (tab/push/sheet/alert)
   the one its content relationship prescribes?
2. Gesture audit — edge-swipe back everywhere? System zones unblocked?
   Custom gestures duplicated by visible controls?
3. Stress: largest Dynamic Type, dark mode, iPad split view, Reduce Motion.
4. Foreign-idiom scan — hamburgers, FABs, toasts-as-primary-feedback,
   Material patterns: flag each with the native replacement.
5. Integration scan — custom controls where system ones exist; missing
   share sheet/context menus; permission timing.
Findings cite AP-rules; WCAG substance findings route to the wcag pack.
```

## One-liner

```text
HIG: platform grammar (tabs/push/sheet/alert) by relationship; 44pt +
thumb zones + safe areas; Dynamic Type end-to-end; both appearances;
system gestures sacred; integrate (SF Symbols, share sheet, haptics,
VoiceOver); permissions in context; no splash marketing.
```
