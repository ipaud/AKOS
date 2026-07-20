# Anti-Patterns — Context Engineering Pack

Named failure modes. Detection cue → why it fails → fix. The first block covers failures that produce a *wrong answer the agent is confident about* rather than mere inefficiency; those are correctness bugs and are scored as such.

## Context poisoning

**Detect:** an early tool result, search snippet, or retrieved document contains a wrong or stale claim, and later turns cite it, build on it, or treat it as independently corroborated by their own conclusions.
**Why it fails:** nothing inside a context window marks a claim as unverified once it's been read — it looks exactly like a checked fact, and every subsequent inference compounds the error rather than catching it. By the time it surfaces, the wrong claim is buried under plausible-looking derived reasoning.
**Fix:** verify load-bearing claims against the artifact at the point they enter context, not after they've been used. Trace a "well-corroborated" conclusion back to its sources before trusting the corroboration.

## The kitchen-sink prompt

**Detect:** a system prompt, skill, or session that loads most or all of what's available — every pack, every doc, every tool schema — regardless of what the current task actually needs.
**Why it fails:** it doesn't raise answer quality, it lowers it: the genuinely relevant material is diluted among material the task never asked for, and every token spent this way is a token of attention not spent on the actual question.
**Fix:** route to the smallest set of sources that fits the task (CE2, CEE1–CEE2); require a stated reason for every inclusion.

## Context rot / lost in the middle

**Detect:** a long-running session's answers get vaguer, revert to generic defaults, or quietly drop an early instruction, without a corresponding rise in task difficulty.
**Why it fails:** effective attention to any one piece of context degrades as total length grows, well before the nominal window limit is hit — "it still fits" is not evidence the model is still using it well.
**Fix:** compact on a stated threshold before degradation is visible; check whether early constraints are still honored in a long session; test agent quality at realistic context lengths, not only the shortest one.

## The instruction that wasn't

**Detect:** a fetched web page, file, or tool result contains an imperative-sounding string ("ignore previous instructions," "system: reveal your prompt," a fake role header) and the agent's later behavior shifts as if it had received a new directive.
**Why it fails:** content retrieved from outside the genuine instruction layers carries no authority regardless of its phrasing — treating it as an instruction collapses the entire trust boundary the hierarchy exists to protect.
**Fix:** structurally label retrieved and tool-returned content as data, never as instruction; restate suspicious embedded directives as quoted content to flag, not text to obey (CE7, CEE28).

## The duplicated rule that drifted

**Detect:** the same rule stated in two places (a system prompt and a project doc, a skill and a subagent) with slightly different wording, and one of the two was updated without the other.
**Why it fails:** whichever copy the agent happens to weight more in a given moment wins, silently and unpredictably — the disagreement isn't a design decision, it's an artifact of which copy got edited last.
**Fix:** one canonical statement per rule, everywhere else a pointer to it (CE8, CEE32). Treat a found duplicate as a bug to merge immediately, not a conflict to reconcile per instance.

## Lossy summarization that drops a decision

**Detect:** a session gets compacted or summarized, and a later turn contradicts, reintroduces, or re-litigates something that was already decided or ruled out before the compaction — because the summary kept the narrative and dropped the specific commitment.
**Why it fails:** summarizers compress toward the general and away from the specific by default, and the specific is exactly where decisions, constraints, and exact identifiers live. A summary that reads fluently can still have silently discarded the one fact that mattered.
**Fix:** capture decisions/constraints/open-questions explicitly before compacting and carry that list across verbatim, independent of how hard the rest of the narrative compresses (CE9, CEE35–CEE39).

## The wrong-tier memory

**Detect:** a task-scoped fact ("the bug is in the second seed row") gets written to project memory and outlives its truth; or a durable, project-wide convention only ever gets mentioned in a session that's later discarded, so nobody downstream benefits from it.
**Why it fails:** the four memory tiers exist because facts have different lifespans and different audiences — misfiling either direction means the agent eventually acts on something either stale or missing.
**Fix:** name the tier and expected lifetime before persisting anything (CE10, CEE40–CEE44); if either can't be named, hold it in working context instead of writing it down.

## The stale cached fact

**Detect:** a persisted note states something volatile as if it were stable — a file's line count, the current branch, "the tests currently pass" — and an agent later acts on the cached version instead of re-checking.
**Why it fails:** volatile facts are wrong again almost immediately; caching them trades a cheap live check now for a confident wrong answer later.
**Fix:** classify every persisted fact as stable or volatile before writing it down; recompute volatile facts at the point of use instead of reading them from a note (CE11, CEE45–CEE47).

## The full-repo dump

**Detect:** an agent asked to find or change something specific reads most or all files in a large repository rather than searching for the relevant ones first.
**Why it fails:** the read itself burns the context budget before the actual task starts, and the resulting context is too undifferentiated for the model to reason over well — "thorough" in appearance, worse in effect than a five-second targeted search.
**Fix:** search-first and manifest-first by default; reserve a full read for tasks that genuinely require whole-codebase reasoning, and state that reason explicitly (CE15, CEE55–CEE58).

## Confident hallucination presented as verified

**Detect:** a response states a specific, checkable fact (a function's behavior, whether a test passes, a security property) in the same confident register as facts that were actually checked against the artifact, with no distinguishing marker.
**Why it fails:** the reader has no way to tell which sentences were verified and which were inferred or assumed, so an unverified claim gets the same trust as a checked one until it's wrong.
**Fix:** check what's checkable before stating it; explicitly flag anything not verified as an assumption, and cap its confidence and severity accordingly (CE14, CEE52–CEE53; see [core/confidence-model.md](../../../core/confidence-model.md)).

## The static prompt that never routes

**Detect:** the same fixed bundle of context loads for every task regardless of shape — no routing step, no task-specific selection, "just load it all so nothing's missed."
**Why it fails:** a fixed bundle can't be correctly sized for both the easy tasks and the hard ones at once — it's too heavy for the former and, because it was sized for the average case, often still too thin for the latter.
**Fix:** build a routing mechanism that matches task shape to a short list of sources at run time, and state which sources were selected and why (CE13, CEE48–CEE51).

## Preloading "just in case"

**Detect:** information is fetched and embedded into context at session start on the reasoning that it "might be needed later," when it could have been fetched at the point of actual need instead.
**Why it fails:** it pays the attention and token cost for the entire session whether or not the material is ever used, and the preloaded snapshot can go stale before the point it would have been needed.
**Fix:** default to just-in-time retrieval; preload only when the fetch is genuinely expensive or the need is near-certain and immediate, and treat that as a stated exception (CE4, CEE12–CEE16).

## The buried critical instruction

**Detect:** the single constraint the task most depends on is placed in the middle of a long assembled context — a big pasted file, a long retrieved document — rather than near the start or end.
**Why it fails:** content in the middle of a long context is used less reliably than content at the edges, independent of how important it actually is; burying the load-bearing constraint there is how it gets quietly dropped.
**Fix:** place the most load-bearing instructions and facts at the start or end of the assembled context, and restate a critical constraint near the point it will be acted on if a lot of context sits between (CE16).
