# PROJECT_STATE — Frontend Extension Template

> Extensión específica de frontend para `PROJECT_STATE.md`.
> La estructura base y las reglas duras viven en `project_state_fill_guide.md` (el contrato primario).
> Este archivo define SOLO las expectativas específicas del frontend.

## Frontend-Specific Expectations (Sección 3 del PROJECT_STATE)

La sección "Component-by-Component Technical State" para un frontend debe cubrir:

- Application shell and navigation.
- Screens and shared components.
- API client and environment configuration.
- State management approach (si aplica).
- Test status: unit (componentes) + integration (API client) + E2E (flujos críticos) cuando existan.

## User Story Status (Sección 4)

Cada HU frontend usa exactamente el mismo bloque de estado compartido
(`Status` / `Evidence` / `Open items` / `Technical risks` / `Recent change`)
definido en `project_state_fill_guide.md`.

## Update Triggers

Update `PROJECT_STATE.md` when one of these is true:

- a frontend user story changes status
- screens, components, routes, or contracts change
- critical frontend test status changes
- environment or runtime assumptions for the frontend change

Never update it for plans, ideas, or speculative notes.
