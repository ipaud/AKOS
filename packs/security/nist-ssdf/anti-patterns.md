# Anti-Patterns — NIST SSDF Pack

## Security-by-hero

One engineer who "handles security stuff" informally, with no documented process, no backup, and no defined scope — when they leave, the org's entire secure-development practice leaves with them. Fix: NS2 — named, documented ownership independent of any one person.

## Dependency blind spot

No dependency scanning in CI; the team finds out about vulnerable dependencies only when a customer or researcher reports an incident. Fix: NS3, NS8.

## Unprotected build pipeline

Anyone with repo access can modify CI configuration and inject arbitrary build steps, with no review requirement — a compromised contributor account becomes a full supply-chain compromise vector. Fix: NS4, NS6.

## No disclosure channel

A security researcher who finds a real vulnerability has no idea how to report it responsibly, so they either give up, post it publicly (0-day disclosure), or sell it. Fix: NS10 — a security.txt and monitored contact, minimal effort, meaningful risk reduction.

## Threat modeling as review-time archaeology

Security requirements for a payments feature are discovered for the first time during a pre-launch security review, three days before ship, forcing a scramble or a risky rushed fix. Fix: NS7 — threat model before implementation, not after.

## Ad hoc patch timing

A critical CVE in a production dependency sits unpatched for months because there's no severity-based SLA driving prioritization — it competes with feature work on an equal footing. Fix: NS11 — severity-based remediation targets.

## SBOM as a one-time document

An SBOM generated once at a compliance deadline, never regenerated as dependencies change — stale within weeks and useless for actually answering "are we affected by this new CVE." Fix: NS5 — generated per release, automated, not manual.
