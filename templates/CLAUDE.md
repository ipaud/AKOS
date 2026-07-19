# CLAUDE.md Template (AKOS integration)

This is the AKOS section that `akos install-project` writes into a project's `CLAUDE.md`, between markers so it can be safely re-generated without clobbering your own content.

It is deliberately short. The `akos` and `akos-review` **skills** carry the full bootstrap (constitution → authority model → profile → Level-0 layer → pack routing), so the project file only has to signal that AKOS applies here and where the profile lives. Everything else loads on demand, when the skill fires — not on every turn of every session.

```markdown
<!-- AKOS:START -->
## AKOS
This project uses AKOS. Invoke the `akos` skill before non-trivial work on
user-facing features, architecture, security, or data; `akos-review` to review.
Active profile and overrides: `.akos/config.md`
<!-- AKOS:END -->
```

## Prerequisite

The skills must be linked into `~/.claude/skills/` — `./install.sh` does this. Verify with `akos list-skills` or `./doctor.sh`.

On a tool without skill support, use the long-form bootstrap in [generic-agent-instructions.md](generic-agent-instructions.md) or [prompts/load-akos.md](../prompts/load-akos.md) instead.
