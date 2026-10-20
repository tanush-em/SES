# SES setup

## Kit repo (this repository)

Open this repo in Cursor. Project rules under `.cursor/rules/` load automatically; skills under `.cursor/skills/` appear via `/feature-planning`, `/feature-implementation`, `/independent-review`.

## CLI

Requires Python 3.11+.

```bash
# From PyPI (after publish):
pip install ses-cli

# Kit development:
pip install -e packages/ses-cli

ses version
```

### New product (own repo, current directory)

```bash
mkdir my-app && cd my-app
git init   # optional
ses init   # interactive, scaffolds cwd
# or:
ses init --yes --name my-app --purpose "One-liner" --languages python \
  --no-api --no-ui --no-db --risk side-project --sensitive none
```

Init writes the skeleton into **cwd**, runs `ses setup`, and gitignores regenerable SES Cursor files. Install product deps (see generated README), then:

```bash
ses check
```

### Existing product

```bash
cd my-existing-app
ses setup          # Cursor rules + skills
ses setup --docs   # also refresh .ses/standards/
```

After upgrading the CLI: `pip install -U ses-cli && ses setup`.

### Local checks

```bash
ses check              # cwd with ses.toml
ses check --path ../other-app
```

| Exit | Meaning |
|------|---------|
| 0 | All configured checks passed |
| 1 | At least one check failed |
| 2 | Not configured (missing/empty `ses.toml` steps) |

Not configured ≠ pass. No GitHub Actions integration in SES v1.

### Commit vs regenerate

**Commit:** app source, `ses.toml`, `.env.example`, product `docs/`.

**Gitignore / restore with `ses setup`:** `.cursor/rules/ses-*.mdc`, SES skills under `.cursor/skills/`, optional `.ses/standards/`.

See [`ses-init-questionnaire.md`](ses-init-questionnaire.md).
