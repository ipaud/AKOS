# Philosophy — Why "Don't Make Me Think"

## Cognitive load is the enemy

Users arrive with a goal and a limited budget of attention. Every element that demands interpretation — an ambiguous label, a clever name, an unconventional layout — spends that budget on *your interface* instead of *their goal*. Usability isn't decoration on top of function; it's the discipline of not taxing the user.

The tax compounds. One puzzling label is nothing. Ten small puzzles per page across a five-page flow is a user who leaves — often without being able to say why. Friction is felt cumulatively but inflicted incrementally, which is why it survives review: each individual sin looks minor.

## Usability as courtesy, not science

This school treats usability as common sense rigorously applied. You don't need a lab or a PhD to know that a button should look like a button and say what it does. What you need is the humility to accept that *you* are not the user: you know where everything is because you built it. The curse of knowledge is the default state of every team, and the only cure is watching real people use the thing.

## The goodwill reservoir

Every user starts with a reserve of goodwill. It drains when the site hides information, punishes them for its own convenience (forced registration, format-picky inputs), looks amateurish, or wastes their time. It refills when the site is obvious, honest, saves them effort, and recovers gracefully from their mistakes. Design decisions should be evaluated as deposits or withdrawals — and the reserve differs per user and per day. Design for the user arriving with the reserve nearly empty.

## Real use is messier than design assumes

People don't read pages; they scan. They don't weigh options; they pick the first plausible one (satisfice). They don't learn how things work; they muddle through with folk theories that work well enough. None of this is stupidity — it's rational time allocation: the interface is not their job. Design that fights this loses; design that embraces it (scannable hierarchy, forgiving choices, conventional patterns) wins.

## Testing over debating

Design arguments between team members ("users will/won't understand this") are usually two people generalizing from themselves. Three users thinking aloud for an hour settles most such arguments, cheaply, in the direction of reality. The point of testing is not proof — it's the steady supply of humbling, actionable surprises. Test early, test small, test often; fix the worst thing you saw; repeat.

## Where this philosophy stops

Krug's lens is *task usability on the web*. It doesn't cover visual craft (see [refactoring-ui](../refactoring-ui/philosophy.md)), deep interaction psychology (see [don-norman](../don-norman/philosophy.md)), or delight/brand. In AKOS, personality and identity are welcome (Level 0 preference) — *on top of* obviousness, never instead of it.
