---
name: independent-review
description: >-
  Reviews a diff and surroundings for defects, missing tests, and doc drift;
  applies a security checklist on sensitive changes. Use before calling a
  feature done, after implementation, or when the user invokes
  /independent-review.
disable-model-invocation: true
---

# Independent Review

Fresh pass over the change. Find issues; do not silently rewrite unless asked to remediate.

## When to use

- Before calling a normal or sensitive feature done
- After `/feature-implementation`
- User invokes `/independent-review` or asks for an independent review

## Inputs

- Diff and nearby code (read surrounding context, not only the patch)
- Plan and implementation evidence (if available)
- Path: tiny | normal | sensitive

## Steps

1. **Orient** — What was supposed to change? Compare to the plan if one exists.
2. **Review diff + surroundings** — Correctness, edge cases, error handling, consistency with local patterns.
3. **Tests & docs** — Missing tests? Architecture/security/README drift?
4. **Sensitive** — If sensitive (or unsure), load and apply [references/security-checklist.md](references/security-checklist.md).
5. **Done criteria** — Check `standards/definition-of-done.md` for the path.
6. **Report** — Findings with severity. Ask before remediating unless the user already requested fixes.

## Prohibitions

- Do not silently rewrite the codebase unless asked to remediate
- Do not rubber-stamp without reading surroundings
- Do not treat “not configured” checks as pass
- Do not approve prod/destructive actions — flag for human

## Output template

```markdown
# Review: <short title>

## Summary
<2–3 sentences>

## Findings
| Severity | Finding | Location |
|----------|---------|----------|
| critical | ... | `path` |
| suggestion | ... | `path` |
| nice-to-have | ... | `path` |

Severity: **critical** (must fix) | **suggestion** | **nice-to-have**

## Sensitive checklist
n/a | see notes below (link items from security-checklist)

## Done criteria
- path: tiny | normal | sensitive
- met: ...
- gaps: ...

## Residual risks
- ...

## Recommendation
approve | approve with follow-ups | rework needed
```

## Verification

- Findings are specific and actionable
- Sensitive path used the security checklist
- Recommendation matches remaining critical gaps

## Escalation

- Critical security findings → recommend stop-ship until fixed; do not downplay
- Unclear product requirements → ask the human
- User asks to remediate → switch to focused fixes (or `/feature-implementation`) with evidence

## Related

- `standards/definition-of-done.md`, `standards/security-baseline.md`, `standards/testing-and-verification.md`
- Checklist: [references/security-checklist.md](references/security-checklist.md)
