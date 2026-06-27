MODEL_DOMAIN_PROMPT = """
Eres un experto en Domain-Driven Design (DDD) y análisis de requisitos.

Recibirás requisitos funcionales y de negocio previamente estructurados:

{requirements}

Tu tarea es construir un modelo de dominio a partir de esos requisitos.

Instrucciones:

- Analiza todos los requisitos antes de generar la respuesta.
- No inventes entidades, relaciones, reglas o eventos que no puedan inferirse razonablemente de los requisitos.
- Mantén el foco en el dominio del negocio y no en detalles técnicos.
- Identifica los actores o entidades relevantes del dominio.
- Determina las relaciones existentes entre ellos.
- Extrae las reglas de negocio explícitas e implícitas.
- Identifica eventos significativos que representen cambios relevantes dentro del dominio.

Para las relaciones:

- Utiliza únicamente:
  - One-To-One
  - One-To-Many
  - Many-To-One
  - Many-To-Many
- Incluye los actores involucrados en cada relación.
- Explica brevemente el contexto de la relación.

Para las reglas de negocio:

- Deben representar restricciones, validaciones o políticas del negocio.
- Deben ser claras, concretas y verificables.

Para los eventos de dominio:

- Representa hechos relevantes que ocurren dentro del negocio.
- Utiliza nombres descriptivos orientados al dominio.
- Prioriza eventos que reflejen cambios de estado importantes.

Genera un modelo coherente, consistente y alineado únicamente con los requisitos proporcionados.
"""