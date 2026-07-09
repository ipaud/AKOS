# Principles — NIST SSDF Pack

## PO — Prepare the Organization

- **PO1** — Security requirements for the organization's software are defined and communicated, reviewed/updated periodically.
- **PO2** — Roles and responsibilities for secure development are defined (who threat-models, who reviews, who owns dependency updates).
- **PO3** — Toolchains (SAST, dependency scanning, secrets scanning) are selected, configured, and integrated into the development process, not left optional/ad hoc.

## PS — Protect the Software

- **PS1** — Source code and build artifacts are protected from unauthorized access (repository permissions, branch protection, signed commits where warranted).
- **PS2** — Provenance of all software components (including third-party/open-source) is tracked — an SBOM or equivalent exists and is kept current.
- **PS3** — Software is protected against tampering through the build and release process (integrity verification, protected CI pipelines).

## PW — Produce Well-Secured Software

- **PW1** — Software design considers security requirements and threat models before implementation (overlaps [OWASP ASVS AS3](../owasp-asvs/principles.md), [A04 Insecure Design](../owasp-top-10/principles.md)).
- **PW2** — Secure coding practices are followed and enforced (overlaps [OWASP Top 10](../owasp-top-10/principles.md) engineering rules directly).
- **PW3** — Third-party components are vetted before adoption and monitored for vulnerabilities continuously after.
- **PW4** — Code is reviewed (human and/or automated) for security issues before merge, with security-specific review distinct from general code review where risk warrants it.
- **PW5** — Executable code is tested for security issues (SAST/DAST/penetration testing where warranted by ASVS level) before release.

## RV — Respond to Vulnerabilities

- **RV1** — A vulnerability disclosure/reporting channel exists and is publicized, so researchers/users have a defined way to report issues.
- **RV2** — Discovered vulnerabilities are triaged by severity with defined response-time targets, and root-caused (not just patched superficially).
- **RV3** — Patches/mitigations are deployed promptly per severity-based SLA, and affected users/stakeholders are communicated with per a defined plan.
