from domain.schemas.documentation import Documentation
from langchain_core.prompts import PromptTemplate
from infrastructure.llm.prompts.documentation_prompt import DOCUMENTATION_PROMPT
from infrastructure.llm.chain_builder import build_chain

def generator_documentation(requirements, pre_architecture, architecture, llm) -> Documentation:
    """
    Genera la documentación final del sistema a partir de los
    requerimientos, el análisis previo de arquitectura y la
    arquitectura propuesta.
    """
    chain = build_chain(llm, prompt=DOCUMENTATION_PROMPT, schema=Documentation)
    
    return chain.ainvoke({
        "requirements": requirements,
        "pre_architecture": pre_architecture,
        "architecture": architecture
    })