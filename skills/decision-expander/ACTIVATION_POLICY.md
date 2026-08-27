# ACTIVATION_POLICY.md

## 1. Propósito del archivo

Este archivo registra la política operativa de uso de `decision-expander` dentro del workspace.

No define una nueva arquitectura.
No reemplaza `SKILL.md`.
No reemplaza `DECISION_LENSES.md`.

Su función es dejar explícito cuándo conviene activar esta skill, cuándo no aporta valor suficiente y bajo qué condiciones tendría sentido considerar una integración más fuerte en el futuro.

---

## 2. Estado actual de decision-expander

`decision-expander` se mantiene como una skill repo-scoped invocable.

Su estado actual es:

- skill explícita
- uso contextual
- sin integración en `AGENTS.md`
- sin activación desde `intent_map.md`
- sin hooks
- sin subagents
- sin enforcement global

Su función actual es expandir decisiones antes de fijar dirección cuando el riesgo principal no está en ejecutar mal, sino en decidir con marco incompleto.

---

## 3. Cuándo usarla

Usar `decision-expander` cuando la decisión todavía no esté suficientemente cerrada y exista riesgo real de:

- variables omitidas
- límites mal entendidos
- capacidades subestimadas
- capacidades sobreestimadas
- descarte prematuro de opciones
- institucionalización prematura de una dirección débil

Regla operativa:
- usarla cuando haya al menos 1 disparador fuerte
- o cuando haya al menos 2 disparadores suaves

No usarla por reflejo.
Usarla cuando la expansión cognitiva probablemente cambie la calidad de la decisión.

---

## 4. Disparadores fuertes

Activar `decision-expander` cuando ocurra cualquiera de estos casos:

- la decisión puede convertirse en regla, workflow, criterio persistente, ADR o DDR
- existe riesgo de descartar una opción por un límite no demostrado
- la decisión tiene alto costo de reversión
- la decisión cambia cómo trabajará el sistema, no solo una tarea local
- la decisión puede institucionalizar una lectura incompleta del problema
- la decisión afecta arquitectura, tooling o workflow con impacto más allá del caso inmediato

---

## 5. Disparadores suaves

Activar `decision-expander` cuando se acumulen al menos 2 de estos casos:

- hay alta ambigüedad
- faltan variables o contexto relevante
- se mezclan capacidades reales con capacidades imaginadas
- no está claro si el problema es de calidad, activación, autoridad, integración o trazabilidad
- la decisión toca tooling, workflow o arquitectura sin evidencia suficiente
- la decisión depende demasiado de intuición no validada
- la discusión está colapsando demasiado pronto en una sola recomendación
- no está claro qué parte del razonamiento es hecho, inferencia, hipótesis o riesgo

---

## 6. Cuándo no usarla

No usar `decision-expander` para:

- tareas locales y reversibles
- fixes tácticos de bajo impacto
- ejecución ya definida
- cambios donde el costo de error sea bajo
- trabajo donde no se esté tomando una decisión de dirección
- validaciones mecánicas que ya dependen de reglas claras o checks automáticos
- casos donde la incertidumbre relevante ya fue resuelta con evidencia suficiente

La skill no debe convertirse en un paso ritual para trabajo que no necesita expansión cognitiva.

---

## 7. Qué NO implica esta policy

Esta policy no convierte a `decision-expander` en:

- obligación global
- hook
- subagent
- regla constitucional
- enforcement automático
- requisito previo universal antes de ejecutar trabajo

Tampoco implica que toda decisión de arquitectura, tooling o workflow deba usar la skill sin umbral.
La activación sigue siendo contextual.

---

## 8. Criterio futuro para considerar una integración más fuerte

Solo considerar una integración más fuerte si aparece evidencia repetida de que:

- la skill mejora decisiones reales de forma consistente
- el valor principal ya no es solo estructura reusable, sino reducción observable de errores de decisión
- el problema dominante deja de ser claridad de la skill y pasa a ser activación insuficiente
- la falta de activación empieza a generar decisiones débiles, descartes prematuros o institucionalización prematura
- existe un patrón estable de casos donde su uso debería ocurrir y hoy no ocurre

Mientras esa evidencia no exista, el estado correcto de `decision-expander` es:
- skill repo-scoped
- activación contextual
- sin escalamiento arquitectónico adicional
