# Mental Models — Design Patterns Pack

## Three families

**Creational** (Factory Method, Abstract Factory, Builder, Singleton, Prototype) — control how objects are created, decoupling creation from use. **Structural** (Adapter, Decorator, Facade, Composite, Proxy, Bridge) — compose objects/classes into larger structures while keeping them flexible. **Behavioral** (Strategy, Observer, Command, State, Template Method, Iterator, Chain of Responsibility, Mediator) — manage algorithms, responsibilities, and communication between objects. Recognizing which family a problem belongs to narrows the search fast.

## Program to an interface, not an implementation

The GoF's foundational advice: depend on the abstract shape of a collaborator, not its concrete type. Nearly every pattern in the catalog is one specific application of this one idea — Strategy programs against an algorithm interface, Observer against a subscriber interface, Factory against a product interface.

## Trigger condition, not aesthetic

Each pattern exists to solve one recognizable problem shape. The mental model to hold: "do I currently have *this specific pain*?" not "would this pattern look sophisticated here?" A codebase can be simple and pattern-free and be *better* architecture than one with patterns applied speculatively.

## Patterns compose

Real systems combine patterns: a Factory producing Strategy objects, a Decorator wrapping a Composite, an Observer notifying via a Command queue. Learn them individually, expect to see them mixed.
