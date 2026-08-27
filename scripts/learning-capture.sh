#!/usr/bin/env bash

# Purpose:
# Minimum learning-capture helper.
# Appends a structured entry to LEARNING_CAPTURE_INBOX.md so reusable lessons
# survive beyond the current session, even before they become Anki cards.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INBOX_FILE="$ROOT_DIR/LEARNING_CAPTURE_INBOX.md"

if [[ $# -lt 7 ]]; then
  echo "usage: scripts/learning-capture.sh <repo_scope> <title> <trigger> <lesson> <reusable_rule> <evidence> <follow_up> [anki_candidate]"
  exit 1
fi

repo_scope="$1"
title="$2"
trigger="$3"
lesson="$4"
reusable_rule="$5"
evidence="$6"
follow_up="$7"
anki_candidate="${8:-review}"
today="$(date +%F)"

cat >> "$INBOX_FILE" <<EOF

### $today — $title
- Repo/scope: $repo_scope
- Trigger: $trigger
- Lesson: $lesson
- Reusable rule: $reusable_rule
- Evidence: $evidence
- Follow-up: $follow_up
- Anki candidate: $anki_candidate
EOF

echo "learning-capture: appended to $INBOX_FILE"
