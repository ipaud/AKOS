# Examples — TDD Pack

## Red-Green-Refactor cycle

```
RED:
test('calculateDiscount applies 10% for orders over $100', () => {
  expect(calculateDiscount(150)).toBe(15);
});
// run → fails: calculateDiscount is not defined

GREEN:
function calculateDiscount(amount) { return amount > 100 ? amount * 0.1 : 0; }
// run → passes

REFACTOR:
// extract magic numbers to named constants, tests stay green throughout
const DISCOUNT_THRESHOLD = 100;
const DISCOUNT_RATE = 0.1;
function calculateDiscount(amount) {
  return amount > DISCOUNT_THRESHOLD ? amount * DISCOUNT_RATE : 0;
}
```

## Triangulation forcing generalization

```
Test 1: expect(double(2)).toBe(4)  → implementation: return 4; (cheating, hardcoded)
Test 2: expect(double(3)).toBe(6)  → forces real implementation: return x * 2;
```

## Behavior-focused assertion (not implementation)

Bad: `expect(component.state.isOpen).toBe(true)` (internal state).
Good: `expect(screen.getByRole('dialog')).toBeVisible()` (observable behavior).
