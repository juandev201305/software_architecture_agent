from langchain_core.prompts import PromptTemplate
from infrastructure.llm.prompts.requirements_prompt import REQUIREMENTS_PROMPT, QUERY_REFINEMENT_PROMPT
from domain.schemas.requirements import Requirements, RequirementsRefinement
from infrastructure.llm.chain_builder import build_chain

def refine_query(query: str, llm) -> RequirementsRefinement:
    """
    Refina una consulta del usuario en una descripción clara y estructurada del sistema.

    Toma una entrada en lenguaje natural y la transforma en una única query más
    precisa y desambiguada, manteniendo la intención original del usuario.

    Esta query refinada se utiliza como entrada para el flujo de generación
    de requerimientos y arquitectura del sistema.
    """
    chain = build_chain(llm, prompt=QUERY_REFINEMENT_PROMPT, schema=RequirementsRefinement)
    return chain.ainvoke({"query": query})


def generator_requirements(query: str, llm) -> Requirements:
    """
    Extrae y estructura los requerimientos funcionales y no funcionales
    a partir de una descripción en lenguaje natural del sistema.

    Usa un LLM con salida estructurada para convertir el input en un objeto Requirements.
    """
    chain = build_chain(llm, prompt=REQUIREMENTS_PROMPT, schema=Requirements)

    return chain.ainvoke({"query": query})