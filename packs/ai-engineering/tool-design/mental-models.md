# Mental Models — Tool Design Pack

Named models this pack contributes. Use them as diagnostic lenses while designing, reviewing, or debugging a tool an agent calls.

## The blind selection

An agent chooses a tool with no ability to inspect it first. There is no hovering, no opening it to look, no cheap experiment — the choice is made from the name, the description, and the schema, and it is committed the moment it is made. This is the opposite of how a human meets an unfamiliar API, and nearly every agent-facing design mistake traces back to forgetting it. Whatever a caller would have needed to look up must be present at the point of selection or it is not present at all.

**Diagnostic:** cover the implementation and read only the name, description, and schema. Can you say exactly what calling it does, to what, and whether anything changes? If not, neither can the agent, and it will find out by calling.

## The ambiguity tax

Every ambiguity in a tool's surface is paid for in extra calls, and the payments are spread thin enough to be invisible individually. An unclear parameter format costs a malformed call and an error read. Two plausibly-overlapping names cost a wrong selection and a correction. An unmentioned prerequisite costs a failure and a recovery. None of these look like a defect in a log; collectively they turn a four-call task into an eleven-call one, and the symptom reads as model unreliability rather than as interface debt.

**Diagnostic:** take a real trace and mark every call that exists only because something was unclear. That count, not the error rate, is the tool surface's actual quality signal.

## The evidence gap

Between what a tool did and what the agent can claim it did sits a gap whose width is set entirely by the response. A success token leaves it maximally wide: the agent knows only that nothing threw, and anything it says beyond that is inference dressed as observation. A response carrying the resulting state closes it: the agent can compare intent to effect without spending another call, and its report is grounded in something it actually saw. The gap does not stay empty — the agent fills it with an assumption, and that assumption enters the transcript looking exactly like a verified fact.

**Diagnostic:** read only the response and ask what the caller can now assert. If the honest answer is "that the call did not error," the response is an acknowledgement, not evidence.

## The blast radius

The scope of an operation is a function of its arguments and the current state of the world, and the agent can see only the first half. A delete filtered by a date range matches what it matches; the agent's estimate and the reality differ by however wrong its model of the data is, and nothing in the call reveals the difference. The tool holds the other half. A preview is simply the tool telling the caller the size of the thing it is about to do, before it becomes irreversible.

**Diagnostic:** for any operation, ask whether the number of affected entities is knowable from the arguments alone. If it depends on state the caller cannot see, that operation needs a dry run before it needs anything else.

## The three primitives

Three genuinely different contracts get flattened into the single word "tool," and they differ on the one property most relevant to an agent about to call something — whether calling costs anything irreversible.

| Primitive | What it is | The question it answers | Consequence of calling |
|---|---|---|---|
| **Tool** | An operation with an effect | "What can I *do*?" | May change the world; weigh before calling |
| **Resource** | Readable material addressable by identifier | "What can I *read*?" | Free; retrieves context, changes nothing |
| **Prompt** | A parameterized, reusable template | "What established procedure can I invoke?" | Structures a request; no effect of its own |

Collapsing them costs in both directions. Expose a document read as a tool and it gets weighed with the caution due a mutation; expose a mutation among a crowd of read-shaped tools and it gets called with the freedom due a read.

**Diagnostic:** for each item in a surface, ask whether calling it changes anything. If the answer varies across items that look and are named alike, the surface has flattened the primitives and the agent has no way to tell them apart.

## The composition ladder

Any capability can be exposed anywhere along a range from one tool that does everything to a tool per primitive operation, and the two ends fail differently. The monolith fails at partial failure: several effects behind one name, one error, no way to know what landed. The over-decomposed surface fails at selection and at ritual: fifteen near-identical names to choose between, and a fixed four-call sequence the agent must reproduce on every task. The right rung is neither end — it is the coarsest granularity at which every failure is still attributable to one effect the caller can act on.

**Diagnostic:** for each tool, ask what a caller can do when it half-succeeds. If the answer is "nothing useful, because it can't tell what happened," it's too coarse. Then ask whether every task begins with the same invariant three calls; if so, it's too fine at that seam.

## The description as a live artifact

A tool description is not documentation written once at the end. It is the surface the agent reasons over, and like any interface it has a real user whose behavior can be observed. The first version is written from inside the knowledge of how the tool works, which is exactly the vantage point that hides its ambiguities; the second version is written from the evidence of an agent getting it wrong. Descriptions that are never revised against observed calls are untested interfaces that happen to be made of prose.

**Diagnostic:** ask when the description was last changed in response to something an agent actually did. If the answer is "never," it is a first draft in production.

## The surface as a set

Tool quality does not decompose per tool. Selection is a comparison across everything available, so a new tool overlapping two existing ones lowers the accuracy of choosing those two — and no amount of improvement to any single description fixes an overlap that exists between them. This reframes "should we add this tool" from a question about the tool to a question about the set: what does it do to the discriminability of everything already there.

**Diagnostic:** before adding a tool, name the request it serves that nothing existing serves. If the sentence needs a qualifier to distinguish it from a neighbour, the agent will need the same qualifier, and it will not have it.

## The reference round trip

An agent that receives a result and must later act on it either carries a handle the surface gave it, or reconstructs a reference from what it remembers — "the third one," "the file from that listing," "the newest of those." Reconstruction is a derivation performed against a world that may have changed since, and it is where the wrong entity gets modified. Every returned identifier that a subsequent tool accepts removes one derivation and the error class attached to it.

**Diagnostic:** trace a two-step task end to end. At the second step, is the agent passing something the first step handed it, or something it rebuilt? Rebuilt means the surface dropped an identity it already had.
