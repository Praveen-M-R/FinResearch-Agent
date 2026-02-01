import time
from fastapi import APIRouter, HTTPException
from pydantic_ai import Agent
from app.core.llm_models import ollama_model
from app.api.v1.types import ChatRequest, ChatResponse
from app.agent_tools.news_search import financial_news_tool
from app.api.v1.utils import print_agent_execution_steps

router = APIRouter(prefix="/agent")


@router.post("/chat")
def run_agent(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        model = ollama_model
        agent = Agent(
            model,
            instructions="Be Professional!",
            tools=[financial_news_tool],
        )
        start_time = time.time()
        result = agent.run_sync(request.message)
        end_time = time.time()
        print(f"Tokens: {result.usage()}")
        print(f"Thinking part: {result}")
        print(
            f"Time: {end_time - start_time} seconds, For {request.message[:10]} with model {model.model_name}\n"
        )
        print_agent_execution_steps(result)

    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(
            status_code=500,
            detail="We are facing some issues. Please try again later.",
        )

    return ChatResponse(message=result.output, status="success")
