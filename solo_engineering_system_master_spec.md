# Solo Engineering System (SES)

**Version:** 1.1  
**Status:** Build contract (replaces the v1.0 encyclopedic draft)  
**Owner:** Solo developer  
**Primary environment:** Cursor  
**Tone:** Practical — do this / don’t do that

---

## 1. What SES is

SES is a **reusable engineering kit** for building many products with heavy AI help in Cursor, without losing understanding, consistency, or basic safety.

It is **not**:
- an autonomous multi-agent company
- a GitHub/PR/CI-as-a-service product
- a mega-framework every app must inherit
- a promise that prompts alone make software safe

It **is**:
1. Short engineering standards (shared language)
2. Cursor rules (persistent guidance)
3. Three core skills (plan → implement → review)
4. Specialist **modes** you invoke when useful (not a permanent agent fleet)
5. A CLI: `ses init`, `ses setup`, `ses check` (pip: `ses-cli`)
6. One universal product skeleton + optional modules
7. Local quality checks (not GitHub Actions)
8. Light vs sensitive change paths
9. A kit repo you maintain; products live in their own repos

**Mission:** Help one engineer ship many maintainable products with AI assistance, while still understanding important flows and catching common pitfalls early.

**Success (30 days):** Ship one real feature using plan + local checks + review, and be able to explain the important execution path.

**Failure:** Weeks of docs/ceremony while real work skips the process.

---

## 2. Design decisions (locked)

| Decision | Choice |
|----------|--------|
| Primary pains | Code you don’t understand later; inconsistent quality; every repo from scratch |
| Guidance style | **Remind and guide** — not remote merge blocks |
| Scale | 15+ products planned → generalize bootstrap, don’t multiply templates |
| Risk mix | Side projects and paid B2B → risk-based depth |
| Standards | **Six** concise documents |
| Skills | **Three** core |
| Roles | Architect / Implementer / Reviewer as **invoke-when-needed** modes |
| Hooks | Out of v1; SES must work **without** hooks |
| Templates | **One** skeleton + `ses init` questionnaire/modules |
| CLI | `ses init` + `ses check` from day one |
| Ops / LLM extras | Checklists when the product needs them — not mandatory core |
| Tiny fixes | Minimal ceremony; run light local checks |
| Normal features | Tests before done; update architecture docs |
| Git / GitHub / PRs | **You** own remotes, PRs, and pushing. SES does not manage them |
| “CI” | Means **local** `ses check` only — not GitHub Actions |
| Secrets | `.env` only; never commit secrets |
| Destructive / prod | Always ask the human |
| Default DB | **SQLite**, with clear “graduate to Postgres when…” |
| Languages | Python and TypeScript |
| Repo shape | Kit repo separate from product repos; `ses` via pip |
| Hosting | Out of scope for v1 |

---

## 3. Operating principles

1. **Standardize process, not every architecture.** Shared rules for secrets, docs, verification, and safety. Stacks may differ when requirements justify it.
2. **Guide in Cursor; verify locally.** Rules and skills shape behavior. `ses check` verifies what can be verified. Nothing here silently guarantees production safety.
3. **Evidence over confidence.** “Should work” is not evidence. Prefer command output, test results, or a short manual verification note.
4. **Keep the human in control.** You own requirements, risk acceptance, and production. Agents recommend; they don’t authorize destructive or prod actions.
5. **Risk-based rigor.** Tiny ≠ normal ≠ sensitive.
6. **SES must stay smaller than the products it helps.** Add machinery only when a real pilot shows a repeatable gap.
7. **Prefer simplest architecture that works.** Modular monolith over microservices by default. Don’t add Redis, brokers, vector DBs, K8s, etc. unless a stated requirement needs them.
8. **Honest limits.** If Cursor cannot enforce something, say so and use docs + `ses check` + human judgment.

---

## 4. What Cursor can and cannot do

### Cursor is good at
- Applying persistent rules and skills
- Planning, implementing, and reviewing in a guided workflow
- Updating docs when asked as part of Done
- Reminding you about sensitive paths and `.env` hygiene

### Cursor cannot reliably guarantee
- That you ran tests before shipping
- That secrets never leaked
- That production wasn’t touched
- That architecture stayed coherent after you skipped the process
- Security or correctness of AI-generated code without review/checks

### SES response
| Concern | How SES handles it |
|---------|-------------------|
| Forgotten process | Rules + skills remind; short paths so you’ll use them |
| Broken quality | `ses check` (local) |
| Secrets | Standards + `.env.example`; never commit `.env` |
| Prod / destructive | Explicit human approval every time |
| Understanding | Plan + arch docs + light “explain the flow” for significant features |
| New repo sprawl | `ses init` + one skeleton |

**Enforcement matrix (v1):**

| Requirement | Rule/skill reminder | `ses check` | Human decision |
|-------------|---------------------|-------------|----------------|
| Format / lint / types / tests | yes | yes (when configured) | — |
| Update arch docs on features | yes | optional stub check | — |
| No secrets in git | yes | basic scan if available | — |
| Sensitive change extra care | yes | — | yes (approve plan) |
| Production / destructive ops | yes | — | **always** |
| Push / PR / remote CI | — | — | you own it |

---

## 5. Change paths

### 5.1 Tiny (typo, copy, pure CSS, trivial fix)
- Implement
- Run light `ses check` if the project has it
- Done  
No feature plan required.

### 5.2 Normal feature
1. **Plan** (`feature-planning` skill) — short plan: goal, approach, files/areas, risks, how to verify
2. **Implement** (`feature-implementation`) — code + tests + arch/docs touch if behavior changed
3. **`ses check`**
4. **Review** (`independent-review`) — fresh pass for defects, missing tests, doc drift
5. Done when checks pass and you can explain the important flow

### 5.3 Sensitive (mandatory extra care)
Treat as sensitive if the change touches any of:
- Authentication / authorization / tenant isolation
- Payments or money movement
- Personal / confidential data handling
- Cryptographic material or secret handling
- Destructive data ops or tricky migrations
- Production configuration or access control

**Extra requirements:**
- Plan must label **risk: sensitive** and list blast radius
- **You approve the plan** before implementation
- Review uses the security-minded checklist (inside the review skill)
- Still guide-mode — SES won’t remotely block you, but the workflow asks for approval

When unsure whether something is sensitive: **treat it as sensitive**.

---

## 6. Layers

### 6.1 Standards (six documents — keep all, keep them short)

| File | Job |
|------|-----|
| `standards/engineering-principles.md` | Simplicity, evidence, ownership, risk-based rigor |
| `standards/security-baseline.md` | `.env`, least privilege, authz basics, no secret-in-prompt dumping |
| `standards/testing-and-verification.md` | What “verified” means; local check expectations |
| `standards/documentation.md` | README, architecture, when to write ADRs |
| `standards/production-readiness.md` | Checklist when you actually ship (hosting later) |
| `standards/definition-of-done.md` | Tiny / normal / sensitive Done criteria |

Detailed procedures live in skills, not in standards.

### 6.2 Cursor rules
Small, non-contradictory rules:
- Global SES principles
- Monorepo / product layout conventions
- Testing & verification
- Security & sensitive ops
- Documentation maintenance
- Language-specific only when needed (Python / TS)

Do not paste this whole spec into every rule. Point to standards/skills.

### 6.3 Skills (three core)

1. **`feature-planning`** — inspect → plan → flag sensitive → list verification → wait for approval if sensitive  
2. **`feature-implementation`** — implement approved/agreed scope → tests → update docs → run `ses check` → report evidence  
3. **`independent-review`** — review diff & surroundings → findings with severity → security checklist when sensitive → do not silently rewrite unless asked to remediate  

**Later (only after pilot proves need):** codebase-audit, release-readiness, incident-investigation as extras — not v1 blockers.

Each skill defines: when to use, inputs, steps, prohibitions, output, verification, escalation.

### 6.4 Specialist modes (advantages without an agent fleet)

| Mode | Use when | Maps to |
|------|----------|---------|
| Architect / Planner | Ambiguous or multi-file design | `feature-planning` + Plan-style work |
| Implementer | Approved/clear scope | `feature-implementation` |
| Independent Reviewer | Before you call a feature done | `independent-review` |
| Release / Ops | Actually shipping or incident | Short checklist; optional future skill |

Invoke deliberately. Do not require four agents for a button label change.

### 6.5 CLI and local checks
- `ses init` — scaffold a product **in the current directory** from the universal skeleton  
- `ses setup` — materialize Cursor rules/skills (and optional `.ses/standards/`) for **new or existing** product repos; refresh after `pip install -U ses-cli`  
- `ses check` — run that product’s configured local checks (cwd / `--path`)  

Install: `pip install ses-cli` (kit development: `pip install -e packages/ses-cli`).

No GitHub Actions integration in SES v1.

### 6.6 Universal skeleton + modules
One skeleton for all products. Modules turn on via `ses init` answers — not a matrix of full templates.

---

## 7. Default technology posture

**Preferred defaults (not mandates):**
- Languages: Python and/or TypeScript as chosen at init
- DB: **SQLite** by default
- API: simple HTTP API when needed (e.g. FastAPI or a small TS server) — only if module enabled
- UI: React/Next only if module enabled
- Packaging: optional; don’t force Docker in v1

**Graduate SQLite → Postgres when:**
- Multiple app instances need concurrent writers
- Write contention or locking becomes a real problem
- You need operational features SQLite doesn’t give you (and you don’t want to own that complexity yourself)
- A customer/compliance requirement forces it

**Before adding any non-trivial component, answer:**
1. What requirement does it satisfy?  
2. What’s the simplest alternative?  
3. What operational burden does it add?  
4. How do we test, observe, and secure it?  
5. What’s the exit path if it’s wrong?

---

## 8. `ses init` questionnaire

The questionnaire must be **small, decisive, and module-oriented**. Bad questionnaires ask vanity questions; good ones change files on disk.

### 8.1 Required questions

1. **Product name** (slug: `^[a-z][a-z0-9-]*$`)
2. **One-line purpose** (stored in README)
3. **Languages**  
   - `python` | `typescript` | `both`
4. **Has a documented HTTP API?**  
   - `yes` | `no`
5. **Has a web UI?**  
   - `yes` | `no`
6. **Needs a database?**  
   - `yes` | `no`  
   - If yes: default **SQLite** (note shown about Postgres graduation)
7. **Risk posture**  
   - `side-project` | `commercial`  
   - Affects how loud security/docs reminders are — not a different framework
8. **Likely sensitive domains?** (multi-select, optional)  
   - auth | payments | PII | none yet  
   - Seeds a short `docs/security.md` stub and points at the sensitive path

### 8.2 Questions we deliberately do **not** ask at init
- Hosting provider
- Microservices vs monolith (always start modular monolith)
- Which agent framework / vector DB / Redis
- GitHub org, Actions, branch protection
- Coverage percentage targets

Those are later product decisions, not bootstrap decisions.

### 8.3 What `ses init` does
1. Validate name and options  
2. Scaffold into **cwd** (refuse non-empty without `--force`; `.git` alone is OK)  
3. Enable modules (language runtimes, API stub, UI stub, DB + SQLite)  
4. Write `.env.example` (never a real `.env` with secrets)  
5. Wire `ses.toml` for `ses check`  
6. Append regenerable SES paths to `.gitignore`  
7. Run `ses setup` (Cursor rules/skills)  
8. Print exact next commands; optional smoke `ses check`  
9. Fail clearly if something didn’t apply — don’t claim success  

### 8.4 What `ses setup` does
1. Copy SES-managed Cursor rules + three skills from the installed package (or kit templates)  
2. Optional `--docs`: write/refresh `.ses/standards/` from kit standards  
3. Overwrite only SES-managed paths unless `--force`  
4. Safe on existing products that already have app code  

### 8.5 Commit vs regenerate

| Commit (product truth) | Gitignore (restore with `ses setup`) |
|------------------------|--------------------------------------|
| App source, tests, lockfiles | `.cursor/rules/ses-*.mdc` |
| `ses.toml` | `.cursor/skills/feature-*`, `independent-review` |
| `.env.example` | `.ses/standards/` (when using `--docs`) |
| Product `docs/architecture.md`, `docs/security.md` | — |

### 8.6 What `ses init` / `ses setup` must not do
- Overwrite a non-empty product cwd without explicit `--force`  
- Create cloud resources  
- Copy secrets  
- Require network/GitHub  
- Install every optional dependency “just in case”  
- Nest apps under a kit `products/` folder

---

## 9. Local checks (`ses check`)

Per-product, configured at init. Typical menu (only what the modules need):

- Format  
- Lint  
- Typecheck (if applicable)  
- Unit/integration tests  
- Optional: basic secret-pattern scan on tracked files  
- Optional: “architecture.md exists” for commercial posture  

**Rules:**
- Meaningful exit codes  
- Distinguish **pass / fail / not configured** (not configured ≠ pass)  
- No secret leakage in output  
- You run it locally; SES does not push or open PRs

---

## 10. Documentation expectations (per product)

Keep docs **short and true**:

| Doc | Purpose |
|-----|---------|
| `README.md` | Setup, commands, `ses check`, config |
| `docs/architecture.md` | Components, boundaries, main flows — update on normal+ features |
| `docs/security.md` | Assumptions, sensitive areas (stub OK at init) |
| `docs/decisions/` | ADRs only for consequential choices |
| `.env.example` | Names of required env vars — no real values |

**Understanding check (significant features):** You should be able to explain request path, data changes, security boundary, how it’s tested, and failure behavior. Agents may quiz lightly; no fake certification process.

---

## 11. Security baseline (summary)

- Secrets only in `.env` (gitignored); ship `.env.example` without values  
- Don’t paste production secrets into chats/agent context  
- Least privilege; don’t weaken authz casually  
- Sensitive path for auth, payments, PII, crypto, destructive data, prod config  
- Human approval for production and destructive operations  
- Dependencies: prefer known tools; review new MCP servers for permissions  

Full detail: `standards/security-baseline.md`.

---

## 12. Kit repo layout (this repository)

This repo is the **SES kit only**. Real products are **separate GitHub repos** (pip install → `ses init` / `ses setup` in that product’s cwd).

```text
SES/
├── README.md
├── VERSION
├── solo_engineering_system_master_spec.md   # this file
├── standards/                # six standards (source of truth)
├── .cursor/
│   ├── rules/                # kit Cursor rules
│   └── skills/               # three core skills (kit development)
├── templates/
│   └── product-cursor/       # rules/skills copied by `ses setup` into products
├── skeleton/                 # universal product skeleton + modules
├── packages/
│   └── ses-cli/              # pip package: ses init, setup, check
├── recipes/                  # optional short stack notes — not full apps
├── workflows/                # optional short playbooks
└── docs/
    ├── setup.md
    ├── ses-init-questionnaire.md
    ├── publishing.md
    └── pilot-lessons.md      # after pilot
```

Cursor discovers kit rules/skills under `.cursor/`. Product repos get regenerable copies via `ses setup` (typically gitignored). SES is not a runtime framework products must import forever.

---

## 13. Out of scope for v1

- GitHub Actions / required PR bots / branch protection as SES features  
- Cursor hooks as a dependency  
- Multiple full project templates  
- Agent orchestration platforms  
- Custom observability backends  
- Hosting/deploy automation  
- Policy-as-code platforms  
- Coverage-percent religion  
- Explaining every generated line  

---

## 14. How we build SES (implementation plan)

### Phase 0 — Spec (this document) ✅ when accepted
Rewrite locked; practical build contract.

### Phase 1 — Standards + rules + three skills
- Write the six short standards  
- Add Cursor rules (verify current Cursor docs for paths/format)  
- Implement the three skills with real workflows and output shapes  
- **Verify:** You can invoke plan → implement → review on a toy change in-repo  

### Phase 2 — Skeleton + CLI ✅
- Build universal `skeleton/`  
- Implement `ses init` + `ses check` (initial monorepo-shaped delivery)  

### Phase 3 — Delivery model (pip + cwd + setup)
- Pivot to pip-first: cwd `ses init`, `ses setup`, vendored package data  
- Commit/ignore table (§8.5); kit repo ≠ product apps  
- **Verify:** empty dir init → check pass → delete Cursor SES files → setup restores  

### Phase 4 — Pilot (non-negotiable)
- Create a **separate** product repo (not under this kit)  
- Ship **one meaningful feature** using the three skills + `ses check`  
- Record friction in `docs/pilot-lessons.md`  
- **Verify:** Success metric in §1  

### Phase 5 — Stabilize v1 + publish
- Fix only demonstrated gaps; delete unused ceremony  
- Tag `v1.0.0`; publish `ses-cli` to PyPI  
- Only then consider extras (more skills, recipes)  

**Do not** freeze publishing API before Phase 4 pilot lessons.

---

## 15. Publishing (recommendation)

### Should you publish?
**Not before Phase 4 pilot lessons.** Shape the pip API in Phase 3; dogfood on a real separate product in Phase 4; publish in Phase 5.

### If you publish later, what goes where?

| Artifact | Good distribution channel | Why |
|----------|---------------------------|-----|
| `ses` CLI (`init`, `check`) | **PyPI** (and later optional npm wrapper if needed) | People expect CLIs on pip/npm |
| Standards / skills / skeleton content | **Versioned package data** shipped *with* the CLI, or a public git repo the CLI can copy | Markdown “OS” isn’t a pip API; it’s content |
| Cursor rules | Copied into consumer repos by `ses init` | Must match Cursor’s current layout |

**Recommendation:** One Python package, e.g. `solo-engineering-system` or `ses-kit`, that:
1. Installs the `ses` command  
2. Vendors the skeleton + standards + skill templates inside the package  
3. Documents how to use with Cursor  

Optional: mirror the same repo publicly on GitHub for reading/star/history — pip for install UX, git for browsing.

### What not to do
- Don’t publish empty standards with no pilot evidence  
- Don’t make apps runtime-depend on SES forever (init-time copy is enough)  
- Don’t require GitHub Actions for consumers — keep local checks  
- Don’t split into five packages on day one  

### When publishing is justified
- You’ve used SES on ≥2 real products  
- `ses init` / `ses check` APIs feel stable  
- Questionnaire hasn’t churned weekly  
- You’re willing to version semver and write a short changelog  

Details when ready: `docs/publishing.md`.

---

## 16. Acceptance criteria for SES v1

- [ ] Spec matches how we actually work (this doc)  
- [ ] Six standards exist and are readable in one sitting each  
- [ ] Three skills are discoverable and usable in Cursor  
- [ ] `ses init` questionnaire matches §8 and scaffolds **cwd**  
- [ ] `ses setup` restores Cursor kit on new/existing repos  
- [ ] `ses check` passes on a fresh init (or fails clearly)  
- [ ] Pilot feature done with plan + checks + explainable flow  
- [ ] `ses-cli` installable via pip for consumers  
- [ ] No dependency on hooks or GitHub Actions  
- [ ] Sensitive path and human approval for prod/destructive are documented  
- [ ] Known limits (Cursor cannot guarantee X) are written plainly  

---

## 17. Working agreement with Cursor agents

1. Follow this spec; prefer the smallest change that works  
2. Verify Cursor capability/format from current docs when implementing rules/skills — don’t invent  
3. Never claim checks passed without running them  
4. Never perform production/destructive actions without explicit approval  
5. Implement **one phase at a time**; stop for approval between phases when scope jumps  
6. After Phase 1–2 exist, pressure-test on a pilot before adding features  

---

## 18. Final test

Can you start a product with `ses init`, implement a meaningful feature with plan → implement → review, run `ses check`, explain the important behavior, and ship without relying on unverified AI confidence or rediscovering your whole process?

If yes, SES is doing its job.
