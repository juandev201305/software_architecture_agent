import logging
from application.services.requirements_service import refine_query
from application.services.query_evaluator_service import query_evaluator
from application.services.query_evaluator_service import enricher_query

logger = logging.getLogger(__name__)

# Refinar la solicitud del usuario
async def run_requirements_refinement(query: str, llm) -> dict:
     # Estado inicial
    state = {
        "request_information": None,
        "requirements_refined": None,
        "errors": []
    }

    try:
        # Evaluar si la solicitud contiene suficiente información
        evaluator = await query_evaluator(query, llm)
        state["request_information"] = evaluator
        # Solicitar aclaraciones cuando existan ambigüedades o falten requisitos
        if evaluator.requires_more_information:
            return state
    except Exception as e:
        logger.exception("Error reviewing architecture")
        state["errors"].append(("architecture-review", str(e)))
    
    try:
        # Enriquecer la consulta utilizando el contexto proporcionado por el usuario
        query_enricher = await enricher_query(query, llm)
    except Exception as e:
        logger.exception("Error reviewing architecture")
        state["errors"].append(("architecture-review", str(e)))
    
    try:
        # Construir una especificación refinada para las siguientes etapas
        requirements_refined = await refine_query(query_enricher, llm)
        state["requirements_refined"] = requirements_refined
    except Exception as e:
        logger.exception("Error reviewing architecture")
        state["errors"].append(("architecture-review", str(e)))
        
    return state