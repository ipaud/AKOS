# Codex Instructions Template (AKOS integration)

For OpenAI Codex CLI. Codex supports the same open agent-skills format as Claude Code, so the primary integration is the **skill**, not an instructions file.

## Primary path — skills

`./install.sh` links AKOS's skills into `~/.agents/skills/`:

```
~/.agents/skills/akos          → <AKOS>/skills/akos
~/.agents/skills/akos-review   → <AKOS>/skills/akos-review
```

Codex discovers skills at `$CWD/.agents/skills`, `$REPO_ROOT/.agents/skills`, `$HOME/.agents/skills`, and `/etc/codex/skills`. Once linked:

- `/skills` lists them
- `$akos` invokes the loader explicitly; `$akos-review` runs the review pipeline
- Both also fire implicitly when the task matches their description

Verify with `akos list-skills` or `./doctor.sh`.

## Alternative — install as a plugin

```bash
codex plugin marketplace add ipaud/AKOS
codex plugin add akos@akos
```

Start a new Codex session after installation so the bundled skills load. This
installs a copy into `~/.codex/plugins/cache/`. Use it to try AKOS or to share
it; use the symlinks above for your own working copy, since a plugin cache does
not track edits to your packs.

## Project marker

`akos install-project` writes a four-line block into the project's `AGENTS.md` — see [AGENTS.md template](AGENTS.md). It only signals that AKOS applies here; the skill carries the bootstrap.

## Fallback

For a Codex setup without skills, paste [prompts/load-akos.md](../prompts/load-akos.md) or use the long-form block in [generic-agent-instructions.md](generic-agent-instructions.md).

`~/.codex/prompts/*.md` custom prompts still work but are deprecated by OpenAI in favour of skills — do not build the AKOS integration on them.
