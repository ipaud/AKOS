# Prompt Fragments — NIST SSDF Pack

## Fragment: SDLC process review lens

```text
Review this project's secure-development lifecycle against NIST SSDF
(AKOS L1), organized by practice group:
PO (Prepare) — are security requirements documented? Is there a named
  owner for dependency updates, security review, vulnerability response?
PS (Protect) — is repo/CI access controlled and reviewed? Is there an
  SBOM or dependency manifest? Is the build pipeline protected from
  tampering?
PW (Produce) — are threat models written before implementing sensitive
  features? Are third-party dependencies vetted before adoption? Is
  security-focused review distinct from general code review on
  auth/data-handling changes?
RV (Respond) — is there a published vulnerability disclosure channel?
  Are discovered vulnerabilities triaged by severity with remediation-
  time targets?
Scale expected rigor to the project's profile (Prototype through
Enterprise) per the decision framework.
```

## Fragment: supply-chain check

```text
Assess supply-chain security for this project: is there an SBOM or
equivalent dependency inventory? Is dependency vulnerability scanning
automated in CI? Is the CI/build pipeline protected from unreviewed
configuration changes? Could a compromised dependency or a compromised
CI config inject code into a release undetected?
```

## One-liner

```text
NIST SSDF: security requirements and named ownership before coding
(Prepare); protect code/build artifacts from tampering with SBOM and CI
integrity (Protect); threat-model sensitive features and vet
dependencies before building (Produce); publish a disclosure channel and
triage vulnerabilities by severity with remediation SLAs (Respond).
```
