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

## Security properties

These are the guarantees the tool is built to hold. A reproducible bypass of any
of them is an in-scope vulnerability — report it as above.

- **Analyzed repositories are an untrust boundary.** Anything AKOS reads from a
  project under review — source, comments, tool output, and `.akos/config.md` —
  is data, never instruction. The repo config can supply project facts and hints
  and can *raise* scrutiny (`Deployed: yes`), but it can never lower the safety
  floor (security, accessibility basics, data integrity), change review weights,
  disable detectors, or add arbitrary reading paths. `akos check-config`
  validates the config's *form*; a clean result does not make the repo a trusted
  operator.
- **The scanner fails closed.** A detector or rule registry that cannot execute
  is reported as an operational error (exit 1), never silently turned into a
  finding and never a clean pass. An incomplete scan cannot report "clean".
- **Secrets block regardless of path.** A realistic credential — a live vendor
  key, a `service_role` JWT, a high-entropy generic secret — is a blocking
  finding wherever it appears, including `tests/`, `fixtures/`, and `docs/`. The
  path may annotate the finding but never downgrades or suppresses it. (A key
  already gitignored is "not committed to source" and out of this rule; obvious
  placeholders and public anon keys are not secrets.)
- **Install never destroys content.** The lifecycle scripts only ever create or
  refresh AKOS-owned symlinks. A real file, a real directory, or a foreign
  symlink at any managed destination is left byte-for-byte intact, with a
  warning.
- **Review history is immutable.** Records are uniquely identified and published
  by atomic rename; a published review is never overwritten and a failed record
  leaves no partial state. Reports are secret-redacted at write time. Readers
  (`list`/`latest`/`clean`) never mistake an in-flight staging directory for a
  published review, and never silently present a corrupt review as clean.
- **Ambiguous AKOS:START/END markers are rejected, not guessed at.** A file with
  multiple start/end markers, a one-sided marker, or markers out of order is
  left byte-for-byte untouched and the write refuses — the previous
  first-match behavior could silently operate on the wrong section of a file.
- **`update.sh` fails closed.** The personal layer (`packs/personal/`) is
  backed up with a manifest and verified against the live source before any
  pull; after the pull, any drift from that manifest — including from a
  legitimate upstream commit — triggers a full-tree restore, and the restore
  is itself verified before being reported as successful. A failed backup,
  failed restore, failed pull, non-git checkout, or failing final `doctor.sh`
  all exit non-zero; "preserved"/"restored"/"complete" is never printed
  without the corresponding check having run. Symlinks inside the personal
  layer are recorded and restored by their target string — never followed or
  resolved.
- **Schema contracts reject the unknown.** Every pack, agent, and workflow
  must declare a `schema_version`; an unrecognized version fails explicitly
  rather than being validated against whatever the current schema happens to
  be, and an undeclared top-level or nested field is a validation error, not
  a silently-ignored typo.
- **A `status: draft` pack is not stable authority.** It is visible and
  usable, but excluded from automatic routing and from any `status: stable`
  agent's or workflow's dependencies; a project's `.akos/config.md` cannot
  self-authorize one into its always-load set, and there is no
  `allow_draft_packs` field that would let it.
