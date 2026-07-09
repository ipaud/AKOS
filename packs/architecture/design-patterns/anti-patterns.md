# Anti-Patterns — Design Patterns Pack

## Pattern for pattern's sake

A `PaymentStrategyFactoryProvider` built for a system with exactly one payment method, "in case we add more someday." Fix: DP-E1 — ≥2 real implementations before the pattern.

## FactoryFactoryFactory

Layered creational patterns (a Factory that creates Builders that create Factories) applied to problems a plain constructor would solve. Symptom of pattern application detached from the trigger condition. Fix: decision-framework step 1 — name the plain-language pain first.

## Singleton-as-global-state

A `ConfigSingleton.getInstance()` reached from forty files, making tests order-dependent and state leak between them. Fix: DP-E2 — dependency-injected shared instance instead.

## Class-based Strategy in a language with functions

A full `interface Comparator` + three classes to sort three ways, in a language where `array.sort((a,b) => ...)` does the same job in one line. Fix: DP-E3.

## Pattern-name cosplay

A class named `UserObserver` that doesn't actually implement the Observer pattern's subscribe/notify shape — just a regular class with a misleading name, confusing anyone who reads it expecting the real pattern. Fix: DP-E5 — name matches structure, or rename.

## Premature Abstract Factory

Building a family-of-related-products abstraction for a system with one product line, because "we might support multiple platforms someday." Fix: decision-framework — defer until the second product line is real.

## Decorator chains as a substitute for design

Wrapping an object in six decorators to avoid deciding what the object's actual responsibilities should be — indirection substituting for a design decision. Fix: consider whether SRP-driven class boundaries would be clearer than decorator stacking.
