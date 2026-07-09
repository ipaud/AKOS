# Philosophy — Apple HIG Pack

## Three commitments: clarity, deference, depth

**Clarity:** text legible at every size, icons precise, adornments subtle, functionality signaled by design. **Deference:** the UI serves content — fluid motion and crisp interface help people understand and interact without competing with what they came for. **Depth:** distinct visual layers and realistic motion convey hierarchy, impart vitality, and communicate transitions between states — depth is *informational*, telling users where things came from and where they went.

## The platform is the user's home

People live in their device's conventions: system gestures, navigation grammar (tab bars, navigation stacks, sheets), text sizes (Dynamic Type), appearance modes, and accessibility settings. An app that respects them feels native and instantly learnable ([Jakob's Law](../laws-of-ux/principles.md) at platform strength); one that fights them feels foreign regardless of quality. This is why platform guidelines get Level 1 authority *on their platform*: the convention isn't just a good idea — it's the environment.

## Integration is a feature

The HIG worldview treats system integration — Dynamic Type, dark mode, VoiceOver, haptics, safe areas, Handoff, widgets — not as checkboxes but as the substance of feeling native. Every system service adopted is UX the app gets for free and consistency the user keeps.

## Adaptivity over pixel perfection

Devices, orientations, split views, text sizes, and displays vary; layouts must be *rules*, not pictures. Design in terms of layout guides, safe areas, and size classes. A screen that breaks when text grows two steps was never finished.

## Where deference to Apple stops

HIG is normative on idiom; WCAG remains normative on accessibility substance ([R12](../../../core/conflict-resolution.md)); your product's identity (Level 0) still owns its personality *within* the platform grammar. Cross-platform apps: keep the product's soul consistent, adapt the platform grammar per OS — never ship Android idioms on iOS (or vice versa) to save effort.
