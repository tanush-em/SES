# Sensitive-change security checklist

Use when the change path is **sensitive** (or unsure). Mark each item pass / fail / n/a with a one-line note.

## Auth and isolation

- [ ] Authn/authz changes cannot be bypassed via alternate routes
- [ ] Tenant/user isolation preserved (no cross-tenant reads/writes)
- [ ] New endpoints/default roles are least privilege

## Secrets and crypto

- [ ] No secrets in code, logs, or committed files
- [ ] `.env.example` updated with names only if new vars added
- [ ] Crypto/secret handling uses known patterns; no homemade crypto

## Data and payments

- [ ] PII collection/storage/access is intentional and documented
- [ ] Money movement / payment paths have clear failure and idempotency behavior
- [ ] Destructive ops / migrations are reversible or explicitly accepted

## Production

- [ ] No prod config or access-control change without recorded human approval
- [ ] Error messages do not leak secrets or sensitive internals

## Residual

- [ ] Residual risks listed for the human
