from application.workflow.requirements_elicitation_workflow import run_requirements_refinement
from application.workflow.architecture_workflow import run_arquitecture
from application.workflow.documentation_workflow import run_documentation
from infrastructure.llm.llm_factory import get_llm
from application.utils.documentation_formatter import formatter_document
import logging 

logger = logging.getLogger(__name__)

async def arun_agent(query) -> dict:
    global_state = {
        "request_information": None,
        "architecture": None,
        "documentation": None
    }

    try:
        # Inicializa cliente LLM.
        # Puede fallar por configuración inválida o problemas de API key.
        llm = get_llm()
    except Exception as e:
        logger.exception("Error get_llm", str(e))
        return {"error": "error in obtaining the llm"}

    requirements_refined = await run_requirements_refinement(query, llm)
    global_state["request_information"] = requirements_refined["request_information"]
    if requirements_refined["request_information"].requires_more_information:
        return global_state

    architecture = await run_arquitecture(requirements_refined, llm)
    global_state["architecture"] = architecture

    documentation = await run_documentation(architecture, llm)
    global_state["documentation"] = formatter_document(documentation)
    
    return global_state