---
name: governance-gatekeeper
description: Use when governed repository work needs intent routing, re-entry, reconciliation, commit or deploy checks, or handoff. Loads governing docs, routes verified drift into authorized mechanical remediation, and pauses for missing decisions or permissions.
---

# Governance Gatekeeper

This skill executes the repository's governance system. It does not define the law by itself — the constitution (`AGENTS.md`) wins in any conflict.

Use this skill when:
- the user wants to code, edit, commit, deploy, or resume work
- the task may impact docs, architecture, workflow, setup, or state tracking
- an audit found documentation or state drift that should be reconciled
- the user is vague and the agent must infer which process applies
- the session should end in a recoverable state

Do not use this skill for casual conversation or requests unrelated to repository work.

## Operating Goal

Detect what the user is trying to do, load the governing docs, identify missing obligations, and either:
- allow execution, or
- interrupt and redirect with a short operational explanation

## Execution Contract

1. **Identify the active repo and scope** from `docs/process/CURRENT_STAGE.md` (fallback: `PROJECT_MAP.md`).
2. **Infer the primary intent** from the operating modes below; propose one primary and at most one alternate.
3. **Load the governing docs** for that intent (the routing matrix in `AGENTS.md` maps activity → docs).
4. **Detect missing obligations** before implementation proceeds (state updates, ADR/DDR, templates, doc-health, handoff).
5. **Interrupt** with the standard format when obligations are missing.
6. **Reconcile** detected drift only through the governed reconciliation
   protocol below; an audit by itself does not authorize mutation.

Do not restate governance rules from memory when the authoritative files can be loaded directly. Use the docs as law and this skill as the execution adapter.

## Operating modes

```text
reentry          — resuming after time away
work             — implementing, editing, documenting
reconcile        — aligning canonical state after drift or an audit
close-session    — leaving the repo in a recoverable state
commit-readiness — checking whether a logical unit is ready to commit
deploy           — shipping to an environment
decision-record  — an architectural/structural decision may need ADR or DDR
learning-capture — a reusable lesson was found and should be captured
```

### Clarification gate

Do not force a clarification interview when intent, scope, and risk are clear enough to act. Ask only when at least one of these is true:
- the active repo or scope is materially ambiguous
- multiple intents are plausible and the order changes the outcome
- the task is destructive, architectural, deploy-related, or otherwise high-risk
- the user named constraints that are incomplete or internally conflicting

### Intent chain

If multiple intents apply, build the chain before doing work: prerequisites run first, blocking intents complete before dependents. If the order is ambiguous, propose an order and pause for confirmation.

### Proactive commit boundary

Do not require the user to say "commit" before activating `commit-readiness`.
Before a new implementation request, look for strong boundary signals from the
conversation and repository evidence:

- a declared subtask or logical slice is complete;
- code, tests, and required documentation for one slice are aligned;
- the new request changes or expands scope while the previous slice is
  uncheckpointed; or
- the working tree mixes unrelated concerns.

Do not infer a completed slice from elapsed time, one changed file, or an
unverified assumption. When a signal is present, inspect `git status` and the
relevant diff in read-only mode, then interrupt before new implementation.

Use this short decision prompt:

```text
Commit-readiness activated:
Evidence:
Recommended boundary:
Decision needed: evaluate a checkpoint, separate changes, or leave an explicit handoff?
```

Do not stage, stash, commit, push, or write a handoff until the human has
authorized that specific state-changing action. After the decision, resume only
within the authorized boundary.

### Convergence gate

Before accepting `CURRENT_STAGE.md` as operational state, validate its single
frontier. It is actionable only when it names:

- one imperative action;
- one exact file, decision ID, or gate;
- one observable completion condition.

An instruction such as "review the remaining findings" is invalid unless the
same frontier points to an existing, bounded inventory by exact coordinate.
Do not create that missing inventory merely to satisfy the reference. Report
`NON_ACTIONABLE_FRONTIER` once and route directly to repairing the owner state.

Re-entry and reconciliation must converge:

- run the entry audit at most once per session unless new evidence appears;
- report warnings once, but never promote them into blockers, phase work, or
  transition conditions without an explicit governing rule;
- never make "re-enter", "review again", "audit again", or an equivalent action
  the next frontier after the same operation just completed;
- when gate evidence is satisfied and no real blockers remain, make the single
  gate transition decision the frontier instead of starting another review;
- stop expanding findings when every gate criterion has a verified outcome.

### Session rituals

- `reentry` → follow the start ritual in `docs/session_rituals.md`, including
  the advisory `governance-kit-update.py check` when installed. Report a newer
  release and obtain explicit approval before `apply`.
- `close-session` → follow the close ritual in `docs/session_rituals.md`

### Governed reconciliation

When the user asks to make the current phase or canonical documents consistent,
or an audit finds drift that should be fixed, read
[`references/reconciliation.md`](references/reconciliation.md) completely and
follow it. That protocol defines finding classes, authorization boundaries,
batch execution, validation, and stopping conditions.

`governance-reviewer` remains read-only. Its findings may start `reconcile`
mode, but the gatekeeper is the executor only after the required authorization.

## Interruption Format

When blocking or redirecting, keep it short:

```text
Detected intent:
Governing docs:
Missing obligations:
Required next action:
```

## Execution Style

- Prefer short operational outputs over essays.
- Challenge drift early.
- Do not wait for the user to name the right document.
- After a declared batch set is authorized, do not ask for separate approval
  for each mechanical batch. Pause only when the authorized boundary is crossed
  or the platform itself requires confirmation.
- Do not assume examples are exhaustive.
- Treat forgetting as a system design problem, not as user error.
- Prefer a closure decision over a complete inventory of non-blocking debt.
