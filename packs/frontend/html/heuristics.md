# Heuristics — HTML Pack

- Before writing a `div` with a click handler, ask "is there a native element for this?" (button, a, details, dialog, summary).
- Read the page as an outline (headings only) — does it make sense stripped of all styling?
- If a form works without labels visually (placeholder-only), it's already broken for screen readers and autofill.
- View source, not just the rendered DOM — does the semantic structure exist in markup, or only via CSS/JS-driven appearance?
