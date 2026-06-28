from pydantic import BaseModel, Field
from domain.schemas.requirements import Requirements
from domain.schemas.model_domain import ModelDomain
from domain.schemas.use_cases import UseCases
from typing import List

# Contexto previo al diseño arquitectonico
class PreArchitecture(BaseModel):
    system_purpose: str  = Field(description="Propósito principal del sistema y el valor que entrega al negocio.")
    business_problem: str = Field(description="Problema de negocio que el sistema busca resolver.")
    actors: list[str] = Field(description="Actores, usuarios o sistemas externos que interactúan con la solución.")
    core_capabilities: list[str] = Field(description="Capacidades principales que el sistema debe proporcionar a sus usuarios.")
    domain_entities: list[str] = Field(description="Entidades relevantes que forman parte del dominio del problema.")
    business_rules: list[str] = Field(description="Reglas de negocio que deben respetarse durante la operación del sistema.")
    constraints: list[str] = Field(description="Restricciones que condicionan o limitan las decisiones arquitectónicas.")
    assumptions: list[str] = Field(description="Supuestos realizados debido a información incompleta o ambigua.")
    risks: list[str] = Field(description="Riesgos identificados que podrían afectar el diseño o implementación.")


# Elementos utilizados para describir una arquictetura
class Layer(BaseModel):
    name: str = Field(description="Nombre de la capa arquitectónica.")
    responsibility: str = Field(description="Responsabilidad principal de la capa.")
class Technology(BaseModel):
    name: str = Field(description="Nombre de la tecnología propuesta.")
    purpose: str = Field(description="Motivo de uso dentro de la arquitectura.")
    layer: str = Field(description="Capa donde se utiliza la tecnología.")
class Decision(BaseModel):
    decision: str = Field(description="Decisión arquitectónica tomada.")
    justification: str = Field(description="Razón que justifica la decisión.")

# Arquitectura propuesta para el sistema
class Architecture(BaseModel):
    pattern: str = Field(description="Patrón o estilo arquitectónico seleccionado para organizar el sistema.")
    layers: List[Layer] = Field(description="Capas arquitectónicas que componen la solución.")
    technologies: List[Technology] = Field(description="Tecnologías seleccionadas para materializar las decisiones arquitectónicas.")
    decisions: List[Decision] = Field(description="Decisiones arquitectónicas tomadas junto a su justificación.")
    risks: List[str] = Field(description="IRiesgos, limitaciones o desafíos asociados a la arquitectura propuesta.")


# Evaluación y observaciones sobre la arquitectura generada
class ReviewArchitecture(BaseModel):
    score : int = Field(description="Puntuación general de la arquitectura considerando adecuación, simplicidad y calidad técnica.")
    strengths: List[str] = Field(description="Aspectos positivos y fortalezas detectadas en la arquitectura propuesta.")
    observations: List[str] = Field(description="Observaciones relevantes que el arquitecto debe considerar.")
    critical_issues: List[str] = Field(description="Problemas criticos de la arquitectura")
    recommendations: List[str] = Field(description="Recomendaciones de mejora para fortalecer la arquitectura.")
    detected_overengineering: bool = Field(description="Indica si la arquitectura incorpora complejidad innecesaria para el problema planteado.")
    detected_underengineering: bool = Field(description="Indica si la solución es insuficiente para el problema")
    alignment_summary: str = Field(description="Conclusión ejecutiva sobre la coherencia y adecuación de la arquitectura respecto al problema de negocio, requisitos y contexto analizado.")

# Área de la arquitectura que debe simplificarse
class SimplificationConstraint(BaseModel):
    area: str = Field(description="Área afectada: 'tecnologia', 'capas', 'patrones', 'infraestructura'.")
    original: str = Field(description="Decisión original que debe simplificarse.")
    reason: str = Field(description="Por qué debe simplificarse según el reviewer.")
    
# Resultado del análisis de simplificación para guiar la re-arquitectura
class SimplificationReview(BaseModel):
    simplification_constraints: List[SimplificationConstraint] = Field(description="Restricciones derivadas del feedback del reviewer para guiar la re-arquitectura.")
    max_complexity_allowed: str = Field(description="Complejidad máxima permitida para la nueva propuesta. Ej: 'app monolítica', 'script con UI simple', 'API mínima con una BD embebida'.")
    must_keep: List[str] = Field(default_factory=list,description="Decisiones de la arquitectura original que sí deben mantenerse.")

# Restricción de enriquecimiento derivada del feedback del reviewer
class EnrichmentConstraint(BaseModel):
    area: str = Field(description="Área afectada: 'tecnologia', 'capas', 'patrones', 'infraestructura'.")
    missing: str = Field(description="Capacidad o decisión ausente en la arquitectura actual.")
    reason: str = Field(description="Por qué es necesaria según el reviewer.")

# Resultado del análisis de enriquecimiento para guiar la re-arquitectura
class EnrichmentReview(BaseModel):
    enrichment_constraints: List[EnrichmentConstraint] = Field(description="Capacidades o decisiones faltantes que deben incorporarse en la siguiente iteración.")
    min_complexity_required: str = Field(description="Complejidad mínima necesaria para cubrir las capacidades requeridas. Ej: 'API REST con lógica de negocio explícita', 'servicio de notificaciones asíncrono'.")
    must_keep: List[str] = Field(default_factory=list, description="Decisiones de la arquitectura original que sí deben mantenerse.")