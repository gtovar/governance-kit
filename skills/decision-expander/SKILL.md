---
name: decision-expander
description: Expande una decisión antes de ejecutarla. Úsala cuando quieras descubrir variables omitidas, capacidades no consideradas, supuestos débiles, límites reales y alternativas no obvias antes de elegir una herramienta, arquitectura, enfoque o apuesta.
---

# Decision Expander

## When to use

Use this skill when the user is:
- deciding between tools, approaches, architectures, or workflows
- about to reject an option because it seems impossible or inconvenient
- exploring whether a system can do more than they currently assume
- worried that important variables were not considered
- trying to separate real limits from assumed limits

Trigger phrases often look like:
- "qué no estoy viendo"
- "qué variables me faltan"
- "qué capacidades no estoy considerando"
- "ayúdame a explorar esto antes de decidir"
- "quiero saber los límites reales"
- "quiero ver si esto sí se puede"
- "quiero ampliar el mapa antes de decidir"

## Activation policy

Use this skill when there is at least 1 strong trigger or at least 2 soft triggers. Do not use it by reflex.

Strong triggers — activate when any of these apply:
- the decision may become a rule, workflow, persistent criterion, ADR, or DDR
- there is risk of discarding an option based on an unproven limit
- the decision has high reversal cost
- the decision changes how the system works, not just a local task
- the decision may institutionalize an incomplete reading of the problem
- the decision affects architecture, tooling, or workflow with impact beyond the immediate case

Soft triggers — activate when at least 2 of these apply:
- high ambiguity
- missing variables or relevant context
- real and imagined capabilities are being mixed
- it is unclear whether the problem is quality, activation, authority, integration, or traceability
- the decision touches tooling, workflow, or architecture without sufficient evidence
- the decision depends too much on unvalidated intuition
- the discussion is collapsing too quickly into a single recommendation
- it is unclear which parts of the reasoning are fact, inference, hypothesis, or risk

Do not use this skill for:
- local and reversible tasks
- low-impact tactical fixes
- already-defined execution
- changes where the cost of error is low
- work where no directional decision is being made
- mechanical validations that already depend on clear rules or automatic checks
- cases where the relevant uncertainty has already been resolved with sufficient evidence

## Primary goal

Do not jump to execution.

First expand the decision space with rigor.

Your job is to help the user see:
1. omitted variables
2. hidden assumptions
3. real capabilities of the tool/system
4. real limitations of the tool/system
5. non-obvious alternatives
6. what is proven vs unproven
7. what deserves further testing before a decision

## Non-goals

Do not:
- start implementing code unless the user explicitly asks for execution
- turn the discussion into a generic brainstorming session
- assume the user's current framing is complete
- present speculation as fact
- optimize for speed over clarity
- collapse exploration into a single premature recommendation

## Required operating behavior

Before expanding, check if this decision was discussed before in the current session or referenced in any prior context. If yes, load that context first and note what has changed since then. Do not re-expand from scratch what was already explored.

Always separate the response into these sections:

### 1. Qué existe realmente
List only what is known, verified, or explicitly stated.

### 2. Qué parece que el usuario quiere decir
Interpret the likely intent, but label it as interpretation.

### 3. Qué podría estar mal nombrado o mal asumido
Identify naming errors, hidden assumptions, category mistakes, or false limits.

### 4. Variables omitidas
List relevant variables the user may not have considered.

### 5. Capacidades no consideradas
List tool/system capabilities that might expand the solution space.

### 6. Límites reales
Distinguish real limitations from assumed limitations.

### 7. Alternativas no obvias
Provide plausible alternatives or combinations the user may not be considering.

### 8. Riesgos
Explain decision risks, including the risk of underestimating or overestimating the system.

### 9. Prueba mínima para salir de la duda
Name the smallest experiment or verification that would reduce the main uncertainty. Only recommend full commitment after this test is clear or already done.

### 10. Recomendación
Give a recommendation only after the exploration is done.

## Decision lenses

Every decision analyzed with this skill must pass through these lenses. Do not skip a lens because the first intuition seems sufficient. If a lens does not apply, say explicitly why.

### 1. contexto omitido
- What part of the problem was not stated but changes the decision?
- What actor, environment, dependency, or sequence is missing from the framing?
- Is the decision being made too early relative to available context?
- Is a real need being mixed with an implementation preference?

### 2. restricciones reales
- Which constraints are proven and which were only assumed?
- Is the constraint technical, operational, contractual, temporal, or political?
- What evidence confirms the constraint exists today?
- Does the constraint apply to the full system or only to one usage variant?

### 3. supuestos no verificados
- What is being treated as fact without sufficient proof?
- What dependency, cost, or limitation is being assumed without validation?
- What part of the reasoning depends on an unverified interpretation?
- What would have to be true for the current recommendation to work?

### 4. capacidades nativas ya existentes
- Does the system or tool already solve part of the problem without extensions?
- Are there built-in functions not being considered due to lack of awareness?
- Is something being proposed that already exists natively?
- What part of the problem could be solved using what is already available?

### 5. capacidades posibles con configuración o composición
- Does the limitation disappear if configuration, integration, or flow is changed?
- Is there a simple combination of existing capabilities that opens another option?
- Does the tool seem insufficient only because it is being used narrowly?
- What composed solution could cover the goal without major redesign?

### 6. límites reales del sistema
- Which limits are proven by architecture, contract, or observable behavior?
- Where does the system's capability actually end?
- Which cases fail structurally, not due to bad configuration?
- What should not be promised because the system does not support it reliably?

### 7. alternativas no obvias
- What other way to achieve the goal avoids the current bottleneck?
- Is there an indirect route simpler than the initially discussed option?
- Can the shape of the problem be changed instead of forcing the original solution?
- Is there an intermediate option between "do it fully" and "don't do it"?

### 8. costo de no explorar
- What is the risk of deciding too soon?
- Which option might be incorrectly discarded if expansion stops here?
- What debt or rework does a prematurely closed decision introduce?
- What opportunity is lost if the current framing is accepted without critical tension?

### 9. costo de sobreestimar
- What damage comes from assuming capabilities that are not proven?
- What kind of promise, design, or plan would rest on fantasy?
- What future dependency becomes fragile if the system is overestimated?
- What failure would appear late due to excess technical optimism?

### 10. prueba mínima para salir de la duda
- What is the smallest experiment that reduces the main uncertainty?
- What minimum evidence separates a real possibility from speculation?
- Which test has the best cost-to-learning ratio?
- What result would genuinely change the recommendation?

## Findings hierarchy

Not all findings carry the same weight. Order them as follows:

- **hecho verificado** — confirmed by observable evidence, reliable documentation, or verified behavior
- **inferencia fuerte** — reasonable conclusion supported by multiple facts, but not direct proof
- **hipótesis útil** — plausible possibility that expands the decision space but requires validation before influencing architecture or operational commitment
- **riesgo** — possible consequence of deciding with incomplete information, underestimating, or overestimating the system
- **recomendación** — final judgment after exploration, conditioned by the relative weight of facts, inferences, hypotheses, and risks

Rules:
- a verified fact outweighs a strong inference
- a strong inference outweighs a useful hypothesis
- a useful hypothesis must not be sold as a conclusion
- a recommendation cannot contradict verified facts
- if the factual base is weak, the recommendation must be more cautious and lean on minimum tests

Never present:
- inferences as facts
- hypotheses as real limits
- unverified capabilities as real capabilities
- possibilities through configuration or composition as if they already exist in the current implementation

## Exploration closure

The exploration is complete when all of these conditions are met:

- every applicable lens was covered and answered
- every non-applicable lens was explicitly discarded with a reason
- the most important findings are classified by level
- the minimum test to resolve the doubt was identified or discarded with a reason
- the recommendation does not contradict any verified fact
- if relevant uncertainties remain, they are named explicitly and not hidden in the recommendation

Do not extend exploration beyond this. If something remains unresolved, name it as open and propose how to close it.

## Exploration rules

- Be critical, not agreeable.
- Treat the user's framing as a hypothesis, not truth.
- Explicitly mark every important claim as: hecho verificado, inferencia fuerte, hipótesis útil, riesgo, or recomendación.
- If current facts are insufficient, say what remains unverified.
- Prefer a map of possibilities over a fast answer.
- If the tool/system may already support something natively, raise that possibility explicitly.
- If the user is underestimating the system, say so.
- If the user is overestimating the system, say so.
- If the opportunity is real but not yet proven, recommend a test instead of pretending certainty.

## Output style

- Write in Spanish unless the user asks otherwise.
- Be direct and analytical.
- Do not pad the answer.
- Do not flatter.
- Do not summarize too early.
- Contradict the framing when needed.
