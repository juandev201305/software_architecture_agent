import logging
from infrastructure.llm.llm_factory import get_llm
from application.services.requirements_service import generator_requirements
from application.services.model_domain_service import generator_model_domain
from application.services.use_cases_service import generator_use_cases
from application.services.architecture_service import generator_architecture, generator_pre_architecture, review_architecture, simplify_review, enricher_review

logger = logging.getLogger(__name__)

async def run_arquitecture(requirements_refined, llm)-> dict:
  # Estado inicial
  state = {
      "requirements": None,
      "model_domain": None, 
      "use_cases": None,
      "pre-architecture":  None,
      "architecture": None,
      "architecture-review": None,
      "errors": []
  }

  try:
    # Conviertir la idea del usuario en requisitos claros del sistema
    requirements = await generator_requirements(requirements_refined["requirements_refined"].final_query,llm)
    state["requirements"] = requirements
  except Exception as e:
    logger.exception("Error generating requirements")
    state["errors"].append(("requirements", str(e)))
    return state

  try:
    # Identificar entidades del sistema y cómo se relacionan
    model_domain = await generator_model_domain(requirements, llm)
    state["model_domain"] = model_domain
  except Exception as e:
    logger.exception("Error generating model domain")
    state["errors"].append(("model_domain", str(e)))
    return state

  try:
    # Definir qué pueden hacer los usuarios dentro del sistema
    use_cases = await generator_use_cases(model_domain, llm)
    state["use_cases"] = use_cases
  except Exception as e:
    logger.exception("Error generating use cases")
    state["errors"].append(("use_cases", str(e)))
    return state

  try: 
    # Traducir todo a una visión general del sistema y sus restricciones
    pre_architecture = await generator_pre_architecture(requirements, model_domain, use_cases, llm)
    state["pre-architecture"] = pre_architecture
  except Exception as e:
    logger.exception("Error generating pre-architecture")
    state["errors"].append(("pre-architecture", str(e)))
    return state

  # Límite de iteraciones y estado inicial del loop
  MAX_ITERATIONS = 3
  iteration = 0
  previous_score = 0
  architecture_feedback = None
  re_run = True
  while re_run and iteration<MAX_ITERATIONS:
    try:
      # Generar la arquitectura considerando feedback de iteraciones anteriores
      architecture = await generator_architecture(pre_architecture, llm, requirements_refined["requirements_refined"].constraints, architecture_feedback)
      state["architecture"] = architecture
    except Exception as e:
      logger.exception("Error generating architecture")
      state["errors"].append(("architecture", str(e)))
      return state  

    try:
      # Revisar si la arquitectura tiene problemas o está sobrediseñada
      reviewer_architecture = await review_architecture(pre_architecture, architecture, requirements_refined["requirements_refined"].final_query, llm)
      state["architecture-review"] = reviewer_architecture
      re_run = True if reviewer_architecture.detected_overengineering or reviewer_architecture.score<7 else False
    except Exception as e:
      logger.exception("Error reviewing architecture")
      state["errors"].append(("architecture-review", str(e)))
      return state  
    
    # Cortar el loop si el score no mejoró respecto a la iteración anterior
    if reviewer_architecture.score <= previous_score and iteration > 0:
      logger.info(f"Score no mejoró ({previous_score} → {reviewer_architecture.score}), saliendo del loop")
      break

    previous_score = reviewer_architecture.score

    # Clasificar el tipo de problema detectado por el reviewer
    over = reviewer_architecture.detected_overengineering
    under = reviewer_architecture.detected_underengineering
    has_criticals = len(reviewer_architecture.critical_issues) > 0

    if over:
      # Extraer restricciones para simplificar la arquitectura
      architecture_feedback = await simplify_review(llm, reviewer_architecture, architecture)
    elif under or has_criticals:
      # Extraer capacidades faltantes para enriquecer la arquitectura
      architecture_feedback = await enricher_review(llm, reviewer_architecture, architecture)

    re_run = over or under or has_criticals
    iteration += 1

  return state
