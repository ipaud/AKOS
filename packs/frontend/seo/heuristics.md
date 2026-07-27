# Heuristics — SEO Pack

Defaults with known exceptions. Use while deciding; the
[engineering rules](engineering-rules.md) apply once the page exists.

- **Ask which pipeline stage is failing before doing anything.** Discover, crawl, render,
  index, serve. Most "SEO work" is tags added to a page a crawler never fetched.
- **Fetch the page the way a crawler would and read what comes back.** Not view-source in a
  browser that already ran the JavaScript. This single habit catches most render-stage
  problems.
- **If a stranger should be able to land on it from a search result, put the content in the
  response.** Everything else is a performance decision.
- **Pick one URL form on day one and redirect the rest.** Protocol, host, trailing slash,
  case. Costs minutes at the start and a migration later.
- **Never combine `robots.txt` disallow with an expectation of de-indexing.** Blocked
  pages cannot be read to discover they asked to be excluded. It is the most common
  self-inflicted wound in the domain.
- **Keep preview deployments out of the index by configuration, not by memory.** Every
  branch URL is otherwise a full duplicate of production.
- **Write the title for the person scanning results, not for a parser.** If it reads like
  keywords, it is doing neither job.
- **Only add structured data where a documented enhancement consumes it.** Markup with no
  consuming feature is effort with no mechanism behind it.
- **Generate the markup from what the page renders.** Two copies of the same fact drift,
  and the drift is the one enforced violation in this domain.
- **Treat a URL change as a migration with a baseline, not as a refactor.** Capture indexed
  URLs and top landing pages *before*, or you will not be able to tell what broke.
- **Redirect to the specific replacement, never to the homepage.** A bulk homepage redirect
  is a soft 404 wearing a 301.
- **When advice says to trade user experience for crawler attention, distrust it.** Every
  technique of that shape has since been penalized. The interests align far more often
  than folklore claims.
- **Stop at "are we indexable".** Whether you rank is not something this pack — or anyone
  outside the search engine — can tell you.
- **On a login-only app, this is a five-minute exclusion check.** Confirm it is not
  indexable and move on; do not produce an audit of something with no public surface.
- **Assert indexability in CI for the routes that matter.** A `noindex` that appears by
  accident on a marketing page is invisible until traffic disappears a month later.
