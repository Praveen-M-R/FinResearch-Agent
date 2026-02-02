from app.core.config import settings
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.models.openai import OpenAIChatModel

ollama_model = OpenAIChatModel(
    settings.OLLAMA_MODEL,
    provider=OllamaProvider(base_url=settings.OLLAMA_HOST_URL),
)
