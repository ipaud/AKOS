# Decision Framework — Game Accessibility Pack

The choices this domain presents, and how to settle each one.

## Who owns it?

Every finding carries an owner (P5).

| Question | Answer → owner |
|---|---|
| Would every game need the same code? | Yes → **engine** (text scale, remap, volume plumbing, input capture) |
| Does it depend on what this game asks of a player? | Yes → **game** (a timed section, a colour puzzle, effect choice) |
| Engine offers the plumbing, game must use it? | **both**; name which half is missing |
| Engine lacks it, and one game needs it now? | Game may build it; the engine gap stays recorded (P7) |

## What does this surface change?

| Surface | Fixed truths | Walk changes |
|---|---|---|
| Fixed device, many buttons | No other input device; firmware can permute buttons | Remap is at most a swap (GAX14) |
| Fixed device, few buttons | Gestures carry the load | Plain press route replaces remap (GAX10); busy-state input test (GAX12) |
| Desktop | Keyboard, pad, any window size | Full remap (GAX14); test the smallest supported window |
| Web | Keyboard or touch; page shell around the canvas | Shell falls under [ux/wcag](../../ux/wcag/README.md); on a phone, use the held-device limits |

Unshipped surfaces are `n/a`. A shipped surface is reviewed even if it is not the favourite.

## The five walks

These replace WCAG's keyboard walk inside a rendered game. Each records surface, build, evidence
label (GAX41), and who ran it. A walk can pass, fail, or stay `unverified`; only the first is a pass.

| Walk | Method | Artifact | Who |
|---|---|---|---|
| **Control** | Default bindings, the surface's standard input only. Start, play the primary task, pause, leave each screen. Then list every action and find its plain press route. Repeat presses with the machine busy. | Scripted route; sent vs received press log | Agent for logic; **person on hardware** for feel and input capture |
| **Read** | At real size on real pixels, at arm's length: every screen with text, HUD, icons, at each brightness. | Screenshots for overflow and contrast; signed note for legibility | Agent for contrast and overflow; **only a person on the panel** for legibility |
| **Sound-off** | Muted, on the real output as well: finish the primary task. Then listen at default volume: are the cues there on this speaker? | Cue list with each cue's visual counterpart | Agent for the list; **person on hardware** for audibility |
| **Colour** | Grayscale pass, then simulated protan, deutan, tritan, on screens with meaningful pairs. | Screenshot set, pair table with contrast | Agent |
| **Flash** | Every displayed frame across the GAX7 route, general, red, pattern. | Result naming tool, limit, route, rate | Agent; a person checks backlight and LED on hardware |

Thresholds use the panel in use. A simulator screenshot is HOST evidence: it can fail text (clipped,
low contrast), but never pass legibility.

## What is floor?

| Floor, CRITICAL everywhere | Not floor |
|---|---|
| Flash rate, area, red, patterns, default-safe (GAX1 to GAX5) | Remap, gestures, hold lengths (HIGH at most) |
| Cannot complete, or trapped (GAX9) | Text size and scale (a person's read walk decides) |
| Essential text below contrast (GAX20) | Subtitle styling, volume categories |
| Single-channel cue blocks the primary task (GAX25) | Difficulty, assists, absence, narration |

Dropped presses are HIGH, and become GAX9 only if they stop the primary task or an exit. Screen narration
is a recorded gap: the constitution's screen-reader clause cannot be met inside a framebuffer with no
tree or speech, and treating it as floor would block every such game for a reason no game can fix. It
is declared (GAX40), and the maintainer should confirm this reading.

## Flash limit, worked

The sources disagree on area, and each number has a context. BT.1702-3: 25 % of the screen, for a
television, with advice to sit at least 2 m away. Xbox 118: about 20 %. WCAG: 0.006 sr in any 10-degree
field, approximated by 341×256 at 1024×768, which is 25 % of that rectangle and 2.8 % of the frame.

A whole handheld fills less of the visual field than a monitor, but the same panel area spans a bigger
angle as it comes closer. WCAG says plainly that closer viewers are affected by areas that pass. So
*AKOS derives* physical area from the angle: `limit_cm² = 0.006 × d²`; share = limit ÷ panel area.
The 20 cm is an AKOS assumption for a closest plausible distance: a child, a low-vision player, a
bedtime hold. Valve assumes 30 cm for reading.

| Panel | Area | Limit at 20 cm | Limit at 30 cm | 25 % of screen at 20 cm is |
|---|---|---|---|---|
| 2.8 in, 4:3 | 24.3 cm² | 2.4 cm², 9.9 % | 5.4 cm², 22 % | 2.5 × limit |
| 3.5 in, 3:2 | 36.5 cm² | 2.4 cm², 6.6 % | 5.4 cm², 15 % | 3.8 × limit |
| 5.5 in, 16:9 | 83.4 cm² | 2.4 cm², 2.9 % | 5.4 cm², 6.5 % | 8.7 × limit |
| 7 in, 16:10 | 142 cm² | 2.4 cm², 1.7 % | 5.4 cm², 3.8 % | 15 × limit |
| WCAG reference | 1024×768 | 2.8 % of frame | | |

The limit matters only above three flashes a second; at or under, content passes whatever its size.
Count flagged area over the whole frame rather than sliding a 10-degree window: stricter and simpler.
Patterns (GAX4) have no angular source, so that rule keeps a share of the screen.

## Check a captured frame sequence

Capture every displayed frame in sequence, then run this. It was tested against synthetic sequences:
full-screen flicker at 6/s and 3.5/s fails, at 3/s passes; a red flash below luminance limits fails
the red test only; a 2-pixel checkerboard flip averages out; an 8-pixel one does not. It is a screening
aid, not a certified analyzer such as PEAT or Harding, and it has not been compared with one.

```python
from collections import deque
import numpy as np

LUMA = np.array([0.2126, 0.7152, 0.0722])

def _linear(rgb):                       # H x W x 3 floats, 0..1 sRGB
    return np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)

def _uv(lin):                           # CIE 1976 u', v' from linear sRGB
    x = lin @ np.array([0.4124, 0.3576, 0.1805])
    y = lin @ LUMA
    z = lin @ np.array([0.0193, 0.1192, 0.9505])
    d = np.maximum(x + 15 * y + 3 * z, 1e-6)
    return 4 * x / d, 9 * y / d

def _blocks(a, b):                      # mean over b x b pixels, about 0.7 mm: fine dither cancels
    h, w = a.shape[0] // b * b, a.shape[1] // b * b
    return a[:h, :w].reshape(h // b, b, w // b, b, 3).mean(axis=(1, 3))

def worst_flash_share(frames, fps=60, block=4):
    """Largest share of the frame, 0..1, over three flashes in a second: (general, red)."""
    gen, red, state = deque(maxlen=fps), deque(maxlen=fps), None
    worst_g = worst_r = 0.0
    for frame in frames:                # uint8 H x W x 3, every displayed frame; fps as displayed
        lin = _blocks(_linear(frame.astype(float) / 255), block)
        lum, (u, v) = lin @ LUMA, _uv(lin)
        sat = lin[..., 0] / np.maximum(lin.sum(axis=2), 1e-6) >= 0.8
        if state is None:
            state = dict(ext=lum, dirn=np.zeros(lum.shape, int), u=u, v=v, sat=sat)
            continue
        ext, dirn = state["ext"], state["dirn"]
        rise = (dirn <= 0) & (lum - ext >= 0.1) & (ext < 0.8)
        fall = (dirn >= 0) & (lum - ext <= -0.1) & (lum < 0.8)
        further = ((dirn == 1) & (lum > ext)) | ((dirn == -1) & (lum < ext))
        gen.append((rise & (dirn == -1)) | (fall & (dirn == 1)))
        hit = (np.hypot(u - state["u"], v - state["v"]) > 0.2) & (sat | state["sat"])
        red.append(hit)
        state = dict(ext=np.where(rise | fall | further, lum, ext),
                     dirn=np.where(rise, 1, np.where(fall, -1, dirn)),
                     u=np.where(hit, u, state["u"]), v=np.where(hit, v, state["v"]),
                     sat=np.where(hit, sat, state["sat"]))
        worst_g = max(worst_g, (np.sum(gen, axis=0) > 6).mean())
        worst_r = max(worst_r, (np.sum(red, axis=0) > 6).mean())
    return float(worst_g), float(worst_r)       # each must not exceed the GAX2 share
```

More than six transitions in a second is more than three flashes. Luminance here assumes sRGB-like
output; a real panel's response differs, and scrolling produces false candidates that need a look
(GAX6). For a slow target, pass the rate measured on the device as `fps`.

## Text size, worked

Density = screen pixels across ÷ panel mm across. Minimum 1.06 mm, aim 1.41 mm (GAX21); Valve does not say
how it measures "character" height, so AKOS reads it as the smallest letter height in use, x-height if
lowercase appears. Xbox's 4.6 mm is ascender to descender, a different measure, so the two do not
convert directly.

| Panel | Density | 1.06 mm | 1.41 mm | 4.6 mm body |
|---|---|---|---|---|
| 240 px over 43 mm | 5.6 px/mm | 6 px | 8 px | 26 px |
| 480 px over 74 mm | 6.5 px/mm | 7 px | 10 px | 30 px |
| 1280 px over 151 mm | 8.5 px/mm | 9 px | 12 px | 39 px |

## Colour on a restricted palette

Do not rely on colour alone for anything the player must act on: danger vs safe, ally vs enemy, on vs
off, match vs no match, collected vs not. An invented 4-tone ramp, `#E8F0C8 #98B070 #486848 #182820`,
shows the constraint: outer tones reach 13:1, text pairs with the second-lightest step on dark at 6.4:1,
but neighbouring steps give only 2.0 to 2.6:1. So neighbours cannot carry a state on their own. An
invented 16-colour red `#C83C3C` and green `#3C8C3C` look opposite, yet sit at 1.2:1: in grayscale they
are one tone, and a player with a red-green difference may get nothing else to go on.

Test: list the meaningful pairs, compute their contrast, then look at grayscale and simulated CVD shots
of those screens. A pair passes at 3:1 or with a second signifier (GAX26). Any maintained simulator will do;
a display filter for players is not a simulation (GAX47).

## Juice versus readability

Ruled: accessibility wins (P14). Effects that can harm or block reading are optional or capped.

1. Would this effect fail GAX1 to GAX5 at its worst stack? Remove or reduce it. No option can fix it.
2. Does it move something the player must read? Keep that thing out of it (GAX32).
3. Can it cause nausea or discomfort? It goes through the gate (GAX31), and default strength is a design
   choice the player can take to zero.
4. Otherwise it stays. This pack is not against feel.

## Difficulty and assists

State the position, then stop (P17). Hard games are legitimate. An assist never needs moral defence, and
neither does leaving one out. Record the decision (GAX37). Where a game wants assists, cheap ones first:
game speed, skip, more saves, longer windows, a lower-damage mode, then a story mode. Xbox's advice for four
presets, adjustable mid-game, and an ultra-low mode is good and it is advice, not a requirement here.

## Time pressure

| Kind | Example | Ruling |
|---|---|---|
| In the challenge | A race countdown | Exempt from GAX24, listed; assist is a GAX37 decision |
| In reading or menus | A dialog that vanishes | GAX24 |
| Wall clock | A pet hungry while you are in hospital | GAX34 to GAX36; AKOS position, HIGH at most |
| Live multiplayer | Lobby countdown | Exempt: extending it affects others |

Absence checks for a wall-clock game: what is lost after a day, a week, a month? Can it be regained? Could a
person who never saw this coming recover? A game may keep real stakes, such as a character's natural
lifespan, when the player chose them knowingly and absence alone does not decide the ending.

## Profile modulation

- **Prototype** — the eight floor rules on the surface in hand, plus a list of known gaps.
- **Game Dev** — floor rules plus High, all five walks on the primary surface, gaps recorded.
- **Startup MVP** — the same across every shipped surface.
- **Production / Enterprise** — full checklist, plus the declaration (GAX40).

## When NOT to use this pack

- **The surface is a web page, launcher, or form.** That is [ux/wcag](../../ux/wcag/README.md).
- **The question is legal compliance.** No source here answers it (P19).
- **Someone wants the game called accessible.** Report walks and gaps instead.
- **The game is a paper design.** Use the heuristics; walks need a build.
