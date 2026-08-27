# Profiles (governance-kit)

Each profile installs the governance layer that matches the project's PHASE. The rule: do not install enforcement the phase does not need yet (anti-over-architecture).

```text
foundation      (default) — constitution, docs, templates, skills, reviewer, scripts.
                For F0-F2 projects (no code, or in discovery).
implementation  + deterministic pre-commit (detect-secrets, format, hygiene).
                For F8-F9+ projects (real code).
production      + GitHub security workflows (CodeQL, Dependabot, audit).
                For projects with deploys or a public repo.
```

Profiles stack: `--profile production` includes the implementation layer.

## Adapters

```text
--adapter claude   CLAUDE.md (thin adapter → AGENTS.md) + .claude/settings.json (advisory session hooks)
--adapter codex    .codex/agents/reviewer.md (reviewer subagent in Codex format)
--adapter all      both
```

Rule: adapters point to the canon (`AGENTS.md`, `docs/process/`); they never duplicate the truth.
