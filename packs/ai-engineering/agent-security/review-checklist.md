# Review Checklist — Agent Security Pack

Binary checks, ordered by severity. Each unchecked box is a finding at the listed severity. Checks marked ★ are safety-floor items and block in **every** reasoning profile including Prototype, per AS18 and [core/constitution.md](../../../core/constitution.md) Article 2.

Reviewing an agent's security means reading the tool manifest, the permission grants, the sandbox configuration, and at least one real run trace — not the prompt alone. Several checks require the trace or the configuration; those say so.

This checklist covers only the surface the agent adds. Run [owasp-top-10](../../security/owasp-top-10/review-checklist.md) and [owasp-api-top-10](../../security/owasp-api-top-10/README.md) against the underlying application in the same review.

## Critical ★ (blocks in every profile)

- [ ] ★ **Config check:** every content source is classified by channel, and retrieved documents, files, DB rows, email, and tool results are all `untrusted` by default. (ASE1, ASE2)
- [ ] ★ Untrusted content cannot authorize an action, widen a scope, or change a rule; the action gate consults provenance, not content. (ASE3)
- [ ] ★ The agent's rules, toolset, scopes, and approval thresholds are loaded from change-controlled configuration and are not modifiable from the conversation, from retrieved content, or from memory. (ASE7, ASE57)
- [ ] ★ Every path to a consequential action is bounded by a control enforced **outside the model** — scoped credential, sandbox, egress allowlist, or approval gate — and the enforcing component is named per path. (ASE11, ASE86)
- [ ] ★ Outbound network destinations are an allowlist with default-deny at the network layer, not a policy stated in the prompt. (ASE26)
- [ ] ★ Model-generated markup does not auto-load remote resources in any client that renders it. (ASE27)
- [ ] ★ Context-derived data never reaches a URL parameter, path segment, or fragment. (ASE28)
- [ ] ★ No standing administrative, root, or org-wide credential is held by the agent. (ASE38)
- [ ] ★ Every credential is scoped to the narrowest resource set and permission level the task requires. (ASE37)
- [ ] ★ The agent's toolset is the minimum for its task class; unneeded tools are not loaded. (ASE36)
- [ ] ★ Privileged actions carry the requesting principal's identity and are authorized against **that principal's** permissions, server-side, by the resource owner. (ASE45, ASE46)
- [ ] ★ The agent's own service identity is never used to authorize an action taken on a user's behalf. (ASE46)
- [ ] ★ Writing to persistent memory is a distinct gated capability, and facts derived from untrusted content are never promoted to a trusted tier without human confirmation. (ASE52, ASE54)
- [ ] ★ Every memory record stores its provenance — source, session, principal, timestamp. (ASE53)
- [ ] ★ Agent output is escaped, parameterized, or passed as an argument array before it is rendered, queried, or executed. (ASE59–ASE61)
- [ ] ★ Irreversible and externally visible actions require human approval, classified per tool in configuration. (ASE65)
- [ ] ★ The approval surface renders the concrete resolved action, not the agent's summary of it. (ASE66)
- [ ] ★ The approved artifact is the executed artifact; no re-planning or parameter regeneration between approval and call. (ASE67)
- [ ] ★ Every MCP server, tool package, plugin, and skill is pinned to an exact version and verified publisher. (ASE72)
- [ ] ★ Tool definitions are integrity-checked before load, and a change halts loading for human review. (ASE18, ASE19)
- [ ] ★ A new server or tool package is reviewed before first use, including the full text of its tool descriptions. (ASE73)
- [ ] ★ No credential, token, or key appears in a system prompt, tool description, tool argument, or anything else the model can read. (ASE79)
- [ ] ★ Traces and audit records redact secret-shaped values at write time. (ASE80)
- [ ] ★ Code execution, file operations, and shell access run in a sandbox with an explicit filesystem root, an egress allowlist, and no ambient host credentials. (ASE85)
- [ ] ★ **Trace check:** every tool call is logged with tool name, resolved arguments, result summary, timestamp, run ID, and the principal acted for. (ASE90)
- [ ] ★ Audit records are written to a store the agent cannot modify or delete. (ASE91)

## High

- [ ] Every content source the agent can read is enumerated in a threat model with an owner and a trust classification. (ASE10)
- [ ] Untrusted content is delivered inside an explicit structural wrapper with an unguessable per-session delimiter. (ASE4, ASE5)
- [ ] Prompt-level defenses are recorded as mitigations, never as the control bounding impact. (ASE12)
- [ ] Behavior is tested against an **indirect** injection corpus — hidden instructions in retrieved documents, tool results, and file contents. (ASE14)
- [ ] Each injection test asserts that a control blocked the action, not that the model declined. (ASE15)
- [ ] Content is checked for instruction-shaped text in non-visible channels — HTML comments, zero-width and bidirectional characters, alt text, metadata, hidden nodes. (ASE16)
- [ ] Tool results are wrapped and provenance-labeled at the transport boundary, before the model sees them. (ASE21)
- [ ] Tool results are schema-validated; undeclared fields are dropped and size is capped. (ASE22, ASE23)
- [ ] Every tool writing to a third-party-readable location is classified as an egress path and gated. (ASE30)
- [ ] Read, write, and destructive capabilities are separate grants. (ASE39, ASE40)
- [ ] Destructive operations are excluded from the default toolset. (ASE40)
- [ ] Principal identity comes from the authenticated session, never from a document or tool result. (ASE47)
- [ ] Permission checks fail closed on error or timeout. (ASE50)
- [ ] Multi-tenant context, retrieval scope, memory, and credentials are partitioned per principal with no crossing cache. (ASE48, ASE56)
- [ ] Every route to a gated capability — other tools, batch endpoints, sub-agents — passes the same gate. (ASE68)
- [ ] Updates to servers and tool packages re-enter review; no automatic update path exists for anything contributing prompt content or holding credentials. (ASE74)
- [ ] The MCP specification's security expectations — explicit consent before tool invocation, user control over data exposure, untrusted-by-default tool descriptions, human review of sampling requests — are enforced by the host, not documented. (ASE77)
- [ ] Environment variables, credential files, and cloud metadata endpoints are unreachable from the sandbox unless explicitly granted. (ASE83)
- [ ] Shell commands, SQL operations, and file paths are allowlisted with default-deny; blocklisting is not the primary control. (ASE87)
- [ ] Denied actions — blocked egress, refused calls, failed authorization, rejected approvals — are logged as prominently as successes. (ASE93)
- [ ] Security-relevant events raise alerts rather than only appearing in a log. (ASE95)

## Medium

- [ ] Retrieved chunks carry their source identifier into context, so an acted-on claim is attributable to a document. (ASE9)
- [ ] Content claiming to be a system instruction or a prior-instruction revocation, arriving through a non-instruction channel, is logged as suspected injection and changes nothing. (ASE6)
- [ ] An injection classifier, where present, fails closed. (ASE13)
- [ ] Cross-principal content paths (tickets, comments, shared docs, inbound email) are called out in the threat model as the primary injection route. (ASE17)
- [ ] The full text of every loaded tool description is retrievable for review. (ASE20)
- [ ] A server that redefines tools mid-session is disallowed, or its changes trigger the load-time review gate. (ASE24)
- [ ] Tools are namespaced by providing server so names cannot shadow. (ASE25)
- [ ] DNS resolution from the sandbox is restricted to allowlisted destinations. (ASE29)
- [ ] Tool error messages and stack traces are filtered before entering context. (ASE31)
- [ ] Egress is narrowed for the remainder of a run once sensitive data enters context. (ASE32)
- [ ] Bulk-read tools have per-run volume caps and rate limits. (ASE33)
- [ ] Tool invocation rate and per-run call counts are capped per tool. (ASE42)
- [ ] Sub-agents inherit a subset of the parent's permissions, explicitly delegated. (ASE43)
- [ ] Permissions are partitioned per task class rather than unioned into one profile. (ASE44)
- [ ] Agent-initiated requests are distinguishable from human-initiated ones at the receiving service. (ASE49)
- [ ] Privilege-elevating requests (role assumption, account switch, scope escalation) require human approval. (ASE51)
- [ ] Memory records carry an expiry or review date. (ASE55)
- [ ] Memory writes and reads are logged with provenance. (ASE58)
- [ ] Model output used as a filesystem path is canonicalized and confirmed inside an allowed root. (ASE62)
- [ ] Structured output is schema-validated before use; malformed structure is an error, not something to interpret leniently. (ASE63)
- [ ] Output entering another agent's context is labeled `untrusted` on arrival. (ASE64)
- [ ] Approval volume and cadence are bounded; a batch approval enumerates every item it covers. (ASE69)
- [ ] An approval does not establish standing consent for later actions unless explicitly scoped and bounded. (ASE70)
- [ ] Approval decisions are recorded alongside the resulting call. (ASE71)
- [ ] Filesystem roots, network destinations, and credentials are granted per server rather than shared agent-wide. (ASE76)
- [ ] Tool results are scanned for credential patterns before entering context. (ASE81)
- [ ] Sandbox resource limits — CPU, memory, disk, wall clock, spend — are set. (ASE88)
- [ ] Each logged action records the provenance of the content that motivated it. (ASE92)
- [ ] Logs are sufficient to reconstruct a run end to end, with sub-agent runs linked to their parent. (ASE94)

## Low

- [ ] Downgrade-only enforcement is explicit: operator instructions may restrict handling of untrusted content, untrusted content may never widen it. (ASE8)
- [ ] Server binaries and packages are installed from a verified source with integrity verification, and the resolved identity is recorded. (ASE75)
- [ ] A dependency inventory of servers, tools, and transitive packages is scanned on the application cadence. (ASE78)
- [ ] A secret that must transit context is short-lived, single-purpose, revocable, and recorded as an accepted risk with a rotation trigger. (ASE82)
- [ ] Sandbox escapes and denied operations surface as security events rather than being retried silently. (ASE89)
- [ ] Content the agent produces for a principal other than the requester passes a review or filtering step. (ASE34)

## Process

- [ ] The review inspected the tool manifest, the permission grants, the sandbox configuration, and at least one real run trace — not the prompt alone.
- [ ] The reviewer enumerated the agent's full permission set from configuration and stated it as the worst case of a successful injection. (AS4)
- [ ] The three ingredients of the exfiltration triangle were checked for co-occurrence in a single run: sensitive data, untrusted content, reachable egress. (AS8)
- [ ] Exfiltration was tested directly — an attempt to place context data in a URL, an image, and a third-party-visible field — with the assertion that a control blocked each. (ASE35)
- [ ] The injection suite was re-run against the current model, prompt, and tool definitions; all three change behavior. (ASE14)
- [ ] Every defense in the design was sorted into control or mitigation, with the enforcing component named. An empty control column on any consequential path is a CRITICAL finding regardless of how many mitigations are present. (AS3, AS14)
- [ ] For each finding, the review names the specific control and its enforcing component — never "harden the prompt."
