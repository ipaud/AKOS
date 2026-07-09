# Prompt: Create a New Pack

---

Load AKOS (`~/DEV/AKOS/prompts/load-akos.md`), read `~/DEV/AKOS/core/knowledge-schema.md` and `~/DEV/AKOS/core/source-policy.md`, then create a new knowledge pack for [source/domain].

Steps:
1. Run `akos create-pack <domain>/<name>` to scaffold the 16-file structure (or create the files manually per the schema).
2. Set `metadata.yaml`: name, domain, authority-level (0–4 per `core/authority-model.md`), version 1.0.0, tags, sources (title/author/URL only), related packs.
3. Write `principles.md` FIRST — it forces the distillation.
4. Derive `review-checklist.md` and `engineering-rules.md` from the principles.
5. Fill the rest: philosophy, mental-models, heuristics, decision-framework, anti-patterns, examples (invented, never lifted), prompt-fragments, scoring-rubric, glossary, references, README.
6. Link related packs in the relevant `graphs/` file.
7. Run `./doctor.sh` to verify the 16-file contract.

**Copyright discipline (mandatory):** distill ideas, never reproduce text. No copied paragraphs, no long quotes, no chapter-structure mirroring. Original examples only. Attribution by title/author/URL only. The pack must read as if written by an expert who internalized the ideas years ago — not by someone holding the book open. Include the independent-distillation disclaimer line in the README.
