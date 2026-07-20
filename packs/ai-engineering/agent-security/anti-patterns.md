# Anti-Patterns — Agent Security Pack

Named failure modes. Detection cue → why it fails → fix. Every entry here is a security defect; the ones that put data outside the system, take an irreversible action without authority, or execute untrusted content are safety-floor violations and block in every reasoning profile (AS18).

## The obedient document

**Detect:** an agent that reads external content — tickets, pages, PDFs, emails, repository files — and whose behavior can be changed by a sentence inside that content. Nobody hostile ever touched the interface.
**Why it fails:** the operator asked an ordinary question and the agent read the document because that was the task. The attacker's instruction arrives inside the operator's own trusted workflow. Direct injection is bounded by what the typing user could already do; this is bounded by nothing except the agent's permission set.
**Fix:** provenance labels assigned by channel, checked at the action gate, with the consequence of obedience bounded by a control outside the model (AS1, AS2, ASE1–ASE3, ASE11).

## The delimiter that was the whole defense

**Detect:** untrusted content wrapped in tags or fences, with a system-prompt line instructing the model to treat everything inside as data — and no other control on the path to a consequential action.
**Why it fails:** the boundary is adjudicated by the same process the attacker is manipulating, and a fixed marker written in the system prompt is reproducible by anyone who has induced the model to reveal it. It reduces attack frequency, which is worth having, and bounds nothing.
**Fix:** keep the wrapper, use an unguessable per-session delimiter, and record it in the mitigations column. Put a control — scope, sandbox, allowlist, gate — on the path behind it (AS3, ASE4, ASE5, ASE12).

## The helpful markdown image

**Detect:** an agent whose output is rendered in a client that loads remote resources, with any sensitive material in context. The exfiltration is a single image reference whose URL carries the data in a query parameter; nothing in the trace looks like a network call by the agent.
**Why it fails:** the agent never "sent" anything. The client's renderer made the request, dutifully, on behalf of markup the model produced. Every part of the system behaved as designed.
**Fix:** block or proxy remote resource loading from model-generated markup, keep context-derived data out of URLs entirely, and enforce a destination allowlist at the network layer (AS8, ASE27, ASE28).

## The three ingredients nobody counted

**Detect:** a run that holds sensitive data because the task needs it, reads untrusted content because the task needs that too, and has some reachable path by which bytes leave — a public comment, an outbound webhook, a shared document, an arbitrary host.
**Why it fails:** the triangle assembles from three reasonable decisions made by different people at different times. Each is defensible alone. Together they are a live vulnerability, and the third ingredient is the one nobody classified as egress.
**Fix:** enumerate egress honestly — every path by which context bytes become bytes someone else observes — and narrow the permitted set for any run holding sensitive data (AS8, ASE30, ASE32).

## The god-mode token

**Detect:** an agent configured with an admin key, an org-wide token, or a broad service account, because scoping it per task was fiddly and the agent "might need it."
**Why it fails:** a successful injection transfers the whole permission set to whoever wrote the text the agent read. Convenience at configuration time is the exact quantity being converted into blast radius, and the conversion rate is one to one.
**Fix:** narrowest scope that completes the task, read and write and destroy as separate grants, elevated capability requested per task and revoked after (AS4, AS5, ASE36–ASE40).

## The agent that is everyone

**Detect:** a privileged action performed for a user, authorized against the agent's service identity rather than the user's. The logs show a trusted service doing something it is allowed to do.
**Why it fails:** it is the confused deputy, and the reason it survives review is that nothing is bypassed — every check passes. An unprivileged requester (sometimes a document, which has no permissions at all) gets a privileged action performed on their behalf.
**Fix:** carry the requesting principal's identity to the resource owner and authorize against that principal server-side; the agent's own identity authorizes its housekeeping and nothing else (AS6, ASE45–ASE47).

## The tool that changed its mind

**Detect:** a tool or MCP server installed from a floating version, whose descriptions are re-fetched at session start and accepted silently. The reviewed version and the running version are not the same artifact.
**Why it fails:** tool descriptions are prompt content. An update rewrote the system prompt without touching the repository, with no diff, no review, and no signal — and part of the payload is natural language aimed at the model's judgment.
**Fix:** pin to exact versions and publishers, integrity-check definitions before load, and treat any change as a system-prompt change requiring human review (AS7, AS12, ASE18, ASE19, ASE72–ASE74).

## The payload wearing a result

**Detect:** tool responses passed into context as raw text, containing fields the schema never declared — often a long "note" or "system_message" explaining that the prior instructions no longer apply.
**Why it fails:** the transport boundary is where labeling has to happen, and here nothing happened at all. By the time the model sees the result it is indistinguishable from any other text in the window.
**Fix:** validate results against a declared schema, drop undeclared fields, cap size, and wrap with a provenance label before the model sees anything (AS7, ASE21–ASE23).

## The rubber stamp

**Detect:** an approval screen showing the agent's own summary — "Send the requested email", "Apply the configuration change" — rather than the resolved action. Or an approval fired so often that clicking yes is reflex. Or parameters regenerated between the click and the call.
**Why it fails:** the human is ratifying a description written by the component under attack. All three variants produce the appearance of oversight with none of the substance, and the third is a straightforward time-of-check-to-time-of-use gap.
**Fix:** render the exact command, recipients, amounts, and records; freeze parameters at approval; one approval per action; reclassify the routine cases rather than removing the gate (AS11, ASE66, ASE67, ASE69, ASE70).

## The back door around the gate

**Detect:** a capability gated on its primary tool and reachable ungated through a second tool, a batch endpoint, a sub-agent, or a lower-level API the agent also holds.
**Why it fails:** a gate covering one route is a gate covering no routes. The reviewer checked the tool with the gate on it, which is the one designed to be checked.
**Fix:** enumerate every route to the underlying capability and confirm each passes the same gate; make the gate a property of the capability, not of one tool (ASE68).

## The sleeper fact

**Detect:** an agent that writes what it learns to persistent memory, storing the claim and not its origin, with no expiry — including claims read out of documents.
**Why it fails:** the poisoned record is read in later sessions by different users on different tasks, carrying no trace of where it came from. Reasoning built on it looks independently derived. Verification against the record confirms it, because the record is what was poisoned.
**Fix:** gate the write, store provenance with every record, keep untrusted-derived facts in session or task scope until a human promotes them, and give every record an expiry (AS10, ASE52–ASE55, ASE58).

## The rule that came from a document

**Detect:** memory or context that can hold directives — thresholds, permissions, policies, "the user prefers that you skip confirmation" — rather than only facts.
**Why it fails:** any rule an agent will later obey is a rule an attacker can write, and writing it once buys obedience in every future session. It converts memory poisoning into permanent privilege escalation.
**Fix:** rules, tools, scopes, and thresholds load from configuration under change control and are not modifiable from the conversation or from memory (ASE7, ASE57).

## The trusted echo

**Detect:** agent output rendered as HTML, executed as a shell command, interpolated into SQL, used as a filesystem path, or piped into another agent — without the validation the same bytes would get from an anonymous user.
**Why it fails:** the output is generated text, partly derived from content an attacker may have written. Trusting it because it came from your own model is trusting a string for its origin rather than validating it for its destination — the exact mistake application security spent thirty years unlearning.
**Fix:** contextual escaping, argument arrays, parameterized queries, canonicalized paths, schema validation, and an `untrusted` label when it enters another agent (AS9, ASE59–ASE64, and OW3–OW5 in [owasp-top-10](../../security/owasp-top-10/engineering-rules.md)).

## The secret in the system prompt

**Detect:** an API key, token, or connection string placed in the system prompt or a tool description so the agent "has what it needs," or appearing unredacted in traces.
**Why it fails:** anything in the window can be echoed into an answer, captured in a trace, carried into a summary, sent to a provider, and extracted by an injection that simply asks. The model does not know which of its tokens are dangerous.
**Fix:** the agent holds a reference and the tool layer resolves it at the call boundary; redact at write time; block credential files and metadata endpoints from the sandbox; rotate on any confirmed injection (AS13, ASE79–ASE84).

## The sandbox with a network card

**Detect:** code execution isolated from the host filesystem, with unrestricted outbound network access — or a container with the host's environment variables and cloud credentials still visible inside it.
**Why it fails:** containment that stops one class of harm and leaves the egress path open is the third ingredient of the triangle, installed deliberately. Filesystem isolation without network isolation protects the host and not the data.
**Fix:** explicit filesystem root, explicit egress allowlist with default-deny, no ambient host credentials, restricted DNS, and resource limits (AS14, ASE29, ASE83, ASE85, ASE88).

## The blocklist of bad commands

**Detect:** a filter that rejects known-dangerous shell commands, known-bad domains, or suspicious-looking phrasings, standing as the primary control.
**Why it fails:** the input is generated text with unlimited variants, so the blocklist is a list of the defender's imagination, checked against an attacker's. It fails on the first form nobody thought of and reports success until then.
**Fix:** allowlist with default-deny on commands, destinations, paths, and operations, with rejections logged (AS15, ASE87, ASE93).

## The test suite that only types

**Detect:** injection testing consisting of user-typed attempts ("ignore your instructions"), with the assertion being that the agent refused.
**Why it fails:** it tests the bounded form of the attack and skips the dangerous one entirely, and it asserts on a model behavior rather than a control. It will pass right up until a model update changes the refusal rate, and it never demonstrated a bound in the first place.
**Fix:** an indirect corpus with instructions hidden in retrieved documents, tool results, file contents, and non-visible channels; one case per harmful tool; assertions that a *control* blocked the action, re-run on every model, prompt, and tool-definition change (ASE14–ASE16).

## The silent agent

**Detect:** an agent logging only its final answers — no tool names, no resolved arguments, no principal, no provenance for the content that motivated each call, no record of denied actions.
**Why it fails:** after a suspected compromise the incident cannot be scoped, the moved data cannot be identified, and the fix cannot be verified. Every other rule in this pack becomes unenforceable, and controls that fired silently cannot be shown to have fired at all.
**Fix:** log tool name, resolved arguments, result summary, principal, and motivating provenance to a store the agent cannot modify; log denials as prominently as successes; alert on security-relevant events (AS17, ASE90–ASE95).

## "It's only a prototype"

**Detect:** an experimental agent with a broad token, no sandbox, no egress restriction, and no gate, justified by the profile.
**Why it fails:** the profile scales ceremony, not the floor. Prototype credentials are real credentials, prototype agents reach real systems, and prototypes become production by having worked. The controls omitted here are precisely the ones nobody retrofits.
**Fix:** the floor holds in every profile; what a lower profile buys is less documentation and process, never a missing sandbox, allowlist, gate, or log (AS18, [core/constitution.md](../../../core/constitution.md) Article 2).
