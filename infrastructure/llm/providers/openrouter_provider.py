from langchain_openai import ChatOpenAI
from .base import LLMProvider

class OpenRouterProvider(LLMProvider):
    """
    Implementación del LLMProvider para OpenRouter usando ChatOpenAI.
    """
    
    def __init__(self, api_base: str, model: str):
        self.api_base = api_base
        self.model = model
    
    def get_chat_model(self, temperature: float = 0.0):
        """
        Retorna una instancia de ChatOpenAI configurada para OpenRouter.
        """
        return ChatOpenAI(
            model=self.model,
            temperature=temperature,
            openai_api_base=self.api_base
        )