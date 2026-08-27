# Session Rituals (Canonical)

> **Vehicle**: `governance-gatekeeper` skill (intent router that invokes these rituals) + routed from the constitution (Session governance). Audited by the `reviewer` subagent (check #11 Handoff).
> **Authority**: normative.

Rituals make conversational memory unnecessary. They run with fixed durations in minutes, not as "good intentions".

## Start ritual (reentry, ~3 min)

1. Follow the canonical re-entry order in `AGENTS.md` under **Start here**.
   Do not define a second order in this document.
2. When `scripts/governance-audit.py` exists, run it once after reading the
   canonical entry documents:
   - no findings: continue normally;
   - warnings: report them and reconcile only when the current scope or user
     request authorizes that work; warnings do not change the phase, block a
     gate, or become the session objective by themselves;
   - blockers: make `reconcile` the primary intent, but do not mutate files
     without the authorization required by the reconciliation protocol;
   - unable to run reliably: report the limitation and remain fail-open.
3. Declare the block's objective in ONE sentence (mini-block, below) and
   contrast it with the "next allowed work" in `CURRENT_STAGE.md`: if it does
   not match, declare it explicitly before working.
4. Validate that the frontier names one action, one exact target or decision,
   and one observable completion condition. If it does not, report
   `NON_ACTIONABLE_FRONTIER` once and route directly to repairing that owner;
   do not launch a broad findings review.
5. When `scripts/governance-kit-update.py` exists, run
   `python3 scripts/governance-kit-update.py check`. Report an available update
   as advisory; inspect and apply it only after explicit human approval.

Rule: "Monday" is the moment you resume, not the calendar day.
Re-entry ends after this single pass. Never make another re-entry or audit the
next action unless new evidence appears.

## Mini-block (start of every work block)

Four fixed elements before executing:

```text
1. Detected intent:                 (1 sentence)
2. FACT / HYPOTHESIS / PENDING DECISION:  (3 bullets)
3. Minimum next step:               (1 action)
4. Missing evidence:                (1 bullet)
```

Forces iteration and avoids the "solve it all in one go" pattern.

## During the session

- The constitution's routing matrix ("if I touch X → consult/update Y") governs every activity. Do not wait for the human to name it.
- On drift signals (work expanding scope, docs contradicting code): interrupt with the gatekeeper format.
- Before accepting work that changes or expands scope, apply the constitution's
  **Commit boundary** rule. A coherent uncheckpointed slice requires a
  `commit-readiness` decision before further implementation.
- Agreed trigger word: if the human writes **"revisa lógica"**, activate analytic mode: risks, assumptions, 2-3 alternatives, 1 recommendation — before answering.

## Close ritual (close-session, ~5 min)

A read-only re-entry with no state change does not trigger this ritual.

1. Update `PROJECT_STATE.md` per its fill guide (snapshot, one single next action).
2. Add 3 bullets to the sprint log: **what was done / what was learned / what's next** (mini-retro, factual).
3. Run tests if applicable (guard rail).
4. If contracts changed (API/events), update those docs before closing.
5. Run `scripts/doc-health.sh` — must be clean.
6. Record newly changed open decisions in `CURRENT_STAGE.md` and declare one
   actionable frontier using `Action`, `Target`, and `Done when`.
7. After a successful integration, perform the advisory local branch lifecycle
   review in `docs/git_hygiene.md`. Report candidates only; a local-branch
   deletion requires a separate explicit human instruction.

A new agent must be able to continue reading only the canonical artifacts — without the previous conversation.

## Truth hierarchy (when docs and code contradict)

1. Code (what exists and runs) — strongest truth.
2. Automated tests.
3. Living documentation (PROJECT_STATE, sprint log, ADRs).
4. Loose notes.

If there is divergence: declare it with an explicit sentence ("the code says X, the doc says Y") — do not ignore it or assume one of them is right.
