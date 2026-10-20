# Pilot lessons (Phase 4)

**Pilot product:** [`ses-pilot`](https://github.com/tanush-em/ses-pilot) (separate repo; not under this kit).  
**Feature:** In-memory notes API (`POST/GET /notes`) on the FastAPI stub from `ses init --api`.  
**Loop used:** scaffold with cwd `ses init` → implement + tests + arch docs → `ses check` → Cursor kit gitignored / restorable via `ses setup`.

## What worked

- Cwd init + `ses setup` felt right: product repo stays a normal GitHub app; kit is a pip tool.
- Regenerable `.cursor` SES files stayed out of `git status` / commits; `ses.toml` + app + docs committed as intended.
- `ses check` from product root was enough; no kit `products/` path needed.
- Skeleton API + pytest TestClient made a small “real” feature cheap to verify.

## Friction / gaps

1. **Editable install still wants the kit monorepo on `PYTHONPATH` resolution** — for day-to-day, developing against `pip install -e packages/ses-cli` from the kit is fine; consumers need vendored `data/` after `sync_package_data.py` + wheel. Worth a one-line “sync before build” in release checklist (already in `docs/publishing.md`).
2. **Init `--force` wipes cwd contents** (except `.git`) — correct but sharp; CLI help now calls it destructive.
3. **Clone workflow must be documented in every product README** — `pip install ses-cli && ses setup` after clone; generated README covers this.
4. **httpx/Starlette TestClient deprecation warning** — noise in pilot tests; not a SES blocker (optional future skeleton pin).
5. **Setuptools drops hidden skeleton files from wheels** — fixed by storing `dot-gitignore` / `dot-env.example.j2` and renaming on copy (verified via local wheel install).

## What to delete / not add

- Do not revive kit-owned `products/` as the place real apps live.
- Do not commit product `.cursor/rules/ses-*` or SES skills to GitHub.
- No extra skills/recipes until another product shows a repeatable gap.

## Success metric check

- [x] Started product with `ses init` in its own repo  
- [x] Meaningful feature with tests + `ses check` + architecture update  
- [x] Important flow explainable (see pilot `docs/architecture.md`)  
- [x] No hooks / GitHub Actions dependency for SES itself  
