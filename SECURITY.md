# Security Policy

AKOS is a knowledge system and CLI that runs locally on a developer's machine.
Its highest-risk surfaces are the lifecycle scripts (`install.sh`, `update.sh`,
`uninstall.sh`) that write into `$HOME`, and the rule detectors under `rules/`
that read files in a project being reviewed.

## Reporting a vulnerability

Report privately — do not open a public issue for a security bug.

- Preferred: open a [GitHub private security advisory](https://github.com/ipaud/AKOS/security/advisories/new).
- Alternative: email the maintainer at the address on the GitHub profile
  [@ipaud](https://github.com/ipaud).

Please include what the issue is, how to reproduce it, and the impact. A
proof-of-concept helps but is not required.

## Response

This is a personal project maintained on a best-effort basis. Expect an initial
acknowledgement within about a week. Fixes for confirmed issues on the safety
floor (secret exposure, data loss in the lifecycle scripts, path traversal in
the CLI) take priority.

## Scope

In scope: `bin/akos`, the lifecycle scripts, the Python under `schemas/`,
`rules/`, `benchmarks/`, `evals/`, and the GitHub Actions workflows.

Out of scope: findings the tool reports about a project you point it at (that is
the tool working), and the deliberately-vulnerable fixtures under
`benchmarks/cases/**` and `evals/cases/**` (they exist to exercise the
detectors).
