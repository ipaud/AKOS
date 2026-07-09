# Review Checklist — NIST SSDF Pack

Applicability scales with profile — see [decision-framework.md](decision-framework.md).

## High (Production+)

- [ ] Named owner exists for dependency updates, security review, and vulnerability response. (NS2)
- [ ] Dependency and secrets scanning integrated into CI on every merge. (NS3)
- [ ] Repository/CI configuration changes require review; release commits traceable to authenticated identity. (NS4)
- [ ] Sensitive features have a documented threat model/security requirement written before implementation. (NS7)
- [ ] Authentication/authorization/data-handling changes receive explicit security-focused review. (NS9)
- [ ] Published vulnerability disclosure channel exists and is monitored. (NS10)

## Medium (Production/Enterprise)

- [ ] Security requirements documented and reviewed periodically. (NS1)
- [ ] New third-party dependencies vetted before adoption. (NS8)
- [ ] Discovered vulnerabilities triaged with severity and remediation-time targets. (NS11)

## Low (Enterprise)

- [ ] SBOM generated and current for release artifacts. (NS5)
- [ ] CI/CD verifies artifact integrity before deployment. (NS6)
