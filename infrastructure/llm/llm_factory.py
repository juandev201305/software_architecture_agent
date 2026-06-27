from infrastructure.llm.providers.openrouter_provider import OpenRouterProvider
from config.models import LLM_MODEL
from config.setting import OPENROUTER_API

# Obtener modelo LLM
def get_llm(temperature=0.0):
    provider = OpenRouterProvider(
        api_base=OPENROUTER_API,
        model=LLM_MODEL
    )

    return provider.get_chat_model(temperature)
