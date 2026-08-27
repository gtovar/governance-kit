#!/usr/bin/env bash
# governance-kit installer
# Usage:
#   install.sh <project-dir> [options]
#     --with-hooks                 advisory commit-msg hook
#     --profile <name>             foundation (default) | implementation | production
#     --adapter <name>             claude | codex | all
#     --github-repo OWNER/REPO     GitHub Releases source for future update checks
#   install.sh global              Optional: install skills per-machine (OpenCode and Codex).
#   install.sh update <project-dir>  Apply kit changes safely (uses manifest).
#   install.sh configure-update <project-dir> --github-repo OWNER/REPO
# Design rules:
#   - idempotent: running twice changes nothing
#   - fail-safe: never overwrites existing files; reports what it did
#   - portable: default install vendors skills into the project; no machine config required
#   - advisory-first: hooks are advisory unless GOVERNANCE_ENFORCE=1

set -euo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS=0
PROFILE=""
ADAPTER=""
GITHUB_REPO=""

usage() {
  sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
  exit 1
}

log()  { printf '[kit] %s\n' "$*"; }
skip() { printf '[kit] skip (exists): %s\n' "$*"; }
add()  { printf '[kit] add: %s\n' "$*"; }

install_skills_into() {
  local skill_dest="$1"
  mkdir -p "$skill_dest"

  for skill_dir in "$KIT_DIR"/skills/*/; do
    [ -d "$skill_dir" ] || continue
    local skill_name
    skill_name="$(basename "$skill_dir")"
    if [ -e "$skill_dest/$skill_name" ]; then
      skip "$skill_dest/$skill_name"
    else
      cp -R "$skill_dir" "$skill_dest/$skill_name"
      add "$skill_dest/$skill_name"
    fi
  done
}

run_governance_audit() {
  local target="${1%/}"
  # Execute the trusted kit copy; project scripts may be customized.
  local audit="$KIT_DIR/scripts/governance-audit.py"
  [ -f "$audit" ] || return 0

  log "advisory governance audit: $target"
  local audit_status=0
  python3 "$audit" --root "$target" || audit_status=$?
  if [ "$audit_status" -eq 0 ]; then
    return 0
  fi
  if [ "$audit_status" -eq 1 ]; then
    log "note: reported blockers require reconciliation; update remains fail-open."
    log "next: resolve only the blocker coordinates above; warnings stay non-blocking and do not authorize a broader review."
  else
    log "warning: governance audit could not run reliably; update remains fail-open."
  fi
}

# ---------------------------------------------------------------- global

cmd_global() {
  install_skills_into "$HOME/.config/opencode/skills"
  install_skills_into "$HOME/.agents/skills"
  log "done. Restart the agent if newly installed skills do not appear."
}

# ---------------------------------------------------------------- project

cmd_project() {
  local target="${1%/}"
  if [ -d "$target" ]; then
    log "project exists: $target"
  else
    mkdir -p "$target"
    log "created project dir: $target"
  fi

  # Constitution
  if [ -e "$target/AGENTS.md" ]; then
    skip "$target/AGENTS.md"
  else
    cp "$KIT_DIR/core/AGENTS.md" "$target/AGENTS.md"
    add "$target/AGENTS.md"
  fi

  # Process docs (templates; never overwrite project-owned state)
  local process_dest="$target/docs/process"
  mkdir -p "$process_dest"
  for doc in DEVELOPMENT_WORKFLOW.md PROJECT_MAP.md CURRENT_STAGE.md; do
    if [ -e "$process_dest/$doc" ]; then
      skip "$process_dest/$doc"
    else
      cp "$KIT_DIR/core/docs/process/$doc" "$process_dest/$doc"
      add "$process_dest/$doc"
    fi
  done

  # Entry point (never overwrite)
  if [ -e "$target/README.md" ]; then
    skip "$target/README.md"
  else
    cp "$KIT_DIR/core/README.md" "$target/README.md"
    add "$target/README.md"
  fi

  # Session state files (never overwrite) — required by the close-session ritual
  for state_file in PROJECT_STATE.md README_REENTRY.md Sprint_Log.md; do
    if [ -e "$target/$state_file" ]; then
      skip "$target/$state_file"
    else
      cp "$KIT_DIR/core/$state_file" "$target/$state_file"
      add "$target/$state_file"
    fi
  done

  # Documentation governance policies (never overwrite)
  local docs_dest="$target/docs"
  mkdir -p "$docs_dest"
  for doc in index.md ADR_POLICY.md documentation_rules.md git_hygiene.md good_practices.md session_rituals.md TESTING_STRATEGY.md learning_capture.md instruction-registry.json instruction-registry.schema.json; do
    if [ -e "$docs_dest/$doc" ]; then
      skip "$docs_dest/$doc"
    else
      cp "$KIT_DIR/core/docs/$doc" "$docs_dest/$doc"
      add "$docs_dest/$doc"
    fi
  done

  # Templates with fixed structure (never overwrite)
  local tpl_dest="$target/docs/templates"
  mkdir -p "$tpl_dest"
  for tpl in HU_template.md cerrar_historia.md empezar_historia.md project_state_fill_guide.md readme_reentry_template.md readme.guia.md sprint_log_template.md pull_request_template.md issue_feature.md issue_bug_spike.md design_document_template.md api_reference_template.md quickstart_template.md seeders.guia.md project_state_frontend_template.md; do
    if [ -e "$tpl_dest/$tpl" ]; then
      skip "$tpl_dest/$tpl"
    else
      cp "$KIT_DIR/core/templates/$tpl" "$tpl_dest/$tpl"
      add "$tpl_dest/$tpl"
    fi
  done

  # Deterministic doc-health checker
  local script_dest="$target/scripts"
  if [ -e "$script_dest/doc-health.sh" ]; then
    skip "$script_dest/doc-health.sh"
  else
    mkdir -p "$script_dest"
    cp "$KIT_DIR/scripts/doc-health.sh" "$script_dest/doc-health.sh"
    chmod +x "$script_dest/doc-health.sh"
    add "$script_dest/doc-health.sh"
  fi

  # Deterministic comment-hygiene checker
  if [ -e "$script_dest/comment-hygiene.sh" ]; then
    skip "$script_dest/comment-hygiene.sh"
  else
    mkdir -p "$script_dest"
    cp "$KIT_DIR/scripts/comment-hygiene.sh" "$script_dest/comment-hygiene.sh"
    chmod +x "$script_dest/comment-hygiene.sh"
    add "$script_dest/comment-hygiene.sh"
  fi

  # Deterministic learning-capture helper
  if [ -e "$script_dest/learning-capture.sh" ]; then
    skip "$script_dest/learning-capture.sh"
  else
    mkdir -p "$script_dest"
    cp "$KIT_DIR/scripts/learning-capture.sh" "$script_dest/learning-capture.sh"
    chmod +x "$script_dest/learning-capture.sh"
    add "$script_dest/learning-capture.sh"
  fi

  # Deterministic governance checks and adversarial verification
  for py in governance-audit.py check-registry.py verify_votes.py governance-kit-update.py; do
    if [ -e "$script_dest/$py" ]; then
      skip "$script_dest/$py"
    else
      mkdir -p "$script_dest"
      cp "$KIT_DIR/scripts/$py" "$script_dest/$py"
      if [ "$py" = "governance-audit.py" ]; then
        chmod +x "$script_dest/$py"
      fi
      add "$script_dest/$py"
    fi
  done

  # Reviewer agent (opencode adapter)
  local agent_dest="$target/.opencode/agent"
  if [ -e "$agent_dest/reviewer.md" ]; then
    skip "$agent_dest/reviewer.md"
  else
    mkdir -p "$agent_dest"
    cp "$KIT_DIR/adapters/opencode/agent/reviewer.md" "$agent_dest/reviewer.md"
    add "$agent_dest/reviewer.md"
  fi

  # Project-local skills travel with the repository. Each agent reads its native
  # discovery path; both copies are managed from the same skills/ source.
  install_skills_into "$target/.opencode/skills"
  install_skills_into "$target/.agents/skills"
  log "note: skills vendored for OpenCode and Codex (portable). Optional per-machine global install: $0 global"

  # Optional git hooks
  if [ "$HOOKS" = "1" ]; then
    if [ -d "$target/.git" ]; then
      local hook_dest="$target/.git/hooks/commit-msg"
      if [ -e "$hook_dest" ]; then
        skip "$hook_dest"
      else
        cp "$KIT_DIR/hooks/commit-msg.sh" "$hook_dest"
        chmod +x "$hook_dest"
        add "$hook_dest (advisory; GOVERNANCE_ENFORCE=1 to block)"
      fi
    else
      log "note: '$target' is not a git repository yet; skipping hooks."
    fi
  fi

  # Phase profiles (stack: production includes implementation)
  if [ "$PROFILE" = "implementation" ] || [ "$PROFILE" = "production" ]; then
    for impl_file in .pre-commit-config.yaml .secrets.baseline; do
      if [ -e "$target/$impl_file" ]; then
        skip "$target/$impl_file"
      else
        cp "$KIT_DIR/profiles/implementation/$impl_file" "$target/$impl_file"
        add "$target/$impl_file"
      fi
    done
    log "note: run 'pre-commit install' inside '$target' to activate the hooks."
  fi

  if [ "$PROFILE" = "production" ]; then
    local gh_dest="$target/.github"
    mkdir -p "$gh_dest/workflows"
    for wf in codeql.yml governance.yml; do
      if [ -e "$gh_dest/workflows/$wf" ]; then
        skip "$gh_dest/workflows/$wf"
      else
        cp "$KIT_DIR/profiles/production/.github/workflows/$wf" "$gh_dest/workflows/$wf"
        add "$gh_dest/workflows/$wf"
      fi
    done
    if [ -e "$gh_dest/dependabot.yml" ]; then
      skip "$gh_dest/dependabot.yml"
    else
      cp "$KIT_DIR/profiles/production/.github/dependabot.yml" "$gh_dest/dependabot.yml"
      add "$gh_dest/dependabot.yml"
    fi
    log "note: enable branch protection on main with required status checks for public repos."
  fi

  # Agent adapters (point to the canon, never duplicate truth)
  if [ "$ADAPTER" = "claude" ] || [ "$ADAPTER" = "all" ]; then
    if [ -e "$target/CLAUDE.md" ]; then
      skip "$target/CLAUDE.md"
    else
      cp "$KIT_DIR/adapters/claude/CLAUDE.md" "$target/CLAUDE.md"
      add "$target/CLAUDE.md"
    fi
    local claude_dest="$target/.claude"
    if [ -e "$claude_dest/settings.json" ]; then
      skip "$claude_dest/settings.json"
    else
      mkdir -p "$claude_dest"
      cp "$KIT_DIR/adapters/claude/settings.json" "$claude_dest/settings.json"
      add "$claude_dest/settings.json"
    fi
  fi

  if [ "$ADAPTER" = "codex" ] || [ "$ADAPTER" = "all" ]; then
    local codex_dest="$target/.codex/agents"
    if [ -e "$codex_dest/reviewer.md" ]; then
      skip "$codex_dest/reviewer.md"
    else
      mkdir -p "$codex_dest"
      cp "$KIT_DIR/adapters/codex/agents/reviewer.md" "$codex_dest/reviewer.md"
      add "$codex_dest/reviewer.md"
    fi
  fi

  log "done. A new agent should now enter '$target', read AGENTS.md and docs/process/, and know how to work."

  # Record installation manifest (enables safe updates)
  manifest_args=(manifest "$KIT_DIR" "$target")
  if [ -n "$GITHUB_REPO" ]; then
    manifest_args+=(--github-repo "$GITHUB_REPO")
  fi
  python3 "$KIT_DIR/scripts/update.py" "${manifest_args[@]}" || log "warning: manifest generation failed — update command will not be available"
}

# ---------------------------------------------------------------- main

[ "$#" -ge 1 ] || usage

case "$1" in
  global)
    cmd_global
    ;;
  update)
    shift
    [ "$#" -ge 1 ] || usage
    update_status=0
    python3 "$KIT_DIR/scripts/update.py" update "$KIT_DIR" "$1" || update_status=$?
    run_governance_audit "$1"
    exit "$update_status"
    ;;
  configure-update)
    shift
    [ "$#" -ge 3 ] || usage
    target_arg="$1"
    shift
    if [ "$1" != "--github-repo" ] || [ "$#" -ne 2 ]; then
      usage
    fi
    python3 "$KIT_DIR/scripts/update.py" configure "$KIT_DIR" "$target_arg" "$2"
    ;;
  --help|-h)
    usage
    ;;
  *)
    target_arg="$1"
    shift
    while [ "$#" -gt 0 ]; do
      case "$1" in
        --with-hooks) HOOKS=1; shift ;;
        --profile) PROFILE="$2"; shift 2 ;;
        --profile=*) PROFILE="${1#*=}"; shift ;;
        --adapter) ADAPTER="$2"; shift 2 ;;
        --adapter=*) ADAPTER="${1#*=}"; shift ;;
        --github-repo) GITHUB_REPO="$2"; shift 2 ;;
        --github-repo=*) GITHUB_REPO="${1#*=}"; shift ;;
        *) echo "[kit] error: unknown option '$1'" >&2; exit 1 ;;
      esac
    done
    case "$PROFILE" in
      ""|foundation|implementation|production) ;;
      *) echo "[kit] error: unknown profile '$PROFILE' (foundation|implementation|production)" >&2; exit 1 ;;
    esac
    case "$ADAPTER" in
      ""|claude|codex|all) ;;
      *) echo "[kit] error: unknown adapter '$ADAPTER' (claude|codex|all)" >&2; exit 1 ;;
    esac
    cmd_project "$target_arg"
    ;;
esac
