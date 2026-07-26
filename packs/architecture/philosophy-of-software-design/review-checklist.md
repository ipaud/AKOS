# Review Checklist — Philosophy of Software Design Pack

Binary checks, each citing its rule. **Nothing here blocks.** This is a Level 3 design
pack: the highest severity it produces is MEDIUM, and a finding without a stated cost to
a reader or a caller is an aesthetic preference, not a finding
([decision-framework](decision-framework.md)).

## Medium (worth fixing before the code settles)

- [ ] Every module or class can be described in one sentence naming what it hides. (PSD1)
- [ ] No public interface exposes nearly as many concepts as its implementation. (PSD2)
- [ ] Each new class or module introduced by this change states what it hides. (PSD3)
- [ ] The same design decision — format, encoding, key layout, retry policy — is known to
      exactly one module. (PSD8)
- [ ] Modules are grouped by what they know, not by the order work happens in. (PSD9)
- [ ] No public field, getter, or setter exposes an implementation choice. (PSD10)
- [ ] No caller must invoke two methods in a fixed order for a correct result. (PSD11)
- [ ] Adjacent layers offer genuinely different abstractions. (PSD6)
- [ ] Before adding an exception or error return, an absorbing semantic was
      considered. (PSD17)
- [ ] Already-in-desired-state operations succeed rather than raising. (PSD18)
- [ ] Exceptions every caller handles identically are handled once, lower down. (PSD19)
- [ ] Interface comments describe caller-facing behavior and exclude implementation
      detail. (PSD26)
- [ ] Non-obvious *why* is written down. (PSD28)
- [ ] Units, ranges, ownership, and null/empty semantics are stated. (PSD29)
- [ ] Change amplification in this diff is reported with the missing abstraction
      named. (PSD34)

## Low (note it, don't argue about it)

- [ ] No pass-through methods that add no abstraction. (PSD4)
- [ ] No variable threaded through more than two frames to reach one consumer. (PSD5)
- [ ] No wrapper existing only to rename or reorder arguments. (PSD7)
- [ ] Configuration parameters are individually justified. (PSD12)
- [ ] Interfaces are shaped by what callers need to accomplish. (PSD13)
- [ ] Repeated narrow variants were considered for one slightly more general
      operation. (PSD14)
- [ ] No extension point without a present or scheduled second consumer. (PSD15)
- [ ] Behavior differences use a named parameter rather than an opaque boolean. (PSD16)
- [ ] Special-case branches are folded in, or carry a reason. (PSD20)
- [ ] Error handling aggregates at a boundary where recovery does not differ. (PSD21)
- [ ] Names let a reader predict what the thing does not do. (PSD22)
- [ ] One concept, one word, across the codebase. (PSD23)
- [ ] Names that need a comment were renamed instead. (PSD24)
- [ ] Non-trivial block variables are named for what they hold. (PSD25)
- [ ] No comment restates the line below it. (PSD27)
- [ ] Comments sit next to what they describe; duplicated docs have one home. (PSD30)

## Process (ask, don't assert)

- [ ] For a non-trivial new unit, was the interface comment written first? (PSD31)
- [ ] For an expensive-to-reverse decision, was a genuinely different second design
      sketched? (PSD32)
- [ ] Does this change leave the design better, or say why not? (PSD33)
- [ ] Was anything in the diff not understandable without tracing elsewhere? (PSD35)
- [ ] Is there a part nobody understands, and does it have an owner? (PSD36)

## Reviewer discipline

Before reporting any item above, answer: **what would the caller or the next reader stop
having to know if this were fixed?** If there is no answer, drop the finding. Reviews that
apply this pack as a style rulebook produce noise and teach people to ignore design
feedback — which costs more than the shallow module did.
