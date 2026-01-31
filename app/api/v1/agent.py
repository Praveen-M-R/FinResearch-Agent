from fastapi import APIRouter, Form, HTTPException
from pydantic_ai import Agent
from app.core.llm_models import gemini_2_5_model, gemini_2_0_model
from app.api.v1.types import ChatRequest, ChatResponse

router = APIRouter(prefix="/agent")


@router.post("/chat")
def run_agent(
    request: ChatRequest,
):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    finresearch_agent = Agent(gemini_2_5_model, instructions="Be Professional!")
    response = finresearch_agent.run_sync(request.message)

    # Return JSON response with markdown content
    return ChatResponse(message=response.output, status="success")
