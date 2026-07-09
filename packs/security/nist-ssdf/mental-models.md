# Mental Models — NIST SSDF Pack

## Four practice groups as a lifecycle map

**PO (Prepare)** — define security requirements, assign roles, select tools, before writing code. **PS (Protect)** — protect the code, build artifacts, and infrastructure from unauthorized access/tampering while they exist. **PW (Produce)** — the actual secure design/coding/testing/review work most other security packs focus on. **RV (Respond)** — the process for handling vulnerabilities discovered after release. Most teams over-invest in PW and under-invest in PO and RV — SSDF's structure exists partly to correct that imbalance.

## Software Bill of Materials (SBOM)

A machine-readable inventory of every component (direct and transitive dependency) in a software artifact, with version and provenance information. An SBOM turns "do we use anything with the newly-disclosed CVE-2024-XXXXX" from a scramble into a query — this is what makes rapid vulnerability response (RV) actually tractable at scale, rather than depending on someone remembering what's in the dependency tree.

## Provenance and build integrity

Knowing not just *what* code is in an artifact but *how it got there* — which commit, which build system, whether the build process itself could have been tampered with. Signed commits, reproducible builds, and protected CI pipelines (no unreviewed script injection into the build) are the concrete mechanisms; the mental model is "an attacker who compromises the build system doesn't need to find a bug in your code at all."

## Shift-left security requirements

Security requirements (PO) function like non-functional requirements gathered at design time — "this feature handles payment data, so it needs encryption at rest and PCI-relevant access logging" decided *before* implementation, not discovered as a review finding after the feature ships. This is the SSDF-level equivalent of [Inspired's four-risk discovery](../../product/inspired/mental-models.md) applied specifically to security risk.

## Vulnerability response as a defined process, not improvisation

A mature RV practice has: a way for researchers/users to report vulnerabilities (disclosure policy), a triage process with severity criteria, a patching SLA tied to severity, and a communication plan for affected users. Without this defined in advance, a real vulnerability disclosure becomes a chaotic, high-pressure, ad hoc scramble at the worst possible time.
