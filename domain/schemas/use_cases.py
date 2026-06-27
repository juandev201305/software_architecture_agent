from pydantic import BaseModel, Field
from typing import List

# Actor del sistema (usuario o entidad externa)
class Actor(BaseModel):
    name: str

# Representar un caso de uso funcional del sistema
class UseCase(BaseModel):
    actor: Actor = Field(description="Actor que participa en el caso de uso.")
    objective: str = Field(description="Objetivo que busca alcanzar el actor.")
    basic_flow: str = Field(description="Secuencia principal de pasos para completar el caso de uso.")
    alternative_flow: str | None = Field(description="Flujos alternativos o excepciones que pueden ocurrir.")
    precondition: str = Field(description="Condición que debe cumplirse antes de iniciar el caso de uso.")
    postcondition: str = Field(description="Estado esperado del sistema al finalizar el caso de uso.")

# Conjunto de casos de uso del sistema
class UseCases(BaseModel):
    use_cases: List[UseCase] = Field(description="Conjunto de casos de uso principales del sistema.")
