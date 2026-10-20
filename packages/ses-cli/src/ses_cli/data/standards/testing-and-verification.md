# Testing and Verification

What “verified” means in SES. Local checks only — not GitHub Actions as a SES feature.

## Verified means

You have evidence that the change does what you claim:

1. Relevant automated checks ran and passed (when configured), **or**
2. A short manual verification note: what you did, what you saw, what remains untested

“Should work” and “looks fine” are not verification.

## Local checks (`ses check`)

Each product gets a `ses.toml` at init with the menu it needs (format, lint, typecheck, tests, secret-pattern scan, optional arch-doc presence for commercial posture).

```bash
pip install ses-cli   # or: pip install -e packages/ses-cli from the kit repo
ses check             # from the product root (directory with ses.toml)
# or:
ses check --path /path/to/product
```

| Exit | Meaning |
|------|---------|
| 0 | Pass |
| 1 | Fail |
| 2 | Not configured |

Rules:

- Meaningful exit codes
- **Not configured ≠ pass**
- No secret leakage in output
- You run it locally; SES does not push or open PRs

If `ses check` is missing or exit 2, say so plainly and fall back to the project’s native commands (or manual notes).

## Expectations by path

| Path | Verification |
|------|----------------|
| Tiny | Light check if configured; otherwise quick sanity |
| Normal | Tests for the change; `ses check` (or equivalent); you can explain the important flow |
| Sensitive | Same as normal, plus security-minded review; human-approved plan |

## Don’t

- Claim checks passed without running them
- Treat missing config as a green light
- Skip tests on normal/sensitive features because “it’s obvious”

## Related

- Done criteria: `definition-of-done.md`
- Implementation evidence: `/feature-implementation`
- Review of gaps: `/independent-review`
