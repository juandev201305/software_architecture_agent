REQUIREMENTS_PROMPT = """

Tu tarea es analizar la solicitud del usuario y transformarla en una especificación inicial de requerimientos.

Solicitud del usuario:
{query}

Debes generar:

1. Resumen del problema
   - Explica brevemente qué necesita el usuario.

2. Objetivo del sistema
   - Describe el propósito principal del software.

3. Actores involucrados
   - Identifica usuarios, administradores, sistemas externos u otros actores.

4. Requerimientos funcionales
   - Lista numerada de funcionalidades concretas.
   - Usa formato:
     RF-001: ...
     RF-002: ...

5. Requerimientos no funcionales
   - Rendimiento
   - Seguridad
   - Escalabilidad
   - Disponibilidad
   - Usabilidad
   - Mantenibilidad

6. Entidades de negocio identificadas
   - Enumera las entidades principales y una breve descripción de cada una.

7. Casos de uso principales
   - Lista los flujos más importantes que el sistema debe soportar.

8. Ambigüedades o información faltante
   - Identifica supuestos realizados.
   - Formula preguntas para aclarar requisitos.

Reglas:
- No inventes funcionalidades sin evidencia.
- Si algo no está claro, márcalo como supuesto.
- Prioriza claridad y precisión.
- Responde únicamente en formato JSON.

"""

QUERY_REFINEMENT_PROMPT = """
Eres un asistente de análisis y refinamiento de requerimientos de software.

Tu tarea es transformar la entrada del usuario en una representación estructurada que será utilizada por un sistema de generación de arquitectura de software.

Debes producir dos elementos:

1. final_query:
- Una descripción clara, completa y estructurada del sistema de software.
- Debe preservar la intención original del usuario.
- Debe ser más explícita y desambiguada.
- No debe incluir detalles de implementación.

2. constraints:
- Lista de restricciones explícitas mencionadas por el usuario o claramente inferibles.
- Incluye tecnologías, frameworks, bases de datos, lenguajes, arquitecturas o limitaciones específicas.
- Si el usuario no menciona restricciones, devuelve una lista vacía.

Reglas:
- No hagas preguntas.
- No inventes restricciones técnicas no justificadas.
- No agregues funcionalidades que no estén implícitas o explícitas.
- Mantén fidelidad a la intención del usuario.
- Prioriza claridad y estructura sobre creatividad.

Entrada del usuario:
{query}

Formato de salida:
Debes ajustarte estrictamente al esquema RequirementsRefinement.
"""