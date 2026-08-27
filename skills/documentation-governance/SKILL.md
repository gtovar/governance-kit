---
name: documentation-governance
description: Use when deciding whether to update, create, move, split, or defer persistent repository documentation — canonical docs, architecture or contract docs, decision records, roadmaps, project-state updates, or requests to prevent duplicate or orphaned docs. Produces a Documentation Decision Record for non-trivial decisions.
---

# Documentation Governance

Use this skill when:
- a change touches canonical repository documentation
- you are unsure whether to create, extend, or split a document
- you must decide whether something is a fact, decision, plan, hypothesis, or history
- you need to record a documentation decision (DDR)

Do not use this skill for casual notes, chat-only content, or files outside the repository.

## Source of truth

Read `docs/documentation_rules.md` completely before acting. It defines the canonical policy: language and tone, the decision-maker gates G0–G3, the DDR template, and the scoring table. Do not duplicate its rules in this skill.

`docs/ADR_POLICY.md` decides whether a decision is ADR-worthy, DDR-worthy, or still too tentative.

## Workflow

1. Classify the proposed content as one of: fact, decision, plan, hypothesis, history, derived insight.
2. Identify the primary evidence for every factual claim. If a claim lacks evidence, defer it or label it as hypothesis.
3. Read the nearest canonical index (for example `docs/index.md`, or the project's documentation map) to find the existing owner.
4. Apply the decision-maker gates from `docs/documentation_rules.md`:
   - **G0 Evidence gate** — no primary evidence → no canonical doc; open question instead.
   - **G1 Owner doc gate** — an owner exists → update it, do not create.
   - **G2 Split gate** — only create/split if at least one condition C2.1–C2.5 holds.
   - **G3 Anti-duplication gate** — new doc declares Scope, Owner, "Single Source of Truth" line, and updates the index.
   - Use the 0–10 scoring table when the verdict is not obvious (<=4 update, 5–6 update+link, >=7 create).
5. For non-trivial decisions, produce the DDR from the template in `docs/documentation_rules.md`. Keep it short.
6. Make the scoped change and update the nearest index in the same change.
7. Validate the diff: links, paths, evidence, ownership. Run `git diff --check` and `scripts/doc-health.sh` when available.

## Boundaries

- Do not duplicate rules from the constitution (`AGENTS.md`); point to it instead.
- Do not create Email-Cleaner-era or other inherited paths merely because an old rule names them. Follow this repository's owner documents.
- Follow the language and audience of the local owner document; do not force a language.
- Do not add hooks, CI gates, or plugins unless a separately approved decision defines an objective invariant and its failure behavior.
- Do not bulk-export repository knowledge into personal wikis. Promote only curated notes with repository, commit, sources, and date.

The DDR template lives in `docs/documentation_rules.md`. Minor scoped edits follow the owner document directly.
