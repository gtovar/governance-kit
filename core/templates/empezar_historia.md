# Template: Start Story

Checklist and prompt to start a new HU. The central question is not "is this HU valid in isolation?" but:

> Where is the project REALLY (according to the code and living docs) and does this HU make sense NOW?

## Before writing or accepting the HU

1. Re-read `PROJECT_STATE.md` — does the proposed HU fit the "next agreed step", or is it skipping it?
2. Re-read `Sprint_Log.md` (last block) — is there something "half closed" that should be finished first?
3. Confirm the "Ready criterion" from `docs/workflow.md`: green tests (if they exist), clean `git status`, clean doc-health.
4. Classify the HU: functional (uses `HU_template.md` format) or technical task (issue: title + steps + risks + impact)?

## Truth hierarchy to respect during work

1. Code (what exists and runs) — strongest truth.
2. Automated tests.
3. Living documentation (`PROJECT_STATE.md`, `Sprint_Log.md`, ADRs, HUs).
4. Loose notes.

If during work you find something the documentation says but the code contradicts (or vice versa), declare it explicitly — do not ignore it or assume one of them "must be right".

## Prompt to invoke the "where are we and what's next" analysis

> Act as senior architect, functional analyst, QA lead, and custodian of this project's documentation process.
> Your goal is NOT to validate an isolated HU, but to answer: where is the project really (per the code) and which is the next best task?
> Use the truth hierarchy from `docs/documentation_rules.md`. Compare real code against `PROJECT_STATE.md`, `Sprint_Log.md`, and the ADRs. Classify each doc as "aligned", "behind", "ahead", or "confused/contradictory". If I pass a `PROPOSED_HU`, evaluate whether it makes sense now, whether something must come first, or whether it is a duplicate — and if it is badly framed, propose a corrected version.
