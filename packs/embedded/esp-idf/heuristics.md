# Heuristics — ESP-IDF Pack

Defaults with known exceptions. Use while deciding; the
[engineering rules](engineering-rules.md) apply once the code exists.

- **Measure before moving anything.** A placement argument without a number is a guess, however
  well read.
- **Ask what runs out first, and it is usually internal RAM.** Watch the largest block, and expect
  the radio to be the first casualty.
- **Treat the two cores as sharing one straw.** Whatever one does to PSRAM, the other pays for.
- **Copy rows, not frames.** PSRAM-to-PSRAM copies are the slowest path on the board; copy only
  what the next step reads.
- **Keep what the pixel loop reads under the cache size.** Past it, cost can jump rather than grow.
- **Avoid 64-bit division and `double` in per-pixel loops.** Both are software on this chip. A
  table of precomputed values is usually the fix.
- **Check what the compiler did to your hot loop.** It may turn a copy into a library call.
- **Raise stdio buffers before blaming a card.** The 128-byte default makes FAT reads crawl.
- **Set a stack from what it used, and re-measure after adding a feature.**
- **If it would be fine for a task to die silently, ask why the task exists.**
- **Keep power management off in a frame-locked game unless battery life demands it.** It adds
  interrupt latency, and light sleep can drop the USB console.
- **Read the generated `sdkconfig`, not the defaults file.** What was built is what the board got.
- **Before any eFuse, ask what recovery remains afterwards.** If the answer is "nothing", stop.
- **Plan for three boards:** one that stays open, one you are willing to destroy, one final.
- **Keep the fixed layer boring.** Everything that can be changed later should be, and the rest
  should be small enough to read in a sitting.
- **Write the recipient's failure out loud:** "the screen is frozen, and she doesn't know why." If
  the design needs her to power-cycle three times, it has no recovery.
- **Ship the diagnosis before you need it.** The update that adds it can be the one that doesn't
  arrive.
- **Do not start an update on a low battery, even if the design survives a cut.** Surviving and
  wasting a trial boot are different outcomes.
- **Rehearse from the version in the field, not the one on your desk.**
