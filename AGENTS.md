# governance-kit

This repository IS the portable governance kit: the "gem" of rules, skills, and configurations installed into any project so an AI agent loads the way of working without explanation.

## For an agent working HERE (in the kit)

- The kit's content lives in `core/`, `skills/`, `adapters/`, `hooks/`, `profiles/`, `scripts/`. Do not edit installed copies in other projects; edit here and reinstall.
- Before changing anything, apply the kit's own constitution: `core/AGENTS.md` (the norm the kit installs).
- Working rules: same as the kit installs — phases, gates, fact vs inference, small reversible changes, no abstractions without a consumer, record open decisions.
- Language: all kit artifacts are English (canonical rule).
- The kit's roadmap lives in `README.md` (Roadmap section). Do not advance roadmap phases without explicit user approval.
- Handoff: after meaningful work, update `README.md` (Roadmap) and record open decisions.
- Deterministic gates for the kit itself: `scripts/check-skills-lock.py` and `scripts/check-registry.py` must pass before closing a change to `skills/` or the registry.

## For installing the kit into another project

See the kit's `README.md` or run `bin/install.sh`.
