# Heuristics — Krug Pack

Fast defaults with known exceptions. Try these first; deviate with a reason.

## Screens

- **Squint test first.** Blur your eyes: the primary action, page identity, and main content should still be findable. If everything blurs into equal gray, hierarchy is missing.
- **Five-second rule.** A newcomer should name what the page is for within five seconds. Test by showing it cold to anyone nearby.
- **One dominant action per screen.** Exception: true dashboards/hubs, where the dominant element is orientation itself.
- **If it needs instructions, redesign it.** Exception: genuinely novel interactions — then one short in-place hint beats a tutorial.
- **Count the questions.** Walk the screen as a first-timer and count every "hmm?". More than two → revise before shipping.

## Navigation & structure

- **Trunk test any interior page** (site name, page name, sections, local nav, you-are-here, search). Fails → fix nav before content.
- **Clicks are free if confident.** Three obvious clicks beat one ambiguous one. Depth is fine while scent stays strong; ambiguity is what kills.
- **Page name = link name.** The words clicked must appear as the title of the page that loads. Mismatch = user doubts they're in the right place.
- **Breadcrumbs for depth ≥ 3**, small, at top, with ">" separators, current page bolded and last.
- **Search box, not search link**, for any site with enough content to get lost in.

## Words

- **Cut half, then half again.** Applies to intros, instructions, empty-state text, button labels.
- **If a label needs a tooltip to disambiguate, the label failed.** Exception: icons for genuinely secondary actions may carry tooltips + accessible names.
- **Nouns users say, not nouns you invented.** "Pricing", not "Value options". Match the words users bring with them.
- **No happy talk.** Any sentence that could open any site's welcome blurb ("We're passionate about…") gets cut.
- **Front-load everything.** First two words of a heading/link decide whether the rest gets read.

## Choices & forms

- **Mindless > few.** Reducing the *thought per choice* matters more than reducing the *number of choices*. Ten obvious steps beat three head-scratchers.
- **Ask only what you use.** Every form field must justify itself; optional fields default to cut.
- **Accept any reasonable format** (spaces in card numbers, mixed-case emails). Normalize in code; never lecture the user about format.
- **Defaults do the work.** The 90% case should be pre-selected, with change possible.

## Clickability & feedback

- **Looks-clickable audit:** every interactive element passes "would my parent know to click this?" Hover-revealed affordances fail on touch.
- **Feedback within 100ms** for any tap/click — visual state change at minimum, even if the operation continues.

## Testing

- **Three users, one morning, once a month.** Recruit loosely ("grab almost anyone"), pay them, ask them to think aloud, resist helping.
- **Fix the worst thing you saw, not everything.** Severe problems mask the next layer; iterate.
- **Test competitors when you have nothing built.** Their sites are your free prototypes.

## Mobile

- **Thumb reach for primary actions** (bottom half of screen); destructive actions out of accidental-tap zones.
- **No hover-dependent anything.**
- **Tap targets ≥ 44px** with breathing room; adjacent small targets are worse than one bigger one.
- **Test on a real device over Wi-Fi *and* poor network.** Spinners hide usability sins.
