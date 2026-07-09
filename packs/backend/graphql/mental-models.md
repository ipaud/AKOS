# Mental Models — GraphQL Pack

- **The N+1 problem:** a naive resolver fetching each related object individually (one query per parent row) turns a list query into N+1 database round trips; batching (DataLoader pattern) collapses it to a handful.
- **Schema as a contract, not a database mirror:** the GraphQL schema should model the domain/client needs, not directly expose internal database table shapes (same discipline as [DDD anti-corruption layers](../../architecture/domain-driven-design/mental-models.md)).
- **Query cost as an unbounded resource by default:** unlike REST's implicitly bounded endpoints, a GraphQL query's cost is determined by the client's query shape — nested/recursive queries can be arbitrarily expensive unless explicitly bounded.
- **Resolvers as the real API surface:** the schema defines shape; resolvers define authorization, data-fetching, and cost — field-level authorization ([API3](../../security/owasp-api-top-10/mental-models.md)) lives here.
