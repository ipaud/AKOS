# Heuristics — NIST SSDF Pack

- **The "who's responsible" test:** ask who owns dependency updates, who does security review, who responds to a vulnerability report — if the honest answer is "nobody specifically," PO2/RV1 gaps exist.
- **The SBOM spot-check:** pick a recently-disclosed high-profile CVE in a popular library; can you answer "are we affected?" in minutes via an SBOM/dependency inventory, or does it require manually grepping lockfiles across repos? (PS2)
- **The build-tampering test:** could someone with write access to CI configuration (but not the main codebase) inject arbitrary code into a release build unnoticed? (PS3)
- **The disclosure-channel test:** if an external researcher found a vulnerability today, is there a published way for them to report it responsibly (security.txt, a security@ email, a bug bounty)? (RV1)
- **The "threat model before code" check:** for the last few sensitive features shipped, was a threat model or security requirement documented before implementation, or only a post-hoc review after the fact? (PW1)
- **The dependency-vetting check:** before adding a new third-party package, is there any check beyond "does it work" (maintenance status, known vulnerabilities, license)? (PW3)
- **The patch-SLA check:** is there a stated target time-to-patch by severity (e.g. critical in 24-48h, high in a week), or is patching timing ad hoc per incident? (RV2, RV3)
