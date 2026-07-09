# Principles — HTML Pack

- **HT1** — Use the native element that matches the semantic/interactive need before reaching for a generic `div`/`span` + ARIA.
- **HT2** — One `h1` per page; headings sequential, never skipped for visual-size reasons.
- **HT3** — Landmark elements (`header`, `nav`, `main`, `aside`, `footer`) structure every page.
- **HT4** — Every form input has a real, bound `<label>`.
- **HT5** — Interactive elements are natively focusable/activatable (`button`, `a[href]`) — never a click handler on a non-interactive element.
- **HT6** — Use the correct input `type` (`email`, `tel`, `date`, `number`) for the right mobile keyboard and built-in validation.
- **HT7** — Images always have an `alt` attribute (descriptive or empty per purpose).
- **HT8** — Document `lang` is set; content structure doesn't depend on CSS to convey meaning.
