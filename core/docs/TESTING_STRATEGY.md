# Testing Strategy (Canonical)

> **Vehículo**: enrutada desde la constitución (actividad: tests) + aplicada por el subagente `reviewer` (juicio de profundidad). Determinismo (que los tests corran) vive en CI, perfil S4.
> **Autoridad**: normativa para elegir profundidad de test; repo-local docs ejecutan la elección.

Este documento responde: qué nivel de test corresponde a un cambio, cuándo un flujo es crítico, y cuándo una herramienta es táctica vs política.

## Core Principles

- Prefer the smallest test that can prove the risk correctly.
- Do not use E2E for simple isolated logic.
- Do not rely only on unit tests when the risk lives in wiring, contracts, or user flows.
- A test must match the real failure mode you are trying to prevent.
- Natural language can justify a testing choice, but the final validation must be evidence-driven.

## Test Levels

### Unit

Use when:
- logic is isolated; behavior provable without HTTP, DB, browser, or multi-layer wiring
- failure risk is local to one function, helper, builder, parser, or component state helper

Do not rely only on unit tests when:
- the real risk is contract serialization
- multiple layers interact
- auth/session/wiring behavior is the concern

### Integration

Use when:
- the risk lives between two or more layers
- a route/controller/service/model contract needs proof
- serialization, auth, event emission, or persistence behavior may drift

This is the default stronger choice when the bug could hide behind mocks.

### E2E

Use when:
- the user-visible flow itself is the risk
- multiple systems or layers must cooperate
- the question is "does the product flow really work from the user's perspective?"

Do not introduce E2E by default for static rendering, local helper logic, or cases fully covered by unit/integration.

## Critical Flow Definition

A flow is critical when at least one of these is true:
- it changes authentication or session state
- it performs destructive or user-visible irreversible actions
- it crosses frontend + backend boundaries with visible feedback
- it changes stable API contracts
- it changes event or persistence semantics
- it is a core demo flow of the project

Critical-flow default: require at least integration coverage; consider E2E when the user-visible sequence is the main risk.

## Default Decision Rules

1. Isolated and deterministic change → prefer unit.
2. Route/service/model or component/API wiring → require integration.
3. Confirmation UX, auth/session transitions, multi-step feedback → evaluate E2E.
4. A bug could hide behind mocking the wrong layer → strengthen the level.
5. Change affects a documented stable contract → do not stop at unit tests.

## Tactical vs Policy Tooling

- **Tactical**: introduced to validate one story or one narrow risk; not required by CI or repo policy; does not define the default for future work.
- **Policy**: the project treats it as a standard; repo docs say when it must be used; CI or merge readiness depends on it.

If a new test layer is added: record it in repo docs or ADRs when it becomes standard. Do not silently treat tactical tests as mandatory policy.

## Usage

Before validating a task:
1. classify the risk
2. choose the smallest sufficient test level
3. strengthen if the risk involves wiring, contracts, or critical flows
4. record evidence in repo-local state documents when significant

During commit-readiness: do not call work ready if the testing level is obviously too weak for the change.
