from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """
    Contrato base para proveedores de LLM.

    Permite abstraer la creación del modelo de chat para no depender
    de una implementación específica (OpenAI, OpenRouter, etc.).
    """

    @abstractmethod
    def get_chat_model(self, temperature: float = 0.0):
        """
        Retorna un modelo de chat listo para usar.
        """
        pass