import logging
import sys
import json
import time
from fastapi import APIRouter, HTTPException
from pydantic_ai import Agent
from pydantic_ai.messages import ModelRequest, ModelResponse, ToolReturnPart
from app.core.llm_models import ollama_model
from app.api.v1.types import ChatRequest, ChatResponse
from app.agent_tools.web_search import duckduckgo_tool

# 1. Setup Logging to see internal library logs (PydanticAI, HTTPX, etc.)
# This will print every HTTP request sent to Ollama and internal debug info.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Optional: Reduce noise from other libraries if needed
logging.getLogger("httpcore").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)

router = APIRouter(prefix="/agent")


@router.post("/chat")
def run_agent(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        agent = Agent(
            ollama_model,
            instructions="Be Professional!",
            tools=[duckduckgo_tool],
        )
        start_time = time.time()
        result = agent.run_sync(request.message)
        end_time = time.time()
        print(f"Tokens: {result.usage()}")
        print(
            f"Time: {end_time - start_time} seconds, For {request.message[:10]} with model {ollama_model.model_name}"
        )

    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(
            status_code=500,
            detail="We are facing some issues. Please try again later.",
        )

    return ChatResponse(message=result.output, status="success")
