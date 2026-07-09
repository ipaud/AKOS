# Philosophy — DDD Pack

## The model is a shared language, not a diagram

DDD's central claim: software's hardest problem is usually not technical, it's translation loss between how domain experts talk about the business and how the code represents it. Every translation (business term → analyst's spec → developer's class name) leaks meaning. The fix is a **ubiquitous language** — one vocabulary, used identically in conversation, documentation, and code — so the code *is* the specification, not an approximation of one.

## Complexity is often in the boundaries, not the entities

Large domains don't have one true model — they have several, each valid within its own **bounded context** (Sales' "Customer" isn't Support's "Customer"; forcing one shared model across both produces a compromise that serves neither well). DDD's strategic half is about drawing these boundaries honestly and defining explicit translation at their seams, rather than pretending one unified model can serve the whole business.

## Tactical patterns protect invariants, not taste

Entities, value objects, and aggregates aren't stylistic choices — they exist to answer "what must always be true, and who's responsible for enforcing it?" An aggregate is a consistency boundary: the smallest cluster of objects that must be transactionally consistent together. Getting aggregate boundaries wrong (too big → contention and slow transactions; too small → invariants can be silently violated across an aggregate boundary) is DDD's most common tactical failure.

## Most software doesn't need full tactical DDD

Evans and Vernon both warn against this: strategic DDD (ubiquitous language, bounded contexts, context mapping) pays off broadly, cheaply, on almost any domain with real complexity. Full tactical DDD (aggregates, repositories, domain events, specifications) pays off only where the domain has genuine, gnarly business rules and invariants — a CRUD admin panel gets none of the benefit and all of the ceremony cost.
