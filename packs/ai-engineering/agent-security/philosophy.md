# Philosophy — Agent Security

## The agent is a new kind of principal, and it was never designed to be one

Application security spent thirty years learning to distinguish code from data. Parameterized queries, contextual escaping, argument arrays, content security policies — each is the same insight applied at a different boundary: the thing that decides must never be assembled from the thing being processed. Language models arrived having collapsed that distinction by construction. Instructions and data are the same substrate, read by the same mechanism, weighted by the same process. Then we gave that mechanism credentials, network access, and a shell.

This is why agent security is not general application security with a model bolted on. The web layer's problems remain — they are [owasp-top-10](../../security/owasp-top-10/README.md)'s job, and they don't go away. What is new is a component that reads attacker-influenced text and then decides what to do, with no reliable internal boundary between the two roles. Every rule in this pack is a way of restoring, from the outside, a separation the model cannot maintain from the inside.

## The attack you should fear is the one nobody sent

There is a natural tendency to picture prompt injection as an adversarial user typing a clever paragraph into a chat box. That version is real, it is mostly a nuisance, and it is bounded: a user manipulating an agent into misbehaving is bounded by what that user was already permitted to do. The version that matters is the one where nobody hostile ever touches the interface. An instruction sits in the third paragraph of a support ticket, in the alt text of an image on a scraped page, in a comment in a config file, in the body of an email the agent was asked to summarize. The operator asked an ordinary question. The agent read the document because that was the task. The attacker's text arrives inside the operator's own trusted workflow, wearing the operator's own trust.

Once that is the model, the security question stops being "can we stop the model from being fooled" and becomes "what happens when it is." The first question has no reliable answer. The second is engineering.

## Defenses that ask the model to choose correctly are not defenses

The instinctive response to injection is to write better instructions: tell the model that following embedded commands is forbidden, wrap untrusted content in delimiters, add a classifier that screens for suspicious phrasing. All of these help, in the sense that they raise the attacker's cost and reduce the frequency of successful attempts. None of them is a control, because all of them are adjudicated by the same statistical process the attacker is manipulating. A control that the attacker can argue with is a suggestion.

The distinction is worth being pedantic about, because it determines what goes in the threat model. A mitigation reduces how often you get hit. A control bounds what happens when you do. A system whose entire defense is mitigations has no floor — it just has a hit rate nobody has measured. So every proposed defense gets the same question: which component enforces this, and can the attacker's text reach that component? If the answer is "the model, and yes," it is a mitigation, and it should be written down as one.

## Capability is the security boundary, because intent isn't one

If the model cannot be trusted to refuse, then the only honest measure of an agent's risk is what it is able to do. Not what it usually does, not what its prompt says it should do — what its credentials, its tools, its network reach, and its filesystem access permit. A successful injection is best understood as a temporary transfer of the agent's entire permission set to whoever wrote the text it read.

That reframing is uncomfortable in a useful way, because it makes permission a security decision rather than a convenience one. Every extra tool in the default set, every credential scoped broader than the task, every capability kept around because removing it would be annoying — these stop being tidiness issues and become the actual, quantified answer to "how bad is a successful attack." An agent with read access to one repository and no egress is not immune to injection; it is immune to the consequences. That is the only kind of immunity available.

## Exfiltration needs three ingredients, and you control the third

The characteristic agent breach is not dramatic. Sensitive material is in the context because the task required it. Untrusted content is in the context because the task required that too. And somewhere in the agent's reach is a channel that leaves — a URL it can render, a comment it can post, a host it can reach, a file someone else will read. Any two of those are survivable. All three at once is a live vulnerability, and it usually got assembled by three reasonable decisions made by different people at different times, none of whom saw the third ingredient arriving.

The practical consequence is that egress deserves more scrutiny than it usually gets, because it is the ingredient most often invisible. Nobody thinks of a rendered markdown image as an outbound request. Nobody thinks of a public comment as a data channel. Enumerating egress honestly — every path by which bytes in the context can become bytes someone else observes — is one of the highest-yield exercises in this pack, and it is nearly always longer than the first guess.

## Persistence turns one compromise into an ongoing one

The worst property a poisoned fact can have is durability. An injection contained within a session ends when the session does. A false claim written into memory becomes a premise: it is read in a later session by a different user on a different task, carrying no trace of where it came from and no reason for anyone to doubt it. Reasoning built on it will look independently derived. Verification against the record will confirm it, because the record is the thing that was poisoned.

This is why memory writes deserve gating that memory reads do not, and why provenance has to survive into storage. A memory system that stores what it learned without storing where it learned it has no mechanism for recovering from a bad day, and no way to answer the only question that matters afterward: what else did we believe because of that.

## Where this philosophy stops

This pack covers the surface an agent adds. It does not restate general web and API security — injection into your own SQL, broken access control on your own endpoints, TLS, dependency CVEs — which belong to [owasp-top-10](../../security/owasp-top-10/README.md) and [owasp-api-top-10](../../security/owasp-api-top-10/README.md) and must be loaded alongside it whenever the surface under review has both. It does not cover how to *shape* a tool — its parameters, its return type, its description as an affordance — which is [tool-design](../tool-design/README.md); this pack covers the controls guarding that tool once it exists. It does not cover an agent's architecture, its termination conditions, or its authority boundary as an engineering artifact — that is [agent-foundations](../agent-foundations/README.md), whose escalation-conditions work is the operational sibling of this pack's approval gates. And it does not cover context assembly and provenance labeling as a quality discipline, which is [context-engineering](../context-engineering/README.md); here the same labeling is a security control with an enforcing component behind it.

Finally: nothing in this pack licenses a tradeoff against the safety floor. Per [core/constitution.md](../../../core/constitution.md), security is one of three things AKOS never waives, at any authority level, in any reasoning profile. A prototype agent holds real credentials and reaches real systems. The ceremony scales with the profile; the floor does not.
