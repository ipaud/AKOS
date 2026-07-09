# Decision Framework — NIST SSDF Pack

## How much SSDF process for a given project size/profile

| Profile | PO/PS/PW/RV depth |
|---------|-------------------|
| Prototype | Minimal — dependency scanning if free/easy (NS3); skip formal SBOM, threat modeling, disclosure channel |
| Startup MVP | NS3, NS8 (dependency hygiene); lightweight owner assignment (NS2); skip full SBOM/formal disclosure process |
| Production | Full NS1-NS9; RV1/RV2 (disclosure channel + triage) at minimum |
| Enterprise/regulated | Full NS1-NS11; SBOM required (NS5); formal patch SLAs (NS11); often externally audited |

## Prioritizing SSDF adoption when starting from zero

1. NS3 (CI dependency/secrets scanning) — cheapest, highest immediate value.
2. NS2 (named owners) — costs nothing but a decision, closes the "nobody's responsible" gap.
3. NS10 (disclosure channel) — a security.txt file and a monitored email address, an afternoon of work, closes a real gap.
4. NS7/NS9 (threat modeling + security review on sensitive changes) — process change, needs team buy-in.
5. NS5/NS6 (SBOM + build integrity) — more infrastructure investment, prioritize when supply-chain risk is real (public-facing, widely-distributed, or regulated software).

## Build vs. buy for SSDF tooling

Dependency/secrets scanning (NS3): mature free/low-cost tools exist (Dependabot, Snyk, gitleaks) — always buy/adopt, never build custom. SBOM generation (NS5): use standard tooling (Syft, CycloneDX generators) integrated into CI, not a hand-maintained spreadsheet. Threat modeling (NS7): a lightweight structured exercise (STRIDE or the [OWASP ASVS](../owasp-asvs/decision-framework.md) approach) is enough for most teams — dedicated threat-modeling software is rarely justified below Enterprise scale.
