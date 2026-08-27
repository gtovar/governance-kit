# CLAUDE.md — Claude Code adapter

Este archivo es un **adaptador**, no la constitución. La verdad canónica vive en `AGENTS.md` y `docs/process/`.

Al iniciar sesión: leer `AGENTS.md` y seguir el orden canónico de su sección **Start here**.

No duplicar aquí ninguna regla; si algo falta, está en el canon. Si un documento de este proyecto dice algo que contradice a `AGENTS.md`, gana `AGENTS.md` y se corrige el documento.

Los hooks de sesión (`.claude/settings.json`) cargan `CURRENT_STAGE.md` al inicio y corren `doc-health.sh` al cerrar — advisory, nunca bloquean por su cuenta.
