---
name: feature-planning
description: >-
  Produces a short feature plan (goal, approach, files/areas, risks, verification)
  and flags sensitive work for human approval. Use when planning a normal or
  sensitive feature, starting design work, or when the user invokes
  /feature-planning or asks to plan before implementing.
disable-model-invocation: true
---

# Feature Planning

Inspect the codebase, write a short plan, flag sensitive risk, and stop for approval when required. Do not implement in this skill.

## When to use

- Normal or sensitive features (not tiny typos/CSS/trivial one-liners)
- Ambiguous or multi-file design before coding
- User invokes `/feature-planning` or asks to plan first

## Inputs

- User goal / acceptance criteria (ask if missing)
- Relevant existing code and docs (read before proposing)
- Risk hints (auth, payments, PII, etc.)

## Steps

1. **Inspect** — Read the areas you might touch. Prefer facts from the repo over assumptions.
2. **Classify path** — Tiny → say so and skip full plan (point at `standards/definition-of-done.md`). Normal or sensitive → continue.
3. **Draft plan** — Goal, approach, files/areas, risks, how to verify. Keep it short.
4. **Sensitive check** — If the change touches auth/authz/tenancy, payments, PII, crypto/secrets, destructive data/migrations, or prod config/access (or you are unsure): label **risk: sensitive**, list blast radius, and **stop**. Do not implement until the human explicitly approves the plan.
5. **Hand off** — For non-sensitive normal work, present the plan and wait for agreement before `/feature-implementation` unless the user already said to proceed after planning.

## Prohibitions

- Do not implement code in this skill
- Do not expand into unrelated refactors
- Do not skip sensitive labeling when unsure
- Do not touch production or run destructive ops

## Output template

Use this shape:

```markdown
# Plan: <short title>

## Goal
<one paragraph>

## Path
tiny | normal | sensitive

## Approach
- ...

## Files / areas
- `path` — why

## Risks
- ...
<!-- if sensitive: -->
**risk: sensitive**
**Blast radius:** ...

## Verification
- [ ] commands / tests / manual checks

## Open questions
- ...
```

## Verification

- Plan is specific enough to implement without guessing major files
- Sensitive work explicitly blocked pending approval
- Path matches `standards/definition-of-done.md`

## Escalation

- Missing requirements or conflicting goals → ask the human (1–2 critical questions)
- Sensitive plan → wait for explicit approval before any implementation skill
- Out of current phase scope (hosting, publishing, etc.) → say so; do not invent machinery

## Related

- `standards/definition-of-done.md`, `standards/security-baseline.md`, `standards/engineering-principles.md`
