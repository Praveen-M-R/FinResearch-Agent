from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from app.core.config import settings


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
