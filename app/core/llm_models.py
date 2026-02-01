from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from app.core.config import settings
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.models.openai import OpenAIChatModel

# Initialize Ollama model (used by the agent)
try:
    ollama_model = OpenAIChatModel(
        settings.OLLAMA_MODEL,
        provider=OllamaProvider(base_url=settings.OLLAMA_HOST_URL),
    )
except Exception as e:
    print(f"Warning: Failed to initialize Ollama model: {e}")
    ollama_model = None

# Initialize Google models only if API key is available
gemini_2_5_model = None
gemini_2_0_model = None
gemini_3_flash_preview_model = None
gemini_flash_lite_model = None

if settings.GOOGLE_GENAI_API_KEY:
    try:
        gemini_2_5_model = GoogleModel(
            "gemini-2.5-flash",
            provider=GoogleProvider(api_key=settings.GOOGLE_GENAI_API_KEY),
        )

        gemini_2_0_model = GoogleModel(
            "gemini-2.0-flash",
            provider=GoogleProvider(api_key=settings.GOOGLE_GENAI_API_KEY),
        )

        gemini_3_flash_preview_model = GoogleModel(
            "gemini-3-flash-preview",
            provider=GoogleProvider(api_key=settings.GOOGLE_GENAI_API_KEY),
        )

        gemini_flash_lite_model = GoogleModel(
            "gemini-flash-lite-latest",
            provider=GoogleProvider(api_key=settings.GOOGLE_GENAI_API_KEY),
        )
    except Exception as e:
        print(f"Warning: Failed to initialize Google models: {e}")
