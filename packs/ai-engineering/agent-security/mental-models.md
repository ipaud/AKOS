# Mental Models — Agent Security Pack

Named models this pack contributes. Use them as diagnostic lenses while designing, threat-modeling, or reviewing an agent that calls tools and acts.

## The provenance ladder

Text in an agent's context arrives through one of four channels, and its authority is a property of the channel, never of what it says.

| Class | Arrives from | May do | May never do |
|---|---|---|---|
| **System** | The platform's own configuration, under change control | Set the rules, the toolset, and the thresholds | — |
| **Operator** | The developer's prompt, skills, and policy files | Narrow or specialize the rules for a deployment | Widen the system's grants |
| **User** | The authenticated principal's request in this session | Ask for work within that principal's permissions | Exceed that principal's permissions |
| **Untrusted** | Retrieved documents, web pages, files, database rows, email, tool results | Inform an answer | Authorize an action, change a rule, widen a scope |

The ladder only descends. A lower class can restrict; it can never grant. The failure mode is silent: content that reads like an operator instruction gets treated as one because nobody attached the label, and there is nothing in the text itself to attach it from.

**Diagnostic:** point at any sentence in the context and ask which class it is. If you can only answer by reading what it says, the labels do not exist and the ladder is not being enforced.

## The exfiltration triangle

A leak needs three ingredients in the same run: **sensitive data in context**, **untrusted content in context**, and **an egress path the agent can reach**. Any two are survivable. All three at once is a live vulnerability regardless of how well the prompt is written, because the attacker supplies the second ingredient and the first two together mean the third will be used.

The ingredient teams underestimate is the third, because egress rarely looks like egress: a markdown image the client fetches, a link a user is invited to click, a comment posted on a public ticket, a DNS lookup for a subdomain built from the data, a commit message, a filename, an error string.

**Diagnostic:** for each of the three ingredients, name the specific decision that put it there and who made it. If all three are present and no one saw the combination, that is the finding — the triangle assembles from reasonable local choices.

## The actuator boundary

Reading is not the dangerous act; acting is. A model persuaded by a hostile document has done nothing yet. The security-relevant moment is when a decision becomes a tool call, a credential use, a write, or a send. Everything this pack asks for lives at that moment: the provenance check, the scope, the allowlist, the gate.

This relocates the whole problem usefully. Trying to keep the model from being persuaded is an unbounded fight against language. Deciding what the actuator will execute is a bounded engineering problem with a component you own on the other side of it.

**Diagnostic:** draw the line in the architecture where a generated token becomes an effect in the world. Every control in the design should be on that line or beyond it. Controls upstream of it are mitigations.

## Mitigation versus control

A **mitigation** reduces how often an attack succeeds. A **control** bounds what happens when it does. Instructional hardening, delimiters, and injection classifiers are mitigations — useful, worth having, and adjudicated by the component under attack. Scoped credentials, sandboxes, egress allowlists, and approval gates are controls — enforced by something the attacker's text cannot address.

Systems fail here by accumulating mitigations until the list looks like a defense. Five mitigations and no controls is a hit rate, not a floor.

**Diagnostic:** for each defense in the design, name the component that enforces it. Sort into two columns. If the control column is empty, the system's worst case is unbounded and nobody has noticed.

## The confused deputy

An agent holds permissions its users do not. When a request arrives and the agent asks "am I allowed to do this?" instead of "is the person asking allowed to have this done?", an unprivileged requester gets a privileged action performed for them. Every check passes. The logs show a trusted service doing something it is authorized to do. The attack is invisible precisely because nothing was bypassed.

Indirect injection makes this sharper: the "requester" may be a document, which is a principal with no permissions at all.

**Diagnostic:** for each privileged tool call, ask whose permissions were checked. If the answer is the agent's, you have a confused deputy waiting for someone to notice.

## The blast-radius envelope

An agent's risk is not its behavior; it is the union of what its credentials, tools, filesystem access, and network reach permit. A successful injection is a temporary transfer of that whole envelope to whoever authored the text the agent read.

Held this way, permission stops being a convenience question. Every tool left in the default set because removing it was inconvenient is a line item in the incident report you have already written.

**Diagnostic:** list everything the agent can do, from configuration alone, without reading its prompt. That list is your worst case. If it is longer than the task needs, the excess is pure loss.

## The sleeper fact

A false claim written into persistent memory has a dwell time. It is read in a later session, by a different user, on a different task, with no trace of its origin, and it is trusted because it is in the store where trusted things live. Later reasoning appears to corroborate it and is in fact derived from it. Verification against the record confirms it, because the record is what was poisoned.

This is why writes deserve gates that reads do not, and why provenance has to survive into storage: without it there is no way to answer the only question that matters after a compromise — what else did we believe because of that.

**Diagnostic:** pick a fact in the agent's memory and ask where it came from and when it expires. If the store cannot answer, every fact in it is unbounded in both age and origin.

## The rubber stamp

An approval step is worth what it displays. An interface showing the agent's summary of an action asks the human to ratify a description written by the component under attack. Two further failures live in the same place: an approval whose parameters are regenerated after the click, and an approval requested so often that clicking yes becomes reflex.

A gate that fires constantly and a gate that shows nothing fail the same way — they produce the appearance of human oversight without the substance.

**Diagnostic:** read the approval surface for a real action. Can you tell, from the screen alone, exactly what will happen — the command, the recipient, the amount, the records? If not, this is decoration.

## The tool description as a second system prompt

Tool names, parameter descriptions, and usage notes go into the model's context and shape its decisions. They are prompt content authored by whoever maintains the server. A tool that was benign at review time and hostile after an update changed the system prompt without touching the repository. This is what makes an agent's toolset a supply chain rather than a config file: part of the payload is natural language aimed directly at the model's judgment.

**Diagnostic:** print the full text of every tool description currently loaded and read it as if it were the system prompt — because that is its effect. Ask who can change it and how you would know.

## The gate is set by the action, not the confidence

An agent's confidence is a property of its generation, not of the world, and it is exactly as high after a successful injection as before one. What determines the gate an action needs is the action: whether it can be undone, and whether its effect leaves the system to reach a person, an account, or a third party.

| | Internal | Externally visible |
|---|---|---|
| **Reversible** | Autonomous | Autonomous, logged and reviewable |
| **Recoverable** | Autonomous, logged | Approval or staged execution |
| **Irreversible** | Approval | Approval, always |

**Diagnostic:** place every tool the agent can call in one of the four cells. Any tool in the bottom row or right column running autonomously is a finding with a known fix.

## The reconstruction test

After a suspected compromise there is exactly one question, asked five ways: which tools ran, with which arguments, on whose behalf, prompted by which content, and what came back. A system that can answer these has an incident. A system that cannot has an unbounded worry — it cannot scope the damage, cannot tell which data moved, and cannot verify that the fix worked.

**Diagnostic:** take a run from last week and reconstruct it from the logs alone. Whatever you cannot reconstruct is what you will not know during the incident.
