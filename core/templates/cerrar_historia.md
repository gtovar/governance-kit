# Template: Close Story (DoD — binary gate)

An HU is not closed until ALL of these points are true. It is not debatable: either it is done, or it is not.

## DoD Checklist (Definition of Done)

- [ ] Functional code and, when applicable, green tests.
- [ ] `PROJECT_STATE.md` updated (last completed task / next agreed step).
- [ ] `Sprint_Log.md` updated with 3 bullets: what was done / what was learned / what's next.
- [ ] If there was an irreversible decision: ADR created in `docs/adr/` and linked from `docs/index.md`.
- [ ] If code was touched that the routing matrix associates with a document (API, events, models, etc.): that document is updated — not pending for "later".
- [ ] `scripts/doc-health.sh` run and clean (no broken links, no unbalanced fences, no orphan docs).
- [ ] Closing commit done per `docs/git_hygiene.md` (code + docs in the same commit, message that tells the complete story).

## Cross-validations (before marking DONE)

Confirm coherence with:

- `docs/documentation_rules.md` — is the correct document the owner of each piece of information (no new duplicates)?
- `docs/TESTING_STRATEGY.md` — does the test depth reached meet what that document defines as "sufficient"?
- `docs/git_hygiene.md` — is the history readable and explainable to "future you"?

## If any of this is NOT met

The HU is not closed. It is documented honestly in `PROJECT_STATE.md` as `IN_PROGRESS` or `BLOCKED` (never as partial `DONE`) and exactly what is missing is noted.
