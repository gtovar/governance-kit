#!/usr/bin/env bash
# doc-health: deterministic documentation drift checker (governance-kit).
# Checks:
#   1) unbalanced ``` fences
#   2) broken internal links
#   3) docs not indexed in docs/index.md ("ghost docs")
# Exit codes: 0 = clean, 1 = findings (documentation drift detected)
# Advisory by design: this checker reports; it never blocks on its own.
# Usage: ./scripts/doc-health.sh   (from anywhere inside the repo)

set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

REPORT="$(mktemp)"
trap 'rm -f "$REPORT"' EXIT

SOURCE_MODE=0
INDEX="docs/index.md"
SEARCH_ROOT="."
if [ ! -f "$INDEX" ] && [ -f "core/docs/index.md" ]; then
  SOURCE_MODE=1
  INDEX="core/docs/index.md"
  SEARCH_ROOT="core"
fi

MD_FILES="$(
  find "$SEARCH_ROOT" \
    \( -path ./.git -o -path ./.opencode -o -path ./.agents \
       -o -path ./.codex -o -path ./.claude -o -name node_modules \
       -o -name .next \) \
    -prune -o -name '*.md' -print | sed 's|^\./||'
)"

echo "== doc-health =="
echo "Raíz: $ROOT"
echo ""

# 1) Fences ``` desbalanceados
echo "-- 1) Fences (\`\`\`) balanceados --"
while IFS= read -r f; do
  [ -z "$f" ] && continue
  count="$(grep -c '^```' "$f" || true)"
  if [ $(( count % 2 )) -ne 0 ]; then
    echo "FENCE DESBALANCEADO: $f (encontrados $count marcadores \`\`\`)" | tee -a "$REPORT"
  fi
done <<< "$MD_FILES"

# 2) Links internos rotos: [texto](ruta) donde ruta es relativa (no http/https, no solo ancla)
echo ""
echo "-- 2) Links internos rotos --"
while IFS= read -r f; do
  [ -z "$f" ] && continue
  dir="$(dirname "$f")"
  links="$(grep -oE '\]\(([^()# ]+)(#[^()]*)?\)' "$f" | sed -E 's/^\]\(([^()#]+).*\)$/\1/' || true)"
  while IFS= read -r link; do
    [ -z "$link" ] && continue
    case "$link" in
      http://*|https://*|mailto:*) continue ;;
    esac
    if [ "$SOURCE_MODE" -eq 1 ] && [ "$dir" = "core/docs" ] && [[ "$link" = templates/* ]]; then
      target="core/$link"
    elif [ "$dir" = "." ]; then
      target="$link"
    else
      target="$dir/$link"
    fi
    if [ ! -e "$target" ]; then
      echo "LINK ROTO: $f -> $link" | tee -a "$REPORT"
    fi
  done <<< "$links"
done <<< "$MD_FILES"

# 3) Docs no indexados en docs/index.md (conocimiento fantasma)
echo ""
echo "-- 3) Docs no indexados en $INDEX --"
if [ -f "$INDEX" ]; then
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    base="$(basename "$f")"
    # exceptions: the index itself, session-config files, and reusable templates
    case "$f" in
      "$INDEX"|AGENTS.md|core/AGENTS.md|CLAUDE.md|docs/templates/*|core/templates/*) continue ;;
    esac
    if ! grep -qF "$base" "$INDEX"; then
      echo "DOC NO INDEXADO: $f (no aparece referenciado en $INDEX)" | tee -a "$REPORT"
    fi
  done <<< "$MD_FILES"
else
  echo "AVISO: no existe $INDEX — no se puede verificar indexación." | tee -a "$REPORT"
fi

echo ""
ISSUES="$(wc -l < "$REPORT" | tr -d ' ')"
if [ "$ISSUES" -eq 0 ]; then
  echo "OK — doc-health limpio (0 hallazgos)."
  exit 0
else
  echo "doc-health encontró $ISSUES hallazgo(s). Revisa arriba antes de cerrar el bloque."
  exit 1
fi
