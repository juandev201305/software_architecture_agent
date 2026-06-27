from langchain_core.prompts import PromptTemplate
from infrastructure.llm.prompts.architecture_prompt import ARCHITECTURE_PROMPT, PRE_ARCHITECTURE_PROMPT, REVIEWER_ARCHITECTURE_PROMPT
from domain.schemas.archistecture import PreArchitecture, Architecture, ReviewArchitecture
from infrastructure.llm.chain_builder import build_chain


def generator_pre_architecture(requirements, model_domain, use_cases, llm) -> PreArchitecture:
    """
    Genera una pre-arquitectura del sistema a partir de requisitos, modelo de dominio y casos de uso.

    Esta etapa define una visión técnica inicial del sistema, incluyendo capacidades,
    restricciones y estructura general antes de tomar decisiones de implementación.
    """
    chain = build_chain(llm, prompt=PRE_ARCHITECTURE_PROMPT, schema=PreArchitecture)

    return chain.ainvoke({
        "requirements": requirements,
        "model_domain": model_domain,
        "use_cases": use_cases
        })


def generator_architecture(pre_architecture, llm, user_constraints: str = None) -> Architecture:
    """
    Convierte la pre-arquitectura en una arquitectura técnica concreta.

    Define patrones de diseño, tecnologías y estructura de alto nivel del sistema
    basándose en la visión inicial generada en la etapa anterior.
    """
    chain = build_chain(llm, prompt=ARCHITECTURE_PROMPT, schema=Architecture)

    return chain.ainvoke({
        "pre_architecture": pre_architecture,
        "user_constraints": user_constraints if user_constraints else "Sin restricciones especificadas"
        })


def review_architecture(pre_architecture, architecture, query, llm) ->ReviewArchitecture:
    """
    Evalúa la arquitectura generada y detecta problemas de diseño.

    Revisa consistencia, escalabilidad, coherencia con los requerimientos
    y posibles casos de sobreingeniería o decisiones incorrectas.
    """
    chain = build_chain(llm, prompt=REVIEWER_ARCHITECTURE_PROMPT, schema=ReviewArchitecture)
    
    return chain.ainvoke({
        "user_query": query,
        "pre_architecture": pre_architecture,
        "architecture": architecture
    })