# Examples — Design Patterns Pack

## Strategy applied correctly (≥2 real cases)

```ts
interface ShippingStrategy { calculate(order: Order): number; }
class StandardShipping implements ShippingStrategy { calculate(o) { /* ... */ } }
class ExpressShipping implements ShippingStrategy { calculate(o) { /* ... */ } }
// checkout depends on ShippingStrategy interface, injected per order
```

Correct: two real, distinct implementations exist; a third (international) is trivially addable without touching checkout.

## Strategy skipped correctly (only 1 case)

A single tax-calculation rule for a single-country MVP: `function calculateTax(amount) { return amount * 0.21; }` — no interface, no class. Adding a `TaxStrategy` abstraction here would be DP-E1 violation; correctly deferred until a second jurisdiction is real.

## Native-language alternative to Command

Instead of a `Command` class hierarchy for undo/redo:

```ts
type Command = { execute: () => void; undo: () => void };
const commands: Command[] = [];
function run(cmd: Command) { cmd.execute(); commands.push(cmd); }
```

A plain object literal + array does the job; no class hierarchy needed.

## Singleton replaced with DI

Bad: `Logger.getInstance().log(...)` reached from everywhere, hard to test in isolation.
Good: `constructor(private logger: Logger) {}` — one shared `Logger` instance created at the composition root and injected; tests supply a fake logger trivially.

## Decorator applied correctly

```ts
interface Coffee { cost(): number; }
class SimpleCoffee implements Coffee { cost() { return 2; } }
class MilkDecorator implements Coffee {
  constructor(private coffee: Coffee) {}
  cost() { return this.coffee.cost() + 0.5; }
}
// new SoyDecorator(new MilkDecorator(new SimpleCoffee())) — dynamic combos
```

Correct: dynamic per-instance composition is the actual requirement (many combinations of add-ons).
