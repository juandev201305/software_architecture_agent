# Software Architecture Agent

Agente de inteligencia artificial que genera documentación de arquitectura de software a partir de una descripción en lenguaje natural. El sistema evalúa si la consulta tiene información suficiente, puede solicitar aclaraciones al usuario de forma interactiva vía WebSocket, y ejecuta un pipeline multi-paso donde cada etapa modela un aspecto del diseño arquitectónico (requisitos, dominio, casos de uso, arquitectura, revisión) hasta producir un documento estructurado listo para compartir con un equipo de desarrollo. Todo el flujo está expuesto a través de una API WebSocket asíncrona.

## Objetivos

- Automatizar el proceso de diseño arquitectónico desde una descripción textual hasta un documento completo.
- Evaluar la completitud de la consulta inicial y solicitar aclaraciones cuando falte información.
- Ejecutar un pipeline secuencial donde cada paso produce un esquema validado que alimenta al siguiente.
- Incorporar sesgo hacia simplicidad y YAGNI en las decisiones arquitectónicas, evitando sobreingeniería.
- Revisar automáticamente la arquitectura generada para detectar sobreingeniería, subingeniería y desalineación con el problema.
- Exponer el resultado como documento markdown estructurado, listo para README, ADR o documentación técnica.
- Exponer todas las funcionalidades a través de una API WebSocket asíncrona.

## Tecnologías y herramientas

### Backend (Python)

| Categoría | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Framework API | FastAPI + Uvicorn |
| Framework LLM | LangChain |
| Modelo de lenguaje | Gemini 2.5 Flash Lite vía OpenRouter |
| Validación de datos | Pydantic v2 |
| Contenedor | Docker (slim) |
| Configuración | python-dotenv |

## Estructura del proyecto

```
software_architecture_agent/
├── .env                          # Variables de entorno (API key)
├── .gitignore
├── requirements.txt              # Dependencias de Python
├── Dockerfile                    # Imagen Docker con servidor Uvicorn
├── config/                       # Configuración del sistema
│   ├── models.py                 # Modelo LLM configurado
│   └── setting.py                # Variables de entorno y constantes
├── domain/                       # Capa de dominio (esquemas Pydantic)
│   └── schemas/
│       ├── archistecture.py      # Modelos: PreArchitecture, Architecture, Review
│       ├── documentation.py      # Modelo: Documentación final
│       ├── model_domain.py       # Modelos: Entity, Relationship, ModelDomain
│       ├── query_evaluator.py    # Modelos: QueryEvaluator, QueryEnricher, Question
│       ├── requirements.py       # Modelos: Requirements, RequirementsRefinement
│       └── use_cases.py          # Modelos: UseCase, Actor, UseCases
├── application/                  # Capa de aplicación (orquestación)
│   ├── orchestrators/
│   │   └── agent.py              # Orquestador principal asíncrono
│   ├── workflow/
│   │   ├── requirements_elicitation_workflow.py  # Workflow: evaluación, enriquecimiento y refinamiento
│   │   ├── architecture_workflow.py              # Workflow principal de arquitectura (6 etapas)
│   │   └── documentation_workflow.py             # Workflow de generación de documento final
│   ├── services/
│   │   ├── requirements_service.py     # Servicio de refinamiento y generación de requisitos
│   │   ├── query_evaluator_service.py  # Servicio de evaluación y enriquecimiento de consulta
│   │   ├── model_domain_service.py     # Servicio de modelado de dominio DDD
│   │   ├── use_cases_service.py        # Servicio de extracción de casos de uso
│   │   ├── architecture_service.py     # Servicio de diseño y revisión arquitectónica
│   │   └── documentation_service.py    # Servicio de generación de documentación
│   └── utils/
│       └── documentation_formatter.py  # Conversión del modelo Documentación a markdown
└── infrastructure/               # Capa de infraestructura
    ├── api/                      # API WebSocket (FastAPI)
    │   ├── app.py                # Punto de entrada de la aplicación FastAPI
    │   └── controllers/
    │       └── QueryController.py # Controlador WebSocket /ws/chat
    └── llm/
        ├── chain_builder.py      # Constructor genérico de cadenas LangChain
        ├── llm_factory.py        # Fábrica de instancias del proveedor LLM
        ├── providers/
        │   ├── base.py           # Clase abstracta LLMProvider
        │   └── openrouter_provider.py  # Proveedor concreto OpenRouter (ChatOpenAI)
        └── prompts/
            ├── query_evaluator_prompt.py    # Prompts de evaluación y enriquecimiento de consulta
            ├── requirements_prompt.py       # Prompts de refinimiento y requisitos
            ├── model_domain_prompt.py       # Prompt de modelado de dominio
            ├── use_cases_prompt.py          # Prompt de casos de uso
            ├── architecture_prompt.py       # Prompts de pre-arquitectura, arquitectura y revisión
            └── documentation_prompt.py      # Prompt de generación de documento final
```

## Instalación y configuración

### Requisitos previos

- Python 3.11 o superior
- Una clave API de OpenRouter

### Backend

```bash
# Clonar el repositorio
git clone https://github.com/juandev201305/software_architecture_agent.git
cd software_architecture_agent

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate      # Linux / macOS
# venv\Scripts\activate       # Windows

# Instalar dependencias
pip install -r requirements.txt
```

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
OPENAI_API_KEY=sk-or-v1-tu_clave_de_openrouter
```

## Ejecución

### Servidor API

```bash
uvicorn infrastructure.api.app:app --reload --port 8000
```

La API estará disponible en `http://localhost:8000`. El endpoint WebSocket `/ws/chat` recibe un JSON con la consulta. Si la información es insuficiente responde con estado `NEED_INFO` más las preguntas de aclaración con opciones. El cliente debe responder para que el agente continúe hasta recibir `SUCCESS` con la documentación generada.

### Docker

```bash
docker build -t software-architecture-agent .
docker run -p 8000:8000 --env-file .env software-architecture-agent
```

### Uso desde código

```python
from application.orchestrators.agent import arun_agent

result = await arun_agent("Diseña un sistema de reservas para consultorios médicos.")
print(result["documentation"])
```

## Funcionalidades implementadas

- **API WebSocket asíncrona:** Endpoint `/ws/chat` que recibe consultas en JSON, maneja el loop de aclaraciones con estado `NEED_INFO` y devuelve la documentación generada con estado `SUCCESS`. Toda la comunicación es asíncrona.

- **Evaluación de completitud de consulta:** Analiza si la descripción inicial del usuario tiene suficiente información para continuar. Si no, genera preguntas de aclaración con respuestas sugeridas para eliminar ambigüedades antes de avanzar.

- **Enriquecimiento de consulta:** Consolida la consulta original con las respuestas del usuario en una descripción única y coherente, eliminando ambigüedades antes del análisis arquitectónico.

- **Pipeline automatizado multi-etapa:** El sistema ejecuta una secuencia completa: evaluación de consulta, enriquecimiento, refinamiento, generación de requisitos, modelo de dominio DDD, casos de uso UML, pre-arquitectura, diseño arquitectónico, revisión automática y generación de documento final.

- **Modelado de dominio DDD:** Identifica entidades, atributos, comportamientos, relaciones con cardinalidad, reglas de negocio y eventos de dominio a partir de la descripción del problema.

- **Extracción de casos de uso UML:** Produce actores, objetivos, flujos principales y alternativos, precondiciones y postcondiciones.

- **Pre-arquitectura neutral:** Sintetiza el problema sin atarse a tecnología ni patrones, como paso previo a las decisiones arquitectónicas.

- **Diseño arquitectónico:** Propone patrón arquitectónico, capas con responsabilidades, tecnologías justificadas y decisiones de diseño documentadas.

- **Revisión automática:** Evalúa la arquitectura generada con puntuación del 1 al 10, detecta sobreingeniería y subingeniería, y emite observaciones críticas y recomendaciones.

- **Sesgo YAGNI y simplicidad:** Los prompts instruyen explícitamente al modelo a priorizar soluciones simples, evitar complejidad innecesaria y preferir arquitecturas monolíticas modulares sobre microservicios.

- **Salida validada con Pydantic:** Cada etapa produce un objeto Pydantic que es validado antes de pasar a la siguiente etapa, eliminando errores de formato en las transiciones.

- **Proveedor LLM intercambiable:** Arquitectura con clase abstracta `LLMProvider` que permite integrar nuevos proveedores (actualmente implementado OpenRouter vía `ChatOpenAI`).

- **Contenedor Docker:** Imagen con Uvicorn lista para ejecutar el servidor API sin instalar dependencias localmente.

## Autor

**Juan Correa**  
Correo electrónico: juandev201305@gmail.com  
GitHub: [juandev201305](https://github.com/juandev201305)  
Repositorio: [software_architecture_agent](https://github.com/juandev201305/software_architecture_agent)
