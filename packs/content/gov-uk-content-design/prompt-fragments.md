# Prompt Fragments — GOV.UK Content Design Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply GOV.UK content design constraints (AKOS L2):
- Start from a user need: "as a [user] I need to [do/know X] so that [outcome]".
  If you cannot write it without inventing the user, say so instead of writing.
- Answer the user's question in the user's words. Use the terms people search
  with; put the official term in brackets on first mention if it differs.
- Front-load: the answer is the first sentence. No preamble, no welcome, no
  context before the answer. First three words of every heading and link carry
  the meaning — never "Overview", "About", "Information".
- Plain language: sentences <=25 words (mean <=20), one idea each, paragraphs
  <=5 lines, reading grade level <=6 for general audiences.
- Active voice; name who acts in every instruction, deadline, obligation and
  consequence. Passive is banned in those sentences.
- Format is meaning: 3+ ordered actions -> numbered steps; comparisons across
  2+ attributes -> a table; 3+ eligibility conditions -> a question sequence or
  separate pages. Prose only for explanation, and only after the answer.
- Ban jargon, metaphor and filler ("in order to", "please note", "utilise",
  "simply", "just", "journey", "unlock", "seamless"). Define any specialist
  term at first use.
- One page, one need. Say what the reader must do, not everything that is true.
- Title <=65 chars, verb-led for tasks. Link text names the destination and
  works out of context.
- Every page needs a named owner and a review date. If you cannot assign both,
  flag it rather than publishing.
```

## Fragment: review lens

```text
Review this content as a GOV.UK-school content designer. Work in this order:
1. Need — state the user need this content meets, in the "as a / I need to /
   so that" form. If the beneficiary is the organisation, that is the top
   finding and everything else is secondary.
2. Question match — write the question a real person would type. Does that
   wording appear in the title, first heading, or first sentence?
3. Front-loading — is the answer in sentence one? Delete the first paragraph:
   did anything of value disappear?
4. Scan test — read only title, headings and list items. Is the answer already
   there? If meaning lives in connective prose, report a structure failure.
5. Actor test — for every instruction, deadline, obligation and consequence,
   name who acts. Unassigned actions are CRITICAL, not stylistic.
6. Format test — flag any sequence, comparison, or branching condition that is
   trapped in prose; state the format it should be.
7. Readability — measure sentence lengths and grade level against GCE5-GCE9.
8. Lifecycle — owner, review date, staleness, duplicates, retirement candidates.
9. Run review-checklist.md and report by severity, each finding with the
   concrete rewrite, not a description of the problem.
Never write "improve the copy". Quote the sentence, name the rule ID, give the
replacement text.
```

## Fragment: content-structure pass

```text
Restructure this content by format, without changing the facts:
- Extract every ordered sequence into numbered steps.
- Extract every multi-attribute comparison into a table with a header row.
- Extract every branching eligibility rule into short standalone statements or
  a question sequence — no nested "if... unless... except" prose.
- Convert parallel options into bullets with a lead-in line, <=2 sentences and
  parallel grammar per item, <=8 items.
- Rewrite headings so the first three words distinguish the section; the
  headings alone must read as a usable summary.
- Move all explanation and context below the answer.
Output: the restructured content, then a short table of what moved and why.
```

## Fragment: content lifecycle audit

```text
Audit this content estate for lifecycle health. For every page report:
- user need statement (or MISSING)
- owner and review date (or UNOWNED / NO REVIEW DATE)
- staleness: any fact past its review window (prices, dates, thresholds,
  system names) — flag STALE
- duplicates: other pages answering the same question
- verdict: KEEP / EDIT / SPLIT / MERGE / RETIRE
Apply bias order retire > edit > split > new. For every RETIRE, name the
redirect target — never a 404, never an orphan. Rank the output by user harm:
wrong-and-unowned first, then stale on task-critical paths, then duplicates,
then unowned-but-correct.
```

## One-liner (for tight token budgets)

```text
GOV.UK content design: meet a stated user need or do not publish; answer the
user's question in their words, first sentence, first three words of every
heading; plain language (sentences <=25 words, grade <=6) because it costs
readers less, not because they are less able; active voice naming who acts;
steps for sequences, tables for comparisons, prose last; no jargon, metaphor
or filler; one page one need; every page needs an owner and a review date, and
content that no longer meets a need gets retired with a redirect.
```
