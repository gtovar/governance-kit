# API Reference Template

> Por cada endpoint real, exactamente estas 6 secciones.
> Prohibido: endpoints "planeados", ejemplos hipotéticos, variables ocultas.
> Solo endpoints que existen en el código y son reproducibles.

## <Título de la Operación>

### 1. Método y Ruta

```text
GET /api/v1/<path>
```

### 2. Descripción Breve

<una o dos frases>

### 3. Parámetros de Query

| Nombre | Tipo | Requerido | Descripción |
| ------ | ---- | --------- | ----------- |
| <...>  | <...> | sí/no     | <...>       |

### 4. Cuerpo de la Solicitud (solo POST/PUT/PATCH)

```json
{ "field": "value" }
```

### 5. Cuerpo de la Respuesta (éxito)

```json
{ "field": "value" }
```

### 6. Errores Esperados

| Status | Error | Causa |
| ------ | ----- | ----- |
| <...>  | <...> | <...> |

Ejemplos reales basados en tests. Si existe contract test, referenciar su ruta.
