# Glossary — Tool Design Pack

- **Acknowledgement response** — a reply confirming only that a call did not error (`{"status": "ok"}`, an empty 204). Leaves the caller unable to verify that the effect matched the intent, so it substitutes an assumption that then reads like a verified fact.
- **Ambiguity tax** — the extra calls an agent makes because a tool's name, description, or schema left something unclear. Paid in latency, tokens, and context; invisible per call, and the dominant cost of a poorly-shaped surface.
- **Blast radius** — the set of entities an operation actually affects, as opposed to the set the caller intended. Depends on state the caller cannot see, which is why the tool rather than the caller is responsible for bounding it.
- **Blind selection** — the condition an agent chooses a tool under: no inspection, no trial, no hover. Only the name, the description, and the schema are available, and the choice commits the moment it is made.
- **Confirmation parameter** — an explicit input with no default that a caller must set for a destructive operation to proceed. Specific to the operation (naming the target, count, or scope); a generic boolean is a formality rather than a gate.
- **Cursor** — an opaque continuation token returned with a partial result set, used instead of a numeric offset wherever the underlying set can change between calls.
- **Discriminator parameter** — a `mode`, `action`, or `operation` field whose value changes which other parameters apply. A reliable sign that one tool is several tools sharing a name.
- **Dry run / preview** — a mode returning what an operation *would* do, in the same shape as what it did, without performing it. The mechanism by which blast radius becomes checkable before it becomes irreversible.
- **Evidence gap** — the distance between what a tool actually did and what its caller can legitimately assert, set entirely by the response shape. A success token leaves it maximally wide; the returned resulting state closes it.
- **Idempotency key** — a caller-supplied identifier letting a tool recognize a repeated request as the same logical action and return the original result rather than performing the effect again. Reused across retries, never regenerated per attempt.
- **Prompt (MCP primitive)** — a reusable, parameterized template a caller can invoke. Structures a request; performs no effect of its own.
- **Repeat-safety** — whether calling a tool twice with identical arguments is harmless. A property of the tool, declared at its boundary, not a property of the caller's discipline.
- **Resource (MCP primitive)** — readable material addressed by a stable identifier. Calling it is free: it fills context and changes nothing.
- **Stable reference** — an identifier returned by one call and accepted verbatim by the next. Removes the need for a caller to reconstruct an identity from position or attributes, along with the class of wrong-entity errors that reconstruction produces.
- **Stringly-typed parameter** — an input carrying structure inside a string the tool then parses: a query mini-language, a delimited list, a key-value blob. Converts a schema constraint into a grammar the caller must implement, and turns rejection into misinterpretation.
- **Tool (MCP primitive)** — an operation with an effect on the world. The primitive whose invocation carries consequences a caller must weigh.
- **Tool surface** — the complete set of tools available to an agent for a task. The unit at which selection accuracy is determined, since choosing is a comparison across the set rather than an evaluation of one entry.
- **Verb-object naming** — naming a tool for the effect it has and the thing it has it on (`cancel_subscription`), rather than for a noun, an abbreviation, or the endpoint it wraps.
