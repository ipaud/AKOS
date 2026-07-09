# Anti-Patterns — Laws of UX Pack

## The wall of choices (Hick)

Pricing pages with 6 undifferentiated tiers, onboarding asking 12 preferences upfront, dashboards offering 30 equal actions. Fix: defaults, grouping, progressive disclosure, one recommended path.

## Pixel hunting (Fitts)

Frequent actions on tiny targets: 16px icon buttons for hourly operations, close buttons at 1px from screen edge traps, resize handles 2px wide. Fix: LX3, LX5; padding counts as target.

## Danger at thumb's rest (Fitts inverse violation)

Delete buttons in mobile thumb zones, "Discard" adjacent to "Save", destructive swipe with no threshold. Fix: LX4, distance + friction proportional to loss.

## NIH interface syndrome (Jakob)

Reinvented scrollbars, custom-everything selects, novel nav metaphors for standard content ("explore our galaxy"). Every deviation bills learning cost to users. Fix: LX7; innovate on substance.

## Human clipboard (Miller/Tesler)

"Copy this code and paste it in the next screen"; "remember your reference number"; re-asking data the system already has. Fix: LX8, LX10 — the system carries; the user never ferries data between its own screens.

## Complexity dumping (Tesler)

Required fields the backend could infer, format rules as user homework, config screens before first value. Fix: infer + override; defaults; deferred configuration.

## The abrupt ending (Peak-End)

Checkout ending on a spinner; setup wizard ending on "Done." with an empty dashboard; support flow ending on a survey. Fix: LX12 — celebrate, locate the result, point forward.

## Highlight inflation (Von Restorff)

Three "primary" buttons, five badge colors, everything animated. The user's attention defaults to random. Fix: LX14 — one accent; spend it deliberately.

## The pretty mask (Aesthetic-Usability)

Shipping a beautiful broken flow because demo feedback was warm; skipping behavioral testing because satisfaction scores are high. Fix: LX17 — measure behavior; treat praise as contaminated.

## Fake progress (Goal-Gradient abuse)

Progress bars that jump to 90% then crawl; "profile 80% complete" where the last 20% is 15 fields; artificial steps added to trigger completion urges. These are dark patterns: short-term conversion, long-term goodwill bankruptcy. Fix: honest gradients (LX11) or none.

## Law laundering (meta)

Citing a law outside its mechanism to win an argument: Miller's for menu length, Hick's to strip expert features, Peak-End to skip fixing the middle. Fix: check the law's boundary conditions in [principles.md](principles.md) before citing; reviewers reject decorated claims.
