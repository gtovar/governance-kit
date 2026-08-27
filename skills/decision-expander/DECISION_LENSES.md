# DECISION_LENSES.md

## 1. Propósito del archivo

Este archivo define las lentes obligatorias que la skill `decision-expander` debe recorrer al expandir una decisión antes de ejecutarla.

No reemplaza `SKILL.md`.
Lo complementa.

`SKILL.md` define cuándo usar la skill, cómo responder y qué estándar de calidad seguir.
Este archivo define qué dimensiones mínimas deben inspeccionarse para que la expansión cognitiva no dependa solo del criterio momentáneo del agente.

Su función es reducir omisiones repetidas, mejorar la comparabilidad entre decisiones y convertir exploración difusa en exploración disciplinada.

---

## 2. Lentes obligatorias para explorar una decisión

Toda decisión analizada con esta skill debe pasar por estas lentes:

1. contexto omitido
2. restricciones reales
3. supuestos no verificados
4. capacidades nativas ya existentes
5. capacidades posibles con configuración o composición
6. límites reales del sistema
7. alternativas no obvias
8. costo de no explorar
9. costo de sobreestimar
10. prueba mínima para salir de la duda

No se debe saltar una lente solo porque la primera intuición parezca suficiente.
Si una lente no aplica, debe decirse explícitamente por qué.

---

## 3. Preguntas guía por cada lente

### 1. contexto omitido

Preguntas guía:
- ¿Qué parte del problema no fue dicha pero cambia la decisión?
- ¿Qué actor, entorno, dependencia o secuencia falta en el encuadre?
- ¿La decisión está siendo planteada demasiado pronto respecto al contexto disponible?
- ¿Se está mezclando una necesidad real con una preferencia de implementación?

### 2. restricciones reales

Preguntas guía:
- ¿Qué restricciones están demostradas y cuáles solo fueron asumidas?
- ¿La restricción es técnica, operativa, contractual, temporal o política?
- ¿Qué evidencia confirma que la restricción existe hoy?
- ¿La restricción aplica al sistema completo o solo a una variante de uso?

### 3. supuestos no verificados

Preguntas guía:
- ¿Qué se está tratando como hecho sin prueba suficiente?
- ¿Qué dependencia, costo o limitación se está dando por cierta sin validación?
- ¿Qué parte del razonamiento depende de una interpretación no comprobada?
- ¿Qué tendría que ser verdad para que la recomendación actual funcione?

### 4. capacidades nativas ya existentes

Preguntas guía:
- ¿El sistema o herramienta ya resuelve parte del problema sin extensiones?
- ¿Hay funciones integradas que no se están considerando por desconocimiento?
- ¿Se está proponiendo construir algo que ya existe nativamente?
- ¿Qué parte del problema podría resolverse usando lo que ya está disponible?

### 5. capacidades posibles con configuración o composición

Preguntas guía:
- ¿La limitación desaparece si se cambia configuración, integración o flujo?
- ¿Hay una combinación simple de capacidades existentes que abra otra opción?
- ¿La herramienta parece insuficiente solo porque se está usando de forma estrecha?
- ¿Qué solución compuesta podría cubrir el objetivo sin rediseño mayor?

### 6. límites reales del sistema

Preguntas guía:
- ¿Qué límite sí está demostrado por arquitectura, contrato o comportamiento observable?
- ¿Dónde termina realmente la capacidad del sistema?
- ¿Qué casos fallan de forma estructural y no por mala configuración?
- ¿Qué no debe prometerse porque el sistema no lo soporta de forma confiable?

### 7. alternativas no obvias

Preguntas guía:
- ¿Qué otra forma de lograr el objetivo evita el cuello de botella actual?
- ¿Hay una ruta indirecta más simple que la opción inicialmente discutida?
- ¿Se puede cambiar la forma del problema en vez de forzar la solución original?
- ¿Existe una opción intermedia entre “hacerlo completo” y “no hacerlo”?

### 8. costo de no explorar

Preguntas guía:
- ¿Qué riesgo tiene decidir demasiado pronto?
- ¿Qué opción podríamos descartar incorrectamente si no expandimos más?
- ¿Qué deuda o retrabajo introduce una decisión cerrada prematuramente?
- ¿Qué oportunidad se pierde si aceptamos el encuadre actual sin tensión crítica?

### 9. costo de sobreestimar

Preguntas guía:
- ¿Qué daño produce asumir capacidades que no están probadas?
- ¿Qué tipo de promesa, diseño o plan quedaría apoyado en fantasía?
- ¿Qué dependencia futura se vuelve frágil si exageramos lo que el sistema puede hacer?
- ¿Qué falla se vería tarde por exceso de optimismo técnico?

### 10. prueba mínima para salir de la duda

Preguntas guía:
- ¿Cuál es el experimento más pequeño que reduce la incertidumbre principal?
- ¿Qué evidencia mínima separa una posibilidad real de una especulación?
- ¿Qué prueba tiene mejor relación costo/aprendizaje?
- ¿Qué resultado cambiaría de verdad la recomendación?

---

## 4. Criterio de cierre de la exploración

La exploración está completa cuando se cumplan todas estas condiciones:

- cada lente que aplica fue recorrida y respondida
- cada lente que no aplica fue descartada con razón explícita
- los hallazgos más importantes están clasificados por nivel (hecho, inferencia, hipótesis, riesgo)
- la prueba mínima para salir de la duda fue identificada o descartada con razón
- la recomendación no contradice ningún hecho verificado
- si quedan incertidumbres relevantes, están nombradas explícitamente y no ocultas en la recomendación

No extender la exploración más allá de esto. Si hay algo sin resolver, nombrarlo como abierto y proponer cómo cerrarlo, no seguir expandiendo indefinidamente.

---

## 5. Formato mínimo de salida de la skill

Toda respuesta producida con esta skill debe incluir como mínimo:

1. qué existe realmente
2. lectura operativa de la intención del usuario
3. qué podría estar mal nombrado o mal asumido
4. variables omitidas
5. capacidades no consideradas
6. límites reales
7. alternativas no obvias
8. riesgos
9. prueba mínima para salir de la duda
10. recomendación

Reglas de formato:
- cada afirmación importante debe marcarse como `hecho verificado`, `inferencia fuerte`, `hipótesis útil`, `riesgo` o `recomendación`
- si falta evidencia para sostener una afirmación, debe indicarse como no verificado
- si una capacidad parece posible pero no está confirmada, no debe presentarse como capacidad real
- si una sección no aplica, debe decirse explícitamente por qué
- la recomendación debe aparecer al final, nunca antes de la exploración

Este formato no impide ampliar la respuesta, pero sí fija un piso común para que la skill produzca salidas comparables y auditables.

---

## 6. Jerarquía de hallazgos

No todos los hallazgos tienen el mismo peso.
La skill debe ordenarlos así:

### Nivel 1. hechos verificados

Información confirmada por evidencia observable, documentación confiable, comportamiento comprobado o instrucciones explícitas.

### Nivel 2. inferencias fuertes

Conclusiones razonables apoyadas por varios hechos, pero que todavía no equivalen a prueba directa.

### Nivel 3. hipótesis útiles

Posibilidades plausibles que expanden el espacio de decisión, pero que requieren validación antes de influir de forma decisiva en arquitectura o compromiso operativo.

### Nivel 4. riesgos

Consecuencias posibles de decidir con información incompleta, subestimar el sistema o sobreestimarlo.

### Nivel 5. recomendación

Juicio final posterior a la exploración, condicionado por el peso relativo de hechos, inferencias, hipótesis y riesgos.

Reglas de uso:
- un hecho verificado pesa más que una inferencia fuerte
- una inferencia fuerte pesa más que una hipótesis útil
- una hipótesis útil no debe venderse como conclusión
- una recomendación no puede contradecir los hechos verificados
- si la base factual es débil, la recomendación debe ser más cauta y apoyarse en pruebas mínimas

---

## 7. Regla de evidencia y clasificación

Nunca presentar:
- inferencias como hechos
- hipótesis como límites reales
- capacidades no verificadas como capacidades reales
- posibilidades por configuración o composición como si ya existieran en la implementación actual

Cuando una capacidad o límite no esté verificado, debe clasificarse explícitamente como una de estas opciones:
- `hecho verificado`
- `inferencia fuerte`
- `hipótesis útil`
- `riesgo`

Si la evidencia no alcanza para ubicar una afirmación con claridad, la respuesta debe decir que el estado sigue abierto y proponer la prueba mínima necesaria para salir de la duda.

---

## 8. Hallazgos que deberían promoverse luego a reglas permanentes

Promover después a reglas, guías o criterios permanentes cuando el hallazgo sea:

- recurrente en más de una decisión relevante
- verificable y no dependiente de una conversación particular
- suficientemente estable en el tiempo
- útil para prevenir errores repetidos
- una capacidad nativa que el equipo subestima de forma sistemática
- una limitación real que el equipo sobreestima o ignora repetidamente
- un criterio de descarte o adopción que mejora decisiones futuras
- una prueba mínima reusable que conviene estandarizar
- una distinción operacional valiosa entre hecho, inferencia, riesgo y recomendación
- una heurística que reduzca retrabajo sin ocultar complejidad real

Promover especialmente cuando el hallazgo pueda convertirse en:
- regla de decisión
- checklist
- criterio de admisión
- patrón de evaluación
- guía de exploración previa a ejecución

---

## 9. Hallazgos que NO deben institucionalizarse todavía

No institucionalizar todavía hallazgos que sean:

- observaciones de una sola situación no repetida
- dependientes de contexto local o temporal inestable
- conclusiones basadas en evidencia incompleta
- preferencias personales disfrazadas de regla general
- atajos que funcionaron una vez pero no tienen estabilidad demostrada
- hipótesis útiles para explorar, pero no confirmadas
- recomendaciones tácticas ligadas a una herramienta, versión o entorno cambiante
- decisiones que todavía dependen de validación experimental
- marcos demasiado vagos para guiar acción concreta
- formulaciones tan rígidas que cerrarían exploración válida futura

Antes de institucionalizar, preguntar:
- ¿esto es repetible?
- ¿esto ya fue validado fuera de un caso aislado?
- ¿esto reduce errores reales?
- ¿esto sigue siendo cierto si cambia el contexto cercano?
