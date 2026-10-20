# Security Baseline

Minimum expectations for every SES product. Not a full threat model — a floor you don’t go below.

## Secrets

- Secrets live only in `.env` (gitignored). Ship `.env.example` with **names**, never real values.
- Never commit secrets. Never paste production secrets into chats or agent context.
- If a secret may have leaked, rotate it; don’t just “fix the file.”

## Privilege and authz

- Prefer least privilege for tokens, DB users, and cloud roles.
- Don’t weaken authentication or authorization casually to “make it work.”
- Tenant isolation (when applicable) is a hard boundary — treat breaks as sensitive.

## Sensitive domains

Treat a change as **sensitive** if it touches any of:

- Authentication / authorization / tenant isolation
- Payments or money movement
- Personal / confidential data (PII)
- Cryptographic material or secret handling
- Destructive data ops or tricky migrations
- Production configuration or access control

When unsure: **treat it as sensitive**. Sensitive work needs an approved plan and a security-minded review (`/feature-planning`, `/independent-review`).

## Production and destructive ops

- Always ask the human before production changes or destructive data operations.
- Agents must not “just run it” against prod.

## Dependencies and tools

- Prefer known, reviewed tools.
- Review new MCP servers for permissions before trusting them with credentials or filesystem access.

## Related

- Done criteria for sensitive work: `definition-of-done.md`
- Docs stub at product init: `docs/security.md` (per product)
