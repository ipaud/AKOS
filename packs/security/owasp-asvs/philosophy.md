# Philosophy — OWASP ASVS Pack

## Security verification should scale with what's at stake, not be one-size-fits-all

The OWASP Top 10 answers "what are the most common risks?" ASVS answers a different question: "how do I know if *my specific application*, given what it protects, has been verified thoroughly enough?" A todo-list app and a banking platform shouldn't be held to the same verification depth — ASVS's three levels give a principled, named way to calibrate that depth instead of either under-verifying critical systems or wasting effort over-verifying trivial ones. This maps directly onto AKOS's own [reasoning profiles](../../../core/reasoning-profiles.md): Prototype/MVP roughly track ASVS L1, Production tracks L2, Enterprise/regulated tracks L3.

## Verification, not just awareness

Where the Top 10 is a risk-awareness list ("here's what commonly goes wrong"), ASVS is structured as testable, verifiable requirements organized by domain (authentication, session management, access control, validation, cryptography, error handling, data protection, communications, malicious code, business logic, files, API, configuration). Each requirement is written to be checkable — "verify that" — which makes it suitable as an actual audit checklist, not just a reading list.

## Architecture and business logic get first-class treatment

Unlike a purely bug-catalog approach, ASVS explicitly covers architectural concerns (trust boundaries defined, security controls centralized not duplicated ad hoc) and business logic flaws (workflows that can be abused by being executed out of order, or an excessive number of times, even though no individual step has a "bug"). These are exactly the categories that pure code-scanning tools miss and that require an architectural review to catch.

## A shared vocabulary for "how secure is secure enough"

Naming a target level (L1/L2/L3) up front, before development, turns "is this secure enough?" from an endless subjective debate into a checklist exercise against a named, external, industry-recognized bar — useful both for internal alignment and for external communication (compliance, partners, auditors).
