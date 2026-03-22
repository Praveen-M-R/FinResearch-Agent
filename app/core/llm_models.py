from typing import Any

from app.core.config import settings
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai_litellm import LiteLLMModel
from pydantic_ai.models import ModelRequestParameters
from pydantic_ai_litellm import LiteLLMModelSettings
from litellm import Router
import litellm

# litellm.set_verbose = True
# litellm.log_level = "DEBUG"

ollama_model = OpenAIChatModel(
    settings.OLLAMA_MODEL,
    provider=OllamaProvider(base_url=settings.OLLAMA_HOST_URL),
)

GEMINI_RPM = 15
GEMINI_TPM = 250000

model_list = [
    {
        "model_name": "gemini",  # logical name your app calls
        "litellm_params": {
            "model": "gemini/gemini-3.1-flash-lite-preview",
            "api_key": settings.GOOGLE_API_KEY_1,  # Project 1
        },
        "rpm": GEMINI_RPM,
        "tpm": GEMINI_TPM,
        "model_info": {"id": "gemini-key-1"},  # unique ID for tracking
    },
    {
        "model_name": "gemini",
        "litellm_params": {
            "model": "gemini/gemini-3.1-flash-lite-preview",
            "api_key": settings.GOOGLE_API_KEY_2,  # Project 2
        },
        "rpm": GEMINI_RPM,
        "tpm": GEMINI_TPM,
        "model_info": {"id": "gemini-key-2"},
    },
]


class LiteLLMRouterModel(LiteLLMModel):
    """A LiteLLMModel that routes requests through a litellm.Router
    for load-balancing and failover across multiple API keys."""

    def __init__(self, router_instance: Router, model_name: str = "gemini"):
        super().__init__(model_name=model_name)
        self._router = router_instance

    async def _completion_create(
        self,
        messages: list[Any],
        stream: bool,
        model_settings: LiteLLMModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> Any:
        tools = self._get_tools(model_request_parameters)

        tool_choice: str | None = None
        if tools:
            if not model_request_parameters.allow_text_output:
                tool_choice = "required"
            else:
                tool_choice = "auto"

        litellm_messages = await self._map_messages(messages)

        completion_kwargs: dict[str, Any] = {
            "model": self._model_name,
            "messages": litellm_messages,
            "stream": stream,
        }

        if tools:
            completion_kwargs["tools"] = tools
            if tool_choice:
                completion_kwargs["tool_choice"] = tool_choice

        if max_tokens := model_settings.get("max_tokens"):
            completion_kwargs["max_tokens"] = max_tokens

        if temperature := model_settings.get("temperature"):
            completion_kwargs["temperature"] = temperature

        if top_p := model_settings.get("top_p"):
            completion_kwargs["top_p"] = top_p

        if timeout := model_settings.get("timeout"):
            completion_kwargs["timeout"] = timeout

        # Delegate to the Router instead of litellm.acompletion
        return await self._router.acompletion(**completion_kwargs)


litellm_router = Router(
    model_list=model_list,
    routing_strategy="usage-based-routing-v2",
    fallbacks=[{"gemini": ["gemini"]}],
    allowed_fails=1,
    cooldown_time=60,
    retry_policy={
        "RateLimitErrorRetries": 3,
        "TimeoutErrorRetries": 2,
    },
    num_retries=3,
    timeout=30,
)

# Pydantic AI-compatible model backed by the LiteLLM Router
gemini_model = LiteLLMRouterModel(router_instance=litellm_router, model_name="gemini")
