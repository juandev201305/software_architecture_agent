from langchain_core.prompts import PromptTemplate
from infrastructure.llm.prompts.use_cases_prompt import USE_CASES_PROMPT
from domain.schemas.use_cases import UseCases
from infrastructure.llm.chain_builder import build_chain

def generator_use_cases(model_domain, llm) -> UseCases:
    """
    Genera los casos de uso del sistema a partir del modelo de dominio.

    Traduce las entidades y relaciones del dominio en interacciones concretas
    entre actores y el sistema, definiendo qué funcionalidades existen desde
    la perspectiva del usuario.
    """
    chain = build_chain(llm, prompt=USE_CASES_PROMPT, schema=UseCases)

    return chain.ainvoke({"model_domain": model_domain})