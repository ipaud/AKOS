# Philosophy — Context Engineering

## Context is a budget, not a warehouse

A context window looks like storage — a place to put things so they're available later — and that appearance is the source of most bad context engineering. Storage has near-zero marginal cost per item; a context window doesn't. Every token that enters it is read, weighed, and competed against every other token for a fixed amount of the model's attention, and every token costs latency and money whether or not it ever mattered to the answer. The right question when adding something is never "is there room" — there almost always is — but "does this earn its place, for this task, right now." Treating the window as a warehouse produces prompts that are technically valid and quietly worse than a shorter one would have been.

## "It fits" is not "it's usable"

Model context windows have grown by orders of magnitude, and the growth invites a specific mistake: measuring context quality by whether something fits inside the limit rather than by whether the model can actually make good use of it once it's there. Attention is not uniform across a long context — content gets diluted, buried, and mis-weighted well before the nominal limit is reached. A 200,000-token window that holds 180,000 tokens of marginally-relevant material is not "using the window well"; it is spending capacity nobody asked for and making the genuinely relevant 5% harder to find. Capacity and usability are different axes, and conflating them is expensive precisely because it doesn't look like a mistake — the response still comes back, just worse.

## The window has no fact-checker

A human reading a long document keeps a background sense of which claims they've verified and which they're taking on faith. A model's context does not carry that distinction unless something puts it there explicitly — a wrong fact sitting in context looks exactly like a right one, and the model reasons from both with equal confidence. This is not a flaw to be patched later; it is a structural property of how context works, which means the responsibility for keeping bad facts out, or at least labeled, sits entirely with whoever assembles the context. Once a wrong claim is in and unmarked, no later mechanism inside the same context reliably catches it — the error has to be caught from outside, by verification against the actual artifact.

## Retrieval is a design decision, not a fallback

There is a habit of treating "just load everything up front" as the safe, thorough option and treating just-in-time retrieval as a shortcut taken under resource pressure. It is the reverse. Preloaded material is a bet that the content will still be relevant, still be correct, and still be needed by the time the model reaches the part of the task that would use it — and every one of those can fail silently. Fetching at the point of need is not a compromise; it is usually the more accurate design, because it retrieves the current state of the world instead of a snapshot taken at session start. Preloading earns its place only when the fetch itself is expensive enough, or the need certain enough, that paying the cost early is cheaper than paying it twice.

## Not all instructions are equal because they're all "in context"

Once something is inside the window, it is tempting to treat everything in there as roughly the same kind of thing — text the model reads and responds to. But a system prompt, a project convention, a user's request, and the contents of a file the model just fetched carry entirely different authority, and collapsing that distinction is how prompt injection works: a string inside a fetched document that reads like an instruction is still just content, and treating it as anything else hands control of the session to whatever the agent happened to retrieve. Authority in context comes from the layer a piece of text arrived through, never from its phrasing, its confidence, or its position.

## The corollary for compaction

Every long-running agent eventually has to compress its own history, and compression is where a session's real commitments quietly go missing. A summary that reads well and drops the one constraint that mattered is worse than no summary at all, because it looks complete. The discipline is not "summarize faithfully" in the abstract — it's naming, before compacting, exactly which facts are load-bearing (decisions taken, constraints agreed, questions still open) and treating those as a different class of content from the exploration that produced them, one that survives compression whole while the rest is free to compress hard.

## Where this philosophy stops

This pack is about the assembly of context — what's in it, in what order, for how long, from which layer. It does not cover how to phrase an instruction once it's in, how to design a tool's parameters, or how to structure a multi-agent handoff — see [agent-foundations](../agent-foundations/README.md) for those. It does not replace [core/confidence-model.md](../../../core/confidence-model.md)'s levels for how sure to sound about a claim, or [core/source-policy.md](../../../core/source-policy.md)'s rules for citing a source — this pack decides what reaches the model; those decide how the model should talk about what it knows once it's there. And it never licenses skipping verification: a context assembled perfectly by every rule in this pack can still contain a wrong fact, and the safety floor is checking the artifact, not trusting the assembly process.
