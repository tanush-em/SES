# Publishing SES (`ses-cli`)

## When

After Phase 4 pilot lessons and Phase 5 stabilize fixes. Kit version **1.0.0**.

## What to publish

| Artifact | Channel |
|----------|---------|
| CLI (`ses init`, `ses setup`, `ses check`) + vendored skeleton/templates/standards | **PyPI** package `ses-cli` |
| Spec / longer docs | This git repo |

## Build

From kit root:

```bash
python packages/ses-cli/scripts/sync_package_data.py
pip install build twine
python -m build packages/ses-cli
# artifacts: packages/ses-cli/dist/
```

Vendored data under `packages/ses-cli/src/ses_cli/data/` must be present (sync copies from `skeleton/`, `standards/`, `templates/product-cursor/`).

## Upload (requires your PyPI credentials)

```bash
cd packages/ses-cli
twine upload dist/*
# or: TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-... twine upload dist/*
```

Do not commit tokens. Prefer Trusted Publishing later if desired.

## Consumer smoke

```bash
python -m venv /tmp/ses-smoke && source /tmp/ses-smoke/bin/activate
pip install ses-cli
mkdir /tmp/ses-app && cd /tmp/ses-app
ses init --yes --name smoke --purpose "smoke" --languages python \
  --no-api --no-ui --no-db --risk side-project --sensitive none --no-check
ses setup --docs
ses version   # expect 1.0.0+
```

## Semver

- Kit [`VERSION`](../VERSION) and `packages/ses-cli` `project.version` stay aligned.
- Tag `v1.0.0` on the kit repo at release.
