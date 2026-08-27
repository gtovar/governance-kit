# README_REENTRY.md — Template

Re-entry document: resume work after days, weeks, or months, in ≤ 5 minutes.

Question it answers: "What do I need to read, check, run, and remember to get started again?"

## Mandatory sections (6)

1. **Current Context Snapshot**
   - Brief description of current HU and repo state.
   - Branch in use.

2. **What Changed During the Last Session**
   - Only factual changes.
   - No design, no architecture.

3. **Exact Commands to Resume Work**
   - First real executable command.
   - Health URLs or verification commands when applicable.

4. **Where the Workflow Stopped**
   - The last exact point of progress.

5. **Immediate Next Step**
   - The next technical action to continue work.

6. **Technical Quick Reference**
   - One-liners or key files involved.
   - Reentry Status: clean, blocked, or mid-work.

## Forbidden

- Explaining historical decisions (they belong to the ADRs).
- Duplicating `PROJECT_STATE.md` (that is the snapshot; this is the startup manual).
- Including API or roadmap.
- Long sentences; factual and direct tone.

## Sync rule

Update when the workflow or the re-entry point changes.
Each significant edit references its commit.
