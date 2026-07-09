# Philosophy — WCAG Pack

## Accessibility is a floor, not a feature

Accessibility isn't a persona ("the blind user") or a market segment to weigh against others. It's the property that the product *works* — for people using screen readers, keyboards, voice control, magnification, high-contrast modes, switch devices; for people with tremors, low vision, color blindness, cognitive load, broken arms, bright sunlight, or a sleeping baby in one arm. Disability in this frame is a mismatch between person and design, and it is situational, temporary, or permanent for everyone at some point. That's why AKOS makes it constitutionally non-negotiable: a feature that some users cannot operate is not done.

## Accessibility is usability, enforced

Nearly every WCAG requirement is a usability best practice with teeth: honest labels, visible focus, logical structure, sufficient contrast, error messages that identify and explain. Krug's "accessibility is usability, continued" ([P15](../steve-krug/principles.md)) runs the other way too: fixing accessibility fixes usability for everyone (curb-cut effect — captions in loud rooms, keyboard paths for power users, contrast in sunlight).

## Semantics are the API of the interface

Assistive technology consumes the page through the accessibility tree, which is generated from semantics: elements, roles, names, states. A `<div onclick>` is a hole in that API — invisible to the tree, unreachable to the keyboard. The first move of accessible engineering is not ARIA; it's native HTML, which ships correct semantics, keyboard behavior, and states for free. ARIA is the escape hatch for genuinely custom widgets, and *incorrect ARIA is worse than none* — it makes confident false promises to the tree.

## Testable by design

WCAG's genius is normative testability: success criteria are written as pass/fail statements about content, not aspirations. That's what lets accessibility enter the review pipeline as engineering rather than empathy theater. Automated checkers catch perhaps a third (contrast, names, structure); the rest needs a human or agent walking keyboard paths and reading the page as the tree presents it. This pack structures both.

## Legal reality, briefly

Accessibility is regulated in most major markets (ADA/Section 508 in the US, EAA/EN 301 549 in the EU, and equivalents elsewhere), with WCAG as the near-universal technical reference. For AKOS purposes the ethics and the engineering suffice — but for any commercial product, conformance is also risk management.
