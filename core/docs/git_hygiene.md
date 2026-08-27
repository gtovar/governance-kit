# Git Hygiene & Working Tree Protocol

> **Vehículo**: enrutada desde la constitución al tocar git/commits + hook determinista `commit-msg.sh` (Conventional Commits). La clasificación Desk/Tray/Canon y el protocolo de 3 ejes son juicio del agente, auditado por el subagente `reviewer`.
> **Autoridad**: normativa.

> **Key point:** We do not aim for a "perfectly clean working tree". We aim for a working tree that is **readable, classified, and checkpointed with intent**.

**Status:** Canonical (project-wide)
**Audience:** Dev (today), Dev-in-3-weeks (re-entry), reviewer
**Related:** `docs/workflow.md`, `docs/documentation_rules.md`, re-entry doc, `PROJECT_STATE.md`

---

## Purpose

Define a project protocol to maintain **traceability**, **scope control**, and **fast re-entry** using Git's three layers:

- **Working Tree (Desk):** files as they exist on disk right now.
- **Staging/Index (Tray):** changes selected for the next coherent checkpoint.
- **HEAD/History (Canon):** the official history (commits).

This protocol optimizes for **clarity**, not perfection.

---

## Scope and non-goals

### In scope

- Interpreting repo state (desk/tray/canon).
- Preventing *scope drift* (mixing unrelated changes).
- Avoiding "ghost docs" (docs that exist but cannot be found).
- Defining rules for **product vs artifacts vs experiments**.

### Out of scope

- Full branching strategy (see `docs/workflow.md`).
- Forcing "fast commits" or checkbox-driven commits.
- Replacing ADRs when architectural decisions are involved.

---

## When to consult this document

- Before starting a new feature (Ready-for-next-feature gate).
- When `git status` feels overwhelming.
- When you see many `??` files and it is unclear whether they are product or outputs.
- During re-entry after days/weeks away.

---

## Core model (Desk / Tray / Canon)

### 1) Desk (Working Tree)

Where changes live while you are actively working.

- The desk can be messy, but it must remain **interpretable**.
- Primary failure mode: mixing docs + refactor + feature in one unstructured pile.

### 2) Tray (Staging / Index)

A "pre-declaration": **this** is the next coherent checkpoint.

- Without the tray, you get the anti-pattern: *"everything ended up in the commit by accident."*

### 3) Canon (HEAD / History)

Committed history is the official, auditable truth.

- Canonical docs and contracts must be explainable from the commit history.

---

## Reading `git status` (semantic meaning)

- **Modified (M):** changed tracked file.
- **Deleted (D):** removed tracked file (often a strong decision).
- **Renamed (R):** name change; preserve traceability.
- **Untracked (??):** new file not yet part of canon.

**Rule of thumb:** `??` is not "bad". It is **unclassified**. Unclassified things get forgotten.

---

## Mandatory classification (anti-chaos)

Every new file/change must be classified:

### A) Product (must live in the repo)

- Source code in `src/**`
- Tests in `tests/**`
- Canonical docs in `docs/**`
- ADRs and decision records

**Risk signal:** product under `??` is usually **WARN** until explicitly accepted as canon.

### B) Artifact (should NOT live in the repo by default)

- Generated logs
- Temporary outputs (exports, diffs, reports)
- Bundles (`*.tgz`) or dumps

These belong in a dedicated "corral" (e.g., `logs/` or `artifacts/`) or should be ignored.

### C) Experiment (spike)

- Quick prototypes or exploratory changes
- Must have an explicit "expiry": decide Product vs discard

---

## Artifact policy (do not turn the repo into Downloads)

1) All artifacts must either:
   - live in an artifact corral (`logs/` or `artifacts/`), **or**
   - be explicitly ignored.
2) Versioned artifacts are the exception and require a declaration:
   - Why do we version this artifact?
   - How do we regenerate it?
   - What is its value?

---

## Ready for next feature (minimum gate)

Before starting a new feature:

1) Quality gate passes (tests + audit).
2) Canonical docs are indexed (if it is not in the index, it effectively does not exist).
3) No "product untracked" without an explicit decision (canon vs experiment).
4) A minimal narrative exists: what was done, what remains, why.

---

## Common anti-patterns this protocol prevents

- **Ghost doc:** a doc exists but is not indexed, so it disappears during re-entry.
- **Scope drift:** refactor + feature + doc fixes mixed into one pile.
- **Artifact pollution:** generated outputs show up as `??` and confuse the real state.
- **Slow re-entry:** returning to the repo and not knowing what matters.

---

## Tooling integration: Working Tree Report (spec)

The project auditor should print a "Working Tree Report" block with:

- **Tray (staged):** selected files for next checkpoint.
- **Desk (unstaged):** changed files not selected.
- **Untracked:** new files.
- **Suggested classification:**
  - Artifact candidates (outputs/logs/bundles)
  - Product candidates (code/docs/tests)

### Suggested severity

- **FAIL**
  - Canonical docs missing index references (ghost doc risk).
  - Doc Health failures (broken fences, missing canonical links).
- **WARN**
  - Product untracked (may be intentional; still risky).
  - Artifacts outside the corral.
- **INFO**
  - Desk changes that match the current scope.

## Commit boundary before scope expansion

Do not treat a dirty working tree as an automatic commit request. Treat it as a
commit-boundary signal only when a coherent slice is complete or new work would
mix unrelated concerns.

Strong signals are a completed declared subtask, aligned code/tests/required
documentation for one slice, a new request that expands scope before the prior
slice is checkpointed, or evidence of mixed concerns in the working tree.
Elapsed time, one modified file, and unverified assumptions are not signals.

When a strong signal exists, activate `commit-readiness` before new
implementation. Inspect the Desk and relevant diff in read-only mode, then
propose one of three outcomes: a coherent checkpoint, separation of concerns,
or an explicit handoff. The human chooses the outcome; Git state changes still
require explicit approval.

---

## Commit protocol (3 axes)

Before committing, evaluate the change on three axes. Never "hay archivos tocados → commit".

**Eje 1 — Branch**

- `feature/<x>`: intermediate commits allowed (`feat(huN): ...`, `chore(docs): ...`), but never marking DONE prematurely.
- `develop`: only consistent blocks (code + tests + docs together).
- `main`: release-lite — only closed work reflected in canonical docs.

**Eje 2 — Type of change**

- code + tests → strong commit candidate.
- official docs only → commit only if they reflect real code; a doc ahead of the code is not committable (fix the code or downgrade the doc).
- notes/brainstorming → not committable (discard, format into the sprint log, or keep out of the commit).
- refactors without tests → no commit.
- mechanical cleanup → yes, with `chore:`.

**Eje 3 — Stage of the work unit**

- Start: commit on feature branch OK; no DONE, no "falta poquito".
- Middle: commits stay on feature, not develop; don't move statuses.
- Close: commit on feature + PR to develop + `PROJECT_STATE.md` marked DONE with evidence.

Decision format (when a commit needs judgment): 4 blocks — what supports it, what argues against it, recommendation (yes/no/defer), what would be missing for a clear yes.

## Mini glossary

- **Working tree:** actual disk state today.
- **Staging/index:** selected set for the next checkpoint.
- **HEAD:** current commit (official truth).
- **Scope drift:** mixing unrelated changes in one change-set.
