# Scoring Rubric — Agent Security Pack

Standalone 0–100 score for the security of a system where a language model plans, calls tools, and acts. Feeds [scoring/security-score.md](../../../scoring/security-score.md) alongside [owasp-top-10](../../security/owasp-top-10/scoring-rubric.md) and [owasp-api-top-10](../../security/owasp-api-top-10/README.md); those score the underlying application, this one scores the surface the agent adds. A system with a clean OWASP Top 10 pass and an unbounded agent has not been reviewed.

Score = 100 − deductions, floor 0. Bands per [core/scoring-model.md](../../../core/scoring-model.md).

This is a Level 1 safety-floor dimension. Per AS18 and [core/constitution.md](../../../core/constitution.md) Article 2, the reasoning profile scales the ceremony around these controls — the threat-model document, the review cadence, the sign-off — never whether the controls exist. A Prototype profile does not raise the score of an agent with a standing admin credential.

Three classes of finding are graded as breaches rather than as hardening gaps: **data leaving the system through a channel the agent could reach**, **an irreversible or externally visible action taken without authority**, and **untrusted content executing, rendering, or being written to durable memory as trusted**. All three change the state of the world outside the system.

## Deductions

| Finding | Deduction |
|---------|-----------|
| A path exists where untrusted content reaches a consequential action with no control outside the model — only prompt hardening, delimiters, or a classifier (AS3, ASE11) | −30 (CRITICAL) |
| Sensitive data, untrusted content, and a reachable uncontrolled egress path co-occur in one run — the complete triangle (AS8, ASE26, ASE32) | −30 (CRITICAL) |
| Context-derived data can reach a URL parameter, or model-generated markup auto-loads remote resources in a client (ASE27, ASE28) | −25 (CRITICAL) |
| A privileged action is authorized against the agent's service identity rather than the requesting principal's permissions (ASE45, ASE46) | −25 (CRITICAL) |
| An irreversible or externally visible action executes without a human approval gate (ASE65) | −25 (CRITICAL) |
| Untrusted content can write to a durable memory tier, or memory can hold directives (ASE54, ASE57) | −25 (CRITICAL) |
| Agent output is rendered as HTML, executed as a shell command, or interpolated into a query without validation (ASE59–ASE61) | −25 (CRITICAL) |
| The agent holds a standing administrative, root, or org-wide credential (ASE38) | −25 (CRITICAL) |
| A credential appears in a system prompt, tool description, tool argument, or unredacted trace (ASE79, ASE80) | −25 (CRITICAL) |
| Code, shell, or file operations run without a sandbox, or the sandbox has ambient host credentials (ASE85) | −25 (CRITICAL) |
| Servers or tool packages are unpinned, or definitions are not integrity-checked before load (ASE18, ASE72) | −20 (CRITICAL) |
| The approval surface shows the agent's summary rather than the resolved action, or parameters are regenerated after approval (ASE66, ASE67) | −20 (CRITICAL) |
| A gated capability is reachable ungated through a second tool, batch endpoint, or sub-agent (ASE68) | −20 (CRITICAL) |
| No content provenance labeling exists; trust is inferred from what content says (ASE1–ASE3) | −15 (HIGH) |
| Credentials are broader than the task requires, or read/write/destructive are one grant (ASE37, ASE39, ASE40) | −15 (HIGH) |
| Tools unnecessary for the task class are loaded by default (ASE36) | −10 (HIGH) |
| No indirect-injection test corpus, or the suite asserts on model refusal rather than on a control (ASE14, ASE15) | −12 (HIGH) |
| No tool-call audit log, or logs are writable by the agent (ASE90, ASE91) | −12 (HIGH) |
| Egress is controlled by a blocklist rather than a default-deny allowlist (ASE26, ASE87) | −12 (HIGH) |
| Tool results enter context unwrapped and unlabeled, or unvalidated against a schema (ASE21, ASE22) | −10 (HIGH) |
| Memory records store no provenance (ASE53) | −10 (HIGH) |
| A security check fails open on error or timeout (ASE50) | −10 (HIGH) |
| No threat model enumerating content sources with owners and trust classes (ASE10) | −8 (HIGH) |
| Multi-tenant context, memory, retrieval scope, or credentials are not partitioned per principal (ASE48, ASE56) | −10 (HIGH) |
| Server or package updates apply without re-review (ASE74) | −8 (HIGH) |
| Metadata endpoints or credential files are reachable from the sandbox (ASE83) | −8 (HIGH) |
| Principal identity can be taken from a document or tool result (ASE47) | −8 (HIGH) |
| Non-visible channels (HTML comments, zero-width characters, alt text, metadata) are not checked before content enters context (ASE16) | −6 (MEDIUM) |
| Bulk-read tools or per-tool call counts are uncapped (ASE33, ASE42) | −6 each, cap −12 (MEDIUM) |
| Sub-agents inherit permissions not explicitly scoped as a subset (ASE43) | −6 (MEDIUM) |
| Memory records carry no expiry or review date (ASE55) | −5 (MEDIUM) |
| Denied actions are not logged, or security events raise no alert (ASE93, ASE95) | −5 each, cap −10 (MEDIUM) |
| Model output used as a filesystem path is not canonicalized against an allowed root (ASE62) | −5 (MEDIUM) |
| Structured output is used without schema validation (ASE63) | −5 (MEDIUM) |
| Egress is not narrowed for the remainder of a run once sensitive data enters context (ASE32) | −5 (MEDIUM) |
| Tool error output and stack traces enter context unfiltered (ASE31) | −4 (MEDIUM) |
| Approval volume produces habitual approval, or an approval establishes unbounded standing consent (ASE69, ASE70) | −4 each, cap −8 (MEDIUM) |
| A server can redefine its tools mid-session without re-triggering review (ASE24) | −4 (MEDIUM) |
| Filesystem roots, destinations, and credentials are shared agent-wide rather than granted per server (ASE76) | −4 (MEDIUM) |
| Sandbox resource limits are unset (ASE88) | −4 (MEDIUM) |
| Prompt-level defenses are recorded as controls rather than mitigations (ASE12) | −4 (MEDIUM) |
| Retrieved chunks carry no source identifier into context (ASE9) | −3 (LOW) |
| Tools are not namespaced by providing server (ASE25) | −2 (LOW) |
| An injection classifier fails open (ASE13) | −3 (LOW) |
| Loaded tool descriptions are not retrievable in full for review (ASE20) | −2 (LOW) |
| No dependency inventory of servers and their transitive packages (ASE78) | −2 (LOW) |
| Agent-initiated requests are indistinguishable from human-initiated ones downstream (ASE49) | −2 (LOW) |

## Hard caps

- **Any open CRITICAL finding: score ≤ 59 (BLOCKED), in every reasoning profile.** An agent that can leak data, act irreversibly without authority, or execute untrusted content fails this dimension regardless of how well everything else is built. Prototype does not lift this cap.
- No control outside the model on any path to a consequential action — a design defended entirely by mitigations: **cap 49**. There is no floor to measure.
- No sandbox on code, shell, or file execution: **cap 59**.
- No tool-call audit log: **cap 69**. Every other rule here is unenforceable and no incident is reconstructable.
- No indirect-injection testing at all: **cap 74**. The controls may be present; nothing demonstrates they hold.
- Credentials broader than the task requires, with no compensating control: **cap 79**. This is the multiplier on every other finding.
- A fix applied to one instance rather than at the boundary (one URL filtered, one tool gated, one path escaped): **no credit** — score the class, not the instance.

## Modifiers

- The indirect-injection suite has a case per harmful tool, each asserting against a named enforcing component (ASE15): **+5**.
- Exfiltration is tested directly — context data into a URL, a rendered image, and a third-party-visible field, each blocked by a control (ASE35): **+4**.
- The agent's full permission set is enumerable from configuration without reading its prompt, and is recorded in the review as the stated worst case (ASE41, AS4): **+4**.
- Every defense in the design is sorted into control or mitigation with its enforcing component named (AS3, AS14): **+3**.
- Every memory record carries provenance and an expiry, and promotion from untrusted-derived to durable requires human confirmation (ASE53–ASE55): **+3**.
- The injection suite re-runs on model, prompt, and tool-definition changes alike (ASE14): **+3** (cap 100).
- Repeat finding from a previous review, unfixed without a recorded tradeoff: **double its deduction**.

## Interpretation anchors

- **95** — provenance is labeled by channel and checked at the actuator; every consequential path has a named control outside the model; credentials are task-scoped with no standing admin; egress is a default-deny allowlist enforced at the network layer and the renderer; memory writes are gated and provenance-stamped; irreversible actions show a resolved artifact behind a frozen approval; servers are pinned, hashed, and reviewed on change; every call is logged with its motivating provenance. Remaining findings are inventory and alerting polish.
- **85** — controls are in place and the bounds hold, with a cluster of MEDIUMs to schedule: uncapped bulk reads, unfiltered tool error output, no expiry on memory records, hidden-channel checks missing.
- **72** — the shape is right and the demonstration is missing: controls exist, but there is no indirect-injection corpus and no threat model of content sources, so nothing shows the bounds hold. Usable pre-production with the testing queued as real work, not as a documentation chore.
- **58** — a rendered image can carry context data to an arbitrary host, or a document can induce a durable memory write, or the agent authorizes user actions with its own identity. BLOCKED until the control is installed at the boundary — not until the specific instance is patched, which leaves the next one open.
