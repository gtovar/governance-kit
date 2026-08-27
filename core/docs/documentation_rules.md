# Documentation Rules (Canonical)

> **Vehículo**: skill `documentation-governance` (juicio + gates G0–G3) + verificador determinista `scripts/doc-health.sh` (fences, links, ghost docs). Enrutada desde la constitución cuando se tocan docs canónicos.
> **Autoridad**: normativa.

> This file is the authoritative documentation policy of this repository.
> It defines: language and tone, the decision-maker gates for creating documents,
> the Doc Decision Record (DDR) template, and the scoring table.

## Scope (What this applies to)

This policy applies to **canonical documentation**:

- `README.md`, `SUMMARY.md`
- `docs/index.md`
- `docs/architecture.md`, `docs/DESIGN_DOCUMENT.md`, `docs/API_REFERENCE.md`
- `docs/events_contract.md`, `docs/workflow.md`
- `docs/adr/*.md`

Non-canonical content (learning notes, scratchpads) must live under a clearly labeled area (e.g., `docs/notes/`) and must not override canonical docs.

## Language

- Canonical documentation MUST be written in **English**.
- Exceptions: proper names of external docs and unavoidable product names.

## Tone (No speculation)

- Tone MUST be **formal, neutral, factual**. (No hype, no "probably".)
- Allowed verbs: "Exists…", "Was validated…", "Includes…"
- Not allowed: "Will probably…", "Should have…", "We plan to…"
- Put guesses under a dedicated `## Hypotheses` section; never hedge in canonical sections ("maybe/probably/I think").

## Naming (Exact coordinates)

Always use full exact identifiers:

- Files: `src/services/suggestionService.js`
- Endpoints: `/api/v1/notifications/events`
- Env vars: `ML_BASE_URL`
- Tests: `tests/notificationsRoutes.test.js`

## Formatting

- Bullet points MUST use `-`
- Code blocks MUST use triple backticks and specify language when applicable
- Keep sections visually readable (single blank line between major sections)
- Emojis only for non-technical status labels (avoid in code/endpoints/paths)

## Index rule (No ghost docs)

Any new canonical doc MUST be referenced in:

- `docs/index.md` (primary) and, when relevant, `SUMMARY.md`.

A doc that is not reachable from an index does not exist for governance purposes.

## "Before merging docs" checklist

- [ ] Canon docs are in English
- [ ] No speculation words ("probably", "should", "maybe")
- [ ] Paths/endpoints are exact
- [ ] `docs/index.md` updated if a new doc exists
- [ ] Doc Health checks pass (fences, canonical links) — see `scripts/doc-health.sh`

---

## Layer separation

Each document lives in exactly one layer. Writing something outside its layer is an error:

| Capa | Documento |
| ---- | --------- |
| Arquitectura / decisiones | `docs/adr/*.md`, `docs/DESIGN_DOCUMENT.md` |
| Estado técnico actual | `PROJECT_STATE.md` |
| Reentrada mental | `README_REENTRY.md` |
| Bitácora de acciones ejecutadas | `Sprint_Log.md` |
| Cómo correrlo | `QUICKSTART.md` |
| API real | `docs/API_REFERENCE.md` |
| Futuro del producto | Roadmap (fuera del estado) |

Coherencia cruzada:

- **Technical truth (the codebase) overrides everything.** Si PROJECT_STATE contradice al código, gana el código y PROJECT_STATE se corrige.
- **API_REFERENCE gana** sobre PROJECT_STATE en conflictos de endpoints; PROJECT_STATE gana sobre documentos de proceso en estado de HUs.
- Nunca duplicar: "si un dato aparece en dos documentos, debe eliminarse uno". Referenciar por nombre y sección (`See API_REFERENCE.md — Section 4.2`), nunca parafrasear ni incrustar.
- Una HU aparece una sola vez y solo en su estado actual; la historia vive en Git, Sprint_Log y el Version Log.

## Document authority types

No todo documento manda. Clasificar cada documento como:

- **Normativo (política/instrucción):** manda hasta que se cambia formalmente (ej. "nunca acciones destructivas sin confirmación").
- **Semi-normativo (diseño/arquitectura):** manda, pero puede cambiar si el costo/beneficio no cuadra.
- **Descriptivo (notas/recopilación):** no manda; es materia prima.

Esto evita que un documento "bonito" secuestre al proyecto.

## Validation checklist (before closing the day)

1. ¿`PROJECT_STATE.md` refleja el estado real del código hoy?
2. ¿`README_REENTRY.md` dice exactamente dónde retomar mañana?
3. ¿`Sprint_Log.md` tiene lo ejecutado hoy?
4. ¿API Reference coincide con todos los endpoints reales?
5. ¿Se generó ADR si hubo decisión arquitectónica?
6. ¿QUICKSTART sigue funcionando en limpio?
7. ¿No hay duplicación entre documentos?

## Red flags (badly made document)

Si ocurre una sola, el documento debe corregirse de inmediato:

1. Mezcla futuro con presente.
2. Mezcla bitácora con estado.
3. Sin commit hash / fecha de actualización.
4. Sin coordenadas reales (archivos, endpoints, tests).
5. Secciones "por si acaso".
6. Explica sin evidencia en código.
7. Ambiguo sobre DONE.
8. No verificable con tests.

## Creation of new documents

Todo documento nuevo debe responder 3 preguntas:

1. ¿Qué propósito único tiene?
2. ¿Qué documento existente NO puede cumplirlo ya?
3. ¿Qué evidencia del código lo respalda?

Si no cumple estos requisitos, no se crea.

## Technical sanctions

Ante mezcla de capas, inconsistencias, falta de commit hash, duplicación o HU sin coordenadas: **el documento se rechaza y debe reescribirse completo.**

---

## Decision maker: create a new doc vs update an existing one

Default rule:

> **Update an existing document.**
> **Create a new document only if it passes the gates below.**

## Gate 0 — Evidence gate (mandatory)

**Question:** Do we have primary evidence for what we are documenting?
Primary evidence = diff, code, tests, snapshot, commit.

- If **NO**: do not create a canonical doc. Record it as an **Open Question** in the sprint log or as a temporary note.
- If **YES**: continue.

### Gate 1 — Owner doc gate (single source of truth)

**Question:** Does a document already exist whose scope covers this content?

Ownership map (adapt to this repository):

- **HTTP contract** → `docs/API_REFERENCE.md`
- **Event contract** → `docs/events_contract.md`
- **Architectural decision with tradeoffs** → `docs/adr/XXX-*.md`
- **Architecture/flows** → `docs/architecture.md` + `docs/DESIGN_DOCUMENT.md`
- **Process / re-entry** → re-entry doc + `docs/workflow.md`
- **History / evolution** → sprint log
- **Factual state** → `PROJECT_STATE.md`

ADR validity note: use `docs/ADR_POLICY.md` to decide whether the change is truly ADR-worthy, DDR-worthy, or still too tentative for any ADR.

If an owner doc exists: **update it**.
Creating a new doc at this point is only allowed if Gate 2 justifies a split.

### Gate 2 — Split gate (when it does not fit the owner doc)

Creating a new doc (or splitting) is allowed if **at least one** condition holds:

#### C2.1 — Different audience

- The content is for a different audience (e.g., operator vs contributor vs end user) and mixing it reduces clarity.

#### C2.2 — Different nature

- The owner doc is reference-only (e.g., API_REFERENCE) and you are trying to add tutorial or reasoning; that belongs in a dedicated tutorials or design document.

#### C2.3 — Size/complexity

- The new section would be > ~20–30% of the current doc **or** it introduces a complete subsystem that must be referenced repeatedly.

#### C2.4 — Reuse

- The same question appears >= 2 times and the absence of a doc causes drift (high cost of forgetting).

#### C2.5 — Stability

- The content is likely to remain stable for >= 1 sprint (not in flux today).

If none apply: **no new doc**; add it to the owner doc or to the sprint log as provisional.

### Gate 3 — Anti-duplication gate (mandatory)

If a new doc is created:

- It must declare its **Scope** and **Owner**.
- It must include a "Single Source of Truth" line:
  "This doc is the source of truth for X; other docs only link to it."
- It must update `docs/index.md` to add the link (if applicable).
- It must avoid copying content that already lives elsewhere.

---

## Decision record template (required output)

This is the minimum output every time we discuss "new doc?":

**Doc Decision Record (DDR)** (not necessarily a file; can live in the sprint log if no ADR is needed)

- Topic:
- Evidence:
- Candidate Owner Doc:
- Gates passed:
  - G0 Evidence: yes/no
  - G1 Owner exists: yes/no
  - G2 Split reason: (C2.x)
  - G3 Anti-duplication plan: yes/no
- Decision:
  - Update existing: (file + section)
  - Create new: (file path + why)
  - Defer: (sprint log "Open Question")

---

## Scoring (optional) to reduce subjectivity

Use a 0–10 score:

- Evidence strength (0–2)
- Owner fit gap (0–2) (0 = perfect fit; 2 = does not fit)
- Audience separation (0–2)
- Reuse frequency (0–2)
- Stability horizon (0–2)

Rule:

- Score <= 4 → Update existing doc
- Score 5–6 → Update existing + link + sprint log note (if in transition)
- Score >= 7 → Create new doc (or split), with G3 anti-duplication
