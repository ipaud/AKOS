# Mental Models — OWASP ASVS Pack

## The three verification levels as a dial, not a ladder to always max out

L1 → L2 → L3 is often read as "more mature = higher level," but the right model is calibration: an internal tool for 5 employees genuinely only needs L1, permanently — that's not immaturity, it's correct sizing. Choosing L3 for a low-stakes app wastes effort that could go toward actual product value; choosing L1 for a payments platform is negligence. The level is chosen by what the application protects and who might attack it, not by organizational ambition.

## Fourteen control domains, not one list

ASVS organizes requirements into domains: Architecture, Authentication, Session Management, Access Control, Validation/Sanitization/Encoding, Stored Cryptography, Error Handling/Logging, Data Protection, Communications, Malicious Code, Business Logic, Files/Resources, API/Web Service, Configuration. Thinking in domains (rather than one flat checklist) helps assign ownership — architecture and business-logic domains usually need a human architect's judgment; validation and crypto domains are more mechanically checkable.

## Centralized security controls over scattered ad hoc checks

A recurring ASVS theme: authentication, authorization, input validation, and output encoding should be implemented as centralized, reusable controls (a single auth middleware, a single validation layer) rather than re-implemented per endpoint. Centralization means a fix in one place fixes everywhere; scattered ad hoc checks mean every endpoint is a fresh opportunity to forget one.

## Business logic flaws exist without any "bug"

A checkout flow that lets a user submit the payment step, then the shipping step, then the payment step again with a different (lower) price computed from stale state — no single line of code is "wrong" in isolation, but the *sequence* is exploitable. ASVS's business-logic domain exists because these flaws are invisible to code scanners and only found by someone actually reasoning about the workflow's state machine.
