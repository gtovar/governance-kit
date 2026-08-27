# governance-kit

Portable governance kit for AI-assisted projects. The equivalent of installing a gem in Rails: one command, and the next agent (opencode, Claude Code, Codex, Gemini) enters the project and loads the way of working without anyone explaining it.

## Principles

- **Short constitution, not a manual.** `AGENTS.md` is the entry; it routes to `docs/process/`. Agents auto-load it.
- **Agent-agnostic.** The canon lives in the repository. Per-agent adapters only point to it.
- **Advisory-first.** Rules guide; hooks warn and only block when `GOVERNANCE_ENFORCE=1`. Nothing fails closed: a broken hook never blocks the developer.
- **The kit is the source.** Changes are made here and reinstalled; installed copies are never edited in place.
- **Declared phase, not assumed.** The agent acts according to the phase in `docs/process/CURRENT_STAGE.md`, not an implicit "MVP mode". (Anti-MVP rule in the constitution.)
- **English everywhere.** All canonical artifacts (code, comments, docs, templates, commits) are written in English. Conversation with the human may be in Spanish.

## What it installs

| Layer | Artifact | Scope |
| ----- | -------- | ----- |
| Constitution | `AGENTS.md` | per project |
| Process operating system | `docs/process/` (DEVELOPMENT_WORKFLOW, PROJECT_MAP, CURRENT_STAGE) | per project |
| Documentation policies | `docs/ADR_POLICY.md`, `docs/documentation_rules.md` (G0–G3 gates + DDR + scoring), `docs/git_hygiene.md`, `docs/good_practices.md`, `docs/session_rituals.md`, `docs/TESTING_STRATEGY.md`, `docs/learning_capture.md`, `docs/instruction-registry.json` | per project |
| Canonical index | `docs/index.md` (pre-indexed; anti ghost-doc rule) | per project |
| Fixed-structure templates | `docs/templates/` (15) | per project |
| Deterministic checks | `scripts/` (governance-audit, doc-health, comment-hygiene, learning-capture, check-registry, verify-votes) | per project |
| Skills | `decision-expander`, `governance-gatekeeper`, `governance-reviewer`, `useful-comments-reviewer`, `documentation-governance` | vendored to `.opencode/skills/` and `.agents/skills/` per project (optional: global per machine) |
| Reviewer agent | `.opencode/agent/reviewer.md`; optional `.codex/agents/reviewer.md` with `--adapter codex` | per project |
| Git hook (optional) | `commit-msg.sh` (Conventional Commits, advisory) | per project, `--with-hooks` |

## Installation — on any new machine

```bash
# 1. Get the kit (git clone once published; meanwhile: copy the repo)
git clone <repo-url> governance-kit
cd governance-kit

# 2. Install into a project — by default touches NOTHING of the machine:
#    skills vendored inside the project for OpenCode and Codex, plus docs, reviewer, scripts
./bin/install.sh /path/to/project

# Optional flags:
./bin/install.sh /path/to/project --with-hooks          # advisory commit-msg hook
./bin/install.sh /path/to/project --profile implementation|production
./bin/install.sh /path/to/project --adapter claude|codex|all
./bin/install.sh global                                  # optional per-machine skills
```

- **Portability**: the default mode vendors the same skills to `.opencode/skills/` and Codex's repo-local `.agents/skills/` path → everything travels with the project repo, zero machine-state dependency. `global` is an optional per-machine shortcut, not a requirement.
- **Idempotent**: never overwrites a project's existing files.
- Codex and OpenCode discover project skills from their native paths. Restart the agent if newly installed skills do not appear.
- For new empty projects, additionally: `git init`, personalize `docs/process/CURRENT_STAGE.md` (project name, real phase), and write `README.md`.

## Distribution model (where governance lives and runs)

```text
governance-kit (public repository, single source)
   │  install.sh
   └─→ <project>/                       (installed per-project snapshot, autonomous)
         AGENTS.md         ← auto-loaded every session (opencode/Codex/Claude Code)
         docs/             ← policies + templates routed by the matrix
         scripts/          ← deterministic checks (governance-audit, doc-health, ...)
         .opencode/        ← vendored skills + OpenCode reviewer subagent
         .agents/          ← vendored repo-local skills discovered by Codex
         .codex/           ← optional Codex reviewer subagent (`--adapter codex`)
         .git/hooks/       ← commit-msg (optional)
         .governance-kit/  ← installation manifest (enables safe updates)
```

- **During project work, governance runs INSIDE the project**: everything is
  local, autonomous, and fail-open. The kit is used only to install or update
  that snapshot; no server is required.
- **The kit is the source.** Changes are made here; an installed project receives a snapshot.
- **Process state is not duplicated authority.** `core/docs/process/` contains
  source templates in this kit; installation seeds `<project>/docs/process/`,
  whose files then become project-owned state and are never overwritten by an
  update.
- **Updates**: new installations record `gtovar/governance-kit` as their release source and check it advisory at re-entry. When an update exists, the agent asks once before applying safe files. A fork or private distribution overrides the source with `--github-repo OWNER/REPO`. Existing snapshots without a configured source can be configured by their installed update checker after explicit approval; snapshots without that checker require one bootstrap update.

### Publishing an update

The `VERSION` file is the release version. Publish only immutable SemVer tags
that match it, then create the GitHub Release with notes that explain behavior,
migration work, and compatibility impact:

```bash
git tag v0.1.0
git push origin v0.1.0
gh release create v0.1.0 --generate-notes
```

New installations record the source with
`gtovar/governance-kit` by default; `--github-repo OWNER/REPO` overrides it.
Existing installations with the update checker can configure their source from
inside the consumer repository; snapshots without it need one bootstrap update.
- **Post-update audit**: the trusted kit copy of `governance-audit.py` reports
  missing canonical entry files, exact unresolved template markers, missing
  README navigation references, non-actionable frontiers, duplicate frontier
  owners, and untracked canonical entry files. Warnings remain non-blocking;
  the updater stays fail-open and semantic consistency stays with agent review.
- **Vehicles**: every rule declares how it fires — auto-load (constitution), router (if-I-touch-X matrix), skill (per task), hook/script (deterministic), subagent (audit). What has no vehicle is pure reference and is not meant to be enforced.

### Release readiness

When an approved checkpoint changes a source file that `scripts/update.py`
installs into consumer repositories, activate `release-readiness` before the
release commit. Determine the SemVer version, update `VERSION`, include the
consumer migration notes, and validate the kit. A tag, push, and GitHub Release
remain separate human-authorized actions. Kit-internal-only changes do not
create a release requirement.

## Structure

```text
core/                  what gets installed per project (constitution + process templates)
skills/                standard SKILL.md skills (work in opencode, Claude Code, Codex)
adapters/opencode/     reviewer agent for opencode
adapters/claude/       thin CLAUDE.md adapter + session hooks
adapters/codex/        reviewer agent for Codex
hooks/                 git hooks (advisory by default)
profiles/              phase profiles (implementation, production)
scripts/               deterministic checks + kit-internal tools (update, skills-lock)
tests/                 installer, updater, and governance-audit integration tests
bin/install.sh         idempotent installer (+ update subcommand)
```

## Daily use

- **Before closing a session**: run a `reviewer` pass (read-only subagent). Reports BLOCKER / WARNING / ADVISORY with evidence.
- **Hard decisions**: invoke the `decision-expander` skill.
- **Canonical documentation changes**: `documentation-governance` skill (one owner per topic, DDR for non-trivial decisions).
- **Session start/close**: `governance-gatekeeper` routes intents and applies the rituals in `docs/session_rituals.md`.
- **Experimental phase/gate reconciliation**: re-entry runs the mechanical
  governance audit automatically. The gatekeeper reports warnings, routes
  blockers into reconciliation, requests one bounded authorization for
  compatible mechanical batches, and isolates independent judgment findings
  into one decision frontier at a time.
- **Hooks**: enable enforce mode with `GOVERNANCE_ENFORCE=1` when the project decides explicitly.

To request reconciliation without starting a new session, use the optional
manual trigger:

```text
Reconcile governance findings.
```

## Roadmap

**DONE (v1)**: universal layer + opencode + installer + full harvest (constitution, docs with declared vehicles, 15 templates, 5 skills, reviewer, hooks, doc-health, comment-hygiene, precedence, operating policy, portable distribution).

**DONE (S2)**: `governance-gatekeeper` skill (executable intent router, 8 modes, interruption format), `session_rituals.md` (start/close rituals, mini-block, "revisa lógica", truth hierarchy), `learning_capture.md` + script, `TESTING_STRATEGY.md`.

**DONE (S3)**: `instruction-registry.json` + schema (14 typed rules with severity and vehicle) + deterministic validator `check-registry.py`; adversarial verification `verify_votes.py` (3-voter panel, ≥2/3 quorum, "the model never self-declares verified"); PII hygiene + "5 dimensions of repo health" lens in the reviewer (check #12).

**DONE (S4)**: phase profiles in the installer (`--profile foundation|implementation|production` — deterministic pre-commit with detect-secrets, CodeQL/governance/dependabot workflows) + Claude Code adapter (`CLAUDE.md` thin adapter + advisory session hooks), Codex adapter (`reviewer.md`), and repo-local Codex skill discovery through `.agents/skills/`.

**DONE (v5)**: `install.sh update <project>` — safe update via `.governance-kit/manifest.json`; `skills-lock.json` (SHA-256 per skill file) + `check-skills-lock.py` (drift and integrity verification). Both stdlib-only, fixture-tested.

**DONE (commit boundary)**: proactive `commit-readiness` interrupts scope
expansion only after strong logical-slice signals. The gatekeeper inspects Git
state read-only, proposes checkpoint, separation, or handoff, and requires
explicit human authorization for every Git state change.

**DONE (local branch lifecycle hygiene)**: an explicit, read-only Git hygiene
procedure reports safe local cleanup candidates after integration. The
gatekeeper invokes the review only during post-merge review or close-session,
and every ref deletion still requires a separate human instruction.

**READY (v0.2.0 release)**: release readiness, default official-source
discovery for new installations, and agent-guided source and integration-target
configuration are prepared. Publishing `v0.2.0` remains a separate authorized
action.

**EXPERIMENTAL (release discovery)**: installed projects check their configured
GitHub Releases source advisory at re-entry, preview a released snapshot, and
apply only safe files after explicit approval. New installations use the
official source by default; legacy snapshots retain a one-time bootstrap limit.

**EXPERIMENTAL (governed reconciliation)**: `governance-gatekeeper` composes the
read-only reviewer and documentation routing into an audit → classification →
single authorization → mechanical batches → validation loop. The advisory
`governance-audit.py` supplies only mechanically verifiable findings. Pulso
field use exposed a recursive frontier ("review the remaining findings") that
had no canonical inventory or closure condition. The kit now requires one
action, exact target, and observable done condition; warnings cannot become
phase work implicitly. The flow remains experimental until this convergence
contract is validated after rollout in a fresh project session.

**DISCARDED (recorded decision)**: optional state MCP — the kit works serverless and fail-open; a server would add operational dependency against portability.

## Recorded decisions

- **Reconciliation ownership:** extend `governance-gatekeeper` instead of adding
  another skill. `governance-reviewer` audits, `documentation-governance` routes
  owner documents, and the gatekeeper executes only authorized remediation.
- **Convergence before completeness (DDR):** re-entry and reconciliation stop
  after one evidence pass. An undefined findings collection is one state defect,
  not authorization to manufacture an exhaustive inventory. Warnings and
  non-blocking debt do not delay a gate decision.
- **Commit-boundary ownership:** use the constitution and gatekeeper instead of
  a state MCP or Git watcher. This preserves portability and fail-open behavior;
  the human retains authority over every Git state change.
- **Local branch lifecycle ownership:** extend Git hygiene and the existing
  close-session route rather than adding a watcher, script, or new skill. The
  review is read-only and advisory; the human retains deletion authority.
- **Release readiness ownership:** extend `governance-gatekeeper` and the
  source README instead of publishing every commit or adding a release watcher.
  Only approved changes to installed artifacts become release candidates.
- **Update ownership:** GitHub Releases are the authoritative update source.
  Checks are read-only and fail-open; applying a release uses file hashes to
  update unchanged files and report customized files for review.

## Open decisions

- **Legacy global skill migration:** `install.sh global` remains fail-safe and
  does not overwrite an existing user-level skill. Decide whether a future
  explicit migration command should replace or archive stale global copies;
  project-local `.agents/skills/` plus post-update reconciliation is the current
  mitigation.
- **Plugin packaging:** direct repo-local skills are sufficient for the current
  portable snapshot model. Revisit a Codex plugin only when distribution
  outside checked-in project snapshots has a concrete consumer.
- **Structured state format:** reconciliation currently combines deterministic
  invariant checks with agent judgment over Markdown owner documents. Consider
  machine-readable phase metadata only after field evidence shows recurring
  ambiguity that the current protocol cannot resolve reliably.
- **Agent compatibility evidence:** define what evidence justifies the workflow's
  broad "any new agent" Gate F0 wording before narrowing or claiming it. The
  observed Pulso handoff covers Codex only and does not settle that policy.
- **v0.2.0 publication:** verify the current GitHub Release state, then obtain
  authorization to tag, push, and publish `v0.2.0` with the documented legacy
  bootstrap limit.

## v0.2.0 Release Notes

- Adds advisory local branch lifecycle hygiene after successful integration.
- New installations discover releases from `gtovar/governance-kit` without
  requiring a user-supplied source argument.
- Agents can configure a missing consumer release source or integration target
  after a single explicit user answer.
- A consumer snapshot without the installed update checker cannot discover this
  release by itself and requires one bootstrap update.

## Origin

Content harvested from the user's projects: email-cleaner (constitution, capabilities, useful-comments, intent_map/flows), ai-governance (R1-R9, fail-open, onboarding), rrhh (quality matrix, doc-health), cfdi_suite (security CI, determinism), claude-obsidian (skills, session hooks), Pulso (F0-F11 workflow, G0-G3 gates, templates). Foundational research: "IA Gobernanza Cognitiva y Cumplimiento de Reglas" (Pulso).
