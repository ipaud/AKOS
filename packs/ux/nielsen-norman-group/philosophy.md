# Philosophy — NN/g Pack

## Usability is measurable, not a matter of taste

The NN/g school's founding move was turning "good design" from aesthetic debate into inspectable properties: learnability, efficiency, memorability, error rate/recovery, satisfaction. Once named, these can be evaluated, rated for severity, and tracked over time. Design review becomes engineering review.

## Heuristics: compressed evidence

The ten heuristics aren't commandments handed down — they're compression of thousands of observed usability failures into ten recurring causes. That's why they work as an evaluation instrument: most real problems, when found, turn out to be a violation of one of the ten. Their value is *shared vocabulary*: a finding tagged "H6 recognition-over-recall violation" carries its own justification.

## Discount usability: cheap beats perfect

A few evaluators with heuristics, or five users in a hallway test, find most of what a lab study finds at a fraction of cost. The dominant failure mode in practice is not "insufficient rigor" — it's *doing no evaluation at all* because the rigorous version felt too expensive. Method cost must stay below the organization's flinch threshold. (Krug's three-users-a-month is this philosophy as habit.)

## Evaluators find problems; users validate them

Heuristic evaluation and user testing are complements, not substitutes. Experts sweep broadly and cheaply but produce false positives; users are the ground truth but each session covers little. Sequence: heuristic pass first (clear the obvious), then test with users (find the surprises).

## Severity discipline

Not all problems are equal, and pretending they are destroys prioritization. Severity combines frequency (how many users hit it), impact (how badly it hurts the task), and persistence (does it keep hurting after the first encounter). AKOS maps this onto its CRITICAL/HIGH/MEDIUM/LOW scale — see [scoring-rubric.md](scoring-rubric.md).

## Jakob's Law as worldview

Users spend most of their time on *other* sites/apps. Expectations are formed elsewhere and imported into your product for free — or violated at your expense. Consistency (H4) is therefore not conservatism; it's riding the largest training dataset in existence. (Quantified cousin: [laws-of-ux](../laws-of-ux/principles.md).)

## Where this philosophy stops

Heuristics evaluate *usability*, not desirability, not visual identity, not product-market fit. A product can pass all ten heuristics and still be pointless (see [product packs](../../product/inspired/README.md)) or bland (see Level-0 identity rules). Use the instrument for what it measures.
