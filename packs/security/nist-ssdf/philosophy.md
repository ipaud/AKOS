# Philosophy — NIST SSDF Pack

## Security is a lifecycle property, not a code property

OWASP's frameworks largely ask "is this specific code/API/application secure?" SSDF asks a broader question: "is the *process* that produces software secure, end to end?" A single perfectly-reviewed release doesn't mean the next one will be, if the process that produced it (dependency management, build pipeline integrity, vulnerability response readiness) has gaps. SSDF's four practice groups map to the actual lifecycle: before code is written (Prepare), while the codebase and its artifacts exist (Protect), while building the software (Produce), and after release when vulnerabilities are inevitably found (Respond).

## Supply chain is now the attack surface

A large and growing share of real-world breaches don't come from a bug in your own code — they come from a compromised dependency, a poisoned build tool, or a tampered CI pipeline. SSDF's emphasis on artifact provenance, build integrity, and dependency tracking (SBOM — Software Bill of Materials) reflects that modern software is assembled from hundreds of components any one of which could be the actual point of compromise, not written from scratch by the team being reviewed.

## Vulnerability response is not optional even for perfect code

No codebase stays vulnerability-free forever — new classes of attack are discovered, dependencies get CVEs disclosed after the fact, and code that was fine yesterday is exploitable today because the surrounding threat landscape moved. SSDF treats "how do you find out about and fix a newly-discovered vulnerability" as a first-class practice group (RV), not an afterthought — an organization with excellent secure coding but no vulnerability disclosure/response process is still exposed.

## Security requirements defined before development, not discovered during review

The "Prepare the Organization" group front-loads security requirements, roles, and tooling decisions to before code is written — the same logic as [shift-left testing](../../testing/testing-pyramid/philosophy.md) and [threat modeling before building](../owasp-asvs/principles.md): the cheapest time to fix a security gap is before it's built, not after a review finds it.
