# Anti-Patterns — Philosophy of Software Design Pack

Named failure modes, how to spot them, and what to do instead. The last two are failures
of *applying this pack*, which is the more likely risk on a codebase that already has
`solid` and `clean-architecture` loaded.

## The shallow module

**Detect:** a class or module whose public surface exposes nearly everything its
implementation contains — a wrapper whose methods map one-to-one onto the thing it wraps,
a "service" that forwards each call to a repository.
**Why it fails:** the caller pays the full cost of learning a new abstraction and gets
almost nothing hidden in return, so total complexity rose.
**Fix:** either give it something real to hide (validation, retry, caching, invariants), or
delete it and let the caller talk to the thing directly. (PSD2, PSD4)

## Temporal decomposition

**Detect:** modules named for stages — `Reader`, `Parser`, `Transformer`, `Writer` — split
along the order operations happen in, with the same format knowledge in two of them.
**Why it fails:** a format change now touches every stage that understands it, which is the
definition of change amplification. The split followed the control flow rather than the
knowledge.
**Fix:** group by what a unit knows. The reader and the writer for one format belong
together, even when they run at opposite ends of the pipeline. (PSD9)

## Information leakage by convention

**Detect:** two modules that never call each other but must agree — a key naming scheme, a
sort order, a magic value, a rule that column X is null when column Y is set.
**Why it fails:** it's coupling with no import to reveal it, so it survives every
dependency-graph review and breaks the first time someone changes one side.
**Fix:** give the shared decision one owner — a shared type, a constructor, one function
both sides call. (PSD8)

## The pass-through layer

**Detect:** a layer whose method names and signatures largely mirror the layer below;
variables threaded through several frames to reach one consumer.
**Why it fails:** it costs a hop to read, a file to open, and a name to learn, while
offering no new abstraction.
**Fix:** delete the layer, or give it a real job — this is where validation, caching, or
policy usually belongs. (PSD6, PSD5, PSD7)

## The exception nobody could avoid

**Detect:** an error signalled for a condition that could simply have been defined as
normal — deleting an absent file, cancelling a finished task, closing a closed handle —
and the same `try` block copied at every call site.
**Why it fails:** every caller pays a branch forever so the callee could avoid one decision
once.
**Fix:** absorb it into the operation's semantics, or handle it once, lower down. (PSD17,
PSD18, PSD19)

## Configuration as an escape hatch

**Detect:** parameters and flags added because a decision was hard, with defaults nobody
has ever changed and no documentation of when to change them.
**Why it fails:** the module pushed its own complexity onto callers who know less about it
than the module does, and every combination is now nominally supported.
**Fix:** decide inside the module. Keep the parameter only where a caller demonstrably has
information the module cannot have. (PSD12, P7)

## The comment that restates the code

**Detect:** `// increment the counter` above `counter++`; a docstring listing the
parameters by name and no more.
**Why it fails:** it consumes attention, adds nothing, and drifts — at which point it is
actively misleading. Its presence usually means naming was skipped.
**Fix:** delete it. Then ask what a reader actually cannot recover: intent, units,
invariants, the rejected alternative. Write that instead. (PSD27, PSD28, PSD29)

## The implementation comment on the interface

**Detect:** a public docstring describing the algorithm, the data structure, or the
internal call order.
**Why it fails:** it leaks implementation into the interface, so callers start depending on
it and the comment must change every time the implementation does.
**Fix:** interface comments say what a caller needs; implementation comments live inside,
next to the code they explain. (PSD26, PSD30)

## The tactical tornado

**Detect:** high output, always shipping, always the fastest route to "working" — and a
steadily rising cost for everyone else to change the same area afterwards.
**Why it fails:** complexity is incremental, so nothing about any individual change looks
wrong, and by the time the effect is visible the cause is distributed across a year of
commits.
**Fix:** treat a small, continuous design investment as part of "done" rather than a
cleanup to schedule. Measure by whether the next change in that area got easier or
harder. (PSD33, P4, P15)

## Classitis

**Detect:** many small classes, each holding one method, none of which hides anything;
a call chain five frames deep where every frame adds a name and no meaning.
**Why it fails:** decomposition was treated as automatically virtuous. Each split added an
interface, and interface is cost — the total complexity went up while every individual unit
looked admirably small.
**Fix:** ask of each unit what it hides. Merge the ones that hide nothing. Note that this
is a genuine disagreement with a common reading of `solid`, resolved explicitly in
[decision-framework.md](decision-framework.md), and that a Level 0 personal file-size
convention outranks both. (PSD1, PSD3)

## The unfalsifiable design objection

**Detect:** review comments like "this module is shallow" or "that's not deep enough", with
no statement of what a caller would stop needing to know.
**Why it fails:** it cannot be answered, so it either blocks work arbitrarily or teaches
everyone to ignore design feedback — which costs more than the original problem.
**Fix:** every finding names the reader or caller who benefits and what they stop having to
know. If that sentence can't be written, the finding is dropped. Nothing in this pack is
above MEDIUM. (review-checklist, reviewer discipline)

## Design theatre on a prototype

**Detect:** depth analysis, second designs, and interface-comment-first discipline applied
to code that exists to answer a question and will be deleted.
**Why it fails:** it spends the budget this pack exists to protect, on an asset that isn't
one.
**Fix:** Prototype profile skips this pack. Tactical is the correct mode; note the obvious
leakage and move on. (decision-framework, profile modulation)
