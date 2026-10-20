# ses-cli

Solo Engineering System command-line toolkit.

```bash
pip install ses-cli          # or: pip install -e . from this directory (kit monorepo)
ses init                     # scaffold current directory
ses setup [--docs] [--force] # Cursor rules/skills (+ optional standards)
ses check [--path DIR]       # local checks
ses version
```

Before building a wheel from the kit repo, sync vendored data:

```bash
python scripts/sync_package_data.py
python -m build
```
