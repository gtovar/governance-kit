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
| Deterministic checks | `scripts/` (governance-audit, doc-health, log-hygiene, comment-hygiene, learning-capture, check-registry, verify-votes) | per project |
| Skills | `decision-expander`, `governance-gatekeeper`, `governance-reviewer`, `useful-comments-reviewer`, `documentation-governance` | vendored to `.opencode/skills/` and `.agents/skills/` per project always; to `.claude/skills/` per project with `--adapter claude\|all` (Claude Code does not read `.agents/skills/`); optional: global per machine (`install.sh global` now also seeds `~/.claude/skills/`) |
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

- **If the project is worked with Claude Code, always pass `--adapter claude`
  (or `--adapter all`).** Claude Code reads `AGENTS.md` on its own either way,
  but without the adapter's `.claude/settings.json` there is no
  `SessionStart`/`Stop` hook — the advisory kit-update check and the
  doc-health-on-close check then depend entirely on the agent remembering to
  run the `session_rituals.md` steps by itself every session, which drifts
  silently over a long-running project.

- **Portability**: the default mode vendors the same skills to `.opencode/skills/` and Codex's repo-local `.agents/skills/` path → everything travels with the project repo, zero machine-state dependency. `global` is an optional per-machine shortcut, not a requirement.
- **Idempotent**: never overwrites a project's existing files.
- Codex and OpenCode discover project skills from their native paths. Restart the agent if newly installed skills do not appear.
- For Codex startup notices, use `--adapter codex` (or `all`). This installs
  `.codex/hooks.json` and `.codex/hooks/governance-update.py`. Review and trust
  the hook in Codex before it runs (CLI: `/hooks`); project configuration must
  also be trusted and hooks enabled. On startup/resume, the hook calls the
  installed checker and surfaces its result through `systemMessage`: a newer
  published release, no newer publication, or an unavailable/unconfigured check.
  It never applies an update. Existing hook configurations are preserved and
  require an explicit merge with `adapters/codex/hooks.json` when they differ.
  The command requires Git and Python 3 and resolves the project from the Git
  root, including when Codex starts in a subdirectory. See the
  [Codex hook contract](https://learn.chatgpt.com/docs/hooks).
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
  README navigation references, non-actionable or circular frontiers, duplicate frontier
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

**DONE (v0.6.0 — visible Codex update checks and safe archive retirement)**:
the opt-in Codex adapter
now connects the installed release checker to `SessionStart` and emits a UI
warning from the real result. Tests cover version comparisons, failed checks,
command execution from paths with spaces, safe reinstall, and opt-in updates.
Adding an adapter preserves the previous recorded installed version; an
additive reinstall is not an upgrade. Hook trust and an observed notice in
the user's Codex interface remain the activation acceptance step. The release
was published on 2026-10-16; no roadmap phase was advanced.
The same release adds a verified local-bundle procedure for retiring an
explicitly named, non-integrated local branch without discarding its recoverable
history. It does not permit publishing sensitive archive contents.
The adapter was installed additively in Pulso on 2026-10-15: existing managed
file contents and recorded version `0.1.1` were preserved. Its installed hook
queried GitHub and emitted `0.1.1 -> v0.3.0`. The first live run exposed a
project-root resolution error; the corrected installed-entrypoint regression
requires a successful release notice, not merely a generic failure message.

**PREPARED (v0.6.3 — definition of done in the close ritual)**:
`docs/session_rituals.md` adds a whole-system definition of done to the close
ritual (step 9): eight checks that each map to a failure seen in a consumer
repository, plus three working rules (one pull request per slice that carries
its own state documents, one pull request awaiting integration per repository by
default, and a repeated defect class means fixing the root cause). The release is
not published.

**PUBLISHED (v0.6.2 — doc-health.sh ignore handling and scan failures)**:
`.doc-health-ignore` entries with spaces are no longer split into several `find`
arguments, repository-relative entries now match in the kit's source layout, and
a failed scan exits 2 instead of reporting a clean run. `tests/test_doc_health.py`
covers each case. Found by the Codex review of the Pulso consumer repository
(gtovar/Pulso#5).

**PUBLISHED (v0.6.1 — preserve local safety guards when retiring a branch)**:
the archive retirement procedure now requires checking whether local hooks or
scripts rely on the branch ref and preserving/testing those protections before
the ref is removed.

**DONE (v1)**: universal layer + opencode + installer + full harvest (constitution, docs with declared vehicles, 15 templates, 5 skills, reviewer, hooks, doc-health, comment-hygiene, precedence, operating policy, portable distribution).

**DONE (S2)**: `governance-gatekeeper` skill (executable intent router, 8 modes, interruption format), `session_rituals.md` (start/close rituals, mini-block, "revisa lógica", truth hierarchy), `learning_capture.md` + script, `TESTING_STRATEGY.md`.

**DONE (2026-10-08 — testing evidence guidance)**: extended the existing
`core/docs/TESTING_STRATEGY.md` with risk-relevant evidence questions
(independence, behavioral fidelity, oracle strength, and defect sensitivity),
regression-test evaluation at the lowest suitable level, a documented
exception path, and limits on claims from passing runs. The questions guide
judgment; they do not mandate four tests or a testing tool. The change is
grounded in the Matina testing case and keeps the existing strategy as owner;
no new process, skill, agent, or infrastructure was added.

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

**DONE (circular frontier guard)**: the `CURRENT_STAGE.md` template and
workflow distinguish process references from executable frontiers. The advisory
governance audit blocks the mechanically verifiable cycle where a Next action
only consults `PROJECT_MAP.md` while that map declares `CURRENT_STAGE.md`
authoritative.

**DONE (v0.4.0 — field feedback from a multi-day real install)**: reviewed a
production consumer repository (foundation-profile install, several days of
real sessions) for what the kit's own rituals actually produced versus what
sat unused, and fixed what the evidence supported:
- Backported the "Completion and decision protocol" (`AGENTS.md`) and its
  "Completion and decision loop" (`session_rituals.md`) — both were
  independently hand-patched into the consumer repo and never flowed back.
- Added `docs/templates/pending_work_template.md`, generalizing a
  locally-invented deferred-work ledger the kit had no template for.
- `scripts/doc-health.sh` now reads an optional repo-root
  `.doc-health-ignore` file instead of requiring a hand-patched script copy
  per project to exclude generated-doc paths.
- Routed `docs/instruction-registry.json` changes to `check-registry.py` in
  the constitution's activity matrix — previously reachable only through the
  production-profile CI workflow, so a foundation/implementation install
  never validated it.
- Gave `verify_votes.py` a real caller: an "Adversarial verification"
  procedure in the reviewer skill/agents (`findings.json`/`votes.json` →
  panel verdict) for disputed or release-blocking BLOCKER findings —
  previously shipped with zero producer anywhere in the kit.
- Tied the `learning_capture.md` trigger to the close ritual's mandatory
  "what was learned" bullet instead of leaving it to spontaneous mid-session
  judgment, which measurably never fired in the reviewed repo.
- `bin/install.sh` and the README now flag explicitly when `--adapter claude`
  is skipped: without it, Claude Code has no `SessionStart`/`Stop` hooks, so
  the advisory kit-update check and doc-health-on-close depend entirely on
  the agent remembering the ritual by itself — the reviewed repo had silently
  run three minor versions behind for exactly this reason.
**DONE (v0.5.0 — accumulation-without-pruning fix, decision-expander-gated)**:
matina's real data showed the kit's canonical logs grow without bound —
`Sprint_Log.md` reached 1.2MB/21k lines in ~1 week (76% of commits touch it),
`PROJECT_STATE.md` reached 112KB despite being defined as a rewritten
snapshot. Investigated through a full decision-expander expansion + two
evaluated plan iterations (see the session record) before implementing, since
the first-draft fix (cap individual Sprint_Log entries at ~20 lines) was
directly contradicted by real data: median entry is 50 lines, and
`PENDING_WORK.md` actively points *into* Sprint_Log.md for full technical
detail — Sprint_Log is the canonical record by design, not a pointer-only
ledger, so shrinking entries would have fought a working information
architecture. Shipped instead:
- `scripts/log-hygiene.sh check` — advisory size thresholds for
  `PROJECT_STATE.md`/`README_REENTRY.md` (400/300 lines — these should be
  rewritten as compact snapshots, not accumulated), `docs/PENDING_WORK.md`
  (300 lines), `Sprint_Log.md` (1500 lines/100KB), `LEARNING_CAPTURE_INBOX.md`
  (20 entries). No per-entry length check.
- `scripts/log-hygiene.sh archive <file> [--keep N]` — moves all but the last
  N dated (`## `/`### YYYY-MM-DD`) entries of `Sprint_Log.md` or
  `LEARNING_CAPTURE_INBOX.md` to `<stem>_ARCHIVE.<ext>`, write-before-truncate,
  leaves a one-line pointer, reminds to index the archive file if new.
  Verified byte-for-byte lossless against a real 1.2MB production
  `Sprint_Log.md` copy, including a `--keep 0` edge case that was found broken
  (corrupted `sed` ranges) during that same real-data test and fixed before
  shipping. `docs/PENDING_WORK.md` gets a manual archival rule instead (its
  entries are grouped by area, not date — not safe to automate).
- Documented, not automated, an inherent limit: archiving can orphan a prose
  cross-reference from `PENDING_WORK.md`/`CURRENT_STAGE.md` into the archived
  range (`doc-health.sh` only catches broken markdown links, not prose).
  `archive` prints a mandatory pre-check reminder instead of pretending to
  detect this reliably.
- Wired into `adapters/claude/settings.json`'s `Stop` hook alongside
  `doc-health.sh`, and into the close ritual (advisory, not blocking) —
  otherwise this would repeat the exact "shipped but never triggered" pattern
  found in `verify_votes.py`/`check-registry.py`/`.claude/skills` earlier in
  the same review.
- `sprint_log_template.md` reframed: Sprint_Log is the canonical detail
  store, size is controlled by archiving old entries, not by writing thinner
  ones. 42 tests total (15 new for `log-hygiene.sh`, covering real and
  synthetic data, edge cases, and the `--keep 0` regression).

**DONE (v0.5.1 — honest fresh-install handoff, decision-expander-gated)**:
a clean installation necessarily leaves project-owned bootstrap templates
unresolved. The installer previously ended by claiming that a new agent could
already know how to work, while `governance-audit.py` correctly reported the
unresolved README and current-stage fields as blockers. The decision record
kept the templates and blocker semantics intact because the kit cannot infer a
project's purpose or frontier. Plan 1 changed only the handoff, added a
regression test, and prepared the patch release; its evaluation found no
material objection because the audit remains the independent completion check.
`bin/install.sh` now names the exact bootstrap action (`README.md` and
`docs/process/CURRENT_STAGE.md`) and its observable completion condition (the
audit has no template blockers). Existing projects need no migration:
re-running the installer remains additive and never overwrites their state.

**FIXED (v0.4.1 — found while applying v0.4.0 to the reviewed project)**:
`bin/install.sh`'s final manifest step used to unconditionally rehash every
kit-managed file against its current on-disk content, including on a re-run
that only adds an adapter or profile to an *already-installed* project. That
silently reset a customized file's tracked baseline to its own customized
content, so the next `update` treated it as unmodified since install and
overwrote it with the kit's current generic version — destroying real project
content. Observed live: re-running `install.sh <project> --adapter claude` on
an already-customized project, then `install.sh update <project>`, silently
overwrote `AGENTS.md`, `README.md`, `docs/index.md`, and
`docs/instruction-registry.json` with generic kit versions before the loss was
caught and reverted from git. `scripts/update.py`'s manifest step now only
adds entries for files it has not seen before; it never rewrites the tracked
hash of a file already in the manifest. Regression-tested
(`test_reinstall_for_an_adapter_does_not_reset_customized_file_baselines`).
**If your project ever re-ran `install.sh` with a new `--adapter`/`--profile`
flag on an existing install before this fix, treat any file `update` reports
as "safe to update" with suspicion — verify it against your own git history
before trusting it.**

**FIXED (v0.4.2 — found by asking "what else did that bug-hunting miss?")**:
`update.py`'s `collect_pairs()` never listed `.claude/skills/*`, `CLAUDE.md`,
or `.claude/settings.json` (nor the Codex reviewer agent) at all — not
"protected," just entirely absent from what the updater tracks. A project
that opted into `--adapter claude` would never receive future kit
improvements to those files through `install.sh update` or
`governance-kit-update.py apply`; they'd stay frozen at whatever the kit
shipped on the day `--adapter claude` was first run, with no report even
mentioning them as stale. Fixed by making adapter pairs conditional on the
adapter's own marker file already existing in the target (`CLAUDE.md` for
Claude, `.codex/agents/reviewer.md` for Codex) — synced automatically once
opted in, never silently created for a project that skipped the adapter.
Regression-tested (`test_update_syncs_claude_adapter_only_when_already_installed`).

- Fixed the real reason `governance-reviewer`, `governance-gatekeeper`,
  `useful-comments-reviewer`, and `documentation-governance` never fired in
  the reviewed repo: the installer only ever wrote skills to
  `.opencode/skills/` and `.agents/skills/` — never `.claude/skills/`, which
  is where Claude Code actually discovers project skills. `decision-expander`
  worked there only because that one machine happened to have it separately
  under `~/.claude/skills/` already; the other four were never discoverable
  by Claude Code at all. `--adapter claude|all` now also vendors into
  `.claude/skills/`, and `install.sh global` now seeds `~/.claude/skills/`.

**Migration limits for existing installs updating to v0.4.0:** `install.sh
update` never overwrites a file you have hand-edited (verified: it reports
`customized — kept`). If your project independently patched in something this
release now ships upstream — a "Completion and decision protocol" section in
`AGENTS.md`/`session_rituals.md`, a hardcoded `doc-health.sh` path exclusion —
`update` will report that file as customized and leave your version in place;
it will not merge the two. Diff your version against the new kit source by
hand and reconcile deliberately, especially for `doc-health.sh`, since the
kit's new mechanism (an optional `.doc-health-ignore` file) is not the same
shape as a hand-added `-path` exclusion. Existing projects without `--adapter
claude` will not retroactively get `.claude/skills/`; re-run `install.sh
<project> --adapter claude` to add it (idempotent, additive only).

**Migration limit for existing installs updating to v0.6.0:** the safe updater
replaces `docs/git_hygiene.md` only when its installed contents still match the
recorded kit baseline. Customized copies are kept and must be reconciled with
the new non-integrated-branch retirement procedure manually. Project-owned
`docs/process/` state remains protected from kit updates.

**DONE (v0.3.0 release)**: circular-frontier guard, release readiness, default official-source
discovery for new installations, and agent-guided source and integration-target
configuration were published as `v0.3.0` on 2026-09-03.

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

- **Codex update notice ownership (DDR):** extend the existing Codex adapter;
  its hook delegates to the installed checker instead of adding a second
  release client or an MCP server. README owns setup and migration guidance
  (G0: implementation/tests; G1: existing owner; G2: no split; G3: no new doc).
  The visible notice reflects a check against the recorded installation
  version, not a full integrity audit. An unavailable check never means current.

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
- **Circular-frontier ownership:** extend the current-state template, workflow,
  and advisory governance audit rather than introduce another process document
  or agent. The detector is limited to an observable mutual-reference pattern;
  agents retain judgment for all other frontier quality.
- **Release readiness ownership:** extend `governance-gatekeeper` and the
  source README instead of publishing every commit or adding a release watcher.
  Only approved changes to installed artifacts become release candidates.
- **Update ownership:** GitHub Releases are the authoritative update source.
  Checks are read-only and fail-open; applying a release uses file hashes to
  update unchanged files and report customized files for review.

## Open decisions

- **Codex notice activation:** review/trust the installed hook and observe a
  fresh startup/resume notice in Codex. Script/contract tests alone do not
  establish rendering in the user's desktop interface.

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
- **v0.6.3 publication:** merge the reviewed branch, then tag `v0.6.3` and create
  the GitHub Release. The release is not published yet.

## v0.6.3 Release Notes

- `docs/session_rituals.md` gains step 9 of the close ritual and a "Definition of
  done (whole-system check)" section: eight checks (shipped equals said, right CI,
  review of the final commit, a repository-wide sweep before pushing, verified
  replies, reporting what was left open, saying where things stand, saying what was
  not verified) and three working rules.
- No script, hook or installed behavior changes.
- Migration: none for project-owned files. The updated ritual reaches consumer
  repositories through the safe update; a consumer that customized
  `docs/session_rituals.md` keeps its version and must merge the new section by hand.

## v0.6.2 Release Notes

- `scripts/doc-health.sh`: a `.doc-health-ignore` entry containing spaces stays
  one path. Before, it was split into several `find` arguments, `find` failed,
  and the script reported "limpio" with exit 0 while skipping every check.
- Repository-root-relative entries now match when the script scans the kit's
  `core/` source layout.
- Compatibility: when the documentation tree cannot be scanned, the script now
  exits 2 (documented next to the existing 0 = clean and 1 = findings). A caller
  that treats any non-zero status as a failed check keeps working.
- Migration: none for project-owned files. The updated script reaches consumer
  repositories through the safe update; a consumer that edited its copy locally
  keeps its version and must merge the change by hand.

## v0.6.1 Release Notes

- The non-integrated branch retirement procedure now requires checking local
  hooks and scripts that depend on the ref, and preserving/testing those guards
  before branch removal.
- Existing customized `docs/git_hygiene.md` files remain protected by safe
  update and require a manual merge of the added guard-dependency guidance.
- No new hook, script, or process is installed by this documentation update.

## v0.6.0 Release Notes

- Git hygiene now documents how to retire an owner-named, non-integrated local
  branch after its history is verified in a private local bundle. It does not
  authorize remote deletion or publication of archived sensitive material.
- Opt-in Codex startup/resume hooks surface the installed checker's result as
  a visible advisory warning. No update is applied automatically.
- Migration: run `bin/install.sh <project> --adapter codex`, review/trust the
  hook, and start or resume a session. Existing Codex adapters receive the new
  files through safe update; existing custom hook configurations need a manual
  merge. Hook trust is required after changes to the hook definition.
- Additive reinstalls retain the recorded installed version and file baselines;
  legacy manifests without a version retain an unknown `0.0.0` baseline.
- Requires a Codex version supporting `SessionStart` and `systemMessage`, a
  trusted project configuration, Git, Python 3, and the installed checker.
  Local Codex CLI `0.162.1` exposes hooks enabled; desktop rendering acceptance
  remains pending user hook trust and a fresh session.
- Existing customized `docs/git_hygiene.md` files are retained by safe update;
  reconcile the new local-bundle retirement guidance manually. Project-owned
  process state is not overwritten.

## v0.5.1 Release Notes

- Fresh installs now state that they contain bootstrap templates and identify
  the required personalization and audit criterion before governed work begins.
- No project-owned file is changed by an update; existing installations require
  no migration.

## v0.3.0 Release Notes

- Adds an advisory governance-audit blocker for a mechanically verifiable
  circular frontier: a Next action only consults `PROJECT_MAP.md` while that
  map declares `CURRENT_STAGE.md` authoritative.
- New installations receive template and workflow guidance that process
  references are context, not an executable frontier.
- Existing installations receive the audit update only when their managed
  `scripts/governance-audit.py` remains uncustomized; project-owned process
  state files remain protected and are not overwritten.

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
