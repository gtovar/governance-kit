---
name: governance-reviewer
description: Use when reviewing whether work complies with this repository's governance — before committing, before closing a session, at phase gates, or when asked for a QA/audit pass. Audits phase compliance, traceability, canonical-doc updates, scope discipline, and open decisions. This skill audits; it does not produce.
---

# Governance Reviewer

Use this skill when:
- the user asks for a review, QA pass, or audit of recent work
- a session is about to close
- a commit or merge is imminent
- a phase gate in `docs/process/PROJECT_MAP.md` is being checked
- you suspect work drifted outside the declared scope

Do not use this skill to write code, fix findings, or extend scope. The reviewer audits and reports; the executor is a separate pass.

## Standard

Judge compliance **in substance, not only in appearance**.

Review against the constitution (`AGENTS.md` at the repository root) and the canonical process docs. The constitution outranks this skill; if they conflict, report the conflict.

## Checklist

For the work under review, verify:

1. **Scope**: does the work fall inside the current scope declared in `docs/process/CURRENT_STAGE.md` (or `PROJECT_MAP.md` if it is missing)?
2. **Phase**: does it match the current phase and its gates? Was any phase advanced without explicit approval?
3. **Traceability**: can each implementation change be traced back through `need → requirement → spec → plan/task → implementation → verification`? Identify orphans in both directions.
4. **Canonical docs**: were the affected canonical artifacts updated in the same change (PROJECT_MAP, CURRENT_STAGE, decision records)?
5. **Facts vs inferences**: does any claim present an inference, hypothesis, or risk as a verified fact?
6. **Invented requirements**: was any product requirement invented, or modified to justify existing code?
7. **Premature architecture**: was architecture, infrastructure, tooling, or process introduced without a documented need?
8. **Silent decisions**: was any decision made implicitly that the rules require to be recorded as an open decision or ADR/DDR?
9. **Useful comments**: do added comments explain why (intent, tradeoffs, invariants) rather than restate code? (see `useful-comments-reviewer`)
10. **Engineering baseline**: does the code comply with `docs/good_practices.md` (naming, structure, SOLID, error handling, testing)? Flag concrete violations with `file:line`.
11. **Handoff**: if this is a session close, verify the close ritual in `docs/session_rituals.md` and the handoff obligations in `AGENTS.md` were followed.
12. **Repo health lens (5 dimensions)**: evaluate the change against — (a) Correctitud: does it work, are key tests passing or explained; (b) Coherencia arquitectónica: do names reflect responsibilities, are layers and contracts consistent; (c) Mantenibilidad: is it modular and conventionally structured, would changing it break unrelated things silently; (d) Seguridad/privacidad: secrets out of the repo, **no PII in logs/screenshots/fixtures**, least-privilege credentials; (e) Operabilidad: reproducible instructions, useful logs, sane local setup.

## Output format

Report findings first, ordered by severity:

```text
BLOCKER  — violates a hard rule or gate; work must not proceed/close
WARNING  — degrades governance but does not violate a gate
ADVISORY — improvement aligned with the constitution
```

Each finding must cite evidence: `file:line` or the governing rule it violates. Include one line of recommended action per finding.

When findings may enter the gatekeeper's `reconcile` mode, also classify the
recommended action as `MECHANICAL`, `JUDGMENT_REQUIRED`, `TRANSITION`, or
`EXTERNAL_OR_DESTRUCTIVE`. Classification helps the executor request the right
authorization; it does not authorize the reviewer to fix anything.

If no findings exist, say so explicitly and state which checks passed.

Do not fix findings in the same pass. Deliver the report and let the executor act, unless the user explicitly asks for the fix in the same pass.

## Anti-patterns

- Reviewing only the diff and not the affected canonical docs.
- Approving because "it works" without checking phase and traceability.
- Downgrading a BLOCKER to a WARNING because it is inconvenient.
- Producing a general opinion instead of findings with evidence.
- Calling a semantic or phase-changing correction mechanical because its diff
  would be small.
