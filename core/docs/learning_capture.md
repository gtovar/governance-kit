# Learning Capture (Canonical)

> **Vehículo**: enrutada desde la constitución (actividad: lección reutilizable detectada) + script determinista `scripts/learning-capture.sh` (append al inbox). El inbox vive en la raíz del repo: `LEARNING_CAPTURE_INBOX.md`.
> **Disparador real**: no depende solo de juicio espontáneo a media sesión — el close ritual (`docs/session_rituals.md`) revisa cada bullet de "what was learned" contra la lista de abajo en cada cierre de sesión, así que la captura ocurre en un paso que de todos modos ya es obligatorio.
> **Autoridad**: normativa para decidir qué se captura; el formato es fijo.

La lección técnica que no se captura en el momento se evapora cuando se cierra la sesión. Este mecanismo la congela antes de que se pierda — incluso antes de que esté pulida como tarjeta Anki, ADR o doc formal.

## Qué SÍ pertenece al inbox

- debugging lessons worth reusing
- framework or tooling gotchas
- architecture lessons discovered during implementation
- contract mistakes found by tests
- command sequences or checks that solved recurring problems

## Qué NO pertenece

- long tutorials
- vague reflections without evidence
- full ADR content
- temporary TODO lists

## Entry Template (fijo)

```markdown
### YYYY-MM-DD — Short title
- Repo/scope:
- Trigger:
- Lesson:
- Reusable rule:
- Evidence:
- Follow-up:
- Anki candidate:
```

Reglas de escritura: una lección por entrada; "reusable rule" = una regla accionable, no un ensayo; "Evidence" = archivo/test/comando real; "Anki candidate" = yes/no (candidato a repaso espaciado).

## Captura determinista

```bash
scripts/learning-capture.sh "<repo_scope>" "<title>" "<trigger>" "<lesson>" "<reusable_rule>" "<evidence>" "<follow_up>" [yes|no]
```

Append al inbox sin tocar el resto del archivo. Para capturas con más contexto (decisión arquitectónica), usar ADR/DDR en su lugar.

## Graduación / archivado

El inbox es una zona de tránsito, no un archivo permanente. Cuando
`scripts/log-hygiene.sh check` marca más de 20 entradas, archiva las más
viejas con `scripts/log-hygiene.sh archive LEARNING_CAPTURE_INBOX.md` — mueve
las entradas fuera del inbox activo a `LEARNING_CAPTURE_INBOX_ARCHIVE.md` sin
perder ninguna (el archivo de archivo se indexa en `docs/index.md` la primera
vez que se crea). Una entrada ya promovida (a Anki, a un doc formal, o a un
ADR) es candidata inmediata a archivarse aunque el inbox no haya llegado al
umbral — no hace falta esperar.
