from langchain_core.prompts import PromptTemplate
from infrastructure.llm.prompts.architecture_prompt import ARCHITECTURE_PROMPT, PRE_ARCHITECTURE_PROMPT, REVIEWER_ARCHITECTURE_PROMPT, SIMPLIFICATION_PROMPT, ENRICHER_PROMPT
from domain.schemas.archistecture import PreArchitecture, Architecture, ReviewArchitecture, SimplificationReview, EnrichmentReview
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


def generator_architecture(pre_architecture, llm, user_constraints: str = None, feedback= None) -> Architecture:
    """
    Convierte la pre-arquitectura en una arquitectura técnica concreta.

    Define patrones de diseño, tecnologías y estructura de alto nivel del sistema
    basándose en la visión inicial generada en la etapa anterior.
    """
    chain = build_chain(llm, prompt=ARCHITECTURE_PROMPT, schema=Architecture)

    feedback_context = ""
    
    if isinstance(feedback, SimplificationReview):
        feedback_context = f"SIMPLIFICACION REQUERIDA:\n{feedback}"
    elif isinstance(feedback, EnrichmentReview):    
        feedback_context = f"ENRIQUECIMIENTO REQUERIDO:\n{feedback}"

    return chain.ainvoke({
        "pre_architecture": pre_architecture,
        "user_constraints": user_constraints if user_constraints else "Sin restricciones especificadas",
        "architecture_feedback": feedback_context if feedback else "No hay feedback previo"
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

def simplify_review(llm, reviewer_architecture, architecture_refuse):
    """
    Extrae restricciones de simplificación a partir del feedback del reviewer.
    Se activa cuando la arquitectura fue marcada como sobreingeniería,
    guiando al agente de arquitectura hacia una propuesta más simple.
    """
    chain = build_chain(llm, prompt=SIMPLIFICATION_PROMPT, schema=SimplificationReview)
    
    return chain.ainvoke({
        "review": reviewer_architecture,
        "architecture": architecture_refuse
    })

def enricher_review(llm, reviewer_architecture, architecture_refuse):
    """
    Extrae restricciones de enriquecimiento a partir del feedback del reviewer.
    Se activa cuando la arquitectura fue marcada como insuficiente,
    guiando al agente de arquitectura a incorporar las capacidades faltantes.
    """
    chain = build_chain(llm, prompt=ENRICHER_PROMPT, schema=EnrichmentReview)
    
    return chain.ainvoke({
        "review": reviewer_architecture,
        "architecture": architecture_refuse
    })