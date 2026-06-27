from pydantic import BaseModel, Field
from typing import List

# Representar la documentación final del sistema generada a partir del pipeline de análisis de requisitos y arquitectura.
class Documentation(BaseModel):
    project_overview: str = Field(description="Resumen general del sistema, su propósito y el valor que entrega.")
    problem_statement: str = Field(description="Descripción clara del problema que el sistema resuelve.")
    requirements_summary: str = Field(description="Resumen estructurado de los requerimientos funcionales y no funcionales principales.")
    domain_summary: str = Field(description="Descripción del dominio del problema, incluyendo entidades y conceptos clave.")
    architecture_overview: str = Field(description="Descripción de alto nivel de la arquitectura propuesta.")
    architecture_pattern: str = Field(description="Estilo o patrón arquitectónico seleccionado (ej: microservicios, monolito, etc.).")
    key_components: List[str] = Field(description="Componentes principales del sistema (servicios, módulos o capas relevantes).")
    technology_stack: List[str] = Field(description="Tecnologías seleccionadas para implementar la solución.")
    design_decisions: List[str] = Field(description="Decisiones arquitectónicas importantes y su justificación resumida.")
    constraints_and_tradeoffs: List[str] = Field(description="Restricciones del sistema y compromisos realizados en el diseño.")
    risks_and_considerations: List[str] = Field(description="Riesgos técnicos o de negocio identificados en la solución.")
    final_summary: str = Field(description="Conclusión general del sistema y su arquitectura.")