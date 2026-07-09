# Examples — Laws of UX Pack

Invented cases.

## Hick — pricing page

- Bad: 6 tiers × 14-row comparison, no guidance.
- Good: 3 tiers, "Most popular" on one, expandable full comparison below, annual default with toggle.

## Fitts — mobile audio app

- Bad: play/pause 24px, top-right; delete-track swipe fires at 10% drag.
- Good: play/pause 64px bottom-center (thumb home); delete requires 60% swipe + release confirmation, styled distinct.

## Jakob — checkout

- Bad: novel "conversational checkout" replacing cart+address+payment with a chat UI. Users hunt for the order summary.
- Good: conventional 3-step checkout; the brand's personality lives in copy tone and the confirmation moment.

## Miller/Tesler — 2FA flow

- Bad: "Note this backup code, you'll need it on the next screen" → next screen asks to retype it.
- Good: code auto-carried; user confirms with a checkbox "I saved it"; download/copy buttons provided.

## Tesler — expense form

- Bad: 11 fields including currency, category, VAT rate.
- Good: photo upload → OCR prefills amount/date/merchant; currency from merchant country; category from merchant history; user reviews 3 prefilled fields and submits. Complexity moved into the system.

## Peak-End — onboarding

- Bad: 6 setup screens ending on "Settings saved."
- Good: same steps, ending on the user's own data live in the product ("Your first dashboard — built from the source you just connected"). The aha *is* the ending.

## Serial Position — feature nav

- Bad: `Home · Reports · Exports · Settings · Billing · Insights(new flagship)` — flagship buried 6th of 6? No: middle-buried at position 6 is actually last=remembered; the bad version is position 4 of 6.
- Good: `Insights · Reports · Exports · Billing · Settings · Home?` — no: keep convention (Jakob) for Home first; put flagship second and Settings last: `Home · Insights · Reports · Exports · Billing · Settings`.

## Von Restorff — table rows

- Bad: overdue invoices bold + red + badged + animated, 40% of rows qualify.
- Good: one "overdue" treatment (subtle red left-border + badge); if 40% are overdue, the *view* defaults to overdue-first sorting instead of shouting.

## Aesthetic-Usability — beta test readout

- Signal: testers rate the redesign 9/10 "much easier"; task completion actually dropped 12%.
- Action: ship the visual layer, revert the interaction change that caused the drop, re-test. Praise recorded, behavior obeyed.

## Goal-Gradient — setup checklist

- Bad: "0 of 5 steps complete" greeting a new user.
- Good: "1 of 5 complete ✓ (account created)" — honest endowed progress; final step labeled "Last step: invite your team".
