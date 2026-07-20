# Eval providers

Level C (LLM-assisted) benchmark cases need something to generate a review from a fixture. This is a small, swappable provider interface — never a required dependency for the deterministic Level A/B path, which is what every acceptance criterion actually needs.

## Contract

A provider is a Python module exposing:

```python
def generate(prompt: str) -> str:
    """Return raw text. May raise ProviderUnavailable if it can't run right now
    (no network, no CLI installed, etc.) — the caller treats that as `skipped`,
    never as a failure."""
```

See `contract.md` for the full interface, including the `ProviderUnavailable` exception.

## `mock.py` — required, deterministic, no network

Never calls out anywhere. Given a prompt, it returns a canned response built from simple keyword matching against the prompt/fixture content — genuinely weak, and documented as such. Its only job is to prove the Level C plumbing works end-to-end without needing a real model, and to keep CI fully offline. **This is the only provider CI ever uses.**

## `claude_cli.py` — optional, local-only

Shells to `claude -p <prompt>` (Claude Code's non-interactive print mode) if `command -v claude` finds it on `PATH`. Marked experimental. Never invoked by CI or by `akos benchmark`'s default run — only via an explicit `--provider claude_cli` flag, for a maintainer who wants a real (if still not rigorously graded) Level C pass locally.

## Why not wire a real hosted LLM API

Two reasons, not one:

1. Determinism — Level A/B benchmark scoring must be reproducible; adding a live API call to the default run would make `akos benchmark`'s output depend on model version drift and network availability.
2. No new required dependency — this project has exactly one accepted external dependency (`python3` itself). An API key requirement would be a second, and a costed one, for the ONE part of the system (Level C) that every acceptance criterion says is optional.

`claude_cli.py` sidesteps both: it's already on this machine's `PATH` in a Claude Code session, needs no API key of its own, and is opt-in.
