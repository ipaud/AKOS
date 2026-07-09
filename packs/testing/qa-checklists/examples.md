# Examples — QA Checklists Pack

## Four-state sweep for a new feature

```
Feature: Invoice list
[ ] Empty — no invoices yet: shows guidance + "Create invoice" CTA
[ ] Loading — skeleton rows shown, not blank/spinner-only
[ ] Error — network failure shows retry option, not silent failure
[ ] Success — invoices render correctly, sorted, paginated
```

## Boundary-value test set for a text input

```
- Empty string
- Single character
- Maximum allowed length
- Maximum length + 1 (should reject/truncate gracefully)
- Unicode (emoji, accented characters, RTL text)
- HTML/script-like content (<script>alert(1)</script>) — should render as text, not execute
- Leading/trailing whitespace
```

## Exploratory session charter

```
Charter: Explore the checkout flow for data-loss risk under interruption
Timebox: 45 minutes
Focus: browser back button, tab close, network drop, session timeout
  mid-checkout
Findings logged: [steps to reproduce] → [expected] → [actual] → [severity]
```

## Regression checklist entry

```
Bug #482 (fixed 2026-03-01): Coupon code applied twice on double-click
Regression check: click Apply Coupon twice rapidly, verify discount
  applied only once
```
