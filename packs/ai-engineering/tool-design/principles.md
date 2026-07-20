# Principles — Tool Design Pack

Durable rules of how an agent-facing tool is shaped. Each carries an **operational corollary** — the form the principle takes when it hits a tool definition, a schema, or a response payload. Violating one requires an explicit tradeoff statement.

## TD1 — A tool built for a human is not automatically a good tool for an agent

A human calling an API brings context the agent does not have: the docs page open in another tab, the memory of last week's incident, a colleague to ask, and the willingness to try a call and read the stack trace. An agent brings a name, a description, a schema, and whatever came back last time. Wrapping an existing human-facing endpoint and declaring it agent-ready ships all of that missing context as the agent's problem, and the agent absorbs it the only way it can — by guessing, calling, and inferring from the failure.

**Corollary:** a tool exposed to an agent is designed with the agent as its user, not adapted from a surface designed for a person. Every place a human would have consulted something outside the call is a place the tool must carry the information itself.

## TD2 — The name and the description are the entire interface

An agent selects a tool before it can observe what the tool does. The only inputs to that selection are the name, the description, and the parameter schema — there is no exploratory click, no hover state, no "let me just see." A name that reads plausibly for two different effects, or a description that documents the implementation rather than the effect, produces a wrong selection the agent has no way to detect until after the call has landed.

**Corollary:** write the name and description so the effect of calling is unambiguous without a trial call. If two tools in the same surface could each plausibly answer the same request, one of them is misnamed or the pair should be one tool.

## TD3 — Small composable tools beat one tool that does everything

A tool with a `mode` parameter and eleven conditionally-required fields is several tools sharing a name. The agent must first infer which of the several it wants, then satisfy that variant's rules while ignoring the others', and the schema cannot express "these four fields matter only when `mode` is `export`." Small tools with narrow contracts compose: the agent chains them, sees each result, and recovers at the step that failed rather than at the whole operation.

**Corollary:** if a tool's parameter set partitions cleanly by a discriminator field, split it into one tool per partition. A conditionally-required parameter is a signal that the split is already latent in the design.

## TD4 — One call, one coherent effect

A tool that performs several unrelated side effects in one call — creates the record, sends the notification, writes the audit row, invalidates the cache — cannot report partial failure in a way anything can act on. When the third of four succeeds, the agent receives one error and no way to know what landed. Retrying re-applies the first two; not retrying leaves the last undone. Neither is correct, and the agent has no information with which to choose.

**Corollary:** each tool has one effect a caller would describe in one clause. Where several effects genuinely must happen together, they are one transaction with one atomic outcome — not several effects behind one name with independent failure modes.

## TD5 — Inputs are typed and validated at the boundary, never a free-text string parsed by convention

A parameter documented as "a string like `status:open assignee:me sort:-created`" asks the agent to serialize structure into text, using a grammar it can only learn by example, so the tool can parse it back into structure. Every step of that round trip is a place to be silently wrong: a missing colon, a quoted value, an escape the format never anticipated. Typed fields with enumerated values remove the class of error entirely, because the schema rejects a malformed call before it executes rather than misinterpreting it.

**Corollary:** express structure in the schema, not in a convention the description explains. Enumerate closed sets as enums, constrain formats with declared patterns, and reject invalid input at the boundary with a message naming the violated constraint.

## TD6 — A response returns evidence, not acknowledgement

`{"status": "ok"}` tells the agent that the call did not error. It does not say what the resulting state is, so the agent must either trust the acknowledgement or spend another call verifying. Trusting is how a confidently wrong claim enters the transcript — the agent reports the file written, the row updated, the branch pushed, on the strength of a token the tool would have returned whether or not the effect matched the intent. A response carrying the resulting state lets the agent check its own work in the turn it did the work.

**Corollary:** a successful response returns enough of the resulting state for the caller to verify that the effect matched the intent — the created identifier, the new value, the count affected, the resulting content — not a success token.

## TD7 — An error states the next action

An agent reading an error has one decision to make: what to do differently. `400 Bad Request`, `invalid input`, and an unmodified runtime traceback all fail to inform that decision, so the agent falls back on its most expensive strategy — vary something and call again — which is how one malformed parameter becomes six wasted calls. An error naming the offending field, the constraint it violated, and the shape of a valid value converts a retry loop into a single corrected call.

**Corollary:** every error response names what was wrong, which input caused it, and what the caller should do next. An error the agent can only respond to by guessing is an incomplete error, however correct its status code.

## TD8 — Repeat-safety is a property of the tool, declared at the tool's boundary

An agent will call a tool twice with the same arguments — after a timeout that fired late, on a retry, after a replan re-executes a completed step. Whether that is safe is a fact about the tool, not about the agent's discipline, and it is a fact the agent cannot discover except by causing the duplicate. A tool that is safe to repeat and says so can be retried freely; a tool that is not and says so can be gated. A tool silent on the question gets treated as whichever the agent assumed.

**Corollary:** every side-effecting tool either is naturally idempotent, accepts an idempotency key, or states in its description that it is not repeat-safe. The guarantee lives in the contract where a caller can read it — the counterpart to the caller-side obligation in [agent-foundations](../agent-foundations/README.md) AF16.

## TD9 — Consequential operations offer a preview; destructive ones require confirmation

The gap between what an agent intends and what its arguments actually select is invisible until the operation runs. A filter matching four rows in the agent's model and four thousand in the database produces the same call either way. A preview collapses that gap into something checkable before it becomes something irreversible: the agent sees the scope, compares it against its intent, and proceeds or corrects.

**Corollary:** any operation whose blast radius depends on its arguments exposes a dry-run mode returning what *would* happen, in the same shape as what did. Irreversible operations additionally require an explicit confirmation parameter a caller must set deliberately — never a default the agent inherits.

## TD10 — A result set is bounded by the tool, not by the caller's restraint

A tool returning whatever the query matched hands the agent an unbounded liability. The call that returns forty thousand rows does not fail — it succeeds, floods the context window, and degrades everything the agent does for the rest of the session, including its ability to notice what happened. The tool is the only participant positioned to enforce a bound, because it is the only one that knows the size before the payload is committed to.

**Corollary:** every tool that can return a collection enforces its own default limit and hard maximum, and returns a cursor for continuation plus a total count so the caller knows what it did not receive. See [context-engineering](../context-engineering/README.md) CE1 and CE6 for what an unbounded return costs downstream.

## TD11 — Return stable references the next call accepts

An agent that must construct its next call from a positional description — "the third result," "the file from the earlier listing," "that PR" — is re-deriving an identity the tool already had and discarded. Re-derivation is where the wrong record gets modified: the list reordered, the index shifted, the name turned out ambiguous between two matches. A handle returned by one call and accepted by the next removes the derivation step and the whole class of error attached to it.

**Corollary:** every returned entity carries a stable identifier, and the tools acting on that entity accept that identifier directly. A caller should never have to reconstruct a reference the surface could have handed it.

## TD12 — Read-before-write belongs in the surface, not in a hope about the agent

"The agent should check current state before modifying it" is a behavior a prompt can request and cannot guarantee. Where a blind write is genuinely dangerous, the safe ordering is enforceable in the contract: the write requires a version, an etag, or a content hash the agent could only have obtained by reading first, and a stale one is rejected. That converts a convention into a precondition, and a lost update into a rejected call with an actionable error.

**Corollary:** where a blind overwrite would lose information, the write tool requires a token obtained from a prior read and fails loudly when it is stale. Where reading first is merely advisable, the write tool's own description says so — not only the read tool's.

## TD13 — Actions, readable context, and reusable templates are three contracts, not one

Three different things get exposed under the single word "tool": operations that change the world, material that can be read into context, and parameterized templates a caller can invoke. They differ in exactly the property that matters most to an agent deciding whether to call something — whether calling is free. Collapsing them means either every document read is weighed with the caution due a deletion, or, worse, a deletion is weighed with the caution due a read.

**Corollary:** keep the three primitives distinct in the surface, per the Model Context Protocol's tool/resource/prompt separation. Where a capability is exposed as a tool, its description states plainly whether calling it mutates anything.

## TD14 — The first draft of a description is wrong, and observed calls are how you find out

A description is written by someone who already knows what the tool does, which is precisely the state that makes its ambiguities invisible. The ambiguity shows up only in the calls an agent actually makes: the parameter filled with the wrong kind of value, the neighbouring tool reached for instead of this one, the sequence invented because nothing indicated a prerequisite existed. That evidence is cheap to collect and is the only reliable input to a second draft.

**Corollary:** prototype the tool, watch real agent calls against it, and revise the name, description, and schema against the specific mistakes observed. A description never tested against an agent's actual behavior is an untested interface.

## TD15 — Every tool in the surface competes with every other for correct selection

Tool quality is not a per-tool property. Adding a twelfth tool overlapping two existing ones degrades the accuracy of selecting those two, because the agent's decision is a comparison across the whole surface. A surface of near-synonymous tools produces selection errors that look like model failures and are design failures, and the fix is never a longer description on one of them — it is removing or merging the overlap.

**Corollary:** treat the tool surface as a set with a budget, not a catalogue to grow. Before adding a tool, name the request it serves that no existing tool serves; if an existing tool nearly serves it, extend or merge rather than add a neighbour.

## TD16 — A tool's contract is testable, and an untestable contract is one the agent must invent

If you cannot write a test asserting what a tool returns for a given input — including its error cases, its enforced limit, and its behavior on a repeated call — then the contract is not specified, and the agent is inferring it from prose. Whatever it infers becomes the de facto contract, and that inference will differ between models, between versions, and between the happy path and the third retry.

**Corollary:** every tool has tests covering its success shape, its error shapes, its enforced limit, and its behavior when called twice with identical arguments. The tests are the contract; the description is the summary of the contract the agent reads.
