# Examples — NIST SSDF Pack

## Named ownership (NS2)

```markdown
## Security Ownership
- Dependency updates: @alice (weekly Dependabot review)
- Security code review: rotating, tagged via CODEOWNERS on /auth, /payments
- Vulnerability response: security@ourcompany.com, triaged by @bob within 48h
```

## CI dependency scanning (NS3)

```yaml
# .github/workflows/security.yml
- uses: actions/dependency-review-action@v4
- run: npm audit --audit-level=high
- uses: gitleaks/gitleaks-action@v2
```

## Disclosure channel (NS10)

```
# /.well-known/security.txt
Contact: mailto:security@ourcompany.com
Expires: 2027-01-01T00:00:00Z
Preferred-Languages: en
Policy: https://ourcompany.com/security-policy
```

## Threat model before implementation (NS7)

```markdown
## Feature: bulk data export
Threats considered:
- Unauthorized export of other tenants' data (mitigation: scope query to
  tenant_id, verified server-side)
- Export used as a DoS vector (mitigation: rate limit + async job queue,
  not synchronous unbounded query)
- Exported file accessible via guessable URL (mitigation: signed,
  time-limited download URLs)
Written and reviewed before implementation started.
```

## Severity-based patch SLA (NS11)

```
Critical (remote code execution, auth bypass): patch within 24-48h
High (data exposure, privilege escalation): patch within 1 week
Medium: next regular release cycle
Low: backlog, batched
```

## SBOM generation in CI (NS5)

```yaml
- run: syft packages dir:. -o cyclonedx-json > sbom.json
- run: cosign attest --predicate sbom.json ${{ env.IMAGE }}
```
