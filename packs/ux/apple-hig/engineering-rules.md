# Engineering Rules — Apple HIG Pack

Scope: Apple platforms (native or native-feel web/RN/Flutter).

- AHE1. Touch targets ≥44×44pt; adjacent targets separated. (AH6)
- AHE2. Text uses semantic Dynamic Type styles (or CSS equivalents scaling with user settings); layouts verified at the largest accessibility size. (AH7)
- AHE3. All content and controls respect safe areas (notch/island, home indicator, sensor housings); nothing interactive under system-gesture zones. (AH5)
- AHE4. Edge-swipe back works on every pushed view; back is never repurposed. (AH5)
- AHE5. Tab bars: 2–5 items, icon+label, persistent per-tab navigation stacks; selected state obvious. (AH4)
- AHE6. Sheets have explicit resolution (Done/Cancel or clear dismissal); unsaved-work sheets confirm before discard. (AH4, [NR17](../don-norman/engineering-rules.md))
- AHE7. Alerts reserved for critical decisions: ≤2–3 actions, destructive styled destructive, cancel present; never for confirmations a toast/undo covers. (AH4)
- AHE8. Dark and light appearance both designed; colors from system/semantic palettes or dual-defined tokens; contrast verified in both. (AH8, AH11)
- AHE9. Both orientations and split-screen/multitasking handled on iPad; size-class-driven layout, no device-name branching. (AH8)
- AHE10. Icons from SF Symbols (or optically matched custom set); weights/scales aligned to adjacent text. (AH10)
- AHE11. System share sheet, context menus, and standard pickers (date, photo, document) used over custom equivalents. (AH10)
- AHE12. Semantic haptics on meaningful events only (success/warning/selection); silent for routine taps. (AH9)
- AHE13. VoiceOver: every element labeled with traits; custom controls implement accessibility actions; decorative images hidden. (AH11)
- AHE14. Reduce Motion honored: parallax/spring effects degrade to fades. (AH3, AH11)
- AHE15. Permission requests deferred to the point of need, preceded by an in-app explanation; denial paths functional. (AH12)
- AHE16. Launch screen mirrors the first real UI; app restores last state; cold start to interactive fast enough that no marketing splash is "needed". (AH13)
- AHE17. macOS: complete menu bar with shortcuts for all primary actions; standard shortcuts (⌘S/⌘Z/⌘W/⌘,) never remapped; windows resizable with sensible min sizes. (AH14)
- AHE18. Web-on-iOS: viewport-fit + safe-area-inset CSS; no 300ms-delay patterns; inputs sized to prevent zoom-jump; momentum scrolling preserved.
