# Heuristics — Design Systems Pack

- A raw hex/px value appearing in a feature codebase outside the design-system package → should have been a token.
- A one-off component built inside a feature that resembles an existing system component → check if it should be a system component variant instead.
- A component prop list growing past ~8-10 props → API design smell, consider compound-component restructuring.
- Consumers copy-pasting a component and modifying it rather than using props/composition → the API doesn't support their use case; extend it deliberately.
