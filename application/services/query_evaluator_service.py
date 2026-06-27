from domain.schemas.query_evaluator import QueryEvaluator, QueryEnricher
from langchain_core.prompts import PromptTemplate
from infrastructure.llm.prompts.query_evaluator_prompt import QUERY_EVALUATOR_PROMPT, QUERY_ENRICHER_PROMPT
from infrastructure.llm.chain_builder import build_chain

def query_evaluator(query, llm) -> QueryEvaluator:
    """
    Evalúa la calidad y completitud de la consulta proporcionada por el usuario.

    Esta etapa analiza si la información entregada es suficiente para continuar
    con el proceso de generación arquitectónica o si es necesario solicitar
    aclaraciones adicionales.
    """
    chain = build_chain(llm, prompt=QUERY_EVALUATOR_PROMPT, schema=QueryEvaluator)

    return chain.ainvoke({"query": query})

def enricher_query(query, llm) -> QueryEnricher:
    """
    Enriquece la consulta original generando contexto adicional y preguntas
    complementarias cuando la información proporcionada es insuficiente.

    Su objetivo es reducir ambigüedades y construir una especificación más
    completa antes de las etapas de análisis y diseño arquitectónico.
    """
    chain = build_chain(llm, prompt=QUERY_ENRICHER_PROMPT, schema=QueryEnricher)

    return chain.ainvoke({"query": query})
    
    