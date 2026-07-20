# Provider interface

```python
class ProviderUnavailable(Exception):
    """Raised when a provider can't run right now — no network, no CLI
    installed, no credentials. The benchmark runner treats this as
    `skipped: true` for that case, never as a failure."""

def generate(prompt: str) -> str:
    """Return raw text output for the given prompt. Deterministic providers
    (mock.py) must return the same output for the same input, every time."""
```

Every file under `benchmarks/providers/` implementing this is a valid provider. The runner selects one via `--provider NAME` (default: `mock`), importing `benchmarks/providers/NAME.py` and calling its `generate()`.
