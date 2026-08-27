#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/comment-hygiene.sh [repo_path]

Optional deterministic checks for basic comment hygiene.

Checks:
- TODO/FIXME markers must use `TODO:` or `FIXME:` with non-empty detail
- empty comment lines such as `//` or `#` are blocked
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

REPO_PATH="${1:-$(pwd)}"

if [[ ! -d "$REPO_PATH/.git" ]]; then
  echo "comment-hygiene: not a git repo: $REPO_PATH" >&2
  exit 1
fi

cd "$REPO_PATH"

if ! command -v rg >/dev/null 2>&1; then
  echo "comment-hygiene: rg is required" >&2
  exit 1
fi

failures=0

report_block() {
  echo "BLOCK: $1" >&2
  failures=$((failures + 1))
}

CODE_GLOBS=(
  '*.js'
  '*.jsx'
  '*.ts'
  '*.tsx'
  '*.mjs'
  '*.cjs'
  '*.py'
  '*.sh'
)

run_rg() {
  rg --line-number --color never "$@"
}

if output="$(run_rg -g '*.md' -g '*.js' -g '*.jsx' -g '*.ts' -g '*.tsx' -g '*.mjs' -g '*.cjs' -g '*.py' -g '*.sh' 'TODO(?!:\s*\S)|FIXME(?!:\s*\S)' . 2>/dev/null || true)" && [[ -n "$output" ]]; then
  report_block "TODO/FIXME comments must use actionable 'TODO:' or 'FIXME:' text"
  printf '%s\n' "$output" >&2
fi

if output="$(run_rg -g '*.js' -g '*.jsx' -g '*.ts' -g '*.tsx' -g '*.mjs' -g '*.cjs' '^\s*//\s*$' . 2>/dev/null || true)" && [[ -n "$output" ]]; then
  report_block "empty single-line comments are not allowed"
  printf '%s\n' "$output" >&2
fi

if output="$(run_rg -g '*.py' -g '*.sh' '^\s*#\s*$' . 2>/dev/null || true)" && [[ -n "$output" ]]; then
  report_block "empty shell/python comments are not allowed"
  printf '%s\n' "$output" >&2
fi

if (( failures > 0 )); then
  echo "comment-hygiene: failed" >&2
  exit 1
fi

echo "comment-hygiene: OK"
