#!/usr/bin/env bash
# log-hygiene: deterministic size/growth checker and archiver for
# governance-kit's canonical logs (governance-kit).
#
# Checks (advisory, fail-open — never blocks on its own):
#   - PROJECT_STATE.md / README_REENTRY.md size: these are meant to stay
#     compact (PROJECT_STATE.md is a rewritten snapshot per
#     docs/templates/project_state_fill_guide.md, not an accumulating log).
#     Growth here usually means that rule is being violated.
#   - Sprint_Log.md / LEARNING_CAPTURE_INBOX.md size: these are legitimate
#     perpetual ledgers by design (Sprint_Log.md in particular is the
#     canonical detailed technical record other docs point into — do not
#     shrink individual entries). Recommends `archive` once they cross the
#     threshold; does not judge entry length.
#   - docs/PENDING_WORK.md size: recommends a manual review for entries to
#     move to PENDING_WORK_ARCHIVE.md per pending_work_template.md's own rule.
# A missing target file is skipped with an advisory note, not an error — this
# script also runs against the kit's own source tree, which has none of these
# as real files (only templates under core/).
#
# Usage:
#   ./scripts/log-hygiene.sh [check]
#   ./scripts/log-hygiene.sh archive <file> [--keep N]   (default N=20)
#
# `archive` only supports files whose entries are delimited by a
# `## YYYY-MM-DD` or `### YYYY-MM-DD` heading (Sprint_Log.md,
# LEARNING_CAPTURE_INBOX.md). It moves every entry except the last N to
# <stem>_ARCHIVE.<ext> (created or appended to), writing the archive before
# truncating the active file, and leaves a one-line pointer at the top.
#
# IMPORTANT — read before running archive: this script cannot detect whether
# another canonical doc (PENDING_WORK.md, CURRENT_STAGE.md) references a date
# by prose (not a markdown link — doc-health.sh would not catch this either)
# inside the range being archived. Grep for those dates across those docs
# yourself first; if a currently-open item references one, raise --keep or
# defer archiving until it's resolved.
#
# Exit codes: 0 = clean / archive succeeded / nothing to archive,
#             1 = check found advisory findings,
#             2 = usage error or archive precondition not met.

set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PROJECT_STATE_MAX_LINES=400
README_REENTRY_MAX_LINES=300
PENDING_WORK_MAX_LINES=300
SPRINT_LOG_MAX_LINES=1500
SPRINT_LOG_MAX_BYTES=$((100 * 1024))
LEARNING_INBOX_MAX_ENTRIES=20
DEFAULT_KEEP=20

REPORT="$(mktemp)"
trap 'rm -f "$REPORT"' EXIT

check_line_count() {
  local file="$1" label="$2" max="$3" reason="$4"
  if [ ! -f "$file" ]; then
    echo "AVISO: no existe $file — se omite el check de $label."
    return
  fi
  local lines
  lines="$(wc -l < "$file" | tr -d ' ')"
  if [ "$lines" -gt "$max" ]; then
    echo "$label EXCEDE $max líneas ($lines): $file — $reason" | tee -a "$REPORT"
  fi
}

check_sprint_log_size() {
  local file="$1"
  if [ ! -f "$file" ]; then
    echo "AVISO: no existe $file — se omite el check de tamaño."
    return
  fi
  local lines bytes
  lines="$(wc -l < "$file" | tr -d ' ')"
  bytes="$(wc -c < "$file" | tr -d ' ')"
  if [ "$lines" -gt "$SPRINT_LOG_MAX_LINES" ] || [ "$bytes" -gt "$SPRINT_LOG_MAX_BYTES" ]; then
    echo "$file EXCEDE el umbral de archivado ($lines líneas, $bytes bytes) — recomendado: ./scripts/log-hygiene.sh archive $file" | tee -a "$REPORT"
  fi
}

check_dated_entry_count() {
  local file="$1" max="$2"
  if [ ! -f "$file" ]; then
    echo "AVISO: no existe $file — se omite el check de entradas."
    return
  fi
  local count
  count="$(grep -cE '^#{2,3} [0-9]{4}-[0-9]{2}-[0-9]{2}' "$file" || true)"
  if [ "$count" -gt "$max" ]; then
    echo "$file EXCEDE $max entradas ($count) — recomendado: ./scripts/log-hygiene.sh archive $file" | tee -a "$REPORT"
  fi
}

cmd_check() {
  echo "== log-hygiene: check =="
  echo "Raíz: $ROOT"
  echo

  check_line_count "PROJECT_STATE.md" "PROJECT_STATE.md" "$PROJECT_STATE_MAX_LINES" \
    "posible violación de snapshot semantics (docs/templates/project_state_fill_guide.md) — reescribir como snapshot, no acumular"
  check_line_count "README_REENTRY.md" "README_REENTRY.md" "$README_REENTRY_MAX_LINES" \
    "documento operativo, debe mantenerse compacto"
  check_line_count "docs/PENDING_WORK.md" "docs/PENDING_WORK.md" "$PENDING_WORK_MAX_LINES" \
    "revisar entradas Resolved/Fixed candidatas a archivar (docs/templates/pending_work_template.md)"
  check_sprint_log_size "Sprint_Log.md"
  check_dated_entry_count "LEARNING_CAPTURE_INBOX.md" "$LEARNING_INBOX_MAX_ENTRIES"

  echo
  local issues
  issues="$(wc -l < "$REPORT" | tr -d ' ')"
  if [ "$issues" -eq 0 ]; then
    echo "OK — log-hygiene limpio (0 hallazgos)."
    return 0
  else
    echo "log-hygiene encontró $issues hallazgo(s). Advisory — revisa antes de que el archivo crezca más."
    return 1
  fi
}

cmd_archive() {
  local file="${1:-}"
  if [ -z "$file" ]; then
    echo "uso: log-hygiene.sh archive <file> [--keep N]" >&2
    return 2
  fi
  if [ ! -f "$file" ]; then
    echo "log-hygiene: no existe $file" >&2
    return 2
  fi
  shift || true

  local keep="$DEFAULT_KEEP"
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --keep) keep="${2:-}"; shift 2 ;;
      --keep=*) keep="${1#*=}"; shift ;;
      *) echo "log-hygiene: opción desconocida '$1'" >&2; return 2 ;;
    esac
  done
  case "$keep" in
    ''|*[!0-9]*) echo "log-hygiene: --keep debe ser un entero no negativo" >&2; return 2 ;;
  esac

  local total
  total="$(grep -cE '^#{2,3} [0-9]{4}-[0-9]{2}-[0-9]{2}' "$file" || true)"
  if [ "$total" -eq 0 ]; then
    echo "log-hygiene: $file no tiene entradas con encabezado '## YYYY-MM-DD' o '### YYYY-MM-DD' — no se puede archivar automáticamente." >&2
    return 2
  fi
  if [ "$total" -le "$keep" ]; then
    echo "log-hygiene: $file tiene $total entrada(s), <= --keep $keep — nada que archivar."
    return 0
  fi

  echo "log-hygiene: ADVERTENCIA — antes de continuar, verifica manualmente que ninguna"
  echo "entrada abierta en PENDING_WORK.md o CURRENT_STAGE.md apunte a una fecha dentro"
  echo "del rango que se va a archivar (esto no se detecta automáticamente)."
  echo

  local dir base stem ext archive_file
  dir="$(dirname "$file")"
  base="$(basename "$file")"
  if [[ "$base" == *.* ]]; then
    stem="${base%.*}"
    ext="${base##*.}"
  else
    stem="$base"
    ext=""
  fi
  if [ -n "$ext" ]; then
    archive_base="${stem}_ARCHIVE.${ext}"
  else
    archive_base="${stem}_ARCHIVE"
  fi
  if [ "$dir" = "." ]; then
    archive_file="$archive_base"
  else
    archive_file="$dir/$archive_base"
  fi

  local archive_is_new=1
  [ -f "$archive_file" ] && archive_is_new=0

  # 1-indexed line numbers of every dated heading, in file order.
  local heading_lines first_heading_line keep_from_index cutoff_line
  heading_lines="$(grep -nE '^#{2,3} [0-9]{4}-[0-9]{2}-[0-9]{2}' "$file" | cut -d: -f1)"
  first_heading_line="$(echo "$heading_lines" | head -1)"
  cutoff_line=""
  if [ "$keep" -gt 0 ]; then
    keep_from_index=$((total - keep + 1))
    cutoff_line="$(echo "$heading_lines" | sed -n "${keep_from_index}p")"
  fi
  # cutoff_line empty means --keep 0: every dated entry is archived and the
  # active file keeps no entries at all (still valid — preamble + pointer).

  local tmp_archive tmp_active
  tmp_archive="$(mktemp)"
  tmp_active="$(mktemp)"

  if [ -z "$cutoff_line" ]; then
    sed -n "${first_heading_line},\$p" "$file" > "$tmp_archive"
  else
    sed -n "${first_heading_line},$((cutoff_line - 1))p" "$file" > "$tmp_archive"
  fi
  {
    if [ "$first_heading_line" -gt 1 ]; then
      sed -n "1,$((first_heading_line - 1))p" "$file"
    fi
    echo
    echo "> Older entries archived in [\`$archive_base\`]($archive_base) — search there too when following a historical reference."
    if [ -n "$cutoff_line" ]; then
      echo
      sed -n "${cutoff_line},\$p" "$file"
    fi
  } > "$tmp_active"

  # Write-before-truncate: append to the archive only after both temp files
  # were built successfully, and only replace the active file afterward.
  cat "$tmp_archive" >> "$archive_file"
  mv "$tmp_active" "$file"
  rm -f "$tmp_archive"

  local archived_count=$((total - keep))
  echo "log-hygiene: archived $archived_count entries from $file -> $archive_file (kept $keep most recent)."
  if [ "$archive_is_new" -eq 1 ]; then
    echo "log-hygiene: $archive_file is new — add it to docs/index.md in this same change (ghost-doc rule)."
  fi
  return 0
}

case "${1:-check}" in
  check) cmd_check; exit $? ;;
  archive) shift; cmd_archive "$@"; exit $? ;;
  *)
    echo "uso: log-hygiene.sh [check] | archive <file> [--keep N]" >&2
    exit 2
    ;;
esac
