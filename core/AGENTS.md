# Project Constitution

This file is the constitution for any AI agent working in this repository (opencode, Claude Code, Codex, Gemini, or future agents). It is the entry contract, not a manual.

The repository is the canonical source of project knowledge. Do not rely on prior chat history or agent-specific memory as the source of truth.

## Start here

Before significant work, follow this canonical re-entry order:

1. `README.md` — repository entry point, when available.
2. `docs/process/CURRENT_STAGE.md` — current phase, objective, scope, and next allowed work.
3. `docs/process/PROJECT_MAP.md` — project position and phase map.
4. `docs/process/DEVELOPMENT_WORKFLOW.md` — development phases and gates;
   required on first entry and whenever the phase changed.
5. `docs/index.md` — canonical documentation map.

Then read only the documents relevant to the current task.

## Working rules

- Respect the current phase and gates defined in `docs/process/DEVELOPMENT_WORKFLOW.md`.
- Do not advance to another phase without explicit approval.
- Do not invent missing product requirements.
- Distinguish verified facts from inferences, hypotheses, risks, and open decisions. Label them as such.
- Keep exploration, specification, technical design, and implementation separate.
- Do not introduce architecture or infrastructure before a documented need requires it.
- Prefer small, reviewable, reversible changes.
- Do not create documentation, abstractions, agents, or processes without a concrete consumer or problem.
- Keep one actionable frontier: name the action, exact target or decision, and
  observable completion condition. Never make an undefined collection such as
  "remaining findings" or another broad review the next step.
- Warnings, advisories, historical text, and unused templates do not become
  blockers or active work unless a current gate explicitly requires them.
- Keep canonical project artifacts agent-agnostic.
- All canonical artifacts (code, comments, docs, templates, commit messages) are written in **English**. Conversation with the human may be in Spanish.
- If required information is missing, record an open decision instead of silently choosing.
- Do not modify product requirements merely to justify an existing implementation.
- Do not implement a feature merely because it appears in an idea, observation, or backlog.

## Rule precedence

When rules or documents conflict, resolve in this order:

1. **This constitution** (invariant rules) — mandates until formally changed.
2. **Operating policy** (section below) — how to work with the human.
3. **Current state** (`docs/process/CURRENT_STAGE.md`) — beats old examples and historical documents.
4. **Reference library** (`docs/`) — context, not authority; consulted when its activity fires.

Historical documents provide context; the current state overrides old examples. If a reference document contradicts the code, the code wins and the document is corrected.

## Operating policy (truth discipline)

- Label every important claim: `HECHO` (verified), `HIPÓTESIS` (plausible, unvalidated), `DECISIÓN PENDIENTE`, or `RIESGO`. Never present inference as fact.
- Without repository evidence, state `NOT VERIFIED` — never judge code or docs you have not read.
- Use the `decision-expander` skill only when its activation policy applies.
  Do not expand already-defined, local, reversible work by reflex.
- No destructive or irreversible action without explicit confirmation.
- If the human gives ambiguous instructions, ask the minimal question needed to proceed without guessing; do not invent intent.

## Routing by activity (si toco X → consulto/actualizo Y)

The documents below are installed in this repository and are binding when their activity fires. Do not wait to be told:

| If you touch X | Consult and apply Y |
| -------------- | ------------------- |
| Code (any language) | `docs/good_practices.md` — naming, structure, SOLID, error handling, testing, security. Apply by default; do not skip "because MVP". |
| Code comments | Useful comments rule below + `useful-comments-reviewer` skill (judgment) + `scripts/comment-hygiene.sh` (deterministic) |
| Canonical docs (create, update, split) | `docs/documentation_rules.md` — gates G0–G3, DDR, language/tone, layer separation |
| Architectural decisions | `docs/ADR_POLICY.md` — ADR vs DDR vs none |
| Git status / staging / commits | `docs/git_hygiene.md` — Desk/Tray/Canon, Product/Artifact/Experiment, commit protocol (3 axes) |
| Project state docs (`PROJECT_STATE.md` etc.) | `docs/templates/project_state_fill_guide.md` — fixed structure, 4 triggers, snapshot |
| User stories / HUs | `docs/templates/HU_template.md`, `empezar_historia.md`, `cerrar_historia.md` |
| New repository docs | `docs/templates/` — use the fixed templates; never invent section layouts |
| Doc health | `scripts/doc-health.sh` — must be clean before closing a work block |
| Session start / re-entry | `docs/session_rituals.md` (start ritual) + `governance-gatekeeper` skill (intent routing) |
| Kit update check | `scripts/governance-kit-update.py check` — advisory GitHub Release discovery; inspect and approve before applying |
| Session close / handoff | `docs/session_rituals.md` (close ritual) + Handoff section below |
| Tests (choosing depth) | `docs/TESTING_STRATEGY.md` — smallest test that proves the risk |
| Reusable lesson found | `docs/learning_capture.md` + `scripts/learning-capture.sh` (append to inbox) |

If a matrix entry is missing for the activity at hand, follow the nearest existing rule and record an open decision; do not improvise silently.

## Phase awareness (anti-MVP rule)

- Do not optimize for time, effort, or cost unless the human explicitly asks. The project phase is declared in `docs/process/CURRENT_STAGE.md`; act according to that phase.
- Do not degrade quality "because this is an MVP" and do not skip security, tests, or documentation for that reason.
- Before proposing or executing work, state the phase you are acting in. If the phase is not documented, ask or record an open decision — do not assume the project is a prototype.
- When a project stops being a prototype, that transition must be explicit in the canonical docs, never silent.

## Useful comments

Code comments must explain why: intent, context, tradeoffs, invariants, warnings, non-obvious constraints. Remove comments that restate obvious code, narrate control flow, or are stale. If a comment is compensating for confusing structure, prefer refactoring. The `useful-comments-reviewer` skill holds the full review standard.

## Session governance

- Before acting, verify the intended work against the current scope in `docs/process/CURRENT_STAGE.md`. Cite the document that authorizes the change.
- If `CURRENT_STAGE.md` names no actionable frontier, report that single defect
  and resolve it once; do not create an open-ended findings inventory or repeat
  re-entry as the next action.
- Propose; await explicit approval for anything outside the declared scope.
- Before closing a meaningful session, follow the Handoff section below.

## Commit boundary

Do not wait for the human to request a commit before protecting a coherent
checkpoint. Activate `commit-readiness` before starting new implementation when
one or more strong signals are present:

- a declared subtask or logical slice has been completed;
- code, tests, and required documentation for one slice are aligned;
- a new request would change or expand scope while the previous slice remains
  uncheckpointed; or
- the working tree is beginning to mix unrelated concerns.

Do not infer a completed slice from elapsed time, a single changed file, or an
unverified assumption.

When the boundary activates, inspect the working tree and relevant diff in
read-only mode. State that `commit-readiness` is active, propose the coherent
checkpoint, separation, or handoff, and obtain the human's decision before
continuing into the new scope. Staging, stashing, committing, pushing, and
other state-changing Git actions always require their own explicit approval.

## Current scope

The active scope is defined by `docs/process/CURRENT_STAGE.md`. If that file does not exist yet, use the current state recorded in `docs/process/PROJECT_MAP.md`. Work only within that scope unless explicitly asked to expand it.

## Specifications and implementation

Features must follow the workflow appropriate to their current phase. When implementation becomes active, preserve traceability:

```
need → requirement → spec → plan/task → implementation → verification
```

## Commands

Project-specific build, test, lint, formatting, and validation commands belong here once they actually exist. Do not invent placeholder commands.

## Handoff

After meaningful work:

- update the affected canonical artifact;
- update `docs/process/CURRENT_STAGE.md` if project state changed;
- update `docs/process/PROJECT_MAP.md` if a phase status changed;
- record unresolved decisions;
- state the next allowed piece of work.

A new agent should be able to continue from repository state without requiring the previous conversation.
