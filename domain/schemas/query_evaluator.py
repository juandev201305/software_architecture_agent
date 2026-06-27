from pydantic import BaseModel, Field
from typing import List

class ContextAssumption(BaseModel):
    category: str = Field(description="Categoría: 'escala', 'usuarios', 'madurez_tecnica', 'contexto_negocio'.")
    assumption: str = Field(description="Supuesto inferido desde la consulta.")
    confidence: str = Field(description="Confianza: 'alta', 'media', 'baja'.")

# Preguntas de aclaración utilizadas para completar información faltante
class Question(BaseModel):
     name: str = Field(description="Pregunta de aclaración que debe responder el usuario para completar los requisitos faltantes.")
     alternative_answer: List[str] = Field(max_length=3, description="Lista de respuestas sugeridas para facilitar la elección del usuario. Máximo 3 alternativas.")

# Resultado de la evaluación inicial de la solicitud del usuario
class QueryEvaluator(BaseModel):
     requires_more_information: bool = Field(description="Indica si la solicitud del usuario carece de información suficiente para generar una especificación o requerimiento completo.")
     clarification_questions: list[Question] = Field(default_factory=list, description="Conjunto de preguntas que deben realizarse al usuario para obtener la información faltante.")
     inferred_assumptions: List[ContextAssumption] = Field(default_factory=list, description="Obligatorio cuando requires_more_information es False. Escala, usuarios, madurez técnica y contexto del negocio.")

# Consulta enriquecida que servirá como entrada para las siguientes etapas del proceso
class QueryEnricher(BaseModel):
    query: str = Field(description="Consulta enriquecida y reformulada sin ambigüedades.")
    context_summary: str = Field(description="Contexto operacional: tipo de negocio, perfil de usuario, escala y restricciones inferidas.")
    assumptions: List[ContextAssumption] = Field(default_factory=list, description="Supuestos trasladados intactos desde QueryEvaluator.")
