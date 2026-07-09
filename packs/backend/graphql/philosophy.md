# Philosophy — GraphQL Pack

GraphQL trades REST's fixed-shape responses for client-specified queries — power that shifts cost risk from "did we build the right endpoint" to "did we bound what a client can ask for." A schema with no query depth/complexity limits hands every client the ability to construct an accidentally (or maliciously) expensive query; the flexibility that makes GraphQL valuable is exactly what makes resolver performance and query-cost governance non-optional, not nice-to-haves.
