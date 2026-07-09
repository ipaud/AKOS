# Principles — Design Systems Pack

- **DS1** — Tokens are three-layered (reference/system/component); components consume system/component tokens only.
- **DS2** — Every component ships with usage docs, prop reference, and accessibility notes — undocumented components don't count as published.
- **DS3** — Component APIs are designed for the anticipated range of use cases up front, not grown reactively prop-by-prop per feature request.
- **DS4** — Breaking changes to shared components go through a deprecation path (old + new coexist for a transition window), not an instant swap.
- **DS5** — A named owner/team governs additions and changes to the system; ad hoc unreviewed additions are not merged.
- **DS6** — Accessibility (states, focus, contrast) is built into base components once, so consumers inherit it for free.
