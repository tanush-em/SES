---
name: feature-implementation
description: >-
  Implements an agreed or approved feature plan with tests, doc updates, and
  reported verification evidence. Use when implementing approved scope, coding
  a planned feature, or when the user invokes /feature-implementation.
disable-model-invocation: true
---

# Feature Implementation

Implement only the agreed/approved plan. Add tests and docs as required. Report evidence, not confidence.

## When to use

- A plan exists (from `/feature-planning` or an explicit user brief)
- Sensitive plans have **human approval** already
- User invokes `/feature-implementation`

## Inputs

- Approved/agreed plan (goal, files, verification)
- Path: tiny | normal | sensitive
- Product/module context (product repo with `ses.toml` when applicable)

## Steps

1. **Confirm scope** — If no plan, stop and run `/feature-planning` (or ask for a brief). If sensitive and unapproved, stop.
2. **Implement** — Smallest change that satisfies the plan. Match existing style.
3. **Tests** — Add/update tests for normal and sensitive paths. Tiny: usually none.
4. **Docs** — If behavior or boundaries changed, update architecture/README/security per documentation standards.
5. **Check** — Run `ses check` from the product root (or `ses check --path <dir>`) when `ses.toml` exists. Exit `2` means **not configured** (≠ pass). If the CLI is missing, say so and run native project commands or note manual verification.
6. **Report** — Evidence: commands run, exit outcomes, what remains untested.

## Prohibitions

- Do not expand scope beyond the plan without asking
- Do not claim checks passed without running them
- Do not touch production or perform destructive ops without explicit human approval
- Do not commit secrets or create real `.env` with secrets
- Do not silently skip doc updates after behavior changes

## Output template

```markdown
# Implementation: <short title>

## Done
- ...

## Files changed
- `path` — summary

## Tests
- added/updated: ...
- skipped (why): ...

## Docs
- updated: ... | none needed (why)

## Verification evidence
- command: `...` → pass | fail | not configured
- manual: ...

## Follow-ups
- ready for `/independent-review`
- open risks: ...
```

## Verification

- Scope matches the plan
- Evidence section is honest (including not configured)
- Done criteria for the path in `standards/definition-of-done.md` are addressed or listed as remaining

## Escalation

- Plan gaps discovered mid-flight → pause and re-plan with the human
- Sensitive surprise (hit auth/PII unexpectedly) → stop; treat as sensitive and get approval
- `ses check` exit 2 or CLI missing → report not configured; do not invent a fake CI

## Related

- `standards/testing-and-verification.md`, `standards/documentation.md`, `standards/definition-of-done.md`
