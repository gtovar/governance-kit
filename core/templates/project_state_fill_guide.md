# PROJECT_STATE Fill Guide

This document defines how `PROJECT_STATE.md` must be filled in this repository.

This repo uses the shared workspace `PROJECT_STATE` contract.
The structure and required labels below must remain identical across repos.

---

## 1. Master Template

Every `PROJECT_STATE.md` must include this top-level shape:

```md
# PROJECT_STATE.md — <Repo Name>

Single source of truth for the current technical state of this repo.
[Last update: YYYY-MM-DD — Commit: <hash | pending>]

---

## 1. Technical Header (Snapshot Metadata)

PROJECT_NAME: <exact project name>
SNAPSHOT_DATE: <YYYY-MM-DD HH:MM>
COMMIT: <hash | pending>
ENVIRONMENT: <local | develop | main | feature/...>
REPO_PATH: <absolute repo path>
BRANCH: <branch name>
WORKING_TREE_STATUS: <Clean | Dirty (modified files present)>
TEST_STATUS: <PASS | FAIL | Not run>

## 2. Executive Summary

## 3. Component-by-Component Technical State

Per component: Status (ok/warn), tests passing, endpoints active, fallback behavior.

## 4. User Story Status (Evidence-Driven)

### HUXX — <name>

**Status:** DONE | IN_PROGRESS | BLOCKED | BACKLOG
**Evidence:**
- <files, routes, tests>
**Open items:**
- <missing technical items only>
**Technical risks:**
- <objective risks only>
**Recent change:**
- <1–2 factual lines, optional commit>

## 5. Current Technical Risks

## 6. Next Immediate Action

➡️ <one single technical step, realizable in 5–15 min>

## Version log

- YYYY-MM-DD — <description> (commit: <hash | pending | none>)

END OF FILE
```

---

## 2. Hard Rules

- **Only 4 triggers to update**: (1) a user story changes status; (2) architecture really changes (routes, services, contracts, containers, files); (3) a critical test changes project state; (4) a real technical component is added. **Never** update for opinions, plans, ideas, or wishes.
- **Snapshot semantics**: every edit is a complete snapshot (rewrite the full state, not only the diff). Previous version goes to the version log or history.
- **One single next action**: end always with one instruction realizable in 5–15 minutes. Lists of 3/5/10 steps are forbidden.
- **Evidence-anchored**: every HU claims evidence (files, tests, endpoints). Forbidden: "almost ready", "might be finished". No evidence → not DONE. ("Lying to the future" is a governance failure.)
- **Coordinates**: exact identifiers for files, endpoints, env vars, tests, commits.
- **Layer discipline**: this file holds factual state only. No backlog, no roadmap, no process definitions, no tutorials, no opinions, no debugging notes.
- **Technical truth overrides**: if this file contradicts the code, the code wins and this file is corrected immediately.
- **Language**: English only. Tone: formal, neutral, factual ("Exists", "Was validated"); forbidden "probably", "should", "we plan".
- **Concurrence**: DONE requires a real commit and consistency across sections (zero internal contradictions).

---

## 3. Relationship to Other Docs

- `PROJECT_STATE.md` is the factual snapshot.
- `README_REENTRY.md` is the operational restart document.
- `Sprint_Log.md` is the factual event history.

Do not duplicate long factual state from `PROJECT_STATE.md` into `README_REENTRY.md`.
