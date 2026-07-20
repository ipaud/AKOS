# Engineering Rules — Agent Security Pack

Checkable in an agent's code, its configuration, its tool manifest, its permission grants, or a run trace. A reviewer verifies each against the actual artifact; violations are findings. Rules marked ★ are safety-floor items — they hold in every reasoning profile, including Prototype (AS18).

General web and API rules are not repeated here; see [owasp-top-10](../../security/owasp-top-10/engineering-rules.md) (OW1–OW17) and [owasp-api-top-10](../../security/owasp-api-top-10/README.md). These rules cover only the surface the agent adds.

## Provenance and the data/instruction boundary

- ASE1 ★. Every piece of content entering the agent's context is tagged with a provenance class — `system`, `operator`, `user`, or `untrusted` — assigned by the channel it arrived through, never inferred from what the content says about itself.
- ASE2 ★. Retrieved documents, web page contents, file contents, database rows, email bodies, and tool results are all classified `untrusted` by default, regardless of which internal system served them.
- ASE3 ★. The component that authorizes a tool call consults the provenance class of the content that motivated it, not the content itself; `untrusted` content can never raise an action's authorization level.
- ASE4. Untrusted content is delivered to the model inside an explicit structural wrapper (a distinct message role, a fenced block with a random per-session delimiter, or a typed field) rather than concatenated into the same prose stream as instructions.
- ASE5. The wrapper's delimiter is not guessable from the content itself — a fixed literal marker that appears in the system prompt is reproducible by an attacker who has read it.
- ASE6. Content that claims to be a system instruction, an administrator message, a policy update, or a prior-instruction revocation, and arrives through a non-instruction channel, is logged as a suspected injection and does not alter behavior.
- ASE7. The agent's rules, tool list, permission scopes, and approval thresholds are not modifiable by anything in the conversation or in retrieved content; they are loaded from configuration under change control.
- ASE8. A downgrade is possible but an upgrade is not: an operator instruction may restrict what the agent does with untrusted content; untrusted content may never widen what an operator instruction permitted.
- ASE9. Where retrieval assembles a context from multiple sources, each chunk carries its source identifier into the window, so a reviewer can attribute any acted-on claim to a specific document.

## Indirect prompt injection

- ASE10 ★. Every content source the agent can read is enumerated in the threat model with an owner and a trust classification; a source with no entry is treated as untrusted.
- ASE11 ★. The consequence of a successful injection is bounded by a control outside the model — scoped credentials, an egress allowlist, a sandbox, or an approval gate — and this bound is stated per tool, not assumed globally.
- ASE12. Prompt-level defenses (instructional hardening, delimiters, injection classifiers) are recorded as mitigations that reduce frequency, never as the control that bounds impact.
- ASE13. An injection-detection classifier, where present, fails closed: a flagged input halts the action path and escalates rather than proceeding with a warning appended.
- ASE14. Agent behavior is tested against an indirect-injection corpus that includes instructions hidden in retrieved documents, tool results, file contents, and rendered page text — not only against direct user-typed attempts.
- ASE15. The injection test corpus includes at least one case per tool that would cause a security-relevant action (exfiltration, privilege use, memory write, irreversible action) if obeyed, and the assertion is that the action was *blocked by a control*, not that the model declined.
- ASE16. Content is checked for instruction-shaped text in non-visible channels — HTML comments, zero-width and bidirectional control characters, white-on-white text, image alt text, document metadata, and CSS-hidden nodes — before it enters context.
- ASE17. Where an agent processes content on behalf of one user that another user authored (tickets, comments, shared documents, inbound email), that cross-principal path is called out explicitly in the threat model as the primary injection route.

## Tool and resource integrity

- ASE18 ★. Tool definitions — names, descriptions, and parameter schemas — are pinned to a specific version and integrity-checked (hash or signature) before being loaded into context.
- ASE19 ★. A change to a pinned tool definition halts loading and requires human review before the agent runs with it; silent acceptance of an updated description is not permitted.
- ASE20. The full text of every tool description actually loaded into context is retrievable for review, so a reviewer can read what the model was told rather than what the documentation says.
- ASE21. Tool results are wrapped and provenance-labeled at the transport boundary, before any model sees them, rather than by an instruction telling the model to be careful with them.
- ASE22. Tool results are validated against a declared response schema; fields outside the schema are dropped rather than passed through into context.
- ASE23. A tool result's size is capped, and truncation is explicit — an oversized result cannot push the operator's instructions out of the window.
- ASE24. A server that can add, remove, or redefine tools after the session has started is either disallowed, or its changes trigger the same review gate as an initial load (ASE19).
- ASE25. Tools are namespaced by their providing server in the model's view, so two servers cannot present the same tool name and shadow one another.

## Data exfiltration

- ASE26 ★. Outbound network destinations reachable by the agent or its tools are an explicit allowlist with default-deny at the network layer, not a policy expressed in the prompt.
- ASE27 ★. Agent output rendered in a client does not auto-load remote resources: images, iframes, stylesheets, fonts, and link prefetch from model-generated markup are blocked or proxied through an allowlist.
- ASE28 ★. URLs appearing in agent output are not constructed with context-derived data in query parameters, path segments, or fragments unless the destination is on the egress allowlist and the parameter values are validated.
- ASE29. DNS resolution from the agent's sandbox is restricted to the allowlisted destinations, closing the subdomain-encoding channel.
- ASE30. Every tool that writes to a location a third party can read — a public comment, an issue body, a commit message, a shared document, a webhook payload, an outbound email — is classified as an egress path and gated accordingly.
- ASE31. Error messages, stack traces, and debug output produced by tools are filtered before entering context, so failures do not become a data channel (extends OW8).
- ASE32. Where sensitive data is in context, the run's egress set is narrowed for the remainder of the run rather than evaluated per call against a static global list.
- ASE33. Bulk-read tools have per-run volume caps and rate limits, so a single injected instruction cannot enumerate an entire store.
- ASE34. Any content the agent produces that will be shown to a principal other than the requester passes an explicit review or filtering step before delivery.
- ASE35. Exfiltration attempts are tested directly: the suite includes a case where retrieved content instructs the agent to embed context data in a URL, an image, and a third-party-visible field, and asserts the control blocked each.

## Least privilege and excessive agency

- ASE36 ★. The agent's toolset is the minimum set required by its stated task; a tool that is not needed for the current task class is not loaded.
- ASE37 ★. Every credential the agent holds is scoped to the narrowest resource set and permission level that completes the task — read where read suffices, one table rather than a schema, one repository rather than an organization.
- ASE38 ★. No agent holds a standing administrative, root, or org-wide credential; elevated capability is requested per task, granted for a bounded window, and revoked.
- ASE39. Read and write capabilities are separate tools with separate grants, so an agent that only needs to read cannot be induced to write.
- ASE40. Destructive operations (delete, drop, truncate, force-push, revoke, disable) are excluded from the default toolset and require a distinct, explicitly granted capability.
- ASE41. The agent's permission set is enumerable from configuration — a reviewer can list every action it can take without reading its prompt.
- ASE42. Tool invocation rate and per-run call counts are capped per tool, so an injected loop cannot amplify a single capability into a bulk operation.
- ASE43. Sub-agents and workers inherit a subset of the parent's permissions, never a superset, and the delegation is explicit rather than ambient.
- ASE44. Where an agent handles multiple task classes, permissions are partitioned per class rather than unioned into one profile that serves them all.

## Identity, delegation, and the confused deputy

- ASE45 ★. Every privileged action carries the requesting principal's identity to the resource owner, and authorization is evaluated against that principal's permissions server-side (extends OW1).
- ASE46 ★. The agent's own service identity is never used to authorize an action taken on a user's behalf; a user-scoped token, a delegated credential, or an on-behalf-of assertion is used instead.
- ASE47. The agent cannot act for a principal whose identity was asserted by content it read; principal identity comes from the authenticated session, never from a document or a tool result.
- ASE48. Where an agent serves multiple tenants or users, context, memory, retrieval scope, and credentials are partitioned per principal with no shared cache that crosses the boundary.
- ASE49. An agent-initiated request is distinguishable from a human-initiated one at the receiving service, so downstream policy can treat them differently.
- ASE50. Permission checks fail closed: an authorization service that errors or times out denies the action rather than allowing it.
- ASE51. Requests that would elevate the effective privilege of a run — assuming a role, switching an account, escalating a scope — are outside the agent's autonomous authority and require human approval.

## Memory integrity

- ASE52 ★. Writing to persistent memory is a distinct, gated capability, not a side effect of ordinary tool use.
- ASE53 ★. Every persisted memory record stores its provenance: the source, the session, the principal, and the timestamp of the write.
- ASE54 ★. A fact derived from `untrusted` content is never written to a trusted memory tier without human confirmation; it may be stored only in a session- or task-scoped tier that expires.
- ASE55. Memory records carry an expiry or a review date; no record is trusted indefinitely without re-verification.
- ASE56. Memory is partitioned by principal and by project; a write from one context cannot be read from another that should not see it.
- ASE57. Instructions, rules, permissions, and thresholds are not storable in memory — memory holds facts and preferences, never directives the agent will later obey.
- ASE58. Memory writes and reads are logged with provenance, so a poisoned record can be traced to the session that created it and every later run that used it.

## Output handling

- ASE59 ★. Agent output rendered in a browser is escaped for its rendering context; raw HTML from model output is never inserted into the DOM (extends OW5).
- ASE60 ★. Agent output used in a shell command is passed as an argument array with no shell interpretation, never string-concatenated into a command line (extends OW4).
- ASE61 ★. Agent output used in a database query is parameterized; the model never emits an executable query that is run without validation (extends OW3).
- ASE62. Agent output used as a filesystem path is canonicalized and confirmed to resolve inside an allowed root before any read or write.
- ASE63. Structured output the system depends on is validated against a schema before use; a malformed or unexpected structure is an error, not something to interpret leniently.
- ASE64. Output passed into another agent's context is provenance-labeled `untrusted` on arrival, exactly as an external document would be.

## Human approval

- ASE65 ★. Actions classified irreversible or externally visible require human approval before execution, and the classification is recorded per tool in configuration.
- ASE66 ★. The approval surface renders the concrete resolved action — the exact command, recipients, amounts, and affected records — not the agent's natural-language summary of it.
- ASE67 ★. The approved artifact is the executed artifact: parameters are frozen at approval time, and no re-planning, re-resolution, or regeneration occurs between the approval and the call.
- ASE68. There is no alternative path to a gated action: every route to the underlying capability, including other tools, batch operations, and sub-agents, passes the same gate.
- ASE69. Approval requests cannot be generated in a volume or cadence that produces habitual approval; batching and rate limits are explicit, and a batch approval enumerates every item it covers.
- ASE70. An approval is scoped to one action and does not establish standing consent for later similar actions in the same session unless that scope is explicitly stated and bounded.
- ASE71. Approval decisions — who approved, what exactly, and when — are recorded in the audit log alongside the resulting call.

## Agent and MCP supply chain

- ASE72 ★. Every MCP server, tool package, plugin, and skill in the agent's configuration is pinned to an exact version and a verified publisher; floating versions and latest-tag resolution are not used.
- ASE73 ★. A new server or tool package is reviewed before first use — its code, its declared permissions, its network destinations, and the full text of its tool descriptions.
- ASE74. Updates re-enter review; an automatic update path for anything that contributes prompt content or holds credentials is disallowed.
- ASE75. Server binaries and packages are installed from a verified source with integrity verification, and the resolved identity is recorded (extends OW14).
- ASE76. Each server's declared capabilities are constrained at the host: filesystem roots, network destinations, and credentials are granted per server rather than shared across the agent's whole toolset.
- ASE77. The MCP specification's security expectations — explicit user consent before tool invocation, user control over data exposure, treating tool descriptions as untrusted unless the server is trusted, and human review of model-sampling requests — are implemented as enforced host behavior, not as documentation.
- ASE78. A dependency inventory of servers, tools, and their transitive packages exists and is scanned for known vulnerabilities on the same cadence as application dependencies (extends OW10).

## Secrets in context

- ASE79 ★. Credentials, tokens, and keys are not placed in system prompts, tool descriptions, tool arguments, or any content the model can read; the tool layer resolves a reference into the secret at the call boundary.
- ASE80 ★. Traces, transcripts, and audit records redact secret-shaped values, and the redaction is applied at write time rather than at display time.
- ASE81. Tool results are scanned for credential patterns before entering context, and matches are redacted with a marker rather than passed through.
- ASE82. Where a secret must transit context, it is short-lived, single-purpose, and revocable, and its exposure is recorded as an accepted risk with a rotation trigger.
- ASE83. Environment variables, credential files, and cloud metadata endpoints are unreachable from the agent's sandbox unless explicitly granted (extends OW17).
- ASE84. A confirmed injection reaching a context that held a secret triggers rotation of that secret as an incident step, not as a discretionary follow-up.

## Sandboxing and containment

- ASE85 ★. Code execution, file operations, and shell access run inside a sandbox with an explicit filesystem root, an explicit egress allowlist, and no ambient host credentials.
- ASE86 ★. Every control is enforced by a named component outside the model — a proxy, a policy engine, a container boundary, a scoped token — and the enforcing component is identified per control in the design.
- ASE87. Shell commands, SQL operations, and file paths are allowlisted with default-deny; blocklist-style filtering is not used as the primary control (AS15).
- ASE88. Resource limits — CPU, memory, disk, wall clock, and spend — are set on the sandbox so a runaway or induced loop is contained.
- ASE89. Sandbox escapes and denied operations are logged and surfaced as security events rather than retried silently.

## Audit logging

- ASE90 ★. Every tool call is logged with the tool name, the resolved arguments, a result summary, the timestamp, the run identifier, and the principal acted for.
- ASE91 ★. Audit records are written to a store the agent cannot modify or delete, with retention set deliberately.
- ASE92. Each logged action records the provenance of the content that motivated it, so an action traceable to untrusted input is identifiable after the fact.
- ASE93. Denied actions — blocked egress, refused tool calls, failed authorization, rejected approvals — are logged as prominently as successful ones; a control that fires silently cannot be shown to work.
- ASE94. Logs are sufficient to reconstruct a run end to end without re-execution, including sub-agent runs linked to their parent.
- ASE95. Security-relevant events (suspected injection, blocked exfiltration, privilege denial, memory-write rejection, approval denial) raise alerts rather than only appearing in a log nobody reads (extends OW16).
