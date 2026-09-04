# Sprint_Log.md — <Component Name>

Sprint: <YYYY-MM>  
Scope: <system or sub-system>  
Backend: <yes/no or repo name>  
Frontend: <yes/no>

---

# Format rules
- Each entry is a factual event: what happened, not what was discussed.
- No user stories. No backlog. No planning.
- No repetition of Project_State.md.
- No opinions or speculation.
- No technical debates without an outcome.
- Only record events that *actually happened*.
- Always in English.
- Chronological order: newest last.
- A short entry (1–4 lines) is the default. This file is also the canonical
  detailed technical record other docs point into (see
  `docs/templates/pending_work_template.md`'s "Full record in Sprint_Log.md's
  X entry" pattern) — a longer entry is correct when it carries real evidence
  (root cause, verification steps, what was found but not fixed), not a
  violation to shrink. Do not pad; do not omit evidence to hit a length.
- This file's *total* size is controlled by archiving old entries
  (`scripts/log-hygiene.sh archive Sprint_Log.md`), not by writing thinner
  entries. See `scripts/log-hygiene.sh check` for the size threshold.

---

# Example entries (delete before using)

## YYYY-MM-DD — HU# <short action>
- <1–2 bullet points of what was completed>  
- <optional: name of components touched>

## YYYY-MM-DD — Documentation updated
- <brief fact>

## YYYY-MM-DD — Environment changes
- <brief fact>

---

# Daily entries (append below)

## <YYYY-MM-DD> — <short factual title>  
- <bullet 1>  
- <bullet 2>
