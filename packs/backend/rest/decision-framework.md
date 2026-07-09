# Decision Framework — REST Pack

Offset vs cursor pagination: small stable datasets → offset (simpler); large/frequently-changing datasets → cursor (avoids skip/duplicate issues from concurrent inserts). Versioning strategy: URL path versioning (`/v1/`) is simplest and most cache-friendly; header-based versioning is cleaner for URL stability but harder to test/debug manually — pick URL path unless there's a specific reason not to. REST vs GraphQL: see [graphql decision-framework](../graphql/decision-framework.md) for the comparative call.
