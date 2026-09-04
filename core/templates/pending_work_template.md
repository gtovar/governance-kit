# Pending Work

**Scope:** <one sentence: what deferred work this ledger tracks and its boundary>
**Owner:** The current stage in `docs/process/CURRENT_STAGE.md` defines the active item.
**Single Source of Truth:** This document is the source of truth for deferred
work; the current phase and immediate action remain in
`docs/process/CURRENT_STAGE.md`.

## Format rules

- Group entries under a `##` heading per area or component. Do not create a
  new area heading for a single one-off item; use the nearest existing area
  or a short-lived "Misc" heading.
- Prefix every entry with its status and date, bold: **Added YYYY-MM-DD**,
  **Resolved YYYY-MM-DD**, **Fixed YYYY-MM-DD**, or **Corrected YYYY-MM-DD**.
- State *why* the item is deferred: a pending product/UX decision, a missing
  authorization, or explicitly out of scope for the current frontier — not
  just that it exists.
- When something is found incidentally while doing other authorized work,
  record it as **Found, not fixed (pre-existing, unrelated to this slice)**
  instead of silently fixing it (scope creep) or silently dropping it
  (lost knowledge).
- Cite real evidence for a resolution: file, test, commit hash, or ADR —
  never "should work now" without a verification trail.
- Do not use this document for the current authorized frontier; that stays in
  `CURRENT_STAGE.md`. This document is for everything else that was found,
  deferred, or closed along the way.
- Update this document in the same change that finds or resolves the item;
  do not batch retroactively at session close.
- This document is a template consumer of `docs/documentation_rules.md`'s
  gates; it does not replace an ADR when the deferred item is itself an
  architectural decision (see `docs/ADR_POLICY.md`).
- When you instantiate this template as `docs/PENDING_WORK.md` (or an
  equivalent name), add it to `docs/index.md` in the same change — an
  unindexed doc fails `scripts/doc-health.sh`'s ghost-doc check.
- A Resolved/Fixed entry that no longer informs any currently open item moves,
  verbatim, to `docs/PENDING_WORK_ARCHIVE.md` under the same area heading, in
  the same change that archives it. This is manual (entries are grouped by
  area, not by date, so `scripts/log-hygiene.sh archive` — built for
  date-headed logs — does not apply here); `scripts/log-hygiene.sh check`
  flags this file when it exceeds ~300 lines as a prompt to do that review.

## Archive convention (once `docs/PENDING_WORK_ARCHIVE.md` exists)

Add a line to this file's own header: **Archive:** entries resolved before
this ledger's current scope moved to `docs/PENDING_WORK_ARCHIVE.md` (link it,
and add it to `docs/index.md` in the same change it is first created).

## <Area name>

- **Added YYYY-MM-DD — pending <X> decision:** <what was found, and why it
  needs a decision instead of being fixed outright>.
- **Resolved YYYY-MM-DD:** <what was fixed>, verified by <evidence — test
  name, command, commit>. See <doc/ADR/Sprint_Log entry> for the full record.
  - **Found, not fixed (pre-existing, unrelated to this slice):** <what was
    found while doing the above, and why it is out of scope here>.
