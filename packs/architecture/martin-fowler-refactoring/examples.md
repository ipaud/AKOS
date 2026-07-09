# Examples — Refactoring Pack

## Extract Function (Long Method smell)

Before:

```ts
function printInvoice(invoice) {
  let total = 0;
  for (const item of invoice.items) total += item.price * item.qty;
  console.log(`Invoice for ${invoice.customer}`);
  console.log(`Total: ${total}`);
}
```

After:

```ts
function printInvoice(invoice) {
  const total = calculateTotal(invoice.items);
  console.log(`Invoice for ${invoice.customer}`);
  console.log(`Total: ${total}`);
}
function calculateTotal(items) {
  return items.reduce((sum, i) => sum + i.price * i.qty, 0);
}
```

Behavior identical; tests pass unchanged before and after — a pure refactoring.

## Rule of three in action

1st occurrence: inline date-formatting logic in `InvoiceView`. Leave it.
2nd occurrence: same logic appears in `ReceiptView`. Wince, duplicate again, leave it (RF7 — not yet).
3rd occurrence: appears in `ExportCsv`. Now extract `formatInvoiceDate()`, call from all three.

## Two hats, separated commits

Commit 1 (refactor hat): `Extract calculateShipping() from checkout flow — no behavior change` (tests unchanged, all green).
Commit 2 (feature hat): `Add express shipping option` (new tests added, uses the now-extracted function).

## Strangler fig instead of rewrite

Legacy monolith's billing module is unmaintainable. Instead of a rewrite: new billing service built alongside; a routing facade sends new customers to the new service while existing customers stay on the old path; migrate cohorts incrementally; retire the old module once traffic is zero.

## Characterization test before refactoring

Legacy function with no tests and unclear behavior: write a test asserting its *current* output for representative inputs (even if some of that behavior looks like a bug) — this locks in a safety net before any structural change, and the "bug" becomes a separate, deliberate, tested fix afterward.
