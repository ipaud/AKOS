# Decision Framework — Tool Design Pack

Decision rules for tool-shape calls. Compose with [core/decision-framework.md](../../../core/decision-framework.md).

## One tool or several

| The capability looks like | Decision |
|---|---|
| One effect, one clause, one failure mode | **One tool** |
| A discriminator parameter (`mode`, `action`, `type`) changing which other parameters apply | **Split** — one tool per branch of the discriminator |
| Several effects that can each fail independently | **Split** — the caller must be able to see which one failed |
| Several effects that must all happen or none | **One tool**, committing atomically, reporting one outcome |
| An invariant sequence of calls every task repeats in the same order | **Merge** — the ritual is a missing tool |
| Two tools whose descriptions must both be read to tell them apart | **Merge or rename** — the distinction isn't carrying |

**Rule:** the target granularity is the coarsest at which every failure is still attributable to one effect a caller can act on. Ask what a half-success looks like: if the caller can't tell what landed, it's too coarse; if every task opens with the same three calls, it's too fine at that seam.

## Which primitive does this capability belong in

| The capability | Primitive | Why |
|---|---|---|
| Changes state in the world | **Tool** | Calling has consequences the agent must weigh |
| Provides readable material addressed by an identifier | **Resource** | Calling is free; it fills context and changes nothing |
| Packages a reusable, parameterized procedure | **Prompt** | It structures a request rather than performing an effect |
| Reads state, but the read is expensive or rate-limited | **Tool**, with the cost stated in the description | The consequence is budget, not mutation, and it still needs weighing |
| Can't be separated (the surface has only one primitive) | **Tool**, with side-effect status stated explicitly in every description | The distinction has to live somewhere |

**Rule:** the sorting question is "does calling this change anything," asked of every item in the surface. Where similar-looking, similar-named items answer differently, the agent has no way to tell them apart and will treat them alike.

## What does a response return

| Situation | Return |
|---|---|
| A write that creates something | The created entity and its stable identifier |
| A write that modifies something | The changed fields, at their new values, plus the identifier |
| A write affecting many entities | The count affected and their identifiers — not a success flag |
| A read of a collection | The items, a total count (or an explicit "unknown"), and a cursor if more remain |
| A read of one large item | The requested range, plus the total size, plus how to fetch the rest |
| An operation with genuinely nothing to return | Treat as a finding — re-examine whether the effect is verifiable at all |

**Rule:** read only the response and ask what the caller can now assert. If the honest answer is "that the call did not error," it is an acknowledgement, and the agent will fill the gap with an assumption that reads like a fact for the rest of the session.

## What does an error have to carry

Every error answers three questions, in this order:

1. **What failed** — a stable code a caller can branch on, plus a human-readable message.
2. **What caused it** — the specific parameter and the specific constraint, where an input was at fault.
3. **What to do next** — a valid example value, the allowed enum members, or the name of the tool that satisfies the missing prerequisite.

Then one classification: **retryable** (rate limit, timeout, transient upstream) or **not** (invalid input, missing permission, absent resource). The agent cannot infer this reliably from a status code, and getting it wrong costs either a burned budget or an abandoned recoverable call.

**Rule:** if the only response available to the agent is "vary something and call again," the error is incomplete regardless of how correct its status code is.

## Does this operation need a preview, a confirmation, or both

| Situation | Requirement |
|---|---|
| Scope is fully determined by the arguments, and the effect is reversible | Neither |
| Scope depends on state the caller cannot see (a filter, a recursive walk, a bulk match) | **Preview** — a dry run returning the count and identity of what would be affected |
| The effect is irreversible, but narrow and fully specified (delete this one record by ID) | **Confirmation** — an explicit parameter with no default |
| The effect is irreversible and its scope depends on state | **Both** — preview first, then a confirmation naming the previewed scope or count |
| The effect is reversible but expensive or externally visible (sends mail, triggers a deploy) | **Confirmation**, and the description states what becomes visible to whom |

**Rule:** the confirmation is specific to the operation — the target, the count, the scope — never a generic boolean. A bare `confirm: true` is a field an agent can set reflexively, which makes it a formality rather than a gate.

## How is a result set bounded

Work down; all four apply to any collection-returning tool.

1. **A default limit enforced by the tool**, applied when the caller supplies none.
2. **A hard maximum the caller cannot exceed.** A caller-supplied limit is a request for less, never for more.
3. **A cursor for continuation**, not an offset, wherever the underlying set can change between calls.
4. **A byte or token cap alongside the item cap**, because a handful of large items can exceed a bound a thousand small ones would not.

Then the disclosure: the response states the total count (or explicitly that a total is unavailable) and marks truncation in a structured field rather than by the absence of further results.

**Rule:** an unbounded return is a tool-design defect that arrives as a context-engineering failure one call later — see [context-engineering](../context-engineering/README.md) CE1 and CE6. The tool is the only participant that knows the size before the payload is committed to, which makes it the one responsible for the bound.

## Does this write need read-before-write enforced

| Situation | Decision |
|---|---|
| A blind overwrite would silently lose another writer's change | **Enforce** — require a version, etag, or content hash from a prior read; reject a stale one |
| The write is additive or last-write-wins is genuinely acceptable | **Don't enforce** — but say so, so the semantics aren't guessed |
| Reading first is advisable but a stale write is recoverable | **Don't enforce** — state the recommendation in the *write* tool's description, naming the read tool |
| The write is destructive and scoped by a filter | **Enforce, plus a preview** — the version check doesn't bound the blast radius |

**Rule:** "the agent should check first" is a behavior a prompt can request and cannot guarantee. Where it matters, make it a precondition the tool enforces, and convert a lost update into a rejected call with an actionable error.

## Should this tool exist at all

Answer all four. Any "no" means don't add it.

1. **Does it serve a request nothing existing serves?** If the distinguishing sentence needs a qualifier, the agent will need that qualifier at selection time and will not have it.
2. **Would an agent select it correctly against its nearest neighbour?** Read the two names and descriptions side by side, in isolation from the implementation.
3. **Is its effect describable in one clause without "and"?** If not, it is at least two tools.
4. **Can you write its tests?** Success shape, error shapes, enforced limit, and behavior on a repeated identical call. An untestable contract is one the agent has to invent.

**Rule:** adding a tool changes the accuracy of every neighbouring tool, because selection is a comparison across the whole surface. The question is never only "is this tool good" but "what does it do to the discriminability of the set."
