# Heuristics — Game Accessibility Pack

Defaults with known exceptions. Use while deciding; the
[engineering rules](engineering-rules.md) apply once the game exists.

- **Space repeated flashes a third of a second apart and stop thinking about area.** At or
  under three a second, full-screen white is within the limit. The maths only matters for
  small effects that flicker faster.
- **Start a flash effect darker than you want it.** A tint or a smaller burst usually feels
  nearly as strong, and it leaves room for two effects landing at once.
- **Inventory flashes from the player's worst moment, not from the code.** Three hits and a
  super in one second is the case that fails, and no single call shows it.
- **Convert to millimetres before arguing about a font.** Panel width in pixels over panel
  width in mm gives density. Most disagreements about small text end there.
- **Read on the device, in the room's normal light, at arm's length, at each brightness.** A
  screenshot on a monitor is enlarged and backlit. It flatters small text every time.
- **Look at it in grayscale first.** Cheap, and it catches most colour problems. Run the
  simulated colour vision pass afterwards.
- **Pick the meaningful colour pairs before the palette is finished.** Danger against floor,
  ally against enemy, on against off. Changing a tone later means redrawing tiles.
- **On few buttons, design the plain press route first.** Add long press and chords as
  shortcuts over a menu that already reaches everything. Reversing that order leaves actions
  that only a gesture can reach.
- **If a gesture needs a hint on every screen, it is holding too much.** Move the action into
  a menu.
- **Show that the press landed before doing the slow work.** A mark on the button or an LED
  blink tells the player not to press again. Silence during a card read invites a double.
- **Test input with the machine busy on purpose.** A press test on an idle screen proves the
  easy case. Run it during a save, a load, and garbage collection.
- **Assume the speaker is worse than you think.** Small speakers lose low notes. A cue that
  relies on bass or quiet detail is not there. Listen on the device, then turn it off and
  play again.
- **Give every effect one volume knob, including shake.** One scale value set to zero beats
  twenty conditionals, and it can be reviewed by reading one function.
- **Keep the HUD off the shaken camera.** Numbers must stay still enough to read, whatever
  the world does.
- **Keep reading text still.** Wobbling letters are for titles and shouted words, not for
  anything the player must parse.
- **Make the first thing on screen safe, not configured.** A first launch meeting the rules
  beats a settings wizard. A wizard is fine, as long as it can be operated and read before
  anything else.
- **Let text wait for a press.** It removes most timing questions in one decision.
- **Ask what a two-week absence costs, then read the answer back in the game.** Run the
  clock forward in a test. If the answer is gone, decide whether that is the game you want
  to hand someone.
- **Bring the player back with what happened, once, without guilt.** A summary with no
  blame costs nothing. Exception: an in-fiction consequence can land hard, as long as it is
  recoverable and the copy does not scold the person.
- **Never trust the clock on a device without a clock.** Lost time must read as unknown, not
  as neglect.
- **When a game is for one known person, ask about them.** A gift has one player; their eyes,
  hands, and routine beat any average. Exception: floor rules hold regardless, since
  a person cannot tell you about a seizure risk they do not yet know they have.
- **Write the difficulty decision down, whichever way it goes.** A one-line reason is the
  whole requirement.
- **Say what is missing.** A short honest list is more useful to a player than a warm
  paragraph about inclusion.
