# AGENTS.md Template (AKOS integration)

Written into a project's `AGENTS.md` (read by Codex CLI and other agents) between markers.

Codex discovers `AGENTS.md` hierarchically from the git root down to the working directory and budgets the total to 32 KiB, so this block stays short on purpose. The `akos` and `akos-review` **skills** carry the full bootstrap and load on demand.

```markdown
<!-- AKOS:START -->
## AKOS
This project uses AKOS. Invoke the `akos` skill before non-trivial work on
user-facing features, architecture, security, or data; `akos-review` to review.
Active profile and overrides: `.akos/config.md`
<!-- AKOS:END -->
```

## Prerequisite

The skills must be discoverable by Codex — `./install.sh` links them into `~/.agents/skills/`. Verify with `akos list-skills` or `./doctor.sh`. In Codex, `/skills` lists them and `$akos` invokes one explicitly.

For agents without skill support, use the long-form bootstrap in [generic-agent-instructions.md](generic-agent-instructions.md).
