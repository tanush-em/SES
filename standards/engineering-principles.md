# Engineering Principles

Short rules for how SES expects work to be done. Procedures live in skills; this doc is the shared language.

## Do

- Prefer the **simplest architecture that works**. Modular monolith over microservices. Don’t add Redis, brokers, vector DBs, or K8s unless a stated requirement needs them.
- Standardize **process** (secrets, docs, verification, safety) — not every stack choice. Products may diverge when requirements justify it.
- Prefer **evidence** over confidence: command output, test results, or a short manual verification note. “Should work” is not evidence.
- Keep the **human in control**. Agents recommend; they don’t authorize destructive or production actions.
- Match rigor to risk: **tiny ≠ normal ≠ sensitive** (see `definition-of-done.md`).
- Keep SES **smaller than the products it helps**. Add machinery only when a real pilot shows a repeatable gap.

## Don’t

- Treat prompts alone as a safety guarantee.
- Expand scope beyond the agreed plan without asking.
- Claim checks passed without running them.
- Multiply templates or frameworks when one skeleton + modules will do (Phase 2+).

## Ownership

You own requirements, risk acceptance, remotes, PRs, and production. SES guides in Cursor and verifies locally via `ses check` when configured — it does not merge, push, or deploy for you.

## Related

- Change paths and Done: `definition-of-done.md`
- Verification: `testing-and-verification.md`
- Skills: `/feature-planning`, `/feature-implementation`, `/independent-review`
