#!/usr/bin/env bash
# governance-kit commit-msg hook — advisory by default, fail-open by design.
# Verifies the commit message follows Conventional Commits: type(scope): subject
# Modes:
#   advisory (default): warns on violations, never blocks (exit 0).
#   enforce:            blocks non-conforming messages (exit 1).
#                       Enable with: GOVERNANCE_ENFORCE=1
# Install project-locally with bin/install.sh <project-dir> --with-hooks.
# A broken or missing hook must never block the developer: if anything fails
# unexpectedly, exit 0.

set -u

MESSAGE_FILE="$1"
MODE="${GOVERNANCE_ENFORCE:-0}"

# Conventional Commits pattern: type(scope): subject
PATTERN='^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test|process|governance)(\([a-z0-9_.-]+\))?!?: .+'

fail_open() {
  echo "governance commit-msg hook: internal error, failing open" >&2
  exit 0
}

[ -n "${MESSAGE_FILE:-}" ] || fail_open
[ -f "$MESSAGE_FILE" ] || fail_open

MESSAGE="$(head -n 1 "$MESSAGE_FILE" 2>/dev/null)" || fail_open

# Merge commits are exempt.
if echo "$MESSAGE" | grep -qE '^Merge (branch|pull request|remote-tracking)'; then
  exit 0
fi

if echo "$MESSAGE" | grep -Eq "$PATTERN"; then
  exit 0
fi

cat >&2 <<EOF
[governance] Commit message does not follow Conventional Commits.

Expected: type(scope): subject
Example:  feat(auth): add session refresh endpoint

Types: build chore ci docs feat fix perf refactor revert style test process governance

${MODE:+}
EOF

if [ "$MODE" = "1" ]; then
  echo "[governance] ENFORCE mode: commit blocked. Edit the message or run with --no-verify." >&2
  exit 1
fi

echo "[governance] advisory mode: commit allowed." >&2
exit 0
