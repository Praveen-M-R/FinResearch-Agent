from fastapi import APIRouter, HTTPException
from pydantic_ai import Agent
from app.core.llm_models import ollama_model
from app.api.v1.types import ChatRequest, ChatResponse
from app.agent_tools.web_search import duckduckgo_tool
import time

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
        print(f"Time: {end_time - start_time} seconds, For {request.message}")

    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(
            status_code=500,
            detail="We are facing some issues. Please try again later.",
        )

    return ChatResponse(message=result.output, status="success")
