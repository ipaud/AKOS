# Heuristics — Agent Security Pack

Fast defaults with known exceptions. Try these first; deviate with a recorded reason. Nothing here overrides a ★ rule in [engineering-rules.md](engineering-rules.md).

## Deciding what to trust

- **If you did not write it and you cannot revert it, it is untrusted.** Ownership of the system that served the content is not ownership of the content. Your ticketing system is yours; the tickets were written by strangers.
- **Provenance travels with the bytes, not with the pipeline.** A document that becomes a summary that becomes a memory record is still attacker-influenced three hops later.
- **Assume the hostile text is in the part nobody reads.** Page footers, HTML comments, alt text, document metadata, the eleventh row of a CSV, the third page of a PDF.
- **A tool result is a document.** It arrived over a network from a system you do not fully control, and it deserves the same suspicion as a scraped web page.
- **Content asserting its own authority is the signal.** Nothing legitimate needs to tell the agent that prior instructions are revoked.

## Bounding the damage

- **Ask "if it obeyed, what then?" before asking "would it obey?"** The first question has an answer you can engineer.
- **Name the enforcing component for every control.** If the answer is "the prompt," write it in the mitigations column and keep looking.
- **The default toolset is the smallest one that completes the common case.** Rare capabilities are requested, not resident.
- **Split read from write, and write from destroy.** Three grants, three decisions; an agent induced to read cannot thereby be induced to delete.
- **Prefer a narrow tool to a general one with a policy.** A `get_order_status(order_id)` beats a `run_query(sql)` guarded by instructions, every time.
- **If removing a capability would only be inconvenient, remove it.** Inconvenience is the cheapest thing you will trade in this whole pack.

## Egress

- **Enumerate egress before anything else; the list is always longer than the first guess.** Network calls, rendered markup, written files, third-party-visible fields, log sinks, error strings.
- **Treat a rendered image as an outbound request, because it is one.** Same for iframes, stylesheets, fonts, and link prefetch.
- **Never let context data reach a URL parameter.** Not in a link, not in an image source, not in a redirect.
- **Default-deny at the network layer, not in the prompt.** A proxy with an allowlist is a control; an instruction not to call external hosts is not.
- **When sensitive data enters context, narrow egress for the rest of the run.** The safest moment to tighten is the moment the third ingredient of the triangle would matter.
- **Watch the "helpful" write paths.** Posting a comment, filing an issue, sending a summary email — these leave the building and rarely get classified as egress.

## Permissions and identity

- **Check the requester's permissions, never the agent's.** The agent's identity authorizes its own housekeeping and nothing more.
- **A document is not a principal.** Identity comes from the authenticated session; anything else is content.
- **Sub-agents get a subset, never a superset.** Delegation is explicit and downward.
- **Fail closed on every security check.** An authorization service that times out denies.
- **Partition per tenant and per user at every layer that caches:** context, retrieval scope, memory, credentials.
- **A standing admin credential on an agent is a finding on its own,** independent of anything else in the review.

## Memory

- **Gate the write, not the read.** Reads are cheap to get wrong once; writes are expensive forever.
- **Store where a fact came from, or do not store it.** Provenance-free memory has no recovery path.
- **Untrusted content earns session scope at most.** Promotion to a durable tier is a human decision.
- **Memory holds facts, never directives.** A rule that can be written into memory is a rule an attacker can write.
- **Give every record an expiry.** Indefinite trust in an unverified claim is the sleeper fact's habitat.

## Human approval

- **Show the resolved action, never the summary of it.** The exact command, the exact recipient, the exact amount.
- **Freeze the parameters at approval time.** Anything regenerated after the click was not approved.
- **One approval, one action.** Standing consent for "similar" actions is how a gate becomes decoration.
- **If it fires on every run, the boundary is wrong — but widen it deliberately, not by removing the gate.** Reclassify the routine actions; keep the gate on the irreversible ones.
- **Check for the back door.** A gated capability reachable through a second tool, a batch endpoint, or a sub-agent is not gated.

## Tools and supply chain

- **Read the tool descriptions as if they were the system prompt.** They are.
- **Pin everything, and treat an update as a code review.** Floating versions on a component that contributes prompt content is a remote code path.
- **A server that redefines its own tools mid-session is disallowed until proven otherwise.**
- **Grant filesystem roots and network destinations per server,** not once for the whole agent.
- **Namespace tools by server.** Name collisions are a shadowing attack waiting for a coincidence.
- **Prefer fewer servers.** Every additional one is prompt content, code, and credentials at once.

## Secrets

- **The agent holds a handle; the tool layer holds the secret.** Resolution happens at the call boundary, outside the model's view.
- **Redact at write time, not at display time.** A trace written unredacted is already a disclosure.
- **Scan tool results for credential shapes before they enter context.** Other systems leak into their own responses.
- **Block the metadata endpoint and the credential files from the sandbox by default.**
- **A confirmed injection into a context that held a secret means rotation.** Not a follow-up item.

## Output handling

- **Model output is anonymous internet input.** Escape it, parameterize it, canonicalize it, validate it against a schema.
- **Never render model-generated HTML.** Markdown with a strict allowlist, rendered by something that does not fetch remote resources.
- **Never build a shell command by concatenation from model output.** Argument arrays only.
- **Validate structure before acting on it;** leniency toward malformed output is where injected structure gets in.

## Threat modeling and testing

- **Test the indirect form, not the direct one.** Hostile instructions in retrieved documents, tool results, and file contents — a suite that only tests typed attempts tests the easy case.
- **Assert that a control blocked it, never that the model declined.** "The agent refused" is a passing test that will fail silently after the next model update.
- **Write one injection test per tool that would cause real harm if obeyed.**
- **Red-team the egress paths specifically:** try to get context data into a URL, an image, and a third-party-visible field.
- **Re-run the suite on every model, prompt, and tool-definition change.** All three change behavior, and only one of them looks like a deploy.
