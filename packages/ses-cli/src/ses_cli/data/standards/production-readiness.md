# Production Readiness

Use this when you actually ship a product somewhere. **Hosting and deploy automation are out of SES v1 scope** — this is a human checklist, not a SES pipeline.

## Before you call it shipped

- [ ] Secrets are in the real environment (not committed); `.env.example` matches required names
- [ ] Sensitive paths (auth, payments, PII, etc.) were reviewed with the security-minded checklist
- [ ] `ses check` (or equivalent) passes on the release candidate
- [ ] README covers setup and how to run checks
- [ ] Architecture and security docs match what you deployed
- [ ] You know how to roll back or disable the change if it fails
- [ ] Destructive or prod config changes had **explicit human approval**

## What SES does not do

- Provision hosts, DNS, or cloud resources
- Run GitHub Actions or block merges remotely
- Guarantee production safety from prompts alone

You own remotes, deploy, and production access.

## Graduate carefully

Default DB is SQLite. Move to Postgres (or other infra) only when concurrent writers, locking, ops needs, or compliance force it. Answer the five questions in the master spec before adding non-trivial components.

## Related

- Security floor: `security-baseline.md`
- Verification: `testing-and-verification.md`
- Sensitive Done: `definition-of-done.md`
