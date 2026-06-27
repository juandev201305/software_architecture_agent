from pydantic import BaseModel, Field
from typing import Literal, List

# Representar una relación entre dos entidades del dominio
class Relationship(BaseModel):
    source_entity: str = Field(description="Entidad origen de la relación.")
    target_entity: str = Field(description="Entidad destino de la relación.")
    cardinality: Literal[
        "Many-To-Many",
        "One-To-Many",
        "One-To-One",
        "Many-To-One"
    ] = Field(description="Cardinalidad entre las entidades.")
    description: str = Field(description="Descripción funcional de la relación dentro del dominio.")

# Entidad principal del modelo de dominio
class Entity(BaseModel):
    name: str = Field(description="Nombre de la entidad del dominio.")
    description: str = Field(description="Propósito o significado de la entidad dentro del dominio.")
    attributes: List[str] = Field(description="Datos relevantes que describen a la entidad.")
    behaviors: List[str] = Field(description="Acciones o comportamientos asociados a la entidad.")

# Modelo de dominio completo del sistema
class ModelDomain(BaseModel):
    entities: List[Entity] = Field(description="Entidades principales del dominio.")
    relations: List[Relationship] = Field(description="Relaciones identificadas entre las entidades del dominio.")
    business_rules: List[str] = Field(description="Reglas de negocio que deben cumplirse dentro del dominio.")
    domain_events: List[str] = Field(description="Eventos relevantes que representan cambios importantes dentro del dominio.")

