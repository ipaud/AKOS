# Examples — SOLID Pack

## SRP split

Bad: `OrderProcessor.process()` validates input, calculates totals, charges payment, sends confirmation email, and logs analytics — one class, five reasons to change.
Good: `OrderValidator`, `OrderPricer`, `PaymentCharger`, `OrderNotifier`, each owning one axis; an orchestrating function composes them.

## OCP applied at the second variant

First payment method (Stripe) ships as a direct call — no abstraction yet. Second method (PayPal) requested → now extract `PaymentGateway` interface with `StripeGateway`/`PayPalGateway` implementations; the checkout flow depends on the interface.

## LSP violation caught

```ts
class ReadOnlyRepository extends Repository {
  save() { throw new Error("not supported"); } // violates LSP
}
```

Fix: `interface Readable { find(id): T }` and `interface Writable { save(t: T): void }`; `ReadOnlyRepository implements Readable` only — the type signature now tells the truth.

## ISP applied

Bad: `interface Worker { work(); eat(); sleep(); }` forcing a `RobotWorker` to stub `eat()`/`sleep()`.
Good: `interface Workable { work(); }`; `RobotWorker implements Workable` only.

## DIP applied where it matters

```ts
// use case owns the interface
interface NotificationSender { send(to: string, msg: string): Promise<void>; }

function notifyUser(sender: NotificationSender, user: User, msg: string) {
  return sender.send(user.email, msg); // testable with a fake sender
}
```

## SD6 in action (declining an abstraction)

A `formatCurrency(amount, currency)` utility used in one place, unlikely to vary: no interface, no strategy — a plain function is correct and the reviewer notes why no abstraction was added.
