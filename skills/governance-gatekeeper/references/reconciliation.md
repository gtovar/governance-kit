# Governed Reconciliation

Read this reference only in `reconcile` mode.

## Outcome

Turn verified governance drift into a consistent repository state without
requiring the human to prescribe files, lines, prompts, or validation commands.
Preserve project-owned truth and stop before semantic decisions or phase
transitions.

## Preconditions

1. Complete re-entry and state the active phase.
2. Run `python3 scripts/governance-audit.py` when available.
3. Use `governance-reviewer` for the read-only audit when gate compliance or
   broad consistency is in question.
4. Load owner documents through `AGENTS.md` and `documentation-governance`.

An audit finding is evidence of drift, not permission to edit.

## Convergence contract

A reconciliation inventory is bounded only when each finding has an identifier,
an exact source coordinate, a stated relationship to the active gate, and an
observable closure condition. A reference to "remaining findings", "pending
issues", or another collection that does not exist canonically is itself one
`NON_ACTIONABLE_FRONTIER` defect. Do not respond by inventing an exhaustive
inventory.

Apply severity literally:

- `BLOCKER` may prevent the active gate only when its evidence contradicts a
  gate criterion;
- `WARNING` and advisory findings are reported once and remain non-blocking;
- historical or stale text and unused templates are non-blocking unless the
  active gate explicitly requires them;
- an open decision blocks only the criterion that depends on its answer.

Do not rerun an unchanged audit, reopen an already classified finding, or make
another broad review the output of reconciliation. New evidence is required to
repeat any of those operations.

## Finding classes

Classify every proposed correction before requesting authorization:

| Class | Meaning | Default behavior |
| ----- | ------- | ---------------- |
| `MECHANICAL` | One owner and one evidence-backed correction; no product meaning, policy, phase, or gate outcome changes | May be included in one declared batch authorization |
| `JUDGMENT_REQUIRED` | Translation, ambiguous wording, ownership conflict, policy choice, product meaning, or other semantic interpretation | Pause for the smallest decision needed |
| `TRANSITION` | Closes or advances a phase/gate, changes allowed work, or changes a lifecycle status beyond reflecting an already authorized fact | Require explicit transition approval |
| `EXTERNAL_OR_DESTRUCTIVE` | Commit, push, deploy, delete, overwrite protected state, or affect another repository/system | Follow the repository and platform approval rules |

Do not downgrade a finding to `MECHANICAL` merely because the expected edit is
small. Classification depends on meaning and authority, not line count.

## Independent judgment decisions

When two or more `JUDGMENT_REQUIRED` findings can be answered differently
without contradiction, treat them as independent decisions. They may be
inventoried and ordered together, but they must not share a decision question,
recommendation, or implementation authorization.

For independent decisions:

1. label and describe each decision without presupposing its outcome;
2. use `decision-expander` only to recommend which one should be resolved first;
3. make exactly one decision the active frontier and leave the others open;
4. ask the smallest question that resolves that frontier, then stop;
5. after the answer, execute only if the user also authorized its bounded
   implementation; otherwise present that implementation boundary and request
   authorization.

One decided frontier may require coordinated edits to multiple owner files.
Those edits can share one authorization when they implement only that decision.
Do not combine unrelated policy, publication, integration, product, or
transition choices merely because they were discovered in the same audit.

## Batch design

Create the smallest independently valid batches. For each batch declare:

- exact owner file or bounded file set;
- verified contradiction and primary evidence;
- intended outcome, without inventing prose the evidence does not support;
- finding class;
- validation commands;
- dependencies and stopping conditions.

Order batches by evidence dependency. Repair discoverability before relying on
it, update an owner before derived mirrors, and leave translations or semantic
rewrites until their source state is stable. Derive the concrete order from the
repository; do not encode a project-specific filename sequence as policy.

## Authorization contract

Ask once for the declared set of `MECHANICAL` batches. The request must name the
files, intended outcomes, validations, and exclusions in language a human can
review without writing an implementation prompt.

This single-authorization rule applies to compatible `MECHANICAL` batches, not
to independent `JUDGMENT_REQUIRED` decisions. An umbrella authorization must
never replace the one-frontier rule above.

After explicit authorization:

1. execute the authorized mechanical batches in dependency order;
2. validate after each batch;
3. continue without asking for batch-by-batch approval;
4. stop immediately if evidence changes, the diff crosses the declared files or
   outcomes, a validation fails ambiguously, or a finding changes class;
5. never treat approval of reconciliation as approval to commit, push, close a
   gate, advance a phase, or mutate another repository.

Platform-required confirmations may still appear. Do not manufacture extra
confirmation loops in the conversational workflow.

## State cascade

When an authorized fact changes repository state, update its existing owner in
the same batch or in the next declared dependent batch. Do not silently leave a
checkpoint instructing agents to repeat completed work.

Project-owned state files remain protected from installer/update overwrites.
Reconciliation edits them only inside the project, with evidence and authority.

## Validation and close

Run the smallest checks that prove the affected risk. When available, include:

```text
python3 scripts/governance-audit.py
scripts/doc-health.sh
git diff --check
```

Inspect untracked canonical files explicitly because `git diff` does not show
their contents. Finish with a read-only gate audit. Report:

- batches completed;
- validations and evidence;
- unresolved `JUDGMENT_REQUIRED`, `TRANSITION`, or external actions;
- one next allowed action.

Do not declare a gate closed unless that transition was separately authorized.
If validation finds no blocker and the gate evidence is satisfied, report
`READY_FOR_GATE` and ask only for that transition decision. Non-blocking debt
does not justify another findings review.

## Compatibility claims

Do not rewrite agent-compatibility promises as part of mechanical
reconciliation. Their meaning and evidence standard belong to the workflow
owner and are `JUDGMENT_REQUIRED`. A cold re-entry records evidence for the
runtime tested; any broader claim remains an explicit project decision.
