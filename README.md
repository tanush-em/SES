# Solo Engineering System (SES)

Reusable engineering kit for shipping many products with heavy AI help in Cursor — without losing understanding, consistency, or basic safety.

**Status:** v1.0.0 — pip-oriented kit (`ses init` / `ses setup` / `ses check`). Pilot: separate [`ses-pilot`](https://github.com/tanush-em/ses-pilot) repo.

## What’s here (kit only)

| Path | Role |
|------|------|
| [`solo_engineering_system_master_spec.md`](solo_engineering_system_master_spec.md) | Build contract |
| [`standards/`](standards/) | Six short engineering standards |
| [`.cursor/rules/`](.cursor/rules/) | Cursor rules (kit development) |
| [`.cursor/skills/`](.cursor/skills/) | Plan → implement → review |
| [`templates/product-cursor/`](templates/product-cursor/) | Rules/skills `ses setup` copies into products |
| [`skeleton/`](skeleton/) | Universal product skeleton + modules |
| [`packages/ses-cli/`](packages/ses-cli/) | `ses init` / `ses setup` / `ses check` |

Real apps live in **their own repos**. This kit is not a `products/` monorepo host.

## Install CLI

```bash
pip install -e packages/ses-cli   # kit development
# after publish: pip install ses-cli
ses version
```

## New product (separate repo)

```bash
mkdir my-app && cd my-app
ses init
# install product deps (see generated README)
ses check
```

Existing repo: `ses setup` (add `--docs` for `.ses/standards/`).

Commit app + `ses.toml` + `.env.example` + product docs. Regenerable SES Cursor files are gitignored; restore with `ses setup`.

Questionnaire: [`docs/ses-init-questionnaire.md`](docs/ses-init-questionnaire.md). Setup: [`docs/setup.md`](docs/setup.md). Publishing: [`docs/publishing.md`](docs/publishing.md).

## How to use features

1. **Tiny** fix — implement; skip full ceremony (see `standards/definition-of-done.md`).
2. **Normal / sensitive** — invoke deliberately:
   - `/feature-planning` — short plan; sensitive work waits for your approval
   - `/feature-implementation` — code + tests + docs; run `ses check`; report evidence
   - `/independent-review` — findings; security checklist when sensitive

## Standards

- [`engineering-principles.md`](standards/engineering-principles.md)
- [`security-baseline.md`](standards/security-baseline.md)
- [`testing-and-verification.md`](standards/testing-and-verification.md)
- [`documentation.md`](standards/documentation.md)
- [`production-readiness.md`](standards/production-readiness.md)
- [`definition-of-done.md`](standards/definition-of-done.md)

## Version

See [`VERSION`](VERSION) (`1.0.0`). Publishing notes: [`docs/publishing.md`](docs/publishing.md). Lessons: [`docs/pilot-lessons.md`](docs/pilot-lessons.md).
