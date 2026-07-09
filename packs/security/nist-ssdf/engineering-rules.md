# Engineering Rules — NIST SSDF Pack

- NS1. Security requirements for the project/organization are documented and reviewed at least annually or on major scope change. (PO1)
- NS2. A named owner (person or role) exists for: dependency updates, security code review, and vulnerability response. (PO2)
- NS3. Dependency vulnerability scanning and secrets scanning are integrated into CI, running on every merge to main. (PO3)
- NS4. Repository write access and CI configuration changes require review (branch protection, protected CI config files); commits to release branches are traceable to an authenticated identity. (PS1)
- NS5. An SBOM (or equivalent dependency manifest with version pinning) is generated for release artifacts and kept current. (PS2)
- NS6. CI/CD pipelines verify artifact integrity before deployment (checksum/signature verification); pipeline configuration changes are reviewed like code. (PS3)
- NS7. Features handling sensitive data or elevated privilege have a documented threat model or security requirement written before implementation begins. (PW1)
- NS8. New third-party dependencies are checked for maintenance status and known vulnerabilities before adoption; adopted dependencies are monitored continuously (via NS3). (PW3)
- NS9. Code changes affecting authentication, authorization, or data handling receive explicit security-focused review (not only general code review) before merge. (PW4)
- NS10. A published vulnerability disclosure channel exists (security contact, disclosure policy) and is monitored. (RV1)
- NS11. Discovered vulnerabilities are triaged with a severity rating and a target remediation time by severity, tracked to closure. (RV2, RV3)
