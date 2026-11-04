# Heuristics — MicroPython Pack

Defaults with known exceptions. Use while deciding; the
[engineering rules](engineering-rules.md) apply once the code exists. All of these are AKOS's own
judgment, built on the documentation where it speaks.

- **Before believing a number, ask where it was taken.** Board, firmware, commit, scene. A number
  with no address is an opinion. Exception: none on the board side. For pure logic, a host
  result is fine and the question does not arise.
- **Look at the worst frame, not the typical one.** Players feel spikes. A steady frame with an
  occasional one three times longer plays like the long one at the moment that matters.
- **Suspect the allocation first when a frame budget slips.** Then the file read, then the
  drawing. Allocation is usually the cheapest to remove, and removing it delays the next
  collection too.
- **Collect when the player already expects a pause.** Scene change, load, screen off, the end of
  a day. Exception: a small heap, where the documentation's frequent short collections do work.
  Measure which case you are in.
- **The bigger the heap, the less you want to collect by hand in the loop.** Megabytes of PSRAM
  feel like freedom and arrive with a pause many frames long. A heap that large buys room, not
  time.
- **Fix the allocation rate before tuning `gc.threshold`.** The threshold moves the pause around.
  Reducing garbage removes it.
- **Keep one buffer per job, made at startup.** If a function needs scratch space every frame,
  it wants a preallocated buffer on its object.
- **Reach for `memoryview` the moment a slice only feeds another call.** A slice that is just
  passed along should not be a copy. Do not resize what a memoryview points at.
- **Treat every callback as if it were hard, even on a port where it is soft.** The code then
  survives a port change, and the discipline keeps handlers short. Exception: a callback you
  have measured and that needs a library call only available with allocation.
- **Ask what happens to an event during the longest stall you know of.** If the answer is "it is
  gone", and it matters, it needs a hardware counter or a queue outside Python.
- **Assume the bounce.** A mechanical button makes several edges. A hardware filter and a
  decoder that reads stable state beat one callback per edge.
- **Trust neither the ticks nor the clock over a long weekend.** Anything left running for days
  needs a thought about the half-period limit, and anything off for hours needs one about what
  time it now believes it is.
- **Write a smoke test before believing a filesystem.** A ten-line script on the real volume
  settles what rename does there. The documentation does not, and a code comment certainly does
  not.
- **Prefer two slots to one clever file.** Alternating copies survive what no single-file scheme
  can, including a bug in the swap. Atomic replace is a good second layer, not a substitute.
- **Keep saves off FAT if the save can wait.** Faster saves on a card are a real gain, and an
  equally real exposure. If frequent card saves win, copy to LittleFS at every natural pause.
- **Read the file as if a stranger wrote it, because one might have.** A card leaves the device,
  and a save is the largest structured input most games parse.
- **Put limits next to the loops they protect.** Any stored number that sizes a list or counts
  iterations needs a ceiling before it is used.
- **Run the core under MicroPython before you run it on the board.** The unix port finds missing
  modules in seconds, for free. Then remember it has a different heap, clock, and filesystem.
- **On a board you cannot reach, plan for the hang, not only the crash.** An exception is the easy
  failure. A loop that never returns needs a watchdog or a stated gap.
- **Freeze late.** Frozen bytecode saves RAM and costs a firmware flash for every change, so it
  suits code that has stopped moving. On a PSRAM board, RAM may not be the reason at all.
- **Rewrite the record when the words outrun the test.** If a log says "cut" and the script said
  `machine.reset()`, change the word today. Records turn into beliefs within weeks.
