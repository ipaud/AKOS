"""The required, deterministic, no-network eval provider. See README.md for
why this exists and why it's the only provider CI ever uses.

Genuinely weak by design: it does simple keyword matching against the
prompt, not real language understanding. This proves the Level C plumbing
end to end without needing a real model — it is explicitly NOT presented
as rigorous grading. A real LLM-judge pipeline is future work, not this.
"""

from __future__ import annotations


class ProviderUnavailable(Exception):
    pass


_CANNED_RESPONSES = {
    # Each response deliberately echoes its own trigger phrase literally —
    # must_mention checks the RESPONSE text, not the prompt, so a canned
    # response that only paraphrases the trigger (e.g. "loading indicator"
    # instead of "loading state") would fail a case checking for the exact
    # phrase. Caught by running the mock cases before trusting them.
    "empty state": "The list view has no empty state — nothing tells the user what to do when there are zero items.",
    "loading state": "No loading state is shown while data fetches, so a slow network reads as a broken page.",
    "error state": "No error state is shown on a failed request — no message, no retry action.",
    "service_role": "A service_role reference is reachable from a client-side import path.",
    "rls": "One or more tables have no RLS (Row Level Security) policy.",
}


def generate(prompt: str) -> str:
    lower = prompt.lower()
    hits = [resp for trigger, resp in _CANNED_RESPONSES.items() if trigger in lower]
    if not hits:
        return "No matching pattern found in this fixture for the mock provider's fixed trigger list."
    return " ".join(hits)
