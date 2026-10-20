# Documentation

Keep docs **short and true**. Prefer updating existing docs over inventing new ones.

## Per-product docs

| Doc | Purpose |
|-----|---------|
| `README.md` | Setup, commands, `ses check`, config |
| `docs/architecture.md` | Components, boundaries, main flows |
| `docs/security.md` | Assumptions, sensitive areas (stub OK at init) |
| `docs/decisions/` | ADRs only for consequential choices |
| `.env.example` | Required env var **names** — no real values |

## When to update

- **Tiny** (typo, copy, pure CSS): usually no doc change.
- **Normal feature**: update `docs/architecture.md` (and README if commands/setup changed) when behavior or boundaries change.
- **Sensitive**: also ensure `docs/security.md` reflects new assumptions or blast radius.

Stale architecture docs are worse than short ones. If you change a main flow, update the doc in the same change.

## ADRs

Write an ADR under `docs/decisions/` only when the choice is consequential and hard to reverse (e.g. DB graduate to Postgres, auth model, multi-tenant boundary). Skip ADRs for routine implementation details.

## Understanding check

For significant features, you should be able to explain: request path, data changes, security boundary, how it’s tested, and failure behavior. Agents may quiz lightly; there is no fake certification ceremony.

## Related

- Done criteria: `definition-of-done.md`
- Skills that touch docs: `/feature-implementation`, `/independent-review`
