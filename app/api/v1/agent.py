from fastapi import APIRouter, HTTPException
from pydantic_ai import Agent
from app.core.llm_models import ollama_model
from app.api.v1.types import ChatRequest, ChatResponse

router = APIRouter(prefix="/agent")


@router.post("/chat")
def run_agent(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        agent = Agent(ollama_model, instructions="Be Professional!")
        result = agent.run_sync(request.message)

    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(
            status_code=500,
            detail="We are facing some issues. Please try again later.",
        )

    return ChatResponse(message=result.output, status="success")
