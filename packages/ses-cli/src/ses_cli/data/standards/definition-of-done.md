# Definition of Done

Done criteria by change path. When unsure which path applies, use the stricter one. When unsure about sensitive: **treat as sensitive**.

## Tiny

Typos, copy, pure CSS, trivial one-line fixes.

- [ ] Change implemented
- [ ] Light `ses check` (or equivalent) if the project has it
- [ ] No feature plan required

## Normal feature

- [ ] Short plan via `/feature-planning` (goal, approach, files/areas, risks, how to verify)
- [ ] Implemented via `/feature-implementation` within agreed scope
- [ ] Tests for the change
- [ ] Architecture/docs updated if behavior or boundaries changed
- [ ] `ses check` (or equivalent) run; evidence reported
- [ ] Fresh pass via `/independent-review`
- [ ] You can explain the important execution flow

## Sensitive

Same as normal, plus:

- [ ] Plan labeled **risk: sensitive** with blast radius
- [ ] **Human approved the plan** before implementation
- [ ] Review used the security-minded checklist
- [ ] No production/destructive action without explicit human approval

Sensitive triggers: auth/authz/tenant isolation, payments, PII, crypto/secrets, destructive data/migrations, production config/access control.

## Not Done

- Checks “probably fine” without running them
- Scope crept without re-planning
- Docs drift after a behavior change
- Sensitive work shipped without plan approval

## Related

- Principles: `engineering-principles.md`
- Security: `security-baseline.md`
- Verification: `testing-and-verification.md`
