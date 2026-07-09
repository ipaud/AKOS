# Mental Models — Design Systems Pack

- **Token pyramid:** reference tokens (raw palette/scale values) → system/semantic tokens (roles: `color.text.primary`) → component tokens (`button.primary.background`). Consumers use the top layer; theming happens in the middle.
- **API surface as a promise:** a component's props are a contract; every prop added is a permanent-feeling commitment (removing later breaks consumers) — design the API deliberately, not incrementally by accretion.
- **Documentation as the system's actual interface:** an undocumented component might as well not exist — developers will reimplement rather than discover it.
- **Governance model:** who can add/change tokens and components, and how — without this, systems drift into inconsistency as fast as they were built.
