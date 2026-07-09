# Decision Framework — Refactoring UI Pack

## Emphasis decision

Something needs to stand out →
1. Can neighbors be quieted (RP2)? Do that first.
2. Still needs lift → one property at a time: weight, then color, then size. Stop at the first that works.
3. Reaching for the accent color → check the screen's accent budget (one per surface); if spent, reprioritize which element deserves it.

## Separation decision

Two things need visual separation →
whitespace (RP8 ratios) → background shift → shadow → border. Take the lowest rung that reads. Table rows and form sections rarely need lines; cards rarely need borders *and* shadows.

## Palette construction (new project)

1. Personality dials first (tone/energy/formality — see [mental-models](mental-models.md)); pick 1 primary hue + gray temperature accordingly.
2. Build ramps: 8–10 shades per hue, designed at the extremes (lightest usable bg, darkest usable text) then filled.
3. Precompute accessible pairs (RU6); name tokens by role (`text-primary`, `bg-subtle`), not by shade (`gray-300`) at the usage layer.
4. Semantic ramps (success/warning/danger) get the same treatment — including their accessible pairs.
5. Personal identity layer ([pau-avila design language](../../personal/pau-avila/design-language.md)) overrides hue choices, never floor rules.

## Type scale selection

UI-heavy product → hand-picked scale, 12–48px, more steps in the 14–24 zone.
Marketing/editorial → can stretch (up to 72+) with tighter heading spacing.
Never: modular scales generating fractional px; more than 2 font families without a strong identity reason (performance floor: [font-loading rules](../../performance/web-dev/README.md)).

## Density mode decision

Default: generous (RP6). Switch to dense when: users are daily-repeat professionals, data comparison is the core task, or screen real estate is operationally scarce (dashboards, trading, admin tables). Dense means a *tighter scale*, applied systematically — not removed whitespace.

## When to break your own system

A token value looks wrong in one specific composition →
1. Check if the composition misuses hierarchy (usually yes).
2. If genuinely needed, is it a new *system case* (e.g. "compact card" variant)? Add the variant to the system.
3. Never inline a one-off override; one-offs metastasize.
