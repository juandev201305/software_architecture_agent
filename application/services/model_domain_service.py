from domain.schemas.model_domain import ModelDomain
from langchain_core.prompts import PromptTemplate
from infrastructure.llm.prompts.model_domain_prompt import MODEL_DOMAIN_PROMPT
from infrastructure.llm.chain_builder import build_chain

def generator_model_domain(requirements, llm) -> ModelDomain:
    """
    Construye el modelo de dominio del sistema a partir de los requerimentos.

    Identifica entidades principales del sistema y define sus relaciones,
    sirviendo como base para el diseño del modelo de datos y la arquitectura.
    """
    chain = build_chain(llm, prompt=MODEL_DOMAIN_PROMPT, schema=ModelDomain)
    
    return chain.ainvoke({"requirements": requirements})