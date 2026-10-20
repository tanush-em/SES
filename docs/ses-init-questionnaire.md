# `ses init` questionnaire

Small, decisive, module-oriented. Answers change files on disk.

## Required questions

1. **Product name** — slug `^[a-z][a-z0-9-]*$`
2. **One-line purpose** — stored in README
3. **Languages** — `python` | `typescript` | `both`
4. **Has a documented HTTP API?** — `yes` | `no`
5. **Has a web UI?** — `yes` | `no` (Vite + React + TypeScript stub)
6. **Needs a database?** — `yes` | `no` (default SQLite; note about graduating to Postgres)
7. **Risk posture** — `side-project` | `commercial` (how loud security/docs reminders are)
8. **Likely sensitive domains?** — multi-select optional: `auth` | `payments` | `pii` | `none`

## What init does

1. Validate name and options  
2. Scaffold into **cwd** (refuse non-empty without `--force`; `.git` alone is OK)  
3. Enable modules (language runtimes, API stub, UI stub, DB + SQLite)  
4. Write `.env.example` (never a real `.env` with secrets)  
5. Wire `ses.toml` for `ses check`  
6. Append regenerable SES paths to `.gitignore`  
7. Run `ses setup` (Cursor rules/skills)  
8. Print exact next commands (optional `--check` after you install deps)  
9. Fail clearly if something didn’t apply  

If **web UI = yes** and languages were `python` only, TypeScript tooling for `web/` is still enabled.

## What `ses setup` does

- Copies SES-managed Cursor rules + three skills into the product  
- Optional `--docs` writes `.ses/standards/`  
- Safe for existing projects; refresh after CLI upgrades  

## What init / setup must not do

- Overwrite a non-empty cwd without `--force`  
- Create cloud resources  
- Copy secrets  
- Require network/GitHub  
- Install every optional dependency “just in case”  
- Put apps under a kit `products/` folder  

## Questions we deliberately do not ask

- Hosting provider  
- Microservices vs monolith (always start modular monolith)  
- Agent framework / vector DB / Redis  
- GitHub org, Actions, branch protection  
- Coverage percentage targets  

Those are later product decisions, not bootstrap decisions.
