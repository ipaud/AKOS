# Glossary — SEO Pack

Terms this pack uses precisely. Several are used loosely in the wider domain; the entry
says which sense is meant here.

- **Crawling** — fetching a URL. Controlled by `robots.txt`, authentication, and status
  codes.
- **Indexing** — including a fetched page in the searchable set. Controlled by `noindex`.
  Separate from crawling, and confusing the two is the domain's classic self-inflicted
  wound.
- **Rendering** — executing a page's JavaScript to produce the HTML that is actually
  assessed. The stage where client-only content disappears.
- **Discovery** — how a URL becomes known at all: internal links, sitemaps, external links.
- **Serving** — how an indexed page appears in results. Where this pack stops.
- **`robots.txt`** — a fetch-control file (RFC 9309). It does not remove already-known
  URLs, and a page blocked by it cannot be read to discover a `noindex` directive.
- **`noindex`** — a directive excluding a page from results. Requires the page to remain
  fetchable to be effective.
- **Canonical** — a declaration of which URL represents a piece of content. A *hint* weighed
  against internal links, sitemaps, and redirects, not a command.
  `core/conflict-resolution.md` uses "canonical ruling" in an unrelated sense.
- **Self-referencing canonical** — a page declaring itself canonical. The default for every
  indexable page.
- **Duplicate content** — the same content reachable at more than one URL. Usually
  accidental: protocol, host, trailing slash, case, or tracking parameters.
- **Crawl budget** — the finite attention a site receives. Spent on whatever URL space you
  expose, which is why unbounded parameter combinations are a structural problem rather
  than a directives problem.
- **Soft 404** — a page returning 200 while saying nothing is there, including a
  bulk-redirect of removed content to the homepage. Keeps a dead page indexed.
- **Redirect map** — the mapping from every previously indexable URL to its specific
  replacement, built before a migration from analytics and logs.
- **Structured data** — machine-readable markup describing a page's content, typically
  schema.org vocabulary. Buys *eligibility* for an enhanced result, never placement.
- **Rich result / enhanced result** — an augmented search listing. Eligibility is not
  entitlement, and its absence is not a markup bug.
- **`hreflang`** — annotations declaring language and regional variants. Must be reciprocal
  and self-referencing, or they are ignored.
- **Mobile-first indexing** — the mobile rendering is the version assessed. Distinct from
  *mobile-first CSS*, which is
  [mobile/responsive-web](../../mobile/responsive-web/README.md) and a different idea.
- **Page experience** — loading, stability, interactivity, HTTPS, no intrusive
  interstitials. Owned by
  [performance/core-web-vitals](../../performance/core-web-vitals/README.md); this pack
  points there rather than restating it.
- **Cloaking** — serving different content to crawlers than to people. A floor violation
  before it is a policy violation.
- **Ranking factor** — a claimed input to result ordering. Unpublished, therefore Level 4,
  therefore absent from this pack entirely.
