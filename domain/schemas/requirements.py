from pydantic import BaseModel, Field
from typing import List

# Representar la consulta refinada del usuario y sus restricciones asociadas.
class RequirementsRefinement(BaseModel):
    final_query: str = Field(description="Consulta refinada del sistema.")
    constraints: List[str] = Field(description="Restricciones explícitas declaradas por el usuario.")
    context_constraints: List[str] = Field(default_factory=list, description="Restricciones derivadas del contexto inferido. Ej: 'Máximo 2 usuarios simultáneos'.")
    business_context: str = Field(default="", description="Contexto operacional trasladado desde QueryEnricher.")

# Representa el análisis estructurado de requerimientos de un sistema
class Requirements(BaseModel):
    summary: str = Field(description="Explica brevemente lo que quiere el usuario.")
    system_goal: str = Field(description="Describe el proposito principal del software.")
    actors: List[str] = Field(description="Identifica usuarios, administradores, sistemas externos u otros actores.")
    functional_requiments: List[str] = Field(description="Lista numerada de funcionalidades concreta usa el siguiente formato: -RF-001 ... RF-002 ...")
    no_functional_requirements: List[str] = Field(description="Requerimentos no funcionales(rendimiento, seguridad, escalabilidad, disponibilidad u otros).")
    main_use_cases: List[str] = Field(description="Flujos mas importantes que el sistema debe soportar.")
    assumptions: List[str] = Field(description="Identifica supuestos realizados.")